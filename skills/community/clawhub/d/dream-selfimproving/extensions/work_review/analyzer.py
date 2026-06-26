"""
WorkAnalyzer — 工作分析器
从对话日志中提取任务完成情况，分析未完成原因
"""

import re
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict


class WorkAnalyzer:
    """工作分析器"""
    
    # 任务相关关键词
    TASK_PATTERNS = [
        r'完成', r'做完', r'做好了', r'结束', r'搞定了',
        r'未完成', r'还没', r'没做完', r'待办', r'TODO',
        r'下一步', r'继续', r'还没做', r'稍后', r'之后',
        r'需要做', r'要做', r'要做的事', r'任务',
    ]
    
    # 完成标记
    COMPLETION_MARKERS = [
        '完成', '搞定', '做好', '结束了', 'done', '完成✅',
        '搞定了', '解决了', '好了', 'ok', 'OK', '✅',
    ]
    
    # 未完成标记
    INCOMPLETION_MARKERS = [
        '还没', '未完成', '没做完', '待办', 'TODO', '稍后',
        '之后', '需要做', '要做', '没做', '没完成', '继续',
    ]
    
    def __init__(self, log_entries: List[Dict]):
        """
        初始化分析器
        log_entries: 从 hippocampus 日志解析的条目列表
                     每条格式: {'time': str, 'type': str, 'content': str, 'high': bool}
        """
        self.entries = log_entries
        self.today = datetime.now().strftime('%Y-%m-%d')
    
    def analyze(self) -> Dict:
        """执行完整分析"""
        result = {
            'date': self.today,
            'total_entries': len(self.entries),
            'completed_tasks': [],
            'incomplete_tasks': [],
            'decisions': [],
            'corrections': [],
            'insights': [],
            'blockers': [],
            'summary': '',
        }
        
        for entry in self.entries:
            content = entry.get('content', '')
            entry_type = entry.get('type', 'normal')
            
            # 检测完成的任务
            if any(marker in content for marker in self.COMPLETION_MARKERS):
                result['completed_tasks'].append({
                    'content': content,
                    'time': entry.get('time', ''),
                    'type': entry_type
                })
            
            # 检测未完成的任务
            elif any(marker in content for marker in self.INCOMPLETION_MARKERS):
                result['incomplete_tasks'].append({
                    'content': content,
                    'time': entry.get('time', ''),
                    'type': entry_type,
                    'possible_reason': self._infer_reason(content)
                })
            
            # 记录决策
            if entry_type == 'decision':
                result['decisions'].append({
                    'content': content,
                    'time': entry.get('time', '')
                })
            
            # 记录纠正
            if entry_type == 'correction':
                result['corrections'].append({
                    'content': content,
                    'time': entry.get('time', '')
                })
            
            # 记录洞察
            if entry_type == 'insight':
                result['insights'].append({
                    'content': content,
                    'time': entry.get('time', '')
                })
        
        # 分析阻碍因素
        result['blockers'] = self._identify_blockers(result['incomplete_tasks'])
        
        # 生成总结
        result['summary'] = self._generate_summary(result)
        
        return result
    
    def _infer_reason(self, content: str) -> str:
        """推断未完成的原因"""
        reasons = []
        
        if any(w in content for w in ['时间', '来不及', '太久了']):
            reasons.append('时间不足')
        if any(w in content for w in ['复杂', '难', '不容易']):
            reasons.append('复杂度高')
        if any(w in content for w in ['等', '等待', '依赖']):
            reasons.append('等待外部条件')
        if any(w in content for w in ['忘记', '忘了']):
            reasons.append('遗忘')
        if any(w in content for w in ['不确定', '不知道']):
            reasons.append('信息不足')
        
        return '、'.join(reasons) if reasons else '未说明原因'
    
    def _identify_blockers(self, incomplete_tasks: List[Dict]) -> List[str]:
        """识别阻碍因素"""
        blockers = defaultdict(int)
        
        for task in incomplete_tasks:
            reason = task.get('possible_reason', '')
            if reason and reason != '未说明原因':
                blockers[reason] += 1
        
        return [f'{reason} ({count}次)' for reason, count in sorted(blockers.items(), key=lambda x: -x[1])]
    
    def _generate_summary(self, result: Dict) -> str:
        """生成分析总结"""
        completed = len(result['completed_tasks'])
        incomplete = len(result['incomplete_tasks'])
        total = completed + incomplete
        
        if total == 0:
            return "今日无明确任务记录，系统运转正常。"
        
        completion_rate = completed / total * 100 if total > 0 else 0
        
        parts = []
        parts.append(f"今日共识别 {total} 个任务事项")
        parts.append(f"完成 {completed} 个")
        parts.append(f"未完成 {incomplete} 个")
        parts.append(f"完成率约 {completion_rate:.0f}%")
        
        if result['blockers']:
            parts.append(f"主要阻碍：{'；'.join(result['blockers'][:2])}")
        
        return '，'.join(parts)
    
    def get_incomplete_task_details(self) -> str:
        """获取未完成任务的详细信息"""
        result = self.analyze()
        if not result['incomplete_tasks']:
            return "今日任务均已完成，无遗留事项。"
        
        lines = []
        lines.append(f"## 未完成任务 ({len(result['incomplete_tasks'])}项)\n")
        
        for i, task in enumerate(result['incomplete_tasks'][:5], 1):
            lines.append(f"{i}. {task['content']}")
            if task.get('possible_reason'):
                lines.append(f"   可能原因：{task['possible_reason']}")
            lines.append("")
        
        return '\n'.join(lines)
