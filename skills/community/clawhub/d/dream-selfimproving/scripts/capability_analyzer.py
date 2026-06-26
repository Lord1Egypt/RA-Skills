#!/usr/bin/env python3
"""
Capability Evolver Python Wrapper
集成到梦境技能的日志分析器
"""

import json
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

# ─── Types ───────────────────────────────────────────────────

class LogEntry:
    def __init__(self, timestamp: str, level: str, message: str, context: str = None, stack: str = None):
        self.timestamp = timestamp
        self.level = level
        self.message = message
        self.context = context
        self.stack = stack

class PatternEntry:
    def __init__(self, type_: str, severity: str, description: str, occurrences: int,
                 first_seen: str, last_seen: str, affected_files: List[str]):
        self.type = type_
        self.severity = severity
        self.description = description
        self.occurrences = occurrences
        self.first_seen = first_seen
        self.last_seen = last_seen
        self.affected_files = affected_files

# ─── Analyze Engine ─────────────────────────────────────────

def handle_analyze(logs: List[Dict]) -> Dict:
    """分析日志，返回模式、健康评分、建议"""
    patterns: List[PatternEntry] = []
    error_map: Dict[str, Dict] = {}
    
    # 模式检测
    for log in logs:
        level = log.get('level', 'info')
        message = log.get('message', '')[:100]
        context = log.get('context', '')
        timestamp = log.get('timestamp', '')
        
        if level in ('error', 'warn'):
            key = f"{message}|{context}"
            if key not in error_map:
                error_map[key] = {
                    'count': 0,
                    'first': timestamp,
                    'last': timestamp,
                    'message': message,
                    'context': context
                }
            else:
                error_map[key]['count'] += 1
                error_map[key]['last'] = timestamp
    
    # 构建模式
    for key, data in error_map.items():
        count = data['count']
        severity = 'critical' if count >= 10 else 'high' if count >= 5 else 'medium' if count >= 2 else 'low'
        pattern_type = 'regression' if count >= 3 else 'error'
        
        patterns.append(PatternEntry(
            type_=pattern_type,
            severity=severity,
            description=data['message'],
            occurrences=count,
            first_seen=data['first'],
            last_seen=data['last'],
            affected_files=[data['context']] if data['context'] else []
        ))
    
    # 检测效率问题
    slow_ops = [l for l in logs if l.get('level') == 'info' and re.search(r'(\d{4,})ms|slow|timeout', l.get('message', ''), re.I)]
    if len(slow_ops) >= 2:
        patterns.append(PatternEntry(
            type_='inefficiency',
            severity='high' if len(slow_ops) >= 5 else 'medium',
            description=f'{len(slow_ops)} slow operations detected',
            occurrences=len(slow_ops),
            first_seen=slow_ops[0].get('timestamp', ''),
            last_seen=slow_ops[-1].get('timestamp', ''),
            affected_files=list(set([l.get('context', '') for l in slow_ops if l.get('context')]))
        ))
    
    # 计算健康评分
    total_logs = len(logs)
    error_count = sum(1 for l in logs if l.get('level') == 'error')
    warn_count = sum(1 for l in logs if l.get('level') == 'warn')
    health_score = max(0, round(
        100 - (error_count / max(total_logs, 1)) * 100 - (warn_count / max(total_logs, 1)) * 30
    ))
    
    critical_count = sum(1 for p in patterns if p.severity == 'critical')
    
    # 生成建议
    recommendations = []
    if critical_count > 0:
        recommendations.append('Critical patterns detected — prioritize immediate fixes')
    if sum(1 for p in patterns if p.type == 'regression') >= 2:
        recommendations.append('Multiple regressions found — consider "harden" strategy')
    if health_score > 80 and len(patterns) < 3:
        recommendations.append('System is healthy — safe to pursue "innovate" strategy')
    if health_score < 50:
        recommendations.append('Low health score — focus on stability before adding features')
    if any(p.type == 'inefficiency' for p in patterns):
        recommendations.append('Performance bottlenecks detected — profile slow operations')
    
    # 热文件分析
    hot_files = {}
    for p in patterns:
        for f in p.affected_files:
            hot_files[f] = hot_files.get(f, 0) + 1
    if hot_files:
        top_hot = sorted(hot_files.items(), key=lambda x: -x[1])[:3]
        recommendations.append(f'Hot files (most issues): {", ".join([f"{f}({c})" for f, c in top_hot])}')
    
    return {
        'patterns': [
            {
                'type': p.type,
                'severity': p.severity,
                'description': p.description,
                'occurrences': p.occurrences,
                'first_seen': p.first_seen,
                'last_seen': p.last_seen,
                'affected_files': p.affected_files
            } for p in sorted(patterns, key=lambda x: -x.occurrences)[:50]
        ],
        'health_score': health_score,
        'recommendations': recommendations,
        'summary': {
            'total_logs': total_logs,
            'error_count': error_count,
            'warn_count': warn_count,
            'unique_patterns': len(patterns),
            'critical_count': critical_count
        }
    }

