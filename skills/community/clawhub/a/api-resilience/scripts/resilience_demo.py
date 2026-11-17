# -*- coding: utf-8 -*-
"""API 韧性演示：指数退避+抖动重试 + 熔断，模拟失败/恢复。零依赖。"""
import argparse, json, random, time

def call(fail_rate):
    return random.random() > fail_rate  # True=成功

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fail-rate", type=float, default=0.5)
    ap.add_argument("--max-retry", type=int, default=5)
    ap.add_argument("--breaker", type=int, default=3, help="连续失败多少触发熔断")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    consecutive_fail = 0
    opened = 0
    for attempt in range(1, a.max_retry + 1):
        ok = call(a.fail_rate)
        if ok:
            consecutive_fail = 0
            opened += 1
            if a.json:
                print(json.dumps({"attempt": attempt, "result": "ok", "breaker_open": False}, ensure_ascii=False))
            else:
                print(f"  尝试 {attempt}: ✅ 成功（熔断未触发）")
            break
        consecutive_fail += 1
        if consecutive_fail >= a.breaker:
            if a.json:
                print(json.dumps({"attempt": attempt, "result": "circuit_open", "breaker_open": True}, ensure_ascii=False))
            else:
                print(f"  尝试 {attempt}: 🔒 连续失败达 {a.breaker}，熔断！暂停后探测")
            break
        wait = (2 ** attempt) + random.uniform(0, 1)
        if a.json:
            print(json.dumps({"attempt": attempt, "result": "fail", "retry_after": round(wait, 2)}, ensure_ascii=False))
        else:
            print(f"  尝试 {attempt}: ❌ 失败，退避 {wait:.1f}s 后重试")
        time.sleep(0)  # 演示不真睡
    if a.json:
        print(json.dumps({"final": "ok" if opened else "blocked"}, ensure_ascii=False))
    else:
        print("  结论：", "✅ 调用成功" if opened else "🔒 已熔断/放弃")

if __name__ == "__main__":
    main()
