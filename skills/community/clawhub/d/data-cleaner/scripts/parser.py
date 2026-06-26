"""
F1 · Multi-format parser
Supports: Excel (.xlsx/.xls), CSV/TSV, JSON, clipboard-pasted text.

Usage:
    from parser import parse_file, parse_text

    df = parse_file("path/to/data.xlsx")
    df = parse_file("path/to/data.csv")
    df = parse_text("姓名,电话\\n张三,13800138000")
"""

import io
import json
import re
import pandas as pd
from pathlib import Path
from typing import Union, List, Optional

# ─── Helpers ─────────────────────────────────────────────────────────────────

def _sniff_delimiter(text: str) -> str:
    """Sniff the most likely delimiter from the first few lines."""
    sample = text[:2000]
    for delim in [",", "\t", "|", ";"]:
        if delim in sample:
            return delim
    return ","

def _is_json(text: str) -> bool:
    text = text.strip()
    return text.startswith("{") or text.startswith("[")

def _is_excel(path: Union[str, Path]) -> bool:
    p = str(path).lower()
    return p.endswith(".xlsx") or p.endswith(".xls")

# ─── Core parsers ─────────────────────────────────────────────────────────────

def parse_file(
    path: Union[str, Path],
    sheet: Optional[Union[str, int]] = None,
    encoding: str = "utf-8",
) -> pd.DataFrame:
    """
    Auto-detect format and parse a file into a DataFrame.

    Parameters
    ----------
    path : file path
    sheet : for Excel files, sheet name or 0-indexed position
    encoding : text file encoding

    Returns
    -------
    pd.DataFrame
    """
    path = str(path)

    if _is_excel(path):
        return _parse_excel(path, sheet=sheet)

    suffix = Path(path).suffix.lower()
    if suffix in (".csv", ".tsv", ".txt"):
        return _parse_csv(path, delimiter=None, encoding=encoding)
    if suffix == ".json":
        return _parse_json(path)

    # fallback: try CSV then JSON
    try:
        return _parse_csv(path, delimiter=None, encoding=encoding)
    except Exception:
        return _parse_json(path)


def parse_text(text: str, format_hint: str = "auto") -> pd.DataFrame:
    """
    Parse clipboard / pasted text into a DataFrame.

    Parameters
    ----------
    text        : raw pasted content
    format_hint : "csv" | "tsv" | "json" | "auto"

    Returns
    -------
    pd.DataFrame
    """
    text = text.strip()
    if not text:
        raise ValueError("粘贴内容为空，请确认已复制数据。")

    if format_hint == "json" or (format_hint == "auto" and _is_json(text)):
        return _parse_json_str(text)

    if format_hint == "tsv" or (format_hint == "auto" and "\t" in text):
        return _parse_csv_str(text, delimiter="\t")

    # Default: sniff delimiter
    delim = _sniff_delimiter(text) if format_hint == "auto" else ","
    return _parse_csv_str(text, delimiter=delim)


# ─── Private implementations ───────────────────────────────────────────────────

def _parse_excel(path: str, sheet: Optional[Union[str, int]]) -> pd.DataFrame:
    try:
        import openpyxl
    except ImportError:
        raise ImportError("openpyxl is required to read .xlsx files. Install: pip install openpyxl")

    try:
        import xlrd
    except ImportError:
        pass  # .xls may not be readable but .xlsx will work

    xl_kwargs: dict = {"engine": "openpyxl"}
    if Path(path).suffix.lower() == ".xls":
        xl_kwargs["engine"] = "xlrd"

    if sheet is not None:
        xl_kwargs["sheet_name"] = sheet
    else:
        xl_kwargs["sheet_name"] = 0  # first sheet by default

    return pd.read_excel(path, **xl_kwargs)


def _parse_csv(path: str, delimiter: Optional[str], encoding: str) -> pd.DataFrame:
    if delimiter:
        return pd.read_csv(path, delimiter=delimiter, encoding=encoding, dtype=str, keep_default_na=False)
    # Auto-sniff
    try:
        return pd.read_csv(path, encoding=encoding, dtype=str, keep_default_na=False)
    except UnicodeDecodeError:
        for enc in ["gbk", "gb2312", "latin1"]:
            try:
                return pd.read_csv(path, encoding=enc, dtype=str, keep_default_na=False)
            except UnicodeDecodeError:
                continue
    raise ValueError(f"无法解析 CSV 文件 {path}，请确认文件编码（UTF-8 / GBK）。")


def _parse_json(path: str) -> pd.DataFrame:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return _json_to_df(data)


def _parse_csv_str(text: str, delimiter: str = ",") -> pd.DataFrame:
    df = pd.read_csv(io.StringIO(text), delimiter=delimiter, dtype=str, keep_default_na=False)
    # Strip whitespace from all cells
    df = df.apply(lambda col: col.astype(str).str.strip())
    return df


def _parse_json_str(text: str) -> pd.DataFrame:
    data = json.loads(text)
    return _json_to_df(data)


def _json_to_df(data) -> pd.DataFrame:
    """
    Handle three common JSON shapes:
      1. Array of flat objects  : [{a:1},{a:2}]
      2. Object with array field: {rows:[{a:1},...]}
      3. Nested / hierarchical  : flatten if possible
    """
    if isinstance(data, list):
        records = data
    elif isinstance(data, dict):
        # Try to find the array field
        for key in ["data", "rows", "records", "items", "list", "result"]:
            if key in data and isinstance(data[key], list):
                records = data[key]
                break
        else:
            records = [data]
    else:
        raise ValueError("JSON 结构不支持，请提供对象数组或包含数据数组的根对象。")

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    # Flatten any deeply nested columns (one level only)
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, dict)).any():
            exploded = df[col].apply(lambda x: x if isinstance(x, dict) else {})
            norm = pd.json_normalize(exploded)
            norm.columns = [f"{col}_{k}" for k in norm.columns]
            df = pd.concat([df.drop(columns=[col]), norm], axis=1)

    df = df.apply(lambda col: col.astype(str).str.strip())
    return df


# ─── Multi-file loader ─────────────────────────────────────────────────────────

def load_sources(
    sources: List[Union[str, Path, io.IOBase]],
    texts: Optional[List[str]] = None,
) -> List[pd.DataFrame]:
    """
    Load multiple data sources (files or pasted texts) into DataFrames.

    Returns list of (name, df) tuples.
    """
    results = []

    # Files
    for src in (sources or []):
        name = Path(src).name if isinstance(src, (str, Path)) else str(src)
        try:
            df = parse_file(src)
            results.append((name, df))
        except Exception as exc:
            raise ValueError(f"文件「{name}」解析失败：{exc}")

    # Pasted texts
    for i, text in enumerate(texts or []):
        name = f"粘贴数据_{i+1}"
        try:
            df = parse_text(text)
            results.append((name, df))
        except Exception as exc:
            raise ValueError(f"「{name}」解析失败：{exc}")

    return results


# ─── Quick peek (header preview) ──────────────────────────────────────────────

def preview_file(path: Union[str, Path], n: int = 5) -> pd.DataFrame:
    """Return first n rows without full load (for display)."""
    df = parse_file(path)
    return df.head(n)


def preview_text(text: str, n: int = 5) -> pd.DataFrame:
    """Return first n rows of pasted text (for display)."""
    df = parse_text(text)
    return df.head(n)
