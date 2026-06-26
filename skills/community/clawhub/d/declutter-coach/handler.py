"""Declutter Coach - 整理coach"""
import json
import re

CATEGORIES = {
    "衣物": ["当季不穿的", "超过1年没穿的", "变形/褪色的"],
    "书籍": ["不会再翻的", "已看过且无收藏价值的", "重复的版本"],
    "电子产品": ["3年以上未使用的", "已损坏无法修复的", "配件不全的"],
    "文件": ["过期的账单/合同", "无效的会员卡", "无保存价值的宣传单"],
    "纪念品": ["失去情感连接的", "破损无法修复的", "重复的"],
}

def parse_declutter_input(text: str) -> dict:
    area = None
    for cat in CATEGORIES:
        if cat in text: area = cat
    if not area:
        for kw in ["衣柜", "衣橱", "衣服"]: area = "衣物"; break
        for kw in ["书架", "书", "书籍"]: area = "书籍"; break
        for kw in ["抽屉", "桌面", "房间", "家"]: area = "杂物"; break
    area = area or "杂物"
    return {"area": area, "urgency": "high" if "乱" in text or "忍" in text else "medium"}

def generate_declutter_plan(area: str) -> dict:
    plan = {
        "area": area,
        "steps": [
            "拍一张整理前的照片（对比用）",
            "把所有物品拿出来堆在一起（可视化物量）",
            "分成4堆：保留 / 送人 / 卖掉 / 丢弃",
            "保留区按使用者+使用频率重新定位",
            "拍一张整理后的照片"
        ],
        "category_rules": CATEGORIES.get(area, ["功能性判断：过去1年用过？未来6个月会用？"]),
        "time_estimate": {"min": 30, "max": 120, "unit": "分钟"},
        "motivation": "日本整理教主近藤麻理惠：留下让你心动的东西，其余感谢后放手。"
    }
    return plan

def handle(text: str) -> dict:
    parsed = parse_declutter_input(text)
    plan = generate_declutter_plan(parsed["area"])
    return {
        "targetArea": parsed["area"],
        "urgency": parsed["urgency"],
        "declutterPlan": plan,
        "tips": ["先完成一个小角落建立信心", "整理的顺序：先从最简单的地方开始", "卖出闲置可以补贴整理的动力"],
        "donationChannels": ["闲鱼（卖）", "转转", "飞蚂蚁（捐）", "朋友圈送熟人"]
    }

if __name__ == "__main__":
    for tc in ["衣柜太乱了不知道怎么整理", "书太多要断舍离"]:
        r = handle(tc)
        print(f"Input: {tc}\n  -> 目标区域: {r['targetArea']}\n  -> 步骤: {r['declutterPlan']['steps'][0]}\n  -> 预计: {r['declutterPlan']['time_estimate']}\n")
