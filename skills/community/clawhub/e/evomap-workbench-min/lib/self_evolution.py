#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自进化系统 - 完整版
功能：进化记录、学习历史、自适应调整、进化报告
"""

import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict, field


@dataclass
class EvolutionRecord:
    """进化记录"""
    evolution_id: str
    timestamp: str
    trigger: str  # daily/work_complete/manual
    improvements: Dict = field(default_factory=dict)
    efficiency_before: float = 0.0
    efficiency_after: float = 0.0
    learning_points: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class LearningHistory:
    """学习历史"""
    experience: Dict
    analysis: Dict
    rule_changes: Dict
    timestamp: str
    outcome: Optional[str] = None


class SelfEvolution:
    """自进化系统"""
    
    def __init__(self, state_file: str = None, show_version: bool = False):
        if show_version:
            print(f"🧬 EvoMap WorkBench v1.0.11 - 自进化系统已加载")
        self.state_file = state_file or "evolution_state.json"
        self.evolution_count = 0
        self.last_evolution = None
        self.learning_history: List[LearningHistory] = []
        self.adaptive_rules: Dict[str, Dict] = {}
        self.evolution_records: List[EvolutionRecord] = []
        self.load_state()
    
    def load_state(self):
        """加载状态"""
        if Path(self.state_file).exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
                self.evolution_count = state.get('evolution_count', 0)
                self.adaptive_rules = state.get('adaptive_rules', {})
    
    def save_state(self):
        """保存状态"""
        state = {
            'evolution_count': self.evolution_count,
            'adaptive_rules': self.adaptive_rules,
            'last_updated': datetime.utcnow().isoformat()
        }
        
        Path(self.state_file).parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    
    def evolve(self, experience: Dict) -> EvolutionRecord:
        """进化"""
        # 分析经验
        analysis = self._analyze_experience(experience)
        
        # 评估当前规则
        rule_performance = self._evaluate_rules(analysis)
        
        # 调整规则
        new_rules = {}
        if rule_performance < 0.8:
            new_rules = self._adapt_rules(analysis)
            self.adaptive_rules.update(new_rules)
        
        # 记录学习历史
        self.learning_history.append(LearningHistory(
            experience=experience,
            analysis=analysis,
            rule_changes=new_rules,
            timestamp=datetime.utcnow().isoformat(),
            outcome=experience.get('outcome')
        ))
        
        # 创建进化记录
        efficiency_before = self._calculate_efficiency()
        self.evolution_count += 1
        self.last_evolution = datetime.utcnow().isoformat()
        efficiency_after = self._calculate_efficiency()
        
        record = EvolutionRecord(
            evolution_id=f"evo_{self.evolution_count}",
            timestamp=self.last_evolution,
            trigger='work_complete',
            improvements=new_rules,
            efficiency_before=efficiency_before,
            efficiency_after=efficiency_after,
            learning_points=self._extract_learning_points(analysis)
        )
        
        self.evolution_records.append(record)
        self.save_state()
        
        return record
    
    def daily_evolution(self) -> List[EvolutionRecord]:
        """每日进化"""
        records = []
        
        # 分析今日数据
        today = datetime.utcnow().date()
        today_records = [
            h for h in self.learning_history
            if datetime.fromisoformat(h.timestamp).date() == today
        ]
        
        if today_records:
            # 生成每日进化
            analysis = self._analyze_daily_pattern(today_records)
            new_rules = self._adapt_rules(analysis)
            
            if new_rules:
                self.adaptive_rules.update(new_rules)
                self.evolution_count += 1
                
                record = EvolutionRecord(
                    evolution_id=f"evo_daily_{today}",
                    timestamp=datetime.utcnow().isoformat(),
                    trigger='daily',
                    improvements=new_rules,
                    efficiency_before=0.0,
                    efficiency_after=self._calculate_efficiency(),
                    learning_points=self._extract_daily_insights(today_records)
                )
                
                self.evolution_records.append(record)
                records.append(record)
        
        return records
    
    def _analyze_experience(self, experience: Dict) -> Dict:
        """分析经验"""
        return {
            'success': experience.get('success', False),
            'error_type': experience.get('error_type'),
            'auto_recovery': experience.get('auto_recovery', False),
            'scenario': experience.get('scenario_name', ''),
            'duration': experience.get('duration', 0),
            'outcome': experience.get('outcome')
        }
    
    def _analyze_daily_pattern(self, records: List[LearningHistory]) -> Dict:
        """分析每日模式"""
        success_count = sum(1 for r in records if r.experience.get('success', False))
        total = len(records)
        
        return {
            'success_rate': success_count / total if total > 0 else 0,
            'total_experiences': total,
            'common_errors': self._find_common_errors(records),
            'best_scenarios': self._find_best_scenarios(records)
        }
    
    def _find_common_errors(self, records: List[LearningHistory]) -> List[str]:
        """查找常见错误"""
        errors = {}
        for r in records:
            error_type = r.experience.get('error_type')
            if error_type:
                errors[error_type] = errors.get(error_type, 0) + 1
        
        return sorted(errors.keys(), key=lambda x: errors[x], reverse=True)[:5]
    
    def _find_best_scenarios(self, records: List[LearningHistory]) -> List[str]:
        """查找最佳场景"""
        scenarios = {}
        for r in records:
            if r.experience.get('success', False):
                scenario = r.experience.get('scenario_name', 'unknown')
                scenarios[scenario] = scenarios.get(scenario, 0) + 1
        
        return sorted(scenarios.keys(), key=lambda x: scenarios[x], reverse=True)[:5]
    
    def _evaluate_rules(self, analysis: Dict) -> float:
        """评估规则"""
        if not self.adaptive_rules:
            return 0.5
        
        # 基于成功率评估
        recent = self.learning_history[-100:]
        if not recent:
            return 0.5
        
        success_count = sum(1 for h in recent if h.experience.get('success', False))
        return success_count / len(recent)
    
    def _adapt_rules(self, analysis: Dict) -> Dict:
        """调整规则"""
        new_rules = {}
        
        # 基于失败类型调整
        if not analysis.get('success', True) and analysis.get('error_type'):
            error_type = analysis['error_type']
            rule_key = f"handle_{error_type}"
            new_rules[rule_key] = {
                'action': 'auto_recovery' if analysis.get('auto_recovery') else 'manual_review',
                'priority': 'high',
                'updated_at': datetime.utcnow().isoformat(),
                'trigger_count': 1
            }
        elif analysis.get('success', False):
            # 优化成功规则
            for rule_key, rule in list(self.adaptive_rules.items()):
                if rule.get('trigger_count', 0) > 10:
                    rule['efficiency'] = rule.get('efficiency', 0.5) + 0.05
        
        return new_rules
    
    def _calculate_efficiency(self) -> float:
        """计算效率"""
        if not self.learning_history:
            return 0.0
        
        recent = self.learning_history[-100:]
        success_count = sum(1 for h in recent if h.experience.get('success', False))
        return success_count / len(recent)
    
    def _extract_learning_points(self, analysis: Dict) -> List[str]:
        """提取学习点"""
        points = []
        
        if analysis.get('success'):
            points.append(f"成功处理：{analysis.get('scenario', 'unknown')}")
        else:
            points.append(f"失败类型：{analysis.get('error_type', 'unknown')}")
            if analysis.get('auto_recovery'):
                points.append("自动恢复成功")
        
        return points
    
    def _extract_daily_insights(self, records: List[LearningHistory]) -> List[str]:
        """提取每日洞察"""
        insights = []
        
        success_rate = sum(1 for r in records if r.experience.get('success', False)) / len(records) if records else 0
        insights.append(f"今日成功率：{success_rate:.1%}")
        
        common_errors = self._find_common_errors(records)
        if common_errors:
            insights.append(f"常见错误：{', '.join(common_errors[:3])}")
        
        return insights
    
    def get_evolution_report(self) -> Dict:
        """获取进化报告"""
        return {
            'evolution_count': self.evolution_count,
            'last_evolution': self.last_evolution,
            'learning_history_size': len(self.learning_history),
            'adaptive_rules_count': len(self.adaptive_rules),
            'efficiency': self._calculate_efficiency(),
            'recent_records': [r.to_dict() for r in self.evolution_records[-10:]]
        }
    
    def get_adaptive_rules(self) -> Dict:
        """获取自适应规则"""
        return self.adaptive_rules


if __name__ == "__main__":
    # 测试自进化系统
    print("=== 测试自进化系统 ===\n")
    
    evolution = SelfEvolution()
    
    # 模拟经验
    experiences = [
        {'success': True, 'scenario_name': 'test1', 'outcome': 'success'},
        {'success': False, 'error_type': '429', 'auto_recovery': True, 'outcome': 'recovered'},
        {'success': True, 'scenario_name': 'test2', 'outcome': 'success'},
    ]
    
    for exp in experiences:
        record = evolution.evolve(exp)
        print(f"进化记录：{record.evolution_id}")
        print(f"效率：{record.efficiency_before:.2%} → {record.efficiency_after:.2%}")
        print(f"学习点：{record.learning_points}\n")
    
    # 获取报告
    report = evolution.get_evolution_report()
    print(f"进化报告：{json.dumps(report, indent=2, ensure_ascii=False)}")
