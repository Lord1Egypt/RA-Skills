#!/usr/bin/env python3
"""
广告投手 - 数据管理模块
支持多平台（腾讯广告/巨量引擎/百度推广/Meta/Google）数据导入、清洗、标准化
"""

import json
import csv
import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# 列名映射表：将各平台/各种命名的列统一到标准字段
COLUMN_MAP = {
    # 日期
    "date": ["date", "日期", "时间", "day", "statis_date", "report_date", "dt"],
    # 计划/广告组
    "campaign": ["campaign", "campaign_name", "计划", "计划名称", "推广计划", "广告计划",
                 "adgroup", "adgroup_name", "广告组", "广告组名称", "ad_group"],
    # 创意/素材
    "creative": ["creative", "creative_name", "创意", "素材", "素材名称", "creative_title",
                 "ad_name", "广告名称", "ad"],
    # 曝光量
    "impressions": ["impressions", "impression", "曝光", "展现", "曝光量", "展现量",
                    "view", "views", "exposure"],
    # 点击量
    "clicks": ["clicks", "click", "点击", "点击量", "点击数"],
    # 消耗
    "cost": ["cost", "spend", "花费", "消耗", "费用", "金额", "总花费", "real_cost",
             "total_cost", "ad_cost"],
    # 转化量
    "conversions": ["conversions", "conversion", "转化", "转化量", "转化数",
                    "convert", "purchase", "orders", "下单", "订单"],
    # GMV/成交额
    "revenue": ["revenue", "gmv", "成交额", "成交金额", "gmv金额", "交易额",
                "revenue_amount", "total_revenue", "sales"],
    # CTR - 可选
    "ctr": ["ctr", "点击率", "ctr(%)"],
    # CVR - 可选
    "cvr": ["cvr", "转化率", "cvr(%)"],
    # CPC
    "cpc": ["cpc", "cpc(元)", "平均点击价格", "avg_cpc"],
    # CPM
    "cpm": ["cpm", "cpm(元)", "千次曝光成本", "avg_cpm"],
}

# 平台识别特征
PLATFORM_SIGNATURES = {
    "tencent_ads": {
        "patterns": ["广告系列", "推广计划名称", "adgroup_id", "campaign_id", "微信", "QQ"],
        "name": "腾讯广告"
    },
    "ocean_engine": {
        "patterns": ["广告组id", "计划id", "抖音", "穿山甲", "巨量", "oceanengine"],
        "name": "巨量引擎"
    },
    "baidu_ads": {
        "patterns": ["百度", "关键词", "搜索词", "单元id", "baidu"],
        "name": "百度推广"
    },
    "meta_ads": {
        "patterns": ["facebook", "instagram", "audience", "meta", "fb_"],
        "name": "Meta Ads"
    },
    "google_ads": {
        "patterns": ["google", "youtube", "gdn", "search_campaign", "display"],
        "name": "Google Ads"
    },
}


def detect_platform(headers: list) -> str:
    """根据列名识别数据来源平台"""
    header_text = " ".join(headers).lower()
    scores = {}
    for platform, info in PLATFORM_SIGNATURES.items():
        score = sum(1 for p in info["patterns"] if p.lower() in header_text)
        if score > 0:
            scores[platform] = score
    if scores:
        return max(scores, key=scores.get)
    return "unknown"


def normalize_headers(headers: list) -> dict:
    """将原始列名映射为标准列名，返回 {原始列名: 标准列名}"""
    mapping = {}
    headers_lower = [h.lower().strip() for h in headers]

    for i, raw_h in enumerate(headers):
        h = raw_h.lower().strip()
        matched = False
        for standard, aliases in COLUMN_MAP.items():
            for alias in aliases:
                if alias.lower() == h or alias.lower() in h:
                    mapping[headers[i]] = standard
                    matched = True
                    break
            if matched:
                break
        if not matched:
            mapping[headers[i]] = h  # 保留原始名
    return mapping


def parse_value(val):
    """智能解析值：处理百分号、千分位逗号、中文字符"""
    if val is None or val == "" or val == "-":
        return None
    s = str(val).strip()
    s = s.replace(",", "").replace("，", "")
    s = s.replace("¥", "").replace("$", "").replace("￥", "")
    s = s.replace("元", "").replace("次", "").replace("单", "")
    if s.endswith("%"):
        try:
            return float(s[:-1]) / 100
        except ValueError:
            return None
    try:
        return float(s)
    except ValueError:
        return None


