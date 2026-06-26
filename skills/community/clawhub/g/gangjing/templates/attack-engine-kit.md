# Attack Engine Kit

如果当前分发包没有 `scripts/` 目录，就把这里的模板代码写到当前工作区的临时文件里再运行。

规则：

- 只把模板落到**当前工作区**里的临时目录。
- 文件名保持为 `harness.py` / `harness.js`，方便和完整仓库版对齐。
- 只有在用户明确要求测试代码，或对当前工作区代码做出“绝对没问题”之类强断言时，才允许落地并执行。

## harness.py

```python
#!/usr/bin/env python3
"""
Break My Code — Attack Harness

Executes attack vectors against a target function and collects results.
The LLM generates attack_config.json, this script runs it and produces
structured output for the destruction report.

Usage:
    python harness.py attack_config.json [--timeout 5]

attack_config.json format:
{
  "target_module": "/path/to/target.py",
  "target_function": "function_name",
  "attacks": [
    {
      "name": "Attack name",
      "category": "Type Chaos",
      "severity": "HIGH",
      "payload_description": "human-readable description",
      "args": [arg1, arg2],
      "kwargs": {},
      "expected": "expected_value or null",
      "expect_exception": false,
      "validators": ["no_nan", "no_html", "no_invisible_unicode"]
    }
  ]
}
"""

import argparse
import importlib.util
import json
import math
import multiprocessing
import os
import re
import sys
import time
import unicodedata
from pathlib import Path


VERDICTS = {
    "crashed": "💥",
    "wrong": "🎯",
    "hung": "⏳",
    "leaked": "🔓",
    "survived": "🛡️",
}

SEVERITY_WEIGHTS = {"CRITICAL": 20, "HIGH": 10, "MEDIUM": 5, "LOW": 2}


# ---------------------------------------------------------------------------
# Semantic validators — catch silent failures that execution alone misses
# ---------------------------------------------------------------------------

def _deep_check(obj, predicate, path="root", _seen=None, _depth=0, _max_depth=50):
    """Walk a nested structure (dict/list) and apply predicate to all leaf values.
    Guards against circular references and excessive nesting."""
    if _depth > _max_depth:
        return [f"Max depth ({_max_depth}) exceeded at {path}"]
    if _seen is None:
        _seen = set()
    obj_id = id(obj)
    if isinstance(obj, (dict, list, tuple)):
        if obj_id in _seen:
            return [f"Circular reference detected at {path}"]
        _seen.add(obj_id)
    findings = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            findings.extend(_deep_check(v, predicate, f"{path}.{k}", _seen, _depth+1, _max_depth))
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            findings.extend(_deep_check(v, predicate, f"{path}[{i}]", _seen, _depth+1, _max_depth))
    else:
        hit = predicate(obj, path)
        if hit:
            findings.append(hit)
    return findings


def validate_no_nan(value):
    """Flag NaN or Infinity in return values — classic validation bypass."""
    import decimal
    def check(v, path):
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            return f"NaN/Inf found at {path}: {v!r}"
        if isinstance(v, decimal.Decimal) and (v.is_nan() or v.is_infinite()):
            return f"NaN/Inf found at {path}: {v!r}"
    return _deep_check(value, check)


def validate_no_html(value):
    """Flag stored HTML/script tags — potential XSS persistence."""
    pattern = re.compile(r"<\s*(script|img|svg|iframe|on\w+\s*=)", re.IGNORECASE)
    def check(v, path):
        if isinstance(v, str) and pattern.search(v):
            return f"Unsanitized HTML at {path}: {v[:80]!r}"
    return _deep_check(value, check)


def validate_no_invisible_unicode(value):
    """Flag zero-width chars, RTL overrides, and other invisible characters."""
    invisible_cats = {"Cf", "Mn", "Cc"}
    invisible_codepoints = {
        0x200B, 0x200C, 0x200D, 0xFEFF,  # zero-width
        0x202A, 0x202B, 0x202C, 0x202D, 0x202E,  # bidi
        0x2066, 0x2067, 0x2068, 0x2069,  # bidi isolate
    }
    def check(v, path):
        if isinstance(v, str):
            for ch in v:
                cp = ord(ch)
                if cp in invisible_codepoints or (unicodedata.category(ch) in invisible_cats and cp > 127):
                    return f"Invisible Unicode U+{cp:04X} ({unicodedata.name(ch, '?')}) at {path}"
    return _deep_check(value, check)


def validate_no_path_escape(value):
    """Flag path traversal sequences (../) in return values.
    Simple absolute paths are NOT flagged — only traversal patterns."""
    def check(v, path):
        if isinstance(v, str) and ".." in v and ("../" in v or "..\\" in v or v == ".."):
            return f"Path traversal at {path}: {v[:80]!r}"
    return _deep_check(value, check)


def validate_no_bool_as_int(value):
    """Flag booleans smuggled through as integers."""
    def check(v, path):
        if isinstance(v, bool):
            return f"Boolean value at {path}: {v!r} (may have been smuggled as int)"
    return _deep_check(value, check)


def validate_dict_field(value, field=None, expected=None, op="eq"):
    """Validate a specific field in a dict return value.
    Supports ops: eq, ne, lt, gt, le, ge."""
    if not isinstance(value, dict) or field is None:
        return []
    actual = value.get(field)
    ops = {"eq": lambda a,b: a==b, "ne": lambda a,b: a!=b,
           "lt": lambda a,b: a<b, "gt": lambda a,b: a>b,
           "le": lambda a,b: a<=b, "ge": lambda a,b: a>=b}
    check = ops.get(op, ops["eq"])
    if not check(actual, expected):
        return [f"Field '{field}': expected {op} {expected!r}, got {actual!r}"]
    return []


VALIDATORS = {
    "no_nan": validate_no_nan,
    "no_html": validate_no_html,
    "no_invisible_unicode": validate_no_invisible_unicode,
    "no_path_escape": validate_no_path_escape,
    "no_bool_as_int": validate_no_bool_as_int,
}


# ---------------------------------------------------------------------------
# Core execution engine
# ---------------------------------------------------------------------------

def load_target(module_path: str, function_name: str):
    """Dynamically load a function from a file path."""
    path = Path(module_path).resolve()
    spec = importlib.util.spec_from_file_location("target_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, function_name)


def resolve_target_path(config_path: str, target_module: str) -> Path:
    """Resolve target_module relative to the config and keep it in-bounds."""
    if not isinstance(target_module, str) or not target_module.strip():
        raise ValueError("config.target_module must be a non-empty string")

    config_dir = Path(config_path).resolve().parent
    target_path = (config_dir / target_module).resolve()

    try:
        target_path.relative_to(config_dir)
    except ValueError as exc:
        raise ValueError(
            f"Refusing to load a target outside the attack config directory: {target_module}"
        ) from exc

    if not target_path.is_file():
        raise FileNotFoundError(f"Target module not found: {target_path}")

    return target_path


def run_single_attack(target_func, attack, timeout):
    """Run one attack vector with timeout + semantic validation."""
    args = attack.get("args", [])
    kwargs = attack.get("kwargs", {})
    _UNSET = object()
    expected = attack.get("expected", _UNSET)
    expect_exception = attack.get("expect_exception", False)
    validator_names = attack.get("validators", [])

    result = {
        "name": attack["name"],
        "category": attack["category"],
        "severity": attack.get("severity", "MEDIUM"),
        "payload": attack.get("payload_description", str(args)),
        "verdict": None,
        "detail": None,
        "semantic_findings": [],
        "elapsed_ms": None,
    }

    def _execute(conn):
        try:
            start = time.monotonic()
            ret = target_func(*args, **kwargs)
            elapsed = (time.monotonic() - start) * 1000
            conn.send(("ok", ret, elapsed))
        except Exception as e:
            elapsed = (time.monotonic() - start) * 1000
            conn.send(("exception", f"{type(e).__name__}: {e}", elapsed))

    parent_conn, child_conn = multiprocessing.Pipe()
    proc = multiprocessing.Process(target=_execute, args=(child_conn,))
    proc.start()
    proc.join(timeout=timeout)

    if proc.is_alive():
        proc.terminate()
        proc.join(timeout=2)
        if proc.is_alive():
            proc.kill()
        result["verdict"] = "hung"
        result["detail"] = f"Did not complete within {timeout}s"
        return result

    if not parent_conn.poll():
        result["verdict"] = "crashed"
        result["detail"] = "Process died without sending result"
        return result

    status, value, elapsed = parent_conn.recv()
    result["elapsed_ms"] = round(elapsed, 2)

    if status == "exception":
        if expect_exception:
            result["verdict"] = "survived"
            result["detail"] = f"Raised expected exception: {value}"
        else:
            result["verdict"] = "crashed"
            result["detail"] = value
        return result

    # status == "ok"
    if expect_exception:
        result["verdict"] = "wrong"
        result["detail"] = f"Expected exception but got: {repr(value)}"
        return result

    if expected is not _UNSET and value != expected:
        result["verdict"] = "wrong"
        result["detail"] = f"Expected {repr(expected)}, got {repr(value)}"
        return result

    # Execution succeeded — now run semantic validators on the return value
    all_findings = []
    for vname in validator_names:
        validator_fn = VALIDATORS.get(vname)
        if validator_fn:
            findings = validator_fn(value)
            all_findings.extend(findings)

    if all_findings:
        result["semantic_findings"] = all_findings
        if any("HTML" in f or "Invisible" in f or "Path escape" in f for f in all_findings):
            result["verdict"] = "leaked"
        else:
            result["verdict"] = "wrong"
        result["detail"] = f"Execution OK, but semantic check failed: {'; '.join(all_findings)}"
    else:
        result["verdict"] = "survived"
        detail_val = repr(value)
        if len(detail_val) > 200:
            detail_val = detail_val[:200] + "..."
        result["detail"] = f"Returned {detail_val}" + (" (correct)" if expected is not None else "")

    return result


def calculate_score(results):
    """Calculate resilience score from attack results."""
    total = len(results)
    if total == 0:
        return 100

    penalty = 0
    max_penalty = 0
    for r in results:
        w = SEVERITY_WEIGHTS.get(r["severity"], 5)
        max_penalty += w
        if r["verdict"] != "survived":
            penalty += w

    if max_penalty == 0:
        return 100
    return max(0, round(100 * (1 - penalty / max_penalty)))


def grade(score):
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 40:
        return "D"
    return "F"


def main():
    parser = argparse.ArgumentParser(description="Break My Code attack harness")
    parser.add_argument("config", help="Path to attack_config.json")
    parser.add_argument("--timeout", type=int, default=5,
                        help="Per-attack timeout in seconds")
    parser.add_argument("--output", "-o",
                        help="Output JSON file (default: stdout)")
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    target_path = resolve_target_path(args.config, config["target_module"])
    target_func = load_target(str(target_path), config["target_function"])
    attacks = config["attacks"]
    results = []

    for i, attack in enumerate(attacks):
        sys.stderr.write(f"[{i+1}/{len(attacks)}] {attack['name']}...")
        result = run_single_attack(target_func, attack, args.timeout)
        symbol = VERDICTS.get(result["verdict"], "?")
        sys.stderr.write(f" {symbol} {result['verdict'].upper()}")
        if result["semantic_findings"]:
            sys.stderr.write(f" (semantic: {len(result['semantic_findings'])} finding(s))")
        sys.stderr.write("\n")
        results.append(result)

    score = calculate_score(results)
    output = {
        "target": f"{target_path}::{config['target_function']}",
        "total_attacks": len(results),
        "summary": {
            v: sum(1 for r in results if r["verdict"] == v)
            for v in VERDICTS
        },
        "resilience_score": score,
        "grade": grade(score),
        "results": results,
    }

    json_output = json.dumps(output, indent=2, ensure_ascii=False, default=str)

    if args.output:
        with open(args.output, "w") as f:
            f.write(json_output)
        sys.stderr.write(f"\nResults written to {args.output}\n")
    else:
        print(json_output)

    sys.stderr.write(f"\n{'='*50}\n")
    sys.stderr.write(f"RESILIENCE SCORE: {score}/100 (Grade: {grade(score)})\n")
    survived = output["summary"]["survived"]
    sys.stderr.write(f"Survived: {survived}/{len(results)}")
    semantic_total = sum(len(r["semantic_findings"]) for r in results)
    if semantic_total:
        sys.stderr.write(f" | Semantic findings: {semantic_total}")
    sys.stderr.write(f"\n{'='*50}\n")


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn", force=True)
    main()
```

