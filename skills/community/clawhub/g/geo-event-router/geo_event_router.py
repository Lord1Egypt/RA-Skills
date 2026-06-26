#!/usr/bin/env python3
"""
geo-event-router - 宏观地缘事件路由与评分

负责新闻事件的分析、分类、评分和推送决策。
"""

import hashlib
import re
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from datetime import datetime

# =============================================================================
# 配置区
# =============================================================================

VERSION = "1.0.0"

# 推送阈值
PUSH_THRESHOLD_HIGH = 70   # >= 70: 立即推送
PUSH_THRESHOLD_WATCH = 50  # 50-69: 观察池

# 冷却时间（分钟）
COOLDOWN_HIGH = 90
COOLDOWN_MEDIUM = 180

# 事件类型基础分
EVENT_TYPE_SCORES = {
    "military": 35,
    "geopolitics": 28,
    "central_bank": 30,
    "commodity": 25,
    "market": 25,
}

# 关键词分类
KEYWORD_CATEGORIES = {
    "military": ["导弹", "空袭", "军事行动", "战争", "袭击", "打击", "轰炸", "无人机", "战机", "航母"],
    "geopolitics": ["制裁", "外交", "霍尔木兹", "中东", "俄乌", "台海", "南海", "冲突", "封锁", "军演"],
    "central_bank": ["美联储", "央行", "加息", "降息", "利率决议", "FOMC", "QE", "缩表", "点阵图"],
    "commodity": ["原油", "黄金", "白银", "铜", "大宗商品", "油价", "金价", "期货"],
    "market": ["熔断", "暴涨", "暴跌", "跳水", "巨震", "血洗", "千股", "崩盘"],
}

# 区域关键词
REGION_KEYWORDS = {
    "中东": ["中东", "伊朗", "以色列", "沙特", "霍尔木兹", "红海", "也门"],
    "俄乌": ["俄乌", "乌克兰", "俄罗斯", "普京", "泽连斯基"],
    "台海": ["台海", "台湾", "两岸", "解放军"],
    "南海": ["南海", "南沙", "西沙"],
}

# 降噪关键词
NOISE_KEYWORDS = ["传闻", "据悉", "或", "可能", "预计", "分析", "评论", "观点", "认为"]

# =============================================================================
# 数据结构
# =============================================================================

@dataclass
class NewsItem:
    """归一化后的新闻条目"""
    title: str
    content: str
    source: str
    time_str: str
    time_ts: int
    url: str = ""
    raw: Dict = field(default_factory=dict)
    
    def fingerprint(self) -> str:
        """生成新闻指纹（用于快速去重）"""
        text = f"{self.title[:50]}|{self.content[:100]}"
        return hashlib.md5(text.encode('utf-8')).hexdigest()

@dataclass
class EventScore:
    """事件评分结果"""
    total: float = 0.0
    base_score: float = 0.0
    confidence_bonus: float = 0.0
    market_bonus: float = 0.0
    noise_penalty: float = 0.0
    llm_bonus: float = 0.0
    reasons: List[str] = field(default_factory=list)
    
    def add_reason(self, reason: str):
        self.reasons.append(reason)

@dataclass
class MarketImpact:
    """市场影响数据（简化版，完整数据来自 geo-market-impact-mapper）"""
    oil_pct: float = 0.0
    gold_pct: float = 0.0
    
    def is_high_priority(self) -> bool:
        return abs(self.oil_pct) >= 3.0 or abs(self.gold_pct) >= 2.0
    
    def is_watch_level(self) -> bool:
        return abs(self.oil_pct) >= 1.2 or abs(self.gold_pct) >= 0.8

@dataclass
class LLMAnalysis:
    """LLM 分析结果"""
    event_type: str = ""
    urgency: str = "低"
    novelty: str = "中"
    market_bias: str = "中性"
    reasoning: List[str] = field(default_factory=list)
    should_push: bool = False
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'LLMAnalysis':
        return cls(
            event_type=data.get('event_type', ''),
            urgency=data.get('urgency', '低'),
            novelty=data.get('novelty', '中'),
            market_bias=data.get('market_bias', '中性'),
            reasoning=data.get('reasoning', []),
            should_push=data.get('should_push', False),
        )

