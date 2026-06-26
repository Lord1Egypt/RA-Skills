#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
经济数据分析器 - 利多利空判断
根据实际值、预期值、前值分析数据对市场的影响
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
import os


class EconomicDataAnalyzer:
    """经济数据分析器"""

    def __init__(self):
        self.workspace = "/root/.openclaw/workspace/crypto/data"
        os.makedirs(self.workspace, exist_ok=True)
        self.actual_data_file = f"{self.workspace}/actual_data.json"

    def analyze_impact(self, event: Dict) -> Dict:
        """
        分析经济数据对市场的影响

        返回：
        {
            'direction': 'bullish' | 'bearish' | 'neutral',
            'strength': 'strong' | 'moderate' | 'weak',
            'reason': '分析原因',
            'emoji': '🟢' | '🔴' | '🟡'
        }
        """
        # 检查是否有实际值
        if 'actual' not in event:
            return {
                'direction': 'neutral',
                'strength': 'weak',
                'reason': '暂无实际值数据，无法分析',
                'emoji': '🟡'
            }

        actual = event['actual']
        expected = event.get('expected')
        previous = event.get('previous')
        name = event.get('name', '')

        # 根据数据类型判断
        return self._analyze_by_indicator_type(name, actual, expected, previous)

    def _analyze_by_indicator_type(self, name: str, actual: str,
                                     expected: Optional[str],
                                     previous: Optional[str]) -> Dict:
        """根据指标类型分析"""

        # 解析数值
        actual_val = self._parse_value(actual)
        expected_val = self._parse_value(expected) if expected else None
        previous_val = self._parse_value(previous) if previous else None

        # 利多指标（数值越大越好）
        bullish_indicators = [
            '非农', 'NFP', '就业', 'GDP', '零售', 'ADP',
            '制造业PMI', '服务业PMI', 'PMI', '零售销售'
        ]

        # 利空指标（数值越小越好，如通胀、失业率）
        bearish_indicators = [
            'CPI', '通胀', 'PPI', '物价',
            '失业率', '利率', 'FOMC', '美联储'
        ]

        name_upper = name.upper()

        # 判断指标类型
        is_bullish_type = any(kw in name_upper for kw in bullish_indicators)
        is_bearish_type = any(kw in name_upper for kw in bearish_indicators)

        if is_bullish_type:
            return self._analyze_bullish_indicator(
                actual_val, expected_val, previous_val, name
            )
        elif is_bearish_type:
            return self._analyze_bearish_indicator(
                actual_val, expected_val, previous_val, name
            )
        else:
            return self._analyze_neutral(
                actual_val, expected_val, previous_val, name
            )

    def _analyze_bullish_indicator(self, actual: Optional[float],
                                    expected: Optional[float],
                                    previous: Optional[float],
                                    name: str) -> Dict:
        """
        分析利多型指标（数值越大越好）
        例如：非农、GDP、PMI
        """
        if actual is None or expected is None:
            return {
                'direction': 'neutral',
                'strength': 'weak',
                'reason': '数据不完整',
                'emoji': '🟡'
            }

        # 计算偏差百分比
        diff_pct = ((actual - expected) / expected * 100) if expected != 0 else 0

        if diff_pct > 2:
            direction = 'bullish'
            strength = 'strong'
            emoji = '🟢'
            reason = f"实际值 {self._format_value(actual, expected)} 高于预期 {diff_pct:+.1f}%，经济强劲"

        elif diff_pct > 0:
            direction = 'bullish'
            strength = 'moderate'
            emoji = '🟢'
            reason = f"实际值 {self._format_value(actual, expected)} 略高于预期 {diff_pct:+.1f}%，经济表现良好"

        elif diff_pct > -2:
            direction = 'neutral'
            strength = 'weak'
            emoji = '🟡'
            reason = f"实际值 {self._format_value(actual, expected)} 接近预期 {diff_pct:+.1f}%，影响有限"

        else:
            direction = 'bearish'
            strength = 'strong'
            emoji = '🔴'
            reason = f"实际值 {self._format_value(actual, expected)} 低于预期 {diff_pct:+.1f}%，经济疲软"

        return {
            'direction': direction,
            'strength': strength,
            'reason': reason,
            'emoji': emoji,
            'diff_pct': diff_pct
        }

    def _analyze_bearish_indicator(self, actual: Optional[float],
                                     expected: Optional[float],
                                     previous: Optional[float],
                                     name: str) -> Dict:
        """
        分析利空型指标（数值越小越好）
        例如：CPI、PPI、失业率
        """
        if actual is None or expected is None:
            return {
                'direction': 'neutral',
                'strength': 'weak',
                'reason': '数据不完整',
                'emoji': '🟡'
            }

        # 计算偏差百分比
        diff_pct = ((actual - expected) / expected * 100) if expected != 0 else 0

        # 对于通胀、失业率，数值越低越利多
        if diff_pct < -2:
            direction = 'bullish'
            strength = 'strong'
            emoji = '🟢'
            reason = f"实际值 {self._format_value(actual, expected)} 低于预期 {diff_pct:+.1f}%，通胀/失业压力缓解"

        elif diff_pct < 0:
            direction = 'bullish'
            strength = 'moderate'
            emoji = '🟢'
            reason = f"实际值 {self._format_value(actual, expected)} 略低于预期 {diff_pct:+.1f}%，通胀/失业压力有所缓解"

        elif diff_pct < 2:
            direction = 'neutral'
            strength = 'weak'
            emoji = '🟡'
            reason = f"实际值 {self._format_value(actual, expected)} 接近预期 {diff_pct:+.1f}%，影响有限"

        else:
            direction = 'bearish'
            strength = 'strong'
            emoji = '🔴'
            reason = f"实际值 {self._format_value(actual, expected)} 高于预期 {diff_pct:+.1f}%，通胀/失业压力加大"

        return {
            'direction': direction,
            'strength': strength,
            'reason': reason,
            'emoji': emoji,
            'diff_pct': diff_pct
        }

    def _analyze_neutral(self, actual: Optional[float],
                         expected: Optional[float],
                         previous: Optional[float],
                         name: str) -> Dict:
        """分析中性指标"""
        if actual is None or expected is None:
            return {
                'direction': 'neutral',
                'strength': 'weak',
                'reason': '暂无法判断影响',
                'emoji': '🟡'
            }

        diff_pct = ((actual - expected) / expected * 100) if expected != 0 else 0

        if abs(diff_pct) > 2:
            direction = 'bullish' if diff_pct > 0 else 'bearish'
            strength = 'moderate'
            emoji = '🟢' if diff_pct > 0 else '🔴'
            reason = f"实际值 {self._format_value(actual, expected)} {diff_pct:+.1f}%，需关注后续影响"
        else:
            direction = 'neutral'
            strength = 'weak'
            emoji = '🟡'
            reason = f"实际值 {self._format_value(actual, expected)} 接近预期 {diff_pct:+.1f}%，影响有限"

        return {
            'direction': direction,
            'strength': strength,
            'reason': reason,
            'emoji': emoji,
            'diff_pct': diff_pct
        }

    def _parse_value(self, value_str: str) -> Optional[float]:
        """解析数值字符串"""
        if not value_str:
            return None

        # 移除非数字字符（保留数字、小数点、负号）
        cleaned = value_str.strip()
        cleaned = cleaned.replace('+', '').replace('%', '').replace('K', '000').replace('M', '000000').replace('B', '000000000')

        # 处理 "不变" 等特殊值
        if cleaned in ['不变', '维持不变', 'N/A', 'NA']:
            return None

        try:
            return float(cleaned)
        except ValueError:
            return None

    def _format_value(self, actual: float, expected: Optional[float]) -> str:
        """格式化数值显示"""
        if expected is None:
            return f"{actual:.2f}"

        diff = actual - expected
        diff_pct = (diff / expected * 100) if expected != 0 else 0

        # 根据数值大小选择格式
        if abs(actual) >= 1000:
            return f"{actual:,.0f}"
        elif abs(actual) >= 1:
            return f"{actual:.2f}"
        else:
            return f"{actual:.2f}%"

    def load_actual_data(self) -> Dict:
        """加载实际值数据"""
        try:
            if os.path.exists(self.actual_data_file):
                with open(self.actual_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载实际值数据失败: {e}")
        return {}

    def save_actual_data(self, data: Dict):
        """保存实际值数据"""
        try:
            with open(self.actual_data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ 实际值数据已保存")
        except Exception as e:
            print(f"❌ 保存实际值数据失败: {e}")

    def update_actual_value(self, name: str, actual: str, datetime_str: str = None):
        """
        更新经济数据的实际值

        Args:
            name: 数据名称（如"CPI 消费者价格指数"）
            actual: 实际值（如"2.3%"）
            datetime_str: 数据发布时间（如"2026-03-13 21:30"）
        """
        if datetime_str is None:
            datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        data = self.load_actual_data()
        data[name] = {
            'actual': actual,
            'datetime': datetime_str,
            'updated_at': datetime.now().isoformat()
        }
        self.save_actual_data(data)
        print(f"✅ 已更新 {name} 的实际值: {actual}")

    def generate_impact_report(self, event: Dict) -> str:
        """生成影响分析报告"""
        analysis = self.analyze_impact(event)

        lines = []
        lines.append(f"**{analysis['emoji']} {event.get('name', '')}**")
        lines.append("")

        # 显示数值
        if 'actual' in event:
            lines.append(f"📊 实际值: **{event['actual']}**")
            lines.append(f"📌 预期值: {event.get('expected', 'N/A')}")
            lines.append(f"📌 前值: {event.get('previous', 'N/A')}")
            lines.append("")

        # 显示分析
        lines.append(f"**市场影响**: {analysis['emoji']} {self._get_direction_text(analysis['direction'])}")
        lines.append(f"**影响强度**: {self._get_strength_text(analysis['strength'])}")
        lines.append(f"**分析**: {analysis['reason']}")
        lines.append("")

        # 显示建议
        if analysis['direction'] == 'bullish':
            lines.append(f"💡 **建议**: {analysis['emoji']} 利多数据，市场情绪可能偏向积极")
        elif analysis['direction'] == 'bearish':
            lines.append(f"⚠️ **建议**: {analysis['emoji']} 利空数据，市场波动可能增加")
        else:
            lines.append(f"📊 **建议**: {analysis['emoji']} 中性数据，市场反应可能有限")

        return "\n".join(lines)

    def _get_direction_text(self, direction: str) -> str:
        """获取方向文本"""
        texts = {
            'bullish': '利多 🟢',
            'bearish': '利空 🔴',
            'neutral': '中性 🟡'
        }
        return texts.get(direction, '未知')

    def _get_strength_text(self, strength: str) -> str:
        """获取强度文本"""
        texts = {
            'strong': '强 💪',
            'moderate': '中等 ⚖️',
            'weak': '弱 📊'
        }
        return texts.get(strength, '未知')


def main():
    """测试分析器"""
    analyzer = EconomicDataAnalyzer()

    print("🔍 经济数据分析器测试\n")
    print("=" * 80)
    print()

    # 测试案例 1：非农（利多型，高于预期）
    event1 = {
        'name': '非农就业数据 (NFP)',
        'actual': '+280K',
        'expected': '+200K',
        'previous': '+256K',
        'country': '美国'
    }
    print("【测试案例 1】非农就业数据")
    print(analyzer.generate_impact_report(event1))
    print("=" * 80)
    print()

    # 测试案例 2：CPI（利空型，低于预期）
    event2 = {
        'name': 'CPI 消费者价格指数',
        'actual': '2.1%',
        'expected': '2.3%',
        'previous': '2.4%',
        'country': '美国'
    }
    print("【测试案例 2】CPI 通胀数据")
    print(analyzer.generate_impact_report(event2))
    print("=" * 80)
    print()

    # 测试案例 3：GDP（利多型，低于预期）
    event3 = {
        'name': 'GDP 季度报告',
        'actual': '1.8%',
        'expected': '2.0%',
        'previous': '1.6%',
        'country': '美国'
    }
    print("【测试案例 3】GDP 增长数据")
    print(analyzer.generate_impact_report(event3))
    print("=" * 80)
    print()

    # 测试案例 4：失业率（利空型，高于预期）
    event4 = {
        'name': '失业率',
        'actual': '4.0%',
        'expected': '3.8%',
        'previous': '3.7%',
        'country': '美国'
    }
    print("【测试案例 4】失业率数据")
    print(analyzer.generate_impact_report(event4))
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