def handle_evolve(logs: List[Dict], strategy: str = 'auto') -> Dict:
    """生成进化方案"""
    analysis = handle_analyze(logs)
    
    # 自动选择策略
    if strategy == 'auto':
        if analysis['health_score'] < 40:
            effective_strategy = 'repair-only'
        elif analysis['health_score'] < 70:
            effective_strategy = 'harden'
        else:
            effective_strategy = 'balanced'
    else:
        effective_strategy = strategy
    
    evolution_id = f"evo_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    recommendations = []
    for pattern in analysis['patterns']:
        affected = pattern.get('affected_files', [])
        desc = pattern.get('description', '')
        
        if pattern['severity'] == 'critical' or effective_strategy == 'repair-only':
            recommendations.append({
                'priority': 'immediate',
                'category': 'error-handling',
                'description': f"Fix: {desc}",
                'affected_files': affected,
                'suggested_approach': 'Add try-catch or input validation. Review error boundary coverage.'
            })
        
        if pattern['type'] == 'inefficiency' and effective_strategy != 'repair-only':
            recommendations.append({
                'priority': 'medium',
                'category': 'performance',
                'description': f"Optimize: {desc}",
                'affected_files': affected,
                'suggested_approach': 'Profile the slow path, add caching, or batch operations.'
            })
        
        if pattern['type'] == 'regression' and effective_strategy in ('harden', 'balanced'):
            recommendations.append({
                'priority': 'high',
                'category': 'stability',
                'description': f"Stabilize: {desc} ({pattern['occurrences']} occurrences)",
                'affected_files': affected,
                'suggested_approach': 'Write targeted tests. Add monitoring for early detection.'
            })
    
    if effective_strategy == 'innovate' and analysis['health_score'] > 70:
        recommendations.append({
            'priority': 'low',
            'category': 'architecture',
            'description': 'System is stable — consider adding new capabilities',
            'affected_files': [],
            'suggested_approach': 'Identify most-called code paths and optimize or extend.'
        })
    
    if effective_strategy == 'harden':
        all_files = list(set([f for p in analysis['patterns'] for f in p.get('affected_files', [])]))
        recommendations.append({
            'priority': 'high',
            'category': 'monitoring',
            'description': 'Add structured logging and health checks',
            'affected_files': all_files[:5],
            'suggested_approach': 'Add error rate metrics, latency tracking, automated alerting.'
        })
    
    critical_patterns = [p for p in analysis['patterns'] if p['severity'] == 'critical']
    risk_level = 'high' if len(critical_patterns) >= 3 else 'medium' if len(critical_patterns) >= 1 else 'low'
    
    return {
        'evolution_id': evolution_id,
        'strategy': effective_strategy,
        'recommendations': recommendations[:20],
        'risk_assessment': {
            'level': risk_level,
            'factors': [p['description'] for p in critical_patterns[:5]]
        },
        'estimated_improvement': f"Health score: {analysis['health_score']} → ~{min(100, analysis['health_score'] + len(recommendations) * 5)}"
    }

