#!/usr/bin/env python3
"""
矛盾检测模块 - 检测前后记忆中的矛盾
目标：发现"说了一件事但后来做了相反的事"之类的矛盾
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

# 矛盾模式：说X但做Y，或说X但后来否认X
CONTRADICTION_PATTERNS = [
    # 模式1: 说了要A但后来做了非A
    (r'要(做|搞|去|找|买)', r'没有(做|搞|去|找|买)', 0.8),
    (r'计划(做|搞|去)', r'(没做|取消|算了)', 0.8),
    
    # 模式2: 说"不要"但后来"要了"
    (r'不要', r'要了', 0.7),
    (r'不用', r'用了', 0.7),
    
    # 模式3: 说"已经完成"但后来又说"还没做"
    (r'已完成', r'还没', 0.9),
    (r'做好了', r'没做', 0.9),
    
    # 模式4: 之前说过A，但新内容否定了A
    (r'会做', r'没做', 0.8),
    (r'可以', r'不行', 0.6),
]

# 关键实体 - 优先检测这些相关的矛盾
KEY_ENTITIES = [
    '用户', '管理员', 'Agent', '团队', 
    '飞书', '记忆引擎', '调度系统',
    '广告', '投放', '项目'
]

class ContradictionDetector:
    def __init__(self, memory_dir: Path):
        self.detections_file = memory_dir / '.contradiction-detections.json'
        self.data = self._load()
    
    def _load(self) -> Dict:
        if self.detections_file.exists():
            try:
                with open(self.detections_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'detections': [],     # [{text1, text2, date1, date2, type, severity, status}]
            'resolved': [],        # 已解决的矛盾
            'last_check': None,
            'stats': {
                'total': 0,
                'resolved': 0,
                'unresolved': 0
            }
        }
    
    def _save(self):
        self.data['last_check'] = datetime.now().isoformat()
        self.data['stats']['total'] = len(self.data['detections'])
        self.data['stats']['unresolved'] = len([d for d in self.data['detections'] if d.get('status') != 'resolved'])
        self.data['stats']['resolved'] = len(self.data['resolved'])
        with open(self.detections_file, 'w') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def check_fact(self, text: str, date: str, category: str = "general") -> List[Dict]:
        """检查新事实是否与历史矛盾"""
        contradictions = []
        
        for pattern1, pattern2, severity in CONTRADICTION_PATTERNS:
            # 检查正面匹配 pattern1（表示意图/计划）
            if re.search(pattern1, text):
                # 在历史中找对应的否定 pattern2
                for existing in self.data.get('detections', []):
                    # 检查是否已经标记为矛盾
                    if existing.get('status') == 'resolved':
                        continue
                    
                    # 检查时间顺序（新事实必须在后）
                    existing_date = existing.get('date2', '')
                    if existing_date and date > existing_date:
                        # 之前说有计划，现在说做了相反的事
                        if re.search(pattern2, existing.get('text1', '')):
                            contradictions.append({
                                'type': 'intent_vs_action',
                                'severity': severity,
                                'date1': existing.get('date1'),
                                'date2': date,
                                'text1': existing.get('text1', '')[:100],
                                'text2': text[:100],
                                'status': 'detected'
                            })
        
        # 更新检测记录
        for contra in contradictions:
            # 检查是否已存在类似矛盾
            is_new = True
            for existing in self.data['detections']:
                if existing.get('text1') == contra.get('text1') and existing.get('text2') == contra.get('text2'):
                    is_new = False
                    break
            
            if is_new:
                self.data['detections'].append(contra)
        
        if contradictions:
            self._save()
        
        return contradictions
    
    def add_fact_pair(self, text1: str, text2: str, date1: str, date2: str, 
                      contra_type: str = "potential", severity: float = 0.5):
        """主动记录一对可能矛盾的事实"""
        detection = {
            'type': contra_type,
            'severity': severity,
            'text1': text1[:150],
            'text2': text2[:150],
            'date1': date1,
            'date2': date2,
            'status': 'detected',
            'detected_at': datetime.now().isoformat()
        }
        
        # 去重
        for existing in self.data['detections']:
            if existing.get('text1') == text1 and existing.get('text2') == text2:
                return  # 已存在
        
        self.data['detections'].append(detection)
        self._save()
        return detection
    
    def resolve(self, index: int, resolution: str = ""):
        """标记矛盾已解决"""
        if 0 <= index < len(self.data['detections']):
            detection = self.data['detections'].pop(index)
            detection['resolved_at'] = datetime.now().isoformat()
            detection['resolution'] = resolution
            self.data['resolved'].append(detection)
            self._save()
    
    def get_unresolved(self) -> List[Dict]:
        return [d for d in self.data['detections'] if d.get('status') != 'resolved']
    
    def get_summary(self) -> Dict:
        """获取矛盾摘要"""
        unresolved = self.get_unresolved()
        by_severity = {'high': [], 'medium': [], 'low': []}
        
        for d in unresolved:
            sev = 'high' if d.get('severity', 0) >= 0.8 else 'medium' if d.get('severity', 0) >= 0.6 else 'low'
            by_severity[sev].append(d)
        
        return {
            'total': len(self.data['detections']),
            'unresolved': len(unresolved),
            'resolved': len(self.data['resolved']),
            'by_severity': {
                'high': len(by_severity['high']),
                'medium': len(by_severity['medium']),
                'low': len(by_severity['low'])
            },
            'recent_unresolved': unresolved[:5]
        }

if __name__ == '__main__':
    from pathlib import Path
    home = Path.home()
    detector = ContradictionDetector(home / '.agent-mem/memory')
    summary = detector.get_summary()
    print(f"📊 矛盾检测统计: {json.dumps(summary, indent=2, ensure_ascii=False)}")
