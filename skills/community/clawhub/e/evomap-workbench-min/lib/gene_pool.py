#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基因池 - 完整版
功能：基因管理、效率统计、基因优化、基因组合
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from datetime import datetime
import json


@dataclass
class Gene:
    """基因"""
    name: str
    efficiency: float = 1.0
    category: str = "default"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    usage_count: int = 0
    success_count: int = 0
    mutation_history: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def mutate(self, mutation_type: str, delta: float):
        """基因变异"""
        old_efficiency = self.efficiency
        self.efficiency = max(0.0, min(1.0, self.efficiency + delta))
        self.updated_at = datetime.utcnow().isoformat()
        self.mutation_history.append({
            'type': mutation_type,
            'delta': delta,
            'before': old_efficiency,
            'after': self.efficiency,
            'timestamp': self.updated_at
        })


@dataclass
class GeneCombination:
    """基因组合"""
    combination_id: str
    genes: List[str]
    synergy_score: float
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        return asdict(self)


class GenePool:
    """基因池"""
    
    def __init__(self, show_version: bool = False):
        if show_version:
            print(f"🧬 EvoMap WorkBench v1.0.11 - 基因池已加载")
        self.genes: Dict[str, Gene] = {
            'progress_display': Gene('progress_display', 1.0, 'ui'),
            'asset_validator': Gene('asset_validator', 1.0, 'validation'),
            'gep_version_compat': Gene('gep_version_compat', 1.0, 'compat'),
            'dry_run': Gene('dry_run', 1.0, 'validation'),
            'error_recovery': Gene('error_recovery', 1.0, 'recovery'),
            'task_tracker': Gene('task_tracker', 1.0, 'tracking'),
            'tiered_optimization': Gene('tiered_optimization', 1.0, 'optimization'),
            'fault_handling': Gene('fault_handling', 1.0, 'recovery'),
            'api_compatibility': Gene('api_compatibility', 1.0, 'compat'),
            'fee_protection': Gene('fee_protection', 1.0, 'protection'),
            'performance': Gene('performance', 1.0, 'optimization'),
            'network': Gene('network', 1.0, 'optimization'),
            'notification': Gene('notification', 1.0, 'notification'),
            'decision_evaluator': Gene('decision_evaluator', 1.0, 'evaluation')
        }
        self.combinations: Dict[str, GeneCombination] = {}
        self.optimization_history: List[Dict] = []
    
    def get_gene(self, name: str) -> Optional[Gene]:
        """获取基因"""
        return self.genes.get(name)
    
    def get_all_genes(self) -> List[Gene]:
        """获取所有基因"""
        return list(self.genes.values())
    
    def get_genes_by_category(self, category: str) -> List[Gene]:
        """按类别获取基因"""
        return [g for g in self.genes.values() if g.category == category]
    
    def optimize_gene(self, name: str, delta: float, reason: str = "usage"):
        """优化基因"""
        gene = self.genes.get(name)
        if gene:
            gene.mutate(reason, delta)
            self.optimization_history.append({
                'gene': name,
                'delta': delta,
                'reason': reason,
                'timestamp': datetime.utcnow().isoformat()
            })
    
    def auto_optimize(self, performance_data: Dict):
        """自动优化基因"""
        for gene_name, performance in performance_data.items():
            if gene_name in self.genes:
                gene = self.genes[gene_name]
                gene.usage_count += 1
                
                if performance.get('success', False):
                    gene.success_count += 1
                    # 成功时小幅提升
                    self.optimize_gene(gene_name, 0.01, "success")
                else:
                    # 失败时小幅降低
                    self.optimize_gene(gene_name, -0.01, "failure")
    
    def create_combination(self, gene_names: List[str]) -> GeneCombination:
        """创建基因组合"""
        # 计算协同分数
        synergy_score = self._calculate_synergy(gene_names)
        
        combination = GeneCombination(
            combination_id=f"combo_{'_'.join(gene_names)}",
            genes=gene_names,
            synergy_score=synergy_score
        )
        
        self.combinations[combination.combination_id] = combination
        return combination
    
    def _calculate_synergy(self, gene_names: List[str]) -> float:
        """计算协同分数"""
        if len(gene_names) < 2:
            return 0.0
        
        # 基于基因类别计算协同
        categories = set()
        for name in gene_names:
            gene = self.genes.get(name)
            if gene:
                categories.add(gene.category)
        
        # 不同类别的基因组合有更高协同
        synergy = len(categories) / len(gene_names)
        
        # 基于效率计算
        avg_efficiency = sum(self.genes[n].efficiency for n in gene_names if n in self.genes) / len(gene_names)
        
        return (synergy + avg_efficiency) / 2
    
    def get_best_combination(self, target_category: str = None) -> Optional[GeneCombination]:
        """获取最佳组合"""
        if not self.combinations:
            return None
        
        if target_category:
            # 按类别筛选
            filtered = [
                c for c in self.combinations.values()
                if any(self.genes.get(g, Gene(g)).category == target_category for g in c.genes)
            ]
            if filtered:
                return max(filtered, key=lambda c: c.synergy_score)
        
        # 返回协同分数最高的组合
        return max(self.combinations.values(), key=lambda c: c.synergy_score)
    
    def get_avg_efficiency(self) -> float:
        """获取平均效率"""
        if not self.genes:
            return 0.0
        return sum(g.efficiency for g in self.genes.values()) / len(self.genes)
    
    def get_efficiency_by_category(self) -> Dict[str, float]:
        """按类别获取效率"""
        categories = {}
        for gene in self.genes.values():
            if gene.category not in categories:
                categories[gene.category] = []
            categories[gene.category].append(gene.efficiency)
        
        return {
            cat: sum(effs) / len(effs) if effs else 0.0
            for cat, effs in categories.items()
        }
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            'total_genes': len(self.genes),
            'avg_efficiency': self.get_avg_efficiency(),
            'efficiency_by_category': self.get_efficiency_by_category(),
            'total_combinations': len(self.combinations),
            'best_combination': self.get_best_combination().to_dict() if self.get_best_combination() else None,
            'optimization_history_size': len(self.optimization_history),
            'genes': {name: gene.to_dict() for name, gene in self.genes.items()}
        }
    
    def export_genes(self, file_path: str):
        """导出基因"""
        data = {
            'genes': {name: gene.to_dict() for name, gene in self.genes.items()},
            'combinations': {cid: combo.to_dict() for cid, combo in self.combinations.items()},
            'exported_at': datetime.utcnow().isoformat()
        }
        
        from pathlib import Path
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def import_genes(self, file_path: str):
        """导入基因"""
        from pathlib import Path
        if not Path(file_path).exists():
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for name, gene_data in data.get('genes', {}).items():
            if name in self.genes:
                # 更新现有基因
                gene = self.genes[name]
                gene.efficiency = gene_data.get('efficiency', gene.efficiency)
                gene.usage_count = gene_data.get('usage_count', 0)
                gene.success_count = gene_data.get('success_count', 0)


if __name__ == "__main__":
    # 测试基因池
    print("=== 测试基因池 ===\n")
    
    pool = GenePool()
    
    # 获取统计
    stats = pool.get_stats()
    print(f"基因总数：{stats['total_genes']}")
    print(f"平均效率：{stats['avg_efficiency']:.2%}")
    print(f"按类别效率：{stats['efficiency_by_category']}\n")
    
    # 优化基因
    pool.optimize_gene('error_recovery', 0.05, "testing")
    print(f"优化后 error_recovery 效率：{pool.get_gene('error_recovery').efficiency:.2%}\n")
    
    # 创建组合
    combo = pool.create_combination(['error_recovery', 'fault_handling', 'api_compatibility'])
    print(f"基因组合：{combo.combination_id}")
    print(f"协同分数：{combo.synergy_score:.2%}\n")
    
    # 自动优化
    performance_data = {
        'error_recovery': {'success': True},
        'fault_handling': {'success': False},
        'api_compatibility': {'success': True}
    }
    pool.auto_optimize(performance_data)
    
    # 导出统计
    print(f"最终统计：{json.dumps(stats, indent=2, ensure_ascii=False)}")
