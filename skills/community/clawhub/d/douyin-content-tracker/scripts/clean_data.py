"""
清洗数据.py
将原始 CSV 标准化，输出干净的数据文件
"""

import re
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from storage import DATA_DIR
from utils import compute_engagement_rate

# 路径配置
INPUT_DIR = DATA_DIR
OUTPUT_DIR = DATA_DIR

# 原始字段 -> 标准字段映射（精确匹配）
EXACT_COLUMN_MAP = {
    "视频标题": "标题",
    "作品标题": "标题",
    "描述": "标题",
    "点赞数": "点赞",
    "点赞": "点赞",
    "获赞": "点赞",
    "评论数": "评论",
    "评论": "评论",
    "转发数": "转发",
    "分享数": "转发",
    "转发": "转发",
    "收藏数": "收藏",
    "收藏": "收藏",
    "播放量": "播放",
    "播放次数": "播放",
    "观看数": "播放",
    "发布时间": "发布时间",
    "发布时间(原始)": "发布时间",
    "发布时间（原始）": "发布时间",
    "时间": "发布时间",
    "视频链接": "链接",
    "作品链接": "链接",
    "链接": "链接",
    "URL": "链接",
    "url": "链接",
    "博主昵称": "博主",
    "作者昵称": "博主",
    "账号昵称": "博主",
    "博主": "博主",
}

# 缺失标准列时的模糊匹配关键词
FUZZY_COLUMN_MAP = {
    "标题": ["标题", "文案", "描述"],
    "点赞": ["点赞", "获赞", "赞"],
    "评论": ["评论"],
    "转发": ["转发", "分享"],
    "收藏": ["收藏"],
    "播放": ["播放", "观看"],
    "发布时间": ["发布", "时间"],
    "链接": ["链接", "url", "地址"],
    "博主": ["博主", "作者", "账号", "昵称"],
}

# 主流程最小可用字段
CORE_REQUIRED = ["链接", "标题", "博主", "发布时间"]


def read_csv_with_fallback(filepath: Path) -> pd.DataFrame:
    """兼容不同导出编码"""
    encodings = ["utf-8-sig", "utf-8", "gb18030", "gbk", "utf-16"]
    for enc in encodings:
        try:
            df = pd.read_csv(filepath, encoding=enc)
            print(f"  读取编码：{enc}")
            return df
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("csv", b"", 0, 1, f"无法识别文件编码：{filepath.name}")


def normalize_col_name(name: object) -> str:
    return str(name).replace("\ufeff", "").strip()


def map_columns(df: pd.DataFrame) -> pd.DataFrame:
    """先精确匹配，再模糊匹配，提升兼容性"""
    df = df.rename(columns={col: normalize_col_name(col) for col in df.columns})

    # 精确匹配
    rename_map = {}
    for col in df.columns:
        target = EXACT_COLUMN_MAP.get(col)
        if target:
            rename_map[col] = target
    if rename_map:
        df = df.rename(columns=rename_map)

    # 模糊匹配：仅为缺失标准列补齐
    for target, keywords in FUZZY_COLUMN_MAP.items():
        if target in df.columns:
            continue
        for col in df.columns:
            col_text = normalize_col_name(col).lower()
            if any(k.lower() in col_text for k in keywords):
                df = df.rename(columns={col: target})
                break

    return df


def clean_number(val: object) -> int:
    """处理带单位数字，如 1.2万/3.4w/2k/1,234"""
    if pd.isna(val):
        return 0

    text = str(val).strip().replace(",", "").replace("，", "")
    if not text or text in {"--", "-", "暂无", "null", "None", "nan", "NaN"}:
        return 0

    m = re.search(r"-?\d+(?:\.\d+)?", text)
    if not m:
        return 0

    num = float(m.group(0))
    low = text.lower()
    if "亿" in text:
        num *= 100000000
    elif "万" in text or "w" in low:
        num *= 10000
    elif "千" in text or "k" in low:
        num *= 1000

    return int(num)


