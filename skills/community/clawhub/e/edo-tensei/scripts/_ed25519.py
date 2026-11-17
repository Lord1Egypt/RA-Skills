#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_ed25519.py —— 纯 Python Ed25519 签名（RFC 8032），零第三方依赖。

用途：edo-tensei 技能的密钥门禁（maintenance_lock.py）在所有机器上（含未装 pip 的用户机）
都能用标准库完成「私钥签名 / 公钥验签」，无需安装 cryptography。

设计要点（与 RFC 8032 严格对齐，这是上一版公钥对不上的根因）：
  - 私钥是 32 字节 seed；标量 a = prune(SHA512(seed)[:32])，不是直接 clamp(seed)。
  - 签名 r = SHA512(prefix || M)，prefix = SHA512(seed)[32:]，不是 SHA512(seed || M)。
  - 公钥 = 压缩编码( a * B )；编码 = y（小端 255 位）| 签名位( x 的最低位)。

正确性验证：
  - 内置 __main__ 自检：RFC 8032 官方测试向量（seed=9d61b1…）逐字节一致；
  - 若本机装了 cryptography，再跑双向互验（同 seed 公钥一致、互验签名通过）。
仅依赖 hashlib（标准库）。
"""

import hashlib

MOD = 2 ** 255 - 19
L = 2 ** 252 + 27742317777372353535851937790883648493


def _inv(x: int) -> int:
    return pow(x % MOD, MOD - 2, MOD)


d = (-121665 * _inv(121666)) % MOD


def _xrecover(y: int) -> int:
    xx = (y * y - 1) * _inv(d * y * y + 1) % MOD
    x = pow(xx, (MOD + 3) // 8, MOD)
    if (x * x - xx) % MOD != 0:
        x = (x * pow(2, (MOD - 1) // 4, MOD)) % MOD
    if x % 2 != 0:
        x = MOD - x
    return x


By = (4 * _inv(5)) % MOD
Bx = _xrecover(By)
B = (Bx % MOD, By % MOD)


def _edwards(P, Q):
    x1, y1 = P
    x2, y2 = Q
    denom1 = _inv(1 + d * x1 * x2 * y1 * y2)
    denom2 = _inv(1 - d * x1 * x2 * y1 * y2)
    x3 = (x1 * y2 + x2 * y1) * denom1 % MOD
    y3 = (y1 * y2 + x1 * x2) * denom2 % MOD
    return (x3 % MOD, y3 % MOD)


def _scalarmult(P, e: int):
    if e == 0:
        return (0, 1)
    Q = _scalarmult(P, e // 2)
    Q = _edwards(Q, Q)
    if e & 1:
        Q = _edwards(Q, P)
    return Q


def _encode_point(P):
    x, y = P
    bits = y | ((x & 1) << 255)
    return bits.to_bytes(32, "little")


def _decode_point(s: bytes):
    if len(s) != 32:
        raise ValueError("bad point length")
    y = int.from_bytes(s, "little")
    sign = (y >> 255) & 1
    y &= (1 << 255) - 1
    if y >= MOD:
        raise ValueError("y out of range")
    x = _xrecover(y)
    if (x & 1) != sign:
        x = MOD - x
    if (d * x * x * y * y + x * x - y * y + 1) % MOD != 0:
        raise ValueError("point not on curve")
    return (x, y)


def _sha512(m: bytes) -> bytes:
    return hashlib.sha512(m).digest()


def _derive_scalar(seed: bytes):
    """RFC 8032：由 32 字节 seed 导出 (标量 a, 前缀 prefix)。"""
    if len(seed) != 32:
        raise ValueError("seed must be 32 bytes")
    h = _sha512(seed)
    a = int.from_bytes(h[:32], "little")
    a &= ~((1 << 0) | (1 << 1) | (1 << 2))   # 清低 3 位
    a |= (1 << 254)                           # 置位 254
    a &= ~(1 << 255)                          # 清位 255
    return a, h[32:]


def public_key_from_seed(seed: bytes) -> bytes:
    """seed: 32 字节种子 → 32 字节公钥（RFC 8032 压缩编码）。"""
    a, _ = _derive_scalar(seed)
    return _encode_point(_scalarmult(B, a))


def sign_seed(seed: bytes, msg: bytes) -> bytes:
    """seed: 32 字节种子, msg: 消息 → 64 字节签名（R||S）。"""
    a, prefix = _derive_scalar(seed)
    A = _encode_point(_scalarmult(B, a))
    r = int.from_bytes(_sha512(prefix + msg), "little") % L
    R = _encode_point(_scalarmult(B, r))
    k = int.from_bytes(_sha512(R + A + msg), "little") % L
    s = (r + k * a) % L
    return R + s.to_bytes(32, "little")


def verify(pub: bytes, msg: bytes, sig: bytes) -> bool:
    """公钥验签：真=通过，假=失败（含任何格式异常）。"""
    try:
        if len(pub) != 32 or len(sig) != 64:
            return False
        A = _decode_point(pub)
        R = _decode_point(sig[:32])
        s = int.from_bytes(sig[32:], "little")
        if s >= L:
            return False
        k = int.from_bytes(_sha512(sig[:32] + pub + msg), "little") % L
        lhs = _scalarmult(B, s)
        rhs = _edwards(R, _scalarmult(A, k))
        return lhs == rhs
    except Exception:
        return False


# RFC 8032 §7.1 官方测试向量 1（权威交叉验证基准）
_RFC_SEED = bytes.fromhex("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")
_RFC_PUB = bytes.fromhex("d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a")
_RFC_SIG = bytes.fromhex(
    "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e06522490155"
    "5fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"
)


def _self_test():
    ok = True
    # 1) RFC 8032 官方向量
    pub = public_key_from_seed(_RFC_SEED)
    if pub != _RFC_PUB:
        ok = False
        print("FAIL: RFC vector pubkey mismatch")
        print("  got :", pub.hex())
        print("  want:", _RFC_PUB.hex())
    sig = sign_seed(_RFC_SEED, b"")
    if sig != _RFC_SIG:
        ok = False
        print("FAIL: RFC vector signature mismatch")
        print("  got :", sig.hex())
        print("  want:", _RFC_SIG.hex())
    if not verify(pub, b"", sig):
        ok = False
        print("FAIL: RFC vector self-verify")
    # 2) 随机种子自洽
    import os
    for _ in range(20):
        seed = os.urandom(32)
        msg = os.urandom(50)
        pk = public_key_from_seed(seed)
        sg = sign_seed(seed, msg)
        if not verify(pk, msg, sg):
            ok = False
            print("FAIL: random self round-trip")
            break
    # 3) 篡改检测
    if verify(pub, b"x", sig) or verify(pub, b"", sig[:-1] + bytes([sig[-1] ^ 1])):
        ok = False
        print("FAIL: tamper not detected")
    # 4) cryptography 双向互验（可选）
    oracle = False
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        oracle = True
        for _ in range(5):
            seed = os.urandom(32)
            msg = os.urandom(40)
            pk = public_key_from_seed(seed)
            sg = sign_seed(seed, msg)
            ck = Ed25519PrivateKey.from_private_bytes(seed)
            cpub = ck.public_key().public_bytes_raw()
            csig = ck.sign(msg)
            if cpub != pk:
                ok = False
                print("FAIL: pubkey mismatch with cryptography")
                break
            if not verify(cpub, msg, csig):
                ok = False
                print("FAIL: verify cryptography sig")
                break
            try:
                ck.public_key().verify(sg, msg)
            except Exception:
                ok = False
                print("FAIL: cryptography reject pure-python sig")
                break
            if not verify(pk, msg, csig):
                ok = False
                print("FAIL: pure-python reject cryptography sig")
                break
    except Exception as e:
        print("oracle=cryptography unavailable:", e)
    print("self-test:", "PASS" if ok else "FAIL", "(oracle=%s)" % oracle)
    return ok


if __name__ == "__main__":
    _self_test()
