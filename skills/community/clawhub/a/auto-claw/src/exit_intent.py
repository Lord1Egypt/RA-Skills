"""
Exit Intent Detection — WordPress 退出意图干预系统
检测用户退出行为，自动弹出挽留内容
"""
import re
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class ExitIntentOffer:
    """退出挽留优惠"""
    id: str
    offer_type: str  # discount / free_shipping / bonus / urgency
    headline: str = ""
    subheadline: str = ""
    discount_code: str = ""
    discount_percent: int = 0
    cta_text: str = ""
    expires_hours: int = 24
    
    # 触发条件
    min_cart_value: float = 0.0
    is_exiting: bool = True
    
    # 统计
    shown_count: int = 0
    converted_count: int = 0
    
    @property
    def conversion_rate(self) -> float:
        return self.converted_count / self.shown_count if self.shown_count > 0 else 0.0

@dataclass
class ExitIntentRule:
    """退出意图规则"""
    rule_id: str
    name: str = ""
    
    # 触发条件
    trigger_type: str = "mouse_leaving"  # mouse_leaving / idle_timeout / scroll_back / low_cart_value
    
    # 页面类型
    page_types: List[str] = field(default_factory=list)  # home / product / cart / checkout
    url_patterns: List[str] = field(default_factory=list)
    exclude_urls: List[str] = field(default_factory=list)
    
    # 目标优惠
    offers: List[ExitIntentOffer] = field(default_factory=list)
    
    # 设置
    max_shows_per_session: int = 1
    delay_seconds: int = 0
    cookie_expiry_days: int = 7
    
    # 状态
    is_active: bool = True
    shown_count: int = 0
    converted_count: int = 0

@dataclass
class ExitIntentReport:
    """退出干预报告"""
    total_sessions: int = 0
    exit_detected_count: int = 0
    offer_shown_count: int = 0
    converted_count: int = 0
    abandoned_count: int = 0
    
    @property
    def exit_rate(self) -> float:
        return self.exit_detected_count / self.total_sessions if self.total_sessions > 0 else 0.0
    
    @property
    def conversion_rate(self) -> float:
        return self.converted_count / self.offer_shown_count if self.offer_shown_count > 0 else 0.0
    
    @property
    def recovery_rate(self) -> float:
        return self.converted_count / self.abandoned_count if self.abandoned_count > 0 else 0.0

