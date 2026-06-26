#!/usr/bin/env python3
"""calibrate.py: 校准余额并扣除当次消耗
Usage:
  calibrate.py deepseek <transcript> [api_key]    # 自动查询 DeepSeek 余额
  calibrate.py mimo <transcript> <consumed> <total>  # 手动输入 MIMO 余量
"""
import sys, os, json, subprocess, re

SCRIPT_DIR = os.path.dirname(__file__)
BALANCE_FILE = os.path.join(SCRIPT_DIR, "..", "balance.json")
COST_SCRIPT = os.path.join(SCRIPT_DIR, "cost.py")

def load_balance():
    with open(BALANCE_FILE) as f:
        return json.load(f)

def save_balance(b):
    with open(BALANCE_FILE, "w") as f:
        json.dump(b, f, indent=2, ensure_ascii=False)

def get_deepseek_balance(api_key=None):
    """调用 DeepSeek API 查询余额"""
    # 从 openclaw config 获取 api_key
    if not api_key:
        config_path = os.path.expanduser("~/.openclaw/openclaw.json")
        with open(config_path) as f:
            config = json.load(f)
        ds = config.get("models", {}).get("providers", {}).get("deepseek", {})
        api_key = ds.get("apiKey", "")
        # 可能是 file reference
        if api_key.startswith("file:"):
            secret_path = os.path.expanduser("~/.openclaw/" + api_key.replace("file:", ""))
            with open(secret_path) as f:
                api_key = f.read().strip()

    # 调用 API
    import urllib.request
    req = urllib.request.Request(
        "https://api.deepseek.com/user/balance",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())

    # 解析余额
    balance = 0
    for info in data.get("balance_infos", []):
        if info.get("currency") == "CNY":
            balance = float(info.get("total_balance", 0))
            break
    return balance

def get_current_usage(transcript_path):
    """获取当前轮的 usage"""
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

def fmt_tokens(n):
    if n >= 1_000_000: return f"{n/1_000_000:.1f}M"
    if n >= 1000: return f"{n/1000:.1f}k"
    return str(n)

def fmt_credits(n):
    if n >= 1_000_000_000: return f"{n/1_000_000_000:.2f}B"
    if n >= 1_000_000: return f"{n/1_000_000:.1f}M"
    if n >= 1000: return f"{n/1000:.1f}k"
    return str(int(n))

def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)

    provider = args[0]
    transcript_path = args[1]

    # 加载配置
    pricing_path = os.path.join(SCRIPT_DIR, "..", "pricing.json")
    with open(pricing_path) as f:
        pricing = json.load(f)

    usage = get_current_usage(transcript_path)
    if not usage:
        print("No usage data yet")
        return

    inp = usage.get("input", 0)
    out = usage.get("output", 0)
    cache = usage.get("cacheRead", 0)
    total_prompt = inp + cache
    cache_pct = (cache * 100 // total_prompt) if total_prompt > 0 else 0
    token_part = f"in {fmt_tokens(inp)}+{fmt_tokens(cache)}cached({cache_pct}%) · out {fmt_tokens(out)}"

    balance = load_balance()

    if provider == "deepseek":
        # 查询 DeepSeek 余额
        api_key = args[2] if len(args) > 2 else None
        raw_balance = get_deepseek_balance(api_key)

        # 计算当次消耗
        rmb_p = pricing["rmb_per_million_tokens"]["deepseek-v4-flash"]
        turn_cost = inp / 1_000_000 * rmb_p["input"] + cache / 1_000_000 * rmb_p["cache"] + out / 1_000_000 * rmb_p["output"]
        remaining = round(raw_balance - turn_cost, 2)

        # 更新余额
        balance.setdefault("deepseek", {})["balance_rmb"] = remaining
        save_balance(balance)

        print(f"DeepSeek 余额校准：¥{raw_balance:.2f} - ¥{turn_cost:.4f} = ¥{remaining:.2f}")

    elif provider == "mimo":
        # 手动输入 MIMO 余量
        consumed = int(args[2].replace(",", ""))
        total = int(args[3].replace(",", ""))

        # 计算当次消耗
        ct = pricing.get("credits_per_token", {})
        p = ct.get("mimo-v2.5", ct["mimo-v2.5"])

        # 夜间系数
        from datetime import datetime, timezone, timedelta
        now_bj = datetime.now(timezone(timedelta(hours=8)))
        night_coeff = 0.8 if 0 <= now_bj.hour < 8 else 1.0

        turn_c = int((inp * p["input"] + cache * p["cache"] + out * p["output"]) * night_coeff)

        # 扣除当次消耗
        actual_consumed = consumed + turn_c
        remaining = total - actual_consumed
        pct = remaining * 100.0 / total

        # 更新余额
        mb = balance.setdefault("mimo", {})
        mb["total_credits"] = total
        mb["consumed_credits"] = actual_consumed
        save_balance(balance)

        print(f"MIMO 余额校准：已用 {fmt_credits(actual_consumed)} / {fmt_credits(total)}，剩余 {fmt_credits(remaining)} ({pct:.1f}%)")
    else:
        print(f"Unknown provider: {provider}")
        sys.exit(1)

if __name__ == "__main__":
    main()
