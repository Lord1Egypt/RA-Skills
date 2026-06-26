# DLT大乐透预测技能 - Python包入口 v4.0
# 多策略融合完全体，所有模块统一从这里导出

# 确保本包目录在模块搜索路径最前面
import sys as _sys
import os as _os
_pkg_dir = _os.path.dirname(_os.path.abspath(__file__))
if _pkg_dir not in _sys.path:
    _sys.path.insert(0, _pkg_dir)

# ============================================================
# 核心预测器
# ============================================================
from dlt_predictor_upgraded import DLTPredictorUpgraded as DLTPredictor, predict_6_plus_4_v3

# ============================================================
# 多策略融合引擎（v3.0/v4.0 核心）
# ============================================================
from strategy_fusion_engine import StrategyFusionEngine
from five_pool_sampler_complete_final import FivePoolSampler
from dlt_back_fusion import BackZoneFusion, BACK_STRATEGY

# ============================================================
# 多融合管道
# ============================================================
from dlt_multi_fusion_pipeline import (
    DLTMultiFusionPipeline,
    PipelineResult,
    FusionReport,
    predict as dlt_predict,
)

# ============================================================
# 数学与博弈论工具
# ============================================================
from modules.dlt_game_theory import DLTGameTheoryAnalyzer
from modules.dlt_genetic_optimizer import DLTGeneticOptimizer
from modules.dlt_math_filter import DLTMathFilter
from modules.dlt_statistics_analyzer import DLTStatisticsAnalyzer
from modules.dlt_kill_number import DLTKillNumber as DLTKillNumberAnalyzer

# ============================================================
# 兼容旧接口（v1/v2）
# ============================================================
from dlt_five_pool_fusion import FivePoolFusion
from dlt_ranking_output import DLTRankingOutput, Recommendation, GROUP_CONFIGS
from dlt_strategy_fusion_v2 import (
    FeatureScorer,
    ConstraintChecker,
    FUSION_GROUPS,
)

__all__ = [
    # 核心预测器
    'DLTPredictor',
    'predict_6_plus_4_v3',
    # 多策略融合引擎
    'StrategyFusionEngine',
    'FivePoolSampler',
    'BackZoneFusion',
    'BACK_STRATEGY',
    # 多融合管道
    'DLTMultiFusionPipeline',
    'PipelineResult',
    'FusionReport',
    'dlt_predict',
    # 数学与博弈论
    'DLTGameTheoryAnalyzer',
    'DLTGeneticOptimizer',
    'DLTMathFilter',
    'DLTStatisticsAnalyzer',
    'DLTKillNumberAnalyzer',
    # 兼容层
    'FivePoolFusion',
    'DLTRankingOutput',
    'Recommendation',
    'GROUP_CONFIGS',
    'FeatureScorer',
    'ConstraintChecker',
    'FUSION_GROUPS',
]
