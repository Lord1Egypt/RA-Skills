#!/usr/bin/env python3
"""cost-monitor: per-turn cost calculator with balance tracking.
Usage: cost.py <session_jsonl> <model> [--set-balance N]
"""
import sys, os, json
from datetime import datetime, timezone, timedelta

SCRIPT_DIR = os.path.dirname(os.path.dirname(__file__))
PRICING_FILE = os.path.join(SCRIPT_DIR, "pricing.json")
BALANCE_FILE = os.path.join(SCRIPT_DIR, "balance.json")

def load_json(path):
    with open(path) as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def fmt_tokens(n):
    if n >= 1_000_000: return f"{n/1_000_000:.1f}M"
    if n >= 1000: return f"{n/1000:.1f}k"
    return str(n)

def fmt_credits(n):
    if n >= 1_000_000_000: return f"{n/1_000_000_000:.2f}B"
    if n >= 1_000_000: return f"{n/1_000_000:.1f}M"
    if n >= 1000: return f"{n/1000:.1f}k"
    return str(int(n))

def get_last_usage(transcript_path):
    last = None
    with open(transcript_path) as f:
        for line in f:
            try:
                e = json.loads(line.strip())
                msg = e.get("message", {})
                if isinstance(msg, dict) and msg.get("role") == "assistant" and "usage" in msg:
                    if msg.get("stopReason") not in ("toolUse", "error"):
                        last = msg["usage"]
            except:
                continue
    return last

def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print("Usage: cost.py <session_jsonl> <model> [--set-balance N]", file=sys.stderr)
        sys.exit(1)

    transcript_path = args[0]
    model = args[1]
    set_balance = None
    for i, a in enumerate(args[2:]):
        if a == "--set-balance" and i + 1 < len(args[2:]):
            set_balance = float(args[2:][i + 1])

    pricing = load_json(PRICING_FILE)
    balance = load_json(BALANCE_FILE)
    usage = get_last_usage(transcript_path)
    if not usage:
        print("No usage data yet")
        return

    # --- Phase 1: Set new balance (if --set-balance) ---
    if set_balance is not None:
        if model.startswith("mimo"):
            mb = balance.setdefault("mimo", {})
            plan_total = mb.get("total_credits", pricing.get("plans", {}).get("mimo", {}).get(mb.get("plan","standard"), {}).get("credits", 11000000000))
            mb["consumed_credits"] = int(plan_total - set_balance)
            mb["total_credits"] = plan_total
        else:
            balance.setdefault("deepseek", {})["balance_rmb"] = set_balance
        save_json(BALANCE_FILE, balance)

    # --- Phase 2: Calculate cost & deduct ---
    inp = usage.get("input", 0)
    out = usage.get("output", 0)
    cache = usage.get("cacheRead", 0)
    total_prompt = inp + cache
    cache_pct = (cache * 100 // total_prompt) if total_prompt > 0 else 0
    token_part = f"in {fmt_tokens(inp)}+{fmt_tokens(cache)}cached({cache_pct}%) · out {fmt_tokens(out)}"

    if model.startswith("mimo"):
        ct = pricing.get("credits_per_token", {})
        p = ct.get(model, ct["mimo-v2.5"])
        turn_c = inp * p["input"] + cache * p["cache"] + out * p["output"]
        # Apply nighttime coefficient (00:00-08:00 Beijing Time = 0.8x)
        now_bj = datetime.now(timezone(timedelta(hours=8)))
        if 0 <= now_bj.hour < 8:
            night_coeff = pricing.get("plans", {}).get("mimo", {}).get("nighttime_coefficient", 1.0)
            turn_c = int(turn_c * night_coeff)
        mb = balance.setdefault("mimo", {})
        mb["consumed_credits"] = mb.get("consumed_credits", 0) + turn_c
        rem = mb.get("total_credits", 0) - mb.get("consumed_credits", 0)
        pct = max(0, rem * 100.0 / mb.get("total_credits", 1))
        save_json(BALANCE_FILE, balance)
        print(f"MiMo：{pct:.1f}% | {fmt_credits(turn_c)} · {token_part}")
        return

    rmb_p = pricing.get("rmb_per_million_tokens", {}).get(model)
    if rmb_p:
        turn_cost = inp / 1_000_000 * rmb_p["input"] + cache / 1_000_000 * rmb_p["cache"] + out / 1_000_000 * rmb_p["output"]
        if not model.startswith("mimo"):
            ds = balance.setdefault("deepseek", {})
            ds["balance_rmb"] = round(ds.get("balance_rmb", 0) - turn_cost, 2)
            save_json(BALANCE_FILE, balance)
            remaining = ds["balance_rmb"]
            print(f"DeepSeek：¥{remaining:.2f} | ¥{turn_cost:.4f} · {token_part}")
            return

    print(f"Unknown model: {model}")

if __name__ == "__main__":
    main()
