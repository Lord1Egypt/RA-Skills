#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""代码所有权体检 - 客户端支付门禁（x402 编排 + 离线回执校验）。

设计边界（与服务器「纯支付预言机」对应）：
  - 审计本身由 audit.py 在客户本机离线完成，本模块绝不碰审计逻辑、不触网做分析。
  - 本模块只负责「付钱这一步」的编排，以及拿到服务器签发的履约回执后，
    用**内嵌**的商户公钥（见 SERVER_PUBKEY_PEM）**离线**校验回执真伪——
    校验不联网、不依赖服务器存活，确认「这笔钱确实付到了预言机」。

依赖：stdlib（urllib）做 HTTP；pycryptodome 做 RSA2 离线验签。
    pip install pycryptodome
"""
import argparse
import base64
import json
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

BASE_DIR = Path(__file__).parent
DEFAULT_ORACLE = "https://seika.ltd/api/audit"

# 商户应用公钥（RSA2），与服务器私钥配对，仅用于离线验签履约回执。
# why: 直接内嵌而不是随包带 .pem —— ① 公钥本就是公开分发物，内嵌无任何安全损失；
#      ② 部分技能market（如腾讯）不接受 .pem 附件；③ 少一个文件依赖，
#      单文件拷走 paygate.py 也能验签，不会因缺文件静默退化成"无法校验"。
SERVER_PUBKEY_PEM = """\
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAv8I0W+OdiLG+H/QSTAMN
tOLbqftsce8Y1phSOzrSQPcp2jgL1rNw+4MdkorFEXMgcf0m2se6ruWzM49k0r38
+YowE3GIq9HSCGjeLANh/0/VIDivgP234Cx8mW5jTGHKsjK3eqFwQ0vhkxtDOTyh
P9oisnS0Ql3cl7WgsVvijxfB8lQKPJLuAabxK3EAGO6DRMo04gLUj7hmzIWgXLQo
/NZSktwrk8ulBk4N/QCSAJ2NxV+Eck/qCKJr9yxgIMLUATkpRKQy+OQfR/TTI8xa
6PH9bRkcA07/f3U3Lv3eciZg+QG6Yukwi8QsL1P+h96mS0Vj0/b/cQBmNp4a+i43
ewIDAQAB
-----END PUBLIC KEY-----"""

# 可选的外部公钥文件：存在则优先，用于轮换密钥或自建预言机时覆盖内嵌值。
# why: 保留覆盖入口，避免换密钥就必须改代码发新版。
SERVER_PUBKEY = BASE_DIR / "server_pubkey.pem"


def load_pubkey(path: Path | None = None) -> str:
    """取验签公钥：显式路径 > 同目录 server_pubkey.pem > 内嵌常量。"""
    p = path or SERVER_PUBKEY
    if p and p.exists():
        return p.read_text(encoding="utf-8").strip()
    return SERVER_PUBKEY_PEM


# 完整报告单价（元/次）。预览档免费、不限次。
# why: 权威价格在服务端 env AIPAY_AMOUNT；这里只是离线提示用的兜底，
#      真实金额始终由 402 账单与回执携带并经签名校验，不受此常量影响。
PRICE_CNY = "0.2"


# ----------------------------------------------------------------- HTTP 编排

def request_402(oracle_url: str = DEFAULT_ORACLE) -> dict:
    """向预言机索取 402 账单。返回原始账单头 + 易读字段，供 alipay-bot 付款用。"""
    req = Request(oracle_url, data=b"", method="POST",
                  headers={"Content-Type": "application/json"})
    try:
        with urlopen(req, timeout=15) as resp:
            resp.read()
        raise RuntimeError("预期 402，却收到 200")
    except HTTPError as e:
        bill = e.headers.get("Payment-Needed")
        if not bill:
            raise RuntimeError(f"402 响应缺少 Payment-Needed 头: {e.code}")
        return {
            "status": e.code,
            "payment_needed": bill,
            "out_trade_no": e.headers.get("X-Out-Trade-No", ""),
            "raw": e.read().decode(errors="replace"),
        }


def submit_proof(payment_proof: str, oracle_url: str = DEFAULT_ORACLE) -> tuple[dict, str]:
    """把 alipay-bot 拿到的 Payment-Proof 回传给预言机，取回签名回执。

    返回 (receipt_dict, receipt_signature)。非 200 抛 RuntimeError。
    """
    req = Request(oracle_url, data=b"", method="POST",
                  headers={"Payment-Proof": payment_proof,
                           "Content-Type": "application/json"})
    try:
        with urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8")
    except HTTPError as e:
        raise RuntimeError(f"回传凭证失败 {e.code}: {e.read().decode(errors='replace')}")
    data = json.loads(body)
    if data.get("code") != "SUCCESS" or "receipt" not in data:
        raise RuntimeError(f"预言机未返回回执: {body[:300]}")
    return data["receipt"], data["receipt_signature"]


# ----------------------------------------------------------- 离线回执校验

def _canonical(receipt: dict) -> bytes:
    """与服务器签发完全一致：固定字段字典序 & 拼接。"""
    return "&".join(f"{k}={receipt[k]}" for k in sorted(receipt)).encode("utf-8")


def verify_receipt(receipt: dict, signature_b64: str,
                   pubkey_pem: str | None = None) -> bool:
    """离线校验履约回执：用商户公钥验 RSA2 签名，不联网。

    任何字段（含 fulfilled_at）被篡改都会验签失败。
    """
    pub = pubkey_pem or load_pubkey()
    key = RSA.import_key(pub)
    h = SHA256.new(_canonical(receipt))
    try:
        pkcs1_15.new(key).verify(h, base64.b64decode(signature_b64))
        return True
    except (ValueError, TypeError):
        return False


def embed_certification(report: dict, receipt: dict, signature_b64: str) -> dict:
    """把已验证的付款认证块并入审计报告（报告本体仍是 audit.py 离线产出）。"""
    certified = dict(report)
    certified["certification"] = {
        "paid": True,
        "oracle": receipt.get("oracle"),
        "out_trade_no": receipt.get("out_trade_no"),
        "trade_no": receipt.get("trade_no"),
        "amount": receipt.get("amount"),
        "goods_name": receipt.get("goods_name"),
        "fulfilled_at": receipt.get("fulfilled_at"),
        "receipt_signature": signature_b64,
        "verified_offline_with": "embedded_server_pubkey",
    }
    return certified


def render_certification_md(receipt: dict, signature_b64: str) -> str:
    return (
        "\n## 付款认证（离线已核验）\n"
        f"- 支付预言机：`{receipt.get('oracle')}`\n"
        f"- 商户订单号：`{receipt.get('out_trade_no')}`\n"
        f"- 支付宝交易号：`{receipt.get('trade_no')}`\n"
        f"- 金额：`{receipt.get('amount')} {receipt.get('currency', 'CNY')}`\n"
        f"- 履约时间：`{receipt.get('fulfilled_at')}`\n"
        f"- 回执签名（RSA2，可离线复验）：`{signature_b64[:48]}…`\n"
        "\n> 本认证由服务器私钥签发、客户端用内置商户公钥离线校验，"
        "不依赖服务器在线。审计结论由本地 `audit.py` 离线生成，代码未出本机。\n"
    )


# --------------------------------------------------------------- skill 编排

def _load_audit():
    """Lazily import the offline audit engine (sibling audit.py)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "coa_audit", BASE_DIR / "audit.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _build_certified_markdown(full: dict, receipt: dict, signature_b64: str) -> str:
    """Full offline report + verification block = the paid deliverable."""
    audit_mod = _load_audit()
    return (audit_mod.render_markdown(full, payment_notice=False)
            + render_certification_md(receipt, signature_b64))


