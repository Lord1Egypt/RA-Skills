"""
User Journey Personalization — WordPress 用户旅程个性化引擎
基于用户行为动态调整内容展示
"""
import re
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class JourneyEvent:
    """用户旅程事件"""
    timestamp: str = ""
    event_type: str = ""  # page_view / click / scroll / search / add_to_cart / purchase / exit
    page_url: str = ""
    page_title: str = ""
    referrer: str = ""
    time_on_page: int = 0  # 秒
    scroll_depth: int = 0  # 百分比 0-100
    element_clicked: str = ""
    search_query: str = ""
    session_id: str = ""
    visitor_id: str = ""

@dataclass
class UserSegment:
    """用户分群"""
    segment_id: str
    name: str  # "new_visitor" / "returning" / "high_intent" / "cart_abandoner" / "purchaser"
    conditions: Dict = field(default_factory=dict)
    count: int = 0
    conversion_rate: float = 0.0

@dataclass
class PersonalizationRule:
    """个性化规则"""
    rule_id: str
    name: str = ""
    segment_id: str = ""
    trigger_type: str = ""  # entry / exit / time_on_page / scroll_depth / return_visitor
    
    # 内容替换
    replace_element: str = ""  # CSS selector
    content_type: str = ""  # headline / banner / cta / testimonial / recommendation
    headline: str = ""
    body: str = ""
    cta_text: str = ""
    cta_url: str = ""
    
    # 展示条件
    min_pages: int = 0
    min_time_seconds: int = 0
    max_impressions: int = 0  # 0=无限
    
    # 统计
    shown_count: int = 0
    clicked_count: int = 0
    
    @property
    def ctr(self) -> float:
        return self.clicked_count / self.shown_count if self.shown_count > 0 else 0.0

