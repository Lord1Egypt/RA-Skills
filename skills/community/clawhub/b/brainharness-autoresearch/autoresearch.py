#!/usr/bin/env python3
"""
autoresearch.py - Autonomous skill prompt optimizer.

Based on Karpathy's autoresearch methodology: iteratively mutate a SKILL.md
prompt, evaluate outputs against a suite of evals, keep improvements, revert
regressions, and converge toward a high-scoring prompt.

Requirements: Python 3.9+, zero external dependencies (stdlib only).
"""

import argparse
import copy
import datetime
import hashlib
import json
import os
import re
import shutil
import ssl
import sys
import time
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# LLM Providers
# ---------------------------------------------------------------------------

class LLMProvider(ABC):
    """Base class for LLM API providers."""

    def __init__(self, api_key: str, verbose: bool = False, timeout: int = 180):
        self.api_key = api_key
        self.verbose = verbose
        self.timeout = timeout

    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def call(self, system: str, user: str, temperature: float = 0.7,
             max_tokens: int = 4096) -> str:
        """Send a chat request and return the assistant text."""
        ...

    def _http_post(self, url: str, headers: dict, body: dict,
                   timeout: int = 0) -> dict:
        if timeout <= 0:
            timeout = self.timeout
        """Low-level POST via urllib.  Retries once on timeout/5xx."""
        data = json.dumps(body).encode("utf-8")
        for attempt in range(2):
            req = urllib.request.Request(url, data=data, headers=headers,
                                        method="POST")
            try:
                ctx = ssl.create_default_context()
                with urllib.request.urlopen(req, timeout=timeout,
                                           context=ctx) as resp:
                    raw = resp.read().decode("utf-8")
                    if self.verbose:
                        _log_verbose(f"[{self.name()}] HTTP {resp.status}")
                        _log_verbose(raw[:2000])
                    return json.loads(raw)
            except urllib.error.HTTPError as exc:
                body_text = ""
                try:
                    body_text = exc.read().decode("utf-8", errors="replace")
                except Exception:
                    pass
                if attempt == 0 and exc.code >= 500:
                    _log_err(f"[{self.name()}] HTTP {exc.code}, retrying...")
                    time.sleep(2)
                    continue
                raise RuntimeError(
                    f"[{self.name()}] HTTP {exc.code}: {body_text[:500]}"
                ) from exc
            except (urllib.error.URLError, OSError, TimeoutError) as exc:
                if attempt == 0:
                    _log_err(f"[{self.name()}] request error, retrying: {exc}")
                    time.sleep(2)
                    continue
                raise RuntimeError(
                    f"[{self.name()}] request failed after retry: {exc}"
                ) from exc
        # unreachable
        raise RuntimeError(f"[{self.name()}] exhausted retries")

    @staticmethod
    def _extract_text(resp: dict, provider_name: str) -> str:
        """Extract text from Anthropic-style response, handling thinking blocks.

        Models with extended thinking (MiniMax M2.7, Claude) return content like:
          [{"type": "thinking", "thinking": "..."}, {"type": "text", "text": "..."}]
        Sometimes thinking exhausts max_tokens and no text block exists.
        """
        try:
            content = resp["content"]
            # 1. Find explicit text block
            for block in content:
                if isinstance(block, dict):
                    if block.get("type") == "text" and "text" in block:
                        return block["text"]
            # 2. Fallback: any block with a "text" key (not "thinking")
            for block in content:
                if isinstance(block, dict) and "text" in block and "thinking" not in block:
                    return block["text"]
            # 3. Last resort: if only thinking blocks exist (max_tokens exhausted),
            #    return the thinking content so the caller gets *something*
            for block in reversed(content):
                if isinstance(block, dict) and "thinking" in block:
                    _log_err(f"[{provider_name}] no text block, using thinking content as fallback")
                    return block["thinking"]
            raise KeyError("no text or thinking block found")
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(
                f"[{provider_name}] unexpected response shape: "
                f"{json.dumps(resp)[:500]}"
            ) from exc


class MiniMaxProvider(LLMProvider):
    """MiniMax via Anthropic-compatible messages endpoint."""

    MODEL = "MiniMax-M2.7-highspeed"
    URL = "https://api.minimax.io/anthropic/v1/messages"

    def name(self) -> str:
        return "minimax"

    def call(self, system: str, user: str, temperature: float = 0.7,
             max_tokens: int = 4096) -> str:
        headers = {
            "x-api-key": self.api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01",
        }
        body: Dict[str, Any] = {
            "model": self.MODEL,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": user}],
        }
        if system:
            body["system"] = system
        resp = self._http_post(self.URL, headers, body)
        return self._extract_text(resp, "minimax")


