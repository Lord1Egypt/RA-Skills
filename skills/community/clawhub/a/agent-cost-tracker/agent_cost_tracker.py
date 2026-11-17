#!/usr/bin/env python3
"""
agent-cost-tracker.py - estimate LLM token usage + cost from agent run logs.

Agents burn money on tokens; this gives you a running tally from any text log
(pipes stdin, or scans a file for lines like "prompt_tokens: 123"). Zero deps.

Usage:
  python agent-cost-tracker.py tally <logfile> [--model gpt-4o] [--json]
  python agent-cost-tracker.py estimate --prompt 2000 --completion 500 --model claude-3-5-sonnet
  python agent-cost-tracker.py self-test
"""
import argparse
import json
import re
import sys

# rough per-1M-token USD pricing (input, output) - edit as prices change
PRICING = {
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-3.5-turbo": (0.50, 1.50),
    "claude-3-5-sonnet": (3.00, 15.00),
    "claude-3-haiku": (0.25, 1.25),
    "gemini-1.5-pro": (1.25, 5.00),
    "gemini-1.5-flash": (0.075, 0.30),
    "default": (1.00, 3.00),
}


def _price(model):
    for k, v in PRICING.items():
        if k in model.lower():
            return v
    return PRICING["default"]


def tally(logfile, model, as_json):
    txt = open(logfile, encoding="utf-8", errors="ignore").read()
    pin = sum(int(m) for m in re.findall(r'prompt[_ ]?tokens?[:=]\s*(\d+)', txt, re.I))
    pout = sum(int(m) for m in re.findall(r'completion[_ ]?tokens?[:=]\s*(\d+)', txt, re.I))
    # fallback: count 'tokens' lines of any kind
    if pin == 0 and pout == 0:
        pin = sum(int(m) for m in re.findall(r'tokens?[:=]\s*(\d+)', txt, re.I))
    ip, op = _price(model)
    cost = pin / 1_000_000 * ip + pout / 1_000_000 * op
    res = {"model": model, "prompt_tokens": pin, "completion_tokens": pout,
           "total_tokens": pin + pout, "est_cost_usd": round(cost, 4)}
    print(json.dumps(res, indent=2) if as_json else
          f"model={model} prompt={pin} completion={pout} total={pin+pout} ~${cost:.4f}")
    return res


def estimate(prompt, completion, model, as_json):
    ip, op = _price(model)
    cost = prompt / 1_000_000 * ip + completion / 1_000_000 * op
    res = {"model": model, "prompt_tokens": prompt, "completion_tokens": completion,
           "est_cost_usd": round(cost, 4)}
    print(json.dumps(res, indent=2) if as_json else f"~${cost:.4f} for {prompt}+{completion} tokens on {model}")
    return res


def self_test():
    import tempfile, os
    f = tempfile.NamedTemporaryFile("w", suffix=".log", delete=False)
    f.write("prompt_tokens: 1000\ncompletion_tokens: 500\nprompt_tokens: 200\n")
    f.close()
    r = tally(f.name, "gpt-4o", False)
    ok = r["prompt_tokens"] == 1200 and r["completion_tokens"] == 500
    os.unlink(f.name)
    print("self-test:", "PASS" if ok else "FAIL", f"(prompt={r['prompt_tokens']})")
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser(description="agent-cost-tracker")
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("tally"); t.add_argument("logfile"); t.add_argument("--model", default="default"); t.add_argument("--json", action="store_true")
    e = sub.add_parser("estimate"); e.add_argument("--prompt", type=int, required=True); e.add_argument("--completion", type=int, required=True); e.add_argument("--model", default="default"); e.add_argument("--json", action="store_true")
    sub.add_parser("self-test")
    a = p.parse_args()
    if a.cmd == "self-test": return self_test()
    if a.cmd == "tally": tally(a.logfile, a.model, a.json); return 0
    if a.cmd == "estimate": estimate(a.prompt, a.completion, a.model, a.json); return 0


if __name__ == "__main__":
    sys.exit(main())