# --------------------------------------------------------------------- CLI

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="代码所有权体检 - 支付门禁与离线回执校验")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("request-402", help="向预言机索取 402 账单")
    p1.add_argument("--oracle", default=DEFAULT_ORACLE)
    p1.add_argument("--out", help="把账单头写到这里（json）")

    p2 = sub.add_parser("submit-proof", help="回传 Payment-Proof，取回签名回执")
    p2.add_argument("--proof", required=True, help="alipay-bot 返回的 Payment-Proof")
    p2.add_argument("--oracle", default=DEFAULT_ORACLE)
    p2.add_argument("--out", help="把回执写到这里（json）")

    p3 = sub.add_parser("verify", help="离线校验回执真伪")
    p3.add_argument("--receipt", required=True, help="回执 json（含 receipt + receipt_signature）")
    p3.add_argument("--pubkey", default=None,
                    help="可选：外部公钥 pem 路径；不传则用内嵌公钥")

    p4 = sub.add_parser("embed", help="把认证块并入审计报告")
    p4.add_argument("--report", required=True)
    p4.add_argument("--receipt", required=True)
    p4.add_argument("--out", required=True)

    p5 = sub.add_parser("run", help="离线跑审计：出预览并存 full.json（未认证）")
    p5.add_argument("target", help="待检文件或目录")
    p5.add_argument("--reference", help="上游参照文件或目录")
    p5.add_argument("--threshold", type=int, default=3, help="演绎判定阈值")
    p5.add_argument("--out-dir", default=".", help="预览/完整报告输出目录")

    p6 = sub.add_parser("unlock", help="回传 Proof → 离线验签 → 认证完整报告")
    p6.add_argument("--proof", required=True, help="alipay-bot 返回的 Payment-Proof")
    p6.add_argument("--oracle", default=DEFAULT_ORACLE)
    p6.add_argument("--out-dir", default=".", help="含 full.json 的目录")
    p6.add_argument("--full", help="直接指定 full.json 路径")

    args = ap.parse_args(argv)

    if args.cmd == "request-402":
        res = request_402(args.oracle)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        if args.out:
            Path(args.out).write_text(json.dumps(res, ensure_ascii=False), encoding="utf-8")
            print(f"账单已写 {args.out}")
        # why: the buyer agent may not have a wallet CLI yet; tell it where to get one
        #      instead of letting it fail on `command not found` or give up on paying.
        print("\n下一步用支付宝 AI 钱包付款（alipay-bot）。若无该命令，先装官方 Agent 支付：")
        print("  npx -y @alipay/agent-payment@latest install-experience")
        return 0

    if args.cmd == "submit-proof":
        receipt, sig = submit_proof(args.proof, args.oracle)
        ok = verify_receipt(receipt, sig)
        out = {"receipt": receipt, "receipt_signature": sig, "offline_verify": ok}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        if not ok:
            print("⚠ 离线校验失败：回执签名与内置公钥不匹配！", file=sys.stderr)
            return 1
        if args.out:
            Path(args.out).write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
            print(f"回执已写 {args.out}")
        return 0

    if args.cmd == "verify":
        data = json.loads(Path(args.receipt).read_text(encoding="utf-8"))
        receipt = data.get("receipt", data)
        sig = data.get("receipt_signature", "")
        # why: --pubkey 不传时走 load_pubkey()（内嵌公钥），
        #      不能直接 Path(None) 或读不存在的文件。
        pub = load_pubkey(Path(args.pubkey)) if args.pubkey else load_pubkey()
        ok = verify_receipt(receipt, sig, pub)
        print("RECEIPT_VALID" if ok else "RECEIPT_VALID_FALSE")
        return 0 if ok else 1

    if args.cmd == "embed":
        report = json.loads(Path(args.report).read_text(encoding="utf-8"))
        data = json.loads(Path(args.receipt).read_text(encoding="utf-8"))
        receipt = data.get("receipt", data)
        sig = data.get("receipt_signature", "")
        certified = embed_certification(report, receipt, sig)
        Path(args.out).write_text(json.dumps(certified, ensure_ascii=False, indent=2),
                                  encoding="utf-8")
        print(f"已认证报告写 {args.out}")
        return 0

    if args.cmd == "run":
        audit_mod = _load_audit()
        target = Path(args.target)
        reference = Path(args.reference) if args.reference else None
        report = audit_mod.audit(target, reference, args.threshold)
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        preview = audit_mod.build_preview(report)
        (out_dir / "preview.md").write_text(
            audit_mod.render_preview_markdown(preview), encoding="utf-8")
        (out_dir / "full.md").write_text(
            audit_mod.render_markdown(report), encoding="utf-8")
        (out_dir / "full.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(audit_mod.render_preview_text(preview))
        print(f"\n── 预览已生成（免费，可无限次跑）。")
        print(f"   解锁完整报告（代码位置/行号/修复建议/签名认证）：{PRICE_CNY} 元/次")
        print(f"\n   1) python paygate.py request-402 --out {out_dir / 'bill.json'}")
        print(f"   2) alipay-bot 402-buyer-pay --file <payment_needed> "
              f"--resource-url {DEFAULT_ORACLE} --method POST")
        print(f"   3) alipay-bot 402-query-payment-status --trade-no <交易号> "
              f"--resource-url {DEFAULT_ORACLE} --method POST --data '{{}}'")
        print(f"      ↑ 扫码付款时 proof 不在第 2 步返回，必须跑第 3 步取回执")
        print(f"   4) python paygate.py verify --receipt <回执json> "
              f"&& python paygate.py embed --report {out_dir / 'full.json'} "
              f"--receipt <回执json> --out {out_dir / 'certified.json'}")
        print(f"\n   没有 alipay-bot 命令？先装支付宝官方 Agent 支付（AI 钱包）：")
        print(f"     npx -y @alipay/agent-payment@latest install-experience")
        return 0

    if args.cmd == "unlock":
        receipt, sig = submit_proof(args.proof, args.oracle)
        ok = verify_receipt(receipt, sig)
        if not ok:
            print("⚠ 离线校验失败：回执签名与内置公钥不匹配，拒绝解锁。",
                  file=sys.stderr)
            return 1
        out_dir = Path(args.out_dir)
        full_path = Path(args.full) if args.full else out_dir / "full.json"
        if not full_path.exists():
            print(f"error: 找不到完整报告 {full_path}，请先跑 run", file=sys.stderr)
            return 2
        full = json.loads(full_path.read_text(encoding="utf-8"))
        certified = embed_certification(full, receipt, sig)
        (out_dir / "certified.json").write_text(
            json.dumps(certified, ensure_ascii=False, indent=2), encoding="utf-8")
        (out_dir / "certified.md").write_text(
            _build_certified_markdown(full, receipt, sig), encoding="utf-8")
        print(f"✓ 已认证完整报告 → {out_dir / 'certified.json'}")
        print(f"  支付宝交易号：{receipt.get('trade_no')}  "
              f"金额：{receipt.get('amount')} {receipt.get('currency', 'CNY')}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
