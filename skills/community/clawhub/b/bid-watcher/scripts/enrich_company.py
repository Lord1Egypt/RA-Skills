#!/usr/bin/env python3
"""
补充公司背景信息
根据招标方名称，补充公司背景、历史采购记录等字段
"""

import json
import glob
import os
from datetime import datetime

# 基于脚本自身位置确定 data 目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "data")

# 已知公司背景库（可扩展为数据库或 API 调用）
# 格式：公司名关键词 → {背景描述, 是否已知有采购历史, 历史供应商}
COMPANY_DB = {
    "宁德时代": {
        "背景": "全球领先的动力电池制造商，市值超万亿，客户覆盖国内外主流车企",
        "有采购历史": True,
        "历史供应商": "先导智能、海目星、赢合科技、联赢激光",
        "规模": "全球最大锂电池制造商"
    },
    "比亚迪": {
        "背景": "中国新能源汽车龙头企业，业务涵盖汽车、轨道交通、新能源和电子",
        "有采购历史": True,
        "历史供应商": "先导智能、海目星",
        "规模": "世界500强"
    },
    "亿纬锂能": {
        "背景": "锂电池行业领先企业，专注于消费电池和动力电池",
        "有采购历史": True,
        "历史供应商": "赢合科技、先导智能",
        "规模": "行业头部企业"
    },
    "中创新航": {
        "背景": "中创新航是从事新能源汽车动力电池、储能系统的头部企业",
        "有采购历史": True,
        "历史供应商": "海目星、先导智能",
        "规模": "国内动力电池前三"
    },
    "蜂巢能源": {
        "背景": "长城汽车旗下动力电池公司，近年快速扩张",
        "有采购历史": True,
        "历史供应商": "先导智能、赢合科技",
        "规模": "成长型头部企业"
    },
    "瑞浦兰钧": {
        "背景": "青山集团旗下锂电池企业，专注动力及储能电池",
        "有采购历史": True,
        "历史供应商": "海目星",
        "规模": "快速成长型企业"
    },
    "国轩高科": {
        "背景": "中国动力电池头部企业之一，涵盖动力锂电池和储能",
        "有采购历史": True,
        "历史供应商": "先导智能、赢合科技、联赢激光",
        "规模": "行业第一梯队"
    },
    "欣旺达": {
        "背景": "消费电池龙头，近年来动力电池业务快速增长",
        "有采购历史": True,
        "历史供应商": "海目星、赢合科技",
        "规模": "消费电池龙头，动力电池快速扩张"
    },
    "孚能科技": {
        "背景": "专注于新能源汽车动力电池软包技术路线",
        "有采购历史": True,
        "历史供应商": "先导智能",
        "规模": "技术特色型企业"
    },
    "LG新能源": {
        "背景": "韩国电池巨头，在中国及全球均有大型工厂布局",
        "有采购历史": True,
        "历史供应商": "先导智能（部分产线）",
        "规模": "全球前五"
    },
    "松下": {
        "背景": "日本电池巨头，与特斯拉等国际客户合作紧密",
        "有采购历史": False,
        "历史供应商": "进口设备为主",
        "规模": "全球知名"
    },
}

# 竞争公司自身名称（用于识别招标方是否是他们）
COMPETITORS = {
    "先导智能": "无锡先导智能装备股份有限公司",
    "海目星": "海目星激光科技集团股份有限公司",
    "赢合科技": "深圳市赢合科技股份有限公司",
    "联赢激光": "深圳市联赢激光股份有限公司"
}

# 锂电池/储能相关行业关键词（用于判断是否相关）
RELEVANT_KEYWORDS = ["锂电池", "储能", "锂电", "动力电池", "电池生产", "电芯", "pack", "模组"]


def lookup_company(company_name):
    """查询公司背景库"""
    if not company_name or company_name == "未知" or company_name == "待抓取":
        return None

    # 精确匹配
    for kw, info in COMPANY_DB.items():
        if kw in company_name:
            return info

    # 模糊匹配（包含任一关键词即匹配）
    for kw, info in COMPANY_DB.items():
        if any(c in company_name for c in [kw, kw[:2], kw[:4]]):
            return info

    return None


