#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""金融理论大师 —— CSV 读写公共层。

把「读数据集」与「渲染 CSV 文本」两件事各收敛成一个函数，供生成器、校验器、
查询工具共用。

写 CSV 的确定性要求：字段顺序固定、行顺序由调用方给定、行尾统一 "\n"、
开头写 UTF-8 BOM（便于 Excel 直接双击打开）。这三条在任何数据集上都一样，
所以只写一遍。
"""

from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Iterable, Mapping, Sequence

BOM = "\ufeff"


def read_csv(path: Path) -> list[dict[str, str]]:
    """读取带表头的 CSV，去掉 BOM，并把所有值 strip 掉。

    读不到文件或文件为空时抛 FileNotFoundError / ValueError，由调用方决定
    是报错还是降级——本函数不做静默兜底。

    Raises:
        FileNotFoundError: 路径不存在。
        ValueError: 文件没有表头，或只有表头没有数据行。
    """
    if not path.exists():
        raise FileNotFoundError(f"数据集不存在：{path}")
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            raise ValueError(f"数据集缺少表头：{path}")
        rows = [{k: (v or "").strip() for k, v in r.items()} for r in reader]
    if not rows:
        raise ValueError(f"数据集为空：{path}")
    return rows


def read_header(path: Path) -> list[str]:
    """只读表头，用于校验字段列是否齐全。"""
    if not path.exists():
        raise FileNotFoundError(f"数据集不存在：{path}")
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.reader(fh).__next__())


def render_csv(
    records: Iterable[Mapping[str, str]],
    fields: Sequence[str],
    sort_key=None,
) -> str:
    """把记录渲染为 CSV 文本，保证逐字节可复现。

    Args:
        records: 记录序列。
        fields: 字段顺序，同时决定列顺序。
        sort_key: 排序函数。None 表示不排序，保持传入顺序。

    Returns:
        带 BOM、以 "\\n" 换行的 CSV 文本。
    """
    rows = list(records)
    if sort_key is not None:
        rows = sorted(rows, key=sort_key)
    buf = io.StringIO()
    buf.write(BOM)
    writer = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for rec in rows:
        writer.writerow({k: rec.get(k, "") for k in fields})
    return buf.getvalue()


def write_if_changed(path: Path, text: str) -> bool:
    """写入文本；若内容与磁盘一致则跳过。

    避免无谓地改动 mtime——文件没变就不该显示为「已修改」。

    Returns:
        是否真的写入了。
    """
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="")
    return True


def tokens(value: str, separator: str = "|") -> set[str]:
    """把多值字段拆成集合，剔除空白与「—」。

    多值字段用 "|" 分隔（见 data/README.md）。空值与「不适用」标记都不算成员，
    否则互补/冲突关系判断会被「—」污染。
    """
    from schema import NOT_APPLICABLE

    return {
        t.strip()
        for t in value.split(separator)
        if t.strip() and t.strip() not in NOT_APPLICABLE
    }
