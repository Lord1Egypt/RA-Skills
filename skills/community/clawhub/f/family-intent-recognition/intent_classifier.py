#!/usr/bin/env python3
"""
家庭消费意图识别系统 V3.0
按照新格式输出：has_intent, intent_category, intent_stage, intent_strength, keywords, reason
"""

import re
from typing import Optional

# 商品类别映射
CATEGORY_KEYWORDS = {
    "家电": ["电视", "冰箱", "洗衣机", "空调", "风扇", "电饭煲", "微波炉", "油烟机", "热水器", "净化器", "扫地机", "吸尘器"],
    "数码产品": ["手机", "电脑", "平板", "耳机", "音箱", "相机", "摄像机", "无人机", "智能手表", "手环"],
    "电脑外设": ["键盘", "鼠标", "显示器", "硬盘", "内存", "显卡", "U盘", "移动硬盘", "鼠标垫", "电脑包"],
    "家具": ["沙发", "床", "衣柜", "书桌", "餐桌", "椅子", "鞋柜", "电视柜", "书架", "床垫"],
    "食品饮料": ["零食", "饮料", "水果", "牛奶", "酸奶", "茶叶", "咖啡", "保健品", "奶粉", "辅食", "好吃的", "食品"],
    "服装鞋帽": ["衣服", "裤子", "裙子", "外套", "羽绒服", "T恤", "运动鞋", "皮鞋", "帽子", "围巾", "包包", "化妆品", "护肤品", "鞋", "鞋子", "双鞋", "双鞋子"],
    "日用品": ["洗发水", "沐浴露", "牙膏", "牙刷", "毛巾", "纸巾", "洗衣液", "洗洁精", "垃圾袋", "保鲜膜"],
    "汽车": ["汽车", "电动车", "自行车", "摩托车", "汽车用品", "车载充电器", "行车记录仪", "车险"],
    "母婴用品": ["奶粉", "尿不湿", "婴儿车", "婴儿床", "玩具", "童装", "孕妇装", "奶瓶", "婴儿用品", "礼物"],
    "娱乐产品": ["电影", "演唱会", "旅游", "游戏", "健身", "图书", "乐器", "摄影"],
    "教育培训": ["培训", "课程", "学费", "辅导班", "英语班", "钢琴课", "游泳课", "驾校"],
    "医疗保健": ["药品", "保健品", "体检", "保险", "眼镜", "牙科", "医院", "安眠药", "药"],
    "通讯费": ["话费", "流量", "网费", "宽带"],
    "水电燃气": ["电费", "水费", "燃气费", "物业费", "房租"],
    "餐饮": ["火锅", "烧烤", "自助", "日料", "西餐", "快餐", "外卖", "餐厅", "吃饭", "下馆子", "顿饭"],
}

# 意图阶段关键词
STAGE_KEYWORDS = {
    "awareness": [
        # 兴趣阶段
        "不错", "挺好", "好看", "漂亮", "想有一个", "看中", "相中",
        "有个", "发现", "看到", "看见", "提到", "说起", "说到",
        "听说", "据说", "好像有", "好像要", "可能会", "坏了"
    ],
    "consideration": [
        # 考虑阶段
        "多少钱", "价格", "贵不贵", "便宜吗", "性价比", "怎么样", "好不好", 
        "哪个好", "哪个牌子", "什么牌子", "推荐", "建议", "评价", "口碑",
        "对比", "比较", "有什么区别", "有啥区别", "靠谱吗", "可靠吗",
        "有用吗", "值得买吗", "划算吗", "便宜还是贵"
    ],
    "purchase": [
        # 购买阶段
        "买了", "下单", "要买", "准备买", "打算买", "计划买", "需要买",
        "去买", "去买的", "已买", "刚买", "今天买", "昨天买", "买过了",
        "充", "缴费", "交钱", "付钱", "付了", "花了", "转账",
        "该买了", "该缴费了", "要交了", "得买", "去买",
        "想买", "想个", "要一个", "换一个", "换一个新的", "想买一个",
        "买点", "想买点", "买些", "吃点", "顿饭", "去吃",
        "送给", "送人", "没什么", "没啥", "买点"
    ]
}

# 意图强度判断
STRENGTH_PATTERNS = {
    "high": [
        "买了", "下单", "要买", "打算买", "准备买", "必须买", "一定要",
        "已买", "刚买", "今天买", "马上去", "这就去",
        "充", "缴费", "交钱", "付钱", "付了", "花了",
        "想买", "想个", "要一个", "换一个", "换一个新的", "想买一个"
    ],
    "medium": [
        "想要", "计划买", "考虑买",
        "多少钱", "价格", "怎么样", "好不好", "哪个好", "推荐"
    ],
    "low": [
        "不错", "挺好", "好看", "漂亮", "有个",
        "听说", "据说", "看到", "看见", "提到", "说起",
        "坏了", "破了", "旧了"
    ]
}


def extract_keywords(text: str) -> list:
    """提取触发关键词"""
    keywords = []
    text_lower = text.lower()
    
    # 检查各阶段关键词
    for stage, kws in STAGE_KEYWORDS.items():
        for kw in kws:
            if kw in text:
                keywords.append(kw)
                break
    
    # 检查商品类别关键词
    for category, kws in CATEGORY_KEYWORDS.items():
        for kw in kws:
            if kw in text:
                keywords.append(kw)
                break
    
    # 检查购买相关词
    purchase_words = ["买", "购买", "购物", "消费", "花", "充", "付", "缴费"]
    for pw in purchase_words:
        if pw in text and pw not in keywords:
            keywords.append(pw)
    
    # 去重并返回
    return list(set(keywords))


