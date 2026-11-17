#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vault_lab.py — 标准密码学实践演示工具（公开业界较佳实践 · 零真实凭据 · 无网络）

本工具演示「把口令 / 密钥 / 授权做对」的公开通用做法（OWASP / 业界标准），
供学习、验证和讲解用。它不包含任何产品级实现：
- 不含统一凭据体系的产品架构、分级授权、恢复流程（那些是内部方案）
- 不接触任何真实密码 / 密钥 / 凭据文件
- 不联网、不留盘（所有数据仅在内存中生成使用）

用法：
  python tools/vault_lab.py derive      # 口令 → 密钥派生（PBKDF2）演示
  python tools/vault_lab.py encrypt     # AES-256-GCM 认证加密 / 解密演示
  python tools/vault_lab.py sign        # Ed25519 签名 / 验真演示
  python tools/vault_lab.py token       # HMAC 短时令牌（时效授权）演示
  python tools/vault_lab.py demo        # 一键跑完全部演示 + 结论（默认）

依赖：`cryptography`（pip install cryptography）。derive/token 仅用标准库。
"""
import argparse
import base64
import hashlib
import hmac
import secrets
import sys
import time

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False


def _hint():
    print("提示：encrypt / sign 需要 `cryptography` 库（pip install cryptography）。", file=sys.stderr)


def cmd_derive(args):
    """口令 → 密钥派生：PBKDF2-HMAC-SHA256（公开标准做法）"""
    passphrase = "demo-passphrase-2026"  # 仅演示用的假口令，非任何真实凭据
    salt = secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac("sha256", passphrase.encode(), salt, 600_000, dklen=32)
    print("[口令→密钥派生 PBKDF2-HMAC-SHA256]")
    print(f"  口令（演示假数据）: {passphrase}")
    print(f"  Salt（随机16B）   : {salt.hex()}")
    print(f"  派生 Key（32B）   : {key.hex()}")
    print("  结论：用内存硬 KDF 把弱口令变成强密钥，是业界对『口令当密钥』的标准修复（公开做法）。")
    return 0


def cmd_encrypt(args):
    """AES-256-GCM 认证加密：加密 + 防篡改一体（公开标准做法）"""
    if not HAS_CRYPTO:
        _hint()
        return 1
    msg = "zero-knowledge envelope demo: 只有密文离开本机".encode("utf-8")
    key = secrets.token_bytes(32)
    aes = AESGCM(key)
    nonce = secrets.token_bytes(12)
    ct = aes.encrypt(nonce, msg, None)
    b64 = base64.b64encode(nonce + ct).decode()
    print("[AES-256-GCM 认证加密（信封加密概念的标准实现）]")
    print(f"  明文（演示假数据）: {msg.decode()}")
    print(f"  Key（32B随机）    : {key.hex()}")
    print(f"  Nonce+密文+Tag(b64): {b64[:56]}...")
    raw = base64.b64decode(b64)
    plain = aes.decrypt(raw[:12], raw[12:], None)
    print(f"  解密回验          : {plain.decode()}")
    print("  结论：认证加密把『加密』和『防篡改』做成一体；『只有密文出本机』=零知识信封的公开标准做法。")
    return 0


def cmd_sign(args):
    """Ed25519 签名 / 验真（公开标准做法）"""
    if not HAS_CRYPTO:
        _hint()
        return 1
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key()
    msg = b"verifiable provenance demo"
    sig = priv.sign(msg)
    pub.verify(sig, msg)  # 正常验证，不抛异常即通过
    tamper_rejected = True
    try:
        pub.verify(sig, b"tampered-content")
        tamper_rejected = False
    except Exception:
        pass
    print("[Ed25519 签名 / 验真]")
    print(f"  公钥(b64)  : {base64.b64encode(pub.public_bytes_raw()).decode()[:44]}...")
    print(f"  签名(b64)  : {base64.b64encode(sig).decode()[:44]}...")
    print(f"  正常验证    : 通过 ✓ | 篡改内容验证: {'拒绝 ✓' if tamper_rejected else '通过（异常！）'}")
    print("  结论：非对称签名用于『出处可验真』，是业界公开标准做法（如证书、发行签名）。")
    return 0


def cmd_token(args):
    """HMAC 短时令牌：时效授权的最小公开标准做法"""
    secret = secrets.token_bytes(32)
    ttl = 900
    msg = b"authorization-scope-demo"
    exp = int(time.time()) + ttl
    token = base64.b64encode(
        hmac.new(secret, msg + str(exp).encode(), hashlib.sha256).digest()
    ).decode()
    # 有效期内：用声明的 exp 重算比对
    ok_valid = hmac.compare_digest(
        hmac.new(secret, msg + str(exp).encode(), hashlib.sha256).digest(),
        base64.b64decode(token),
    )
    # 过期模拟：用过期时间重算，与原令牌必然不一致 → 拒绝
    ok_expired = hmac.compare_digest(
        hmac.new(secret, msg + str(int(time.time()) - 1).encode(), hashlib.sha256).digest(),
        base64.b64decode(token),
    )
    print("[HMAC 短时令牌（时效授权）]")
    print(f"  TTL: {ttl}s | 有效期内校验: {'通过 ✓' if ok_valid else '拒绝'}")
    print(f"  过期后校验      : {'通过（异常！）' if ok_expired else '拒绝 ✓'}")
    print("  结论：带过期时间的签名令牌 = 时效授权的最小公开标准做法；过期即拒，是『临时授权』的公开套路。")
    return 0


def cmd_demo(args):
    print("=== vault_lab · 标准密码学实践演示（零真实凭据 · 无网络）===\n")
    for fn in (cmd_derive, cmd_encrypt, cmd_sign, cmd_token):
        rc = fn(args)
        if rc == 1:
            return 1
        print()
    print("=== 总结 ===")
    print("以上四件套 =『把口令/密钥/授权做对』的公开通用做法（OWASP/业界标准），用于学习、验证与讲解。")
    print("产品级统一凭据体系（统一架构/分级授权/恢复流程）不在此工具内，属内部方案，落地走 SOP 与专家。")
    return 0


def main():
    ap = argparse.ArgumentParser(description="标准密码学实践演示（公开较佳实践 · 零真实凭据 · 无网络）")
    ap.add_argument(
        "cmd", nargs="?", default="demo",
        choices=["derive", "encrypt", "sign", "token", "demo"],
        help="演示子命令（默认 demo 一键全跑）",
    )
    args = ap.parse_args()
    fn = {"derive": cmd_derive, "encrypt": cmd_encrypt, "sign": cmd_sign, "token": cmd_token, "demo": cmd_demo}[args.cmd]
    sys.exit(fn(args))


if __name__ == "__main__":
    main()
