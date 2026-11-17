#!/usr/bin/env python3
"""内置医学术语表资产管理（路径解析 + 引擎兼容预检）。

CSV 格式对齐 BabelDOC Glossary.from_csv：表头必须恰为 source,target,tgt_lng
（无 BOM——双 BOM 会让 chardet 剥一剩一，表头损坏导致引擎 ValueError，
doc-holmes v2.1.0 差量评审实录）。
"""

import csv
import os

_FILENAME = "medical_glossary.csv"
_REQUIRED_HEADER = ["source", "target", "tgt_lng"]


def glossary_path() -> str:
    """内置术语表绝对路径（随包分发：pip 包/打包视图/开发树均按 __file__ 解析）。"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", _FILENAME)


def glossary_csv_ok(path: str = None) -> bool:
    """注入前预检：文件存在、表头与引擎要求一致（DictReader 严格比对，BOM 不容忍）。"""
    path = path or glossary_path()
    if not os.path.isfile(path):
        return False
    try:
        with open(path, encoding="utf-8") as f:  # 故意不用 utf-8-sig：BOM 必须暴露为错误
            reader = csv.DictReader(f)
            return reader.fieldnames == _REQUIRED_HEADER
    except Exception:
        return False