def extract_category(text: str) -> str:
    """提取商品类别"""
    # 模糊词汇（单独匹配时不返回具体类别）
    vague_keywords = ["礼物", "好吃的", "食品"]
    
    # 优先检查水电燃气（特殊处理）
    if any(kw in text for kw in ["燃气", "天然气", "煤气"]):
        return "水电燃气"
    if "电费" in text:
        return "水电燃气"
    if "水费" in text:
        return "水电燃气"
    
    # 检查其他类别
    matched_categories = []
    for category, kws in CATEGORY_KEYWORDS.items():
        for kw in kws:
            if kw in text:
                # 如果是模糊词汇，记录但不直接返回
                if kw in vague_keywords:
                    matched_categories.append(category)
                else:
                    return category
    
    # 如果只匹配到模糊词汇，返回unknown
    if matched_categories and len(matched_categories) > 0:
        return "unknown"
    
    return "unknown"


def determine_intent_stage(text: str, keywords: list) -> str:
    """判断意图阶段"""
    text_lower = text.lower()
    
    # 优先检查purchase阶段（最强信号）
    for kw in STAGE_KEYWORDS["purchase"]:
        if kw in text:
            return "purchase"
    
    # 然后检查consideration阶段
    for kw in STAGE_KEYWORDS["consideration"]:
        if kw in text:
            return "consideration"
    
    # 最后检查awareness阶段
    for kw in STAGE_KEYWORDS["awareness"]:
        if kw in text:
            return "awareness"
    
    # 默认awareness
    return "awareness"


def determine_intent_strength(text: str, stage: str) -> str:
    """判断意图强度"""
    # 先检查high强度关键词
    for kw in STRENGTH_PATTERNS["high"]:
        if kw in text:
            return "high"
    
    # 然后检查medium
    for kw in STRENGTH_PATTERNS["medium"]:
        if kw in text:
            return "medium"
    
    # 最后检查low
    for kw in STRENGTH_PATTERNS["low"]:
        if kw in text:
            return "low"
    
    # 根据阶段推断
    if stage == "purchase":
        return "high"
    elif stage == "consideration":
        return "medium"
    else:
        return "low"


def generate_reason(text: str, stage: str, strength: str, category: str, keywords: list, has_intent: bool) -> str:
    """生成判断理由"""
    # 无消费意图
    if not has_intent or (stage == "awareness" and len(keywords) == 0):
        return "对话中未出现任何消费相关表达"
    
    # 有消费意图
    if stage == "purchase" and strength == "high":
        return "用户明确表达购买意向或已完成购买"
    elif stage == "consideration":
        return "用户在询问价格、评价或进行比较"
    else:
        return "用户只是提到或对某商品表达兴趣"


def classify(text: str) -> dict:
    """
    家庭消费意图识别主函数
    
    Args:
        text: 输入文本
        
    Returns:
        dict: {
            "has_intent": true/false,
            "intent_category": "商品类别",
            "intent_stage": "awareness|consideration|purchase",
            "intent_strength": "low|medium|high",
            "keywords": ["触发关键词"],
            "reason": "判断原因"
        }
    """
    # 提取关键词
    keywords = extract_keywords(text)
    
    # 提取商品类别
    category = extract_category(text)
    
    # 判断意图阶段
    stage = determine_intent_stage(text, keywords)
    
    # 判断意图强度
    strength = determine_intent_strength(text, stage)
    
    # 判断是否存在消费意图
    # 如果有关键词且类别不是unknown，或者有purchase阶段关键词
    has_intent = (len(keywords) > 0 and category != "unknown") or stage == "purchase"
    
    # 特殊情况：只提到"吃火锅"类的餐饮
    if category == "餐饮" and stage == "awareness" and strength == "low":
        has_intent = True  # 餐饮消费意图
    
    # 生成理由
    reason = generate_reason(text, stage, strength, category, keywords, has_intent)
    
    return {
        "has_intent": has_intent,
        "intent_category": category,
        "intent_stage": stage,
        "intent_strength": strength,
        "keywords": keywords[:5],  # 最多5个关键词
        "reason": reason
    }


if __name__ == "__main__":
    # 测试用例
    test_cases = [
        # 火锅类
        "明天咱们去吃火锅吧",
        "打算吃火锅",
        "去吃火锅",
        "火锅多少钱",
        "哪家火锅好吃",
        "买了火锅食材",
        
        # 燃气类
        "咱家燃气费还剩多少钱",
        "打算购买燃气",
        "燃气费该交了",
        
        # 购物类
        "想买一台电脑",
        "这个电脑怎么样",
        "买了个手机",
        "华为手机好不好",
        "今天花了300买菜",
        
        # 无消费意图
        "今天天气不错",
        "孩子成绩出来了",
    ]
    
    print("=" * 80)
    print("家庭消费意图识别系统 V3.0 测试")
    print("=" * 80)
    
    for text in test_cases:
        result = classify(text)
        print(f"\n输入: {text}")
        print(f"输出: {result}")
