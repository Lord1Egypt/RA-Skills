#!/usr/bin/env python3
"""
Architecture Health Check Script
架构健康度自动化扫描脚本

Usage:
    python health-check.py --system <system-name>
    python health-check.py --systems <system1,system2,system3>
    python health-check.py --system <system-name> --output report.md
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

# 配置
DEFAULT_THRESHOLDS = {
    'cyclomatic_complexity': {'healthy': 15, 'warning': 30},
    'code_duplication': {'healthy': 5, 'warning': 10},
    'lines_per_class': {'healthy': 500, 'warning': 1000},
    'lines_per_method': {'healthy': 50, 'warning': 100},
    'test_coverage': {'healthy': 80, 'warning': 60},
    'downstream_count': {'healthy': 5, 'warning': 10},
    'upstream_count': {'healthy': 10, 'warning': 20},
    'circular_dependency': {'healthy': 0, 'warning': 0},
    'cross_layer_call': {'healthy': 0, 'warning': 0},
    'code_violations': {'healthy': 10, 'warning': 50},
    'security_vulnerabilities': {'healthy': 0, 'warning': 3},
    'deployment_frequency': {'healthy': 1, 'warning': 0.14},  # per day
    'change_failure_rate': {'healthy': 5, 'warning': 15},
    'incident_count': {'healthy': 0, 'warning': 2},
    'technical_debt': {'healthy': 5, 'warning': 15},
}

WEIGHTS = {
    'structure_quality': 0.30,
    'dependency': 0.25,
    'technical_standard': 0.20,
    'evolvability': 0.15,
    'risk_exposure': 0.10,
    'governance_compliance': 0.10,
}

METRIC_DIMENSIONS = {
    'cyclomatic_complexity': 'structure_quality',
    'code_duplication': 'structure_quality',
    'lines_per_class': 'structure_quality',
    'lines_per_method': 'structure_quality',
    'test_coverage': 'structure_quality',
    'downstream_count': 'dependency',
    'upstream_count': 'dependency',
    'circular_dependency': 'dependency',
    'cross_layer_call': 'dependency',
    'code_violations': 'technical_standard',
    'security_vulnerabilities': 'technical_standard',
    'documentation_completeness': 'technical_standard',
    'api_compliance': 'technical_standard',
    'deployment_frequency': 'evolvability',
    'change_failure_rate': 'evolvability',
    'config_externalization': 'evolvability',
    'incident_count': 'risk_exposure',
    'technical_debt': 'risk_exposure',
    'single_point_failure': 'risk_exposure',
    'review_pass_rate': 'governance_compliance',
    'task_completion_rate': 'governance_compliance',
}


def calculate_score(value: float, thresholds: Dict, higher_is_better: bool = True) -> int:
    """
    计算单项指标得分
    
    Args:
        value: 实际值
        thresholds: 阈值配置 (healthy, warning)
        higher_is_better: 值越大越好 (如测试覆盖率)
    
    Returns:
        得分 (0-100)
    """
    healthy = thresholds['healthy']
    warning = thresholds['warning']
    
    if higher_is_better:
        if value >= healthy:
            return 100
        elif value >= warning:
            # 警告区间线性插值
            ratio = (value - warning) / (healthy - warning)
            return int(75 + ratio * 25)
        else:
            # 危险区间
            ratio = min(value / warning, 1.0) if warning > 0 else 0
            return int(ratio * 75)
    else:
        if value <= healthy:
            return 100
        elif value <= warning:
            # 警告区间
            ratio = (warning - value) / (warning - healthy)
            return int(75 + ratio * 25)
        else:
            # 危险区间，值越大得分越低
            ratio = max(0, 1 - (value - warning) / warning)
            return int(ratio * 75)


def collect_metrics(system_name: str) -> Dict[str, float]:
    """
    采集系统指标
    
    实际使用时需要集成：
    - SonarQube API
    - 服务注册中心
    - CI/CD 系统
    - 故障系统
    等
    
    这里提供模拟数据用于演示
    """
    print(f"📊 采集系统 [{system_name}] 指标...")
    
    # TODO: 实现真实的指标采集
    # 以下是模拟数据
    metrics = {
        'cyclomatic_complexity': 25.0,
        'code_duplication': 8.0,
        'lines_per_class': 450.0,
        'lines_per_method': 45.0,
        'test_coverage': 72.0,
        'downstream_count': 8.0,
        'upstream_count': 15.0,
        'circular_dependency': 1.0,
        'cross_layer_call': 0.0,
        'code_violations': 23.0,
        'security_vulnerabilities': 2.0,
        'documentation_completeness': 85.0,
        'api_compliance': 92.0,
        'deployment_frequency': 0.5,  # 每周 3-4 次
        'change_failure_rate': 8.0,
        'config_externalization': 90.0,
        'incident_count': 1.0,
        'technical_debt': 8.0,
        'single_point_failure': 1.0,
        'review_pass_rate': 95.0,
        'task_completion_rate': 88.0,
    }
    
    print(f"✅ 采集完成，共 {len(metrics)} 项指标")
    return metrics


def calculate_dimension_scores(metrics: Dict[str, float]) -> Dict[str, Dict]:
    """
    计算各维度得分
    """
    dimension_metrics = {}
    
    # 按维度分组指标
    for metric, value in metrics.items():
        dimension = METRIC_DIMENSIONS.get(metric)
        if dimension:
            if dimension not in dimension_metrics:
                dimension_metrics[dimension] = []
            dimension_metrics[dimension].append((metric, value))
    
    # 计算各维度得分
    dimension_scores = {}
    for dimension, metric_list in dimension_metrics.items():
        scores = []
        for metric, value in metric_list:
            thresholds = DEFAULT_THRESHOLDS.get(metric, {'healthy': 100, 'warning': 50})
            higher_is_better = metric not in [
                'cyclomatic_complexity', 'code_duplication', 'lines_per_class',
                'lines_per_method', 'downstream_count', 'upstream_count',
                'circular_dependency', 'cross_layer_call', 'code_violations',
                'security_vulnerabilities', 'change_failure_rate', 'incident_count',
                'technical_debt', 'single_point_failure'
            ]
            score = calculate_score(value, thresholds, higher_is_better)
            scores.append(score)
        
        avg_score = sum(scores) / len(scores) if scores else 0
        dimension_scores[dimension] = {
            'score': avg_score,
            'metrics': len(scores),
            'details': [(m, v, calculate_score(v, DEFAULT_THRESHOLDS.get(m, {'healthy': 100, 'warning': 50}), 
                         m not in ['cyclomatic_complexity', 'code_duplication', 'lines_per_class', 'lines_per_method',
                                   'downstream_count', 'upstream_count', 'circular_dependency', 'cross_layer_call',
                                   'code_violations', 'security_vulnerabilities', 'change_failure_rate', 
                                   'incident_count', 'technical_debt', 'single_point_failure'])) 
                       for m, v in metric_list]
        }
    
    return dimension_scores


def calculate_health_score(dimension_scores: Dict[str, Dict]) -> int:
    """
    计算系统健康度总分
    """
    total_score = 0
    for dimension, data in dimension_scores.items():
        weight = WEIGHTS.get(dimension, 0.1)
        total_score += data['score'] * weight
    
    return int(total_score)


def get_health_level(score: int) -> tuple:
    """
    获取健康度等级
    """
    if score >= 90:
        return '优秀', '🟢'
    elif score >= 75:
        return '良好', '🟡'
    elif score >= 60:
        return '一般', '🟠'
    elif score >= 40:
        return '风险', '🔴'
    else:
        return '严重', '⚫'


def generate_report(system_name: str, metrics: Dict, dimension_scores: Dict, 
                   health_score: int, output_file: Optional[str] = None) -> str:
    """
    生成健康度报告
    """
    level, icon = get_health_level(health_score)
    
    report = f"""# 系统架构健康度报告

