#!/usr/bin/env python3
"""
记忆反馈模块 - 用户说"不对，应该是X"能自动修正
借鉴 MemOS 的 Memory Feedback & Correction 概念
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class MemoryFeedback:
    """记忆反馈处理器 - 处理用户的修正和补充"""
    
    def __init__(self, memory_dir: Path):
        self.feedback_file = memory_dir / '.memory-feedback.json'
        self.corrections_file = memory_dir / '.memory-corrections.json'
        self.data = self._load()
        self.corrections = self._load_corrections()
    
    def _load(self) -> Dict:
        if self.feedback_file.exists():
            try:
                with open(self.feedback_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'feedbacks': [],   # [{original, corrected, reason, date, status}]
            'pending': [],     # 待确认的反馈
            'applied': []      # 已应用的反馈
        }
    
    def _load_corrections(self) -> Dict:
        if self.corrections_file.exists():
            try:
                with open(self.corrections_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'corrections': [],  # 长期有效的修正规则
            'last_updated': None
        }
    
    def _save(self):
        with open(self.feedback_file, 'w') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def _save_corrections(self):
        self.corrections['last_updated'] = datetime.now().isoformat()
        with open(self.corrections_file, 'w') as f:
            json.dump(self.corrections, f, indent=2, ensure_ascii=False)
    
    # 反馈模式检测
    FEEDBACK_PATTERNS = [
        # 否定类
        (r'不对', 'negate'),
        (r'不是', 'negate'),
        (r'错了', 'negate'),
        (r'错误', 'negate'),
        (r'应该(不是|没|不)', 'negate'),
        # 修正类
        (r'改成了|改成|改为', 'correct'),
        (r'正确的是', 'correct'),
        (r'其实(是|应该)', 'correct'),
        (r'更正', 'correct'),
        # 补充类
        (r'还(应该|要|需要|要)', 'supplement'),
        (r'补充', 'supplement'),
        (r'还有', 'supplement'),
        (r'另外', 'supplement'),
        # 确认类（正反馈）
        (r'对的', 'confirm'),
        (r'没错', 'confirm'),
        (r'是的', 'confirm'),
        (r'正确', 'confirm'),
    ]
    
    def detect_feedback(self, text: str) -> Optional[Dict]:
        """检测文本中是否包含反馈信息"""
        text = text.strip()
        
        for pattern, ftype in self.FEEDBACK_PATTERNS:
            match = re.search(pattern, text)
            if match:
                return {
                    'type': ftype,
                    'pattern': match.group(0),
                    'position': match.start(),
                    'text': text
                }
        
        return None
    
    def parse_feedback(self, text: str) -> Optional[Dict]:
        """解析反馈，提取原始信息和修正信息"""
        feedback = self.detect_feedback(text)
        if not feedback:
            return None
        
        ftype = feedback['type']
        
        if ftype == 'negate':
            # 否定类：说不对，但需要从上下文推断原信息
            return {
                'feedback_type': 'negate',
                'original_hint': text,
                'corrected_hint': self._extract_correction(text),
                'raw_text': text
            }
        
        elif ftype == 'correct':
            # 修正类：有明确的修正
            parts = re.split(r'(应该是|正确的是|改成了|改成)', text)
            if len(parts) >= 3:
                return {
                    'feedback_type': 'correct',
                    'original_hint': parts[0].strip(),
                    'corrected': parts[-1].strip(),
                    'raw_text': text
                }
        
        elif ftype == 'supplement':
            # 补充类
            return {
                'feedback_type': 'supplement',
                'original_hint': text,
                'supplement': self._extract_supplement(text),
                'raw_text': text
            }
        
        elif ftype == 'confirm':
            # 确认类（正反馈，可以用来加强记忆）
            return {
                'feedback_type': 'confirm',
                'content': text,
                'raw_text': text
            }
        
        return None
    
    def _extract_correction(self, text: str) -> str:
        """提取修正后的内容"""
        # 找"应该是"后面的内容
        match = re.search(r'应该(不是|没|不)?(.+)', text)
        if match:
            return match.group(2).strip()
        return text
    
    def _extract_supplement(self, text: str) -> str:
        """提取补充内容"""
        match = re.search(r'(还|另外)?(应该|要|需要)(.*)', text)
        if match:
            return match.group(3).strip()
        return text
    
    def add_feedback(self, text: str, date: str = None, source: str = "user") -> Dict:
        """添加一条反馈"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        parsed = self.parse_feedback(text)
        
        if not parsed:
            return {'status': 'ignored', 'reason': 'no_feedback_detected'}
        
        parsed['date'] = date
        parsed['source'] = source
        parsed['status'] = 'pending'
        
        self.data['feedbacks'].append(parsed)
        self.data.setdefault('pending', []).append(parsed)
        
        self._save()
        
        return {'status': 'added', 'feedback': parsed}
    
    def apply_feedback(self, feedback_index: int, action: str = "apply") -> Dict:
        """应用反馈到记忆系统"""
        if feedback_index < 0 or feedback_index >= len(self.data.get('pending', [])):
            return {'status': 'error', 'reason': 'invalid_index'}
        
        feedback = self.data['pending'][feedback_index]
        
        if action == 'apply':
            # 创建修正规则
            correction = {
                'original_pattern': feedback.get('original_hint', '')[:100],
                'corrected': feedback.get('corrected', '')[:100],
                'feedback_type': feedback.get('feedback_type'),
                'created_at': datetime.now().isoformat(),
                'use_count': 0
            }
            
            self.corrections['corrections'].append(correction)
            feedback['status'] = 'applied'
            
            # 从 pending 移到 applied
            self.data['pending'].pop(feedback_index)
            self.data.setdefault('applied', []).append(feedback)
            
            self._save()
            self._save_corrections()
            
            return {'status': 'applied', 'correction': correction}
        
        elif action == 'reject':
            self.data['pending'].pop(feedback_index)
            self._save()
            return {'status': 'rejected'}
        
        return {'status': 'error', 'reason': 'invalid_action'}
    
    def check_corrections(self, text: str) -> List[Dict]:
        """检查文本是否需要应用已知的修正"""
        matches = []
        
        for correction in self.corrections.get('corrections', []):
            if correction['original_pattern'] and correction['original_pattern'] in text:
                matches.append({
                    'correction': correction['corrected'],
                    'original': correction['original_pattern']
                })
                correction['use_count'] += 1
        
        if matches:
            self._save_corrections()
        
        return matches
    
    def get_pending_count(self) -> int:
        return len(self.data.get('pending', []))
    
    def get_corrections_summary(self) -> List[Dict]:
        return self.corrections.get('corrections', [])[:20]
    
    def get_stats(self) -> Dict:
        return {
            'total_feedbacks': len(self.data.get('feedbacks', [])),
            'pending': len(self.data.get('pending', [])),
            'applied': len(self.data.get('applied', [])),
            'corrections_count': len(self.corrections.get('corrections', []))
        }

if __name__ == '__main__':
    home = Path.home()
    fb = MemoryFeedback(home / '.agent-mem/memory')
    
    # 测试反馈检测
    tests = [
        "不对，应该先检查再执行",
        "不是这样，应该是先确认",
        "改成了每天早上8点执行",
        "记住了，其实是下午3点",
        "对的，没错",
    ]
    
    print("=== 反馈检测测试 ===")
    for t in tests:
        result = fb.detect_feedback(t)
        parsed = fb.parse_feedback(t)
        print(f"输入: {t}")
        print(f"  检测: {result}")
        print(f"  解析: {parsed}")
        print()
    
    print(f"📊 反馈统计: {fb.get_stats()}")