class ExitIntentDetector:
    """
    WordPress 退出意图检测与干预系统
    
    功能：
    1. 检测退出意图信号（鼠标移动/闲置超时/滚动返回）
    2. 管理多种挽留优惠
    3. 生成弹出代码（JavaScript/短代码）
    4. 跟踪转化效果
    5. A/B测试不同优惠策略
    """
    
    def __init__(self, site_url: str = ""):
        self.site_url = site_url
        self.rules: Dict[str, ExitIntentRule] = {}
        self.offers: Dict[str, ExitIntentOffer] = {}
        self.report = ExitIntentReport()
    
    def create_offer(self, offer_type: str, headline: str,
                    cta_text: str = "CLAIM NOW",
                    discount_percent: int = 0,
                    discount_code: str = "") -> ExitIntentOffer:
        """创建优惠"""
        offer_id = f"offer_{len(self.offers) + 1}"
        offer = ExitIntentOffer(
            id=offer_id,
            offer_type=offer_type,
            headline=headline,
            cta_text=cta_text,
            discount_percent=discount_percent,
            discount_code=discount_code
        )
        self.offers[offer_id] = offer
        return offer
    
    def create_rule(self, name: str, trigger_type: str = "mouse_leaving",
                    page_types: List[str] = None) -> ExitIntentRule:
        """创建规则"""
        rule_id = f"rule_{len(self.rules) + 1}"
        rule = ExitIntentRule(
            rule_id=rule_id,
            name=name,
            trigger_type=trigger_type,
            page_types=page_types or ["cart", "checkout"]
        )
        self.rules[rule_id] = rule
        return rule
    
    def assign_offer_to_rule(self, rule_id: str, offer_id: str):
        """将优惠分配给规则"""
        rule = self.rules.get(rule_id)
        offer = self.offers.get(offer_id)
        if rule and offer:
            rule.offers.append(offer)
    
    def generate_popup_html(self, offer: ExitIntentOffer, rule: ExitIntentRule) -> str:
        """生成弹窗HTML"""
        discount_text = f"{offer.discount_percent}% OFF" if offer.discount_percent else "SPECIAL OFFER"
        urgency = f"限时 {offer.expires_hours} 小时" if offer.expires_hours else ""
        
        html = f'''
<!-- Exit Intent Popup - {offer.headline} -->
<style>
.exit-popup-overlay {{
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.7);
    z-index: 99998;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s;
}}
.exit-popup-overlay.active {{ opacity: 1; }}
.exit-popup {{
    background: #fff;
    border-radius: 16px;
    max-width: 480px;
    padding: 40px;
    text-align: center;
    position: relative;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}}
.exit-popup-close {{
    position: absolute;
    top: 12px; right: 16px;
    font-size: 24px;
    cursor: pointer;
    color: #999;
}}
.exit-popup-badge {{
    background: #e74c3c;
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    text-transform: uppercase;
    margin-bottom: 16px;
    display: inline-block;
}}
.exit-popup-headline {{
    font-size: 28px;
    font-weight: 700;
    color: #222;
    margin-bottom: 12px;
}}
.exit-popup-sub {{
    font-size: 16px;
    color: #666;
    margin-bottom: 24px;
}}
.exit-popup-code {{
    background: #f8f8f8;
    border: 2px dashed #e74c3c;
    padding: 12px 24px;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #e74c3c;
    margin-bottom: 24px;
}}
.exit-popup-cta {{
    background: #e74c3c;
    color: white;
    border: none;
    padding: 16px 40px;
    font-size: 16px;
    font-weight: 700;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s;
}}
.exit-popup-cta:hover {{ background: #c0392b; }}
.exit-popup-note {{
    font-size: 12px;
    color: #999;
    margin-top: 16px;
}}
</style>

<div id="exit-popup-{offer.id}" class="exit-popup-overlay">
    <div class="exit-popup">
        <div class="exit-popup-close" onclick="exitPopupClose()">×</div>
        <div class="exit-popup-badge">{discount_text} {urgency}</div>
        <div class="exit-popup-headline">{offer.headline}</div>
        <div class="exit-popup-sub">{offer.subheadline}</div>
        <div class="exit-popup-code">{offer.discount_code}</div>
        <button class="exit-popup-cta" onclick="exitPopupApply('{offer.discount_code}')">{offer.cta_text}</button>
        <div class="exit-popup-note">无需最低消费 · 有效期至 24:00</div>
    </div>
</div>

<script>
(function() {{
    let shown = false;
    let sessionKey = 'exit_popup_{offer.id}';
    
    function showPopup() {{
        if (shown || sessionStorage.getItem(sessionKey)) return;
        shown = true;
        sessionStorage.setItem(sessionKey, '1');
        document.getElementById('exit-popup-{offer.id}').classList.add('active');
    }}
    
    function exitPopupClose() {{
        document.getElementById('exit-popup-{offer.id}').classList.remove('active');
    }}
    
    function exitPopupApply(code) {{
        exitPopupClose();
        // 应用折扣码逻辑
        console.log('Applying code:', code);
    }}
    
    // 退出意图检测 (鼠标离开窗口)
    document.addEventListener('mouseout', function(e) {{
        if (e.clientY < 10) showPopup();
    }});
    
    // 闲置超时 (30秒无操作)
    let idleTimer;
    document.addEventListener('mousemove', function() {{
        clearTimeout(idleTimer);
        idleTimer = setTimeout(showPopup, 30000);
    }});
}})();
</script>'''
        return html
    
    def generate_wordpress_shortcode(self, rule_id: str) -> str:
        """生成 WordPress 短代码"""
        rule = self.rules.get(rule_id)
        if not rule or not rule.offers:
            return ""
        
        offer = rule.offers[0]
        popup_html = self.generate_popup_html(offer, rule)
        
        # 转义单引号
        escaped = popup_html.replace("'", "\\'").replace("\n", " ")
        
        return f'''[exit-intent id="{rule_id}" trigger="{rule.trigger_type}"]
<!-- {offer.headline} -->
[/exit-intent]'''
    
    def record_offer_shown(self, offer_id: str):
        """记录优惠展示"""
        offer = self.offers.get(offer_id)
        if offer:
            offer.shown_count += 1
        self.report.offer_shown_count += 1
    
    def record_conversion(self, offer_id: str):
        """记录转化"""
        offer = self.offers.get(offer_id)
        if offer:
            offer.converted_count += 1
        self.report.converted_count += 1
    
    def generate_report(self) -> Dict[str, Any]:
        """生成报告"""
        total_offers = sum(o.shown_count for o in self.offers.values())
        total_converted = sum(o.converted_count for o in self.offers.values())
        
        best_offer = None
        best_rate = 0.0
        for offer in self.offers.values():
            rate = offer.conversion_rate
            if rate > best_rate:
                best_rate = rate
                best_offer = offer
        
        return {
            "total_sessions_tracked": self.report.total_sessions,
            "exit_detected": self.report.exit_detected_count,
            "offer_shown": self.report.offer_shown_count,
            "converted": self.report.converted_count,
            "recovery_rate": f"{self.report.converted_count / max(1, self.report.exit_detected_count) * 100:.1f}%",
            "best_offer": {
                "name": best_offer.headline if best_offer else "N/A",
                "conversions": best_offer.converted_count if best_offer else 0,
                "rate": f"{best_rate * 100:.1f}%" if best_offer else "N/A"
            },
            "all_offers": [
                {"id": o.id, "headline": o.headline, "shown": o.shown_count, "converted": o.converted_count, "rate": f"{o.conversion_rate*100:.1f}%"}
                for o in self.offers.values()
            ]
        }