**系统**: {system_name}
**评估日期**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**健康度**: {health_score}/100 {icon} {level}

---

## 维度得分

| 维度 | 权重 | 得分 | 状态 |
|------|------|------|------|
"""
    
    for dimension, data in sorted(dimension_scores.items(), 
                                  key=lambda x: WEIGHTS.get(x[0], 0), 
                                  reverse=True):
        weight = WEIGHTS.get(dimension, 0) * 100
        score = int(data['score'])
        dim_level, dim_icon = get_health_level(score)
        report += f"| {dimension} | {weight:.0f}% | {score} | {dim_icon} |\n"
    
    report += f"""
## 关键指标

"""
    
    # 列出需要关注的指标
    issues = []
    for dimension, data in dimension_scores.items():
        for metric, value, score in data['details']:
            if score < 75:
                issues.append((metric, value, score))
    
    if issues:
        report += "| 指标 | 值 | 得分 | 状态 |\n"
        report += "|------|-----|------|------|\n"
        for metric, value, score in sorted(issues, key=lambda x: x[2])[:10]:
            level = "🔴" if score < 50 else "🟠"
            report += f"| {metric} | {value} | {score} | {level} |\n"
    else:
        report += "✅ 所有指标均在健康范围内\n"
    
    report += f"""
## 治理建议