class JourneyTracker:
    """
    WordPress 用户旅程个性化引擎
    
    功能：
    1. 追踪用户行为事件（页面/点击/滚动/搜索/购买）
    2. 识别用户分群（新访客/回访客/高意图/购物车放弃）
    3. 创建个性化规则
    4. 生成动态内容替换代码
    5. A/B测试不同策略
    """
    
    def __init__(self, site_url: str = ""):
        self.site_url = site_url
        self.events: List[JourneyEvent] = []
        self.segments: Dict[str, UserSegment] = {}
        self.rules: Dict[str, PersonalizationRule] = {}
        self.sessions: Dict[str, List[JourneyEvent]] = defaultdict(list)
    
    # ========== 分群 ==========
    
    def create_segment(self, name: str, conditions: Dict) -> UserSegment:
        """创建用户分群"""
        seg_id = hashlib.md5(name.encode()).hexdigest()[:8]
        seg = UserSegment(segment_id=seg_id, name=name, conditions=conditions)
        self.segments[seg_id] = seg
        return seg
    
    def identify_segment(self, events: List[JourneyEvent]) -> str:
        """根据行为识别用户分群"""
        if not events:
            return "new_visitor"
        
        first_ts = events[0].timestamp
        now = datetime.now()
        first = datetime.fromisoformat(first_ts) if first_ts else now
        is_new = (now - first).total_seconds() < 300  # 5分钟内
        
        page_count = len(set(e.page_url for e in events))
        total_scroll = max(e.scroll_depth for e in events) if events else 0
        has_cart = any("cart" in e.page_url.lower() or e.event_type == "add_to_cart" for e in events)
        has_purchase = any(e.event_type == "purchase" for e in events)
        
        if has_purchase:
            return "purchaser"
        if has_cart and page_count >= 2:
            return "cart_abandoner"
        if page_count >= 3 and total_scroll > 60:
            return "high_intent"
        if not is_new and page_count >= 2:
            return "returning"
        
        return "new_visitor"
    
    def _default_segments(self):
        """默认分群"""
        if not self.segments:
            self.create_segment("new_visitor", {"visit_count": 1})
            self.create_segment("returning", {"min_visits": 2})
            self.create_segment("high_intent", {"min_pages": 3, "min_scroll": 60})
            self.create_segment("cart_abandoner", {"has_cart": True, "no_purchase": True})
            self.create_segment("purchaser", {"has_purchase": True})
    
    # ========== 规则 ==========
    
    def create_rule(self, name: str, segment_name: str, content_type: str,
                   trigger_type: str = "entry", headline: str = "",
                   body: str = "", cta_text: str = "", cta_url: str = "") -> PersonalizationRule:
        """创建个性化规则"""
        self._default_segments()
        
        rule_id = hashlib.md5(f"{name}{time.time()}".encode()).hexdigest()[:8]
        seg = next((s for s in self.segments.values() if s.name == segment_name), None)
        
        rule = PersonalizationRule(
            rule_id=rule_id,
            name=name,
            segment_id=seg.segment_id if seg else "",
            trigger_type=trigger_type,
            content_type=content_type,
            headline=headline,
            body=body,
            cta_text=cta_text,
            cta_url=cta_url
        )
        self.rules[rule_id] = rule
        return rule
    
    def match_rules(self, segment_name: str, page_url: str = "",
                   pages_viewed: int = 0, time_on_page: int = 0) -> List[PersonalizationRule]:
        """匹配适用的规则"""
        matched = []
        
        for rule in self.rules.values():
            # 检查分群
            seg = self.segments.get(rule.segment_id)
            if not seg or seg.name != segment_name:
                continue
            
            # 检查触发类型
            if rule.trigger_type == "entry" and page_url:
                matched.append(rule)
            elif rule.trigger_type == "return_visitor" and pages_viewed >= 1:
                matched.append(rule)
            elif rule.trigger_type == "time_on_page" and time_on_page >= rule.min_time_seconds:
                matched.append(rule)
            
            # 曝光上限
            if rule.max_impressions > 0 and rule.shown_count >= rule.max_impressions:
                continue
            
        return matched
    
    # ========== 追踪 ==========
    
    def track_event(self, visitor_id: str, event_type: str, page_url: str = "",
                   page_title: str = "", referrer: str = "", **kwargs):
        """记录事件"""
        event = JourneyEvent(
            timestamp=datetime.now().isoformat(),
            event_type=event_type,
            page_url=page_url,
            page_title=page_title,
            referrer=referrer,
            session_id=visitor_id[:16],
            visitor_id=visitor_id,
            **kwargs
        )
        self.events.append(event)
        self.sessions[visitor_id[:16]].append(event)
        
        # 更新分群计数
        seg_name = self.identify_segment(self.sessions[visitor_id[:16]])
        seg = next((s for s in self.segments.values() if s.name == seg_name), None)
        if seg:
            seg.count += 1
    
    def get_journey_summary(self, visitor_id: str) -> Dict[str, Any]:
        """获取用户旅程摘要"""
        events = self.sessions.get(visitor_id[:16], [])
        if not events:
            return {"visitor_id": visitor_id, "events": [], "segment": "unknown"}
        
        segment = self.identify_segment(events)
        page_views = sum(1 for e in events if e.event_type == "page_view")
        total_time = sum(e.time_on_page for e in events)
        max_scroll = max(e.scroll_depth for e in events) if events else 0
        pages = [e.page_url for e in events if e.event_type == "page_view"]
        
        return {
            "visitor_id": visitor_id,
            "segment": segment,
            "page_views": page_views,
            "total_time_seconds": total_time,
            "max_scroll_depth": max_scroll,
            "pages_visited": pages,
            "first_page": pages[0] if pages else "",
            "last_page": pages[-1] if pages else "",
            "events_count": len(events)
        }
    
    # ========== 内容生成 ==========
    
    def generate_personalized_headline(self, segment: str, default: str = "") -> str:
        """生成个性化标题"""
        headlines = {
            "new_visitor": "欢迎来到 {site_name} — 发现最适合你的选择",
            "returning": "欢迎回来！这里有新的更新",
            "high_intent": "还在犹豫？看看这些热门推荐",
            "cart_abandoner": "你有一笔订单还没完成",
            "purchaser": "感谢购买！看看这些相关产品"
        }
        return headlines.get(segment, default or headlines["new_visitor"])
    
    def generate_cta_block(self, segment: str) -> str:
        """生成个性化CTA块"""
        ctas = {
            "new_visitor": ('"免费试用"', '/trial'),
            "returning": ('"查看更新"', '/whats-new'),
            "high_intent": ('"立即购买"', '/checkout'),
            "cart_abandoner": ('"返回购物车"', '/cart'),
            "purchaser": ('"查看订单"', '/account')
        }
        text, url = ctas.get(segment, ('"开始"', '/'))
        return f'<a href="{url}" class="cta-button">{text}</a>'
    
    def generate_journey_html(self, visitor_id: str) -> str:
        """生成用户旅程HTML（用于调试展示）"""
        summary = self.get_journey_summary(visitor_id)
        seg = summary["segment"]
        
        headline = self.generate_personalized_headline(seg)
        cta = self.generate_cta_block(seg)
        
        html = f'''
<div class="journey-personalized" data-segment="{seg}" data-visitor="{visitor_id[:8]}">
    <div class="journey-headline">{headline}</div>
    <div class="journey-pages">浏览了 {summary['page_views']} 页面</div>
    <div class="journey-cta">{cta}</div>
</div>'''
        return html
    
    def generate_wp_shortcode(self, rule: PersonalizationRule) -> str:
        """生成WordPress短代码"""
        return f'''[journey-personalize segment="{rule.segment_id}" element="{rule.replace_element}" type="{rule.content_type}"]
  {rule.headline}
  {rule.body}
[/journey-personalize]'''
    
    # ========== 报告 ==========
    
    def generate_report(self) -> Dict[str, Any]:
        """生成个性化报告"""
        self._default_segments()
        
        total_visitors = sum(s.count for s in self.segments.values())
        
        return {
            "total_visitors_tracked": len(self.sessions),
            "total_events": len(self.events),
            "segments": {
                seg.name: {
                    "count": seg.count,
                    "pct": f"{seg.count/total_visitors*100:.1f}%" if total_visitors else "0%"
                }
                for seg in self.segments.values()
            },
            "active_rules": len(self.rules),
            "rules_performance": [
                {
                    "name": r.name,
                    "segment": self.segments.get(r.segment_id, UserSegment("", "")).name,
                    "shown": r.shown_count,
                    "clicked": r.clicked_count,
                    "ctr": f"{r.ctr:.2%}"
                }
                for r in self.rules.values()
            ]
        }

