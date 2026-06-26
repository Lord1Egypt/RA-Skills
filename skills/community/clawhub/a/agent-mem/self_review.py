#!/usr/bin/env python3
"""
主动复盘模块 V2 - 带规律库和验证闭环
目标：从每天的复盘中提炼规律，并追踪"经验是否有效"
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class SelfReview:
    """主动复盘 - 带规律库和验证闭环"""
    
    def __init__(self, memory_dir: Path):
        self.memory_dir = memory_dir
        self.reviews_file = memory_dir / '.self-reviews.json'
        self.patterns_file = memory_dir / '.experience-patterns.json'
        self.validations_file = memory_dir / '.decision-validations.json'
        self.state_file = memory_dir / '.memory-engine-state-v2.json'
        
        self.data = self._load()
        self.patterns = self._load_patterns()
        self.validations = self._load_validations()
    
    def _load(self) -> Dict:
        if self.reviews_file.exists():
            try:
                with open(self.reviews_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'reviews': [],
            'streak': 0
        }
    
    def _load_patterns(self) -> Dict:
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'patterns': [],      # [{rule, context, success_count, fail_count, last_used}]
            'sources': {}        # {pattern: [source_review_date]}
        }
    
    def _load_validations(self) -> Dict:
        if self.validations_file.exists():
            try:
                with open(self.validations_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'validations': [],   # [{decision, context, result, validated_at, effective}]
            'pending': []        # 待验证的决策
        }
    
    def _save(self):
        with open(self.reviews_file, 'w') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def _save_patterns(self):
        with open(self.patterns_file, 'w') as f:
            json.dump(self.patterns, f, indent=2, ensure_ascii=False)
    
    def _save_validations(self):
        with open(self.validations_file, 'w') as f:
            json.dump(self.validations, f, indent=2, ensure_ascii=False)
    
    def _extract_pattern_from_text(self, text: str, date: str) -> Optional[Dict]:
        """从文本中提取可复用的规律"""
        # 匹配"应该/要/用X方法"这类指导性语句
        patterns_to_extract = [
            r'(应该|要|推荐|最好)(.*?)(，|$)',
            r'(用|采用|选择)(.*?)(方法|方案|策略)',
            r'(每次|遇到.*时)(.*?)(就|要)(.*)',
            r'(记住|切记|注意)(.*?)(，|$)',
        ]
        
        for pattern in patterns_to_extract:
            match = re.search(pattern, text)
            if match:
                rule = match.group(0)
                if len(rule) > 10 and len(rule) < 150:
                    return {
                        'rule': rule,
                        'context': text[:100],
                        'date': date,
                        'success_count': 0,
                        'fail_count': 0,
                        'last_used': None,
                        'times_tested': 0
                    }
        return None
    
    def _extract_decision(self, text: str, date: str) -> Optional[Dict]:
        """提取决策点"""
        decision_signals = ['决定', '选择', '用', '采用', '开始', '停止', '做', '不改']
        for signal in decision_signals:
            if signal in text and len(text) > 20:
                return {
                    'decision': text[:150],
                    'context': '',
                    'date': date,
                    'result': None,
                    'validated_at': None,
                    'effective': None  # None=pending, True=有效, False=无效
                }
        return None
    
    def generate_review(self, date: str = None) -> Dict:
        """生成复盘报告 + 提取规律"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        day_file = self.memory_dir / f'{date}.md'
        learnings = []
        mistakes = []
        improvements = []
        new_patterns = []
        decisions = []
        
        if day_file.exists():
            with open(day_file, 'r') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line or len(line) < 10:
                    continue
                
                # 检测成功/学习
                if any(s in line for s in ['✅', '成功', '完成', '学会了', '搞定了']) and '失败' not in line:
                    learnings.append(line[:150])
                    # 提取规律
                    pattern = self._extract_pattern_from_text(line, date)
                    if pattern:
                        new_patterns.append(pattern)
                    # 提取决策
                    decision = self._extract_decision(line, date)
                    if decision:
                        decisions.append(decision)
                
                # 检测问题/踩坑
                if any(s in line for s in ['❌', '失败', '错误', '踩坑', '教训', '注意', '修复']):
                    mistakes.append(line[:150])
                
                # 检测改进建议
                if any(s in line for s in ['改进', '优化', '建议', '应该', '下次']):
                    improvements.append(line[:150])
                    pattern = self._extract_pattern_from_text(line, date)
                    if pattern:
                        new_patterns.append(pattern)
        
        # 去重
        learnings = learnings[:10]
        mistakes = list(dict.fromkeys(mistakes))[:10]
        improvements = improvements[:5]
        
        # 添加新规律（去重）
        for np in new_patterns:
            is_new = True
            for existing in self.patterns['patterns']:
                if existing['rule'] == np['rule']:
                    is_new = False
                    break
            if is_new:
                self.patterns['patterns'].append(np)
        
        # 记录待验证决策
        for d in decisions:
            is_new = True
            for existing in self.validations.get('pending', []):
                if existing['decision'] == d['decision']:
                    is_new = False
                    break
            if is_new:
                self.validations.setdefault('pending', []).append(d)
        
        # 计算得分
        score = self._calc_score(learnings, mistakes)
        
        review = {
            'date': date,
            'learnings': learnings,
            'mistakes': mistakes,
            'improvements': improvements,
            'new_patterns': len(new_patterns),
            'score': score,
            'generated_at': datetime.now().isoformat()
        }
        
        self.data['reviews'].append(review)
        self.data['streak'] += 1
        
        self._save()
        self._save_patterns()
        self._save_validations()
        
        return review
    
    def _calc_score(self, learnings: List, mistakes: List) -> int:
        base = 6
        base += min(len(learnings), 3) * 0.5
        base -= min(len(mistakes), 3) * 0.5
        return max(1, min(10, int(base)))
    
    def validate_decision(self, decision: str, result: str, effective: bool):
        """验证一个决策的有效性"""
        pending = self.validations.get('pending', [])
        
        for i, p in enumerate(pending):
            if p['decision'][:80] == decision[:80]:
                p['result'] = result
                p['validated_at'] = datetime.now().isoformat()
                p['effective'] = effective
                
                # 更新对应规律的有效性
                for pat in self.patterns['patterns']:
                    if pat.get('rule') and pat['rule'] in decision:
                        pat['times_tested'] += 1
                        if effective:
                            pat['success_count'] += 1
                        else:
                            pat['fail_count'] += 1
                
                self.validations.setdefault('validations', []).append(pending.pop(i))
                self._save_validations()
                return True
        return False
    
    def get_top_patterns(self, limit: int = 5) -> List[Dict]:
        """获取最有效的规律（按成功率排序）"""
        valid_patterns = [p for p in self.patterns['patterns'] if p.get('times_tested', 0) >= 1]
        sorted_patterns = sorted(valid_patterns, key=lambda x: (
            x.get('success_count', 0) / max(x.get('times_tested', 1), 1) if x.get('times_tested', 0) > 0 else 0
        ), reverse=True)
        return sorted_patterns[:limit]
    
    def get_pending_validations(self) -> List[Dict]:
        return self.validations.get('pending', [])
    
    def get_daily_review_text(self, date: str = None) -> str:
        """生成复盘文本"""
        review = self.generate_review(date)
        
        score_emoji = "🟢" if review['score'] >= 7 else "🟡" if review['score'] >= 5 else "🔴"
        
        text = f"""
{score_emoji} **每日复盘 {review['date']}** (得分: {review['score']}/10)

"""
        
        if review['learnings']:
            text += "✅ **今天做成的**\n"
            for l in review['learnings'][:5]:
                text += f"  • {l}\n"
            text += "\n"
        
        if review['mistakes']:
            text += "⚠️ **今天踩的坑**\n"
            for m in review['mistakes'][:5]:
                text += f"  • {m}\n"
            text += "\n"
        
        if review['improvements']:
            text += "💡 **改进建议**\n"
            for i in review['improvements'][:3]:
                text += f"  • {i}\n"
        
        # 规律库精华
        top_patterns = self.get_top_patterns(3)
        if top_patterns:
            text += "\n🧠 **验证有效规律**\n"
            for p in top_patterns:
                rate = p['success_count'] / max(p['times_tested'], 1) * 100
                text += f"  • [{rate:.0f}%成功率] {p['rule'][:60]}\n"
        
        # 待验证决策
        pending = self.get_pending_validations()
        if pending:
            text += f"\n📋 **待验证决策** ({len(pending)}个)\n"
            for p in pending[:3]:
                text += f"  • [{p['date']}] {p['decision'][:60]}...\n"
        
        # 每7天深度总结
        if len(self.data['reviews']) % 7 == 0 and len(self.data['reviews']) >= 7:
            text += "\n" + self._get_weekly_summary()
        
        return text.strip()
    
    def _get_weekly_summary(self) -> str:
        recent = self.data['reviews'][-7:]
        
        # 统计高频问题
        problem_counts = {}
        for review in recent:
            for mistake in review.get('mistakes', []):
                topic = mistake[:50]
                problem_counts[topic] = problem_counts.get(topic, 0) + 1
        
        top_problems = sorted(problem_counts.items(), key=lambda x: -x[1])[:3]
        
        text = "📊 **本周问题TOP3**\n"
        for prob, count in top_problems:
            text += f"  {count}次: {prob[:60]}...\n"
        
        avg_score = sum(r['score'] for r in recent) / len(recent)
        text += f"\n📈 本周平均分: {avg_score:.1f}/10\n"
        
        # 规律统计
        total_patterns = len(self.patterns['patterns'])
        tested = sum(1 for p in self.patterns['patterns'] if p.get('times_tested', 0) > 0)
        text += f"🧠 累计规律: {total_patterns}条, 已验证: {tested}条\n"
        
        return text
    
    def get_review_stats(self) -> Dict:
        total = len(self.data['reviews'])
        avg = sum(r['score'] for r in self.data['reviews']) / max(total, 1)
        
        patterns_total = len(self.patterns['patterns'])
        patterns_tested = sum(1 for p in self.patterns['patterns'] if p.get('times_tested', 0) > 0)
        
        pending_count = len(self.validations.get('pending', []))
        
        return {
            'total_reviews': total,
            'streak': self.data['streak'],
            'avg_score': round(avg, 1),
            'total_patterns': patterns_total,
            'patterns_tested': patterns_tested,
            'pending_validations': pending_count
        }

if __name__ == '__main__':
    home = Path.home()
    review = SelfReview(home / '.agent-mem/memory')
    text = review.get_daily_review_text()
    print(text)
    
    stats = review.get_review_stats()
    print(f"\n📊 统计: {stats}")