def demo():
    detector = ExitIntentDetector()
    
    # 创建优惠
    offer1 = detector.create_offer(
        offer_type="discount",
        headline="等等！别走 — 额外 15% OFF",
        cta_text="获取折扣",
        discount_percent=15,
        discount_code="STAY15"
    )
    
    offer2 = detector.create_offer(
        offer_type="free_shipping",
        headline="别让运费杀死这笔订单！",
        cta_text="免费配送",
        discount_code="FREESHIP"
    )
    offer2.subheadline = "使用免费配送码，订单立省运费"
    
    # 创建规则
    rule = detector.create_rule("Cart Exit", trigger_type="mouse_leaving", page_types=["cart", "checkout"])
    detector.assign_offer_to_rule(rule.rule_id, offer1.id)
    detector.assign_offer_to_rule(rule.rule_id, offer2.id)
    
    # 模拟数据
    offer1.shown_count = 1000
    offer1.converted_count = 45
    offer2.shown_count = 800
    offer2.converted_count = 28
    
    detector.report.total_sessions = 5000
    detector.report.exit_detected_count = 1200
    detector.report.offer_shown_count = 1800
    detector.report.converted_count = 73
    
    # 报告
    report = detector.generate_report()
    
    print("\n📊 Exit Intent 报告")
    print(f"   追踪会话: {report['total_sessions_tracked']}")
    print(f"   检测退出: {report['exit_detected']}")
    print(f"   优惠展示: {report['offer_shown']}")
    print(f"   挽回订单: {report['converted']}")
    print(f"   挽回率: {report['recovery_rate']}")
    print(f"\n   最佳优惠: {report['best_offer']['name']}")
    print(f"   转化数: {report['best_offer']['conversions']} ({report['best_offer']['rate']})")
    
    print("\n   所有优惠:")
    for o in report["all_offers"]:
        print(f"   - {o['headline']}: {o['shown']}展示/{o['converted']}转化({o['rate']})")
    
    print("\n   WordPress Shortcode:")
    print(f"   {detector.generate_wordpress_shortcode(rule.rule_id)[:60]}...")

if __name__ == "__main__":
    demo()
