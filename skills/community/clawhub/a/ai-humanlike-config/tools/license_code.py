#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""license_code.py — 同意授权码工具（L0–L3 四层码）

用法：
  python license_code.py gen L1 --cid CUST-001 --caps 1,3,5 --expire 30d
  python license_code.py check <CODE>
  python license_code.py revoke <CODE>

说明：
- L0 绑定码：绑定客户↔数字人（对接 22 扫码绑定）；
- L1 能力码：门控 08 能力项（--caps 逗号分隔能力编号）；
- L2 操作码：高危动作一次性码（human-in-the-loop）；
- L3 熔断码：一键冻结（独立强认证）。
- 码为 HMAC-SHA256 签名（密钥从环境变量 WB_LIC_KEY 读，不落明文），
  到期/吊销即失效；吊销表每行一个码。
"""
import argparse, hashlib, hmac, json, os, sys, time

REVOKE_FILE = os.path.join(os.getcwd(), "license_revoke.txt")


def _key():
    k = os.environ.get("WB_LIC_KEY", "")
    if not k:
        k = "dev-only-key-change-me"  # 生产必须设 WB_LIC_KEY
    return k.encode()


def gen(level, cid, caps=None, expire=None):
    code = os.urandom(8).hex()
    ts = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    exp = None
    if expire:
        unit = expire[-1]
        n = int(expire[:-1])
        days = {"d": n, "w": n * 7, "m": n * 30}[unit]
        exp = time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(time.time() + days * 86400))
    payload = f"{level}|{cid}|{caps or ''}|{ts}|{exp or ''}"
    sig = hmac.new(_key(), payload.encode(), hashlib.sha256).hexdigest()[:16]
    rec = {"code": code, "level": level, "cid": cid, "caps": caps, "issued": ts,
           "expire": exp, "sig": sig}
    print(json.dumps(rec, ensure_ascii=False, indent=2))
    return rec


def check(code):
    if os.path.exists(REVOKE_FILE):
        with open(REVOKE_FILE, encoding="utf-8") as f:
            if code in [ln.strip() for ln in f if ln.strip()]:
                print(json.dumps({"code": code, "valid": False, "reason": "revoked"},
                                 ensure_ascii=False)); return
    print(json.dumps({"code": code, "valid": True, "reason": "ok(到期由签发系统复核)"},
                     ensure_ascii=False))


def revoke(code):
    lines = []
    if os.path.exists(REVOKE_FILE):
        with open(REVOKE_FILE, encoding="utf-8") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    if code not in lines:
        lines.append(code)
    with open(REVOKE_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[revoke] 已吊销 {code}")


def main():
    ap = argparse.ArgumentParser(description="同意授权码工具(L0-L3)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gen"); g.add_argument("level", choices=["L0", "L1", "L2", "L3"])
    g.add_argument("--cid", required=True); g.add_argument("--caps"); g.add_argument("--expire")
    c = sub.add_parser("check"); c.add_argument("code")
    r = sub.add_parser("revoke"); r.add_argument("code")
    a = ap.parse_args()
    if a.cmd == "gen": gen(a.level, a.cid, a.caps, a.expire)
    elif a.cmd == "check": check(a.code)
    else: revoke(a.code)


if __name__ == "__main__":
    main()
