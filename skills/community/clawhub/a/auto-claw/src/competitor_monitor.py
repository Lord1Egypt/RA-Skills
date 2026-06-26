"""
Competitor Monitor — 竞品监控与动态响应
监控竞品价格、活动、SEO变化，自动生成对策
"""
import re
import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class CompetitorData:
    """竞品数据快照"""
    url: str
    name: str = ""
    timestamp: str = ""
    
    # 价格/活动
    price_range: str = ""
    has_discount: bool = False
    discount_text: str = ""
    in_stock: bool = True
    
    # SEO信号
    title: str = ""
    meta_description: str = ""
    word_count: int = 0
    h1_count: int = 0
    backlinks_estimate: int = 0
    da_score: int = 0  # 域名权重估算
    
    # 内容
    main_keywords: List[str] = field(default_factory=list)
    new_content_detected: bool = False
    
    # 变化
    changes_since_last: Dict[str, str] = field(default_factory=dict)
    alerts: List[str] = field(default_factory=list)

@dataclass
class CompetitorAlert:
    """竞品动态告警"""
    severity: str  # CRITICAL / HIGH / MEDIUM / LOW
    competitor: str
    alert_type: str  # price_change / new_content / seo_drop / stock_out
    message: str
    our_action_suggestion: str = ""
    timestamp: str = ""

class CompetitorMonitor:
    """
    竞品监控与响应系统
    
    功能：
    1. 定时抓取竞品页面（价格/活动/内容）
    2. 检测变化（相比上次快照）
    3. SEO监控（关键词排名/新内容）
    4. 生成对策建议
    5. 触发自动响应（通过 Gate Pipeline）
    """
    
    def __init__(self, our_url: str = "", our_price: str = ""):
        self.our_url = our_url
        self.our_price = our_price
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        self.competitors: Dict[str, CompetitorData] = {}
        self.history: Dict[str, List[CompetitorData]] = defaultdict(list)
    
    def add_competitor(self, name: str, url: str):
        """添加竞品"""
        self.competitors[name] = CompetitorData(url=url, name=name)
    
    def fetch_competitor(self, name: str) -> CompetitorData:
        """抓取竞品数据"""
        comp = self.competitors.get(name)
        if not comp:
            return CompetitorData(url="", name=name)
        
        try:
            resp = self.session.get(comp.url, timeout=15)
            html = resp.text
            status = resp.status_code
        except Exception as e:
            comp.alerts.append(f"无法访问: {e}")
            return comp
        
        if status != 200:
            comp.alerts.append(f"HTTP {status}")
            return comp
        
        comp.timestamp = datetime.now().isoformat()
        
        # 价格
        price_patterns = [
            r'class=["\'][^"\']*price[^"\']*["\'][^>]*>.*?([$¥€£]?\d+[\.,]?\d*)',
            r'"price"\s*:\s*["\']?([$¥€£]?\d+[\.,]?\d*)',
            r'<span[^>]+class=["\'][^"\']*amount[^"\']*["\'][^>]*>([\d,]+)',
        ]
        for pat in price_patterns:
            match = re.search(pat, html, re.IGNORECASE | re.DOTALL)
            if match:
                comp.price_range = match.group(1)
                break
        
        # 折扣
        discount_patterns = [
            r'(?:sale|discount|off|%)\s*(\d+)%',
            r'(-?\d+%)\s*(?:off|sale)',
            r'class=["\'][^"\']*(?:sale|badge|tag)[^"\']*["\'][^>]*>([^<]{3,30})',
        ]
        for pat in discount_patterns:
            match = re.search(pat, html, re.IGNORECASE)
            if match:
                comp.has_discount = True
                comp.discount_text = match.group(0)[:50]
                break
        
        # 库存
        stock_patterns = [
            r'(?:out of stock| sold out| unavailable)',
            r'(?:in stock|available|ready to ship)',
        ]
        for pat in stock_patterns:
            if re.search(pat, html, re.IGNORECASE):
                comp.in_stock = "out" in pat.lower()
                break
        
        # SEO标题
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        if title_match:
            comp.title = title_match.group(1).strip()[:100]
        
        # Meta description
        desc_match = re.search(
            r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']',
            html, re.IGNORECASE
        )
        if desc_match:
            comp.meta_description = desc_match.group(1).strip()[:160]
        
        # 内容分析
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text).strip()
        comp.word_count = len(text.split())
        
        # H1
        h1s = re.findall(r'<h1[^>]*>([^<]+)</h1>', html, re.IGNORECASE)
        comp.h1_count = len(h1s)
        
        # 关键词提取（简化版）
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        word_freq = defaultdict(int)
        for w in words:
            word_freq[w] += 1
        top_words = sorted(word_freq.items(), key=lambda x: -x[1])[:10]
        comp.main_keywords = [w for w, _ in top_words]
        
        return comp
    
    def compare_with_us(self, competitor: CompetitorData) -> Dict[str, Any]:
        """对比我方与竞品"""
        return {
            "competitor": competitor.name,
            "competitor_price": competitor.price_range,
            "our_price": self.our_price,
            "price_advantage": competitor.price_range < self.our_price if competitor.price_range and self.our_price else None,
            "competitor_has_discount": competitor.has_discount,
            "competitor_in_stock": competitor.in_stock,
            "our_in_stock": True,
        }
    
    def detect_changes(self, name: str) -> Dict[str, str]:
        """检测相比上次的重大变化"""
        comp = self.competitors.get(name)
        if not comp:
            return {}
        
        history = self.history.get(name, [])
        if not history:
            return {"status": "首次抓取，无历史数据"}
        
        last = history[-1]
        changes = {}
        
        if comp.price_range != last.price_range:
            changes["price"] = f"{last.price_range} → {comp.price_range}"
        
        if comp.has_discount != last.has_discount:
            changes["discount"] = f"{last.has_discount} → {comp.has_discount}"
        
        if comp.in_stock != last.in_stock:
            changes["stock"] = f"{last.in_stock} → {comp.in_stock}"
        
        if comp.title != last.title:
            changes["title"] = "SEO标题已变化"
        
        if comp.word_count > last.word_count * 1.2:
            changes["content"] = f"内容量增加 {last.word_count} → {comp.word_count} 字"
        
        return changes
    
    def generate_alerts(self, name: str) -> List[CompetitorAlert]:
        """生成告警"""
        comp = self.competitors.get(name)
        if not comp:
            return []
        
        alerts = []
        
        # 价格变化
        changes = self.detect_changes(name)
        if changes.get("price"):
            alerts.append(CompetitorAlert(
                severity="HIGH",
                competitor=name,
                alert_type="price_change",
                message=f"竞品调价: {changes['price']}",
                our_action_suggestion="评估是否需要跟进价格策略"
            ))
        
        # 折扣开始
        if comp.has_discount and not self.history.get(name, [CompetitorData(url="")]):
            alerts.append(CompetitorAlert(
                severity="CRITICAL",
                competitor=name,
                alert_type="price_change",
                message=f"竞品开始打折: {comp.discount_text}",
                our_action_suggestion="考虑同步促销或差异化"
            ))
        
        # 缺货
        if not comp.in_stock and (not self.history.get(name) or self.history[name][-1].in_stock):
            alerts.append(CompetitorAlert(
                severity="MEDIUM",
                competitor=name,
                alert_type="stock_out",
                message="竞品缺货",
                our_action_suggestion="这是我们的流量机会，加强该品类推广"
            ))
        
        # SEO变化
        if changes.get("title"):
            alerts.append(CompetitorAlert(
                severity="LOW",
                competitor=name,
                alert_type="seo_change",
                message="竞品SEO标题已更新",
                our_action_suggestion="检查是否针对同一关键词"
            ))
        
        if changes.get("content"):
            alerts.append(CompetitorAlert(
                severity="MEDIUM",
                competitor=name,
                alert_type="new_content",
                message=f"竞品内容大幅更新 ({changes['content']})",
                our_action_suggestion="评估是否需要更新我们内容"
            ))
        
        return alerts
    
    def monitor_all(self) -> Dict[str, Any]:
        """监控所有竞品"""
        results = {}
        all_alerts = []
        
        for name in self.competitors:
            # 保存历史
            self.history[name].append(self.competitors[name])
            
            # 抓取
            comp = self.fetch_competitor(name)
            results[name] = comp
            
            # 检测变化
            changes = self.detect_changes(name)
            
            # 生成告警
            alerts = self.generate_alerts(name)
            all_alerts.extend(alerts)
        
        return {
            "competitors": results,
            "alerts": all_alerts,
            "monitored_at": datetime.now().isoformat(),
        }

