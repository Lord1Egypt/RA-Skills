"""
外卖评价数据加载器 - 支持CSV/Excel导入，自动识别各平台格式
支持：美团外卖、饿了么/淘宝闪购、京东外卖
"""
import pandas as pd
import json
import os
import re
from datetime import datetime
from pathlib import Path

# 各平台CSV列名映射（中文列名 → 标准字段名）
PLATFORM_COLUMN_MAP = {
    "meituan": {
        "评价内容": "content", "评论内容": "content", "评价": "content",
        "评分": "rating", "综合评分": "rating", "星级": "rating", "star": "rating",
        "评价时间": "review_time", "评论时间": "review_time", "时间": "review_time",
        "用户名": "user_name", "用户": "user_name", "顾客": "user_name",
        "配送时长": "delivery_time", "送达时间": "delivery_time",
        "菜品": "dish_name", "商品": "dish_name", "订单内容": "dish_name",
        "回复": "reply", "商家回复": "reply",
    },
    "eleme": {
        "评价内容": "content", "评论": "content",
        "评分": "rating", "综合评分": "rating",
        "评价时间": "review_time", "时间": "review_time",
        "用户名": "user_name", "顾客": "user_name",
        "配送时长": "delivery_time",
        "菜品": "dish_name", "商品": "dish_name",
        "回复": "reply",
    },
    "jd": {
        "评价内容": "content", "评论": "content",
        "评分": "rating", "综合评分": "rating",
        "评价时间": "review_time", "时间": "review_time",
        "用户名": "user_name", "顾客": "user_name",
        "配送时长": "delivery_time",
        "商品": "dish_name", "菜品": "dish_name",
        "回复": "reply",
    },
}

# 平台识别关键词
PLATFORM_KEYWORDS = {
    "meituan": ["美团", "meituan", "mt", "wm"],
    "eleme": ["饿了么", "淘宝闪购", "eleme", "elm", "饿"],
    "jd": ["京东", "jd", "jingdong"],
}


def detect_platform(filename: str = "", df: pd.DataFrame = None) -> str:
    """自动识别平台类型"""
    filename_lower = filename.lower()

    # 按文件名识别
    for platform, keywords in PLATFORM_KEYWORDS.items():
        for kw in keywords:
            if kw in filename_lower:
                return platform

    # 按列名识别
    if df is not None:
        cols = " ".join(df.columns.astype(str).str.lower())
        if "美团" in cols or "meituan" in cols:
            return "meituan"
        if "饿了么" in cols or "eleme" in cols or "闪购" in cols:
            return "eleme"
        if "京东" in cols or "jd" in cols:
            return "jd"

    return "unknown"


def normalize_columns(df: pd.DataFrame, platform: str = "unknown") -> pd.DataFrame:
    """标准化列名"""
    column_map = PLATFORM_COLUMN_MAP.get(platform, {})
    if not column_map:
        # 尝试所有平台的映射
        for p in ["meituan", "eleme", "jd"]:
            column_map.update(PLATFORM_COLUMN_MAP[p])

    df = df.copy()
    rename_map = {}
    for col in df.columns:
        col_stripped = col.strip()
        if col_stripped in column_map:
            rename_map[col] = column_map[col_stripped]

    df.rename(columns=rename_map, inplace=True)
    return df


def parse_rating(value) -> float:
    """解析评分值"""
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        rating = float(value)
        # 如果是百分制，转为5分制
        if rating > 5:
            rating = rating / 20
        return min(5.0, max(0.0, rating))
    # 字符串解析
    s = str(value).strip()
    # 匹配数字
    match = re.search(r'(\d+(?:\.\d+)?)', s)
    if match:
        rating = float(match.group(1))
        if rating > 5:
            rating = rating / 20
        return min(5.0, max(0.0, rating))
    return None


def parse_time(value):
    """解析时间字段"""
    if pd.isna(value):
        return None
    try:
        if isinstance(value, (int, float)):
            # Unix timestamp (秒或毫秒)
            if value > 1e12:
                return datetime.fromtimestamp(value / 1000)
            elif value > 1e9:
                return datetime.fromtimestamp(value)
        dt = pd.to_datetime(value, errors='coerce')
        if pd.notna(dt):
            return dt
    except Exception:
        pass
    return None


