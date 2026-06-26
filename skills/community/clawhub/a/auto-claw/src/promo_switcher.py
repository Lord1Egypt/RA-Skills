"""
Promo Switch — WordPress 大促页面自动切换引擎
支持全站点主题/横幅/落地页自动切换
"""
import re
import json
import time
import hashlib
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

@dataclass
class PromoEvent:
    """大促事件"""
    event_id: str
    name: str  # "Black Friday 2026" / "双11 2026" / "618大促"
    
    # 时间
    start_date: str = ""  # ISO date
    end_date: str = ""
    timezone: str = "UTC"
    
    # 提前切换（小时）
    pre_start_hours: int = 24
    post_end_hours: int = 24  # 结束后保持时间
    
    # 激活状态
    is_active: bool = False
    current_phase: str = "inactive"  # pre / active / post / inactive
    
    # 配置
    theme_name: str = ""  # 切换到的主题
    banner_headline: str = ""
    banner_subheadline: str = ""
    banner_cta_text: str = ""
    banner_cta_url: str = ""
    banner_bg_color: str = "#e74c3c"
    
    # 落地页
    landing_page_url: str = ""
    hero_headline_override: str = ""
    promotional_pricing: str = ""  # "全站5折起"
    
    # 统计
    views: int = 0
    clicks: int = 0
    conversions: int = 0

@dataclass
class PromoSchedule:
    """大促日程"""
    events: List[PromoEvent] = field(default_factory=list)
    
    # 当前激活
    active_event: Optional[PromoEvent] = None
    upcoming_event: Optional[PromoEvent] = None

