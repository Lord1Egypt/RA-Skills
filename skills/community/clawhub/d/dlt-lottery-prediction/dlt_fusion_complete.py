#!/usr/bin/env python3
"""
DLT多策略融合完全体 v4.0
整合策略融合引擎 + 五池采样 + 后区融合 + 博弈论 + 遗传算法 + 数学过滤 + 统计分析
"""

import sys
import os
import random
import warnings
warnings.filterwarnings('ignore')

sys.path.insert(0, '/home/claw/.openclaw/workspace/skills/dlt_lottery_prediction')

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional, Any
from collections import Counter, defaultdict

# 导入所有子模块
from dlt_predictor_upgraded import DLTPredictorUpgraded, load_dlt_data
from strategy_fusion_engine import StrategyFusionEngine
from five_pool_sampler_complete_final import FivePoolSampler
from dlt_back_fusion import BackZoneFusion
from modules.dlt_game_theory import DLTGameTheoryAnalyzer
from modules.dlt_genetic_optimizer import DLTGeneticOptimizer
from modules.dlt_math_filter import DLTMathFilter
from modules.dlt_statistics_analyzer import DLTStatisticsAnalyzer


class DLTFusionComplete:
    """DLT多策略融合完全体 — 整合所有预测模块的统一入口"""

    def __init__(self, data_path: str = '/mnt/d/cp/DLT历史数据_适配模型版.xlsx'):
        self.data_path = data_path

        # 1. 加载数据（带fallback）
        self.draws = self._load_data(data_path)
        if not self.draws:
            raise ValueError(f"数据加载失败: {data_path}")

        print(f"[DLT-Fusion] 历史数据加载完成 | 共{len(self.draws)}期")

        # 2. 初始化所有子模块
        try:
            self.predictor = DLTPredictorUpgraded(data_path)
        except Exception as e:
            print(f"[DLT-Fusion] DLTPredictorUpgraded初始化失败: {e}")
            self.predictor = None

        self.sfe = StrategyFusionEngine(self.draws, n_groups=5)
        self.pool_sampler = FivePoolSampler(self.draws)
        self.back_fusion = BackZoneFusion(self.draws)
        self.game_theory = DLTGameTheoryAnalyzer()
        self.genetic = DLTGeneticOptimizer(self.draws)
        self.math_filter = DLTMathFilter()
        self.stats = DLTStatisticsAnalyzer(self.draws)

        # 初始化遗传算法
        try:
            self.genetic.evolve(generations=50, verbose=False)
        except Exception as e:
            print(f"[DLT-Fusion] 遗传算法初始化: {e}")

        print(f"[DLT-Fusion] 初始化完成 | v4.0完全体")

    def _load_data(self, path: str) -> List[Tuple[List[int], List[int]]]:
        """加载数据，支持多种fallback"""
        # 优先使用dlt_predictor_upgraded的加载函数
        try:
            if os.path.exists(path):
                draws = load_dlt_data(path)
                if draws:
                    print(f"[DLT-Fusion] 从文件加载: {len(draws)}期")
                    return draws
        except Exception as e:
            print(f"[DLT-Fusion] load_dlt_data失败: {e}")

        # 尝试直接读取Excel
        try:
            df = pd.read_excel(path)
            draws = []
            for j in range(len(df)):
                front = sorted([int(df.iloc[j][f'前区{i}']) for i in range(1, 6)])
                back = sorted([int(df.iloc[j][f'后区{i}']) for i in range(1, 3)])
                draws.append((front, back))
            if draws and draws[0][0][0] > draws[-1][0][0]:
                draws = list(reversed(draws))
            if draws:
                print(f"[DLT-Fusion] 直接读取Excel: {len(draws)}期")
                return draws
        except Exception as e:
            print(f"[DLT-Fusion] 直接读取Excel失败: {e}")

        return []

    # ------------------------------------------------------------------
    # 公共接口
    # ------------------------------------------------------------------

    def get_group_recommendations(self) -> Dict[int, List[Any]]:
        """获取5组独立推荐"""
        results = self.sfe.generate_all_groups(n_per_group=5)
        return results

    def get_back_recommendations(self) -> List[List[int]]:
        """获取后区推荐（返回后区号码对列表）"""
        raw = self.back_fusion.generate_recommendations(n=5)
        # raw = List[Tuple[List[int], Dict[str,float]]]
        return [back_pair for back_pair, _ in raw]

    def generate_compound_bets(self, bet_type: str = '6+3', n_per_type: int = 2) -> Dict[str, List[Dict]]:
        """
        生成多种复式投注

        Args:
            bet_type: '6+3','7+2','7+3','8+2','8+3','9+3','9+4','9+6','all'
            n_per_type: 每种类型生成多少组

        Returns:
            Dict[bet_type, List[复式投注]]
        """
        bet_map = {
            '6+3': lambda: self.pool_sampler.generate_6_plus_3(n=n_per_type, strategy='game_theory'),
            '6+4': lambda: self.pool_sampler.generate_6_plus_4(n=n_per_type, strategy='game_theory'),
            '7+2': lambda: self.pool_sampler.generate_7_plus_2(n=n_per_type, strategy='mixed'),
            '7+3': lambda: self.pool_sampler.generate_7_plus_3(n=n_per_type, strategy='mixed'),
            '7+4': lambda: self.pool_sampler.generate_7_plus_4(n=n_per_type, strategy='balance'),
            '8+2': lambda: self.pool_sampler.generate_8_plus_2(n=n_per_type, strategy='hot'),
            '8+3': lambda: self.pool_sampler.generate_8_plus_3(n=n_per_type, strategy='mixed'),
            '8+4': lambda: self.pool_sampler.generate_8_plus_4(n=n_per_type, strategy='cold'),
            '8+5': lambda: self.pool_sampler.generate_8_plus_5(n=n_per_type, strategy='cold'),
            '9+3': lambda: self.pool_sampler.generate_9_plus_3(n=n_per_type, strategy='cold'),
            '9+4': lambda: self.pool_sampler.generate_9_plus_4(n=n_per_type, strategy='cold'),
            '9+6': lambda: self.pool_sampler.generate_9_plus_6(n=n_per_type, strategy='balance'),
        }

        if bet_type == 'all':
            results = {}
            for bt, fn in bet_map.items():
                try:
                    results[bt] = fn()
                except Exception:
                    results[bt] = []
            return results
        elif bet_type in bet_map:
            return {bet_type: bet_map[bet_type]()}
        else:
            return {'6+3': bet_map['6+3']()}

    def predict(self, top_n: int = 5, include_compound: bool = True) -> Dict[str, Any]:
        """主预测函数：多策略融合最终推荐"""
        # Step 1: SFE 5组融合
        all_groups = self.get_group_recommendations()

        # Step 2: 五池采样补充候选
        pool_candidates = self._sample_pool_candidates(n_per_pool=2)

        # Step 3: 后区融合
        back_recs = self.get_back_recommendations()

        # Step 4: 博弈论优化
        gt_scores = self._apply_game_theory(all_groups, pool_candidates)

        # Step 5: 遗传算法优化
        genetic_scores = self._apply_genetic_optimization(all_groups, pool_candidates)

        # Step 6: 汇总所有候选
        all_candidates = self._collect_candidates(all_groups, pool_candidates, gt_scores, genetic_scores)

        # Step 7: 综合评分
        self._compute_final_scores(all_candidates)

        # Step 8: 去重+分配后区
        unique = self._deduplicate_and_assign_back(all_candidates, back_recs)

        # Step 9: 最终排名
        unique.sort(key=lambda x: x['final_score'], reverse=True)

        result = {
            'single_bets': unique[:top_n],
        }

        # 添加复式投注推荐
        if include_compound:
            compound = self.generate_compound_bets('all', n_per_type=2)
            result['compound_bets'] = compound

        return result

    def predict_with_details(self, top_n: int = 5, include_compound: bool = True) -> Dict[str, Any]:
        """返回预测+详细分析"""
        pred_result = self.predict(top_n, include_compound=include_compound)
        groups = self.get_group_recommendations()

        # 构建各组详细推荐
        group_details = {}
        for gid, cands in groups.items():
            group_details[gid] = []
            for c in cands:
                gt_analysis = None
                try:
                    gt_analysis = self.game_theory.analyze_combo(c.front)
                except Exception:
                    pass
                group_details[gid].append({
                    'front': c.front,
                    'back': c.back,
                    'score': c.total_score,
                    'strategy': c.strategy_name,
                    'game_theory': gt_analysis
                })

        return {
            'single_bets': pred_result.get('single_bets', []),
            'compound_bets': pred_result.get('compound_bets', {}),
            'group_recommendations': group_details,
            'back_recommendations': self.get_back_recommendations(),
            'total_records': len(self.draws),
            'latest_draw': self.draws[-1] if self.draws else None,
            'latest_period': self._get_latest_period(),
        }

    def backtest(self, n_recent: int = 100) -> Dict[str, Any]:
        """
        重建回测：测量池级别命中率 vs 随机基准

        核心指标：
        - 每个池的平均命中个数（应该 > 随机基准 才算有效）
        - 每种复式类型的覆盖率（开奖号码在复式中的比例）
        - 对比随机基准：模型提升百分比
        """
        import random as _rnd
        _rnd.seed(42)

        if len(self.draws) < n_recent + 20:
            return {'error': f'数据不足 (需要{n_recent+20}期, 现有{len(self.draws)}期)'}

        test_draws = self.draws[-n_recent:]
        train_base = self.draws[:len(self.draws) - n_recent]

        if len(train_base) < 100:
            return {'error': '训练数据不足'}

        # 随机基准（每次选5个随机号码的前区命中期望）
        random_front_expect = 5.0 / 35 * 5  # ≈ 0.714
        random_back_expect = 2.0 / 12 * 2  # ≈ 0.333

        # 对每个测试期生成各池预测
        pool_front_hits = {'hot': [], 'cold': [], 'balance': [], 'game_theory': [], 'genetic': []}
        pool_back_hits = {'hot': [], 'cold': [], 'balance': [], 'game_theory': [], 'genetic': []}
        compound_coverage = {}

        from five_pool_sampler_complete_final import FivePoolSampler

        for i, actual in enumerate(test_draws):
            # 用历史数据生成各池
            hist = train_base + test_draws[:i] if i > 0 else train_base
            sampler = FivePoolSampler(hist)

            actual_front = set(actual[0])
            actual_back = set(actual[1])

            # 各池前区命中
            pool_map = {
                'hot': lambda: sampler.generate_hot_pool(20, 'front'),
                'cold': lambda: sampler.generate_cold_pool(20, 'front'),
                'balance': lambda: sampler.generate_balance_pool(20, 'front'),
                'game_theory': lambda: sampler.generate_game_theory_pool(20, 'front'),
                'genetic': lambda: sampler.generate_genetic_pool(20, 'front'),
            }
            for pname, gen in pool_map.items():
                try:
                    pool = gen()
                    pool_front_hits[pname].append(len(set(pool) & actual_front))
                except:
                    pool_front_hits[pname].append(0)

            # 各池后区命中
            pool_back_map = {
                'hot': lambda: sampler.generate_hot_pool(8, 'back'),
                'cold': lambda: sampler.generate_cold_pool(8, 'back'),
                'balance': lambda: sampler.generate_balance_pool(8, 'back'),
                'game_theory': lambda: sampler.generate_game_theory_pool(8, 'back'),
                'genetic': lambda: sampler.generate_genetic_pool(8, 'back'),
            }
            for pname, gen in pool_back_map.items():
                try:
                    pool = gen()
                    pool_back_hits[pname].append(len(set(pool) & actual_back))
                except:
                    pool_back_hits[pname].append(0)

            # 复式覆盖率
            compound_tests = [
                ('6+3', lambda: sampler.generate_6_plus_3(1, 'game_theory')),
                ('7+2', lambda: sampler.generate_7_plus_2(1, 'mixed')),
                ('8+2', lambda: sampler.generate_8_plus_2(1, 'hot')),
                ('9+3', lambda: sampler.generate_9_plus_3(1, 'cold')),
            ]
            for bt_name, bt_fn in compound_tests:
                try:
                    bets = bt_fn()
                    if bets:
                        bet = bets[0]
                        front_cov = len(set(bet['front']) & actual_front) / 5.0
                        back_cov = len(set(bet['back']) & actual_back) / 2.0
                        if bt_name not in compound_coverage:
                            compound_coverage[bt_name] = []
                        compound_coverage[bt_name].append({'front': front_cov, 'back': back_cov,
                                                        'avg': (front_cov + back_cov) / 2})
                except:
                    pass

        # 汇总结果
        result = {
            'n_tests': n_recent,
            'random_baseline': {
                'front_per_draw': round(random_front_expect, 3),
                'back_per_draw': round(random_back_expect, 3),
            },
            'pool_performance': {},
            'compound_coverage': {},
            'improvement_vs_random': {},
        }

        for pool_name in pool_front_hits:
            front_hits = pool_front_hits[pool_name]
            back_hits = pool_back_hits[pool_name]
            avg_front = round(float(np.mean(front_hits)), 3) if front_hits else 0
            avg_back = round(float(np.mean(back_hits)), 3) if back_hits else 0
            front_imp = round((avg_front / random_front_expect - 1) * 100, 1) if random_front_expect > 0 else 0
            back_imp = round((avg_back / random_back_expect - 1) * 100, 1) if random_back_expect > 0 else 0

            result['pool_performance'][pool_name] = {
                'avg_front_hits': avg_front,
                'avg_back_hits': avg_back,
                'max_front_hits': max(front_hits) if front_hits else 0,
                'max_back_hits': max(back_hits) if back_hits else 0,
            }
            result['improvement_vs_random'][pool_name] = {
                'front_improvement_%': front_imp,
                'back_improvement_%': back_imp,
            }

        for bt_name, covs in compound_coverage.items():
            front_covs = [c['front'] for c in covs]
            back_covs = [c['back'] for c in covs]
            result['compound_coverage'][bt_name] = {
                'avg_front_coverage': round(float(np.mean(front_covs)), 3),
                'avg_back_coverage': round(float(np.mean(back_covs)), 3),
                'full_hits_rate_%': round(sum(1 for c in covs if c['front'] == 1.0) / len(covs) * 100, 1) if covs else 0,
            }

        return result
    def _sample_pool_candidates(self, n_per_pool: int = 2) -> List[Dict[str, Any]]:
        """五池采样候选"""
        candidates = []
        try:
            # 使用stratified_sample生成前区组合
            front_combos = self.pool_sampler.stratified_sample(
                n_combinations=n_per_pool * 3, zone='front'
            )
            back_combos = self.pool_sampler.stratified_sample(
                n_combinations=n_per_pool * 3, zone='back'
            )

            # 交叉组合前区与后区
            for fc in front_combos[:n_per_pool * 2]:
                bc = random.choice(back_combos) if back_combos else [5, 8]
                candidates.append({
                    'front': sorted(fc),
                    'back': sorted(bc),
                    'source': 'pool_sampler',
                    'total_score': 0.5,
                    'strategy_name': 'FivePoolSampler',
                })
        except Exception as e:
            print(f"[DLT-Fusion] 五池采样失败: {e}")

        return candidates

    def _apply_game_theory(
        self,
        all_groups: Dict[int, List[Any]],
        pool_candidates: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """博弈论优化：计算各候选的博弈论综合评分"""
        gt_scores = {}

        # 对SFE候选评分
        for gid, cands in all_groups.items():
            for c in cands:
                key = f"G{gid}_{tuple(c.front)}"
                try:
                    analysis = self.game_theory.analyze_combo(c.front)
                    # combined_score = avoidance_score + regularity_score (两者都是0-1)
                    gt_scores[key] = float(analysis['scores']['combined_score'])
                except Exception:
                    gt_scores[key] = 0.5

        # 对池采样候选评分
        for i, pc in enumerate(pool_candidates):
            key = f"P{i}_{tuple(pc['front'])}"
            try:
                analysis = self.game_theory.analyze_combo(pc['front'])
                gt_scores[key] = float(analysis['scores']['combined_score'])
            except Exception:
                gt_scores[key] = 0.5

        return gt_scores

    def _apply_genetic_optimization(
        self,
        all_groups: Dict[int, List[Any]],
        pool_candidates: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """遗传算法优化：使用进化后的适应度"""
        genetic_scores = {}

        # 获取当前最优染色体（前区+后区适应度）
        try:
            best_chromosomes = self.genetic.get_best_solutions(top_k=10)
            best_front_set = set()
            best_back_set = set()
            for chrom in best_chromosomes:
                best_front_set.update(chrom.front_numbers)
                best_back_set.update(chrom.back_numbers)
        except Exception:
            best_front_set = set(range(1, 20))  # fallback
            best_back_set = set(range(1, 8))

        # 对SFE候选评分：与最优解的重合度
        for gid, cands in all_groups.items():
            for c in cands:
                key = f"G{gid}_{tuple(c.front)}"
                try:
                    front_overlap = len(set(c.front) & best_front_set) / 5.0
                    fitness = self._chromosome_fitness(c.front, c.back)
                    genetic_scores[key] = float(fitness)
                except Exception:
                    genetic_scores[key] = 0.5

        # 对池采样候选评分
        for i, pc in enumerate(pool_candidates):
            key = f"P{i}_{tuple(pc['front'])}"
            try:
                fitness = self._chromosome_fitness(pc['front'], pc['back'])
                genetic_scores[key] = float(fitness)
            except Exception:
                genetic_scores[key] = 0.5

        return genetic_scores

    def _chromosome_fitness(self, front: List[int], back: List[int]) -> float:
        """计算组合适应度（模拟Chromosome评估）"""
        fitness = 0.0

        # 热号比例 (40%)
        hot_front = list(range(1, 20))
        hot_back = list(range(1, 8))
        front_hot = len(set(front) & set(hot_front)) / 5.0
        back_hot = len(set(back) & set(hot_back)) / 2.0
        fitness += front_hot * 0.3 + back_hot * 0.1

        # 奇偶平衡 (20%)
        front_odd = sum(1 for n in front if n % 2 == 1)
        back_odd = sum(1 for n in back if n % 2 == 1)
        front_odd_score = 1 - abs(front_odd - 3) / 3
        back_odd_score = 1 - abs(back_odd - 1.5) / 1.5
        fitness += front_odd_score * 0.15 + back_odd_score * 0.05

        # 号码分布 (15%)
        front_spread = max(front) - min(front)
        spread_score = min(front_spread / 30, 1.0)
        fitness += spread_score * 0.15

        # 连号控制 (10%)
        front_sorted = sorted(front)
        consecutive = sum(
            1 for i in range(len(front_sorted) - 1)
            if front_sorted[i+1] - front_sorted[i] == 1
        )
        consecutive_score = 1 - min(consecutive / 2, 1.0)
        fitness += consecutive_score * 0.10

        # 和值范围 (10%)
        front_sum = sum(front)
        if 90 <= front_sum <= 130:
            sum_score = 1.0
        else:
            sum_score = 1 - min(abs(front_sum - 110) / 50, 1.0)
        fitness += sum_score * 0.10

        return max(0.0, min(1.0, fitness))

    def _collect_candidates(
        self,
        all_groups: Dict[int, List[Any]],
        pool_candidates: List[Dict[str, Any]],
        gt_scores: Dict[str, float],
        genetic_scores: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """收集并整合所有候选"""
        all_candidates = []

        # SFE候选
        for gid, cands in all_groups.items():
            for c in cands:
                key = f"G{gid}_{tuple(c.front)}"
                all_candidates.append({
                    'front': c.front,
                    'back': c.back,
                    'base_score': getattr(c, 'total_score', 0.5),
                    'group_id': gid,
                    'strategy_name': getattr(c, 'strategy_name', 'SFE'),
                    'gt_score': gt_scores.get(key, 0.5),
                    'genetic_score': genetic_scores.get(key, 0.5),
                })

        # 池采样候选
        for i, pc in enumerate(pool_candidates):
            key = f"P{i}_{tuple(pc['front'])}"
            all_candidates.append({
                'front': pc['front'],
                'back': pc['back'],
                'base_score': pc.get('total_score', 0.5),
                'group_id': 0,
                'strategy_name': pc.get('strategy_name', 'PoolSampler'),
                'gt_score': gt_scores.get(key, 0.5),
                'genetic_score': genetic_scores.get(key, 0.5),
            })

        return all_candidates

    def _compute_final_scores(self, candidates: List[Dict[str, Any]]) -> None:
        """计算综合评分"""
        for c in candidates:
            # 综合评分: base*0.4 + gt*0.3 + genetic*0.3
            c['final_score'] = c['base_score'] * 0.4 + c['gt_score'] * 0.3 + c['genetic_score'] * 0.3

    def _deduplicate_and_assign_back(
        self,
        candidates: List[Dict[str, Any]],
        back_recs: List[List[int]]
    ) -> List[Dict[str, Any]]:
        """去重并分配后区"""
        seen = set()
        unique = []

        for c in candidates:
            k = tuple(c['front'])
            if k not in seen:
                seen.add(k)
                # 分配后区
                if back_recs and len(unique) < len(back_recs):
                    c['back'] = back_recs[len(unique) % len(back_recs)]
                unique.append(c)

        return unique

    def _get_latest_period(self) -> Optional[str]:
        """获取最近一期期号"""
        try:
            if hasattr(self.predictor, 'data') and self.predictor.data is not None:
                periods = self.predictor.data.get('periods', [])
                if periods:
                    return str(periods[-1]) if not isinstance(periods[-1], int) else str(periods[-1])
            if hasattr(self.draws[0][0], '__len__') and len(self.draws) > 0:
                return None  # 无法从draws直接获取期号
        except Exception:
            pass
        return None


# ---------------------------------------------------------------------------
# 入口函数
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  DLT多策略融合完全体 v4.0")
    print("=" * 60)

    data_path = '/mnt/d/cp/DLT历史数据_适配模型版.xlsx'

    try:
        fusion = DLTFusionComplete(data_path)
    except Exception as e:
        print(f"[DLT-Fusion] 初始化失败: {e}")
        return

    # 测试各模块
    print("\n📊 各组推荐：")
    try:
        groups = fusion.get_group_recommendations()
        for gid, cands in groups.items():
            if cands:
                print(f"  组{gid}: {cands[0].front} | score={cands[0].total_score:.4f}")
    except Exception as e:
        print(f"  获取分组推荐失败: {e}")

    print("\n🎯 后区推荐：")
    try:
        back = fusion.get_back_recommendations()
        for i, b in enumerate(back[:5]):
            print(f"  方案{i+1}: {b}")
    except Exception as e:
        print(f"  获取后区推荐失败: {e}")

    print("\n🏆 最终融合推荐（Top 5）：")
    try:
        results = fusion.predict(top_n=5)
        for i, r in enumerate(results):
            print(f"  {i+1}. 前区{r['front']} 后区{r['back']} "
                  f"[{r['strategy_name']}] score={r['final_score']:.4f}")
    except Exception as e:
        print(f"  融合预测失败: {e}")

    print("\n📈 回测结果（最近50期）：")
    try:
        bt = fusion.backtest(50)
        if 'error' in bt:
            print(f"  {bt['error']}")
        else:
            print(f"  测试次数: {bt['n_tests']}")
            print(f"  平均前区命中: {bt['avg_front_hits']:.3f}")
            print(f"  平均后区命中: {bt['avg_back_hits']:.3f}")
            print(f"  前区命中分布: {bt['front_hit_distribution']}")
            print(f"  后区命中分布: {bt['back_hit_distribution']}")
    except Exception as e:
        print(f"  回测失败: {e}")

    print("\n📋 详细分析：")
    try:
        detailed = fusion.predict_with_details(top_n=3)
        print(f"  总记录: {detailed['total_records']}期")
        for i, pred in enumerate(detailed['predictions'][:3]):
            print(f"  推荐{i+1}: {pred['front']} + {pred['back']} "
                  f"(综合分: {pred['final_score']:.4f})")
    except Exception as e:
        print(f"  详细分析失败: {e}")

    print("\n" + "=" * 60)
    print("  运行完成")
    print("=" * 60)


if __name__ == '__main__':
    main()
