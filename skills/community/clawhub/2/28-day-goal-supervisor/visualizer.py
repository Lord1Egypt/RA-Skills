"""
Habit Tracker - 可视化模块
支持 SVG 和文本（emoji）两种输出模式
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Habit


class HabitVisualizer:
    """习惯可视化生成器"""

    # ============ 文本模式（emoji，跨端兼容）============

    def generate_text(self, habits: list["Habit"]) -> str:
        """生成 emoji 文本可视化"""
        if not habits:
            return "📭 暂无习惯数据"

        lines = []
        today_str = datetime.now().strftime("%Y年%m月%d日")
        lines.append(f"📊 习惯追踪 - {today_str}")
        lines.append("")

        total_active = len(habits)
        checked_today = 0

        for h in habits:
            section = self._generate_habit_text(h)
            lines.append(section)
            lines.append("")

            # 检查今天是否已打卡
            today_checkin = h.get_checkin_for_day(h.current_day)
            if today_checkin:
                checked_today += 1

        # 总览
        lines.insert(1, f"✅ 今日进度：{checked_today}/{total_active} 个习惯已打卡")
        lines.insert(2, "")

        return "\n".join(lines)

    def _generate_habit_text(self, habit: "Habit") -> str:
        """生成单个习惯的文本可视化"""
        from models import HabitType, TaskStatus

        lines = []

        # 图标
        icon = "🔄" if habit.habit_type == HabitType.PROGRESSIVE.value else "✅"
        goal = habit.goal_refined or habit.goal_raw

        lines.append(f"{icon} {goal} (Day {habit.current_day}/{habit.total_days})")

        # 进度条
        rate = habit.stats.completion_rate
        bar = self._text_progress_bar(rate)
        lines.append(f"  进度: {bar} {int(rate * 100)}%")

        # 连续打卡
        streak_icon = "🔥" if habit.stats.current_streak > 0 else "💤"
        lines.append(f"  连续: {streak_icon} {habit.stats.current_streak}天 | 最长: {habit.stats.best_streak}天")

        # 最近打卡记录（最近 7 天）
        recent = self._recent_days_emoji(habit, days=7)
        lines.append(f"  最近: {recent}")

        # 今日任务
        today_task = habit.get_task_for_day(habit.current_day)
        today_checkin = habit.get_checkin_for_day(habit.current_day)

        if today_task:
            if today_checkin and today_checkin.tasks_result:
                status = today_checkin.tasks_result[0].status
                status_icon = {"completed": "✅", "partial": "🟡", "skipped": "⏭️", "missed": "❌"}.get(status, "⏳")
            else:
                status_icon = "⏳"
            lines.append(f"  今日: {today_task} {status_icon}")

        # 周趋势（如果有）
        if len(habit.stats.weekly_rates) >= 2:
            current = habit.stats.weekly_rates[-1]
            prev = habit.stats.weekly_rates[-2]
            change = current - prev
            arrow = "📈" if change > 0 else "📉" if change < 0 else "➡️"
            lines.append(f"  趋势: {arrow} 本周 {int(current * 100)}%（{'+' if change >= 0 else ''}{int(change * 100)}%）")

        return "\n".join(lines)

    def _text_progress_bar(self, rate: float, length: int = 10) -> str:
        """emoji 进度条"""
        filled = int(rate * length)
        return "█" * filled + "░" * (length - filled)

    def _recent_days_emoji(self, habit: "Habit", days: int = 7) -> str:
        """最近 N 天的 emoji 日历"""
        from models import TaskStatus

        emojis = []
        start_day = max(1, habit.current_day - days + 1)

        for d in range(start_day, habit.current_day + 1):
            ci = habit.get_checkin_for_day(d)
            if ci and ci.tasks_result:
                status = ci.tasks_result[0].status
                emoji = {
                    TaskStatus.COMPLETED.value: "✅",
                    TaskStatus.PARTIAL.value: "🟡",
                    TaskStatus.SKIPPED.value: "⬜",
                    TaskStatus.MISSED.value: "❌",
                }.get(status, "⬜")
            else:
                if d < habit.current_day:
                    emoji = "❌"  # 过去未打卡
                else:
                    emoji = "⏳"  # 今天还没打卡
            emojis.append(emoji)

        return "".join(emojis)

    # ============ SVG 模式 ============

    def generate_svg(self, habits: list["Habit"]) -> str:
        """生成 SVG 可视化（包含热力图 + 进度条 + 趋势图）"""
        if not habits:
            return self._svg_empty()

        sections = []
        y_offset = 60

        for h in habits:
            section, height = self._generate_habit_svg(h, y_offset)
            sections.append(section)
            y_offset += height + 30

        total_height = y_offset + 20
        today_str = datetime.now().strftime("%Y-%m-%d")

        svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 {total_height}" width="600" height="{total_height}">
  <style>
    .title {{ font: bold 18px sans-serif; fill: #1a1a2e; }}
    .subtitle {{ font: 12px sans-serif; fill: #666; }}
    .habit-name {{ font: bold 14px sans-serif; fill: #16213e; }}
    .stat-text {{ font: 12px sans-serif; fill: #555; }}
    .rate-text {{ font: bold 24px sans-serif; }}
    .day-cell {{ rx: 2; ry: 2; }}
  </style>

  <rect width="600" height="{total_height}" fill="#fafafa" rx="12"/>

  <text x="20" y="30" class="title">📊 习惯追踪报告</text>
  <text x="20" y="48" class="subtitle">{today_str}</text>

  {''.join(sections)}
</svg>"""
        return svg

    def _generate_habit_svg(self, habit: "Habit", y_start: int) -> tuple[str, int]:
        """生成单个习惯的 SVG 区块，返回 (svg_string, height)"""
        from models import HabitType, TaskStatus

        goal = habit.goal_refined or habit.goal_raw
        rate = habit.stats.completion_rate
        rate_color = self._rate_color(rate)

        parts = []

        # 背景卡片
        card_height = 140
        parts.append(
            f'<rect x="10" y="{y_start}" width="580" height="{card_height}" '
            f'fill="white" rx="8" stroke="#e0e0e0" stroke-width="1"/>'
        )

        # 习惯名称
        parts.append(
            f'<text x="20" y="{y_start + 22}" class="habit-name">'
            f'{self._escape_xml(goal)} (Day {habit.current_day}/{habit.total_days})</text>'
        )

        # 完成率大数字
        parts.append(
            f'<text x="500" y="{y_start + 35}" class="rate-text" fill="{rate_color}" text-anchor="end">'
            f'{int(rate * 100)}%</text>'
        )

        # 进度条
        bar_y = y_start + 38
        bar_width = 400
        filled_width = int(rate * bar_width)
        parts.append(f'<rect x="20" y="{bar_y}" width="{bar_width}" height="8" fill="#e8e8e8" rx="4"/>')
        if filled_width > 0:
            parts.append(f'<rect x="20" y="{bar_y}" width="{filled_width}" height="8" fill="{rate_color}" rx="4"/>')

        # 统计文字
        stat_y = bar_y + 22
        streak_text = f"🔥 连续 {habit.stats.current_streak} 天 | 最长 {habit.stats.best_streak} 天"
        parts.append(f'<text x="20" y="{stat_y}" class="stat-text">{streak_text}</text>')

        # 热力图（最近 28 天）
        heatmap_y = stat_y + 15
        heatmap = self._generate_heatmap_svg(habit, x_start=20, y_start=heatmap_y, days=28)
        parts.append(heatmap)

        # 周趋势迷你图
        if len(habit.stats.weekly_rates) >= 2:
            sparkline = self._generate_sparkline_svg(
                habit.stats.weekly_rates,
                x_start=440, y_start=y_start + 55,
                width=140, height=50,
            )
            parts.append(sparkline)

        return "\n  ".join(parts), card_height

    def _generate_heatmap_svg(
        self, habit: "Habit", x_start: int, y_start: int, days: int = 28
    ) -> str:
        """生成打卡热力图"""
        from models import TaskStatus

        cells = []
        cell_size = 14
        gap = 2
        cols = min(days, 28)

        start_day = max(1, habit.current_day - days + 1)

        for i, d in enumerate(range(start_day, start_day + cols)):
            ci = habit.get_checkin_for_day(d)
            if ci and ci.tasks_result:
                status = ci.tasks_result[0].status
                color = {
                    TaskStatus.COMPLETED.value: "#4caf50",
                    TaskStatus.PARTIAL.value: "#aed581",
                    TaskStatus.SKIPPED.value: "#e0e0e0",
                    TaskStatus.MISSED.value: "#ef9a9a",
                }.get(status, "#e0e0e0")
            else:
                if d < habit.current_day:
                    color = "#ef9a9a"  # 过去未打卡
                elif d == habit.current_day:
                    color = "#fff9c4"  # 今天待打卡
                else:
                    color = "#f5f5f5"  # 未来

            col = i % 14
            row = i // 14
            x = x_start + col * (cell_size + gap)
            y = y_start + row * (cell_size + gap)

            cells.append(
                f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" '
                f'fill="{color}" class="day-cell"/>'
            )

        return "\n    ".join(cells)

    def _generate_sparkline_svg(
        self, values: list[float],
        x_start: int, y_start: int,
        width: int = 140, height: int = 50,
    ) -> str:
        """生成迷你趋势折线图"""
        if not values or len(values) < 2:
            return ""

        max_val = max(values) if max(values) > 0 else 1
        n = len(values)
        step_x = width / max(n - 1, 1)

        points = []
        for i, v in enumerate(values):
            x = x_start + i * step_x
            y = y_start + height - (v / max_val) * height
            points.append(f"{x:.1f},{y:.1f}")

        polyline = f'<polyline points="{" ".join(points)}" fill="none" stroke="#42a5f5" stroke-width="2"/>'

        # 添加数据点
        dots = []
        for i, v in enumerate(values):
            x = x_start + i * step_x
            y = y_start + height - (v / max_val) * height
            color = "#42a5f5" if i < n - 1 else "#1565c0"
            r = 2 if i < n - 1 else 3
            dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}"/>')

        label = f'<text x="{x_start}" y="{y_start - 3}" class="stat-text" font-size="10">周趋势</text>'

        return "\n    ".join([label, polyline] + dots)

    def _rate_color(self, rate: float) -> str:
        """根据完成率返回颜色"""
        if rate >= 0.8:
            return "#4caf50"  # 绿色
        elif rate >= 0.6:
            return "#ff9800"  # 橙色
        elif rate >= 0.3:
            return "#ff5722"  # 红橙
        else:
            return "#f44336"  # 红色

    def _escape_xml(self, text: str) -> str:
        """XML 转义"""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    def _svg_empty(self) -> str:
        return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 100" width="600" height="100">
  <rect width="600" height="100" fill="#fafafa" rx="12"/>
  <text x="300" y="55" text-anchor="middle" font-size="14" fill="#999">暂无习惯数据</text>
</svg>"""
