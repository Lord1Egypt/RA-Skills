#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""id_verify.py — 加密ID来源认证工具（Ed25519 非对称签名）

用法（命令行）：
  python id_verify.py genkey --dir ./keys
  python id_verify.py issue --key ./keys/signing.key --cid CUST-001 --dh DH-001 --ver 1.0.0 --out cert.json
  python id_verify.py verify --cert cert.json --pub ./keys/verify.pub --revoke revoke.txt
  python id_verify.py revoke --revoke revoke.txt --cid CUST-001

说明：
- 私钥仅用于签发（生产应置于 HSM/KMS，永不进发布包，见 18）；
- 公钥公开，任何人可验签；
- 吊销表每行一个客户 ID，命中即 revoked；
- 输出凭证为 JSON，含签名与指纹哈希，可进 07 追溯链。
"""
import argparse, hashlib, json, os, sys, time

# 优先 cryptography，回退 openssl CLI
try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
    from cryptography.hazmat.primitives import serialization
    HAVE_CRYPTO = True
except Exception:
    HAVE_CRYPTO = False

ISSUER = "注册老炮"


def _payload(iss, cid, dh, ver, iat, dh_hash):
    return f"{iss}|{cid}|{dh}|{ver}|{iat}|{dh_hash}"


def genkey(outdir):
    os.makedirs(outdir, exist_ok=True)
    if HAVE_CRYPTO:
        priv = Ed25519PrivateKey.generate()
        priv_pem = priv.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        pub_pem = priv.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    else:
        import subprocess
        subprocess.run(["openssl", "genpkey", "-algorithm", "ed25519",
                        "-out", os.path.join(outdir, "signing.key")], check=True)
        subprocess.run(["openssl", "pkey", "-in", os.path.join(outdir, "signing.key"),
                        "-pubout", "-out", os.path.join(outdir, "verify.pub")], check=True)
        return
    with open(os.path.join(outdir, "signing.key"), "wb") as f:
        f.write(priv_pem)
    with open(os.path.join(outdir, "verify.pub"), "wb") as f:
        f.write(pub_pem)
    print(f"[genkey] 已生成密钥对 -> {outdir}（私钥仅签发用，勿进发布包）")


def issue(key_path, cid, dh, ver, out_path):
    iat = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    dh_hash = hashlib.sha256(f"{cid}|{dh}".encode()).hexdigest()[:32]
    payload = _payload(ISSUER, cid, dh, ver, iat, dh_hash)
    if HAVE_CRYPTO:
        with open(key_path, "rb") as f:
            priv = serialization.load_pem_private_key(f.read(), password=None)
        sig = priv.sign(payload.encode())
    else:
        import subprocess, tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".bin", delete=False) as tf:
            tf.write(payload)
            tfn = tf.name
        subprocess.run(["openssl", "pkeyutl", "-sign", "-inkey", key_path,
                        "-in", tfn, "-out", tfn + ".sig"], check=True)
        sig = open(tfn + ".sig", "rb").read()
        os.unlink(tfn); os.unlink(tfn + ".sig")
    cert = {
        "iss": ISSUER, "cid": cid, "dh": dh, "ver": ver, "iat": iat,
        "hash": "sha256:" + dh_hash,
        "sig": sig.hex(),
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, ensure_ascii=False, indent=2)
    print(f"[issue] 已签发凭证 -> {out_path}")


def verify(cert_path, pub_path, revoke_path=None):
    with open(cert_path, encoding="utf-8") as f:
        cert = json.load(f)
    payload = _payload(cert["iss"], cert["cid"], cert["dh"], cert["ver"], cert["iat"], cert["hash"].split(":", 1)[1])
    try:
        sig = bytes.fromhex(cert["sig"])
        if HAVE_CRYPTO:
            with open(pub_path, "rb") as f:
                pub = serialization.load_pem_public_key(f.read())
            pub.verify(sig, payload.encode())
        else:
            import subprocess, tempfile
            with tempfile.NamedTemporaryFile("w", suffix=".bin", delete=False) as tf:
                tf.write(payload); tfn = tf.name
            with open(tfn + ".sig", "wb") as sf:
                sf.write(sig)
            r = subprocess.run(["openssl", "pkeyutl", "-verify", "-pubin", "-inkey", pub_path,
                                "-in", tfn, "-sigfile", tfn + ".sig"], capture_output=True, text=True)
            os.unlink(tfn); os.unlink(tfn + ".sig")
            if "Signature Verified" not in r.stdout:
                raise ValueError("bad signature")
        sig_ok = True
    except Exception:
        sig_ok = False
    status = "valid"
    if revoke_path and os.path.exists(revoke_path):
        with open(revoke_path, encoding="utf-8") as f:
            if cert["cid"] in [ln.strip() for ln in f if ln.strip()]:
                status = "revoked"
    result = {
        "valid": sig_ok and status == "valid",
        "issuer": cert["iss"], "cid": cert["cid"], "version": cert["ver"],
        "issued_at": cert["iat"], "status": status, "hash": cert["hash"],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def revoke(revoke_path, cid):
    lines = []
    if os.path.exists(revoke_path):
        with open(revoke_path, encoding="utf-8") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    if cid not in lines:
        lines.append(cid)
    with open(revoke_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[revoke] 已吊销 {cid} -> {revoke_path}")


def main():
    ap = argparse.ArgumentParser(description="加密ID来源认证工具（Ed25519）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("genkey"); p1.add_argument("--dir", required=True)
    p2 = sub.add_parser("issue"); p2.add_argument("--key", required=True)
    p2.add_argument("--cid", required=True); p2.add_argument("--dh", required=True)
    p2.add_argument("--ver", default="1.0.0"); p2.add_argument("--out", required=True)
    p3 = sub.add_parser("verify"); p3.add_argument("--cert", required=True)
    p3.add_argument("--pub", required=True); p3.add_argument("--revoke")
    p4 = sub.add_parser("revoke"); p4.add_argument("--revoke", required=True)
    p4.add_argument("--cid", required=True)
    a = ap.parse_args()
    if a.cmd == "genkey": genkey(a.dir)
    elif a.cmd == "issue": issue(a.key, a.cid, a.dh, a.ver, a.out)
    elif a.cmd == "verify": verify(a.cert, a.pub, a.revoke)
    elif a.cmd == "revoke": revoke(a.revoke, a.cid)


if __name__ == "__main__":
    main()
