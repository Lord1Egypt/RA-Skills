"""markdown.py — dict/DataFrame → markdown 表格字符串"""
import pandas as pd

def dict_to_md(data, title=None, units=None):
    """dict 转 markdown 表格（key-value 对）"""
    if not data:
        return ""
    lines = []
    if title:
        lines.append(f"### {title}")
        lines.append("")
    rows = []
    for k, v in data.items():
        if isinstance(v, (list, dict, pd.DataFrame)):
            continue
        if isinstance(v, float):
            v = f"{v:.4f}"
        if _is_ndarray(v):
            # numpy 数组只显示摘要
            v = f"[array({len(v)} elements)]"
        rows.append(f"| {k} | {v} |")
    if rows:
        lines.append("| 指标 | 值 |")
        lines.append("|------|-----|")
        lines.extend(rows)
        lines.append("")
    return "\n".join(lines)


def _is_ndarray(v):
    """检查是否为 numpy ndarray（不是标量）"""
    return v.__class__.__module__ == 'numpy' and hasattr(v, 'shape') and len(v.shape) > 0


def df_to_md(df, title=None):
    """DataFrame 转 markdown 表格"""
    if df is None or df.empty:
        return ""
    lines = []
    if title:
        lines.append(f"### {title}")
        lines.append("")
    headers = "| " + " | ".join(str(c) for c in df.columns) + " |"
    sep = "| " + " | ".join("---" for _ in df.columns) + " |"
    lines.append(headers)
    lines.append(sep)
    for _, row in df.iterrows():
        vals = []
        for v in row:
            if isinstance(v, float):
                vals.append(f"{v:.4f}")
            else:
                vals.append(str(v))
        lines.append("| " + " | ".join(vals) + " |")
    lines.append("")
    return "\n".join(lines)


def section_to_md(title, content):
    """包装为一个 markdown 段落"""
    lines = [f"## {title}", "", content.strip(), ""]
    return "\n".join(lines)


def concat_md(*parts):
    """拼接多个 markdown 片段"""
    return "\n".join(p for p in parts if p.strip())