def load_reviews(file_path: str, platform: str = None) -> pd.DataFrame:
    """
    加载评价数据文件
    支持: .csv, .xlsx, .xls, .json
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    ext = path.suffix.lower()

    # 加载文件
    if ext == '.csv':
        # 尝试不同编码
        for enc in ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']:
            try:
                df = pd.read_csv(file_path, encoding=enc)
                break
            except (UnicodeDecodeError, UnicodeError):
                continue
        else:
            df = pd.read_csv(file_path, encoding='utf-8', errors='replace')
    elif ext in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    elif ext == '.json':
        df = pd.read_json(file_path)
    else:
        raise ValueError(f"不支持的文件格式: {ext}")

    if df.empty:
        raise ValueError("文件中没有数据")

    # 自动识别平台
    if platform is None:
        platform = detect_platform(path.name, df)

    # 标准化列名
    df = normalize_columns(df, platform)

    # 确保必要字段存在
    if 'content' not in df.columns:
        raise ValueError(
            f"未找到评价内容列。请确保CSV中包含'评价内容'/'评论'等列。\n"
            f"当前列名: {list(df.columns)}"
        )

    # 数据类型标准化
    if 'rating' in df.columns:
        df['rating'] = df['rating'].apply(parse_rating)
    else:
        df['rating'] = None

    if 'review_time' in df.columns:
        df['review_time'] = df['review_time'].apply(parse_time)
    else:
        df['review_time'] = datetime.now()

    if 'delivery_time' in df.columns:
        df['delivery_time'] = pd.to_numeric(df['delivery_time'], errors='coerce')

    # 添加元数据
    df['platform'] = platform
    df['import_time'] = datetime.now()

    # 清理空内容
    df = df[df['content'].notna() & (df['content'].astype(str).str.strip() != '')]

    return df


def load_history(data_dir: str) -> pd.DataFrame:
    """加载历史评价数据"""
    history_path = Path(data_dir) / "history.csv"
    if history_path.exists():
        df = pd.read_csv(history_path)
        if 'review_time' in df.columns:
            df['review_time'] = pd.to_datetime(df['review_time'], errors='coerce')
        return df
    return pd.DataFrame()


def merge_history(new_df: pd.DataFrame, history_df: pd.DataFrame, data_dir: str):
    """合并新数据到历史记录（去重）"""
    if history_df.empty:
        combined = new_df
    else:
        # 基于内容和时间去重
        if 'content' in new_df.columns and 'review_time' in new_df.columns:
            combined = pd.concat([history_df, new_df], ignore_index=True)
            combined = combined.drop_duplicates(
                subset=['content', 'review_time'], keep='last'
            )
        else:
            combined = pd.concat([history_df, new_df], ignore_index=True)

    # 保存
    os.makedirs(data_dir, exist_ok=True)
    history_path = Path(data_dir) / "history.csv"
    combined.to_csv(history_path, index=False, encoding='utf-8-sig')
    return combined


class ReviewDataLoader:
    """评价数据加载器主类"""

    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir or os.path.expanduser("~/.food_review_monitor/data")
        os.makedirs(self.data_dir, exist_ok=True)

    def load(self, file_path: str, platform: str = None, merge: bool = True):
        """加载并处理评价数据"""
        df = load_reviews(file_path, platform)

        print(f"✅ 加载完成: {len(df)} 条评价")
        print(f"   平台: {df['platform'].iloc[0] if 'platform' in df.columns else 'unknown'}")
        if 'rating' in df.columns:
            valid_ratings = df['rating'].dropna()
            if len(valid_ratings) > 0:
                print(f"   评分范围: {valid_ratings.min():.1f} - {valid_ratings.max():.1f}")
                print(f"   平均评分: {valid_ratings.mean():.2f}")
        if 'review_time' in df.columns:
            times = df['review_time'].dropna()
            if len(times) > 0:
                print(f"   时间范围: {times.min()} ~ {times.max()}")

        if merge:
            history = load_history(self.data_dir)
            df = merge_history(df, history, self.data_dir)
            print(f"   历史总计: {len(df)} 条评价")

        return df