def demo():
    """演示"""
    monitor = CompetitorMonitor(
        our_url="http://example.com/product",
        our_price="$99"
    )
    
    # 添加竞品（示例）
    monitor.add_competitor("竞品A", "https://example.com/competitor-a")
    
    # 模拟首次抓取
    comp_a = monitor.fetch_competitor("竞品A")
    comp_a.price_range = "$89"
    comp_a.has_discount = True
    comp_a.discount_text = "20% OFF"
    comp_a.in_stock = True
    comp_a.title = "Best Widget Pro"
    comp_a.word_count = 1500
    monitor.history["竞品A"].append(comp_a)
    
    # 模拟变化（第二次）
    time.sleep(1)
    comp_a2 = monitor.fetch_competitor("竞品A")
    comp_a2.price_range = "$79"  # 降价
    comp_a2.has_discount = True
    comp_a2.discount_text = "30% OFF"  # 折扣加深
    comp_a2.in_stock = True
    comp_a2.title = "Best Widget Pro - New Version"
    comp_a2.word_count = 2000  # 新增内容
    monitor.competitors["竞品A"] = comp_a2
    
    results = monitor.monitor_all()
    
    print("竞品监控结果:")
    for name, comp in results["competitors"].items():
        print(f"\n{name}:")
        print(f"  价格: {comp.price_range}")
        print(f"  折扣: {comp.has_discount} ({comp.discount_text})")
        print(f"  库存: {'有货' if comp.in_stock else '缺货'}")
    
    print("\n告警:")
    for alert in results["alerts"]:
        icon = "🔴" if alert.severity == "CRITICAL" else "🟡"
        print(f"  {icon} [{alert.severity}] {alert.message}")
        print(f"     建议: {alert.our_action_suggestion}")

if __name__ == "__main__":
    demo()
