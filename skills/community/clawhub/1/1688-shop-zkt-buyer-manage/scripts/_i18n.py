"""字段中英对照 & 宽松数据解析

集中管理所有 cmd.py 渲染时遇到的英文字段 → 中文译名映射。
同时提供 parse_loose：先 json.loads，失败再 ast.literal_eval（兼容 Python repr 字典）。

对应 SKILL.md「字段中英对照知识库」章节，二者保持同步。
"""

import ast
import json
import re


# ============================================================
# 字段中英对照知识库
# ============================================================
FIELD_NAME_ALIAS = {
    # —— 用户画像 / 客户档案
    "nickName": "买家昵称",
    "buyerId": "客户 ID",
    "buyerIdList": "客户 ID 列表",
    "buyerType": "客户类型",
    "lLevel": "客户等级",
    "buyerConstitution": "客户体质",
    "followUpState": "跟进阶段",
    "mainCate": "主采类目",
    "payCnt180d": "近半年采购次数",
    "payAmt180d": "近半年同类目采购额",
    "buyerPurchaseHabits": "客户采购习惯",
    "otherShopInqInfor": "跨店询盘信息",
    "purchaseDecisions": "采购决策依据",
    "recentChatNeedsAna": "近期沟通需求分析",
    "lostAnalysis": "流失风险分析",
    "awakenReason": "商机唤醒理由",
    "wakenAdvice": "唤醒话术建议",
    "retentionAdvice": "挽留话术建议",
    "followUpScript": "跟进话术建议",

    # —— 客户采购习惯（buyerPurchaseHabits 子字段）
    "pay_distribution": "采购分布特征",
    "supply_chain_stability": "供应链选择稳定性",
    "supply_cnt": "供应链上游数目",
    "supply_change_cycle": "供应链新增状况",
    "supply_change_cnt": "供应链新增数量",
    "inq_shop_cnt_30d": "近90天询盘店铺",
    "inq_cates_30d": "近90天询盘品类",
    "inq_items_30d": "近90天询盘商品",
    "search_keyword_30d": "近90天搜索词",
    "inq_shop_cnt_90d": "近90天询盘店铺",
    "inq_cates_90d": "近90天询盘品类",
    "inq_items_90d": "近90天询盘商品",
    "search_keyword_90d": "近90天搜索词",

    # —— 近期沟通需求（recentChatNeedsAna 子字段）
    "demands": "需求清单",
    "demand_gmv": "预算/GMV",
    "demand_scale": "需求规模",
    "wuliu_requirement": "物流要求",
    "dingzhi_requirement": "定制要求",

    # —— 采购决策依据（purchaseDecisions 子字段）
    "decision_points": "决策点",
    "next_step": "建议动作",
    "importance": "重要性",

    # —— 流失 / 商机
    "lostReason": "流失原因",
    "lostRiskType": "流失类型",
    "lost_reason": "流失原因",
    "lostScore": "流失风险程度",
    "riskScore": "风险程度",
    "awakenType": "唤醒类型",
    "awaken_reason": "唤醒切入点",

    # —— 跨店询盘
    "shopName": "店铺名称",
    "shop_name": "店铺名称",
    "inqCnt": "询盘次数",
    "inq_cnt": "询盘次数",
    "lastInqTime": "最近询盘时间",
    "last_inq_time": "最近询盘时间",
    "cate": "类目",
    "cates": "类目",
    "items": "商品",
    "item": "商品",
    "keyword": "关键词",
    "keywords": "关键词",

    # —— 通用
    "summary": "摘要",
    "title": "关注点",
    "content": "正文",
    "reason": "原因",
    "detail": "详情",
    "desc": "描述",
    "description": "描述",
    "name": "名称",
    "type": "类型",
    "level": "等级",
    "score": "分数",
    "count": "数量",
    "cnt": "数量",
    "amount": "金额",
    "amt": "金额",
    "time": "时间",
    "date": "日期",
    "speech_script": "话术",
    "scripts": "话术列表",

    # —— 话术字段（已是中文，保持原名）
    "开场白": "开场白",
    "核心话术": "核心话术",
    "促单话术": "促单话术",
    "场景": "场景",
    "挽留话术": "挽留话术",
    "唤醒话术": "唤醒话术",
    "跟进话术": "跟进话术",
}


# 兜底分词翻译
_TOKEN_FALLBACK = {
    "pay": "采购", "supply": "供应链", "inq": "询盘", "shop": "店铺",
    "cate": "类目", "cates": "类目", "item": "商品", "items": "商品",
    "search": "搜索", "keyword": "关键词", "keywords": "关键词",
    "name": "名称", "type": "类型", "level": "等级", "score": "分数",
    "count": "数量", "cnt": "数量", "num": "数量",
    "amount": "金额", "amt": "金额", "time": "时间", "date": "日期",
    "stability": "稳定性", "cycle": "周期", "change": "变更",
    "distribution": "分布", "chain": "链", "buyer": "买家",
    "seller": "卖家", "advice": "建议", "reason": "原因",
    "list": "列表", "detail": "详情", "history": "历史",
    "recent": "近期", "last": "最近", "first": "首次",
    "main": "主要", "total": "总计", "average": "平均",
    "30d": "近30天", "60d": "近60天", "90d": "近90天",
    "180d": "近半年", "365d": "近一年",
    "1m": "近一月", "3m": "近三月", "6m": "近半年", "12m": "近一年",
}


def tr(key) -> str:
    """字段英文 → 中文译名。

    1. 优先在 FIELD_NAME_ALIAS 完全匹配
    2. 大小写无关再查一次
    3. 用下划线/驼峰拆词，逐 token 用 _TOKEN_FALLBACK 模糊翻译
    4. 全部失败则原样返回（agent 层可再做兜底）
    """
    if not isinstance(key, str):
        return str(key)
    if key in FIELD_NAME_ALIAS:
        return FIELD_NAME_ALIAS[key]
    if key.lower() in FIELD_NAME_ALIAS:
        return FIELD_NAME_ALIAS[key.lower()]

    # camelCase 拆词
    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", key).lower()
    if snake in FIELD_NAME_ALIAS:
        return FIELD_NAME_ALIAS[snake]

    # 模糊翻译
    parts = [p for p in re.split(r"[_\-\s]+", snake) if p]
    if not parts:
        return key
    translated = []
    hit = 0
    for p in parts:
        if p in _TOKEN_FALLBACK:
            translated.append(_TOKEN_FALLBACK[p])
            hit += 1
        else:
            translated.append(p)
    if hit == 0:
        return key
    return "".join(translated)


def parse_loose(data):
    """宽松解析字符串：先 json.loads，失败再 ast.literal_eval（兼容 Python repr）。

    解决 1688 接口偶尔返回 `{'开场白':'...'}` 这种单引号字典字符串的问题。
    解析失败则返回原值（不再包成 {"内容": ...}）。
    """
    if not isinstance(data, str):
        return data
    s = data.strip()
    if not s or s[0] not in "{[":
        return data
    try:
        return json.loads(s)
    except Exception:
        pass
    try:
        return ast.literal_eval(s)
    except Exception:
        return data


def deep_parse(data):
    """递归把 data 中所有形如 dict/list 的字符串解析为对象"""
    if isinstance(data, str):
        parsed = parse_loose(data)
        if parsed is data:
            return data
        return deep_parse(parsed)
    if isinstance(data, dict):
        return {k: deep_parse(v) for k, v in data.items()}
    if isinstance(data, list):
        return [deep_parse(x) for x in data]
    return data
