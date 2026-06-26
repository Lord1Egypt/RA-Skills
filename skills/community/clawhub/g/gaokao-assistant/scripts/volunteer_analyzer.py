#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高考分数投档分析工具
用于计算位次、投档线分析、冲稳保志愿建议
"""

import json
from datetime import datetime


def calculate_equivalent_score(current_score, current_rank, year_data):
    """
    计算等效分
    
    参数:
        current_score: 当前年份分数
        current_rank: 当前年份位次
        year_data: 往年数据字典，格式：{year: {'score': 分数，'rank': 位次}}
    
    返回:
        等效分数
    """
    # 查找往年相同位次的分数
    min_diff = float('inf')
    equivalent_score = None
    
    for year, data in year_data.items():
        diff = abs(data['rank'] - current_rank)
        if diff < min_diff:
            min_diff = diff
            equivalent_score = data['score']
    
    return equivalent_score, min_diff


def calculate_line_difference(score, control_line):
    """
    计算线差
    
    参数:
        score: 考生分数
        control_line: 控制线（一本线/特控线）
    
    返回:
        线差
    """
    return score - control_line


def analyze_volunteer_strategy(score, rank, control_line, university_data):
    """
    分析冲稳保志愿策略
    
    参数:
        score: 考生分数
        rank: 考生位次
        control_line: 控制线
        university_data: 院校数据列表，格式：
            [
                {
                    'name': '院校名称',
                    'last_3_years': [
                        {'year': 2025, 'score': 645, 'rank': 900},
                        {'year': 2024, 'score': 638, 'rank': 980},
                        {'year': 2023, 'score': 642, 'rank': 950}
                    ]
                },
                ...
            ]
    
    返回:
        冲稳保建议列表
    """
    strategy = {
        '冲': [],
        '稳': [],
        '保': []
    }
    
    # 计算各院校近三年平均位次
    for uni in university_data:
        ranks = [y['rank'] for y in uni['last_3_years']]
        avg_rank = sum(ranks) / len(ranks)
        
        # 根据位次差分类
        rank_diff = avg_rank - rank
        
        if rank_diff > 0:
            # 院校位次高于自己，属于"冲"
            if rank_diff < 150:
                strategy['冲'].append({
                    'name': uni['name'],
                    'avg_rank': avg_rank,
                    'diff': rank_diff,
                    'probability': 'medium'
                })
            elif rank_diff < 300:
                strategy['冲'].append({
                    'name': uni['name'],
                    'avg_rank': avg_rank,
                    'diff': rank_diff,
                    'probability': 'low'
                })
        else:
            # 院校位次低于自己，属于"稳"或"保"
            if abs(rank_diff) < 200:
                strategy['稳'].append({
                    'name': uni['name'],
                    'avg_rank': avg_rank,
                    'diff': rank_diff,
                    'probability': 'high'
                })
            else:
                strategy['保'].append({
                    'name': uni['name'],
                    'avg_rank': avg_rank,
                    'diff': rank_diff,
                    'probability': 'very_high'
                })
    
    # 排序
    strategy['冲'].sort(key=lambda x: x['diff'])
    strategy['稳'].sort(key=lambda x: x['diff'], reverse=True)
    strategy['保'].sort(key=lambda x: x['diff'], reverse=True)
    
    return strategy


def generate_volunteer_report(current_score, current_rank, control_line, university_data):
    """
    生成志愿填报报告
    
    返回:
        报告字典
    """
    strategy = analyze_volunteer_strategy(
        current_score, current_rank, control_line, university_data
    )
    
    report = {
        '考生信息': {
            '分数': current_score,
            '位次': current_rank,
            '线差': calculate_line_difference(current_score, control_line)
        },
        '冲': strategy['冲'],
        '稳': strategy['稳'],
        '保': strategy['保'],
        '建议': []
    }
    
    # 生成建议
    if len(strategy['冲']) > 0:
        best_chong = strategy['冲'][0]
        report['建议'].append(f"冲刺：{best_chong['name']}（位次差{best_chong['diff']:.0f}，概率{best_chong['probability']}）")
    
    if len(strategy['稳']) > 0:
        best_wen = strategy['稳'][0]
        report['建议'].append(f"稳妥：{best_wen['name']}（位次差{abs(best_wen['diff']):.0f}，概率{best_wen['probability']}）")
    
    if len(strategy['保']) > 0:
        best_bao = strategy['保'][0]
        report['建议'].append(f"保底：{best_bao['name']}（位次差{abs(best_bao['diff']):.0f}，概率{best_bao['probability']}）")
    
    # 风险提示
    risks = []
    if len(strategy['保']) < 2:
        risks.append("⚠️  保底院校不足 2 所，建议增加保底志愿")
    if len(strategy['稳']) < 3:
        risks.append("⚠️  稳妥院校不足 3 所，建议增加稳妥志愿")
    if len(strategy['冲']) > 4:
        risks.append("⚠️  冲刺院校过多（>4 所），可能影响后续批次录取")
    
    if risks:
        report['风险提示'] = risks
    
    return report


def main():
    """示例演示"""
    
    # 考生信息
    score = 642
    rank = 1050
    control_line = 520  # 一本线
    
    # 院校数据示例
    universities = [
        {
            'name': '中山大学',
            'last_3_years': [
                {'year': 2025, 'score': 648, 'rank': 900},
                {'year': 2024, 'score': 635, 'rank': 1050},
                {'year': 2023, 'score': 640, 'rank': 1000}
            ]
        },
        {
            'name': '华南理工大学',
            'last_3_years': [
                {'year': 2025, 'score': 640, 'rank': 1100},
                {'year': 2024, 'score': 628, 'rank': 1200},
                {'year': 2023, 'score': 635, 'rank': 1150}
            ]
        },
        {
            'name': '暨南大学',
            'last_3_years': [
                {'year': 2025, 'score': 630, 'rank': 1300},
                {'year': 2024, 'score': 620, 'rank': 1400},
                {'year': 2023, 'score': 625, 'rank': 1350}
            ]
        },
        {
            'name': '深圳大学',
            'last_3_years': [
                {'year': 2025, 'score': 625, 'rank': 1400},
                {'year': 2024, 'score': 615, 'rank': 1500},
                {'year': 2023, 'score': 620, 'rank': 1450}
            ]
        }
    ]
    
    # 生成报告
    report = generate_volunteer_report(score, rank, control_line, universities)
    
    # 打印报告
    print("=" * 60)
    print("高考志愿填报分析报告")
    print("=" * 60)
    print(f"\n考生信息:")
    print(f"  分数：{report['考生信息']['分数']}")
    print(f"  位次：{report['考生信息']['位次']}")
    print(f"  线差：{report['考生信息']['线差']}")
    
    print(f"\n冲刺院校 ({len(report['冲'])}所):")
    for uni in report['冲']:
        print(f"  - {uni['name']} (位次差：{uni['diff']:.0f}, 概率：{uni['probability']})")
    
    print(f"\n稳妥院校 ({len(report['稳'])}所):")
    for uni in report['稳']:
        print(f"  - {uni['name']} (位次差：{abs(uni['diff']):.0f}, 概率：{uni['probability']})")
    
    print(f"\n保底院校 ({len(report['保'])}所):")
    for uni in report['保']:
        print(f"  - {uni['name']} (位次差：{abs(uni['diff']):.0f}, 概率：{uni['probability']})")
    
    if '建议' in report:
        print(f"\n填报建议:")
        for item in report['建议']:
            print(f"  ✓ {item}")
    
    if '风险提示' in report:
        print(f"\n风险提示:")
        for risk in report['风险提示']:
            print(f"  {risk}")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()
