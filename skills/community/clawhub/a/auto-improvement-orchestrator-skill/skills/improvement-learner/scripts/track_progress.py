#!/usr/bin/env python3
"""
Skill Evaluator 能力演进追踪

用法:
    python track_progress.py --skill-path /path/to/skill --output reports/
    python track_progress.py --skill-path /path/to/skill --output reports/ --plot
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import logging

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Skill Evaluator 能力演进追踪")
    parser.add_argument("--skill-path", type=str, required=True, help="要追踪的 Skill 路径")
    parser.add_argument("--output", type=str, default="reports/", help="输出目录")
    parser.add_argument("--plot", action="store_true", help="生成可视化图表")
    parser.add_argument("--verbose", action="store_true", help="输出详细日志")
    return parser.parse_args()


def load_eval_history(skill_path: str) -> list:
    """加载评估历史"""
    reports_dir = Path(skill_path) / "reports"
    
    if not reports_dir.exists():
        logger.warning(f"未找到评估报告目录：{reports_dir}")
        return []
    
    history = []
    
    # 加载所有评估报告
    for report_file in sorted(reports_dir.glob("*.json")):
        try:
            with open(report_file, 'r', encoding='utf-8') as f:
                report = json.load(f)
                
            history.append({
                "timestamp": report.get("timestamp", report_file.stem),
                "accuracy": report.get("accuracy", 0),
                "reliability": report.get("reliability", 0),
                "efficiency": report.get("efficiency", 0),
                "cost": report.get("cost", 1),
                "coverage": report.get("coverage", 0),
                "skill_level": report.get("skill_level", "Unknown"),
            })
        except Exception as e:
            logger.warning(f"加载报告失败 {report_file}: {e}")
    
    logger.info(f"加载了 {len(history)} 条评估记录")
    return history


def calculate_trend(history: list, metric: str) -> str:
    """计算指标趋势"""
    if len(history) < 5:
        return "insufficient_data"
    
    values = [h.get(metric, 0) for h in history]
    
    recent = values[-5:]
    older = values[-10:-5] if len(values) >= 10 else values[:5]
    
    recent_avg = sum(recent) / len(recent)
    older_avg = sum(older) / len(older)
    
    if recent_avg > older_avg * 1.05:  # 5% 提升
        return "improving"
    elif recent_avg < older_avg * 0.95:  # 5% 下降
        return "declining"
    else:
        return "stable"


def plot_metric(history: list, metric: str, title: str, output_file: str):
    """绘制指标曲线"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except ImportError:
        logger.warning("matplotlib 未安装，跳过可视化")
        return
    
    # 提取数据
    timestamps = [h["timestamp"] for h in history]
    values = [h.get(metric, 0) for h in history]
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(timestamps, values, marker='o', linestyle='-', linewidth=2, markersize=6)
    ax.set_xlabel("时间")
    ax.set_ylabel(metric.capitalize())
    ax.set_title(f"{title} - {metric}")
    ax.grid(True, alpha=0.3)
    
    # 旋转 x 轴标签
    plt.xticks(rotation=45)
    
    # 添加趋势线
    import numpy as np
    z = np.polyfit(range(len(values)), values, 1)
    p = np.poly1d(z)
    ax.plot(timestamps, p(range(len(values))), "r--", alpha=0.5, label=f"Trend (y={z[0]:.2f}x+{z[1]:.2f})")
    ax.legend()
    
    # 保存图表
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    logger.info(f"图表已保存到：{output_file}")


