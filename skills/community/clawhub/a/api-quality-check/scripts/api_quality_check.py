#!/usr/bin/env python3
from __future__ import annotations

import argparse
from html import escape
import json
import random
import re
import statistics
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

APP_VERSION = "0.1.0"
HTTP_USER_AGENT = f"api-quality-check/{APP_VERSION}"
DEFAULT_TIMEOUT_SECONDS = 60
REASONING_DISABLE_BODY = {"thinking": {"type": "disabled"}}
DEFAULT_B3_STABLE_MIN_COUNT = 2
DEFAULT_B3_STABLE_MIN_RATIO = 0.35
DEFAULT_LT_PROMPTS = [
    "x",
    "Summarize in one word: stable",
    "Continue with one token: The capital of France is",
    "Classify in one token: positive",
    "Output only the next token: 2 + 2 =",
]


def canonical_connection_type(connection_type: str, base_url: str = "") -> str:
    raw = (connection_type or "").strip().lower()
    base = (base_url or "").strip().lower()
    if "anthropic" in raw or "claude" in raw or "anthropic" in base:
        return "Anthropic"
    if raw == "openai" or raw.startswith("openai ") or "api.openai.com" in base:
        return "OpenAI"
    if "compatible" in raw or "兼容" in raw:
        return "OpenAI-Compatible"
    openai_like_keywords = [
        "deepseek",
        "openrouter",
        "moonshot",
        "kimi",
        "qwen",
        "dashscope",
        "siliconflow",
        "ollama",
        "lmstudio",
        "vllm",
        "xinference",
        "fireworks",
        "together",
        "mistral",
        "azure",
        "doubao",
        "volc",
        "baidu",
        "zhipu",
        "glm",
        "baichuan",
        "hunyuan",
        "xai",
        "grok",
    ]
    if any(keyword in raw or keyword in base for keyword in openai_like_keywords):
        return "OpenAI-Compatible"
    return "OpenAI-Compatible"


def normalize_base_url(connection_type: str, base_url: str) -> str:
    normalized = (base_url or "").strip().rstrip("/")
    provider = canonical_connection_type(connection_type, normalized)
    if provider in {"OpenAI", "OpenAI-Compatible"}:
        for suffix in ("/chat/completions", "/completions"):
            if normalized.lower().endswith(suffix):
                normalized = normalized[: -len(suffix)]
                break
    elif provider == "Anthropic" and normalized.lower().endswith("/messages"):
        normalized = normalized[: -len("/messages")]
    return normalized


def default_extra_body_for(connection_type: str, base_url: str, model_id: str) -> Dict[str, Any]:
    provider = canonical_connection_type(connection_type, base_url)
    haystack = " ".join([(base_url or "").lower(), (model_id or "").lower(), provider.lower()])
    thinking_markers = [
        "ark.cn-beijing.volces.com",
        "volces",
        "doubao",
        "seed",
        "ark-",
        "open.bigmodel.cn",
        "bigmodel",
        "zhipu",
        "glm-4.7",
        "glm",
    ]
    if any(marker in haystack for marker in thinking_markers):
        return dict(REASONING_DISABLE_BODY)
    return {}


def build_sample_vector(sample: Dict[str, float], vocab: List[str]) -> List[float]:
    floor = min(sample.values()) if sample else -9999.0
    return [float(sample.get(token, floor)) for token in vocab]


def permutation_test(
    baseline_samples: List[Dict[str, float]],
    current_samples: List[Dict[str, float]],
    permutations: int = 200,
) -> Dict[str, Any]:
    vocab = sorted({k for s in baseline_samples + current_samples for k in s.keys()})
    if not vocab:
        raise ValueError("No comparable logprob tokens were returned.")

    base_vectors = [build_sample_vector(s, vocab) for s in baseline_samples]
    curr_vectors = [build_sample_vector(s, vocab) for s in current_samples]

    def avg(vectors: List[List[float]]) -> List[float]:
        return [statistics.fmean(col) for col in zip(*vectors)]

    def distance(a: List[List[float]], b: List[List[float]]) -> float:
        ma = avg(a)
        mb = avg(b)
        return statistics.fmean(abs(x - y) for x, y in zip(ma, mb))

    observed = distance(base_vectors, curr_vectors)
    pooled = base_vectors + curr_vectors
    n_base = len(base_vectors)
    exceed = 0
    rng = random.Random(42)
    for _ in range(permutations):
        shuffled = pooled[:]
        rng.shuffle(shuffled)
        pa = shuffled[:n_base]
        pb = shuffled[n_base:]
        if distance(pa, pb) >= observed:
            exceed += 1
    p_value = (exceed + 1) / (permutations + 1)

    token_deltas: List[Any] = []
    for token in vocab:
        base_m = statistics.fmean(s.get(token, min(s.values())) for s in baseline_samples)
        curr_m = statistics.fmean(s.get(token, min(s.values())) for s in current_samples)
        token_deltas.append((token, curr_m - base_m, base_m, curr_m))
    token_deltas.sort(key=lambda x: abs(x[1]), reverse=True)

    return {
        "p_value": p_value,
        "distance": observed,
        "top_deltas": [
            {
                "token": token,
                "delta": round(delta, 6),
                "baseline_mean": round(base_m, 6),
                "current_mean": round(curr_m, 6),
            }
            for token, delta, base_m, curr_m in token_deltas[:10]
        ],
    }


@dataclass
class ProviderConfig:
    provider: str
    base_url: str
    api_key: str
    model_id: str
    temperature: float = 0.0
    stream: bool = False
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS
    headers: Optional[Dict[str, str]] = None
    extra_body: Optional[Dict[str, Any]] = None
    extra_body_source: str = "none"
    input_base_url: str = ""


class ApiCapabilityError(RuntimeError):
    pass