class PromoSwitcher:
    """
    WordPress 大促页面自动切换引擎
    
    功能：
    1. 管理全年大促日历（Black Friday/双11/618/双12/新年等）
    2. 自动时间轴切换（预热→激活→延续）
    3. 主题/横幅/落地页自动切换
    4. 倒计时器显示
    5. 历史数据分析
    6. WP mu-plugin代码生成
    """
    
    # 内置大促日历
    BUILTIN_EVENTS = [
        {"name": "New Year Sale", "start": "01-01", "end": "01-07", "discount": "新年特惠"},
        {"name": "Spring Sale", "start": "03-15", "end": "03-22", "discount": "春季大促"},
        {"name": "618大促", "start": "06-18", "end": "06-20", "discount": "618半价"},
        {"name": "Summer Sale", "start": "07-01", "end": "07-15", "discount": "暑期优惠"},
        {"name": "Black Friday", "start": "11-27", "end": "11-30", "discount": "黑五折扣"},
        {"name": "双11", "start": "11-11", "end": "11-11", "discount": "双11特惠"},
        {"name": "双12", "start": "12-12", "end": "12-12", "discount": "双12特惠"},
        {"name": "Christmas", "start": "12-24", "end": "12-26", "discount": "圣诞特惠"},
    ]
    
    def __init__(self, site_url: str = "", web_root: str = ""):
        self.site_url = site_url
        self.web_root = web_root
        self.wp_cli = "/usr/local/bin/wp"
        self.php_bin = "/www/server/php/82/bin/php"
        self.events: Dict[str, PromoEvent] = {}
        self._load_builtin_events()
    
    def _load_builtin_events(self):
        """加载内置大促日历"""
        current_year = datetime.now().year
        
        for ev in self.BUILTIN_EVENTS:
            event_id = hashlib.md5(f"{ev['name']}{current_year}".encode()).hexdigest()[:8]
            
            # 解析日期
            try:
                start = datetime.strptime(f"{current_year}-{ev['start']}", "%Y-%m-%d")
                end = datetime.strptime(f"{current_year}-{ev['end']}", "%Y-%m-%d")
                # 如果结束日期在开始日期之前，说明跨年
                if end < start:
                    end = datetime.strptime(f"{current_year+1}-{ev['end']}", "%Y-%m-%d")
            except:
                continue
            
            promo = PromoEvent(
                event_id=event_id,
                name=f"{ev['name']} {current_year}",
                start_date=start.isoformat(),
                end_date=end.isoformat(),
                banner_headline=f"🎉 {ev['discount']}",
                banner_subheadline=f"{ev['name']} — 限时优惠",
                banner_cta_text="立即抢购",
                banner_bg_color="#e74c3c"
            )
            
            self._update_promo_phase(promo)
            self.events[event_id] = promo
    
    def _update_promo_phase(self, promo: PromoEvent):
        """更新大促阶段"""
        now = datetime.now()
        start = datetime.fromisoformat(promo.start_date)
        end = datetime.fromisoformat(promo.end_date)
        
        # 预热开始
        pre_start = start - timedelta(hours=promo.pre_start_hours)
        # 活动结束后延续
        post_end = end + timedelta(hours=promo.post_end_hours)
        
        if now < pre_start:
            promo.current_phase = "inactive"
            promo.is_active = False
        elif now < start:
            promo.current_phase = "pre"
            promo.is_active = False
        elif now <= end:
            promo.current_phase = "active"
            promo.is_active = True
        elif now <= post_end:
            promo.current_phase = "post"
            promo.is_active = False
        else:
            promo.current_phase = "inactive"
            promo.is_active = False
    
    def create_custom_event(self, name: str, start_date: str, end_date: str,
                          headline: str = "", theme: str = "",
                          cta_text: str = "立即抢购") -> PromoEvent:
        """创建自定义大促"""
        event_id = hashlib.md5(f"{name}{time.time()}".encode()).hexdigest()[:8]
        
        promo = PromoEvent(
            event_id=event_id,
            name=name,
            start_date=start_date,
            end_date=end_date,
            banner_headline=headline or f"🎉 {name}",
            theme_name=theme,
            banner_cta_text=cta_text
        )
        
        self._update_promo_phase(promo)
        self.events[event_id] = promo
        return promo
    
    def get_active_promos(self) -> List[PromoEvent]:
        """获取当前激活的大促"""
        return [e for e in self.events.values() if e.is_active]
    
    def get_current_promo(self) -> Optional[PromoEvent]:
        """获取当前最优先的大促"""
        active = self.get_active_promos()
        if active:
            return active[0]
        
        # 查找预热或延续中的
        for phase in ["pre", "post"]:
            pre_active = [e for e in self.events.values() if e.current_phase == phase]
            if pre_active:
                return pre_active[0]
        
        return None
    
    def get_upcoming_promos(self, days: int = 30) -> List[PromoEvent]:
        """获取即将到来30天内的大促"""
        now = datetime.now()
        cutoff = now + timedelta(days=days)
        
        upcoming = []
        for e in self.events.values():
            start = datetime.fromisoformat(e.start_date)
            if now <= start <= cutoff:
                upcoming.append(e)
        
        upcoming.sort(key=lambda x: x.start_date)
        return upcoming
    
    def generate_countdown(self, promo: PromoEvent) -> Dict[str, Any]:
        """生成倒计时"""
        now = datetime.now()
        
        if promo.current_phase == "active":
            end = datetime.fromisoformat(promo.end_date)
            remaining = end - now
            return {
                "phase": "active",
                "message": "活动进行中",
                "days": remaining.days,
                "hours": remaining.seconds // 3600,
                "minutes": (remaining.seconds % 3600) // 60,
                "seconds": remaining.seconds % 60
            }
        elif promo.current_phase == "pre":
            start = datetime.fromisoformat(promo.start_date)
            remaining = start - now
            return {
                "phase": "pre",
                "message": "距开始",
                "days": remaining.days,
                "hours": remaining.seconds // 3600,
                "minutes": (remaining.seconds % 3600) // 60,
                "seconds": remaining.seconds % 60
            }
        
        return {"phase": "inactive", "message": "", "days": 0, "hours": 0, "minutes": 0, "seconds": 0}
    
    def generate_banner_html(self, promo: PromoEvent) -> str:
        """生成促销横幅HTML"""
        countdown = self.generate_countdown(promo)
        
        if countdown["phase"] == "inactive":
            return ""
        
        cd_str = ""
        if countdown["days"] > 0:
            cd_str = f'{countdown["days"]}天{countdown["hours"]}时{countdown["minutes"]}分'
        elif countdown["hours"] > 0:
            cd_str = f'{countdown["hours"]}时{countdown["minutes"]}分{countdown["seconds"]}秒'
        else:
            cd_str = f'{countdown["minutes"]}分{countdown["seconds"]}秒'
        
        phase_texts = {
            "active": "距结束",
            "pre": "距开始"
        }
        
        return f'''
<!-- Auto-Claw Promo Banner: {promo.name} -->
<style>
.promo-banner {{
    background: {promo.banner_bg_color};
    color: white;
    padding: 12px 0;
    text-align: center;
    position: relative;
    z-index: 9999;
    display: none;
}}
.promo-banner.active {{ display: block; }}
.promo-banner-inner {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    flex-wrap: wrap;
}}
.promo-headline {{
    font-size: 18px;
    font-weight: 700;
    margin: 0;
}}
.promo-countdown {{
    background: rgba(255,255,255,0.2);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 14px;
}}
.promo-cta {{
    background: white;
    color: {promo.banner_bg_color};
    padding: 8px 20px;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 700;
    font-size: 14px;
}}
.promo-cta:hover {{ background: #f0f0f0; }}
</style>

<div class="promo-banner active" id="promo-banner-{promo.event_id}">
    <div class="promo-banner-inner">
        <span class="promo-headline">🎉 {promo.banner_headline}</span>
        <span class="promo-countdown">{phase_texts.get(countdown["phase"], "")} {cd_str}</span>
        <a href="{promo.banner_cta_url or "/"}" class="promo-cta">{promo.banner_cta_text}</a>
    </div>
</div>

<script>
(function() {{
    // 自动隐藏已结束的大促
    var end = new Date("{promo.end_date}");
    var now = new Date();
    var postEnd = new Date(end.getTime() + {promo.post_end_hours * 3600 * 1000});
    if (now > postEnd) {{
        var banner = document.getElementById("promo-banner-{promo.event_id}");
        if (banner) banner.classList.remove("active");
    }}
}})();
</script>'''
    
    def generate_wp_mu_plugin(self) -> str:
        """生成WordPress mu-plugin"""
        active_promo = self.get_current_promo()
        upcoming = self.get_upcoming_promos()
        
        # 序列化活动数据
        events_data = []
        for e in self.events.values():
            events_data.append({
                "id": e.event_id,
                "name": e.name,
                "start": e.start_date,
                "end": e.end_date,
                "headline": e.banner_headline,
                "phase": e.current_phase,
                "is_active": e.is_active
            })
        
        return f'''<?php
/**
 * Auto-Claw Promo Switcher
 * Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
 */
add_action('wp_head', 'auto_claw_promo_header', 5);
add_action('get_footer', 'auto_claw_promo_footer');

function auto_claw_get_active_promo() {{
    $promos = json_decode('{json.dumps([e.__dict__ for e in self.events.values()], default=str)}', true);
    $now = time();
    
    foreach ($promos as $promo) {{
        $start = strtotime($promo['start_date']);
        $end = strtotime($promo['end_date']);
        
        if ($start - 86400 <= $now && $now <= $end + 86400) {{
            return $promo;
        }}
    }}
    return null;
}}

function auto_claw_promo_header() {{
    $promo = auto_claw_get_active_promo();
    if (!$promo) return;
    
    $bg = $promo['banner_bg_color'] ?: '#e74c3c';
    $headline = esc_html($promo['banner_headline'] ?: $promo['name']);
    $cta = esc_html($promo['banner_cta_text'] ?: '立即抢购');
    $cta_url = esc_url($promo['banner_cta_url'] ?: '/');
    
    echo <<<HTML
<style>
.promo-banner{{
    background: $bg;
    color: white;
    padding: 12px;
    text-align: center;
    font-size: 16px;
}}
.promo-banner a{{
    background: white;
    color: $bg;
    padding: 6px 16px;
    border-radius: 4px;
    text-decoration: none;
    margin-left: 12px;
    font-weight: 700;
}}
</style>
<div class="promo-banner">
    🎉 $headline
    <a href="$cta_url">$cta</a>
</div>
HTML;
}}

function auto_claw_promo_footer() {{
    // 统计代码等
}}
'''
    
    def generate_wp_cli_activate_commands(self, promo: PromoEvent) -> List[str]:
        """生成激活大促的WP-CLI命令"""
        cmds = []
        
        if promo.theme_name:
            cmds.append(f"# 切换主题\n{self.wp_cli} theme activate {promo.theme_name}")
        
        if promo.landing_page_url:
            cmds.append(f"# 设置落地页\n{self.wp_cli} option update show_on_front page")
            cmds.append(f"{self.wp_cli} option update page_on_front $({self.wp_cli} post list --post_type=page --title='{promo.landing_page_url}' --field=ID)")
        
        cmds.append(f"# 发布大促公告\n{self.wp_cli} post create --post_type=post --post_title='{promo.name} 促销活动' --post_status=publish")
        
        return cmds
    
    def generate_report(self) -> Dict[str, Any]:
        """生成大促报告"""
        now = datetime.now()
        
        active = self.get_active_promos()
        upcoming = self.get_upcoming_promos()
        
        # 统计
        total_events = len(self.events)
        past_events = sum(1 for e in self.events.values() 
                         if datetime.fromisoformat(e.end_date) < now)
        
        return {
            "total_events_this_year": total_events,
            "active_now": len(active),
            "upcoming_30_days": len(upcoming),
            "past_events": past_events,
            "active_event": {
                "name": active[0].name if active else None,
                "phase": active[0].current_phase if active else None,
                "ends": active[0].end_date if active else None
            },
            "next_event": {
                "name": upcoming[0].name if upcoming else None,
                "starts": upcoming[0].start_date if upcoming else None,
                "days_until": (datetime.fromisoformat(upcoming[0].start_date) - now).days if upcoming else None
            } if upcoming else None,
            "all_events": [
                {"name": e.name, "start": e.start_date, "phase": e.current_phase}
                for e in sorted(self.events.values(), key=lambda x: x.start_date)
            ]
        }