def handle_status() -> Dict:
    """返回状态"""
    return {
        'skill': 'capability-evolver-integrated',
        'version': '1.0.0',
        'mode': 'local',
        'engine': 'pure-logic',
        'supported_actions': ['analyze', 'evolve', 'status'],
        'supported_strategies': ['balanced', 'innovate', 'harden', 'repair-only', 'auto'],
        'integration': 'dream-selfimproving'
    }

def logs_to_analysis_format(log_file: Path) -> List[Dict]:
    """从梦境日志文件提取分析格式的日志"""
    logs = []
    if not log_file.exists():
        return logs
    
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    current_entry = None
    for line in content.split('\n'):
        if line.startswith('## ['):
            match = re.match(r'## \[(\d{2}:\d{2}:\d{2})\].*?\((weight=(\d+\.?\d*))', line)
            if match:
                timestamp_str = match.group(1)
                today = date.today().isoformat()
                timestamp = f"{today}T{timestamp_str}Z"
                
                if 'error' in line.lower():
                    level = 'error'
                elif 'correction' in line.lower() or 'warning' in line.lower():
                    level = 'warn'
                elif 'completed' in line.lower() or 'success' in line.lower():
                    level = 'info'
                else:
                    level = 'info'
                
                current_entry = {
                    'timestamp': timestamp,
                    'level': level,
                    'message': '',
                    'context': ''
                }
        elif current_entry and line.strip() and not line.startswith('#'):
            current_entry['message'] += line.strip() + ' '
        elif line.strip() == '' and current_entry:
            current_entry['message'] = current_entry['message'].strip()
            if current_entry['message']:
                logs.append(current_entry)
            current_entry = None
    
    return logs

def run_from_hippocampus_logs(date_str: str = None) -> Dict:
    """从hippocampus日志运行分析"""
    if date_str is None:
        date_str = date.today().isoformat()
    
    year, month, day = date_str.split('-')
    log_file = Path.home() / '.openclaw' / 'workspace' / 'memory' / 'logs' / year / month / f"{date_str}.md"
    
    logs = logs_to_analysis_format(log_file)
    
    if not logs:
        return {
            'status': 'no_logs',
            'date': date_str,
            'message': f'No logs found for {date_str}'
        }
    
    analysis = handle_analyze(logs)
    evolution = handle_evolve(logs)
    
    return {
        'status': 'success',
        'date': date_str,
        'analysis': analysis,
        'evolution': evolution,
        'log_count': len(logs)
    }

# ─── CLI Entry ──────────────────────────────────────────────

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Capability Evolver - 日志分析引擎')
    parser.add_argument('action', choices=['analyze', 'evolve', 'status', 'run'], 
                        help='操作类型')
    parser.add_argument('--logs', type=str, help='JSON格式的日志数组文件')
    parser.add_argument('--date', type=str, help='日期 (YYYY-MM-DD)，用于run模式')
    parser.add_argument('--strategy', type=str, default='auto', 
                        choices=['auto', 'balanced', 'harden', 'innovate', 'repair-only'])
    
    args = parser.parse_args()
    
    if args.action == 'status':
        print(json.dumps(handle_status(), indent=2, ensure_ascii=False))
    
    elif args.action == 'analyze':
        if args.logs:
            with open(args.logs, 'r') as f:
                logs = json.load(f)
            result = handle_analyze(logs)
            print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.action == 'evolve':
        if args.logs:
            with open(args.logs, 'r') as f:
                logs = json.load(f)
            result = handle_evolve(logs, args.strategy)
            print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.action == 'run':
        result = run_from_hippocampus_logs(args.date)
        print(json.dumps(result, indent=2, ensure_ascii=False))