## harness.js

```javascript
#!/usr/bin/env node
/**
 * Break My Code — JS Attack Harness (v2)
 *
 * Process-isolated execution: each attack runs in a child_process.fork()
 * with a per-attack timeout. If the child hangs or crashes, the parent
 * kills it and records the verdict.
 *
 * Usage:
 *   node harness.js attack_config.json [--timeout 5] [-o output.json]
 */
const { fork } = require("child_process");
const fs = require("fs");
const path = require("path");

const VERDICTS = { crashed: "\u{1F4A5}", wrong: "\u{1F3AF}", hung: "\u23F3", leaked: "\u{1F513}", survived: "\u{1F6E1}\uFE0F" };
const SEV_W = { CRITICAL: 20, HIGH: 10, MEDIUM: 5, LOW: 2 };

// ── Child worker mode ───────────────────────────────────────────────
// When invoked with --worker, this script runs a single attack in an
// isolated process and sends the result back via IPC.
if (process.argv.includes("--worker")) {
  const UNSET = Symbol("UNSET");
  const PROTO_KEYS = ["isAdmin", "role", "admin", "polluted", "__admin"];

  function cleanProto() {
    for (const k of PROTO_KEYS) {
      try { delete Object.prototype[k]; } catch (_) {}
    }
  }

  function vNoProto(_val) {
    const f = [];
    for (const k of PROTO_KEYS) {
      if (Object.prototype[k] !== undefined)
        f.push(`Object.prototype.${k} = ${JSON.stringify(Object.prototype[k])}`);
    }
    if (({}).isAdmin === true) f.push("({}).isAdmin === true");
    return f;
  }

  function vNoHtml(val) {
    const f = [], pat = /<\s*(script|img|svg|iframe|on\w+\s*=)/i;
    (function walk(v, p) {
      if (typeof v === "string" && pat.test(v)) f.push(`HTML at ${p}: ${v.slice(0, 80)}`);
      else if (v && typeof v === "object" && !Array.isArray(v))
        for (const [k, x] of Object.entries(v)) walk(x, `${p}.${k}`);
      else if (Array.isArray(v))
        v.forEach((x, i) => walk(x, `${p}[${i}]`));
    })(val, "root");
    return f;
  }

  function vNoNaN(val) {
    const f = [];
    (function walk(v, p) {
      if (typeof v === "number" && (Number.isNaN(v) || !Number.isFinite(v)))
        f.push(`NaN/Inf at ${p}: ${v}`);
      else if (v && typeof v === "object" && !Array.isArray(v))
        for (const [k, x] of Object.entries(v)) walk(x, `${p}.${k}`);
      else if (Array.isArray(v))
        v.forEach((x, i) => walk(x, `${p}[${i}]`));
    })(val, "root");
    return f;
  }

  const VALIDATORS = { no_proto_pollution: vNoProto, no_html: vNoHtml, no_nan: vNoNaN };

  function isThenable(v) { return v && typeof v === "object" && typeof v.then === "function"; }

  function judgeReturn(ret, result, expectException, expected, validators) {
    if (expectException) {
      result.verdict = "wrong";
      result.detail = `Expected throw but got: ${safeStr(ret)}`;
    } else if (expected !== UNSET) {
      if (!deepEqual(expected, ret)) {
        result.verdict = "wrong";
        result.detail = `Expected ${safeStr(expected).slice(0, 80)}, got ${safeStr(ret).slice(0, 120)}`;
      }
    }

    if (!result.verdict) {
      const findings = [];
      for (const vn of validators) {
        const vfn = VALIDATORS[vn];
        if (vfn) findings.push(...vfn(ret));
      }
      if (findings.length) {
        result.semantic_findings = findings;
        result.verdict = findings.some(f => /pollut|HTML/i.test(f)) ? "leaked" : "wrong";
        result.detail = `Semantic: ${findings.join("; ")}`;
      } else {
        result.verdict = "survived";
        result.detail = safeStr(ret).slice(0, 200);
      }
    }
  }

  function handleError(e, result, expectException) {
    if (expectException) {
      result.verdict = "survived";
      result.detail = `Threw ${e.constructor?.name || "Error"} (expected): ${e.message}`.slice(0, 200);
    } else {
      result.verdict = "crashed";
      result.detail = `${e.constructor?.name || "Error"}: ${e.message}`.slice(0, 200);
    }
  }

  process.on("message", (msg) => {
    const { targetPath, attack } = msg;
    const { name, category, severity = "MEDIUM", payload_description } = attack;
    const funcName = attack.function || attack.target_function;
    const args = attack.args || [];
    const expectException = attack.expect_exception || false;
    const expected = "expected" in attack ? attack.expected : UNSET;
    const validators = attack.validators || [];

    const result = {
      name, category, severity,
      payload: payload_description || JSON.stringify(args).slice(0, 200),
      verdict: null, detail: null, semantic_findings: [],
    };

    cleanProto();

    function finish() {
      cleanProto();
      process.send(result);
      process.exit(0);
    }

    try {
      const targetModule = require(targetPath);
      const fn = targetModule[funcName];
      if (typeof fn !== "function") {
        result.verdict = "crashed";
        result.detail = `Function '${funcName}' not found`;
        finish();
        return;
      }

      const ret = fn(...args);

      if (isThenable(ret)) {
        ret.then((resolved) => {
          judgeReturn(resolved, result, expectException, expected, validators);
          finish();
        }).catch((e) => {
          handleError(e, result, expectException);
          finish();
        });
      } else {
        judgeReturn(ret, result, expectException, expected, validators);
        finish();
      }
    } catch (e) {
      handleError(e, result, expectException);
      finish();
    }
  });

  function safeStr(v) {
    try { return JSON.stringify(v) || String(v); }
    catch (_) { return String(v); }
  }

  function deepEqual(a, b) {
    if (a === b) return true;
    if (a == null || b == null) return a === b;
    if (typeof a !== typeof b) return false;
    if (typeof a !== "object") return false;
    if (Array.isArray(a) !== Array.isArray(b)) return false;
    if (a instanceof Date && b instanceof Date) return a.getTime() === b.getTime();
    if (a instanceof RegExp && b instanceof RegExp) return a.toString() === b.toString();
    const ka = Object.keys(a), kb = Object.keys(b);
    if (ka.length !== kb.length) return false;
    return ka.every(k => deepEqual(a[k], b[k]));
  }

  return;
}

// ── Parent orchestrator ─────────────────────────────────────────────

function runAttackIsolated(targetPath, attack, timeoutSec) {
  return new Promise((resolve) => {
    const child = fork(__filename, ["--worker"], {
      stdio: ["pipe", "pipe", "pipe", "ipc"],
      timeout: (timeoutSec + 1) * 1000,
    });

    let settled = false;
    const timer = setTimeout(() => {
      if (!settled) {
        settled = true;
        child.kill("SIGKILL");
        resolve({
          name: attack.name, category: attack.category,
          severity: attack.severity || "MEDIUM",
          payload: attack.payload_description || JSON.stringify(attack.args || []).slice(0, 200),
          verdict: "hung", detail: `Timed out (${timeoutSec}s)`,
          semantic_findings: [],
        });
      }
    }, timeoutSec * 1000);

    child.on("message", (result) => {
      if (!settled) {
        settled = true;
        clearTimeout(timer);
        resolve(result);
      }
    });

    child.on("exit", (code) => {
      if (!settled) {
        settled = true;
        clearTimeout(timer);
        resolve({
          name: attack.name, category: attack.category,
          severity: attack.severity || "MEDIUM",
          payload: attack.payload_description || JSON.stringify(attack.args || []).slice(0, 200),
          verdict: "crashed", detail: `Child exited with code ${code}`,
          semantic_findings: [],
        });
      }
    });

    child.on("error", (err) => {
      if (!settled) {
        settled = true;
        clearTimeout(timer);
        resolve({
          name: attack.name, category: attack.category,
          severity: attack.severity || "MEDIUM",
          payload: attack.payload_description || "",
          verdict: "crashed", detail: `Fork error: ${err.message}`,
          semantic_findings: [],
        });
      }
    });

    child.send({ targetPath, attack });
  });
}

async function main() {
  const args = process.argv.slice(2);
  let configPath = null, timeout = 5, outputPath = null;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--timeout" && args[i + 1]) { timeout = parseInt(args[++i], 10); }
    else if ((args[i] === "-o" || args[i] === "--output") && args[i + 1]) { outputPath = args[++i]; }
    else if (!configPath && args[i] !== "--worker") { configPath = args[i]; }
  }

  if (Number.isNaN(timeout) || timeout <= 0) {
    process.stderr.write(`Invalid timeout: ${timeout}, using default 5s\n`);
    timeout = 5;
  }

  if (!configPath) {
    process.stderr.write("Usage: node harness.js config.json [--timeout 5] [-o out.json]\n");
    process.exit(1);
  }

  const config = JSON.parse(fs.readFileSync(configPath, "utf8"));
  const configDir = path.resolve(path.dirname(configPath));
  const targetPath = resolveTargetPath(configDir, config.target_module);
  const attacks = config.attacks;
  const results = [];

  process.stderr.write(`${"=".repeat(60)}\n  \u{1F480} ${config.target_module}\n${"=".repeat(60)}\n`);

  for (let i = 0; i < attacks.length; i++) {
    const r = await runAttackIsolated(targetPath, attacks[i], timeout);
    const sym = VERDICTS[r.verdict] || "?";
    const sem = (r.semantic_findings || []).length ? " [sem]" : "";
    process.stderr.write(`  [${String(i + 1).padStart(2)}/${attacks.length}] ${sym} ${r.verdict.toUpperCase().padEnd(10)} [${(r.severity || "MEDIUM").padEnd(8)}] ${r.name}${sem}\n`);
    results.push(r);
  }

  let penalty = 0, maxP = 0;
  for (const r of results) {
    const w = SEV_W[r.severity] || 5;
    maxP += w;
    if (r.verdict !== "survived") penalty += w;
  }
  const score = maxP > 0 ? Math.max(0, Math.round(100 * (1 - penalty / maxP))) : 100;
  const grade = score >= 90 ? "A" : score >= 75 ? "B" : score >= 60 ? "C" : score >= 40 ? "D" : "F";
  const summary = {};
  for (const v of Object.keys(VERDICTS)) summary[v] = results.filter(r => r.verdict === v).length;

  const output = {
    target: config.target_module,
    total_attacks: results.length,
    summary, resilience_score: score, grade, results,
  };

  const jsonStr = JSON.stringify(output, null, 2);
  if (outputPath) {
    fs.writeFileSync(outputPath, jsonStr);
    process.stderr.write(`\nResults: ${outputPath}\n`);
  } else {
    process.stdout.write(jsonStr + "\n");
  }
  process.stderr.write(`\n  \u2192 Score: ${score}/100 (Grade: ${grade})\n`);
}

function resolveTargetPath(configDir, targetModule) {
  if (typeof targetModule !== "string" || !targetModule.trim()) {
    throw new Error("config.target_module must be a non-empty string");
  }

  const resolved = path.resolve(configDir, targetModule);
  const relative = path.relative(configDir, resolved);
  const escapesConfigDir = relative.startsWith("..") || path.isAbsolute(relative);

  if (escapesConfigDir) {
    throw new Error(
      `Refusing to load a target outside the attack config directory: ${targetModule}`
    );
  }

  const stat = fs.statSync(resolved, { throwIfNoEntry: false });
  if (!stat || !stat.isFile()) {
    throw new Error(`Target module not found: ${resolved}`);
  }

  return resolved;
}

main().catch(e => { process.stderr.write(`Fatal: ${e.message}\n`); process.exit(1); });
```
