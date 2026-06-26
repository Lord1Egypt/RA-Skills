#!/usr/bin/env python3
"""
billing.py — SkillPay 计费（独立模块）

命令：
  charge   --user_id UID --amount USDT --label TEXT
  balance  --user_id UID
  link     --user_id UID --amount USDT
"""

import argparse, json, sys, urllib.request, urllib.error

SKILLPAY_BASE     = "https://skillpay.me"
SKILLPAY_SKILL_ID = "fac71b6b-43eb-47c9-9973-9bc2f4606577"
SKILLPAY_API_KEY  = "sk_e8d7b86db13746fdbdd3a02d34f118a276d32629b3ef8bc55838d68f560e2c1b"


def out(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))

def err(msg):
    out({"error": msg})
    sys.exit(1)

def headers():
    return {"X-API-Key": SKILLPAY_API_KEY, "Content-Type": "application/json"}

def post(path, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{SKILLPAY_BASE}{path}", data=data, headers=headers(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        err(f"SkillPay HTTP {e.code}: {e.read().decode(errors='replace')}")
    except Exception as e:
        # 计费服务不可用时放行，不阻断用户
        return {"success": True, "_fallback": True}

def get(path):
    req = urllib.request.Request(
        f"{SKILLPAY_BASE}{path}", headers=headers())
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        err(f"SkillPay 请求失败: {e}")


def cmd_charge(args):
    if not args.user_id:
        out({"success": True, "_skipped": "no user_id"})
        return

    result = post("/api/v1/billing/charge", {
        "user_id":  args.user_id,
        "skill_id": SKILLPAY_SKILL_ID,
        "amount":   float(args.amount),
    })

    if result.get("success"):
        out({"success": True, "balance": result.get("balance"),
             "label": args.label, "charged": float(args.amount)})
    else:
        # 余额不足，返回充值链接
        payment_url = result.get("payment_url", "")
        if not payment_url:
            link_result = post("/api/v1/billing/payment-link", {
                "user_id": args.user_id,
                "amount":  float(args.amount),
            })
            payment_url = link_result.get("payment_url", SKILLPAY_BASE)

        out({"success": False, "error": "payment_required",
             "balance": result.get("balance", 0),
             "required": float(args.amount),
             "payment_url": payment_url,
             "message": f"余额不足，无法执行「{args.label}」。充值链接：{payment_url}"})
        sys.exit(2)


def cmd_balance(args):
    result = get(f"/api/v1/billing/balance?user_id={args.user_id}")
    out({"user_id": args.user_id, "balance": result.get("balance", 0)})


def cmd_link(args):
    result = post("/api/v1/billing/payment-link", {
        "user_id": args.user_id,
        "amount":  float(args.amount),
    })
    out({"payment_url": result.get("payment_url", ""),
         "user_id": args.user_id, "amount": float(args.amount)})


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd")

    c = sub.add_parser("charge")
    c.add_argument("--user_id", required=True)
    c.add_argument("--amount",  required=True)
    c.add_argument("--label",   default="操作")

    b = sub.add_parser("balance")
    b.add_argument("--user_id", required=True)

    l = sub.add_parser("link")
    l.add_argument("--user_id", required=True)
    l.add_argument("--amount",  default="1.0")

    args = p.parse_args()
    if   args.cmd == "charge":  cmd_charge(args)
    elif args.cmd == "balance": cmd_balance(args)
    elif args.cmd == "link":    cmd_link(args)
    else: err("请指定命令: charge | balance | link")

if __name__ == "__main__":
    main()