"""
    
    if health_score >= 90:
        report += "🟢 系统架构健康度优秀，建议：\n"
        report += "- 保持当前架构实践\n"
        report += "- 总结最佳实践并分享\n"
        report += "- 持续监控关键指标\n"
    elif health_score >= 75:
        report += "🟡 系统架构健康度良好，建议：\n"
        report += "- 关注得分较低的维度\n"
        report += "- 制定持续改进计划\n"
        report += "- 定期复查关键指标\n"
    elif health_score >= 60:
        report += "🟠 系统架构健康度一般，建议：\n"
        report += "- 制定专项改进计划\n"
        report += "- 优先处理高风险问题\n"
        report += "- 增加架构评审频率\n"
    else:
        report += "🔴 系统架构健康度风险较高，建议：\n"
        report += "- **立即启动治理专项**\n"
        report += "- 限制新功能开发，优先还债\n"
        report += "- 每周跟踪治理进展\n"
        report += "- 必要时进行架构重构\n"
    
    report += f"""
---

*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"📄 报告已保存至：{output_file}")
    
    return report


def main():
    parser = argparse.ArgumentParser(description='架构健康度扫描脚本')
    parser.add_argument('--system', type=str, help='系统名称')
    parser.add_argument('--systems', type=str, help='多个系统名称，逗号分隔')
    parser.add_argument('--output', type=str, help='输出报告文件路径')
    
    args = parser.parse_args()
    
    if not args.system and not args.systems:
        parser.print_help()
        sys.exit(1)
    
    systems = []
    if args.system:
        systems = [args.system]
    elif args.systems:
        systems = [s.strip() for s in args.systems.split(',')]
    
    print(f"🚀 开始架构健康度扫描")
    print(f"📋 系统列表：{', '.join(systems)}\n")
    
    all_reports = []
    
    for system in systems:
        print(f"\n{'='*60}")
        metrics = collect_metrics(system)
        dimension_scores = calculate_dimension_scores(metrics)
        health_score = calculate_health_score(dimension_scores)
        level, icon = get_health_level(health_score)
        
        print(f"\n📊 {system} 健康度：{health_score}/100 {icon} {level}")
        
        report = generate_report(system, metrics, dimension_scores, health_score)
        all_reports.append(report)
    
    # 如果是单个系统且指定了输出文件
    if len(systems) == 1 and args.output:
        generate_report(systems[0], metrics, dimension_scores, health_score, args.output)
    
    print(f"\n{'='*60}")
    print("✅ 扫描完成")


if __name__ == '__main__':
    main()
