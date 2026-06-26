#!/usr/bin/env python3
"""
DLT彩票预测技能 - OpenClaw技能封装
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Any, Optional

# 添加技能模块路径
skill_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(skill_dir, "modules"))

# 尝试导入模块，如果失败则设置为 None
DLTDataLoader = None
DLTFeatureExtractor = None
DLTRulesValidator = None
DLTPredictor = None
DLTTrainer = None
DLTBacktester = None
DLTDataValidator = None
DLTDataRepair = None
DLT_RULES = None
COLUMN_NAMES = None
generate_compound_predictions = None
generate_all_compound_types = None
format_compound_report = None
ALL_COMPOUND_TYPES = None
compound_info = None

# 尝试导入融合引擎（这个应该存在）
try:
    from dlt_strategy_fusion_v2 import StrategyFusionEngine, FUSION_GROUPS, FusionGroup
    print("✅ DLT融合引擎导入成功")
except ImportError as e:
    print(f"❌ DLT融合引擎导入失败: {e}")
    StrategyFusionEngine = None
    FUSION_GROUPS = None
    FusionGroup = None

# 尝试导入其他模块
for module_name in [
    'dlt_data_loader', 'dlt_feature_extractor', 'dlt_rules_validator',
    'dlt_predictor', 'dlt_trainer', 'dlt_backtester',
    'dlt_smart_data_validator', 'dlt_data_repair', 'dlt_validation_config',
    'dlt_compound_betting'
]:
    try:
        exec(f'from {module_name} import *', globals())
        print(f"  ✅ {module_name} 导入成功")
    except ImportError:
        print(f"  ⚠️  {module_name} 导入失败（使用None替代）")


class DLTLotterySkill:
    """DLT彩票预测技能主类"""

    def __init__(self, config_path: Optional[str] = None):
        """初始化技能

        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self._init_components()

        # 直接加载数据（融合引擎predict需要）
        try:
            import pandas as pd
            DATA_PATH = self.config.get('data_file_path', '/mnt/d/cp/DLT历史数据_适配模型版.xlsx')
            df = pd.read_excel(DATA_PATH)
            # 自动检测列名格式（中文"前区1" 或 英文"front_1"）
            if '前区' in df.columns:
                self.front_draws = df['前区'].values.tolist()
                self.back_draws = df['后区'].values.tolist()
            elif '前区1' in df.columns:
                front_cols = [f'前区{i}' for i in range(1, 6)]
                back_cols = [f'后区{i}' for i in range(1, 3)]
                self.front_draws = df[front_cols].values.tolist()
                self.back_draws = df[back_cols].values.tolist()
            elif 'front_1' in df.columns:
                front_cols = [f'front_{i}' for i in range(1, 6)]
                back_cols = [f'back_{i}' for i in range(1, 3)]
                self.front_draws = df[front_cols].values.tolist()
                self.back_draws = df[back_cols].values.tolist()
            else:
                raise ValueError(f"未知列名格式: {df.columns.tolist()[:10]}")
            print(f"  ✅ 数据直接加载: {len(self.front_draws)}期")
        except Exception as e:
            print(f"  ⚠️ 数据加载失败: {e}")
            self.front_draws = []
            self.back_draws = []

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """加载配置"""
        default_config = {
            "data_file_path": "/mnt/d/cp/DLT历史数据_适配模型版.xlsx",
            "front_range": [1, 35],
            "back_range": [1, 12],
            "prediction_format": {
                "front_count": 5,
                "back_count": 2
            },
            "hit_standard": {
                "front_hit": 4,
                "back_hit": 1
            }
        }

        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                # 合并配置
                default_config.update(user_config)
                print(f"✅ 从 {config_path} 加载配置")
            except Exception as e:
                print(f"⚠️  配置文件加载失败,使用默认配置: {e}")

        return default_config

    def _init_components(self):
        """初始化技能组件"""
        print("初始化DLT彩票预测技能组件...")

        # 数据加载器
        try:
            self.data_loader = DLTDataLoader()
            print("  ✅ 数据加载器初始化完成")
        except Exception as e:
            self.data_loader = None
            print(f"  ⚠️  数据加载器初始化失败: {e}")

        # 高级数据检测器
        try:
            self.data_validator = DLTDataValidator()
            print("  ✅ 智能数据验证器初始化完成")
        except Exception as e:
            self.data_validator = None
            print(f"  ⚠️  智能数据验证器初始化失败: {e}")

        # 数据修复器
        try:
            self.data_repairer = DLTDataRepair()
            print("  ✅ 数据修复器初始化完成")
        except Exception as e:
            self.data_repairer = None
            print(f"  ⚠️  数据修复器初始化失败: {e}")

        # 特征提取器
        try:
            self.feature_extractor = DLTFeatureExtractor()
            print("  ✅ 特征提取器初始化完成")
        except Exception as e:
            self.feature_extractor = None
            print(f"  ⚠️  特征提取器初始化失败: {e}")

        # 规则验证器
        try:
            self.rules_validator = DLTRulesValidator()
            print("  ✅ 规则验证器初始化完成")
        except Exception as e:
            self.rules_validator = None
            print(f"  ⚠️  规则验证器初始化失败: {e}")

        # 预测器
        try:
            self.predictor = DLTPredictor()
            print("  ✅ 预测器初始化完成")
        except Exception as e:
            self.predictor = None
            print(f"  ⚠️  预测器初始化失败: {e}")

        # 训练器
        try:
            self.trainer = DLTTrainer()
            print("  ✅ 训练器初始化完成")
        except Exception as e:
            self.trainer = None
            print(f"  ⚠️  训练器初始化失败: {e}")

        # 回测器
        try:
            self.backtester = DLTBacktester()
            print("  ✅ 回测器初始化完成")
        except Exception as e:
            self.backtester = None
            print(f"  ⚠️  回测器初始化失败: {e}")

        # 预缓存数据(用于查询)
        self._loaded_data = None
        self._query_ready = False

        print("✅ 所有技能组件初始化完成（部分组件可能不可用）")

    def _build_candidate_pool(self, data, top_k: int = 15) -> tuple:
        """从最近数据构建候选池（绕过ML模型超时问题）"""
        from collections import Counter
        front_cols = [f'front_{i}' for i in range(1, 6)]
        back_cols = [f'back_{i}' for i in range(1, 3)]
        recent = data.tail(top_k)
        fc = Counter()
        bc = Counter()
        for _, row in recent.iterrows():
            for c in front_cols:
                fc[int(row[c])] += 1
            for c in back_cols:
                bc[int(row[c])] += 1
        hot_front = [n for n, _ in fc.most_common(12)]
        hot_back = [n for n, _ in bc.most_common(7)]
        return hot_front, hot_back

    def predict_compound(
        self,
        front_compound: int = 6,
        back_compound: int = 3,
        group_count: int = 5,
        compound_types: List[tuple] = None
    ) -> Dict[str, Any]:
        """生成复式投注预测

        Args:
            front_compound: 默认前区复式数（单类型时使用）
            back_compound: 默认后区复式数（单类型时使用）
            group_count: 每种类型生成多少组
            compound_types: 指定复式类型列表，如[(6,3),(7,2),(8,4)]
                           如果为None，则使用单类型(front_compound, back_compound)

        Returns:
            包含复式预测结果的字典
        """
        print(f"🔮 开始DLT复式投注预测...")
        try:
            data = self.data_loader.load_data()
            print(f"  数据加载: {len(data)}期")
            front_pool, back_pool = self._build_candidate_pool(data)
            print(f"  候选池: 前区{len(front_pool)}个 {front_pool}")
            print(f"          后区{len(back_pool)}个 {back_pool}")

            latest = data.iloc[-1]
            period = int(latest['period']) + 1

            if compound_types is None:
                compound_types = [(front_compound, back_compound)]

            report = generate_all_compound_types(
                front_pool, back_pool,
                compound_types=compound_types,
                groups_per_type=group_count
            )

            latest_draw = {f'front_{i}': int(latest[f'front_{i}']) for i in range(1, 6)}
            latest_draw.update({f'back_{i}': int(latest[f'back_{i}']) for i in range(1, 3)})

            text = format_compound_report(report, period, latest_draw)
            print(f"\n{text}")

            return {"report": report, "period": period, "text": text}
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"error": str(e)}

    def predict(self, n_per_group: int = 1, strategy: str = 'all') -> Dict:
        """
        生成预测结果（基于融合引擎 v2）

        Args:
            n_per_group: 每组生成数量
            strategy: 'all' 或 1-5（指定组别）

        Returns:
            包含推荐号码和策略信息的字典
        """
        try:
            import pandas as pd

            # 直接从 Excel 加载历史数据
            data_path = "/mnt/d/cp/DLT历史数据_适配模型版.xlsx"
            df = pd.read_excel(data_path)

            if len(df) < 10:
                return {'error': '历史数据不足', 'draws': len(df)}

            # 构建 draw 格式：list of (front_list, back_list)
            draws = []
            for _, row in df.iterrows():
                front = [int(row['前区1']), int(row['前区2']), int(row['前区3']),
                         int(row['前区4']), int(row['前区5'])]
                back = [int(row['后区1']), int(row['后区2'])]
                draws.append((front, back))

            # 使用 v2 融合引擎
            fusion_engine = StrategyFusionEngine(draws)

            if strategy == 'all':
                results = fusion_engine.select_and_rank(n_per_group)
                recommendations = [results[gid][0] if results.get(gid) else None for gid in range(1, 6)]
                recommendations = [r for r in recommendations if r is not None]
            else:
                gid = int(strategy)
                results = getattr(fusion_engine, f'generate_group_{gid}')(n_per_group)
                recommendations = results

            if not recommendations:
                return {'error': '生成失败'}

            group_names = ['稳中求胜', '冷号反弹', '连号追击', '区间聚焦', '黄金组合']
            output = {
                'total_draws': len(draws),
                'strategy': strategy,
                'recommendations': []
            }

            for i, (front, back) in enumerate(recommendations, 1):
                gid = int(strategy) if strategy != 'all' else i
                output['recommendations'].append({
                    'group': gid,
                    'name': group_names[gid - 1],
                    'front': front,
                    'back': back,
                    'front_str': ','.join(map(str, front)),
                    'back_str': ','.join(map(str, back)),
                })

            return output

        except Exception as e:
            import traceback
            return {'error': str(e), 'trace': traceback.format_exc()}

    def validate(self, front_numbers: List[int], back_numbers: List[int]) -> Dict[str, Any]:
        """验证预测结果格式

        Args:
            front_numbers: 前区号码列表
            back_numbers: 后区号码列表

        Returns:
            验证结果
        """
        print(f"🔍 验证预测结果格式: {front_numbers} + {back_numbers}")

        try:
            result = self.rules_validator.validate_prediction_format(front_numbers, back_numbers)

            if result['format_valid']:
                print(f"✅ 格式验证通过")
                if result['meets_format_requirement']:
                    print(f"✅ 满足格式要求: 前区≥5个 + 后区≥2个")
                else:
                    print(f"⚠️  格式要求: 前区≥5个 + 后区≥2个 (当前: 前区{result['front_count']}个, 后区{result['back_count']}个)")
            else:
                print(f"❌ 格式验证失败")
                for error in result['errors']:
                    print(f"  错误: {error}")

            return result

        except Exception as e:
            print(f"❌ 验证失败: {e}")
            return {'format_valid': False, 'valid': False, 'errors': [str(e)]}

    def train(self, epochs: int = 100) -> Dict[str, Any]:
        """训练DLT预测模型

        Args:
            epochs: 训练轮数

        Returns:
            训练结果
        """
        print(f"🏋️  开始训练DLT预测模型 (epochs={epochs})...")

        try:
            # 加载数据
            data = self.data_loader.load_data()
            print(f"  数据加载成功: {len(data)} 期")

            # 提取特征
            features, feature_names = self.feature_extractor.extract_all_features(data)
            print(f"  特征提取成功: {len(feature_names)} 个特征")

            # 训练模型
            result = self.trainer.train(data, features, epochs=epochs)

            if result['success']:
                print(f"✅ 模型训练完成")
                print(f"  训练轮数: {result['epochs']}")
                print(f"  最终损失: {result['final_loss']:.6f}")
                print(f"  训练时间: {result['training_time']:.2f}秒")
                print(f"  模型保存到: {result['model_path']}")
            else:
                print(f"❌ 模型训练失败: {result.get('error', '未知错误')}")

            return result

        except Exception as e:
            print(f"❌ 训练失败: {e}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e)}

    def backtest(self, periods: int = 50) -> Dict[str, Any]:
        """回测模型性能

        Args:
            periods: 回测期数

        Returns:
            回测结果
        """
        print(f"📊 开始回测DLT模型性能 (periods={periods})...")

        try:
            # 加载数据
            data = self.data_loader.load_data()
            print(f"  数据加载成功: {len(data)} 期")

            # 执行回测
            result = self.backtester.run_backtest(data, test_periods=periods)
            summary = result.get('performance_summary', {})

            print(f"✅ 回测完成")
            print(f"  回测期数: {result.get('test_config', {}).get('test_periods', 0)}")
            avg_front = summary.get('front_hit_rate_mean', 0) * 5
            avg_back = summary.get('back_hit_rate_mean', 0) * 2
            print(f"  平均命中: 前区{avg_front:.2f}个, 后区{avg_back:.2f}个")
            print(f"  达标率: {summary.get('meets_standard_rate', 0):.2%}")

            return {'success': True, 'summary': summary, 'report': result}

        except Exception as e:
            print(f"❌ 回测失败: {e}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e)}

    def get_info(self) -> Dict[str, Any]:
        """获取技能信息"""
        return {
            'skill_name': 'dlt-lottery-prediction',
            'version': '1.0.0',
            'description': '中国体育彩票超级大乐透(DLT)预测技能',
            'constraints': [
                '文件路径硬编码:D:\\cp\\DLT历史数据_适配模型版.xlsx',
                '彩票规则严格遵守:前区1-35选5,后区1-12选2',
                '预测格式验证:前区≥5个不同号码 + 后区≥2个不同号码',
                '命中标准:前区≥4个命中 + 后区≥1个命中',
                '数据倒序处理:Excel文件中的数据已经是倒序排列',
                '技能完全分离:不与SSQ技能交叉使用数据或规则'
            ],
            'components': [
                'DLTDataLoader - 数据加载器',
                'DLTDataValidator - 智能数据验证器',
                'DLTDataRepair - 数据修复器',
                'DLTFeatureExtractor - 特征提取器',
                'DLTRulesValidator - 规则验证器',
                'DLTPredictor - 预测器',
                'DLTTrainer - 训练器',
                'DLTBacktester - 回测器'
            ]
        }

    # ==================== 高级数据检测与查询功能 ====================

    def validate_data(self, file_path: Optional[str] = None) -> Dict[str, Any]:
        """智能数据验证 - 多层检测、自动修复、生成报告

        Args:
            file_path: 数据文件路径,默认使用配置路径

        Returns:
            验证报告字典(状态/文件信息/问题/修复/数据摘要)
        """
        print("🔍 开始智能数据验证...")
        status, data, report = self.data_validator.validate_and_load(file_path)
        print(f"  验证状态: {status}")
        s = report.get('summary', {})
        print(f"  错误={s.get('errors',0)} 警告={s.get('warnings',0)} 修复={s.get('repairs',0)}")
        di = report.get('data_info', {})
        if di:
            print(f"  数据: {di.get('total_rows','N/A')}期 范围={di.get('date_range','N/A')}")
        return report

    def query_period(self, period) -> Optional[Dict[str, Any]]:
        """智能查询指定期号数据

        Args:
            period: 期号(支持 26010 / "26010" / 26010.0 / "26010.0")

        Returns:
            期号数据字典(period/front/back/row_index/elapsed_ms),未找到返回None
        """
        if not self._query_ready:
            # 自动加载并构建索引
            report = self.validate_data()
            if report.get('status') not in ('success', 'warning'):
                print(f"  ❌ 数据验证失败,无法查询: {report.get('status')}")
                return None
            self._query_ready = True
        result = self.data_validator.query_period(period)
        if result:
            print(f"  ✅ 找到 {result['period']}: 前区={result['front']} 后区={result['back']} ({result['elapsed_ms']}ms)")
        else:
            print(f"  ❌ 未找到期号 {period}")
        return result

    def query_periods(self, periods: List) -> List[Dict[str, Any]]:
        """批量查询期号数据

        Args:
            periods: 期号列表

        Returns:
            查询结果列表
        """
        if not self._query_ready:
            report = self.validate_data()
            if report.get('status') not in ('success', 'warning'):
                return []
            self._query_ready = True
        results = self.data_validator.query_periods(periods)
        print(f"  📊 批量查询完成: {len(results)} 个期号")
        return results

    def find_by_number(self, *numbers) -> Optional[Dict[str, Any]]:
        """通过号码反查期号

        Args:
            numbers: 5个前区+2个后区号码,共7个

        Returns:
            匹配期号信息
        """
        if not self._query_ready:
            report = self.validate_data()
            if report.get('status') not in ('success', 'warning'):
                return None
            self._query_ready = True
        result = self.data_validator.find_by_number(*numbers)
        if result:
            print(f"  ✅ 号码匹配到期号: {result['period']}")
        else:
            print(f"  ❌ 未找到匹配的期号")
        return result

    def get_data_summary(self) -> Dict[str, Any]:
        """获取数据摘要统计

        Returns:
            摘要信息(数据量/期号范围/统计指标)
        """
        if not self._query_ready:
            report = self.validate_data()
            if report.get('status') not in ('success', 'warning'):
                return {}
            self._query_ready = True
        df = self.data_validator._data
        if df is None:
            return {}
        pcol = COLUMN_NAMES['period']
        fc = COLUMN_NAMES['front']
        bc = COLUMN_NAMES['back']

        all_front = []
        for c in fc:
            if c in df.columns:
                all_front.extend(df[c].dropna().astype(int).tolist())

        all_back = []
        for c in bc:
            if c in df.columns:
                all_back.extend(df[c].dropna().astype(int).tolist())

        summary = {
            'total_periods': len(df),
            'date_range': f"{df[pcol].iloc[0]}~{df[pcol].iloc[-1]}" if len(df) > 0 else 'N/A',
            'front_range': [min(all_front), max(all_front)] if all_front else [],
            'back_range': [min(all_back), max(all_back)] if all_back else [],
            'ordering': '倒序(最新在前)'
        }

        # 计算冷热号
        if all_front:
            from collections import Counter
            front_counter = Counter(all_front)
            sorted_front = sorted(front_counter.items(), key=lambda x: x[1], reverse=True)
            summary['hottest_front3'] = [x[0] for x in sorted_front[:3]]
            summary['coldest_front3'] = [x[0] for x in sorted_front[-3:]]

        print(f"  📊 数据摘要: {len(df)}期 ({summary['date_range']})")
        return summary

    def check_data_quality(self, file_path: Optional[str] = None) -> Dict[str, Any]:
        """数据质量检测(仅检查,不加载)

        Returns:
            详细检测报告
        """
        print("🔍 数据质量检查(仅检查模式)...")
        report = self.data_validator.check_only(file_path)
        print(f"  状态: {report['status']}")
        vr = report.get('validation_results', {})
        for name, result in vr.items():
            icon = "✅" if result.get('passed') else "❌"
            print(f"  {icon} {name}: {result.get('message', '')}")
        return report


def main():
    """命令行入口点"""
    parser = argparse.ArgumentParser(description='DLT彩票预测技能')
    parser.add_argument('command',
                       choices=['predict', 'validate', 'train', 'backtest', 'info',
                                'query', 'query_batch', 'validate_data', 'quality_check',
                                'summary', 'find_by_number'],
                       help='技能命令')
    parser.add_argument('--top-k', type=int, default=3,
                       help='预测方案数量(仅predict命令)')
    parser.add_argument('--epochs', type=int, default=100,
                       help='训练轮数(仅train命令)')
    parser.add_argument('--periods', type=int, default=50,
                       help='回测期数(仅backtest命令)')
    parser.add_argument('--front-numbers', type=str,
                       help='前区号码,逗号分隔(仅validate命令)')
    parser.add_argument('--back-numbers', type=str,
                       help='后区号码,逗号分隔(仅validate命令)')
    parser.add_argument('--config', type=str,
                       help='配置文件路径')
    parser.add_argument('--period', type=str, default=None,
                       help='查询期号(query/find_by_number命令)')
    parser.add_argument('--numbers', type=str, default=None,
                       help='7个号码查期号,逗号分隔(find_by_number命令)')
    parser.add_argument('--file', type=str, default=None,
                       help='数据文件路径(validate_data/quality_check命令)')

    args = parser.parse_args()

    # 创建技能实例
    skill = DLTLotterySkill(config_path=args.config)

    # 执行命令
    if args.command == 'predict':
        predictions = skill.predict(top_k=args.top_k)
        print("\n🎯 预测结果汇总:")
        for pred in predictions:
            print(f"  方案 {pred['方案编号']}: {pred['前区号码']} + {pred['后区号码']} (置信度: {pred['置信度']:.4f})")

    elif args.command == 'validate':
        if not args.front_numbers or not args.back_numbers:
            print("❌ 请提供前区和后区号码")
            sys.exit(1)

        front_numbers = [int(x.strip()) for x in args.front_numbers.split(',')]
        back_numbers = [int(x.strip()) for x in args.back_numbers.split(',')]

        result = skill.validate(front_numbers, back_numbers)
        print(f"\n📋 验证结果: {'✅ 通过' if result.get('format_valid', False) else '❌ 失败'}")

    elif args.command == 'train':
        result = skill.train(epochs=args.epochs)
        print(f"\n📋 训练结果: {'✅ 成功' if result.get('success', False) else '❌ 失败'}")

    elif args.command == 'backtest':
        result = skill.backtest(periods=args.periods)
        print(f"\n📋 回测结果: {'✅ 成功' if result.get('success', False) else '❌ 失败'}")

    elif args.command == 'info':
        info = skill.get_info()
        print(f"\n📋 DLT彩票预测技能信息:")
        print(f"  名称: {info['skill_name']}")
        print(f"  版本: {info['version']}")
        print(f"  描述: {info['description']}")
        print(f"  约束条件:")
        for constraint in info['constraints']:
            print(f"    • {constraint}")
        print(f"  组件:")
        for component in info['components']:
            print(f"    • {component}")

    elif args.command == 'validate_data':
        report = skill.validate_data(file_path=args.file)
        print(f"\n📋 数据验证: {report.get('status')}")

    elif args.command == 'quality_check':
        report = skill.check_data_quality(file_path=args.file)
        print(f"\n📋 质量检查完成")

    elif args.command == 'summary':
        summary = skill.get_data_summary()
        print(f"\n📊 数据摘要:")
        for k, v in summary.items():
            print(f"  {k}: {v}")

    elif args.command == 'query':
        if not args.period:
            print("❌ 请提供期号 (--period)")
            sys.exit(1)
        result = skill.query_period(args.period)
        if result:
            print(f"\n📋 查询结果: {result}")
        else:
            print(f"\n❌ 未找到期号 {args.period}")

    elif args.command == 'query_batch':
        if not args.period:
            print("❌ 请提供期号列表 (--period 逗号分隔)")
            sys.exit(1)
        periods = [p.strip() for p in args.period.split(',')]
        results = skill.query_periods(periods)
        for r in results:
            if r:
                print(f"  ✅ {r['period']}: {r['front']} + {r['back']}")
            else:
                print(f"  ❌ 未找到")

    elif args.command == 'find_by_number':
        if not args.numbers:
            print("❌ 请提供7个号码 (--numbers x,x,x,x,x,x,x)")
            sys.exit(1)
        nums = [int(x.strip()) for x in args.numbers.split(',')]
        result = skill.find_by_number(*nums)
        if result:
            print(f"\n📋 反查结果: {result}")
        else:
            print(f"\n❌ 未找到匹配的期号")


if __name__ == "__main__":
    main()