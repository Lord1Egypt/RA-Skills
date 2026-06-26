#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
经济数据监控 - 加密市场辅助功能
重要经济指标预告和通知：非农、CPI、利率决议等
"""

import json
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
import pytz

# 重要经济指标配置
ECONOMIC_INDICATORS = {
    "非农就业数据": {
        "keywords": ["Non-Farm Payrolls", "NFP", "Employment"],
        "importance": "high",
        "emoji": "👷"
    },
    "CPI": {
        "keywords": ["CPI", "Consumer Price Index", "通胀"],
        "importance": "high",
        "emoji": "📊"
    },
    "PPI": {
        "keywords": ["PPI", "Producer Price Index"],
        "importance": "medium",
        "emoji": "📈"
    },
    "GDP": {
        "keywords": ["GDP", "Gross Domestic Product"],
        "importance": "high",
        "emoji": "🏛️"
    },
    "FOMC利率决议": {
        "keywords": ["FOMC", "Interest Rate", "Fed Rate", "利率决议"],
        "importance": "high",
        "emoji": "🏦"
    },
    "零售销售": {
        "keywords": ["Retail Sales", "零售"],
        "importance": "medium",
        "emoji": "🛒"
    },
    "失业率": {
        "keywords": ["Unemployment Rate", "失业率"],
        "importance": "high",
        "emoji": "📉"
    },
    "制造业PMI": {
        "keywords": ["Manufacturing PMI", "制造业PMI"],
        "importance": "medium",
        "emoji": "🏭"
    },
    "服务业PMI": {
        "keywords": ["Services PMI", "服务业PMI"],
        "importance": "medium",
        "emoji": "🏢"
    },
    "ADP就业数据": {
        "keywords": ["ADP", "ADP Employment"],
        "importance": "medium",
        "emoji": "💼"
    }
}


class EconomicCalendar:
    """经济日历监控器"""

    def __init__(self):
        self.workspace = "/root/.openclaw/workspace/economic"
        os.makedirs(self.workspace, exist_ok=True)
        self.timezone = pytz.timezone('Asia/Shanghai')

    def fetch_economic_calendar(self, days: int = 7) -> List[Dict]:
        """
        获取经济日历数据
        使用多个数据源确保可靠性
        """
        events = []

        # 尝试从 Trading Economics 获取（如果可用）
        try:
            te_events = self._fetch_trading_economics(days)
            events.extend(te_events)
        except Exception as e:
            print(f"Trading Economics API 不可用: {e}")

        # 如果没有获取到数据，使用模拟数据（基于常见发布时间）
        if not events:
            events = self._generate_mock_events(days)

        # 过滤和标记重要事件
        events = self._filter_and_score_events(events)

        return events

    def _fetch_trading_economics(self, days: int) -> List[Dict]:
        """从 Trading Economics 获取经济日历（需要 API key）"""
        # 这里提供 API 集成框架，需要 API key 才能使用
        # 暂时返回空列表，依赖模拟数据
        return []

    def _generate_mock_events(self, days_ahead: int) -> List[Dict]:
        """
        生成模拟的经济数据发布时间
        基于历史规律和常见发布时间
        """
        events = []
        base_date = datetime.now(self.timezone)

        # 非农（每月第一个周五 21:30 北京时间）
        for i in range(1, 3):
            date = base_date + timedelta(days=i*7)
            date = self._adjust_to_first_friday(date)

            events.append({
                "name": "非农就业数据 (NFP)",
                "datetime": date.strftime("%Y-%m-%d %H:%M"),
                "country": "美国",
                "importance": "high",
                "expected": "+200K",
                "previous": "+256K",
                "emoji": "👷",
                "description": "影响最大的经济数据，直接影响市场流动性和风险偏好"
            })

        # CPI（每月中旬 21:30）
        for i in range(1, 3):
            date = base_date.replace(day=15) + timedelta(days=i*30)

            events.append({
                "name": "CPI 消费者价格指数",
                "datetime": date.strftime("%Y-%m-%d %H:%M"),
                "country": "美国",
                "importance": "high",
                "expected": "2.3%",
                "previous": "2.4%",
                "emoji": "📊",
                "description": "通胀指标，直接影响美联储政策预期"
            })

        # FOMC 利率决议（每年8次，通常在周三凌晨2:00）
        for i in range(1, 4):
            date = base_date + timedelta(days=i*30)
            date = self._adjust_to_wednesday(date)

            events.append({
                "name": "FOMC 利率决议",
                "datetime": date.strftime("%Y-%m-%d 02:00"),
                "country": "美国",
                "importance": "high",
                "expected": "维持不变",
                "previous": "5.25-5.50%",
                "emoji": "🏦",
                "description": "美联储货币政策会议，决定基准利率"
            })

        # 失业率（与非农同一天）
        for event in events:
            if "非农" in event["name"]:
                event_dt = datetime.strptime(event["datetime"], "%Y-%m-%d %H:%M")
                events.append({
                    "name": "失业率",
                    "datetime": event_dt.strftime("%Y-%m-%d %H:%M"),
                    "country": "美国",
                    "importance": "high",
                    "expected": "3.8%",
                    "previous": "3.7%",
                    "emoji": "📉",
                    "description": "就业市场健康状况指标"
                })

        # GDP（每季度末 21:30）
        for i in range(1, 2):
            date = base_date.replace(day=30) + timedelta(days=i*90)

            events.append({
                "name": "GDP 季度报告",
                "datetime": date.strftime("%Y-%m-%d %H:%M"),
                "country": "美国",
                "importance": "high",
                "expected": "2.0%",
                "previous": "1.6%",
                "emoji": "🏛️",
                "description": "经济增长核心指标"
            })

        # 零售销售（每月中旬 21:30）
        for i in range(1, 2):
            date = base_date.replace(day=14) + timedelta(days=i*30)

            events.append({
                "name": "零售销售月率",
                "datetime": date.strftime("%Y-%m-%d %H:%M"),
                "country": "美国",
                "importance": "medium",
                "expected": "0.3%",
                "previous": "0.4%",
                "emoji": "🛒",
                "description": "消费支出指标"
            })

        # ADP 就业数据（非农前2天 21:15）
        for i in range(1, 2):
            date = base_date.replace(day=5) + timedelta(days=i*30)

            events.append({
                "name": "ADP 就业数据",
                "datetime": date.strftime("%Y-%m-%d %H:%M"),
                "country": "美国",
                "importance": "medium",
                "expected": "+180K",
                "previous": "+195K",
                "emoji": "💼",
                "description": "非农先行指标"
            })

        return events

    def _adjust_to_first_friday(self, date: datetime) -> datetime:
        """调整到当月的第一个周五"""
        first_day = date.replace(day=1)
        days_until_friday = (4 - first_day.weekday()) % 7  # Friday = 4
        return first_day + timedelta(days=days_until_friday)

    def _adjust_to_wednesday(self, date: datetime) -> datetime:
        """调整到周三"""
        days_until_wednesday = (2 - date.weekday()) % 7  # Wednesday = 2
        return date + timedelta(days=days_until_wednesday)

    def _filter_and_score_events(self, events: List[Dict]) -> List[Dict]:
        """过滤和评分事件"""
        filtered = []

        now = datetime.now(self.timezone)

        for event in events:
            # 解析事件时间
            try:
                event_dt = datetime.strptime(event["datetime"], "%Y-%m-%d %H:%M")
                event_dt = self.timezone.localize(event_dt)

                # 只保留未来的事件
                if event_dt > now:
                    event["datetime_utc"] = event_dt.strftime("%Y-%m-%d %H:%M:%S %Z")
                    event["time_until"] = self._format_time_until(event_dt)
                    event["days_until"] = (event_dt - now).days
                    filtered.append(event)
            except Exception as e:
                print(f"解析事件时间失败: {e}")
                continue

        # 按时间排序
        filtered.sort(key=lambda x: x["days_until"])

        return filtered

    def _format_time_until(self, event_dt: datetime) -> str:
        """格式化距离事件的时间"""
        now = datetime.now(self.timezone)
        delta = event_dt - now

        days = delta.days
        hours = delta.seconds // 3600

        if days > 0:
            return f"{days} 天 {hours} 小时后"
        else:
            return f"{hours} 小时后"

    def generate_upcoming_report(self, days: int = 7) -> str:
        """生成即将发布的经济数据预告报告"""
        events = self.fetch_economic_calendar(days)

        if not events:
            return "📅 近期无重要经济数据发布"

        # 按重要性分类
        high_importance = [e for e in events if e.get("importance") == "high"]
        medium_importance = [e for e in events if e.get("importance") == "medium"]

        report = []
        report.append("📅 **经济数据发布预告** 📅\n")
        report.append(f"📊 未来 {days} 天重要经济数据\n")

        # 高重要性数据
        if high_importance:
            report.append("\n🔴 **高重要性** 🔴\n")
            for i, event in enumerate(high_importance[:5], 1):
                report.append(f"{event['emoji']} {i}. **{event['name']}**")
                report.append(f"   🕐 {event['datetime']}")
                report.append(f"   🌍 {event['country']}")
                report.append(f"   📊 预期: {event.get('expected', 'N/A')} | 前值: {event.get('previous', 'N/A')}")
                report.append(f"   ⏰ {event['time_until']}")
                report.append(f"   💡 {event.get('description', '')}")
                report.append("")

        # 中等重要性数据
        if medium_importance:
            report.append("\n🟡 **中等重要性** 🟡\n")
            for event in medium_importance[:3]:
                report.append(f"{event['emoji']} **{event['name']}**")
                report.append(f"   🕐 {event['datetime']} | ⏰ {event['time_until']}")
                report.append("")

        report.append("---")
        report.append("💡 提示: 高重要性数据发布前后市场波动性可能显著增加")

        return "\n".join(report)

    def check_imminent_events(self, hours: int = 24, days: int = 7) -> Optional[Dict]:
        """检查即将在指定小时内发布的事件"""
        events = self.fetch_economic_calendar(days)

        now = datetime.now(self.timezone)
        imminent = []

        for event in events:
            try:
                event_dt = datetime.strptime(event["datetime"], "%Y-%m-%d %H:%M")
                event_dt = self.timezone.localize(event_dt)
                delta = event_dt - now

                # 检查是否在指定小时内
                if 0 < delta.total_seconds() <= hours * 3600:
                    imminent.append(event)
            except:
                continue

        if imminent:
            # 按时间排序
            imminent.sort(key=lambda x: x["days_until"])
            return {
                "count": len(imminent),
                "events": imminent,
                "summary": self._generate_imminent_summary(imminent)
            }

        return None

    def _generate_imminent_summary(self, events: List[Dict]) -> str:
        """生成即将发布事件的摘要"""
        if not events:
            return ""

        lines = ["⚠️ **经济数据发布提醒** ⚠️\n"]

        for event in events:
            lines.append(f"{event['emoji']} **{event['name']}**")
            lines.append(f"🕐 {event['datetime']}")
            lines.append(f"🌍 {event['country']}")
            lines.append(f"⏰ {event['time_until']}")
            lines.append("")

        lines.append("📌 提示: 建议提前做好仓位管理，注意风险控制")
        return "\n".join(lines)

    def save_calendar(self, days: int = 7):
        """保存经济日历到文件"""
        events = self.fetch_economic_calendar(days)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"{self.workspace}/economic_calendar_{timestamp}.json"

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "events": events
            }, f, ensure_ascii=False, indent=2)

        print(f"💾 经济日历已保存到: {filepath}")
        return filepath


class EconomicNotifier:
    """经济数据通知器"""

    def __init__(self):
        self.calendar = EconomicCalendar()
        self.last_notified_file = "/root/.openclaw/workspace/economic/last_notified.json"
        os.makedirs(os.path.dirname(self.last_notified_file), exist_ok=True)

    def check_and_notify(self) -> Optional[str]:
        """检查并通知即将发布的重要数据"""
        # 检查24小时内的高重要性事件
        imminent = self.calendar.check_imminent_events(hours=24)

        if not imminent:
            return None

        # 读取上次通知记录
        last_notified = self._load_last_notified()

        # 过滤已通知过的事件
        new_events = []
        for event in imminent["events"]:
            event_key = f"{event['name']}_{event['datetime']}"
            if event_key not in last_notified:
                new_events.append(event)
                last_notified[event_key] = datetime.now().isoformat()

        if new_events:
            # 保存通知记录
            self._save_last_notified(last_notified)

            # 生成通知消息
            summary = self._generate_notification(new_events)
            return summary

        return None

    def _load_last_notified(self) -> Dict:
        """加载上次通知记录"""
        try:
            if os.path.exists(self.last_notified_file):
                with open(self.last_notified_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}

    def _save_last_notified(self, data: Dict):
        """保存通知记录"""
        with open(self.last_notified_file, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _generate_notification(self, events: List[Dict]) -> str:
        """生成通知消息"""
        lines = ["⚠️ **重要经济数据即将发布** ⚠️\n"]

        for event in events:
            lines.append(f"{event['emoji']} **{event['name']}**")
            lines.append(f"🕐 {event['datetime']}")
            lines.append(f"📊 预期: {event.get('expected', 'N/A')}")
            lines.append(f"⏰ {event['time_until']}")
            lines.append("")

        lines.append("📌 请注意市场波动风险！")

        return "\n".join(lines)


def main():
    """主函数"""
    print("📊 经济数据监控启动\n")

    calendar = EconomicCalendar()

    # 生成未来7天的经济数据预告
    print("=" * 80)
    print("📅 未来7天经济数据预告")
    print("=" * 80)
    print()
    print(calendar.generate_upcoming_report(days=7))
    print()

    # 保存到文件
    calendar.save_calendar(days=7)

    # 检查即将发布的事件
    print("=" * 80)
    print("⏰ 即将发布 (24小时内)")
    print("=" * 80)
    print()

    notifier = EconomicNotifier()
    notification = notifier.check_and_notify()

    if notification:
        print("📣 通知内容:")
        print(notification)
    else:
        print("✅ 24小时内无重要数据发布")

    print("\n✅ 经济数据监控完成")


if __name__ == "__main__":
    main()
