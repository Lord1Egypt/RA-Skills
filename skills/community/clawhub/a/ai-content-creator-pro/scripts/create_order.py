#!/usr/bin/env python3
"""ai-content-creator-pro - Order Creation Script (Phase 1)

Buyout version: pay 楼9.90 once, use forever.
Creates local order file for clawtip payment processing.
AI generates content in conversation after payment.
"""
import argparse
import hashlib
import json
import os
import platform
import random
import re
import struct
import sys
import time

SLUG = "ai-content-creator-pro"
AMOUNT = 990  # 9.9 yuan = 990 fen (buyout)
DESCRIPTION = "Multi-platform content creation buyout (unlimited use)"
RESOURCE_URL = os.environ.get("CLAWTIP_RESOURCE_URL", f"https://clawhub.ai/skill/{SLUG}")

_INDICATOR_RE = re.compile(r"^[a-fA-F0-9]{32}$")
_ORDER_NO_RE = re.compile(r"^[0-9]{14,32}$")

def _validate_indicator(indicator):
    if not _INDICATOR_RE.fullmatch(indicator):
        raise ValueError("Invalid indicator format")
def _validate_order_no(order_no):
    if not _ORDER_NO_RE.fullmatch(order_no):
        raise ValueError("Invalid order_no format")
def _get_orders_dir(indicator):
    _validate_indicator(indicator)
    home = os.path.expanduser("~")
    if platform.system() == "Windows":
        return os.path.join(home, "openclaw", "skills", "orders", indicator)
    else:
        return os.path.join(home, ".openclaw", "skills", "orders", indicator)