def parse_publish_time(val: object):
    """兼容中文相对时间与常见日期格式"""
    if pd.isna(val):
        return pd.NaT

    raw = str(val).strip()
    if not raw or raw in {"--", "-", "暂无", "null", "None", "nan", "NaN"}:
        return pd.NaT

    now = datetime.now()

    if raw == "刚刚":
        return now

    rules = [
        (r"(\d+)\s*秒前", "seconds"),
        (r"(\d+)\s*分钟前", "minutes"),
        (r"(\d+)\s*小时前", "hours"),
        (r"(\d+)\s*天前", "days"),
    ]
    for pattern, unit in rules:
        m = re.match(pattern, raw)
        if m:
            return now - timedelta(**{unit: int(m.group(1))})

    m = re.match(r"昨天(?:\s+(\d{1,2}:\d{1,2}))?", raw)
    if m:
        base = now - timedelta(days=1)
        hhmm = m.group(1)
        if hhmm:
            h, mi = hhmm.split(":")
            return base.replace(hour=int(h), minute=int(mi), second=0, microsecond=0)
        return base

    # 兼容无年份格式：03-21 12:30
    m = re.match(r"(\d{1,2})-(\d{1,2})(?:\s+(\d{1,2}:\d{1,2}))?$", raw)
    if m:
        month = int(m.group(1))
        day = int(m.group(2))
        hhmm = m.group(3) or "00:00"
        h, mi = hhmm.split(":")
        try:
            return datetime(now.year, month, day, int(h), int(mi))
        except ValueError:
            return pd.NaT

    normalized = (
        raw.replace("年", "-")
        .replace("月", "-")
        .replace("日", " ")
        .replace("/", "-")
        .strip()
    )
    return pd.to_datetime(normalized, errors="coerce")


def ensure_core_schema(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    missing = [c for c in CORE_REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(
            f"{source_name} 缺少关键字段 {missing}；当前列：{list(df.columns)}"
        )

    # 链接为空会导致后续步骤全跳过，提前在清洗阶段阻断并提示。
    df["链接"] = df["链接"].astype(str).str.strip()
    invalid = df["链接"].isin(["", "nan", "None", "null"])
    if invalid.any():
        print(f"  警告：检测到 {int(invalid.sum())} 条空链接，已剔除")
        df = df[~invalid].copy()

    if df.empty:
        raise ValueError(f"{source_name} 清洗后无有效链接数据")

    return df


def clean_csv(filepath: Path) -> pd.DataFrame:
    print(f"正在清洗：{filepath.name}")
    df = read_csv_with_fallback(filepath)
    if df.empty:
        print("  文件为空，跳过")
        return df

    df = map_columns(df)
    df = ensure_core_schema(df, filepath.name)

    required = ["点赞", "评论", "转发", "收藏", "发布时间"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        print(f"  警告：未识别字段 {missing}，请检查 CSV 列名")

    for col in ["点赞", "评论", "转发", "收藏", "播放"]:
        if col in df.columns:
            df[col] = df[col].apply(clean_number).astype(int)

    if "发布时间" in df.columns:
        df["发布时间"] = df["发布时间"].apply(parse_publish_time)

    if all(c in df.columns for c in ["点赞", "评论", "转发", "播放"]):
        df["互动率"] = compute_engagement_rate(df)

    df.drop_duplicates(subset=["链接"], inplace=True)

    out_path = OUTPUT_DIR / f"cleaned_{filepath.stem}.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")

    stats = []
    for col in required:
        if col in df.columns:
            if col == "发布时间":
                stats.append(f"{col}有效 {int(df[col].notna().sum())}/{len(df)}")
            else:
                stats.append(f"{col}>0 {int((df[col] > 0).sum())}/{len(df)}")
    if stats:
        print("  字段统计：" + "，".join(stats))

    print(f"已保存：{out_path.name}，共 {len(df)} 条")
    return df


def run():
    csv_files = [f for f in INPUT_DIR.glob("*.csv") if not f.stem.startswith("cleaned_")]
    if not csv_files:
        print("采集数据/ 目录下没有找到 CSV 文件")
        return

    for f in csv_files:
        try:
            clean_csv(f)
        except ValueError as e:
            print(f"  跳过 {f.name}：{e}")


if __name__ == "__main__":
    run()
