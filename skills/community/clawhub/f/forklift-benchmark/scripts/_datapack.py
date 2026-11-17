#!/usr/bin/env python3
"""FK-Bench Skill — 数据集打包/解包模块(版权保护)。

把 data/v2.0 下的明文 JSON 压缩并异或混淆成一个 ``data.bin``，
运行时按需解包，避免他人直接翻阅题目与 gold 答案。

说明: 此层用于增加"快速模仿"的成本, 而非密码学级防护——密钥随 skill
分发, 有能力的人仍可解开。真正的约束来自 LICENSE.md 的授权条款。
"""

from __future__ import annotations

import json
import struct
import zlib
from pathlib import Path

# 打包数据头: magic "FKB2" + 解压后长度(小端 uint32)
_MAGIC = b"FKB2"
# 混淆密钥(固定 40 字节)。分发前可自行替换成任意 hex 串。
_KEY = bytes.fromhex(
    "9d3b71a6c2f04e8d5b9a1c7f3e6d2a4b8c5f0e1d7a3b6c9f2e5d8a0b7c4f1e"
)


def _xor(data: bytes) -> bytes:
    k = _KEY
    return bytes(b ^ k[i % len(k)] for i, b in enumerate(data))


def pack_dir(src_dir: Path, out_path: Path) -> int:
    """把 src_dir 下所有题目 JSON 打包成单个 data.bin, 返回条目数。

    只打包 fk-*.json(题目: fk-500-* 基础题 + fk-ext-* / fk-ext2-* 扩充题),
    跳过 index.json 等汇总文件。
    """
    items: dict[str, str] = {}
    for p in sorted(src_dir.glob("fk-*.json")):
        items[p.name] = p.read_text(encoding="utf-8")
    blob = json.dumps(items, ensure_ascii=False).encode("utf-8")
    comp = zlib.compress(blob, 9)
    enc = _xor(comp)
    out_path.write_bytes(_MAGIC + struct.pack("<I", len(blob)) + enc)
    return len(items)


def load_pack(path: Path) -> dict[str, str]:
    """读取 data.bin, 返回 {文件名: JSON 文本}。"""
    raw = path.read_bytes()
    if raw[:4] != _MAGIC:
        raise ValueError(f"not a valid data pack: {path}")
    (orig_len,) = struct.unpack("<I", raw[4:8])
    blob = zlib.decompress(_xor(raw[8:]))
    if len(blob) != orig_len:
        raise ValueError("data pack corrupted (length mismatch)")
    return json.loads(blob.decode("utf-8"))