def demo():
    switcher = PromoSwitcher(
        site_url="http://example.com",
        web_root=""
    )
    
    # 报告
    report = switcher.generate_report()
    
    print(f"\n📅 大促日历报告:")
    print(f"   全年大促: {report['total_events_this_year']}个")
    print(f"   已完成: {report['past_events']}个")
    print(f"   未来30天: {report['upcoming_30_days']}个")
    
    if report.get("active_event") and report["active_event"].get("name"):
        ae = report["active_event"]
        print(f"\n   🔴 当前激活: {ae['name']} ({ae['phase']})")
    else:
        print(f"\n   当前无激活大促")
    
    if report.get("next_event") and report["next_event"].get("name"):
        ne = report["next_event"]
        print(f"   📅 下一个: {ne['name']} ({ne['days_until']}天后)")
    
    print(f"\n   全部大促:")
    for e in report["all_events"]:
        phase_icons = {"active": "🔴", "pre": "🟡", "post": "🟢", "inactive": "⚪"}
        icon = phase_icons.get(e["phase"], "⚪")
        print(f"   {icon} {e['name']}: {e['start']}")
    
    # 横幅
    promo = list(switcher.events.values())[0]  # 第一个
    countdown = switcher.generate_countdown(promo)
    print(f"\n⏱️  倒计时演示 ({promo.name}):")
    print(f"    {countdown['message']}: {countdown['days']}天{countdown['hours']}时{countdown['minutes']}分")
    
    # WP-CLI命令
    cmds = switcher.generate_wp_cli_activate_commands(promo)
    print(f"\n📝 WP-CLI命令:")
    for c in cmds[:3]:
        print(f"    {c[:60]}")

if __name__ == "__main__":
    demo()
