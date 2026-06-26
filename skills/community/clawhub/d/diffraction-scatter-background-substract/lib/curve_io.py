#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
curve_io.py — 1D curve file I/O
一维曲线文件读写

Handles loading and saving of 1D curve files (.txt, .csv, .dat, .xy, .gr).
处理一维曲线文件的加载与保存。
"""

from __future__ import annotations

import csv
import io
import os
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict, Any

import h5py
import numpy as np

from .curve_data import Curve1D, CurveMetadata

try:
    import fabio

    HAS_FABIO = True
except ImportError:
    fabio = None
    HAS_FABIO = False

# Supported 1D curve file extensions / 支持的一维曲线文件扩展名
CURVE_EXTS = {".txt", ".csv", ".dat", ".xy", ".gr"}

CURVE_OUTPUT_EXTS = {".txt", ".csv", ".dat", ".xy", ".gr", ".npy", ".h5", ".hdf5"}


@dataclass
class CurveColumnSpec:
    """
    Column mapping for one logical curve in a text table.
    文本表格中一条逻辑曲线的列映射。
    """

    x_column: int
    y_column: int
    label: str


def _split_text_line(line: str, delimiter: Optional[str]) -> List[str]:
    """Split one text line with optional delimiter. 用可选分隔符拆分文本行。"""
    if delimiter == "tab":
        return [part.strip() for part in line.split("\t")]
    if delimiter == "comma":
        return [part.strip() for part in line.split(",")]
    if delimiter == "space":
        return [part for part in line.split()]
    if delimiter:
        return [part.strip() for part in line.split(delimiter)]
    return line.split()


def _iter_numeric_rows(
    path: str,
    skip_header: int = 0,
    comment: str = "#",
    delimiter: Optional[str] = None,
    max_rows: int = 20,
) -> List[List[float]]:
    """
    Read a few numeric rows from a curve text file.
    从曲线文本文件中读取若干数值行。
    """
    rows: List[List[float]] = []
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        for _ in range(skip_header):
            next(handle, None)
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith(comment):
                continue
            parts = _split_text_line(line, delimiter)
            try:
                numeric = [float(part) for part in parts if str(part).strip() != ""]
            except ValueError:
                continue
            if numeric:
                rows.append(numeric)
            if len(rows) >= max_rows:
                break
    return rows


def inspect_curve_layout(
    path: str,
    parse_mode: str = "single",
    skip_header: int = 0,
    comment: str = "#",
    delimiter: Optional[str] = None,
    x_column: int = 0,
    y_column: int = 1,
) -> Dict[str, Any]:
    """
    Inspect numeric layout and derive logical curve column specs.
    检查数值列布局并推导逻辑曲线列映射。
    """
    rows = _iter_numeric_rows(
        path,
        skip_header=skip_header,
        comment=comment,
        delimiter=delimiter,
    )
    column_count = max((len(row) for row in rows), default=0)
    specs: List[CurveColumnSpec] = []
    normalized_mode = (parse_mode or "single").lower()

    if column_count == 0:
        return {
            "column_count": 0,
            "curve_specs": [],
            "preview_rows": rows,
            "parse_mode": normalized_mode,
        }

    if normalized_mode == "xyxy":
        pair_count = column_count // 2
        if pair_count <= 0:
            raise ValueError("XYXY 模式至少需要 2 列数值数据")
        specs = [
            CurveColumnSpec(
                x_column=pair_index * 2,
                y_column=pair_index * 2 + 1,
                label=f"curve_{pair_index + 1:02d}",
            )
            for pair_index in range(pair_count)
        ]
    elif normalized_mode == "xyyy":
        if column_count < 2:
            raise ValueError("XYYY 模式至少需要 2 列数值数据")
        specs = [
            CurveColumnSpec(
                x_column=x_column,
                y_column=col_index,
                label=f"curve_{curve_index + 1:02d}",
            )
            for curve_index, col_index in enumerate(range(1, column_count))
        ]
    else:
        if column_count <= max(x_column, y_column):
            raise ValueError(
                f"列数不足：检测到 {column_count} 列，但请求 x={x_column}, y={y_column}"
            )
        specs = [CurveColumnSpec(x_column=x_column, y_column=y_column, label="curve_01")]

    return {
        "column_count": column_count,
        "curve_specs": specs,
        "preview_rows": rows,
        "parse_mode": normalized_mode,
    }


def detect_curve_format(path: str) -> str:
    """
    Detect the format of a 1D curve file based on extension and content.
    根据扩展名和内容检测一维曲线文件格式。

    Returns one of: 'xy', 'csv', 'pyfai_dat', 'auto'
    """
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        return "csv"
    if ext in {".dat", ".xy"}:
        return "xy"
    if ext == ".gr":
        return "xy"
    if ext == ".txt":
        # Peek at first non-comment line to distinguish pyFAI .dat from plain xy
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    # pyFAI .dat files typically have 3 columns: q  I  sigma
                    parts = line.split()
                    if len(parts) >= 3:
                        return "pyfai_dat"
                    break
        except Exception:
            pass
        return "xy"
    return "auto"


def load_curve_file(
    path: str,
    x_column: int = 0,
    y_column: int = 1,
    skip_header: int = 0,
    comment: str = "#",
    delimiter: Optional[str] = None,
) -> Optional[Curve1D]:
    """
    Load a 1D curve from a text file.
    从文本文件加载一维曲线。

    Supports: plain space/tab-delimited xy, CSV, pyFAI .dat (3+ columns).

    Parameters / 参数
    -----------------
    path : str
        File path / 文件路径
    x_column : int
        Column index for x axis / x 轴列索引
    y_column : int
        Column index for y axis / y 轴列索引
    skip_header : int
        Number of header lines to skip / 跳过的头部行数
    comment : str
        Comment character / 注释字符
    delimiter : str or None
        Column delimiter (None = whitespace) / 列分隔符

    Returns / 返回
    ---------------
    Curve1D or None
        Loaded curve, or None on failure
    """
    fmt = detect_curve_format(path)
    try:
        if fmt == "csv":
            return _load_csv(path, x_column, y_column, skip_header, comment)
        elif fmt == "pyfai_dat":
            return _load_pyfai_dat(path, x_column, y_column, comment)
        else:
            return _load_xy(path, x_column, y_column, skip_header, comment, delimiter)
    except Exception:
        return None


def load_curve_collection(
    path: str,
    parse_mode: str = "single",
    x_column: int = 0,
    y_column: int = 1,
    skip_header: int = 0,
    comment: str = "#",
    delimiter: Optional[str] = None,
) -> List[Curve1D]:
    """
    Load one or more logical curves from the same text table.
    从同一个文本表格中加载一条或多条逻辑曲线。
    """
    layout = inspect_curve_layout(
        path=path,
        parse_mode=parse_mode,
        skip_header=skip_header,
        comment=comment,
        delimiter=delimiter,
        x_column=x_column,
        y_column=y_column,
    )
    curves: List[Curve1D] = []
    for spec in layout["curve_specs"]:
        curve = load_curve_file(
            path=path,
            x_column=spec.x_column,
            y_column=spec.y_column,
            skip_header=skip_header,
            comment=comment,
            delimiter=delimiter,
        )
        if curve is None:
            continue
        curve.metadata.extra["curve_label"] = spec.label
        curve.metadata.extra["x_column"] = spec.x_column
        curve.metadata.extra["y_column"] = spec.y_column
        curve.metadata.extra["parse_mode"] = layout["parse_mode"]
        curves.append(curve)
    return curves


def _load_xy(
    path: str,
    x_col: int,
    y_col: int,
    skip_header: int,
    comment: str,
    delimiter: Optional[str],
) -> Curve1D:
    """Load space/tab delimited xy file."""
    x_vals: List[float] = []
    y_vals: List[float] = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for _ in range(skip_header):
            next(f, None)
        for line in f:
            line = line.strip()
            if not line or line.startswith(comment):
                continue
            parts = line.split(delimiter) if delimiter else line.split()
            if len(parts) > max(x_col, y_col):
                try:
                    x_vals.append(float(parts[x_col]))
                    y_vals.append(float(parts[y_col]))
                except ValueError:
                    continue
    return Curve1D(
        x=np.array(x_vals, dtype=np.float64),
        y=np.array(y_vals, dtype=np.float64),
        metadata=CurveMetadata(
            source_file=path,
            source_type="1d_curve",
            x_label="x",
            y_label="I",
        ),
    )


def _load_csv(
    path: str,
    x_col: int,
    y_col: int,
    skip_header: int,
    comment: str,
) -> Curve1D:
    """Load CSV file with header detection."""
    x_vals: List[float] = []
    y_vals: List[float] = []
    with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.reader(f)
        for _ in range(skip_header):
            next(reader, None)
        for row in reader:
            if not row:
                continue
            if row[0].startswith(comment):
                continue
            try:
                x_vals.append(float(row[x_col]))
                y_vals.append(float(row[y_col]))
            except (ValueError, IndexError):
                continue
    return Curve1D(
        x=np.array(x_vals, dtype=np.float64),
        y=np.array(y_vals, dtype=np.float64),
        metadata=CurveMetadata(
            source_file=path,
            source_type="1d_curve",
            x_label="x",
            y_label="I",
        ),
    )


def _load_pyfai_dat(
    path: str,
    x_col: int,
    y_col: int,
    comment: str,
) -> Curve1D:
    """Load pyFAI .dat file (typically 3 columns: q  I  sigma)."""
    x_vals: List[float] = []
    y_vals: List[float] = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(comment):
                continue
            parts = line.split()
            if len(parts) > max(x_col, y_col):
                try:
                    x_vals.append(float(parts[x_col]))
                    y_vals.append(float(parts[y_col]))
                except ValueError:
                    continue
    return Curve1D(
        x=np.array(x_vals, dtype=np.float64),
        y=np.array(y_vals, dtype=np.float64),
        metadata=CurveMetadata(
            source_file=path,
            source_type="1d_curve",
            x_label="q",
            y_label="I",
            x_unit="A^-1",
        ),
    )


def save_curve_file(
    curve: Curve1D,
    path: str,
    fmt: str = "auto",
    include_header: bool = True,
    delimiter: str = "\t",
    data_type: str = "raw",
) -> bool:
    """
    Save a 1D curve to a text file.
    保存一维曲线到文本文件。

    Parameters / 参数
    -----------------
    curve : Curve1D
        Curve to save / 要保存的曲线
    path : str
        Output file path / 输出文件路径
    fmt : str
        'auto', 'xy', 'csv' / 格式
    include_header : bool
        Whether to write comment header / 是否写入注释头部
    delimiter : str
        Column delimiter / 列分隔符
    data_type : str
        Which data to save: 'raw' (main y), 'background', 'subtracted'
        要保存的数据类型：'raw'(主y值)、'background'(背景)、'subtracted'(扣除后)

    Returns / 返回
    ---------------
    bool
        Success / 是否成功
    """
    try:
        ext = os.path.splitext(path)[1].lower()
        meta = curve.metadata
        if fmt == "auto":
            if ext == ".csv":
                fmt = "csv"
            elif ext in {".h5", ".hdf5"}:
                fmt = "h5"
            else:
                fmt = "xy"

        # Select y data based on type / 根据类型选择y数据
        if data_type == "background":
            if curve.background is None:
                return False
            y_data = curve.background
            y_label = f"{meta.y_label}_background"
        elif data_type == "subtracted":
            if curve.subtracted is None:
                return False
            y_data = curve.subtracted
            y_label = f"{meta.y_label}_subtracted"
        else:  # raw
            y_data = curve.y
            y_label = meta.y_label

        lines: List[str] = []
        if include_header:
            lines.append(f"# source: {meta.source_file}")
            lines.append(f"# x_label: {meta.x_label}")
            lines.append(f"# y_label: {y_label}")
            lines.append(f"# data_type: {data_type}")
            if meta.x_unit:
                lines.append(f"# x_unit: {meta.x_unit}")
            if meta.process_mode:
                lines.append(f"# process_mode: {meta.process_mode.value}")
            lines.append(f"# n_points: {curve.n_points}")
            if meta.extra:
                for k, v in meta.extra.items():
                    lines.append(f"# {k}: {v}")

        if fmt == "npy":
            payload = np.column_stack((curve.x, y_data)).astype(np.float64)
            np.save(path, payload)
            return True
        if fmt == "h5":
            with h5py.File(path, "w") as handle:
                handle.create_dataset("x", data=curve.x.astype(np.float64))
                handle.create_dataset("y", data=y_data.astype(np.float64))
                meta_group = handle.require_group("metadata")
                meta_group.attrs["source_file"] = meta.source_file
                meta_group.attrs["x_label"] = meta.x_label
                meta_group.attrs["y_label"] = y_label
                meta_group.attrs["data_type"] = data_type
                if meta.x_unit:
                    meta_group.attrs["x_unit"] = meta.x_unit
                if meta.process_mode:
                    meta_group.attrs["process_mode"] = meta.process_mode.value
                for key, value in meta.extra.items():
                    meta_group.attrs[str(key)] = str(value)
            return True
        if fmt == "csv":
            if include_header:
                x_lbl = meta.x_label
                lines.append(f"{x_lbl},{y_label}")
            for i in range(curve.n_points):
                lines.append(f"{curve.x[i]:.8e},{y_data[i]:.8e}")
        else:
            for i in range(curve.n_points):
                lines.append(f"{curve.x[i]:.8e}{delimiter}{y_data[i]:.8e}")

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return True
    except Exception:
        return False


def save_curve_with_background(
    curve: Curve1D,
    path: str,
    include_bg: bool = True,
    include_subtracted: bool = True,
    fmt: str = "xy",
) -> bool:
    """
    Save a 1D curve with optional background and subtracted columns.
    保存一维曲线，可选包含背景列和扣除列。
    """
    try:
        normalized_fmt = "csv" if fmt == "csv" else ("h5" if fmt == "h5" else "xy")
        lines: List[str] = []
        meta = curve.metadata
        lines.append(f"# source: {meta.source_file}")
        if meta.process_mode:
            lines.append(f"# process_mode: {meta.process_mode.value}")

        has_bg = include_bg and curve.background is not None
        has_sub = include_subtracted and curve.subtracted is not None
        bg_values = curve.background if has_bg else None
        sub_values = curve.subtracted if has_sub else None

        header_parts = [meta.x_label, meta.y_label]
        if has_bg:
            header_parts.append("background")
        if has_sub:
            header_parts.append("subtracted")
        separator = "," if normalized_fmt == "csv" else "\t"
        lines.append("# " + separator.join(header_parts))

        if normalized_fmt == "h5":
            with h5py.File(path, "w") as handle:
                handle.create_dataset("x", data=curve.x.astype(np.float64))
                handle.create_dataset("raw", data=curve.y.astype(np.float64))
                if bg_values is not None:
                    handle.create_dataset(
                        "background", data=np.asarray(bg_values, dtype=np.float64)
                    )
                if sub_values is not None:
                    handle.create_dataset(
                        "subtracted", data=np.asarray(sub_values, dtype=np.float64)
                    )
                meta_group = handle.require_group("metadata")
                meta_group.attrs["source_file"] = meta.source_file
                if meta.process_mode:
                    meta_group.attrs["process_mode"] = meta.process_mode.value
                for key, value in meta.extra.items():
                    meta_group.attrs[str(key)] = str(value)
            return True

        for i in range(curve.n_points):
            row = [f"{curve.x[i]:.8e}", f"{curve.y[i]:.8e}"]
            if bg_values is not None:
                row.append(f"{bg_values[i]:.8e}")
            if sub_values is not None:
                row.append(f"{sub_values[i]:.8e}")
            lines.append(separator.join(row))

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return True
    except Exception:
        return False


def save_curve_collection(
    curves: List[Curve1D],
    path: str,
    fmt: str = "xy",
    include_bg: bool = True,
    include_subtracted: bool = True,
) -> bool:
    """
    Save multiple processed curves into one merged file.
    将多条处理后的曲线合并保存到单个文件。
    """
    try:
        if not curves:
            return False
        normalized_fmt = "csv" if fmt == "csv" else ("h5" if fmt == "h5" else "xy")
        if normalized_fmt == "h5":
            with h5py.File(path, "w") as handle:
                meta_group = handle.require_group("metadata")
                meta_group.attrs["curve_count"] = len(curves)
                for index, curve in enumerate(curves):
                    curve_group = handle.require_group(f"curves/curve_{index:03d}")
                    curve_group.create_dataset("x", data=curve.x.astype(np.float64))
                    curve_group.create_dataset("raw", data=curve.y.astype(np.float64))
                    if include_bg and curve.background is not None:
                        curve_group.create_dataset(
                            "background", data=np.asarray(curve.background, dtype=np.float64)
                        )
                    if include_subtracted and curve.subtracted is not None:
                        curve_group.create_dataset(
                            "subtracted", data=np.asarray(curve.subtracted, dtype=np.float64)
                        )
                    curve_group.attrs["source_file"] = curve.metadata.source_file
                    curve_group.attrs["curve_label"] = curve.metadata.extra.get(
                        "curve_label", f"curve_{index + 1:02d}"
                    )
            return True

        separator = "," if normalized_fmt == "csv" else "\t"
        lines: List[str] = [f"# merged_curve_count: {len(curves)}"]
        for index, curve in enumerate(curves):
            label = curve.metadata.extra.get("curve_label", f"curve_{index + 1:02d}")
            lines.append(f"# curve[{index}]: {curve.metadata.source_file} | label={label}")

        column_labels: List[str] = []
        matrix_parts: List[np.ndarray] = []
        for index, curve in enumerate(curves):
            label = str(curve.metadata.extra.get("curve_label", f"curve_{index + 1:02d}"))
            matrix_parts.append(curve.x.reshape(-1, 1))
            column_labels.append(f"x_{label}")
            matrix_parts.append(curve.y.reshape(-1, 1))
            column_labels.append(f"raw_{label}")
            if include_bg and curve.background is not None:
                matrix_parts.append(np.asarray(curve.background, dtype=np.float64).reshape(-1, 1))
                column_labels.append(f"background_{label}")
            if include_subtracted and curve.subtracted is not None:
                matrix_parts.append(np.asarray(curve.subtracted, dtype=np.float64).reshape(-1, 1))
                column_labels.append(f"subtracted_{label}")

        matrix = np.hstack(matrix_parts)
        lines.append("# " + separator.join(column_labels))
        for row in matrix:
            lines.append(separator.join(f"{float(value):.8e}" for value in row))
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(lines) + "\n")
        return True
    except Exception:
        return False


def is_1d_curve_file(path: str) -> bool:
    """Check if a file is a 1D curve format / 检查文件是否为 1D 曲线格式"""
    ext = os.path.splitext(path)[1].lower()
    return ext in CURVE_EXTS