def demo():
    tracker = JourneyTracker(site_url="http://example.com")
    
    # 模拟新访客旅程
    vid = "visitor_001"
    tracker.track_event(vid, "page_view", page_url="/", page_title="Home", scroll_depth=30)
    tracker.track_event(vid, "page_view", page_url="/products", page_title="Products", scroll_depth=70)
    tracker.track_event(vid, "page_view", page_url="/product/widget-a", page_title="Widget A", scroll_depth=80, time_on_page=45)
    tracker.track_event(vid, "add_to_cart", page_url="/cart", page_title="Cart")
    
    # 模拟高意图用户
    vid2 = "visitor_002"
    tracker.track_event(vid2, "page_view", page_url="/", scroll_depth=50)
    tracker.track_event(vid2, "page_view", page_url="/products", scroll_depth=90)
    tracker.track_event(vid2, "page_view", page_url="/pricing", scroll_depth=80)
    
    # 获取摘要
    summary = tracker.get_journey_summary("visitor_001")
    print(f"\n📊 用户旅程: {summary['visitor_id']}")
    print(f"   分群: {summary['segment']}")
    print(f"   页面浏览: {summary['page_views']}")
    print(f"   最大滚动深度: {summary['max_scroll_depth']}%")
    print(f"   访问页面: {summary['pages_visited']}")
    
    # 个性化内容
    seg = summary["segment"]
    headline = tracker.generate_personalized_headline(seg)
    cta = tracker.generate_cta_block(seg)
    print(f"\n   个性化标题: {headline}")
    print(f"   个性化CTA: {cta}")
    
    # 报告
    report = tracker.generate_report()
    print(f"\n📈 整体报告:")
    print(f"   追踪访客: {report['total_visitors_tracked']}")
    print(f"   总事件数: {report['total_events']}")
    print(f"   分群分布:")
    for name, data in report["segments"].items():
        print(f"     {name}: {data['count']} ({data['pct']})")
    
    # 创建规则演示
    rule = tracker.create_rule(
        name="高意图用户Banner",
        segment_name="high_intent",
        content_type="banner",
        trigger_type="entry",
        headline="还在犹豫？立即决定享优惠"
    )
    
    print(f"\n   规则: {rule.name}")
    print(f"   短代码: {tracker.generate_wp_shortcode(rule)[:60]}...")

if __name__ == "__main__":
    demo()