class ApiClient:
    def __init__(self, config: ProviderConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": HTTP_USER_AGENT})

    def _normalize_base_url(self) -> str:
        provider = canonical_connection_type(self.config.provider, self.config.base_url)
        base = (self.config.base_url or "").strip()
        if provider == "OpenAI":
            return base or "https://api.openai.com/v1"
        if provider == "OpenAI-Compatible":
            return base or "https://api.openai.com/v1"
        if provider == "Anthropic":
            return base or "https://api.anthropic.com"
        return base

    def _endpoint(self, suffix: str) -> str:
        base = self._normalize_base_url().rstrip("/")
        if base.endswith(suffix):
            return base
        return base + suffix

    def _merge_extra_body(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        extra = self.config.extra_body or {}
        if not extra:
            return payload

        return merge_dict(payload, extra)

    def _merge_request_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        custom_headers = self.config.headers or {}
        if not custom_headers:
            return headers
        merged = dict(headers)
        merged.update(custom_headers)
        return merged

    def _openai_headers(self) -> Dict[str, str]:
        return self._merge_request_headers({
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        })

    def _anthropic_headers(self) -> Dict[str, str]:
        return self._merge_request_headers({
            "x-api-key": self.config.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        })

    def request_text(
        self,
        prompt: str,
        *,
        max_tokens: int,
        temperature: Optional[float] = None,
        stream: Optional[bool] = None,
        want_logprobs: bool = False,
        top_logprobs: int = 10,
    ) -> Dict[str, Any]:
        provider = canonical_connection_type(self.config.provider, self.config.base_url)
        temp = self.config.temperature if temperature is None else temperature
        use_stream = self.config.stream if stream is None else stream
        if provider in {"OpenAI", "OpenAI-Compatible"}:
            return self._request_openai(
                prompt,
                max_tokens=max_tokens,
                temperature=temp,
                stream=use_stream,
                want_logprobs=want_logprobs,
                top_logprobs=top_logprobs,
            )
        if provider == "Anthropic":
            return self._request_anthropic(
                prompt,
                max_tokens=max_tokens,
                temperature=temp,
                stream=use_stream,
                want_logprobs=want_logprobs,
                top_logprobs=top_logprobs,
            )
        raise ValueError(f"Unsupported provider: {self.config.provider}")

    def _request_openai(
        self,
        prompt: str,
        *,
        max_tokens: int,
        temperature: float,
        stream: bool,
        want_logprobs: bool,
        top_logprobs: int,
    ) -> Dict[str, Any]:
        url = self._endpoint("/chat/completions")
        base_payload: Dict[str, Any] = {
            "model": self.config.model_id,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": stream,
        }
        if want_logprobs:
            base_payload["logprobs"] = True
            base_payload["top_logprobs"] = max(1, min(20, int(top_logprobs)))
        payload = self._merge_extra_body(base_payload)

        data = self._post_json(url, self._openai_headers(), payload)
        request_profile = {
            "provider": canonical_connection_type(self.config.provider, self.config.base_url),
            "base_url": self.config.base_url,
            "extra_body_source": self.config.extra_body_source,
            "extra_body": self.config.extra_body or {},
            "auto_retry": False,
        }
        choice, message = self._first_openai_choice(data)
        text = self._flatten_openai_content(message.get("content", ""))
        if not text and message.get("reasoning_content"):
            retry_data = self._retry_openai_with_reasoning_disabled(url, base_payload, current_payload=payload)
            if retry_data is not None:
                data = retry_data
                request_profile["auto_retry"] = True
                request_profile["retry_extra_body"] = dict(REASONING_DISABLE_BODY)
                choice, message = self._first_openai_choice(data)
                text = self._flatten_openai_content(message.get("content", ""))
        if not text and message.get("reasoning_content"):
            raise ApiCapabilityError(
                "The endpoint returned reasoning_content but no normal content. "
                "Disable thinking/reasoning or use a non-reasoning response mode."
            )
        logprob_dict = None
        if want_logprobs:
            logprob_dict = self._extract_openai_logprobs(choice)
        return {
            "text": text,
            "raw": data,
            "logprob_dict": logprob_dict,
            "request_profile": request_profile,
        }

    def _post_json(self, url: str, headers: Dict[str, str], payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self.session.post(
            url,
            headers=headers,
            json=payload,
            timeout=self.config.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()

    def _first_openai_choice(self, data: Dict[str, Any]) -> tuple[Dict[str, Any], Dict[str, Any]]:
        choices = data.get("choices", [])
        if not choices:
            raise RuntimeError("The endpoint did not return choices.")
        choice = choices[0]
        message = choice.get("message", {})
        return choice, message

    def _retry_openai_with_reasoning_disabled(
        self,
        url: str,
        original_payload: Dict[str, Any],
        *,
        current_payload: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        if payload_disables_reasoning(current_payload):
            return None
        retry_payload = merge_dict(original_payload, REASONING_DISABLE_BODY)
        try:
            return self._post_json(url, self._openai_headers(), retry_payload)
        except requests.HTTPError:
            return None

    def _flatten_openai_content(self, content: Any) -> str:
        if content is None:
            return ""
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts: List[str] = []
            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        parts.append(item.get("text", ""))
                    elif "text" in item:
                        parts.append(str(item.get("text", "")))
            return "".join(parts)
        return str(content)

    def _extract_openai_logprobs(self, choice: Dict[str, Any]) -> Dict[str, float]:
        lp = choice.get("logprobs")
        if not lp:
            raise ApiCapabilityError("The endpoint did not return logprobs; LT-lite is unavailable.")
        content = lp.get("content") or []
        if not content:
            raise ApiCapabilityError("The endpoint returned empty logprobs.content.")
        first = content[0]
        result: Dict[str, float] = {}
        token = first.get("token")
        token_lp = first.get("logprob")
        if token is not None and token_lp is not None:
            result[str(token)] = float(token_lp)
        for item in first.get("top_logprobs") or []:
            if item.get("token") is None or item.get("logprob") is None:
                continue
            result[str(item["token"])] = float(item["logprob"])
        if not result:
            raise ApiCapabilityError("The endpoint returned no usable top_logprobs.")
        return result

    def _request_anthropic(
        self,
        prompt: str,
        *,
        max_tokens: int,
        temperature: float,
        stream: bool,
        want_logprobs: bool,
        top_logprobs: int,
    ) -> Dict[str, Any]:
        del stream
        del top_logprobs
        if want_logprobs:
            raise ApiCapabilityError("Anthropic mode is treated as B3IT-only in this skill.")
        base = self._normalize_base_url().rstrip("/")
        url = self._endpoint("/messages" if base.endswith("/v1") else "/v1/messages")
        payload: Dict[str, Any] = {
            "model": self.config.model_id,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
        }
        payload = self._merge_extra_body(payload)
        response = self.session.post(
            url,
            headers=self._anthropic_headers(),
            json=payload,
            timeout=self.config.timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()
        content = data.get("content", [])
        text = self._flatten_anthropic_content(content)
        if not text and self._anthropic_has_thinking_only(content):
            raise ApiCapabilityError(
                "The endpoint returned thinking blocks but no text blocks. "
                "Disable thinking/reasoning or use a non-reasoning response mode."
            )
        return {"text": text, "raw": data, "logprob_dict": None}

    def _flatten_anthropic_content(self, content: Any) -> str:
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts: List[str] = []
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    parts.append(block.get("text", ""))
            return "".join(parts)
        return str(content)

    def _anthropic_has_thinking_only(self, content: Any) -> bool:
        if not isinstance(content, list):
            return False
        has_text = False
        has_thinking = False
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text" and block.get("text"):
                has_text = True
            if block.get("type") == "thinking" and block.get("thinking") is not None:
                has_thinking = True
        return has_thinking and not has_text


class LTLiteEngine:
    def __init__(self, client: ApiClient):
        self.client = client

    def collect_samples(
        self,
        prompts: List[str],
        *,
        runs_per_prompt: int,
        top_logprobs: int,
        temperature: float,
    ) -> Dict[str, Any]:
        results: Dict[str, Any] = {"method": "LT-lite", "prompts": []}
        for prompt in prompts:
            samples: List[Dict[str, Any]] = []
            for _ in range(runs_per_prompt):
                resp = self.client.request_text(
                    prompt,
                    max_tokens=1,
                    temperature=temperature,
                    stream=False,
                    want_logprobs=True,
                    top_logprobs=top_logprobs,
                )
                samples.append(
                    {
                        "text": (resp.get("text") or "").strip("\r\n"),
                        "logprob_dict": resp.get("logprob_dict") or {},
                    }
                )
            results["prompts"].append({"prompt": prompt, "samples": samples})
        return results

    def compare(
        self,
        baseline: Dict[str, Any],
        current: Dict[str, Any],
        *,
        permutations: int,
    ) -> Dict[str, Any]:
        current_by_prompt = {item["prompt"]: item for item in current.get("prompts", [])}
        report_prompts: List[Dict[str, Any]] = []
        changed_count = 0
        for item in baseline.get("prompts", []):
            prompt = item["prompt"]
            other = current_by_prompt.get(prompt)
            if not other:
                report_prompts.append({"prompt": prompt, "error": "Current run is missing this prompt."})
                changed_count += 1
                continue
            base_samples = [s["logprob_dict"] for s in item.get("samples", []) if s.get("logprob_dict")]
            curr_samples = [s["logprob_dict"] for s in other.get("samples", []) if s.get("logprob_dict")]
            if not base_samples or not curr_samples:
                report_prompts.append({"prompt": prompt, "error": "Missing logprob samples."})
                changed_count += 1
                continue
            stats = permutation_test(base_samples, curr_samples, permutations=permutations)
            flagged = stats["p_value"] < 0.05
            if flagged:
                changed_count += 1
            report_prompts.append(
                {
                    "prompt": prompt,
                    "flagged": flagged,
                    "p_value": stats["p_value"],
                    "distance": stats["distance"],
                    "top_deltas": stats["top_deltas"],
                }
            )
        return {
            "method": "LT-lite",
            "overall_changed": changed_count > 0,
            "changed_prompts": changed_count,
            "total_prompts": len(report_prompts),
            "prompts": report_prompts,
            "permutations": permutations,
        }


class B3ITLiteEngine:
    def __init__(self, client: ApiClient):
        self.client = client

    def _candidate_prompts(self, count: int, seed: int) -> List[str]:
        rng = random.Random(seed)
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_:/.?@#"
        prompts: List[str] = []
        seen = set()

        one_char = list(chars)
        rng.shuffle(one_char)
        for prompt in one_char:
            if prompt in seen:
                continue
            prompts.append(prompt)
            seen.add(prompt)
            if len(prompts) >= count:
                return prompts

        size = 2
        while len(prompts) < count:
            batch: List[str] = []
            target = max(count - len(prompts), len(chars))
            while len(batch) < target:
                prompt = "".join(rng.choice(chars) for _ in range(size))
                if prompt in seen:
                    continue
                batch.append(prompt)
                seen.add(prompt)
            rng.shuffle(batch)
            prompts.extend(batch[: count - len(prompts)])
            size += 1
        return prompts

    def discover_baseline(
        self,
        *,
        candidate_count: int,
        discovery_repeats: int,
        keep_count: int,
        reference_samples: int,
        temperature: float,
        seed: int,
    ) -> Dict[str, Any]:
        candidates = self._candidate_prompts(candidate_count, seed)
        border_inputs: List[Dict[str, Any]] = []
        target_raw_candidates = max(keep_count, keep_count * 3)
        for prompt in candidates:
            outputs = []
            for _ in range(discovery_repeats):
                resp = self.client.request_text(
                    prompt,
                    max_tokens=1,
                    temperature=temperature,
                    stream=False,
                    want_logprobs=False,
                )
                outputs.append(resp.get("text", ""))
            support = sorted(set(outputs))
            if len(support) > 1:
                border_inputs.append(
                    {
                        "prompt": prompt,
                        "discovery_outputs": outputs,
                        "discovery_support": support,
                        "diversity": len(support),
                    }
                )
                if len(border_inputs) >= target_raw_candidates:
                    break
        if not border_inputs:
            raise RuntimeError("No border inputs were found.")

        selected: List[Dict[str, Any]] = []
        rejected_inputs: List[Dict[str, Any]] = []
        for item in border_inputs:
            outputs = []
            for _ in range(reference_samples):
                resp = self.client.request_text(
                    item["prompt"],
                    max_tokens=1,
                    temperature=temperature,
                    stream=False,
                    want_logprobs=False,
                )
                outputs.append(resp.get("text", ""))
            reference_counts = count_outputs(outputs)
            item["reference_outputs"] = outputs
            item["reference_support"] = sorted(set(outputs))
            item["reference_counts"] = reference_counts
            item["reference_frequencies"] = {
                token: round(count / reference_samples, 6)
                for token, count in sorted(reference_counts.items())
            }
            item["reference_stable_support"] = stable_support_from_counts(
                reference_counts,
                total=reference_samples,
                min_count=DEFAULT_B3_STABLE_MIN_COUNT,
                min_ratio=DEFAULT_B3_STABLE_MIN_RATIO,
            )
            if len(item["reference_stable_support"]) > 1:
                selected.append(item)
                if len(selected) >= keep_count:
                    break
            else:
                rejected_inputs.append(
                    {
                        "prompt": item["prompt"],
                        "reference_support": item["reference_support"],
                        "reference_counts": item["reference_counts"],
                        "reference_stable_support": item["reference_stable_support"],
                    }
                )
        if not selected:
            raise RuntimeError("No stable border inputs were found after reference sampling.")
        return {
            "method": "B3IT-lite",
            "temperature": temperature,
            "candidate_count": candidate_count,
            "discovery_repeats": discovery_repeats,
            "keep_count": keep_count,
            "reference_samples": reference_samples,
            "stable_support_threshold": {
                "min_count": DEFAULT_B3_STABLE_MIN_COUNT,
                "min_ratio": DEFAULT_B3_STABLE_MIN_RATIO,
            },
            "rejected_inputs": rejected_inputs,
            "border_inputs": selected,
        }

    def detect(
        self,
        baseline: Dict[str, Any],
        *,
        detection_repeats: int,
        temperature: float,
        min_stable_count: int,
        min_stable_ratio: float,
        confirm_passes: int,
    ) -> Dict[str, Any]:
        prompts_report = []
        changed = 0
        for item in baseline.get("border_inputs", []):
            outputs = []
            for _ in range(detection_repeats):
                resp = self.client.request_text(
                    item["prompt"],
                    max_tokens=1,
                    temperature=temperature,
                    stream=False,
                    want_logprobs=False,
                )
                outputs.append(resp.get("text", ""))
            baseline_counts = item.get("reference_counts")
            if not isinstance(baseline_counts, dict):
                baseline_counts = count_outputs(item.get("reference_outputs", []))
            baseline_total = len(item.get("reference_outputs", [])) or sum(
                int(v) for v in baseline_counts.values() if isinstance(v, int)
            )
            if baseline_total <= 0:
                baseline_total = max(len(item.get("reference_support", [])), 0)
                baseline_counts = {token: 1 for token in item.get("reference_support", [])}

            current_counts = count_outputs(outputs)
            baseline_stable_support = set(
                stable_support_from_counts(
                    baseline_counts,
                    total=baseline_total,
                    min_count=min_stable_count,
                    min_ratio=min_stable_ratio,
                )
            )
            current_stable_support = set(
                stable_support_from_counts(
                    current_counts,
                    total=len(outputs),
                    min_count=min_stable_count,
                    min_ratio=min_stable_ratio,
                )
            )
            if not baseline_stable_support:
                baseline_stable_support = set(item.get("reference_support", []))
            if not current_stable_support and current_counts:
                current_stable_support = set(sorted(current_counts))
            symmetric_diff = sorted(
                (baseline_stable_support - current_stable_support)
                | (current_stable_support - baseline_stable_support)
            )
            flagged = len(symmetric_diff) > 0
            confirm_reports = []
            if flagged and confirm_passes > 0:
                confirmed = False
                for _ in range(confirm_passes):
                    confirm_outputs = []
                    for _ in range(detection_repeats):
                        resp = self.client.request_text(
                            item["prompt"],
                            max_tokens=1,
                            temperature=temperature,
                            stream=False,
                            want_logprobs=False,
                        )
                        confirm_outputs.append(resp.get("text", ""))
                    confirm_counts = count_outputs(confirm_outputs)
                    confirm_stable_support = set(
                        stable_support_from_counts(
                            confirm_counts,
                            total=len(confirm_outputs),
                            min_count=min_stable_count,
                            min_ratio=min_stable_ratio,
                        )
                    )
                    if not confirm_stable_support and confirm_counts:
                        confirm_stable_support = set(sorted(confirm_counts))
                    confirm_diff = sorted(
                        (baseline_stable_support - confirm_stable_support)
                        | (confirm_stable_support - baseline_stable_support)
                    )
                    confirm_reports.append(
                        {
                            "outputs": confirm_outputs,
                            "counts": dict(sorted(confirm_counts.items())),
                            "stable_support": sorted(confirm_stable_support),
                            "symmetric_difference": confirm_diff,
                        }
                    )
                    if confirm_diff:
                        confirmed = True
                flagged = confirmed
            if flagged:
                changed += 1
            prompts_report.append(
                {
                    "prompt": item["prompt"],
                    "flagged": flagged,
                    "baseline_support": sorted(set(item.get("reference_support", []))),
                    "current_support": sorted(set(outputs)),
                    "baseline_stable_support": sorted(baseline_stable_support),
                    "current_stable_support": sorted(current_stable_support),
                    "symmetric_difference": symmetric_diff,
                    "baseline_counts": dict(sorted(baseline_counts.items())),
                    "current_counts": dict(sorted(current_counts.items())),
                    "stable_support_threshold": {
                        "min_count": min_stable_count,
                        "min_ratio": min_stable_ratio,
                    },
                    "confirm_passes": confirm_passes,
                    "confirmation_reports": confirm_reports,
                    "current_outputs": outputs,
                }
            )
            if flagged:
                return {
                    "method": "B3IT-lite",
                    "overall_changed": True,
                    "changed_prompts": changed,
                    "total_prompts": len(prompts_report),
                    "prompts": prompts_report,
                    "stopped_early": True,
                    "stable_support_threshold": {
                        "min_count": min_stable_count,
                        "min_ratio": min_stable_ratio,
                    },
                    "confirm_passes": confirm_passes,
                }
        return {
            "method": "B3IT-lite",
            "overall_changed": changed > 0,
            "changed_prompts": changed,
            "total_prompts": len(prompts_report),
            "prompts": prompts_report,
            "stopped_early": False,
            "stable_support_threshold": {
                "min_count": min_stable_count,
                "min_ratio": min_stable_ratio,
            },
            "confirm_passes": confirm_passes,
        }


def merge_dict(target: Dict[str, Any], source: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(target)
    for key, value in source.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge_dict(result[key], value)
        else:
            result[key] = value
    return result


def payload_disables_reasoning(payload: Dict[str, Any]) -> bool:
    thinking = payload.get("thinking")
    return isinstance(thinking, dict) and thinking.get("type") == "disabled"


def load_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path: Optional[str], data: Dict[str, Any]) -> None:
    if path:
        Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def save_html(path: Optional[str], html_text: str) -> None:
    if path:
        Path(path).write_text(html_text, encoding="utf-8")


def mask_key(key: str) -> str:
    if len(key) <= 8:
        return "*" * len(key)
    return key[:4] + "..." + key[-4:]


def public_provider_config(cfg: ProviderConfig) -> Dict[str, Any]:
    data = asdict(cfg)
    data["api_key"] = mask_key(data.get("api_key", ""))
    if data.get("input_base_url") == data.get("base_url"):
        data.pop("input_base_url", None)
    return data


def normalize_headers(raw_headers: Any) -> Dict[str, str]:
    if raw_headers in (None, {}):
        return {}
    if not isinstance(raw_headers, dict):
        raise ValueError("headers must be a JSON object.")
    normalized: Dict[str, str] = {}
    for key, value in raw_headers.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError("headers keys must be non-empty strings.")
        if value is None:
            continue
        normalized[key] = str(value)
    return normalized


def parse_json_object(text: Optional[str], *, field_name: str) -> Dict[str, Any]:
    if not text:
        return {}
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{field_name} must be valid JSON.") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must decode to a JSON object.")
    return value


def slugify(value: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9._-]+", "-", (value or "").strip())
    text = re.sub(r"-{2,}", "-", text).strip("-._")
    return text or "config"


def pretty_label(key: str) -> str:
    return key.replace("_", " ").strip().title()


def is_scalar(value: Any) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


def format_scalar(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def count_outputs(outputs: List[str]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for output in outputs:
        counts[output] = counts.get(output, 0) + 1
    return counts


def stable_support_from_counts(
    counts: Dict[str, int],
    *,
    total: int,
    min_count: int,
    min_ratio: float,
) -> List[str]:
    if total <= 0:
        return []
    stable = [
        token
        for token, count in counts.items()
        if count >= min_count and (count / total) >= min_ratio
    ]
    return sorted(stable)


def summary_items(result: Dict[str, Any]) -> List[tuple[str, Any]]:
    keys = [
        "mode",
        "total_configs",
        "success_count",
        "failure_count",
        "changed_count",
        "b3it_supported_count",
        "lt_supported_count",
        "overall_changed",
        "changed_prompts",
        "total_prompts",
        "permutations",
    ]
    return [(pretty_label(key), result[key]) for key in keys if key in result]


def status_badge(value: Any) -> str:
    text = format_scalar(value)
    raw = str(value).lower() if value is not None else ""
    kind = "neutral"
    if raw in {"ok", "true"}:
        kind = "good"
    elif raw in {"error", "false"}:
        kind = "bad"
    elif raw in {"skipped"}:
        kind = "warn"
    return f"<span class='badge {kind}'>{escape(text)}</span>"


def render_meter(label: str, value: int, total: int, kind: str = "good") -> str:
    total = max(total, 1)
    pct = max(0.0, min(100.0, (value / total) * 100.0))
    return (
        "<div class='meter-card'>"
        f"<div class='meter-head'><span>{escape(label)}</span><strong>{value}/{total}</strong></div>"
        f"<div class='meter-track'><div class='meter-fill {escape(kind)}' style='width:{pct:.2f}%'></div></div>"
        "</div>"
    )


def render_summary_bars(result: Dict[str, Any]) -> str:
    total = int(result.get("total_configs", 0) or 0)
    bars = []
    if total:
        if "success_count" in result:
            bars.append(render_meter("Successful", int(result.get("success_count", 0) or 0), total, "good"))
        if "failure_count" in result:
            bars.append(render_meter("Failed", int(result.get("failure_count", 0) or 0), total, "bad"))
        if "changed_count" in result:
            bars.append(render_meter("Changed", int(result.get("changed_count", 0) or 0), total, "warn"))
        if "b3it_supported_count" in result:
            bars.append(render_meter("B3IT Ready", int(result.get("b3it_supported_count", 0) or 0), total, "good"))
        if "lt_supported_count" in result:
            bars.append(render_meter("LT Ready", int(result.get("lt_supported_count", 0) or 0), total, "accent"))
    return "<div class='meters'>" + "".join(bars) + "</div>" if bars else ""


def render_key_value_table(data: Dict[str, Any]) -> str:
    rows = []
    for key, value in data.items():
        if not is_scalar(value):
            continue
        rows.append(
            f"<tr><th>{escape(pretty_label(key))}</th><td>{escape(format_scalar(value))}</td></tr>"
        )
    if not rows:
        return ""
    return "<table class='kv'>" + "".join(rows) + "</table>"


def render_prompt_list(prompts: List[Dict[str, Any]]) -> str:
    cards = []
    for item in prompts:
        if not isinstance(item, dict):
            cards.append(
                "<div class='prompt-card'>"
                f"<h4>{escape(str(item))}</h4>"
                "</div>"
            )
            continue
        title = escape(str(item.get("prompt", "(prompt)")))
        meta = []
        for key in ["flagged", "p_value", "distance", "error"]:
            if key in item:
                meta.append(f"<span class='pill'>{escape(pretty_label(key))}: {escape(format_scalar(item.get(key)))}</span>")
        blocks = [f"<div class='prompt-card'><h4>{title}</h4><div class='pills'>{''.join(meta)}</div>"]
        if "top_deltas" in item and isinstance(item["top_deltas"], list):
            rows = []
            for delta in item["top_deltas"][:10]:
                rows.append(
                    "<tr>"
                    f"<td>{escape(format_scalar(delta.get('token')))}</td>"
                    f"<td>{escape(format_scalar(delta.get('delta')))}</td>"
                    f"<td>{escape(format_scalar(delta.get('baseline_mean')))}</td>"
                    f"<td>{escape(format_scalar(delta.get('current_mean')))}</td>"
                    "</tr>"
                )
            if rows:
                blocks.append(
                    "<table class='grid'><thead><tr><th>Token</th><th>Delta</th><th>Baseline</th><th>Current</th></tr></thead><tbody>"
                    + "".join(rows)
                    + "</tbody></table>"
                )
        for key in [
            "baseline_support",
            "reference_support",
            "reference_stable_support",
            "current_support",
            "baseline_stable_support",
            "current_stable_support",
            "symmetric_difference",
            "reference_counts",
            "baseline_counts",
            "current_counts",
            "stable_support_threshold",
            "confirm_passes",
            "confirmation_reports",
            "current_outputs",
        ]:
            if key in item:
                blocks.append(
                    f"<div class='mono-block'><strong>{escape(pretty_label(key))}</strong><pre>{escape(json.dumps(item[key], ensure_ascii=False, indent=2))}</pre></div>"
                )
        blocks.append("</div>")
        cards.append("".join(blocks))
    return "".join(cards)


def render_results_table(results: List[Dict[str, Any]]) -> str:
    headers = ["Index", "Name", "Status", "B3IT", "LT", "Changed", "Details"]
    rows = []
    for item in results:
        detail_parts = []
        for key in ["error", "reason", "baseline_file", "first_token_error", "logprob_error"]:
            if item.get(key):
                detail_parts.append(f"{pretty_label(key)}: {item.get(key)}")
        if item.get("report"):
            detail_parts.append("embedded report")
        rows.append(
            "<tr>"
            f"<td>{escape(format_scalar(item.get('index')))}</td>"
            f"<td>{escape(format_scalar(item.get('name')))}</td>"
            f"<td>{status_badge(item.get('status', 'ok'))}</td>"
            f"<td>{status_badge(item.get('b3it_supported', item.get('border_input_count', '-')))}</td>"
            f"<td>{status_badge(item.get('lt_supported', item.get('prompt_count', '-')))}</td>"
            f"<td>{status_badge(item.get('overall_changed', '-'))}</td>"
            f"<td>{escape('; '.join(detail_parts))}</td>"
            "</tr>"
        )
    return (
        "<table class='grid'><thead><tr>"
        + "".join(f"<th>{escape(h)}</th>" for h in headers)
        + "</tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table>"
    )


def render_html_report(result: Dict[str, Any]) -> str:
    title = f"API Quality Report: {result.get('mode', 'result')}"
    summary = "".join(
        f"<div class='stat'><div class='label'>{escape(label)}</div><div class='value'>{escape(format_scalar(value))}</div></div>"
        for label, value in summary_items(result)
    )
    sections: List[str] = []
    summary_bars = render_summary_bars(result)

    provider_config = result.get("provider_config")
    if isinstance(provider_config, dict):
        sections.append("<section><h2>Provider</h2>" + render_key_value_table(provider_config) + "</section>")

    if isinstance(result.get("results"), list):
        sections.append("<section><h2>Results</h2>" + render_results_table(result["results"]) + "</section>")

    if isinstance(result.get("prompts"), list):
        sections.append("<section><h2>Prompts</h2>" + render_prompt_list(result["prompts"]) + "</section>")

    embedded_reports = []
    for item in result.get("results", []) if isinstance(result.get("results"), list) else []:
        report = item.get("report")
        if isinstance(report, dict):
            embedded_reports.append(
                "<details class='detail-card'><summary>"
                + escape(f"{item.get('name', 'report')} | changed={report.get('overall_changed')}")
                + "</summary>"
                + (render_key_value_table(report) or "")
                + (render_prompt_list(report.get("prompts", [])) if isinstance(report.get("prompts"), list) else "")
                + "</details>"
            )
    if embedded_reports:
        sections.append("<section><h2>Embedded Reports</h2>" + "".join(embedded_reports) + "</section>")

    sections.append(
        "<section><h2>Raw JSON</h2><details class='detail-card' open><summary>Expand JSON</summary>"
        f"<pre>{escape(json.dumps(result, ensure_ascii=False, indent=2))}</pre></details></section>"
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(title)}</title>
  <style>
    :root {{
      --bg: #f6f7f9;
      --card: #ffffff;
      --line: #e5e7eb;
      --text: #111827;
      --muted: #6b7280;
      --soft: #f3f4f6;
      --accent: #dbeafe;
      --good: #d1fae5;
      --good-text: #065f46;
      --bad: #fee2e2;
      --bad-text: #991b1b;
      --warn: #fef3c7;
      --warn-text: #92400e;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: var(--bg); color: var(--text); }}
    .wrap {{ max-width: 1180px; margin: 0 auto; padding: 24px; }}
    h1, h2, h4 {{ margin: 0 0 12px; }}
    p {{ color: var(--muted); }}
    .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin: 20px 0 24px; }}
    .stat, section, .prompt-card, .detail-card {{ background: var(--card); border: 1px solid var(--line); border-radius: 16px; }}
    .stat {{ padding: 16px; }}
    .label {{ font-size: 12px; color: var(--muted); margin-bottom: 6px; text-transform: uppercase; letter-spacing: .04em; }}
    .value {{ font-size: 22px; font-weight: 700; }}
    section {{ padding: 18px; margin-bottom: 16px; }}
    .grid, .kv {{ width: 100%; border-collapse: collapse; }}
    .grid th, .grid td, .kv th, .kv td {{ border-bottom: 1px solid var(--line); padding: 10px 12px; text-align: left; vertical-align: top; }}
    .grid th, .kv th {{ color: var(--muted); font-weight: 600; width: 180px; }}
    .pills {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }}
    .pill {{ background: var(--accent); color: #1f2937; border-radius: 999px; padding: 4px 10px; font-size: 12px; }}
    .badge {{ display: inline-flex; align-items: center; border-radius: 999px; padding: 4px 10px; font-size: 12px; font-weight: 700; }}
    .badge.neutral {{ background: var(--soft); color: var(--text); }}
    .badge.good {{ background: var(--good); color: var(--good-text); }}
    .badge.bad {{ background: var(--bad); color: var(--bad-text); }}
    .badge.warn {{ background: var(--warn); color: var(--warn-text); }}
    .meters {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin: 0 0 20px; }}
    .meter-card {{ background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 14px; }}
    .meter-head {{ display: flex; justify-content: space-between; gap: 12px; margin-bottom: 10px; font-size: 13px; color: var(--muted); }}
    .meter-head strong {{ color: var(--text); font-size: 14px; }}
    .meter-track {{ height: 10px; background: var(--soft); border-radius: 999px; overflow: hidden; }}
    .meter-fill {{ height: 100%; border-radius: 999px; }}
    .meter-fill.good {{ background: #10b981; }}
    .meter-fill.bad {{ background: #ef4444; }}
    .meter-fill.warn {{ background: #f59e0b; }}
    .meter-fill.accent {{ background: #3b82f6; }}
    .prompt-card {{ padding: 16px; margin-bottom: 12px; }}
    .detail-card {{ padding: 12px 14px; margin-bottom: 12px; }}
    .detail-card summary {{ cursor: pointer; font-weight: 600; }}
    pre {{ white-space: pre-wrap; word-break: break-word; background: var(--soft); padding: 12px; border-radius: 12px; overflow: auto; }}
    .mono-block strong {{ display: block; margin: 8px 0; }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>{escape(title)}</h1>
    <p>Generated by api-quality-check {escape(APP_VERSION)}.</p>
    <div class="stats">{summary}</div>
    {summary_bars}
    {''.join(sections)}
  </div>
</body>
</html>"""


def build_config_from_raw(raw: Dict[str, Any]) -> ProviderConfig:
    provider = raw.get("provider")
    input_base_url = raw.get("base_url")
    base_url = normalize_base_url(provider, input_base_url)
    api_key = raw.get("api_key")
    model_id = raw.get("model_id")
    headers = normalize_headers(raw.get("headers"))
    extra_body = raw.get("extra_body")
    if not provider or not base_url or not api_key or not model_id:
        raise ValueError("provider, base_url, api_key, and model_id are required.")
    extra_body_source = "user" if extra_body else "none"
    if not extra_body:
        extra_body = default_extra_body_for(provider, base_url, model_id)
        if extra_body:
            extra_body_source = "auto"
    return ProviderConfig(
        provider=provider,
        base_url=base_url,
        api_key=api_key,
        model_id=model_id,
        temperature=0.0,
        stream=False,
        timeout_seconds=DEFAULT_TIMEOUT_SECONDS,
        headers=headers,
        extra_body=extra_body,
        extra_body_source=extra_body_source,
        input_base_url=input_base_url,
    )


def build_config(args: argparse.Namespace) -> ProviderConfig:
    if args.config:
        raw = load_json(args.config)
    else:
        raw = {
            "provider": args.provider,
            "base_url": args.base_url,
            "api_key": args.api_key,
            "model_id": args.model_id,
        }
        headers = parse_json_object(getattr(args, "headers_json", None), field_name="headers")
        if headers:
            raw["headers"] = headers
    return build_config_from_raw(raw)


def load_config_list(path: str) -> List[Dict[str, Any]]:
    raw = load_json(path)
    if isinstance(raw, list):
        items = raw
    elif isinstance(raw, dict) and isinstance(raw.get("configs"), list):
        items = raw["configs"]
    else:
        raise ValueError("Batch config file must be a JSON array or an object with a top-level configs array.")
    if not items:
        raise ValueError("Batch config file is empty.")
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"Batch config item #{idx + 1} must be an object.")
    return items


def smoke_result_for_config(cfg: ProviderConfig) -> Dict[str, Any]:
    client = ApiClient(cfg)
    result: Dict[str, Any] = {
        "mode": "smoke",
        "provider_config": public_provider_config(cfg),
        "protocol": canonical_connection_type(cfg.provider, cfg.base_url),
    }
    try:
        first = client.request_text("x", max_tokens=1, stream=False, want_logprobs=False)
        result["first_token_text"] = first.get("text", "")
        result["b3it_supported"] = bool(result["first_token_text"])
        if first.get("request_profile"):
            result["first_token_request_profile"] = first["request_profile"]
    except Exception as exc:
        result["first_token_error"] = f"{type(exc).__name__}: {exc}"
        result["b3it_supported"] = False

    if canonical_connection_type(cfg.provider, cfg.base_url) != "Anthropic":
        try:
            lp = client.request_text("x", max_tokens=1, stream=False, want_logprobs=True, top_logprobs=10)
            result["lt_supported"] = bool(lp.get("logprob_dict"))
            result["logprob_preview"] = lp.get("logprob_dict")
            if lp.get("request_profile"):
                result["logprob_request_profile"] = lp["request_profile"]
        except Exception as exc:
            result["lt_supported"] = False
            result["logprob_error"] = f"{type(exc).__name__}: {exc}"
    else:
        result["lt_supported"] = False
        result["logprob_error"] = "Anthropic mode is treated as B3IT-only by this skill."
    if result.get("lt_supported"):
        result["recommended_detector"] = "LT-lite+B3IT-lite"
    elif result.get("b3it_supported"):
        result["recommended_detector"] = "B3IT-lite"
    else:
        result["recommended_detector"] = "unsupported"
    return result


def render_config_template(cfg: ProviderConfig, *, name: Optional[str] = None) -> Dict[str, Any]:
    template: Dict[str, Any] = {
        "provider": canonical_connection_type(cfg.provider, cfg.base_url),
        "base_url": cfg.base_url,
        "api_key": cfg.api_key,
        "model_id": cfg.model_id,
    }
    if name:
        template["name"] = name
    if cfg.headers:
        template["headers"] = cfg.headers
    if cfg.extra_body:
        template["extra_body"] = cfg.extra_body
    return template


def command_init_config(args: argparse.Namespace) -> Dict[str, Any]:
    cfg = build_config(args)
    template = render_config_template(cfg, name=getattr(args, "name", None))
    config_payload: Any = {"configs": [template]} if getattr(args, "batch", False) else template
    config_output = getattr(args, "config_output", None)
    if config_output:
        Path(config_output).write_text(
            json.dumps(config_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    smoke_target = config_output or "./provider.json"
    return {
        "mode": "init-config",
        "config_output": config_output,
        "config_format": "batch" if getattr(args, "batch", False) else "single",
        "template": config_payload,
        "normalized_provider": canonical_connection_type(cfg.provider, cfg.base_url),
        "normalized_base_url": cfg.base_url,
        "extra_body_source": cfg.extra_body_source,
        "recommended_smoke_command": f'python "$APIQ" smoke --config "{smoke_target}"',
    }


def command_init_batch_config(args: argparse.Namespace) -> Dict[str, Any]:
    items = load_config_list(args.configs)
    normalized_items: List[Dict[str, Any]] = []
    for index, item in enumerate(items, start=1):
        cfg = build_config_from_raw(item)
        label = item.get("name") or item.get("label") or item.get("model_id") or f"config-{index}"
        normalized_items.append(render_config_template(cfg, name=label))
    config_payload: Dict[str, Any] = {"configs": normalized_items}
    config_output = getattr(args, "config_output", None)
    if config_output:
        Path(config_output).write_text(
            json.dumps(config_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    batch_target = config_output or "./providers.json"
    return {
        "mode": "init-batch-config",
        "config_output": config_output,
        "config_count": len(normalized_items),
        "template": config_payload,
        "recommended_batch_smoke_command": f'python "$APIQ" batch-smoke --configs "{batch_target}"',
        "recommended_batch_pipeline_command": f'"$APIQ_BATCH" "{batch_target}" ./api-quality-out',
    }


def command_smoke(args: argparse.Namespace) -> Dict[str, Any]:
    cfg = build_config(args)
    return smoke_result_for_config(cfg)


def command_batch_smoke(args: argparse.Namespace) -> Dict[str, Any]:
    items = load_config_list(args.configs)
    results: List[Dict[str, Any]] = []
    b3it_supported_count = 0
    lt_supported_count = 0
    for index, item in enumerate(items, start=1):
        label = item.get("name") or item.get("label") or item.get("model_id") or f"config-{index}"
        try:
            cfg = build_config_from_raw(item)
            smoke = smoke_result_for_config(cfg)
            smoke["name"] = label
            smoke["index"] = index
            results.append(smoke)
            if smoke.get("b3it_supported"):
                b3it_supported_count += 1
            if smoke.get("lt_supported"):
                lt_supported_count += 1
        except Exception as exc:
            results.append(
                {
                    "name": label,
                    "index": index,
                    "mode": "smoke",
                    "b3it_supported": False,
                    "lt_supported": False,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
    return {
        "mode": "batch-smoke",
        "total_configs": len(items),
        "b3it_supported_count": b3it_supported_count,
        "lt_supported_count": lt_supported_count,
        "results": results,
    }


def load_prompts(path: Optional[str]) -> List[str]:
    if not path:
        return DEFAULT_LT_PROMPTS
    raw = load_json(path)
    if isinstance(raw, dict):
        prompts = raw.get("prompts", DEFAULT_LT_PROMPTS)
    elif isinstance(raw, list):
        prompts = raw
    else:
        raise ValueError("Prompts file must be a JSON array or an object with a top-level prompts array.")
    prompts = [str(item).strip() for item in prompts if str(item).strip()]
    if not prompts:
        raise ValueError("Prompts list is empty.")
    return prompts


def b3it_attempt_profiles(args: argparse.Namespace, cfg: ProviderConfig) -> List[Dict[str, int]]:
    provider = canonical_connection_type(cfg.provider, cfg.base_url)
    profiles = [
        {
            "candidate_count": args.candidate_count,
            "discovery_repeats": args.discovery_repeats,
            "keep_count": args.keep_count,
            "reference_samples": args.reference_samples,
        }
    ]
    if provider in {"OpenAI", "OpenAI-Compatible"}:
        fallback_profiles = [
            {
                "candidate_count": max(args.candidate_count, 36),
                "discovery_repeats": max(args.discovery_repeats, 3),
                "keep_count": args.keep_count,
                "reference_samples": max(args.reference_samples, 4),
            },
            {
                "candidate_count": max(args.candidate_count, 120),
                "discovery_repeats": max(args.discovery_repeats, 3),
                "keep_count": args.keep_count,
                "reference_samples": max(args.reference_samples, 12),
            },
        ]
        for profile in fallback_profiles:
            if profile not in profiles:
                profiles.append(profile)
    return profiles


def discover_b3it_baseline_with_fallbacks(
    engine: B3ITLiteEngine,
    cfg: ProviderConfig,
    args: argparse.Namespace,
) -> Dict[str, Any]:
    attempts: List[Dict[str, Any]] = []
    last_exc: Optional[Exception] = None
    for profile in b3it_attempt_profiles(args, cfg):
        try:
            baseline = engine.discover_baseline(
                candidate_count=profile["candidate_count"],
                discovery_repeats=profile["discovery_repeats"],
                keep_count=profile["keep_count"],
                reference_samples=profile["reference_samples"],
                temperature=0.0,
                seed=args.seed,
            )
            attempts.append({"status": "ok", **profile})
            baseline["search_attempts"] = attempts
            baseline["selected_search_profile"] = profile
            return baseline
        except RuntimeError as exc:
            if "No border inputs were found." not in str(exc):
                raise
            attempts.append({"status": "no-border-inputs", **profile})
            last_exc = exc
    if last_exc is not None:
        raise last_exc
    raise RuntimeError("No border inputs were found.")


def command_lt_baseline(args: argparse.Namespace) -> Dict[str, Any]:
    cfg = build_config(args)
    prompts = load_prompts(args.prompts)
    engine = LTLiteEngine(ApiClient(cfg))
    baseline = engine.collect_samples(
        prompts,
        runs_per_prompt=args.runs_per_prompt,
        top_logprobs=args.top_logprobs,
        temperature=1.0,
    )
    baseline["provider_config"] = public_provider_config(cfg)
    baseline["used_temperature"] = 1.0
    return baseline


def command_lt_detect(args: argparse.Namespace) -> Dict[str, Any]:
    cfg = build_config(args)
    baseline = load_json(args.baseline)
    engine = LTLiteEngine(ApiClient(cfg))
    current = engine.collect_samples(
        [p["prompt"] for p in baseline.get("prompts", [])],
        runs_per_prompt=args.runs_per_prompt,
        top_logprobs=args.top_logprobs,
        temperature=1.0,
    )
    report = engine.compare(baseline, current, permutations=args.permutations)
    report["provider_config"] = public_provider_config(cfg)
    report["baseline_file"] = args.baseline
    report["used_temperature"] = 1.0
    return report


def command_batch_lt_baseline(args: argparse.Namespace) -> Dict[str, Any]:
    items = load_config_list(args.configs)
    prompts = load_prompts(args.prompts)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    results: List[Dict[str, Any]] = []
    success_count = 0
    failure_count = 0
    for index, item in enumerate(items, start=1):
        label = item.get("name") or item.get("label") or item.get("model_id") or f"config-{index}"
        try:
            cfg = build_config_from_raw(item)
            engine = LTLiteEngine(ApiClient(cfg))
            baseline = engine.collect_samples(
                prompts,
                runs_per_prompt=args.runs_per_prompt,
                top_logprobs=args.top_logprobs,
                temperature=1.0,
            )
            baseline["provider_config"] = public_provider_config(cfg)
            baseline["used_temperature"] = 1.0
            baseline_name = f"{index:02d}-{slugify(label)}-lt-baseline.json"
            baseline_path = output_dir / baseline_name
            save_json(str(baseline_path), baseline)
            success_count += 1
            results.append(
                {
                    "name": label,
                    "index": index,
                    "status": "ok",
                    "baseline_file": str(baseline_path),
                    "prompt_count": len(baseline.get("prompts", [])),
                    "provider_config": public_provider_config(cfg),
                }
            )
        except Exception as exc:
            failure_count += 1
            results.append(
                {
                    "name": label,
                    "index": index,
                    "status": "error",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
    return {
        "mode": "batch-lt-baseline",
        "total_configs": len(items),
        "success_count": success_count,
        "failure_count": failure_count,
        "output_dir": str(output_dir),
        "prompts": prompts,
        "results": results,
    }


def command_batch_lt_detect(args: argparse.Namespace) -> Dict[str, Any]:
    manifest = load_json(args.baseline_manifest)
    results_in = manifest.get("results", []) if isinstance(manifest, dict) else []
    if not isinstance(results_in, list) or not results_in:
        raise ValueError("Baseline manifest must contain a non-empty top-level results array.")

    items = load_config_list(args.configs)
    config_by_key: Dict[str, Dict[str, Any]] = {}
    for index, item in enumerate(items, start=1):
        label = item.get("name") or item.get("label") or item.get("model_id") or f"config-{index}"
        config_by_key[str(index)] = item
        config_by_key[label] = item

    results: List[Dict[str, Any]] = []
    success_count = 0
    failure_count = 0
    changed_count = 0
    for item in results_in:
        label = item.get("name") or item.get("label") or item.get("model_id") or f"config-{item.get('index', '?')}"
        baseline_file = item.get("baseline_file")
        index = item.get("index")
        raw_cfg = config_by_key.get(label) or config_by_key.get(str(index))
        if item.get("status") != "ok":
            results.append(
                {
                    "name": label,
                    "index": index,
                    "status": "skipped",
                    "reason": "baseline failed",
                }
            )
            continue
        if not raw_cfg:
            failure_count += 1
            results.append(
                {
                    "name": label,
                    "index": index,
                    "status": "error",
                    "error": "Matching provider config was not found in the configs file.",
                }
            )
            continue
        if not baseline_file:
            failure_count += 1
            results.append(
                {
                    "name": label,
                    "index": index,
                    "status": "error",
                    "error": "Baseline file is missing from the manifest.",
                }
            )
            continue
        try:
            cfg = build_config_from_raw(raw_cfg)
            baseline = load_json(baseline_file)
            engine = LTLiteEngine(ApiClient(cfg))
            current = engine.collect_samples(
                [p["prompt"] for p in baseline.get("prompts", [])],
                runs_per_prompt=args.runs_per_prompt,
                top_logprobs=args.top_logprobs,
                temperature=1.0,
            )
            report = engine.compare(baseline, current, permutations=args.permutations)
            report["provider_config"] = public_provider_config(cfg)
            report["baseline_file"] = baseline_file
            report["used_temperature"] = 1.0
            success_count += 1
            if report.get("overall_changed"):
                changed_count += 1
            results.append(
                {
                    "name": label,
                    "index": index,
                    "status": "ok",
                    "overall_changed": report.get("overall_changed", False),
                    "changed_prompts": report.get("changed_prompts", 0),
                    "baseline_file": baseline_file,
                    "report": report,
                }
            )
        except Exception as exc:
            failure_count += 1
            results.append(
                {
                    "name": label,
                    "index": index,
                    "status": "error",
                    "baseline_file": baseline_file,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
    return {
        "mode": "batch-lt-detect",
        "total_configs": len(results_in),
        "success_count": success_count,
        "failure_count": failure_count,
        "changed_count": changed_count,
        "baseline_manifest": args.baseline_manifest,
        "results": results,
    }


def command_b3it_baseline(args: argparse.Namespace) -> Dict[str, Any]:
    cfg = build_config(args)
    engine = B3ITLiteEngine(ApiClient(cfg))
    baseline = discover_b3it_baseline_with_fallbacks(engine, cfg, args)
    baseline["provider_config"] = public_provider_config(cfg)
    baseline["used_temperature"] = 0.0
    return baseline


def command_b3it_detect(args: argparse.Namespace) -> Dict[str, Any]:
    cfg = build_config(args)
    baseline = load_json(args.baseline)
    engine = B3ITLiteEngine(ApiClient(cfg))
    report = engine.detect(
        baseline,
        detection_repeats=args.detection_repeats,
        temperature=0.0,
        min_stable_count=args.min_stable_count,
        min_stable_ratio=args.min_stable_ratio,
        confirm_passes=args.confirm_passes,
    )
    report["provider_config"] = public_provider_config(cfg)
    report["baseline_file"] = args.baseline
    report["used_temperature"] = 0.0
    return report


def command_batch_b3it_baseline(args: argparse.Namespace) -> Dict[str, Any]:
    items = load_config_list(args.configs)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    results: List[Dict[str, Any]] = []
    success_count = 0
    failure_count = 0
    for index, item in enumerate(items, start=1):
        label = item.get("name") or item.get("label") or item.get("model_id") or f"config-{index}"
        try:
            cfg = build_config_from_raw(item)
            engine = B3ITLiteEngine(ApiClient(cfg))
            baseline = discover_b3it_baseline_with_fallbacks(engine, cfg, args)
            baseline["provider_config"] = public_provider_config(cfg)
            baseline["used_temperature"] = 0.0
            baseline_name = f"{index:02d}-{slugify(label)}-b3it-baseline.json"
            baseline_path = output_dir / baseline_name
            save_json(str(baseline_path), baseline)
            success_count += 1
            results.append(
                {
                    "name": label,
                    "index": index,
                    "status": "ok",
                    "baseline_file": str(baseline_path),
                    "border_input_count": len(baseline.get("border_inputs", [])),
                    "provider_config": public_provider_config(cfg),
                }
            )
        except Exception as exc:
            failure_count += 1
            results.append(
                {
                    "name": label,
                    "index": index,
                    "status": "error",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
    return {
        "mode": "batch-b3it-baseline",
        "total_configs": len(items),
        "success_count": success_count,
        "failure_count": failure_count,
        "output_dir": str(output_dir),
        "results": results,
    }


def command_batch_b3it_detect(args: argparse.Namespace) -> Dict[str, Any]:
    manifest = load_json(args.baseline_manifest)
    results_in = manifest.get("results", []) if isinstance(manifest, dict) else []
    if not isinstance(results_in, list) or not results_in:
        raise ValueError("Baseline manifest must contain a non-empty top-level results array.")

    items = load_config_list(args.configs)
    config_by_key: Dict[str, Dict[str, Any]] = {}
    for index, item in enumerate(items, start=1):
        label = item.get("name") or item.get("label") or item.get("model_id") or f"config-{index}"
        config_by_key[str(index)] = item
        config_by_key[label] = item

    results: List[Dict[str, Any]] = []
    success_count = 0
    failure_count = 0
    changed_count = 0
    for item in results_in:
        label = item.get("name") or item.get("label") or item.get("model_id") or f"config-{item.get('index', '?')}"
        baseline_file = item.get("baseline_file")
        index = item.get("index")
        raw_cfg = config_by_key.get(label) or config_by_key.get(str(index))
        if item.get("status") != "ok":
            results.append(
                {
                    "name": label,
                    "index": index,
                    "status": "skipped",
                    "reason": "baseline failed",
                }
            )
            continue
        if not raw_cfg:
            failure_count += 1
            results.append(
                {
                    "name": label,
                    "index": index,
                    "status": "error",
                    "error": "Matching provider config was not found in the configs file.",
                }
            )
            continue
        if not baseline_file:
            failure_count += 1
            results.append(
                {
                    "name": label,
                    "index": index,
                    "status": "error",
                    "error": "Baseline file is missing from the manifest.",
                }
            )
            continue
        try:
            cfg = build_config_from_raw(raw_cfg)
            baseline = load_json(baseline_file)
            engine = B3ITLiteEngine(ApiClient(cfg))
            report = engine.detect(
                baseline,
                detection_repeats=args.detection_repeats,
                temperature=0.0,
                min_stable_count=args.min_stable_count,
                min_stable_ratio=args.min_stable_ratio,
                confirm_passes=args.confirm_passes,
            )
            report["provider_config"] = public_provider_config(cfg)
            report["baseline_file"] = baseline_file
            report["used_temperature"] = 0.0
            success_count += 1
            if report.get("overall_changed"):
                changed_count += 1
            results.append(
                {
                    "name": label,
                    "index": index,
                    "status": "ok",
                    "overall_changed": report.get("overall_changed", False),
                    "changed_prompts": report.get("changed_prompts", 0),
                    "stopped_early": report.get("stopped_early", False),
                    "baseline_file": baseline_file,
                    "report": report,
                }
            )
        except Exception as exc:
            failure_count += 1
            results.append(
                {
                    "name": label,
                    "index": index,
                    "status": "error",
                    "baseline_file": baseline_file,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
    return {
        "mode": "batch-b3it-detect",
        "total_configs": len(results_in),
        "success_count": success_count,
        "failure_count": failure_count,
        "changed_count": changed_count,
        "baseline_manifest": args.baseline_manifest,
        "results": results,
    }


def add_config_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", help="Path to a config JSON file.")
    parser.add_argument("--provider", help="OpenAI, OpenAI-Compatible, or Anthropic.")
    parser.add_argument("--base-url", help="API base URL.")
    parser.add_argument("--api-key", help="API key.")
    parser.add_argument("--model-id", help="Model ID.")
    parser.add_argument("--headers-json", help="Optional JSON object of request headers.")
    parser.add_argument("--output", help="Optional output JSON path.")
    parser.add_argument("--html-output", help="Optional output HTML path.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Headless API quality checks for coding-model endpoints.")
    sub = parser.add_subparsers(dest="command", required=True)

    init_config = sub.add_parser("init-config", help="Generate a normalized provider config JSON template.")
    init_config.add_argument("--config", help="Optional input config JSON to normalize.")
    init_config.add_argument("--provider", help="OpenAI, OpenAI-Compatible, or Anthropic.")
    init_config.add_argument("--base-url", help="API base URL or full endpoint URL.")
    init_config.add_argument("--api-key", help="API key.")
    init_config.add_argument("--model-id", help="Model ID.")
    init_config.add_argument("--headers-json", help="Optional JSON object of request headers.")
    init_config.add_argument("--name", help="Optional config name for batch workflows.")
    init_config.add_argument("--batch", action="store_true", help="Wrap the template in a top-level configs array.")
    init_config.add_argument("--config-output", help="Optional output path for the generated provider config JSON.")
    init_config.add_argument("--output", help="Optional output JSON path for the command result.")

    init_batch_config = sub.add_parser("init-batch-config", help="Generate a normalized providers.json template from a config list.")
    init_batch_config.add_argument("--configs", required=True, help="Path to a JSON array or object with a top-level configs array.")
    init_batch_config.add_argument("--config-output", help="Optional output path for the generated providers.json file.")
    init_batch_config.add_argument("--output", help="Optional output JSON path for the command result.")

    smoke = sub.add_parser("smoke", help="Check whether B3IT/LT prerequisites are available.")
    add_config_args(smoke)

    batch_smoke = sub.add_parser("batch-smoke", help="Run smoke checks for a list of provider configs.")
    batch_smoke.add_argument("--configs", required=True, help="Path to a JSON array or object with a top-level configs array.")
    batch_smoke.add_argument("--output", help="Optional output JSON path.")
    batch_smoke.add_argument("--html-output", help="Optional output HTML path.")

    batch_b3_base = sub.add_parser("batch-b3it-baseline", help="Build B3IT-lite baselines for a list of provider configs.")
    batch_b3_base.add_argument("--configs", required=True, help="Path to a JSON array or object with a top-level configs array.")
    batch_b3_base.add_argument("--output-dir", required=True, help="Directory where per-provider baseline JSON files will be written.")
    batch_b3_base.add_argument("--output", help="Optional summary manifest JSON path.")
    batch_b3_base.add_argument("--html-output", help="Optional output HTML path.")
    batch_b3_base.add_argument("--candidate-count", type=int, default=120)
    batch_b3_base.add_argument("--discovery-repeats", type=int, default=3)
    batch_b3_base.add_argument("--keep-count", type=int, default=5)
    batch_b3_base.add_argument("--reference-samples", type=int, default=12)
    batch_b3_base.add_argument("--seed", type=int, default=42)

    batch_b3_detect = sub.add_parser("batch-b3it-detect", help="Run B3IT-lite detection for a list of provider configs using a baseline manifest.")
    batch_b3_detect.add_argument("--configs", required=True, help="Path to a JSON array or object with a top-level configs array.")
    batch_b3_detect.add_argument("--baseline-manifest", required=True, help="Manifest JSON produced by batch-b3it-baseline.")
    batch_b3_detect.add_argument("--output", help="Optional summary report JSON path.")
    batch_b3_detect.add_argument("--html-output", help="Optional output HTML path.")
    batch_b3_detect.add_argument("--detection-repeats", type=int, default=5)
    batch_b3_detect.add_argument("--min-stable-count", type=int, default=DEFAULT_B3_STABLE_MIN_COUNT)
    batch_b3_detect.add_argument("--min-stable-ratio", type=float, default=DEFAULT_B3_STABLE_MIN_RATIO)
    batch_b3_detect.add_argument("--confirm-passes", type=int, default=1)

    batch_lt_base = sub.add_parser("batch-lt-baseline", help="Build LT-lite baselines for a list of provider configs.")
    batch_lt_base.add_argument("--configs", required=True, help="Path to a JSON array or object with a top-level configs array.")
    batch_lt_base.add_argument("--output-dir", required=True, help="Directory where per-provider LT baseline JSON files will be written.")
    batch_lt_base.add_argument("--output", help="Optional summary manifest JSON path.")
    batch_lt_base.add_argument("--html-output", help="Optional output HTML path.")
    batch_lt_base.add_argument("--prompts", help="Optional JSON file with a prompts array.")
    batch_lt_base.add_argument("--runs-per-prompt", type=int, default=12)
    batch_lt_base.add_argument("--top-logprobs", type=int, default=10)

    batch_lt_detect = sub.add_parser("batch-lt-detect", help="Run LT-lite detection for a list of provider configs using a baseline manifest.")
    batch_lt_detect.add_argument("--configs", required=True, help="Path to a JSON array or object with a top-level configs array.")
    batch_lt_detect.add_argument("--baseline-manifest", required=True, help="Manifest JSON produced by batch-lt-baseline.")
    batch_lt_detect.add_argument("--output", help="Optional summary report JSON path.")
    batch_lt_detect.add_argument("--html-output", help="Optional output HTML path.")
    batch_lt_detect.add_argument("--runs-per-prompt", type=int, default=6)
    batch_lt_detect.add_argument("--top-logprobs", type=int, default=10)
    batch_lt_detect.add_argument("--permutations", type=int, default=200)

    lt_base = sub.add_parser("lt-baseline", help="Build an LT-lite baseline JSON.")
    add_config_args(lt_base)
    lt_base.add_argument("--prompts", help="Optional JSON file with a top-level prompts array.")
    lt_base.add_argument("--runs-per-prompt", type=int, default=12)
    lt_base.add_argument("--top-logprobs", type=int, default=10)

    lt_detect = sub.add_parser("lt-detect", help="Run LT-lite detection from a baseline JSON.")
    add_config_args(lt_detect)
    lt_detect.add_argument("--baseline", required=True)
    lt_detect.add_argument("--runs-per-prompt", type=int, default=6)
    lt_detect.add_argument("--top-logprobs", type=int, default=10)
    lt_detect.add_argument("--permutations", type=int, default=200)

    b3_base = sub.add_parser("b3it-baseline", help="Build a B3IT-lite baseline JSON.")
    add_config_args(b3_base)
    b3_base.add_argument("--candidate-count", type=int, default=120)
    b3_base.add_argument("--discovery-repeats", type=int, default=3)
    b3_base.add_argument("--keep-count", type=int, default=5)
    b3_base.add_argument("--reference-samples", type=int, default=12)
    b3_base.add_argument("--seed", type=int, default=42)

    b3_detect = sub.add_parser("b3it-detect", help="Run B3IT-lite detection from a baseline JSON.")
    add_config_args(b3_detect)
    b3_detect.add_argument("--baseline", required=True)
    b3_detect.add_argument("--detection-repeats", type=int, default=5)
    b3_detect.add_argument("--min-stable-count", type=int, default=DEFAULT_B3_STABLE_MIN_COUNT)
    b3_detect.add_argument("--min-stable-ratio", type=float, default=DEFAULT_B3_STABLE_MIN_RATIO)
    b3_detect.add_argument("--confirm-passes", type=int, default=1)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "init-config":
        result = command_init_config(args)
    elif args.command == "init-batch-config":
        result = command_init_batch_config(args)
    elif args.command == "smoke":
        result = command_smoke(args)
    elif args.command == "batch-smoke":
        result = command_batch_smoke(args)
    elif args.command == "batch-lt-baseline":
        result = command_batch_lt_baseline(args)
    elif args.command == "batch-lt-detect":
        result = command_batch_lt_detect(args)
    elif args.command == "batch-b3it-baseline":
        result = command_batch_b3it_baseline(args)
    elif args.command == "batch-b3it-detect":
        result = command_batch_b3it_detect(args)
    elif args.command == "lt-baseline":
        result = command_lt_baseline(args)
    elif args.command == "lt-detect":
        result = command_lt_detect(args)
    elif args.command == "b3it-baseline":
        result = command_b3it_baseline(args)
    elif args.command == "b3it-detect":
        result = command_b3it_detect(args)
    else:
        parser.error(f"Unknown command: {args.command}")
        return 2

    save_json(getattr(args, "output", None), result)
    save_html(getattr(args, "html_output", None), render_html_report(result))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except requests.HTTPError as exc:
        response = exc.response
        detail = ""
        if response is not None:
            try:
                detail = response.text[:1200]
            except Exception:
                detail = ""
        sys.stderr.write(f"HTTPError: {exc}\n{detail}\n")
        raise