@dataclass
class Event:
    """事件对象"""
    event_id: str
    fingerprint: str
    title: str
    event_type: str
    severity: str
    score: EventScore
    llm_analysis: Optional[LLMAnalysis] = None
    market_impact: Optional[MarketImpact] = None
    sources: List[str] = field(default_factory=list)
    related_stocks: List[Dict] = field(default_factory=list)
    impact_path: str = ""
    first_seen: str = ""
    last_seen: str = ""
    push_count: int = 0
    stage: str = "new"
    
    def to_dict(self) -> Dict:
        return {
            'event_id': self.event_id,
            'fingerprint': self.fingerprint,
            'title': self.title,
            'event_type': self.event_type,
            'severity': self.severity,
            'score': asdict(self.score),
            'llm_analysis': asdict(self.llm_analysis) if self.llm_analysis else None,
            'market_impact': asdict(self.market_impact) if self.market_impact else None,
            'sources': self.sources,
            'related_stocks': self.related_stocks,
            'impact_path': self.impact_path,
            'first_seen': self.first_seen,
            'last_seen': self.last_seen,
            'push_count': self.push_count,
            'stage': self.stage,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Event':
        score_data = data.get('score', {})
        score = EventScore(
            total=score_data.get('total', 0),
            base_score=score_data.get('base_score', 0),
            confidence_bonus=score_data.get('confidence_bonus', 0),
            market_bonus=score_data.get('market_bonus', 0),
            noise_penalty=score_data.get('noise_penalty', 0),
            llm_bonus=score_data.get('llm_bonus', 0),
            reasons=score_data.get('reasons', []),
        )
        
        llm_data = data.get('llm_analysis')
        llm = LLMAnalysis.from_dict(llm_data) if llm_data else None
        
        market_data = data.get('market_impact')
        market = MarketImpact(**market_data) if market_data else None
        
        return cls(
            event_id=data.get('event_id', ''),
            fingerprint=data.get('fingerprint', ''),
            title=data.get('title', ''),
            event_type=data.get('event_type', ''),
            severity=data.get('severity', 'low'),
            score=score,
            llm_analysis=llm,
            market_impact=market,
            sources=data.get('sources', []),
            related_stocks=data.get('related_stocks', []),
            impact_path=data.get('impact_path', ''),
            first_seen=data.get('first_seen', ''),
            last_seen=data.get('last_seen', ''),
            push_count=data.get('push_count', 0),
            stage=data.get('stage', 'new'),
        )

# =============================================================================
# 事件检测与评分
# =============================================================================

def detect_event_type(news: NewsItem) -> str:
    """检测新闻事件类型"""
    text = news.title + " " + news.content
    
    scores = {}
    for event_type, keywords in KEYWORD_CATEGORIES.items():
        count = sum(1 for kw in keywords if kw in text)
        scores[event_type] = count
    
    if max(scores.values()) == 0:
        return "other"
    
    return max(scores, key=scores.get)

def generate_event_fingerprint(news: NewsItem, event_type: str) -> str:
    """
    生成事件指纹（多维度）
    格式：区域 | 主题 | 资产 | 行为
    """
    text = news.title + " " + news.content
    
    # 区域
    region = "global"
    for r, keywords in REGION_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            region = r.lower()
            break
    
    # 主题
    theme = event_type
    
    # 资产
    asset = "general"
    if any(kw in text for kw in ["原油", "石油", "油价", "布油", "WTI"]):
        asset = "oil"
    elif any(kw in text for kw in ["黄金", "贵金属", "金价"]):
        asset = "gold"
    elif any(kw in text for kw in ["美元", "汇率", "USD"]):
        asset = "usd"
    elif any(kw in text for kw in ["美股", "标普", "纳指", "道指"]):
        asset = "us_stock"
    elif any(kw in text for kw in ["A 股", "沪深", "上证", "创业板"]):
        asset = "cn_stock"
    
    # 行为
    action = "news"
    if any(kw in text for kw in ["袭击", "打击", "导弹", "空袭", "战争"]):
        action = "attack"
    elif any(kw in text for kw in ["制裁", "禁令", "限制"]):
        action = "sanction"
    elif any(kw in text for kw in ["加息", "降息", "利率"]):
        action = "rate"
    elif any(kw in text for kw in ["减产", "增产", "OPEC"]):
        action = "production"
    elif any(kw in text for kw in ["暴涨", "暴跌", "拉升", "跳水"]):
        action = "price_move"
    
    return f"{region}|{theme}|{asset}|{action}"

def score_news_item(news: NewsItem, market: MarketImpact, state: Optional[Dict] = None) -> EventScore:
    """
    多因子评分机制
    """
    score = EventScore()
    text = news.title + " " + news.content
    
    # 1. 事件类型基础分
    event_type = detect_event_type(news)
    base = EVENT_TYPE_SCORES.get(event_type, 10)
    score.base_score = base
    score.add_reason(f"事件类型：{event_type} (+{base})")
    
    # 2. 置信度加分
    if news.source == "财联社":
        score.confidence_bonus += 10
        score.add_reason("权威来源：财联社 (+10)")
    
    # 3. 市场映射加分
    if market.is_high_priority():
        score.market_bonus += 15
        score.add_reason(f"市场异动：原油{market.oil_pct:+.1f}% 黄金{market.gold_pct:+.1f}% (+15)")
    elif market.is_watch_level():
        score.market_bonus += 8
        score.add_reason(f"市场脉冲：原油{market.oil_pct:+.1f}% 黄金{market.gold_pct:+.1f}% (+8)")
    
    # 4. 降噪扣分
    noise_count = sum(1 for kw in NOISE_KEYWORDS if kw in text)
    if noise_count >= 2:
        score.noise_penalty = -20
        score.add_reason(f"噪声过多：{noise_count} 个不确定词 (-20)")
    
    # 计算总分
    score.total = score.base_score + score.confidence_bonus + score.market_bonus + score.noise_penalty
    
    return score

def generate_event_id(event_type: str, fingerprint: str) -> str:
    """生成事件唯一 ID"""
    text = f"{event_type}|{fingerprint}"
    return hashlib.md5(text.encode('utf-8')).hexdigest()[:16]

# =============================================================================
# LLM 分析（可选）
# =============================================================================

LLM_ENABLED = False
try:
    from llm_news_analyzer import analyze_semantic
    LLM_ENABLED = True
except ImportError:
    pass

def analyze_by_llm(news: NewsItem) -> Optional[LLMAnalysis]:
    """对单条新闻进行 LLM 分析"""
    if not LLM_ENABLED:
        return None
    
    try:
        result = analyze_semantic([{'title': news.title, 'content': news.content[:200]}])
        if result and len(result) > 0:
            r = result[0]
            return LLMAnalysis(
                event_type="geopolitics",
                urgency=r.get('urgency', '低'),
                novelty=r.get('novelty', '中'),
                market_bias=r.get('sentiment', '中性'),
                reasoning=r.get('semantic_analysis', '').split(';'),
                should_push=r.get('urgency') == '高' or r.get('sentiment') in ['利好', '利空'],
            )
    except Exception:
        pass
    
    return None

def merge_rule_and_llm(score: EventScore, llm: Optional[LLMAnalysis]) -> EventScore:
    """合并规则评分和 LLM 分析"""
    if not llm:
        return score
    
    if llm.urgency == '高':
        score.llm_bonus += 15
        score.add_reason("LLM 判定：高紧急度 (+15)")
    elif llm.urgency == '中':
        score.llm_bonus += 5
        score.add_reason("LLM 判定：中紧急度 (+5)")
    
    if llm.should_push:
        score.llm_bonus += 10
        score.add_reason("LLM 建议推送 (+10)")
    
    score.total = score.base_score + score.confidence_bonus + score.market_bonus + score.noise_penalty + score.llm_bonus
    
    return score

# =============================================================================
# 推送决策
# =============================================================================

def should_push_event(event: Event, state: Optional[Dict] = None) -> Tuple[bool, str]:
    """
    判断事件是否应该推送
    考虑：评分、冷却期、级别升级
    """
    score = event.score.total
    
    if state and event.event_id in state.get('event_cache', {}):
        cached = state['event_cache'][event.event_id]
        push_count = cached.get('push_count', 0)
        last_seen = cached.get('last_seen', '')
        severity = cached.get('severity', 'low')
        
        cooldown = COOLDOWN_HIGH if severity == 'high' else COOLDOWN_MEDIUM
        
        if last_seen:
            try:
                last_time = datetime.fromisoformat(last_seen.replace('Z', '+08:00'))
                elapsed_minutes = (datetime.now() - last_time).total_seconds() / 60
                
                if elapsed_minutes < cooldown:
                    if score >= 70 and push_count > 0:
                        return True, f"事件升级（冷却期内，评分{score}）"
                    return False, f"冷却期内（{elapsed_minutes:.0f}/{cooldown} 分钟）"
            except:
                pass
        
        if push_count >= 3:
            return False, "已达到最大推送次数"
    
    if score >= PUSH_THRESHOLD_HIGH:
        return True, f"高优先级（评分{score}）"
    elif score >= PUSH_THRESHOLD_WATCH:
        return False, f"观察池（评分{score}）"
    else:
        return False, f"评分不足（{score}）"

# =============================================================================
# 工具函数
# =============================================================================

def normalize_news(news: NewsItem) -> NewsItem:
    """新闻归一化"""
    news.title = re.sub(r'\s+', ' ', news.title).strip()
    news.content = re.sub(r'\s+', ' ', news.content).strip()
    return news

def select_llm_candidates(news_list: List[NewsItem], market: MarketImpact) -> List[NewsItem]:
    """筛选高价值 LLM 候选"""
    candidates = []
    
    for news in news_list:
        score = 0
        text = news.title + " " + news.content
        
        high_weight_kw = ["导弹", "空袭", "战争", "袭击", "加息", "降息", "熔断", "暴涨", "暴跌", "制裁"]
        if any(kw in text for kw in high_weight_kw):
            score += 20
        
        if any(kw in text for kw in ["中东", "俄乌", "台海", "霍尔木兹", "美联储", "央行"]):
            score += 15
        
        if market.is_high_priority():
            score += 15
        elif market.is_watch_level():
            score += 8
        
        if news.source == "财联社":
            score += 10
        
        if score >= 30:
            candidates.append(news)
    
    return candidates[:8]