class OpenAIProvider(LLMProvider):
    """OpenAI (or compatible) chat completions."""

    MODEL = "gpt-4o-mini"

    def __init__(self, api_key: str, verbose: bool = False):
        super().__init__(api_key, verbose)
        self.base_url = (
            os.environ.get("OPENAI_BASE_URL")
            or os.environ.get("OPENAI_API_BASE")
            or "https://api.openai.com/v1"
        ).rstrip("/")

    def name(self) -> str:
        return "openai"

    def call(self, system: str, user: str, temperature: float = 0.7,
             max_tokens: int = 4096) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        messages: list = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": user})
        body = {
            "model": self.MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        resp = self._http_post(url, headers, body)
        try:
            return resp["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as exc:
            raise RuntimeError(
                f"[openai] unexpected response: {json.dumps(resp)[:500]}"
            ) from exc


class AnthropicProvider(LLMProvider):
    """Anthropic Messages API."""

    MODEL = "claude-sonnet-4-20250514"
    URL = "https://api.anthropic.com/v1/messages"

    def name(self) -> str:
        return "anthropic"

    def call(self, system: str, user: str, temperature: float = 0.7,
             max_tokens: int = 4096) -> str:
        headers = {
            "x-api-key": self.api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01",
        }
        body: Dict[str, Any] = {
            "model": self.MODEL,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": user}],
        }
        if system:
            body["system"] = system
        resp = self._http_post(self.URL, headers, body)
        return self._extract_text(resp, "anthropic")


def detect_provider(explicit: Optional[str] = None,
                    verbose: bool = False,
                    model_override: Optional[str] = None,
                    timeout: int = 180) -> LLMProvider:
    """Auto-detect or create the requested LLM provider."""
    provider: Optional[LLMProvider] = None
    if explicit:
        mapping = {
            "minimax": ("MINIMAX_API_KEY", MiniMaxProvider),
            "openai": ("OPENAI_API_KEY", OpenAIProvider),
            "anthropic": ("ANTHROPIC_API_KEY", AnthropicProvider),
        }
        if explicit not in mapping:
            _die(f"Unknown provider '{explicit}'. Choose: minimax, openai, anthropic")
        env_var, cls = mapping[explicit]
        key = os.environ.get(env_var)
        if not key:
            _die(f"Provider '{explicit}' requires {env_var} environment variable")
        provider = cls(key, verbose=verbose, timeout=timeout)
    else:
        # Auto-detect in priority order
        for env_var, cls in [
            ("MINIMAX_API_KEY", MiniMaxProvider),
            ("OPENAI_API_KEY", OpenAIProvider),
            ("ANTHROPIC_API_KEY", AnthropicProvider),
        ]:
            key = os.environ.get(env_var)
            if key:
                _log(f"Auto-detected provider: {cls.__name__} (via {env_var})")
                provider = cls(key, verbose=verbose, timeout=timeout)
                break

    if provider is None:
        _die("No LLM API key found. Set one of: MINIMAX_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY")
        raise SystemExit(1)  # unreachable, for type checker

    if model_override:
        provider.MODEL = model_override
        _log(f"Model override: {model_override}")

    return provider


# ---------------------------------------------------------------------------
# Eval System
# ---------------------------------------------------------------------------

class EvalSpec:
    """A single eval criterion loaded from eval.json."""

    def __init__(self, raw: dict):
        self.name: str = raw.get("name", "unnamed")
        self.eval_type: str = raw.get("type", "rule")  # "rule" or "llm"

        if self.eval_type == "rule":
            self.check: str = raw.get("rule", raw.get("check", ""))
            self.pattern: str = raw.get("pattern", "")
            self.phrases: List[str] = raw.get("phrases", [])
            # Support both "values" (list) and "value" (string)
            values = raw.get("values", raw.get("value", []))
            self.values: List[str] = [values] if isinstance(values, str) else values
            self.match_mode: str = raw.get("match", "any")  # "any" or "all"
            self.min_val: Optional[int] = raw.get("min")
            self.max_val: Optional[int] = raw.get("max")
        elif self.eval_type == "llm":
            self.question: str = raw.get("question", "")
            self.pass_desc: str = raw.get("pass_description", raw.get("pass", ""))
            self.fail_desc: str = raw.get("fail_description", raw.get("fail", ""))
        else:
            _die(f"Unknown eval type '{self.eval_type}' in eval '{self.name}'")

    def describe(self) -> str:
        """Human-readable description for the mutation prompt."""
        if self.eval_type == "rule":
            if self.check == "regex":
                return f"[rule:regex] {self.name}: output must match /{self.pattern}/"
            elif self.check == "banned_phrases":
                return f"[rule:banned] {self.name}: output must NOT contain: {self.phrases}"
            elif self.check == "word_count":
                parts = []
                if self.min_val is not None:
                    parts.append(f">={self.min_val}")
                if self.max_val is not None:
                    parts.append(f"<={self.max_val}")
                return f"[rule:word_count] {self.name}: word count {' and '.join(parts)}"
            elif self.check == "contains":
                return f"[rule:contains] {self.name}: output must contain one of: {self.values}"
            elif self.check == "not_contains":
                return f"[rule:not_contains] {self.name}: output must NOT contain: {self.values}"
            else:
                return f"[rule:{self.check}] {self.name}"
        else:
            return f"[llm] {self.name}: {self.question}"


class EvalRunner:
    """Runs eval checks against LLM output."""

    def __init__(self, evals: List[EvalSpec], provider: LLMProvider):
        self.evals = evals
        self.provider = provider

    def score_output(self, output: str) -> List[Tuple[EvalSpec, bool, str]]:
        """Score a single output against all evals.

        Returns list of (eval, passed, reason) tuples.
        """
        results = []
        for ev in self.evals:
            passed, reason = self._check_one(ev, output)
            results.append((ev, passed, reason))
        return results

    def _check_one(self, ev: EvalSpec, output: str) -> Tuple[bool, str]:
        """Evaluate one criterion.  Returns (passed, reason)."""
        if ev.eval_type == "rule":
            return self._check_rule(ev, output)
        else:
            return self._check_llm(ev, output)

    # -- Rule checks --

    def _check_rule(self, ev: EvalSpec, output: str) -> Tuple[bool, str]:
        check = ev.check

        if check == "regex":
            if re.search(ev.pattern, output, re.MULTILINE):
                return True, "regex matched"
            return False, f"regex /{ev.pattern}/ not found in output"

        elif check == "banned_phrases":
            lower = output.lower()
            found = [p for p in ev.phrases if p.lower() in lower]
            if found:
                return False, f"banned phrase(s) found: {found}"
            return True, "no banned phrases"

        elif check == "word_count":
            # CJK-aware: count CJK characters individually, other words by split
            cjk_count = sum(1 for c in output if '\u4e00' <= c <= '\u9fff'
                            or '\u3400' <= c <= '\u4dbf'
                            or '\uf900' <= c <= '\ufaff')
            # Remove CJK chars, count remaining by whitespace split
            non_cjk = re.sub(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]', ' ', output)
            non_cjk_count = len([w for w in non_cjk.split() if w])
            wc = cjk_count + non_cjk_count
            if ev.min_val is not None and wc < ev.min_val:
                return False, f"word count {wc} < min {ev.min_val}"
            if ev.max_val is not None and wc > ev.max_val:
                return False, f"word count {wc} > max {ev.max_val}"
            return True, f"word count {wc} in range"

        elif check == "contains":
            lower = output.lower()
            matched = [v for v in ev.values if v.lower() in lower]
            if ev.match_mode == "all":
                missing = [v for v in ev.values if v.lower() not in lower]
                if not missing:
                    return True, f"contains all of {ev.values}"
                return False, f"missing: {missing}"
            else:  # "any"
                if matched:
                    return True, f"contains '{matched[0]}'"
                return False, f"none of {ev.values} found"

        elif check == "not_contains":
            lower = output.lower()
            found = [v for v in ev.values if v.lower() in lower]
            if found:
                return False, f"forbidden content found: {found}"
            return True, "does not contain forbidden content"

        else:
            return False, f"unknown rule check: {check}"

    # -- LLM judge --

    def _check_llm(self, ev: EvalSpec, output: str) -> Tuple[bool, str]:
        prompt = (
            f"You are an eval judge. Given the following output, answer YES or NO.\n\n"
            f"Question: {ev.question}\n\n"
            f"A YES answer means: {ev.pass_desc}\n"
            f"A NO answer means: {ev.fail_desc}\n\n"
            f"--- OUTPUT START ---\n{output}\n--- OUTPUT END ---\n\n"
            f"Answer with exactly one word: YES or NO."
        )
        try:
            resp = self.provider.call(system="", user=prompt,
                                     temperature=0.0, max_tokens=256)
            answer = resp.strip().upper()
            if "YES" in answer:
                return True, "LLM judge: YES"
            else:
                return False, f"LLM judge: {resp.strip()[:80]}"
        except Exception as exc:
            _log_err(f"LLM eval error for '{ev.name}': {exc}")
            return False, f"LLM eval error: {exc}"


# ---------------------------------------------------------------------------
# Eval Config Loader
# ---------------------------------------------------------------------------

class EvalConfig:
    """Parsed eval.json configuration."""

    def __init__(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except FileNotFoundError:
            _die(f"Eval file not found: {path}")
        except json.JSONDecodeError as exc:
            _die(f"Invalid JSON in {path}: {exc}")

        if not isinstance(raw, dict):
            _die(f"eval.json must be a JSON object, got {type(raw).__name__}")

        raw_inputs = raw.get("test_inputs", [])
        if not raw_inputs:
            _die("eval.json must contain a non-empty 'test_inputs' array")
        # Support both plain strings and {"name": ..., "input": ...} objects
        self.test_inputs: List[str] = []
        for item in raw_inputs:
            if isinstance(item, str):
                self.test_inputs.append(item)
            elif isinstance(item, dict) and "input" in item:
                self.test_inputs.append(item["input"])
            else:
                _die(f"test_inputs items must be strings or objects with 'input' field, got: {item}")

        self.system_context: str = raw.get("system_context", "")
        self.runs_per_experiment: int = raw.get("runs_per_experiment", 5)
        self.max_experiments: int = raw.get("max_experiments", 30)

        raw_evals = raw.get("evals", [])
        if not raw_evals:
            _die("eval.json must contain a non-empty 'evals' array")

        self.evals: List[EvalSpec] = []
        for i, e in enumerate(raw_evals):
            if not isinstance(e, dict):
                _die(f"evals[{i}] must be a JSON object")
            if "type" not in e:
                _die(f"evals[{i}] missing 'type' field")
            self.evals.append(EvalSpec(e))

        _log(f"Loaded {len(self.evals)} evals, {len(self.test_inputs)} test inputs")


# ---------------------------------------------------------------------------
# Experiment Loop
# ---------------------------------------------------------------------------

class ExperimentResult:
    """Result of a single experiment."""

    def __init__(self, experiment_id: int, score: int, max_score: int,
                 status: str, description: str,
                 run_details: List[dict]):
        self.experiment_id = experiment_id
        self.score = score
        self.max_score = max_score
        self.pass_rate = (score / max_score * 100) if max_score > 0 else 0.0
        self.status = status        # "baseline" | "keep" | "discard"
        self.description = description
        self.run_details = run_details
        self.timestamp = datetime.datetime.utcnow().isoformat() + "Z"


class ExperimentLoop:
    """Main autoresearch optimization loop."""

    def __init__(self, target_path: str, eval_config: EvalConfig,
                 provider: LLMProvider, runs: int, max_experiments: int,
                 output_dir: str, generate_dashboard: bool,
                 verbose: bool):
        self.target_path = os.path.abspath(target_path)
        self.eval_config = eval_config
        self.provider = provider
        self.runs = runs
        self.max_experiments = max_experiments
        self.output_dir = os.path.abspath(output_dir)
        self.generate_dashboard = generate_dashboard
        self.verbose = verbose

        self.eval_runner = EvalRunner(eval_config.evals, provider)
        self.results: List[ExperimentResult] = []
        self.best_score = -1
        self.best_skill: str = ""
        self.consecutive_95 = 0

    def run(self) -> None:
        """Execute the full optimization loop."""
        # Validate target
        if not os.path.isfile(self.target_path):
            _die(f"Target file not found: {self.target_path}")

        # Read original
        original_skill = _read_file(self.target_path)

        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)

        # Backup
        baseline_path = self.target_path + ".baseline"
        if not os.path.exists(baseline_path):
            shutil.copy2(self.target_path, baseline_path)
            _log(f"Backed up original to {baseline_path}")

        # Initialize output files
        tsv_path = os.path.join(self.output_dir, "results.tsv")
        with open(tsv_path, "w", encoding="utf-8") as f:
            f.write("experiment\tscore\tmax_score\tpass_rate\tstatus\tdescription\n")

        changelog_path = os.path.join(self.output_dir, "changelog.md")
        with open(changelog_path, "w", encoding="utf-8") as f:
            ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
            f.write(f"# Autoresearch Changelog\n\n")
            f.write(f"Started: {ts}\n")
            f.write(f"Target: `{self.target_path}`\n")
            f.write(f"Provider: {self.provider.name()}\n\n")

        # -- Experiment 0: baseline --
        _log("\n=== Experiment 0: Baseline ===")
        baseline_result = self._run_experiment(0, original_skill, "baseline",
                                               "Original SKILL.md (baseline)")
        self.results.append(baseline_result)
        self.best_score = baseline_result.score
        self.best_skill = original_skill
        self._log_result(baseline_result)
        self._append_tsv(tsv_path, baseline_result)
        self._append_changelog(changelog_path, baseline_result, "")

        current_skill = original_skill

        # -- Main loop --
        for exp_id in range(1, self.max_experiments + 1):
            _log(f"\n=== Experiment {exp_id}/{self.max_experiments} ===")

            # Analyze failures from last experiment
            last_result = self.results[-1]
            failures = self._collect_failures(last_result)

            if not failures:
                _log("No failures to fix, trying to reach 100%...")
                failures = [("(no specific failure)", "trying to reach 100%")]

            # Mutate
            _log("Requesting mutation from LLM...")
            try:
                new_skill = self._mutate(current_skill, failures)
            except Exception as exc:
                _log_err(f"Mutation failed: {exc}")
                result = ExperimentResult(
                    exp_id, self.best_score,
                    self._max_score(), "discard",
                    f"Mutation LLM call failed: {exc}", [])
                self.results.append(result)
                self._log_result(result)
                self._append_tsv(tsv_path, result)
                self._append_changelog(changelog_path, result,
                                       "LLM mutation request failed.")
                continue

            if not new_skill.strip():
                _log_err("Mutation returned empty content, skipping.")
                result = ExperimentResult(
                    exp_id, self.best_score,
                    self._max_score(), "discard",
                    "Mutation returned empty content", [])
                self.results.append(result)
                self._log_result(result)
                self._append_tsv(tsv_path, result)
                self._append_changelog(changelog_path, result,
                                       "Empty mutation output.")
                continue

            # Compute a short description of what changed
            change_desc = self._describe_change(current_skill, new_skill)

            # Write mutated skill
            _write_file(self.target_path, new_skill)

            # Test
            result = self._run_experiment(exp_id, new_skill, "", change_desc)

            # Decide
            if result.score > self.best_score:
                result.status = "keep"
                self.best_score = result.score
                self.best_skill = new_skill
                current_skill = new_skill
                _log(f"KEEP: score improved to {result.pass_rate:.1f}%")
            else:
                result.status = "discard"
                # Revert to best
                _write_file(self.target_path, current_skill)
                _log(f"DISCARD: score {result.pass_rate:.1f}% <= best {self.best_score}/{self._max_score()}")

            # Track convergence
            if result.pass_rate >= 95.0:
                self.consecutive_95 += 1
            else:
                self.consecutive_95 = 0

            self.results.append(result)
            self._log_result(result)
            self._append_tsv(tsv_path, result)
            self._append_changelog(changelog_path, result, change_desc)

            # Save results.json after each experiment
            self._save_results_json()

            # Check exit
            if self.consecutive_95 >= 3:
                _log("Converged: 95%+ for 3 consecutive experiments.")
                break

        # -- Finalize --
        # Ensure the best skill is in place
        _write_file(self.target_path, self.best_skill)
        self._save_results_json()

        if self.generate_dashboard:
            self._generate_dashboard()

        self._print_summary()

    def _run_experiment(self, exp_id: int, skill_content: str,
                        status: str, description: str) -> ExperimentResult:
        """Run the skill against all test inputs for N runs and score."""
        all_details: List[dict] = []
        total_score = 0
        total_max = 0

        for run_idx in range(self.runs):
            for inp in self.eval_config.test_inputs:
                # Generate output
                system_prompt = skill_content
                if self.eval_config.system_context:
                    system_prompt = (
                        self.eval_config.system_context + "\n\n"
                        + skill_content
                    )

                try:
                    output = self.provider.call(
                        system=system_prompt,
                        user=inp,
                        temperature=0.7,
                        max_tokens=4096,
                    )
                except Exception as exc:
                    _log_err(f"  Run {run_idx+1} input {inp[:40]!r}: LLM error: {exc}")
                    # Score as all-fail for this run
                    detail = {
                        "run": run_idx,
                        "input": inp,
                        "output": f"[ERROR: {exc}]",
                        "eval_results": [
                            {"name": ev.name, "passed": False,
                             "reason": f"LLM call failed: {exc}"}
                            for ev in self.eval_config.evals
                        ],
                        "score": 0,
                        "max_score": len(self.eval_config.evals),
                    }
                    all_details.append(detail)
                    total_max += len(self.eval_config.evals)
                    continue

                # Score
                eval_results = self.eval_runner.score_output(output)
                run_score = sum(1 for _, p, _ in eval_results if p)
                run_max = len(eval_results)
                total_score += run_score
                total_max += run_max

                detail = {
                    "run": run_idx,
                    "input": inp,
                    "output": output,
                    "eval_results": [
                        {"name": ev.name, "passed": p, "reason": r}
                        for ev, p, r in eval_results
                    ],
                    "score": run_score,
                    "max_score": run_max,
                }
                all_details.append(detail)

                passed_str = f"{run_score}/{run_max}"
                _log(f"  Run {run_idx+1}, input {inp[:40]!r}: {passed_str}")

        return ExperimentResult(exp_id, total_score, total_max,
                                status, description, all_details)

    def _max_score(self) -> int:
        """Maximum possible score for one full experiment."""
        return self.runs * len(self.eval_config.test_inputs) * len(self.eval_config.evals)

    def _collect_failures(self, result: ExperimentResult
                          ) -> List[Tuple[str, str]]:
        """Extract (eval_name, reason) pairs from failed checks."""
        failures: List[Tuple[str, str]] = []
        for detail in result.run_details:
            for er in detail.get("eval_results", []):
                if not er["passed"]:
                    failures.append((er["name"], er["reason"]))
        return failures

    def _mutate(self, current_skill: str,
                failures: List[Tuple[str, str]]) -> str:
        """Ask LLM to suggest a single targeted change to the SKILL.md."""
        # Summarize failures by frequency
        failure_counts: Dict[str, int] = {}
        failure_examples: Dict[str, List[str]] = {}
        for name, reason in failures:
            failure_counts[name] = failure_counts.get(name, 0) + 1
            if name not in failure_examples:
                failure_examples[name] = []
            if len(failure_examples[name]) < 3:
                failure_examples[name].append(reason)

        # Sort by frequency
        sorted_failures = sorted(failure_counts.items(),
                                 key=lambda x: -x[1])

        failure_report = []
        for name, count in sorted_failures[:5]:
            examples = failure_examples.get(name, [])
            failure_report.append(
                f"- {name} (failed {count} times): {'; '.join(examples)}"
            )

        # Build eval descriptions
        eval_descs = "\n".join(ev.describe() for ev in self.eval_config.evals)

        # Collect sample failing outputs
        last = self.results[-1] if self.results else None
        failing_outputs = []
        if last:
            for detail in last.run_details:
                any_fail = any(not er["passed"]
                               for er in detail.get("eval_results", []))
                if any_fail and len(failing_outputs) < 3:
                    snippet = detail["output"][:800]
                    input_snippet = detail["input"][:200]
                    fail_names = [er["name"] for er in detail["eval_results"]
                                  if not er["passed"]]
                    failing_outputs.append(
                        f"Input: {input_snippet}\n"
                        f"Output (truncated): {snippet}\n"
                        f"Failed evals: {fail_names}"
                    )

        prompt = (
            "You are optimizing an AI skill prompt. "
            "Here is the current SKILL.md:\n\n"
            "```\n" + current_skill + "\n```\n\n"
            "Here are the eval criteria:\n" + eval_descs + "\n\n"
            "Here are the most common failures:\n"
            + "\n".join(failure_report) + "\n\n"
        )

        if failing_outputs:
            prompt += (
                "Here are sample outputs that FAILED and why:\n\n"
                + "\n---\n".join(failing_outputs) + "\n\n"
            )

        prompt += (
            "Rules:\n"
            "- Make exactly ONE targeted change to fix the most common failure\n"
            "- Do not rewrite the entire skill\n"
            "- Do not add vague instructions like \"be better\" or \"try harder\"\n"
            "- Keep the change minimal and specific\n"
            "- Return the COMPLETE updated SKILL.md content (not just the diff)\n"
            "\n"
            "Return ONLY the updated SKILL.md content, no explanation, "
            "no code fences, no preamble."
        )

        response = self.provider.call(system="", user=prompt,
                                      temperature=0.7, max_tokens=8192)

        # Strip any markdown code fences the LLM might have added
        cleaned = response.strip()
        if cleaned.startswith("```"):
            # Remove opening fence (possibly with language tag)
            first_newline = cleaned.index("\n") if "\n" in cleaned else len(cleaned)
            cleaned = cleaned[first_newline + 1:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        return cleaned.strip()

    def _describe_change(self, old: str, new: str) -> str:
        """Generate a short description of what changed between two versions."""
        old_lines = set(old.splitlines())
        new_lines = set(new.splitlines())
        added = new_lines - old_lines
        removed = old_lines - new_lines

        if not added and not removed:
            return "no visible change"

        parts = []
        if added:
            parts.append(f"+{len(added)} lines")
        if removed:
            parts.append(f"-{len(removed)} lines")

        # Try to find a meaningful snippet from added lines
        for line in sorted(added):
            stripped = line.strip()
            if stripped and len(stripped) > 10 and not stripped.startswith("#"):
                parts.append(f"e.g. added: {stripped[:80]!r}")
                break

        return "; ".join(parts)

    def _log_result(self, result: ExperimentResult) -> None:
        """Print a one-line summary."""
        _log(f"Experiment {result.experiment_id}/{self.max_experiments}: "
             f"score {result.pass_rate:.1f}% ({result.score}/{result.max_score}) "
             f"-- {result.status.upper()}: {result.description[:80]}")

    def _append_tsv(self, path: str, result: ExperimentResult) -> None:
        """Append a row to results.tsv."""
        with open(path, "a", encoding="utf-8") as f:
            desc = result.description.replace("\t", " ").replace("\n", " ")
            f.write(
                f"{result.experiment_id}\t{result.score}\t{result.max_score}\t"
                f"{result.pass_rate:.1f}\t{result.status}\t{desc}\n"
            )

    def _append_changelog(self, path: str, result: ExperimentResult,
                          change_desc: str) -> None:
        """Append an entry to changelog.md."""
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"\n## Experiment {result.experiment_id} "
                    f"-- {result.status.upper()}\n\n")
            f.write(f"- **Score**: {result.score}/{result.max_score} "
                    f"({result.pass_rate:.1f}%)\n")
            f.write(f"- **Status**: {result.status}\n")
            f.write(f"- **Description**: {result.description}\n")
            if change_desc and change_desc != result.description:
                f.write(f"- **Change**: {change_desc}\n")
            f.write(f"- **Time**: {result.timestamp}\n")

            # Summarize failures
            failures = self._collect_failures(result)
            if failures:
                counts: Dict[str, int] = {}
                for name, _ in failures:
                    counts[name] = counts.get(name, 0) + 1
                f.write("- **Failures**: "
                        + ", ".join(f"{n} ({c}x)" for n, c in
                                    sorted(counts.items(), key=lambda x: -x[1]))
                        + "\n")
            f.write("\n")

    def _save_results_json(self) -> None:
        """Write results.json with all experiment data."""
        data = {
            "target": self.target_path,
            "provider": self.provider.name(),
            "runs_per_experiment": self.runs,
            "max_experiments": self.max_experiments,
            "best_score": self.best_score,
            "best_max_score": self._max_score(),
            "best_pass_rate": (self.best_score / self._max_score() * 100
                               if self._max_score() > 0 else 0),
            "total_experiments": len(self.results),
            "experiments": [],
        }
        for r in self.results:
            data["experiments"].append({
                "id": r.experiment_id,
                "score": r.score,
                "max_score": r.max_score,
                "pass_rate": round(r.pass_rate, 2),
                "status": r.status,
                "description": r.description,
                "timestamp": r.timestamp,
                "run_details": r.run_details,
            })

        path = os.path.join(self.output_dir, "results.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _generate_dashboard(self) -> None:
        """Generate a self-contained dashboard.html with Chart.js."""
        path = os.path.join(self.output_dir, "dashboard.html")
        labels = [str(r.experiment_id) for r in self.results]
        scores = [round(r.pass_rate, 2) for r in self.results]
        statuses = [r.status for r in self.results]

        # Color points by status
        colors = []
        for s in statuses:
            if s == "keep":
                colors.append("'#22c55e'")    # green
            elif s == "discard":
                colors.append("'#ef4444'")     # red
            else:
                colors.append("'#3b82f6'")     # blue (baseline)

        ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Autoresearch Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif;
         max-width: 900px; margin: 40px auto; padding: 0 20px;
         background: #0f172a; color: #e2e8f0; }}
  h1 {{ color: #f1f5f9; }}
  .meta {{ color: #94a3b8; font-size: 14px; margin-bottom: 24px; }}
  .card {{ background: #1e293b; border-radius: 12px; padding: 24px;
           margin-bottom: 20px; }}
  .best {{ font-size: 48px; font-weight: 700; color: #22c55e; }}
  .legend {{ display: flex; gap: 16px; margin-top: 12px; font-size: 13px; }}
  .dot {{ width: 10px; height: 10px; border-radius: 50%;
          display: inline-block; margin-right: 4px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
  th, td {{ padding: 8px 12px; text-align: left;
            border-bottom: 1px solid #334155; }}
  th {{ color: #94a3b8; }}
  .keep {{ color: #22c55e; }}
  .discard {{ color: #ef4444; }}
  .baseline {{ color: #3b82f6; }}
</style>
</head>
<body>
<h1>Autoresearch Dashboard</h1>
<p class="meta">Generated: {ts} | Target: {self.target_path}</p>

<div class="card">
  <div>Best Score</div>
  <div class="best">{max(scores) if scores else 0}%</div>
  <div class="legend">
    <span><span class="dot" style="background:#3b82f6"></span> Baseline</span>
    <span><span class="dot" style="background:#22c55e"></span> Keep</span>
    <span><span class="dot" style="background:#ef4444"></span> Discard</span>
  </div>
</div>

<div class="card">
  <canvas id="chart" height="120"></canvas>
</div>

<div class="card">
  <table>
    <tr><th>#</th><th>Score</th><th>Pass Rate</th><th>Status</th><th>Description</th></tr>
"""
        for r in self.results:
            css_class = r.status if r.status in ("keep", "discard", "baseline") else ""
            desc_escaped = r.description[:100].replace("&", "&amp;").replace("<", "&lt;")
            html += (
                f"    <tr><td>{r.experiment_id}</td>"
                f"<td>{r.score}/{r.max_score}</td>"
                f"<td>{r.pass_rate:.1f}%</td>"
                f'<td class="{css_class}">{r.status}</td>'
                f"<td>{desc_escaped}</td></tr>\n"
            )

        html += f"""  </table>
</div>

<script>
new Chart(document.getElementById('chart'), {{
  type: 'line',
  data: {{
    labels: {json.dumps(labels)},
    datasets: [{{
      label: 'Pass Rate (%)',
      data: {json.dumps(scores)},
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      fill: true,
      tension: 0.3,
      pointBackgroundColor: [{','.join(colors)}],
      pointRadius: 6,
      pointHoverRadius: 8,
    }}]
  }},
  options: {{
    scales: {{
      y: {{
        min: 0, max: 100,
        grid: {{ color: '#334155' }},
        ticks: {{ color: '#94a3b8' }}
      }},
      x: {{
        grid: {{ color: '#334155' }},
        ticks: {{ color: '#94a3b8' }}
      }}
    }},
    plugins: {{
      legend: {{ labels: {{ color: '#e2e8f0' }} }}
    }}
  }}
}});
</script>
</body>
</html>"""

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        _log(f"Dashboard written to {path}")

    def _print_summary(self) -> None:
        """Print final summary to stdout."""
        total = len(self.results)
        keeps = sum(1 for r in self.results if r.status == "keep")
        discards = sum(1 for r in self.results if r.status == "discard")
        best_rate = (self.best_score / self._max_score() * 100
                     if self._max_score() > 0 else 0)

        _log("\n" + "=" * 60)
        _log("AUTORESEARCH COMPLETE")
        _log("=" * 60)
        _log(f"  Experiments run: {total}")
        _log(f"  Kept:           {keeps}")
        _log(f"  Discarded:      {discards}")
        _log(f"  Best score:     {self.best_score}/{self._max_score()} "
             f"({best_rate:.1f}%)")
        _log(f"  Output dir:     {self.output_dir}")
        _log(f"  Target:         {self.target_path}")
        if os.path.exists(self.target_path + ".baseline"):
            _log(f"  Baseline saved: {self.target_path}.baseline")
        _log("=" * 60)


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def _log(msg: str) -> None:
    """Print to stdout."""
    print(msg, flush=True)


def _log_verbose(msg: str) -> None:
    """Print verbose info to stdout."""
    print(f"  [verbose] {msg}", flush=True)


def _log_err(msg: str) -> None:
    """Print to stderr."""
    print(msg, file=sys.stderr, flush=True)


def _die(msg: str) -> None:
    """Print error and exit."""
    print(f"ERROR: {msg}", file=sys.stderr, flush=True)
    sys.exit(1)


def _read_file(path: str) -> str:
    """Read a file, die on error."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as exc:
        _die(f"Cannot read {path}: {exc}")
        return ""  # unreachable


def _write_file(path: str, content: str) -> None:
    """Write a file, die on error."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as exc:
        _die(f"Cannot write {path}: {exc}")


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    p = argparse.ArgumentParser(
        prog="autoresearch",
        description="Autonomous skill prompt optimizer (zero-dep, stdlib only).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python autoresearch.py --target skills/search/SKILL.md --evals eval.json\n"
            "  python autoresearch.py --target SKILL.md --evals eval.json --runs 3 --max-experiments 10 --dashboard\n"
            "  python autoresearch.py --target SKILL.md --evals eval.json --provider openai --verbose\n"
        ),
    )
    p.add_argument("--target", required=True,
                   help="Path to the SKILL.md file to optimize")
    p.add_argument("--evals", required=True,
                   help="Path to eval.json file")
    p.add_argument("--provider", choices=["minimax", "openai", "anthropic"],
                   default=None,
                   help="LLM provider (auto-detect from env if not specified)")
    p.add_argument("--model", default=None,
                   help="Override the default model for the provider")
    p.add_argument("--runs", type=int, default=5,
                   help="Runs per experiment (default: 5)")
    p.add_argument("--max-experiments", type=int, default=30,
                   help="Maximum experiment cycles (default: 30)")
    p.add_argument("--dashboard", action="store_true",
                   help="Generate dashboard.html with score progression chart")
    p.add_argument("--output-dir", default=None,
                   help="Output directory (default: autoresearch-{skill}/ next to target)")
    p.add_argument("--timeout", type=int, default=180,
                   help="HTTP timeout in seconds per LLM call (default: 180)")
    p.add_argument("--verbose", action="store_true",
                   help="Verbose logging (full LLM responses)")
    return p


def main() -> None:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()

    # Validate target
    target = os.path.abspath(args.target)
    if not os.path.isfile(target):
        _die(f"Target file not found: {target}")

    # Validate evals
    evals_path = os.path.abspath(args.evals)
    if not os.path.isfile(evals_path):
        _die(f"Eval file not found: {evals_path}")

    # Load eval config
    eval_config = EvalConfig(evals_path)

    # CLI takes precedence; fall back to eval.json values
    runs = args.runs if args.runs != 5 else eval_config.runs_per_experiment
    max_experiments = args.max_experiments if args.max_experiments != 30 else eval_config.max_experiments

    # Detect provider
    provider = detect_provider(args.provider, verbose=args.verbose,
                               model_override=args.model,
                               timeout=args.timeout)
    _log(f"Using provider: {provider.name()}")

    # Output directory
    if args.output_dir:
        output_dir = os.path.abspath(args.output_dir)
    else:
        skill_name = os.path.basename(os.path.dirname(target))
        if not skill_name or skill_name == ".":
            skill_name = os.path.splitext(os.path.basename(target))[0]
        output_dir = os.path.join(os.path.dirname(target),
                                  f"autoresearch-{skill_name}")

    _log(f"Target:     {target}")
    _log(f"Evals:      {evals_path}")
    _log(f"Output dir: {output_dir}")
    _log(f"Runs/exp:   {runs}")
    _log(f"Max exp:    {max_experiments}")

    # Run
    loop = ExperimentLoop(
        target_path=target,
        eval_config=eval_config,
        provider=provider,
        runs=runs,
        max_experiments=max_experiments,
        output_dir=output_dir,
        generate_dashboard=args.dashboard,
        verbose=args.verbose,
    )
    loop.run()


if __name__ == "__main__":
    main()