def is_relevant_bid(bid):
    """判断招标是否与目标行业相关"""
    title = bid.get('title', '') or ''
    keyword = bid.get('keyword', '') or ''
    text = title + keyword

    # 排除竞争对手自身的招标公告
    for short_name in COMPETITORS:
        full_name = COMPETITORS[short_name]
        if short_name in bid.get('company', '') or full_name in bid.get('company', ''):
            return False

    return any(kw.lower() in text.lower() for kw in RELEVANT_KEYWORDS)


def enrich_bids(parsed_file):
    """补充公司背景信息"""
    with open(parsed_file, 'r', encoding='utf-8') as f:
        bids = json.load(f)

    enriched = []
    stats = {"total": 0, "enriched": 0, "relevant": 0, "competitor_bid": 0}

    for bid in bids:
        stats["total"] += 1
        company = bid.get('company', '')

        # 查询公司背景
        info = lookup_company(company)

        if info:
            bid["公司背景"] = info["背景"]
            bid["是否有采购历史"] = "是" if info.get("有采购历史") else "未知"
            bid["历史供应商"] = info.get("历史供应商", "未知")
            bid["规模"] = info.get("规模", "未知")
            stats["enriched"] += 1
        else:
            bid["公司背景"] = "未知（建议人工核实）"
            bid["是否有采购历史"] = "未知"
            bid["历史供应商"] = "未知"
            bid["规模"] = "未知"

        # 判断是否相关
        if is_relevant_bid(bid):
            bid["相关性"] = "高"
            bid["优先级"] = score_priority(bid)
            stats["relevant"] += 1
        else:
            bid["相关性"] = "低"
            bid["优先级"] = "C"
            stats["competitor_bid"] += 1

        enriched.append(bid)

    return enriched, stats


def score_priority(bid):
    """根据多个维度计算优先级"""
    score = 0
    amount = bid.get('amount', '未知')
    company = bid.get('company', '')
    title = bid.get('title', '')

    # 有预算信息 +1分
    if amount and amount != '未知' and amount != '待抓取':
        score += 1
        # 大预算 +1分（超过1000万）
        if any(u in amount for u in ['万', '千万', '亿']):
            try:
                num = float(''.join(c for c in amount if c.isdigit() or c == '.'))
                if num >= 1000:
                    score += 1
            except:
                pass

    # 公司在背景库中 +1分
    if lookup_company(company):
        score += 1

    # 有投标时间 +1分
    if bid.get('bid_time') and bid.get('bid_time') != '未知' and bid.get('bid_time') != '待抓取':
        score += 1

    # 标题含"储能"或"锂电" +1分
    if any(kw in title for kw in ['储能', '锂电', '动力电池']):
        score += 1

    # 竞争公司直接招标 -1分
    for short_name in COMPETITORS:
        if short_name in company:
            score -= 2

    if score >= 4:
        return "S"
    elif score >= 3:
        return "A"
    elif score >= 2:
        return "B"
    else:
        return "C"


def save_enriched(bids, original_file):
    """保存补充后的数据"""
    os.makedirs(DATA_DIR, exist_ok=True)
    today = datetime.now().strftime('%Y%m%d')
    output = original_file.replace('.json', f'_enriched_{today}.json')
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(bids, f, ensure_ascii=False, indent=2)
    return output


if __name__ == "__main__":
    files = glob.glob(os.path.join(DATA_DIR, "bids_parsed_*.json"))
    if not files:
        print("[错误] 没有找到解析后的数据文件，请先运行 parse_bids.py")
        exit(1)

    latest = max(files)
    print(f"补充公司背景: {latest}\n")

    enriched, stats = enrich_bids(latest)

    output_file = save_enriched(enriched, latest)

    print(f"\n{'='*50}")
    print(f"补充完成")
    print(f"  总线索: {stats['total']}")
    print(f"  匹配到公司背景: {stats['enriched']}")
    print(f"  高相关招标: {stats['relevant']}")
    print(f"  竞争公司自身招标（已过滤）: {stats['competitor_bid']}")
    print(f"\n优先级分布:")
    priority_counts = {}
    for b in enriched:
        p = b.get('优先级', 'C')
        priority_counts[p] = priority_counts.get(p, 0) + 1
    for p in ['S', 'A', 'B', 'C']:
        if p in priority_counts:
            print(f"  [{p}] {priority_counts[p]} 条")
    print(f"\n输出: {output_file}")
