#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maintenance_lock.py —— 秽土转生技能包的完整性维护脚本

子命令：
  gen-keys            生成 ed25519 密钥对，写 assets/pubkey.pem，打印私钥 PEM
  sign <技能包目录>    从 stdin 读取私钥，对 provenance/SEAL.json 签名
  verify [技能包目录]  用 assets/pubkey.pem 验证 SEAL 签名；缺失或失败→退出码 1
  freeze <live_dir>   对活副本目录树加系统只读属性
  unlock <live_dir>   读取私钥(stdin)核验身份后，解除活副本只读属性
  selftest            自测 _ed25519 与 PEM 编解码
"""

import argparse
import base64
import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ed25519 as ed25519

# ed25519 的 AlgorithmIdentifier DER（OID 1.3.101.112）
_OID_ED25519 = bytes([0x30, 0x05, 0x06, 0x03, 0x2B, 0x65, 0x70])


# ---------- PEM / DER 编解码（零依赖） ----------
def _b64(b: bytes) -> str:
    return base64.standard_b64encode(b).decode("ascii")


def _pem(der: bytes, kind: str) -> str:
    body = "\n".join([_b64(der)[i:i + 64] for i in range(0, len(_b64(der)), 64)])
    return "-----BEGIN %s-----\n%s\n-----END %s-----\n" % (kind, body, kind)


def _build_priv_pem(seed: bytes) -> str:
    """PKCS8 PrivateKeyInfo：SEQUENCE{INTEGER 0, AlgID, OCTET STRING{OCTET STRING{seed}}}"""
    inner = bytes([0x04, 0x20]) + seed          # OCTET STRING 包裹 32 字节种子
    priv_octet = bytes([0x04, 0x22]) + inner    # 外层 OCTET STRING (len 34)
    der = bytes([0x30, 0x2E, 0x02, 0x01, 0x00]) + _OID_ED25519 + priv_octet
    return _pem(der, "PRIVATE KEY")


def _build_pub_pem(point: bytes) -> str:
    """SubjectPublicKeyInfo：SEQUENCE{AlgID, BIT STRING{0, point}}"""
    bitstr = bytes([0x03, 0x21, 0x00]) + point  # BIT STRING, unused=0, 32 字节点
    der = bytes([0x30, 0x2A]) + _OID_ED25519 + bitstr
    return _pem(der, "PUBLIC KEY")


def _pem_payload(pem_text: str) -> bytes:
    """从 PEM 文本提取并解码 base64 负载。

    兼容性要点（修复单列 PEM 解析 bug）：私钥/公钥在复制粘贴时可能被压成
    单行（-----BEGIN/END----- 与 base64 挤在同一行），旧的按行过滤算法会把
    整行当标记滤掉、解出空串 → 种子非 32 字节报错。这里改为「按 ----- 切出
    首尾标记块、再对中间 base64 解码」，多行/单行/任意换行包裹都正确。
    """
    m = re.search(
        r"-----BEGIN[^-]*-----\s*(.*?)\s*-----END[^-]*-----",
        pem_text, re.DOTALL,
    )
    if not m:
        raise ValueError("PEM 格式无法解析：找不到私钥/公钥块")
    b64 = re.sub(r"\s+", "", m.group(1))
    if not b64:
        raise ValueError("PEM 负载为空")
    try:
        return base64.standard_b64decode(b64)
    except Exception as e:
        raise ValueError("PEM base64 解码失败: %s" % e)


def _extract_seed(priv_text: str) -> bytes:
    t = priv_text.strip()
    if "-----BEGIN" in t and "-----END" in t:
        der = _pem_payload(t)
        return der[-32:]  # PKCS8 ed25519 私钥末尾 32 字节即种子
    # 退化路径：纯 hex 种子
    try:
        return bytes.fromhex(re.sub(r"\s+", "", t))
    except Exception:
        raise ValueError("无法解析私钥：既非 PEM 也非 hex")


def _extract_point(pub_text: str) -> bytes:
    t = pub_text.strip()
    if "-----BEGIN" in t and "-----END" in t:
        der = _pem_payload(pub_text)
        return der[-32:]  # SPKI ed25519 公钥末尾 32 字节即压缩点
    try:
        return bytes.fromhex(re.sub(r"\s+", "", t))
    except Exception:
        raise ValueError("无法解析公钥：既非 PEM 也非 hex")


# ---------- SEAL 规范化与签名 ----------
def _canonical(seal: dict) -> str:
    """签名/验签共用的规范化载荷：排除 seal_signature 字段，其余按排序键紧凑 JSON。"""
    s = {k: v for k, v in seal.items() if k != "seal_signature"}
    return json.dumps(s, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _load_pubkey_pem(skill_root: str) -> str:
    p = os.path.join(skill_root, "assets", "pubkey.pem")
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


def _seal_path(skill_root: str) -> str:
    return os.path.join(skill_root, "provenance", "SEAL.json")


def _sha256_of_file(path: str) -> str:
    import hashlib as _hl
    h = _hl.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_seal(skill_root: str) -> bool:
    """H3 被动验签：用钉死的公钥验证 SEAL 签名，并逐文件比对哈希。
    缺失签名 / 签名不符 / 任一文件哈希变化 → False（拒绝运行）。"""
    try:
        sp = _seal_path(skill_root)
        if not os.path.isfile(sp):
            return False
        with open(sp, "r", encoding="utf-8") as f:
            seal = json.load(f)
        if "seal_signature" not in seal:
            return False
        pub_text = _load_pubkey_pem(skill_root)
        point = _extract_point(pub_text)
        payload = _canonical(seal).encode("utf-8")
        sig = base64.standard_b64decode(seal["seal_signature"])
        if not ed25519.verify(point, payload, sig):
            return False
        # 文件完整性：逐个比对 SEAL.files 中记录的 sha256
        for rel, meta in seal.get("files", {}).items():
            fp = os.path.join(skill_root, rel)
            if not os.path.isfile(fp):
                return False
            if _sha256_of_file(fp) != meta.get("sha256"):
                return False
        return True
    except Exception:
        return False


def cmd_gen_keys(args):
    import secrets
    seed = secrets.token_bytes(32)
    point = ed25519.public_key_from_seed(seed)
    skill_root = os.path.abspath(args.skill_root)
    os.makedirs(os.path.join(skill_root, "assets"), exist_ok=True)
    with open(os.path.join(skill_root, "assets", "pubkey.pem"), "w", encoding="utf-8") as f:
        f.write(_build_pub_pem(point))
    print("[OK] 公钥已写入: %s" % os.path.join(skill_root, "assets", "pubkey.pem"))
    print("[OK] 公钥(hex): %s" % point.hex())
    print()
    print("===== 以下私钥仅输出到本终端，请立即手动存入你的私有密钥库（如腾讯文档私有文档）=====")
    print("----- 私钥 PEM（签名时用，从 stdin 粘贴）-----")
    print(_build_priv_pem(seed))
    print("----- 私钥种子(hex，备用) -----")
    print(seed.hex())
    print("=====================================================================")
    print("⚠️ 私钥绝不允许进入技能包 / 技能目录 / 包内任何文本，也不会被本脚本写入任何本地文件。")
    print("   请将其粘贴进你的私有密钥库后，确保本终端输出不被记录/同步。")


def cmd_sign(args):
    skill_root = os.path.abspath(args.skill_root)
    sp = _seal_path(skill_root)
    if not os.path.isfile(sp):
        print("[错误] 找不到 SEAL: %s" % sp, file=sys.stderr)
        sys.exit(1)
    priv_text = sys.stdin.read()
    try:
        seed = _extract_seed(priv_text)
    except Exception as e:
        print("[错误] 无法从 stdin 解析私钥: %s" % e, file=sys.stderr)
        sys.exit(1)
    # 用同一私钥推导公钥，确认与钉死公钥一致（防签错包）
    point = ed25519.public_key_from_seed(seed)
    pinned = _extract_point(_load_pubkey_pem(skill_root))
    if point != pinned:
        print("[错误] stdin 私钥对应的公钥与钉死公钥不一致，拒绝签名。", file=sys.stderr)
        sys.exit(1)
    with open(sp, "r", encoding="utf-8") as f:
        seal = json.load(f)
    seal["signed_at"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    seal["signed_key_id"] = args.key_id or "edo-tensei-main"
    payload = _canonical(seal).encode("utf-8")
    sig = ed25519.sign_seed(seed, payload)
    seal["seal_signature"] = base64.standard_b64encode(sig).decode("ascii")
    with open(sp, "w", encoding="utf-8") as f:
        json.dump(seal, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("[OK] SEAL 已签名: %s" % sp)
    print("     signed_at:    %s" % seal["signed_at"])
    print("     signed_key_id:%s" % seal["signed_key_id"])


def cmd_verify(args):
    skill_root = os.path.abspath(args.skill_root) if args.skill_root else _default_skill_root()
    ok = verify_seal(skill_root)
    if ok:
        print("[门禁·通过] SEAL 验签成功，技能包完整可信。")
        sys.exit(0)
    else:
        print("[门禁·拒绝] SEAL 验签失败（缺签名/被篡改/公钥不符），拒绝执行维护或运行。", file=sys.stderr)
        sys.exit(1)


def cmd_freeze(args):
    _set_readonly(args.live_dir, True)


def cmd_unlock(args):
    priv_text = sys.stdin.read()
    try:
        seed = _extract_seed(priv_text)
    except Exception as e:
        print("[错误] 无法从 stdin 解析私钥: %s" % e, file=sys.stderr)
        sys.exit(1)
    point = ed25519.public_key_from_seed(seed)
    pinned = _extract_point(_load_pubkey_pem(_default_skill_root()))
    if point != pinned:
        print("[门禁·拒绝] 私钥核验失败，未授权，不解除冻结。", file=sys.stderr)
        sys.exit(1)
    _set_readonly(args.live_dir, False)


def _default_skill_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _set_readonly(tree: str, readonly: bool):
    """H1：对目录树递归设置/清除 Windows FILE_ATTRIBUTE_READONLY(=1)。"""
    tree = os.path.abspath(tree)
    if not os.path.isdir(tree):
        print("[错误] 目录不存在: %s" % tree, file=sys.stderr)
        sys.exit(1)
    if os.name != "nt":
        print("[提示] 非 Windows 平台，H1 系统只读属性跳过（仅记录意图）。", file=sys.stderr)
        return
    import ctypes
    kernel32 = ctypes.windll.kernel32
    READONLY = 1
    count = 0
    for root, dirs, files in os.walk(tree):
        for name in files:
            p = os.path.join(root, name)
            cur = kernel32.GetFileAttributesW(p)
            if cur == -1:
                continue
            if readonly:
                kernel32.SetFileAttributesW(p, cur | READONLY)
            else:
                kernel32.SetFileAttributesW(p, cur & ~READONLY)
            count += 1
    print("[OK] H1 %s完成：%s (文件数 %d)" %
          ("冻结" if readonly else "解冻", tree, count))


def _selftest_pem():
    import secrets
    seed = secrets.token_bytes(32)
    priv_pem = _build_priv_pem(seed)
    pub_pem = _build_pub_pem(ed25519.public_key_from_seed(seed))
    # 多行（标准）
    assert _extract_seed(priv_pem) == seed, "多行私钥解析失败"
    assert _extract_point(pub_pem) == ed25519.public_key_from_seed(seed), "多行公钥解析失败"
    # 单行（base64 与标记挤在一行）—— 旧算法会崩，新算法必须过
    single_priv = priv_pem.replace("\n", "")
    single_pub = pub_pem.replace("\n", "")
    assert _extract_seed(single_priv) == seed, "单行私钥解析失败"
    assert _extract_point(single_pub) == ed25519.public_key_from_seed(seed), "单行公钥解析失败"
    # 退化 hex
    assert _extract_seed(seed.hex()) == seed, "hex 私钥解析失败"
    print("[OK] PEM 解析自测通过（多行/单行/hex）")


def cmd_selftest(args):
    ed25519._self_test()
    _selftest_pem()


def main():
    ap = argparse.ArgumentParser(description="秽土转生技能包密钥门禁")
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("gen-keys", help="生成密钥对并写公钥")
    g.add_argument("skill_root", help="技能包根目录（写 assets/pubkey.pem）")
    g.set_defaults(func=cmd_gen_keys)

    s = sub.add_parser("sign", help="对 SEAL 签名（私钥从 stdin）")
    s.add_argument("skill_root", help="技能包根目录")
    s.add_argument("--key-id", default="edo-tensei-main", help="签名者密钥标识，写入 SEAL.signed_key_id")
    s.set_defaults(func=cmd_sign)

    v = sub.add_parser("verify", help="验证 SEAL 签名（H3）")
    v.add_argument("skill_root", nargs="?", default=None, help="技能包根目录（默认本脚本所在技能包）")
    v.set_defaults(func=cmd_verify)

    f = sub.add_parser("freeze", help="冻结活副本（H1 只读）")
    f.add_argument("live_dir", help="活副本目录（如 ~/.workbuddy/skills/edo-tensei）")
    f.set_defaults(func=cmd_freeze)

    u = sub.add_parser("unlock", help="解冻活副本（需私钥，H1）")
    u.add_argument("live_dir", help="活副本目录")
    u.set_defaults(func=cmd_unlock)

    st = sub.add_parser("selftest", help="自测")
    st.set_defaults(func=cmd_selftest)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
