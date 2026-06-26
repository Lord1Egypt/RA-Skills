#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情感分析模块 - 判断新闻利好/利空/中性
Author: Lin Hui
"""

import re
from typing import Dict, List, Tuple


# ============================================================================
# 情感词典
# ============================================================================

# 利好词汇（正面）
BULLISH_WORDS = [
    # 业绩/财务
    "增长", "上涨", "盈利", "利润", "营收", "净利", "超预期", "预增", 
    "暴增", "大增", "扭亏", "分红", "高送转", "回购", "增持",
    # 政策/宏观
    "利好", "支持", "鼓励", "扶持", "刺激", "放宽", "改革", "开放",
    "新基建", "碳中和", "新能源", "芯片", "半导体", "国产替代",
    # 交易/市场
    "涨停", "放量", "突破", "金叉", "买入", "推荐", "看多", "牛市",
    "主力资金流入", "机构调研", "外资增持",
    # 合作/并购
    "签约", "中标", "合作", "并购", "重组", "借壳", "整体上市",
    # 技术/创新
    "突破", "创新", "专利", "研发", "量产", "上车", "壁垒"
]

# 利空词汇（负面）
BEARISH_WORDS = [
    # 业绩/财务
    "下跌", "亏损", "下滑", "暴雷", "商誉减值", "计提", "预警", 
    "预亏", "停产", "停工", "裁员", "降薪", "承压", "不及预期",
    # 政策/监管
    "利空", "监管", "处罚", "罚款", "调查", "立案", "违规", 
    "暂停", "禁止", "限制", "收紧", "调控", "打压",
    # 交易/市场
    "跌停", "放量下跌", "破位", "死叉", "卖出", "看空", "熊市",
    "主力资金流出", "机构出逃", "质押爆仓",
    # 风险/危机
    "风险", "债务危机", "资金链断裂", "退市", "ST", "*ST", 
    "诉讼", "仲裁", "担保", "冻结", "查封", "暴雷", "爆雷",
    # 负面事件
    "造假", "欺诈", "财务造假", "虚增", "操纵", "内幕交易",
    "高管离职", "董事长", "总裁", "被调查", "拘留", "逮捕"
]

# 中性词汇（需结合上下文）
NEUTRAL_WORDS = [
    "公告", "披露", "发布", "召开", "股东大会", "董事会",
    "季报", "年报", "中报", "预案", "停牌", "复牌",
    "问询函", "关注函", "监管函"
]


# ============================================================================
# 板块情感词典（针对特定板块）
# ============================================================================

SECTOR_BULLISH = {
    "新能源": ["碳中和", "光伏", "风电", "储能", "动力电池", "充电桩", "氢能"],
    "芯片": ["国产替代", "半导体", "光刻机", "晶圆", "封测", "EDA"],
    "人工智能": ["AI", "大模型", "算力", "GPU", "数据中心", "机器学习"],
    "医药": ["创新药", "临床试验", "FDA", "NMPA", "医疗器械", "疫苗"],
    "房地产": ["限购放松", "首付降低", "LPR", "棚改", "旧改"],
}

SECTOR_BEARISH = {
    "新能源": ["产能过剩", "价格战", "补贴退坡"],
    "芯片": ["出口管制", "制裁", "断供", "光刻机禁运"],
    "人工智能": ["监管", "算法备案", "数据安全"],
    "医药": ["集采", "医保谈判", "降价", "带量采购"],
    "房地产": ["调控", "限购", "三道红线", "债务危机"],
}


# ============================================================================
# 情感分析器
# ============================================================================

class SentimentAnalyzer:
    """新闻情感分析器"""
    
    def __init__(self):
        # 预编译正则表达式
        self.bullish_pattern = self._build_pattern(BULLISH_WORDS)
        self.bearish_pattern = self._build_pattern(BEARISH_WORDS)
    
    def _build_pattern(self, words: List[str]) -> re.Pattern:
        """构建正则模式"""
        # 按长度倒序排列，优先匹配长词
        sorted_words = sorted(words, key=len, reverse=True)
        pattern = "|".join([re.escape(w) for w in sorted_words])
        return re.compile(pattern)
    
    def analyze_text(self, text: str, sector: str = "") -> Dict[str, any]:
        """
        分析文本情感
        返回: {"sentiment": "利好/利空/中性", "score": float, "bullish_count": int, "bearish_count": int}
        """
        if not text:
            return {"sentiment": "中性", "score": 0.0, "bullish_count": 0, "bearish_count": 0}
        
        # 统计利好词
        bullish_matches = self.bullish_pattern.findall(text)
        bullish_count = len(bullish_matches)
        
        # 统计利空词
        bearish_matches = self.bearish_pattern.findall(text)
        bearish_count = len(bearish_matches)
        
        # 板块特定词汇
        if sector and sector in SECTOR_BULLISH:
            for word in SECTOR_BULLISH[sector]:
                if word in text:
                    bullish_count += 2  # 板块利好词权重更高
        
        if sector and sector in SECTOR_BEARISH:
            for word in SECTOR_BEARISH[sector]:
                if word in text:
                    bearish_count += 2  # 板块利空词权重更高
        
        # 计算情感得分 (-1 到 1)
        total = bullish_count + bearish_count
        if total == 0:
            score = 0.0
            sentiment = "中性"
        else:
            score = (bullish_count - bearish_count) / total
            if score > 0.3:
                sentiment = "利好 📈"
            elif score < -0.3:
                sentiment = "利空 📉"
            else:
                sentiment = "中性 ➡️"
        
        return {
            "sentiment": sentiment,
            "score": round(score, 2),
            "bullish_count": bullish_count,
            "bearish_count": bearish_count
        }
    
    def analyze_news(self, title: str, content: str = "", sector: str = "") -> Dict[str, any]:
        """
        分析新闻情感（标题权重更高）
        """
        # 标题权重 x3，内容权重 x1
        title_result = self.analyze_text(title, sector)
        content_result = self.analyze_text(content, sector)
        
        # 综合得分（标题权重更高）
        combined_score = title_result["score"] * 0.6 + content_result["score"] * 0.4
        
        if combined_score > 0.3:
            sentiment = "利好 📈"
        elif combined_score < -0.3:
            sentiment = "利空 📉"
        else:
            sentiment = "中性 ➡️"
        
        return {
            "sentiment": sentiment,
            "score": round(combined_score, 2),
            "bullish_count": title_result["bullish_count"] + content_result["bullish_count"],
            "bearish_count": title_result["bearish_count"] + content_result["bearish_count"],
            "title_sentiment": title_result["sentiment"],
            "content_sentiment": content_result["sentiment"]
        }
    
    def batch_analyze(self, news_list: List[Dict], sector: str = "") -> List[Dict]:
        """
        批量分析新闻列表
        news_list: [{"title": "...", "content": "..."}, ...]
        """
        results = []
        for news in news_list:
            title = news.get("title", "")
            content = news.get("content", "")
            result = self.analyze_news(title, content, sector)
            news_with_sentiment = news.copy()
            news_with_sentiment["sentiment"] = result["sentiment"]
            news_with_sentiment["sentiment_score"] = result["score"]
            news_with_sentiment["bullish_count"] = result["bullish_count"]
            news_with_sentiment["bearish_count"] = result["bearish_count"]
            results.append(news_with_sentiment)
        return results


# ============================================================================
# 汇总分析
# ============================================================================

def summarize_sentiment(news_list: List[Dict]) -> Dict[str, any]:
    """
    汇总多条新闻的情感倾向
    返回整体市场情绪：看涨/看跌/观望
    """
    if not news_list:
        return {"overall": "观望", "bullish_ratio": 0, "bearish_ratio": 0, "total": 0}
    
    bullish = sum(1 for n in news_list if "利好" in n.get("sentiment", ""))
    bearish = sum(1 for n in news_list if "利空" in n.get("sentiment", ""))
    neutral = len(news_list) - bullish - bearish
    
    total = len(news_list)
    bullish_ratio = bullish / total if total > 0 else 0
    bearish_ratio = bearish / total if total > 0 else 0
    
    if bullish_ratio > 0.5:
        overall = "看涨 📈"
    elif bearish_ratio > 0.5:
        overall = "看跌 📉"
    else:
        overall = "观望 ➡️"
    
    return {
        "overall": overall,
        "bullish_count": bullish,
        "bearish_count": bearish,
        "neutral_count": neutral,
        "bullish_ratio": round(bullish_ratio, 2),
        "bearish_ratio": round(bearish_ratio, 2),
        "total": total
    }


# ============================================================================
# CLI测试
# ============================================================================

if __name__ == "__main__":
    import sys
    import json
    
    analyzer = SentimentAnalyzer()
    
    test_texts = [
        "公司净利润同比增长50%，超预期",
        "突发！公司爆雷，亏损10亿",
        "公司发布年度财报",
        "政策利好！新能源行业迎来重大支持",
        "芯片出口管制升级，相关企业承压",
    ]
    
    print("=" * 60)
    print("情感分析测试")
    print("=" * 60)
    
    for text in test_texts:
        result = analyzer.analyze_text(text)
        print(f"\n文本: {text}")
        print(f"情感: {result['sentiment']}")
        print(f"得分: {result['score']}")
        print(f"利好词: {result['bullish_count']} | 利空词: {result['bearish_count']}")
    
    # 测试汇总
    print("\n" + "=" * 60)
    print("汇总测试")
    print("=" * 60)
    
    news_list = [
        {"title": "公司业绩大增50%", "sentiment": ""},
        {"title": "政策利好新能源", "sentiment": ""},
        {"title": "公司发布年报", "sentiment": ""},
        {"title": "行业监管趋严", "sentiment": ""},
    ]
    
    analyzed = analyzer.batch_analyze(news_list, sector="新能源")
    summary = summarize_sentiment(analyzed)
    
    print(json.dumps(summary, ensure_ascii=False, indent=2))