def _save_order(indicator, order_no, order_data):
    _validate_order_no(order_no)
    order_dir = _get_orders_dir(indicator)
    os.makedirs(order_dir, exist_ok=True)
    path = os.path.join(order_dir, f"{order_no}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(order_data, f, ensure_ascii=False, indent=2)
    return path

_SBOX = [
    0xd6,0x90,0xe9,0xfe,0xcc,0xe1,0x3d,0xb7,0x16,0xb6,0x14,0xc2,0x28,0xfb,0x2c,0x05,0x2b,0x67,0x9a,0x76,0x2a,0xbe,0x04,0xc3,0xaa,0x44,0x13,0x26,0x49,0x86,0x06,0x99,0x9c,0x42,0x50,0xf4,0x91,0xef,0x98,0x7a,0x33,0x54,0x0b,0x43,0xed,0xcf,0xac,0x62,0xe4,0xb3,0x1c,0xa9,0xc9,0x08,0xe8,0x95,0x80,0xdf,0x94,0xfa,0x75,0x8f,0x3f,0xa6,0x47,0x07,0xa7,0xfc,0xf3,0x73,0x17,0xba,0x83,0x59,0x3c,0x19,0xe6,0x85,0x4f,0xa8,0x68,0x6b,0x81,0xb2,0x71,0x64,0xda,0x8b,0xf8,0xeb,0x0f,0x4b,0x70,0x56,0x9d,0x35,0x1e,0x24,0x0e,0x5e,0x63,0x58,0xd1,0xa2,0x25,0x22,0x7c,0x3b,0x01,0x21,0x78,0x87,0xd4,0x00,0x46,0x57,0x9f,0xd3,0x27,0x52,0x4c,0x36,0x02,0xe7,0xa0,0xc4,0xc8,0x9e,0xea,0xbf,0x8a,0xd2,0x40,0xc7,0x38,0xb5,0xa3,0xf7,0xf2,0xce,0xf9,0x61,0x15,0xa1,0xe0,0xae,0x5d,0xa4,0x9b,0x34,0x1a,0x55,0xad,0x93,0x32,0x30,0xf5,0x8c,0xb1,0xe3,0x1d,0xf6,0xe2,0x2e,0x82,0x66,0xca,0x60,0xc0,0x29,0x23,0xab,0x0d,0x53,0x4e,0x6f,0xd5,0xdb,0x37,0x45,0xde,0xfd,0x8e,0x2f,0x03,0xff,0x6a,0x72,0x6d,0x6c,0x5b,0x51,0x8d,0x1b,0xaf,0x92,0xbb,0xdd,0xbc,0x7f,0x11,0xd9,0x5c,0x41,0x1f,0x10,0x5a,0xd8,0x0a,0xc1,0x31,0x88,0xa5,0xcd,0x7b,0xbd,0x2d,0x74,0xd0,0x12,0xb8,0xe5,0xb4,0xb0,0x89,0x69,0x97,0x4a,0x0c,0x96,0x77,0x7e,0x65,0xb9,0xf1,0x09,0xc5,0x6e,0xc6,0x84,0x18,0xf0,0x7d,0xec,0x3a,0xdc,0x4d,0x20,0x79,0xee,0x5f,0x3e,0xd7,0xcb,0x39,0x48,
]
_FK = [0xa3b1bac6,0x56aa3350,0x677d9197,0xb27022dc]
_CK = [0x00070e15,0x1c232a31,0x383f464d,0x545b6269,0x70777e85,0x8c939aa1,0xa8afb6bd,0xc4cbd2d9,0xe0e7eef5,0xfc030a11,0x181f262d,0x343b4249,0x50575e65,0x6c737a81,0x888f969d,0xa4abb2b9,0xc0c7ced5,0xdce3eaf1,0xf8ff060d,0x141b2229,0x30373e45,0x4c535a61,0x686f767d,0x848b9299,0xa0a7aeb5,0xbcc3cad1,0xd8dfe6ed,0xf4fb0209,0x10171e25,0x2c333a41,0x484f565d,0x646b7279]
def _rotl(x, n): return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF
def _tau(a):
    b = 0
    for i in range(4): b |= _SBOX[(a >> (8*(3-i))) & 0xFF] << (8*(3-i))
    return b
def _l(b): return b ^ _rotl(b,2) ^ _rotl(b,10) ^ _rotl(b,18) ^ _rotl(b,24)
def _lp(b): return b ^ _rotl(b,13) ^ _rotl(b,23)
def _t(a): return _l(_tau(a))
def _tp(a): return _lp(_tau(a))
def _key_expand(key):
    mk = list(struct.unpack(">4I", key))
    k = [mk[i] ^ _FK[i] for i in range(4)]
    rk = []
    for i in range(32):
        k.append(k[i] ^ _tp(k[i+1] ^ k[i+2] ^ k[i+3] ^ _CK[i]))
        rk.append(k[i+4])
    return rk
def _enc_block(pt, rk):
    x = list(struct.unpack(">4I", pt))
    for i in range(32):
        tmp = x[i+1] ^ x[i+2] ^ x[i+3] ^ rk[i]
        x.append(x[i] ^ _t(tmp))
    return struct.pack(">4I", x[35], x[34], x[33], x[32])
def _sm4_encrypt_ecb(key, data):
    if len(key) != 16: raise ValueError("SM4 key must be 16 bytes")
    pad = 16 - (len(data) % 16)
    data = data + bytes([pad] * pad)
    rk = _key_expand(key)
    out = b""
    for i in range(0, len(data), 16): out += _enc_block(data[i:i+16], rk)
    return out
def _sm4_encrypt_hex(key_hex, plain):
    return _sm4_encrypt_ecb(bytes.fromhex(key_hex), plain.encode("utf-8")).hex()


def compute_indicator(slug: str) -> str:
    return hashlib.md5(slug.encode("utf-8")).hexdigest()

def generate_order_no() -> str:
    ts = int(time.time() * 1000)
    rand = random.randint(100000, 999999)
    return f"{ts}{rand}"

def create_order_file(question: str, indicator: str) -> dict:
    pay_to = os.environ.get("CLAWTIP_PAY_TO", "")
    sm4_key = os.environ.get("CLAWTIP_SM4_KEY", "")
    if not pay_to:
        print("WARNING: CLAWTIP_PAY_TO environment variable not set")
    if not sm4_key:
        print("WARNING: CLAWTIP_SM4_KEY environment variable not set")
    order_no = generate_order_no()
    encrypt_payload = json.dumps({"orderNo": order_no, "amount": str(AMOUNT), "payTo": pay_to}, ensure_ascii=False)
    encrypted_data = encrypt_payload
    if sm4_key:
        try:
            if len(sm4_key) == 32 and all(c in "0123456789abcdefABCDEF" for c in sm4_key):
                encrypted_data = _sm4_encrypt_hex(sm4_key, encrypt_payload)
            else:
                import base64; key_hex = base64.b64decode(sm4_key).hex()
                encrypted_data = _sm4_encrypt_hex(key_hex, encrypt_payload)
        except Exception as e:
            print(f"WARNING: SM4 encryption failed: {e}")
    order_data = {"payTo": pay_to, "amount": AMOUNT, "order_no": order_no, "encrypted_data": encrypted_data, "slug": SLUG, "question": question, "description": DESCRIPTION, "resource_url": RESOURCE_URL}
    _save_order(indicator, order_no, order_data)
    return order_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create ai-content-creator-pro buyout order")
    parser.add_argument("question", help="User question / consultation content")
    args = parser.parse_args()
    indicator = compute_indicator(SLUG)
    print("=" * 60)
    print("= Creating buyout order. Pay 9.90 once, use forever. =")
    print(f" Saved to: ~/.openclaw/skills/orders/{indicator}/")
    print(" Fields: orderNo, amount, question, slug, payTo, encrypted_data.")
    print(" Caution: question text is stored locally. No passwords or secrets.")
    print("=" * 60)
    try:
        order_data = create_order_file(args.question, indicator)
    except Exception as e:
        print(f"Order creation failed: {e}"); sys.exit(1)
    print(f"ORDER_NO={order_data['order_no']}")
    print(f"AMOUNT={order_data['amount']}")
    print(f"QUESTION={args.question}")
    print(f"INDICATOR={indicator}")

