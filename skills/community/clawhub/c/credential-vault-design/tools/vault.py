#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vault.py — 统一凭据保险库（真实可用 · 本地零知识 · 全生态同读）

一个真正能落地的本地凭据保险库：把分散的口令 / 密钥 / 授权码收敛成一套
统一、可恢复、分级授权、带防篡改审计链的体系。所有明文只在本机内存中存在，
落盘内容均为密文 + 认证标签（AES-256-GCM）。

> 注：本程序占位符（如 demo-user）非真实账号，零真实凭据参与测试。

设计要点（公开标准做法，已落地为代码）：
  * 密钥派生 KDF ：PBKDF2-HMAC-SHA256，600,000 轮（OWASP 2023 对 PBKDF2-SHA256 的建议下限）
  * 信封加密     ：主口令派生 KEK；每条凭据用随机 DEK（AES-256-GCM）加密，DEK 再由 KEK 包裹
  * 分级授权     ：凭据按密级（public/low/medium/high/secret）标记；时效令牌按作用域最小权限发放
  * 可恢复不锁死 ：初始化时生成一次性恢复密钥（recovery key），以 recovery KEK 托管 KEK，忘密可恢复
  * 时效授权     ：HMAC 签名的短时作用域令牌（scope + exp），过期即拒、越权即拒
  * 防篡改审计   ：审计记录组成 SHA-256 哈希链；整库带 file_mac（HMAC），任何外部篡改加载即拒
  * 零知识边界   ：落盘只有密文 / 盐 / nonce / tag；明文不出本机、不进云、不留盘

依赖：仅标准库 + `cryptography`（pip install cryptography）。零真实凭据、本地闭环。

用法（交互模式用 getpass 隐藏输入；自动化用 --password / 环境变量 UCV_PASS）：
  python tools/vault.py init                                   # 建库（生成主口令 + 一次性恢复密钥）
  python tools/vault.py set  github --scope high --username demo-user   # 添加（会提示输入密值）
  python tools/vault.py get  github                           # 取回明文（仅内存）
  python tools/vault.py list --scope medium                   # 列出某密级及以下条目（不含密值）
  python tools/vault.py token --scope low --ttl 900           # 发一个 900s 的 low 级时效令牌
  python tools/vault.py verify <token>                        # 校验令牌作用域/时效
  python tools/vault.py audit                                 # 打印并校验审计哈希链完整性
  python tools/vault.py change-pass                           # 改主口令（重裹全部 DEK）
  python tools/vault.py recover --recovery-key <key>          # 用恢复密钥解锁并重置主口令
  python tools/vault.py status                                # 仓库概览
