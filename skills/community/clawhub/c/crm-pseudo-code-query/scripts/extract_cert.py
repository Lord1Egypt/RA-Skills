#!/usr/bin/env python3
"""
从 PKCS12 文件中提取指定用户的证书+私钥，写入 PEM 文件。
在 mTLS 客户端证书丢失时使用。

前置条件:
  1. HexinCA 已添加为受信任根证书:
     security find-certificate -c "HexinCA" -p > /tmp/hexin_ca.pem
     security add-trusted-cert -r trustRoot -k ~/Library/Keychains/login.keychain-db /tmp/hexin_ca.pem
  2. 已从 Keychain 导出 PKCS12 (需要用户在系统弹窗中点击"始终允许"):
     security export -k ~/Library/Keychains/login.keychain-db -t identities -f pkcs12 -P "temppass" -o /tmp/client_cert.p12

用法: python3 extract_cert.py [--email <email>] [--p12 <path>] [--output <path>]
示例: python3 extract_cert.py --email <你的邮箱>@myhexin.com --p12 /tmp/client_cert.p12 --output /tmp/my_cert.pem
"""
import subprocess
import re
import sys
import argparse

parser = argparse.ArgumentParser(description="从 PKCS12 提取 mTLS 客户端证书+私钥")
parser.add_argument("--email", default="", help="证书邮箱 (CN 匹配)，如 zhangsan@myhexin.com")
parser.add_argument("--p12", default="/tmp/client_cert.p12", help="PKCS12 文件路径")
parser.add_argument("--p12-pass", default="temppass", help="PKCS12 密码")
parser.add_argument("--output", default="/tmp/my_cert.pem", help="输出 PEM 文件路径")
args = parser.parse_args()

PKCS12_FILE = args.p12
PKCS12_PASS = args.p12_pass
OUTPUT_PEM = args.output
MATCH_EMAIL = args.email.lower()
if not MATCH_EMAIL:
    print("ERROR: 请通过 --email 指定你的证书邮箱，例如 --email zhangsan@myhexin.com")
    sys.exit(1)

# Extract everything from PKCS12 to PEM
result = subprocess.run(
    ["openssl", "pkcs12", "-in", PKCS12_FILE, "-password", f"pass:{PKCS12_PASS}", "-nodes"],
    capture_output=True, text=True
)
pem_data = result.stdout

if not pem_data.strip():
    print(f"ERROR: 无法读取 PKCS12 文件 {PKCS12_FILE}")
    print("请先运行:")
    print(f'  security export -k ~/Library/Keychains/login.keychain-db -t identities -f pkcs12 -P "{PKCS12_PASS}" -o {PKCS12_FILE}')
    sys.exit(1)

# Split into individual PEM blocks
blocks = re.split(r'(?=-----BEGIN)', pem_data)
blocks = [b.strip() for b in blocks if b.strip() and '-----BEGIN' in b]

certs = [b for b in blocks if 'CERTIFICATE' in b.split('\n')[0] and 'REQUEST' not in b.split('\n')[0]]
keys = [b for b in blocks if 'PRIVATE KEY' in b.split('\n')[0]]

print(f"Found {len(certs)} certificates and {len(keys)} private keys")

# Find the target cert by email
target_cert = None
target_idx = -1
for i, cert in enumerate(certs):
    result = subprocess.run(
        ["openssl", "x509", "-noout", "-subject"],
        input=cert, capture_output=True, text=True
    )
    subject = result.stdout.strip()
    print(f"  Cert {i}: {subject}")
    if MATCH_EMAIL in subject.lower():
        target_cert = cert
        target_idx = i

if target_cert is None:
    print(f"ERROR: 未找到匹配 {MATCH_EMAIL} 的证书")
    sys.exit(1)

print(f"\nFound target cert at index {target_idx}")

# Match the key by comparing modulus
def get_modulus(pem_block, is_key=False):
    if is_key:
        result = subprocess.run(["openssl", "rsa", "-modulus", "-noout"], input=pem_block, capture_output=True, text=True)
    else:
        result = subprocess.run(["openssl", "x509", "-modulus", "-noout"], input=pem_block, capture_output=True, text=True)
    return result.stdout.strip()

cert_mod = get_modulus(target_cert)
print(f"Cert modulus: {cert_mod[:40]}...")

matching_key = None
for i, key in enumerate(keys):
    key_mod = get_modulus(key, is_key=True)
    print(f"  Key {i} modulus: {key_mod[:40]}...")
    if key_mod == cert_mod:
        matching_key = key
        print(f"  -> MATCHES target cert!")
        break

if matching_key is None:
    print("ERROR: No matching private key found!")
    sys.exit(1)

# Write cert + key to output PEM
with open(OUTPUT_PEM, 'w') as f:
    f.write(target_cert)
    f.write('\n')
    f.write(matching_key)
    f.write('\n')

print(f"\nWritten cert+key to {OUTPUT_PEM}")

# Verify
result = subprocess.run(
    ["openssl", "x509", "-in", OUTPUT_PEM, "-noout", "-subject", "-issuer"],
    capture_output=True, text=True
)
print(f"Verification:\n{result.stdout}")
result = subprocess.run(
    ["openssl", "rsa", "-in", OUTPUT_PEM, "-check", "-noout"],
    capture_output=True, text=True
)
print(f"Key check: {result.stdout}{result.stderr}")