def load_file(file_path: str) -> tuple:
    """
    加载数据文件，返回 (records, platform, meta)
    records: list[dict] 标准化后的数据
    platform: str 平台标识
    meta: dict 元信息
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    suffix = file_path.suffix.lower()

    if suffix == ".json":
        return load_json(file_path)
    elif suffix == ".csv":
        return load_csv(file_path)
    elif suffix in (".xlsx", ".xls"):
        return load_excel(file_path)
    else:
        raise ValueError(f"不支持的文件格式: {suffix}")


def load_csv(file_path: Path) -> tuple:
    """加载CSV文件"""
    records = []
    encodings = ["utf-8-sig", "utf-8", "gbk", "gb2312", "gb18030"]

    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                if headers is None:
                    continue
                # 跳过空行
                for row in reader:
                    if any(v and v.strip() for v in row.values()):
                        records.append(dict(row))
                if records:
                    break
        except (UnicodeDecodeError, UnicodeError):
            continue

    if not records:
        # 最后尝试
        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            for row in reader:
                records.append(dict(row))

    platform = detect_platform(list(headers or []))
    normalized = normalize_data(records)
    return normalized, platform, {"source": str(file_path), "format": "csv", "raw_count": len(records)}


def load_excel(file_path: Path) -> tuple:
    """加载Excel文件"""
    try:
        import openpyxl
    except ImportError:
        raise ImportError("需要安装 openpyxl: pip install openpyxl")

    wb = openpyxl.load_workbook(file_path, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        raise ValueError("Excel文件为空")

    headers = [str(h) if h else "" for h in rows[0]]
    records = []
    for row in rows[1:]:
        record = {}
        for i, h in enumerate(headers):
            if i < len(row):
                record[h] = row[i]
        if any(v is not None and str(v).strip() for v in record.values()):
            records.append(record)

    platform = detect_platform(headers)
    normalized = normalize_data(records)
    return normalized, platform, {"source": str(file_path), "format": "excel", "raw_count": len(records)}


def load_json(file_path: Path) -> tuple:
    """加载JSON文件"""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        records = data
    elif isinstance(data, dict):
        # 尝试从常见结构中提取
        for key in ["data", "list", "records", "rows", "results"]:
            if key in data and isinstance(data[key], list):
                records = data[key]
                break
        else:
            records = [data]
    else:
        raise ValueError("无法解析JSON数据，需要数组或对象格式")

    # 尝试检测平台
    platform = "unknown"
    if records:
        sample = records[0]
        if isinstance(sample, dict):
            headers = list(sample.keys())
            platform = detect_platform(headers)

    normalized = normalize_data(records)
    return normalized, platform, {"source": str(file_path), "format": "json", "raw_count": len(records)}


def normalize_data(records: list) -> list:
    """将原始数据标准化为统一定段"""
    if not records:
        return []

    # 构建列映射
    headers = list(records[0].keys())
    col_mapping = normalize_headers(headers)

    normalized = []
    for record in records:
        norm = {}
        for raw_key, std_key in col_mapping.items():
            val = record.get(raw_key)
            parsed = parse_value(val)
            if parsed is not None:
                norm[std_key] = parsed
            elif std_key in ("campaign", "creative"):
                norm[std_key] = str(val) if val else "未命名"

        # 日期标准化
        if "date" in norm and isinstance(norm["date"], str):
            norm["date"] = parse_date(norm["date"])

        # 补充缺失的计算指标
        enrich_record(norm)
        normalized.append(norm)

    return normalized


def parse_date(date_str: str) -> str:
    """标准化日期为 YYYY-MM-DD"""
    date_str = str(date_str).strip()
    patterns = [
        (r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", "{}-{:02d}-{:02d}"),
        (r"(\d{4})(\d{2})(\d{2})", "{}-{}-{}"),
        (r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})", "{2}-{:02d}-{:02d}"),
    ]
    for pattern, fmt in patterns:
        m = re.match(pattern, date_str)
        if m:
            groups = [int(g) for g in m.groups()]
            if fmt == "{2}-{:02d}-{:02d}":
                return f"{groups[2]}-{groups[0]:02d}-{groups[1]:02d}"
            return fmt.format(*groups)
    return date_str


def enrich_record(record: dict):
    """补充计算指标"""
    impr = record.get("impressions", 0) or 0
    clicks = record.get("clicks", 0) or 0
    cost = record.get("cost", 0) or 0
    conv = record.get("conversions", 0) or 0
    revenue = record.get("revenue", 0) or 0

    if "ctr" not in record and impr > 0:
        record["ctr"] = clicks / impr
    if "cvr" not in record and clicks > 0:
        record["cvr"] = conv / clicks
    if "cpc" not in record and clicks > 0:
        record["cpc"] = cost / clicks
    if "cpm" not in record and impr > 0:
        record["cpm"] = cost / impr * 1000
    if "cpa" not in record and conv > 0:
        record["cpa"] = cost / conv
    if "roas" not in record and cost > 0:
        record["roas"] = revenue / cost
    if "roi" not in record and cost > 0 and revenue > 0:
        record["roi"] = (revenue - cost) / cost


def get_summary(records: list) -> dict:
    """生成数据概览"""
    if not records:
        return {"error": "无数据"}

    total_impressions = sum(r.get("impressions", 0) or 0 for r in records)
    total_clicks = sum(r.get("clicks", 0) or 0 for r in records)
    total_cost = sum(r.get("cost", 0) or 0 for r in records)
    total_conversions = sum(r.get("conversions", 0) or 0 for r in records)
    total_revenue = sum(r.get("revenue", 0) or 0 for r in records)

    campaigns = set()
    for r in records:
        if "campaign" in r:
            campaigns.add(r["campaign"])

    dates = set()
    for r in records:
        if "date" in r:
            dates.add(str(r["date"]))

    return {
        "record_count": len(records),
        "date_range": f"{min(dates)} ~ {max(dates)}" if dates else "未知",
        "dates": sorted(dates) if dates else [],
        "campaign_count": len(campaigns),
        "campaigns": sorted(campaigns) if campaigns else [],
        "total_impressions": total_impressions,
        "total_clicks": total_clicks,
        "total_cost": round(total_cost, 2),
        "total_conversions": total_conversions,
        "total_revenue": round(total_revenue, 2),
        "avg_ctr": round(total_clicks / total_impressions * 100, 2) if total_impressions > 0 else 0,
        "avg_cvr": round(total_conversions / total_clicks * 100, 2) if total_clicks > 0 else 0,
        "avg_cpc": round(total_cost / total_clicks, 2) if total_clicks > 0 else 0,
        "avg_cpm": round(total_cost / total_impressions * 1000, 2) if total_impressions > 0 else 0,
        "avg_cpa": round(total_cost / total_conversions, 2) if total_conversions > 0 else 0,
        "roas": round(total_revenue / total_cost, 2) if total_cost > 0 else 0,
        "roi": round((total_revenue - total_cost) / total_cost * 100, 1) if total_cost > 0 else 0,
    }


def save_normalized(records: list, output_path: str):
    """保存标准化数据"""
    output_path = Path(output_path)
    suffix = output_path.suffix.lower()

    if suffix == ".json":
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2, default=str)
    elif suffix == ".csv":
        if not records:
            return
        keys = records[0].keys()
        with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(records)
    else:
        raise ValueError(f"不支持输出格式: {suffix}")

    print(f"数据已保存: {output_path} ({len(records)} 条)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python data_manager.py <数据文件路径> [--output 输出路径]")
        print("支持: CSV, Excel(.xlsx), JSON")
        sys.exit(1)

    file_path = sys.argv[1]
    output_path = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]

    try:
        records, platform, meta = load_file(file_path)
        platform_name = PLATFORM_SIGNATURES.get(platform, {}).get("name", "未知平台")
        print(f"平台: {platform_name}")
        print(f"格式: {meta['format']}")
        print(f"原始记录: {meta['raw_count']} 条")
        print(f"标准化: {len(records)} 条")

        summary = get_summary(records)
        print(f"\n数据概览:")
        print(f"  日期范围: {summary['date_range']}")
        print(f"  计划数: {summary['campaign_count']}")
        print(f"  总消耗: ¥{summary['total_cost']:,.2f}")
        print(f"  总曝光: {summary['total_impressions']:,}")
        print(f"  总点击: {summary['total_clicks']:,}")
        print(f"  总转化: {summary['total_conversions']:,}")
        print(f"  总收入: ¥{summary['total_revenue']:,.2f}")
        print(f"  平均CTR: {summary['avg_ctr']}%")
        print(f"  平均CVR: {summary['avg_cvr']}%")
        print(f"  平均CPA: ¥{summary['avg_cpa']:,.2f}")
        print(f"  ROAS: {summary['roas']}")
        print(f"  ROI: {summary['roi']}%")

        if output_path:
            save_normalized(records, output_path)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)