def generate_suggestions(history: list, trends: dict) -> list:
    """生成改进建议"""
    suggestions = []
    
    for metric, trend in trends.items():
        if trend == "improving":
            suggestions.append(f"✅ {metric}: 正在改进，继续保持")
        elif trend == "stable":
            suggestions.append(f"⚠️ {metric}: 改进停滞，考虑调整策略")
        elif trend == "declining":
            suggestions.append(f"❌ {metric}: 性能下降，建议检查")
    
    # 总体建议
    improving_count = sum(1 for t in trends.values() if t == "improving")
    declining_count = sum(1 for t in trends.values() if t == "declining")
    
    if improving_count > len(trends) / 2:
        suggestions.append("\n🎉 总体趋势良好，大部分指标正在改进")
    elif declining_count > len(trends) / 2:
        suggestions.append("\n⚠️ 总体趋势不佳，建议回滚到最佳版本并重新评估")
    else:
        suggestions.append("\n📊 总体趋势稳定，部分指标需要关注")
    
    return suggestions


def track_skill_progress(skill_path: str, output_dir: str, plot: bool):
    """追踪 Skill 能力演进"""
    logger.info(f"开始追踪 Skill 进展：{skill_path}")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 加载评估历史
    history = load_eval_history(skill_path)
    
    if not history:
        logger.warning("没有评估历史，无法追踪")
        return
    
    # 计算各指标趋势
    metrics = ["accuracy", "reliability", "efficiency", "cost", "coverage"]
    trends = {}
    
    for metric in metrics:
        trends[metric] = calculate_trend(history, metric)
    
    # 生成改进建议
    suggestions = generate_suggestions(history, trends)
    
    # 生成报告
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_file = Path(output_dir) / f"skill-progress-report-{timestamp}.md"
    
    report = f"""# Skill 能力演进报告

**Skill 路径**: {skill_path}  
**报告时间**: {datetime.now().isoformat()}  
**评估记录数**: {len(history)}

---

## 总体趋势

| 指标 | 趋势 | 说明 |
|------|------|------|
"""
    
    trend_emoji = {
        "improving": "✅ 改进",
        "stable": "⚠️ 稳定",
        "declining": "❌ 下降",
        "insufficient_data": "➖ 数据不足",
    }
    
    for metric in metrics:
        trend = trends[metric]
        emoji = trend_emoji.get(trend, trend)
        report += f"| {metric.capitalize()} | {emoji} | {trend} |\n"
    
    report += f"""
---

## 评估历史

| 时间 | 准确性 | 可靠性 | 效率 | 成本 | 覆盖率 |
|------|--------|--------|------|------|--------|
"""
    
    for h in history[-10:]:  # 只显示最近 10 条
        report += f"| {h['timestamp']} | {h['accuracy']:.2%} | {h['reliability']:.2%} | {h['efficiency']:.2%} | {h['cost']:.2%} | {h['coverage']:.2%} |\n"
    
    report += f"""
---

## 改进建议

"""
    
    for suggestion in suggestions:
        report += f"{suggestion}\n"
    
    report += f"""
---

## 可视化

"""
    
    if plot:
        try:
            import numpy as np
            
            for metric in metrics:
                chart_file = Path(output_dir) / f"skill-progress-{metric}-{timestamp}.png"
                plot_metric(history, metric, f"{skill_path}", str(chart_file))
                report += f"![{metric}](skill-progress-{metric}-{timestamp}.png)\n\n"
        except ImportError:
            report += "*需要安装 matplotlib: `pip install matplotlib`*\n"
    else:
        report += "*使用 `--plot` 参数生成可视化图表*\n"
    
    report += f"""
---

*报告由 Skill Evaluator 能力演进追踪工具生成*
"""
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    logger.info(f"能力演进报告已保存到：{report_file}")
    
    # 打印摘要
    logger.info(f"\n{'='*50}")
    logger.info(f"Skill 能力演进追踪完成！")
    logger.info(f"评估记录数：{len(history)}")
    logger.info(f"改进趋势:")
    for metric, trend in trends.items():
        emoji = trend_emoji.get(trend, trend)
        logger.info(f"  {metric.capitalize()}: {emoji}")
    logger.info(f"报告：{report_file}")
    
    return report_file


def main():
    args = parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
    
    track_skill_progress(args.skill_path, args.output, args.plot)


if __name__ == "__main__":
    main()
