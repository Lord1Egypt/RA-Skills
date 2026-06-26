#!/usr/bin/env python3
"""
analyze_cycle.py - 7 天周期分析与智能进化规划

功能:
- 读取完整一周（7 天）的交互记录
- 统计完成率趋势、能量模式识别、障碍类型分布
- 生成第{{cycle_number+1}}周期的优化计划建议
"""

import sys
import os
from datetime import datetime, timedelta
import re
from collections import defaultdict
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from config import CURRENT_SKILL_PATH, NOTE_BASE_DIR, DAILY_RECORDER_SUBDIR
STATE_FILE = os.path.join(CURRENT_SKILL_PATH, "state.json")

def get_weekday_from_date(d):
    """获取周 Day (周一=1, 周日=7)"""
    return d.weekday() + 1 if d.weekday() != 0 else 7

def find_cycle_notes():
    """查找最近 7 天交互记录"""
    
    today = datetime.now().date()
    notes_dir = os.path.join(NOTE_BASE_DIR, DAILY_RECORDER_SUBDIR)
    
    if not os.path.exists(notes_dir):
        return []
    
    # 按日期范围筛选（前 7 天 + 今日，新命名规范：YYYY-MM-DD-day_N.md）
    matching_files = [f for f in os.listdir(notes_dir) 
                      if '-day_' in f and f.startswith((today - timedelta(days=6)).strftime('%Y-%m-%d'))]
    
    notes_content = []
    for filename in sorted(matching_files):  # 按文件名排序（日期顺序）
        note_path = os.path.join(notes_dir, filename)
        with open(note_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        notes_content.append({
            'filename': filename,
            'content': content,
            'date': datetime.strptime(filename[:10], '%Y-%m-%d').date(),
            'weekday_num': get_weekday_from_date(datetime.strptime(filename[:10], '%Y-%m-%d'))
        })
    
    return notes_content

def extract_cycle_metrics(notes):
    """提取完整周期指标"""
    
    metrics = {
        'completion_rates_by_day': {},
        'energy_scores_by_day': {},
        'barriers_by_type': defaultdict(list),
        'plan_deviations_by_day': {}
    }
    
    for note in notes:
        date_str = note['date'].strftime('%Y-%m-%d')
        
        # 完成率
        completion_rates = re.findall(r'\[\s*([0-9]+)\s*\%\]', note['content'])
        metrics['completion_rates_by_day'][date_str] = [int(c) for c in completion_rates[:3]] if completion_rates else []
        
        # 能量评分
        energy_match = re.search(r'总体评分.*?:\s*\[\s*([1-5])', note['content'])
        metrics['energy_scores_by_day'][date_str] = int(energy_match.group(1)) if energy_match else None
        
        # 问题点分类统计（简化版：基于关键词识别）
        barrier_keywords = {
            '技术阻碍': ['AI', '生成质量', '工具故障', '流程错误'],
            '时间分配': ['耗时增加', '预估差异', '多任务冲突'],
            '疲劳累积': ['疲惫', '累', '效率下降'],
            '计划偏差': ['未完成', '推迟', '跳过']
        }
        
        for barrier_line in note['content'].split('\n'):
            if barrier_line.strip().startswith('-') and '待记录' not in barrier_line:
                # 分类识别
                for b_type, keywords in barrier_keywords.items():
                    if any(kw in barrier_line for kw in keywords):
                        metrics['barriers_by_type'][b_type].append({
                            'date': date_str,
                            'description': barrier_line.strip()[2:]  # 去除 '- '前缀
                        })
                        break
    
    return metrics

def identify_patterns_from_metrics(metrics):
    """基于数据识别模式"""
    
    patterns = {
        'task_adaptation': [],  # 任务 - 能量适配推荐列表
        'best_start_window': None,  # 最佳开始时间窗建议
        'risk_alerts': []  # 风险预警列表
    }
    
    # A. 计算各周 Day 平均能量 -> 识别高效时段
    energy_by_weekday = defaultdict(list)
    for date_str, score in metrics['energy_scores_by_day'].items():
        if score:
            # 根据 filename 提取 weekday（简化：直接按日期顺序推断）
            pass
    
    # B. 基于完成率统计识别高适配任务类型
    avg_completion = {}
    for date_str, rates in metrics['completion_rates_by_day'].items():
        if rates and len(rates) >= 2:
            avg_completion[date_str] = sum(rates[:2]) / 2
    
    # C. 障碍模式识别 -> 生成风险预警
    for b_type, barrier_list in metrics['barriers_by_type'].items():
        if len(barrier_list) >= 3:
            patterns['risk_alerts'].append({
                'barrier_type': b_type,
                'probability': f"[[ {len(barrier_list)/7 * 100:.0f} ]]%",
                'strategy': "预案建议：提前准备替代方案 / 调整时间分配 / 降低强度"
            })
    
    return patterns

def generate_cycle_summary_report(metrics, patterns):
    """生成周期总结报告"""
    
    report = {
        'summary_section': [],
        'pattern_recognition': [],
        'next_cycle_recommendations': []
    }
    
    # 汇总统计
    avg_completion = sum(sum(v) for v in metrics['completion_rates_by_day'].values()) / len(metrics['completion_rates_by_day']) if metrics['completion_rates_by_day'] else None
    avg_energy = sum(v for v in metrics['energy_scores_by_day'].values() if v) / len([v for v in metrics['energy_scores_by_day'].values() if v]) if any(metrics['energy_scores_by_day'].values()) else None
    
    report['summary_section'] = [
        f"本周期平均完成率：[{avg_completion:.1f}%] ({'高完成度 ✓' if avg_completion and avg_completion >= 80 else '中等/低 ⚠️'})",
        f"本周期平均能量状态：[{avg_energy:.1f}] ({['极累','疲惫','正常','充沛','满电'][int(avg_energy)-1] if avg_energy else '待分析'})",
    ]
    
    # 模式识别汇总
    report['pattern_recognition'] = [
        f"主要障碍类型分布：{[(k, len(v)) for k,v in metrics['barriers_by_type'].items()]}]"
    ]
    
    if patterns.get('risk_alerts'):
        report['next_cycle_recommendations'].append({
            'type': '风险预警',
            'details': f"建议在第{{cycle_number+1}}周期预设预案应对：{[p['barrier_type'] for p in patterns['risk_alerts']]}"
        })
    
    return report

def print_report(report):
    """输出报告"""
    
    print("=" * 60)
    print("=== 周期总结与智能规划报告 ===")
    print("=" * 60)
    
    print("\n【本周期汇总】")
    for item in report['summary_section']:
        print(f"  {item}")
    
    print("\n【模式识别】")
    for item in report['pattern_recognition']:
        print(f"  {item}")
    
    print("\n【第{{cycle_number+1}}周期建议】")
    for rec in report['next_cycle_recommendations']:
        print(f"  - [{rec['type']}]: {rec['details']}")
    
    print("=" * 60)

def main():
    """主流程"""
    
    notes = find_cycle_notes()
    
    if len(notes) < 7:
        print("✗ 不足 7 天完整记录，无法进行周期分析")
        return
    
    metrics = extract_cycle_metrics(notes)
    patterns = identify_patterns_from_metrics(metrics)
    
    report = generate_cycle_summary_report(metrics, patterns)
    print_report(report)

if __name__ == "__main__":
    main()