所有命令支持 --home <DIR> 指定仓库位置（默认 ~/.ucvault）；测试用临时目录。
"""
from __future__ import annotations

import argparse
import base64
import getpass
import hashlib
import hmac
import json
import os
import secrets
import sys
import time
from pathlib import Path

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# ----------------------------- 常量 -----------------------------
KDF_ITERS = 600_000
GRADES = ["public", "low", "medium", "high", "secret"]
GRADE_WEIGHT = {g: i for i, g in enumerate(GRADES)}
DEFAULT_HOME = Path(os.path.expanduser("~")) / ".ucvault"


class VaultError(Exception):
    """业务错误（友好提示，不抛栈）。"""


class TamperError(VaultError):
    """检测到仓库被篡改。"""


# ----------------------------- 底层原语 -----------------------------
def b64e(b: bytes) -> str:
    return base64.b64encode(b).decode("ascii")


def b64d(s: str) -> bytes:
    return base64.b64decode(s)


def derive_kek(password: str, salt: bytes) -> bytes:
    """主口令 -> 密钥加密密钥（KEK），32 字节。"""
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, KDF_ITERS, dklen=32)


def hkdf(ikm: bytes, info: bytes, length: int = 32) -> bytes:
    """从 KEK 派生确定性的子密钥（file_mac / token 用）。"""
    return HKDF(algorithm=hashes.SHA256(), length=length, salt=None, info=info).derive(ikm)


def aes_seal(key: bytes, plaintext: bytes, aad=None) -> bytes:
    """AES-256-GCM 加密，返回 nonce(12B) + 密文+Tag。"""
    nonce = secrets.token_bytes(12)
    ct = AESGCM(key).encrypt(nonce, plaintext, aad)
    return nonce + ct


def aes_open(key: bytes, blob: bytes, aad=None) -> bytes:
    """AES-256-GCM 解密并验真（篡改即抛 InvalidTag）。"""
    return AESGCM(key).decrypt(blob[:12], blob[12:], aad)


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


# ----------------------------- 保险库 -----------------------------
class Vault:
    def __init__(self, home: Path):
        self.home = Path(home)
        self.path = self.home / "vault.json"
        self.data: dict = {}

    # ---- 加载 / 保存 ----
    def exists(self) -> bool:
        return self.path.exists()

    def load(self, kek: bytes):
        """用 KEK 解密并校验整库完整性（file_mac）。"""
        try:
            raw = self.path.read_text("utf-8")
            data = json.loads(raw)
        except (OSError, json.JSONDecodeError) as e:
            raise VaultError(f"仓库文件损坏或无法读取：{e}")
        # 校验 file_mac
        fmk = hkdf(kek, b"ucv-file-mac")
        mac_stored = b64d(data.get("file_mac", ""))
        body = {k: v for k, v in data.items() if k != "file_mac"}
        mac_calc = hmac.new(fmk, canonical(body).encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(mac_stored, mac_calc):
            raise TamperError("整库 file_mac 校验失败：仓库可能在你不知情时被篡改。")
        self.data = data

    def _seal_and_save(self, kek: bytes):
        fmk = hkdf(kek, b"ucv-file-mac")
        body = {k: v for k, v in self.data.items() if k != "file_mac"}
        mac = hmac.new(fmk, canonical(body).encode(), hashlib.sha256).digest()
        self.data["file_mac"] = b64e(mac)
        self.home.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(canonical(self.data), "utf-8")
        tmp.replace(self.path)  # 原子替换

    # ---- 审计哈希链 ----
    def _audit_record(self, op: str, target: str) -> dict:
        chain = self.data.get("audit", [])
        prev = chain[-1]["hash"] if chain else "0" * 64
        rec = {"seq": len(chain) + 1, "ts": int(time.time()),
               "op": op, "target": target, "prev": prev}
        rec["hash"] = hashlib.sha256(
            (prev + "|" + canonical(rec)).encode()).hexdigest()
        return rec

    def append_audit(self, op: str, target: str):
        self.data.setdefault("audit", []).append(self._audit_record(op, target))

    def verify_audit(self) -> tuple[bool, int]:
        """重算审计链；返回 (完整?, 出错序号)。"""
        chain = self.data.get("audit", [])
        prev = "0" * 64
        for i, rec in enumerate(chain, 1):
            expect = hashlib.sha256(
                (prev + "|" + canonical({k: rec[k] for k in rec if k != "hash"})).encode()
            ).hexdigest()
            if not secrets.compare_digest(expect, rec.get("hash", "")):
                return False, i
            prev = rec["hash"]
        return True, 0

    # ---- KEK 派生辅助 ----
    def kek_from_password(self, password: str) -> bytes:
        return derive_kek(password, b64d(self.data["kek_salt"]))

    def kek_from_recovery(self, recovery_key: str) -> bytes:
        rsalt = b64d(self.data["recovery_salt"])
        rkek = derive_kek(recovery_key, rsalt)
        blob = b64d(self.data["recovery_wrap"])
        return aes_open(rkek, blob)  # -> KEK

    # ---- 条目读写 ----
    def _encrypt_entry(self, kek: bytes, scope: str, username: str, value: str, notes: str) -> dict:
        dek = secrets.token_bytes(32)
        blob = canonical({"username": username, "value": value, "notes": notes}).encode()
        ct = aes_seal(dek, blob)
        dek_wrap = aes_seal(kek, dek)
        return {"scope": scope, "dek_wrap": b64e(dek_wrap),
                "nonce": b64e(ct[:12]), "ct": b64e(ct[12:])}

    def _decrypt_entry(self, kek: bytes, entry: dict) -> dict:
        dek = aes_open(kek, b64d(entry["dek_wrap"]))
        blob = b64d(entry["nonce"]) + b64d(entry["ct"])
        plain = aes_open(dek, blob)
        return json.loads(plain)

    def set_entry(self, kek: bytes, label: str, scope: str, username: str, value: str, notes: str):
        if scope not in GRADE_WEIGHT:
            raise VaultError(f"非法密级 {scope!r}；可选：{', '.join(GRADES)}")
        self.data.setdefault("entries", {})[label] = self._encrypt_entry(
            kek, scope, username, value, notes)
        self.append_audit("set", label)

    def get_entry(self, kek: bytes, label: str) -> dict:
        if label not in self.data.get("entries", {}):
            raise VaultError(f"条目不存在：{label}")
        return self._decrypt_entry(kek, self.data["entries"][label])

    def delete_entry(self, kek: bytes, label: str):
        if label not in self.data.get("entries", {}):
            raise VaultError(f"条目不存在：{label}")
        del self.data["entries"][label]
        self.append_audit("delete", label)

    def list_entries(self, max_scope: str = "secret") -> list:
        out = []
        for label, e in self.data.get("entries", {}).items():
            if GRADE_WEIGHT[e["scope"]] <= GRADE_WEIGHT[max_scope]:
                out.append((label, e["scope"]))
        return sorted(out)

    # ---- 时效作用域令牌 ----
    def issue_token(self, kek: bytes, scope: str, ttl: int) -> str:
        if scope not in GRADE_WEIGHT:
            raise VaultError(f"非法作用域 {scope!r}")
        tk = hkdf(kek, b"ucv-token")
        payload = canonical({"scope": scope, "exp": int(time.time()) + ttl,
                             "jti": b64e(secrets.token_bytes(8))})
        sig = hmac.new(tk, payload.encode(), hashlib.sha256).digest()
        return b64e(payload.encode()) + "." + b64e(sig)

    def verify_token(self, kek: bytes, token: str) -> dict:
        try:
            payload_b64, sig_b64 = token.split(".")
            payload = base64.b64decode(payload_b64).decode()
            sig = base64.b64decode(sig_b64)
        except Exception:
            return {"valid": False, "reason": "格式错误"}
        tk = hkdf(kek, b"ucv-token")
        calc = hmac.new(tk, payload.encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(calc, sig):
            return {"valid": False, "reason": "签名不符（可能被篡改/重放）"}
        p = json.loads(payload)
        if int(time.time()) > p["exp"]:
            return {"valid": False, "reason": "已过期", "scope": p["scope"], "exp": p["exp"]}
        return {"valid": True, "scope": p["scope"], "exp": p["exp"]}

    @staticmethod
    def token_grants(token_scope: str, entry_scope: str) -> bool:
        """最小权限：令牌作用域必须 >= 条目密级才放行。"""
        return GRADE_WEIGHT[entry_scope] <= GRADE_WEIGHT[token_scope]


# ----------------------------- 口令获取 -----------------------------
def get_password(args, prompt: str) -> str:
    if getattr(args, "password", None):
        return args.password
    if os.environ.get("UCV_PASS"):
        return os.environ["UCV_PASS"]
    return getpass.getpass(prompt)


def get_recovery(args) -> str:
    if getattr(args, "recovery_key", None):
        return args.recovery_key
    if os.environ.get("UCV_RECOVERY"):
        return os.environ["UCV_RECOVERY"]
    return getpass.getpass("恢复密钥： ")


# ----------------------------- 子命令实现 -----------------------------
def cmd_init(args):
    v = Vault(args.home)
    if v.exists() and not args.force:
        raise VaultError(f"仓库已存在：{v.path}（如需重建加 --force）")
    pw = get_password(args, "设置主口令： ")
    if len(pw) < 8:
        raise VaultError("主口令至少 8 位。")
    salt = secrets.token_bytes(16)
    kek = derive_kek(pw, salt)
    recovery_key = args.recovery_key or b64e(secrets.token_bytes(32))
    rsalt = secrets.token_bytes(16)
    rkek = derive_kek(recovery_key, rsalt)
    recovery_wrap = aes_seal(rkek, kek)
    v.data = {
        "version": 1, "kdf": "pbkdf2-sha256", "kdf_iterations": KDF_ITERS,
        "kek_salt": b64e(salt), "recovery_salt": b64e(rsalt),
        "recovery_wrap": b64e(recovery_wrap), "entries": {}, "audit": [],
    }
    v.append_audit("init", "(vault)")
    v._seal_and_save(kek)
    print(f"✔ 仓库已创建：{v.path}")
    print("⚠ 请立即抄存以下【一次性恢复密钥】（忘密时核心恢复途径，服务端永不可见）：")
    print(f"   {recovery_key}")
    return 0


def _open(args, use_recovery=False) -> tuple[Vault, bytes]:
    v = Vault(args.home)
    if not v.exists():
        raise VaultError(f"仓库不存在：{v.path}（先跑 init）")
    try:
        raw = v.path.read_text("utf-8")
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError) as e:
        raise VaultError(f"仓库文件损坏或无法读取：{e}")
    if use_recovery:
        rk = get_recovery(args)
        v.data = data
        try:
            kek = v.kek_from_recovery(rk)
        except Exception:
            raise VaultError("恢复密钥错误。")
        v.load(kek)  # 校验 file_mac
        return v, kek
    pw = get_password(args, "主口令： ")
    v.data = data
    kek = v.kek_from_password(pw)
    v.load(kek)  # 校验 file_mac（错口令 → mac 不符 → 拒）
    return v, kek


def cmd_set(args):
    v, kek = _open(args)
    value = args.value if args.value is not None else getpass.getpass(f"输入 [{args.label}] 的密值： ")
    v.set_entry(kek, args.label, args.scope, args.username or "", value, args.notes or "")
    v._seal_and_save(kek)
    print(f"✔ 已保存：{args.label}（密级 {args.scope}）")
    return 0


def cmd_get(args):
    v, kek = _open(args)
    if args.label not in v.data.get("entries", {}):
        raise VaultError(f"条目不存在：{args.label}")
    scope = v.data["entries"][args.label]["scope"]
    e = v.get_entry(kek, args.label)
    print(f"标签：{args.label}  密级：{scope}")
    if e.get("username"):
        print(f"账号：{e['username']}")
    print(f"密值：{e['value']}")
    if e.get("notes"):
        print(f"备注：{e['notes']}")
    return 0


def cmd_list(args):
    v, kek = _open(args)
    rows = v.list_entries(args.scope)
    if not rows:
        print("（无条目）")
        return 0
    print(f"密级≤{args.scope} 的条目（{len(rows)}）：")
    for label, scope in rows:
        print(f"  - {label}  [{scope}]")
    return 0


def cmd_delete(args):
    v, kek = _open(args)
    v.delete_entry(kek, args.label)
    v._seal_and_save(kek)
    print(f"✔ 已删除：{args.label}")
    return 0


def cmd_token(args):
    v, kek = _open(args)
    tok = v.issue_token(kek, args.scope, args.ttl)
    print(f"时效令牌（作用域 {args.scope}，{args.ttl}s）：", file=sys.stderr)
    print(tok)  # 令牌独占 stdout，便于管道/脚本抓取
    return 0


def cmd_verify(args):
    v, kek = _open(args)
    res = v.verify_token(kek, args.token)
    print(json.dumps(res, ensure_ascii=False))
    return 0


def cmd_audit(args):
    v, kek = _open(args)
    ok, bad = v.verify_audit()
    print(f"审计记录数：{len(v.data.get('audit', []))}  完整性：{'✔ 完整' if ok else '✘ 第'+str(bad)+'条起被篡改'}")
    for r in v.data.get("audit", []):
        print(f"  #{r['seq']:>3} {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r['ts']))} "
              f"{r['op']:<8} {r['target']}")
    return 0 if ok else 2


def cmd_change_pass(args):
    v, kek = _open(args)
    new = get_password(args, "设置新主口令： ")
    if len(new) < 8:
        raise VaultError("新主口令至少 8 位。")
    old_salt = b64d(v.data["kek_salt"])
    new_salt = secrets.token_bytes(16)
    new_kek = derive_kek(new, new_salt)
    # 重裹所有 DEK
    for label, e in v.data["entries"].items():
        dek = aes_open(kek, b64d(e["dek_wrap"]))
        e["dek_wrap"] = b64e(aes_seal(new_kek, dek))
    v.data["kek_salt"] = b64e(new_salt)
    v.append_audit("change-pass", "(vault)")
    v._seal_and_save(new_kek)
    print("✔ 主口令已更新，全部条目 DEK 已用新 KEK 重裹。")
    return 0


def cmd_recover(args):
    v = Vault(args.home)
    if not v.exists():
        raise VaultError(f"仓库不存在：{v.path}")
    rk = get_recovery(args)
    data = json.loads(v.path.read_text("utf-8"))
    v.data = data
    try:
        kek = v.kek_from_recovery(rk)
    except Exception:
        raise VaultError("恢复密钥错误。")
    v.load(kek)
    new = get_password(args, "设置新主口令： ")
    if len(new) < 8:
        raise VaultError("新主口令至少 8 位。")
    new_salt = secrets.token_bytes(16)
    new_kek = derive_kek(new, new_salt)
    for label, e in v.data["entries"].items():
        dek = aes_open(kek, b64d(e["dek_wrap"]))
        e["dek_wrap"] = b64e(aes_seal(new_kek, dek))
    v.data["kek_salt"] = b64e(new_salt)
    v.append_audit("recover", "(vault)")
    v._seal_and_save(new_kek)
    print("✔ 已用恢复密钥解锁并重置主口令，仓库恢复可用。")
    return 0


def cmd_status(args):
    v, kek = _open(args)
    entries = v.data.get("entries", {})
    by_scope = {}
    for e in entries.values():
        by_scope[e["scope"]] = by_scope.get(e["scope"], 0) + 1
    ok, _ = v.verify_audit()
    print(f"仓库：{v.path}")
    print(f"条目数：{len(entries)}  按密级：{by_scope}")
    print(f"审计链：{'✔ 完整' if ok else '✘ 异常'}（{len(v.data.get('audit', []))} 条）")
    print(f"KDF：{v.data.get('kdf')} / {v.data.get('kdf_iterations')} 轮")
    return 0


# ----------------------------- CLI 入口 -----------------------------
def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--home", type=Path, default=DEFAULT_HOME, help="仓库目录（默认 ~/.ucvault）")
    common.add_argument("--password", help="主口令（非交互/测试用；优先于环境变量 UCV_PASS）")
    ap = argparse.ArgumentParser(description="统一凭据保险库（本地零知识 · 真实可用）", parents=[common])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", parents=[common], help="初始化仓库")
    p.add_argument("--force", action="store_true")
    p.add_argument("--recovery-key", help="指定恢复密钥（测试/可复现用）")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("set", parents=[common], help="添加/更新条目")
    p.add_argument("label")
    p.add_argument("--scope", default="medium")
    p.add_argument("--username", default="")
    p.add_argument("--notes", default="")
    p.add_argument("--value", help="密值（不指定的话会交互隐藏输入）")
    p.set_defaults(func=cmd_set)

    p = sub.add_parser("get", parents=[common], help="取回条目明文")
    p.add_argument("label")
    p.set_defaults(func=cmd_get)

    p = sub.add_parser("list", parents=[common], help="列出条目")
    p.add_argument("--scope", default="secret")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("delete", parents=[common], help="删除条目")
    p.add_argument("label")
    p.set_defaults(func=cmd_delete)

    p = sub.add_parser("token", parents=[common], help="发时效作用域令牌")
    p.add_argument("--scope", default="low")
    p.add_argument("--ttl", type=int, default=900)
    p.set_defaults(func=cmd_token)

    p = sub.add_parser("verify", parents=[common], help="校验令牌")
    p.add_argument("token")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("audit", parents=[common], help="校验审计链")
    p.set_defaults(func=cmd_audit)

    p = sub.add_parser("change-pass", parents=[common], help="改主口令")
    p.set_defaults(func=cmd_change_pass)

    p = sub.add_parser("recover", parents=[common], help="用恢复密钥解锁")
    p.add_argument("--recovery-key", help="恢复密钥（测试用；否则交互输入）")
    p.set_defaults(func=cmd_recover)

    p = sub.add_parser("status", parents=[common], help="仓库概览")
    p.set_defaults(func=cmd_status)
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except VaultError as e:
        print(f"✘ {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
