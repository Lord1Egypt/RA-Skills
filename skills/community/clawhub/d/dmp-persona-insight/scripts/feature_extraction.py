#!/usr/bin/env python3
"""
特征识别标准化模块 v7.0

实现 dmp-persona-insight 技能的核心特征识别算法：
- 三步法特征筛选（TGI ≥ 1.0 → 占比排序 → 取前40%）
- 并列核心特征识别
- 互斥关系处理
- 无区分度特征排除

作者：OpenClaw AI Assistant
版本：7.0
日期：2026-03-30
"""

from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class FeatureExtractor:
    """标准特征识别提取器"""
    
    def __init__(self, min_tgi: float = 1.0, parallel_tgi_diff: float = 0.2):
        """
        初始化特征提取器
        
        Args:
            min_tgi: TGI 最低阈值（默认 1.0）
            parallel_tgi_diff: 并列特征的 TGI 最大差值（默认 0.2）
        """
        self.min_tgi = min_tgi
        self.parallel_tgi_diff = parallel_tgi_diff
        
        # 互斥关系对（可扩展）
        self.mutually_exclusive_pairs = [
            ("苹果", "安卓"), ("苹果", "Android"), ("苹果", "华为"),
            ("iOS", "Android"), ("iOS", "安卓"),
            ("一二线城市", "三四线城市"), ("一线城市", "二线城市"),
            ("男性", "女性"), ("男", "女"),
            ("年轻", "中年"), ("18-25岁", "35-45岁"),
        ]
    
    def sort_features(self, features: List[Dict]) -> List[Dict]:
        """
        排序特征：主排序 TGI，次排序占比
        
        Args:
            features: 特征列表 [{'name': '', 'tgi': 1.5, 'coverage': 0.1}, ...]
            
        Returns:
            排序后的特征列表
        """
        return sorted(
            features,
            key=lambda x: (
                -x.get('tgi', 0),  # TGI 降序（主）
                -x.get('coverage', 0)  # 占比降序（次）
            )
        )
    
    def filter_by_tgi(self, features: List[Dict], min_tgi: Optional[float] = None) -> List[Dict]:
        """
        第1步：筛选 TGI ≥ min_tgi 的特征
        
        Args:
            features: 特征列表
            min_tgi: TGI 最低阈值（默认使用初始化的值）
            
        Returns:
            已筛选的特征列表
        """
        min_tgi = min_tgi or self.min_tgi
        valid = [f for f in features if f.get('tgi', 0) >= min_tgi]
        
        logger.info(f"第1步 TGI筛选：{len(features)} → {len(valid)} 条（≥{min_tgi}）")
        
        return valid
    
    def calculate_core_feature_count(self, total_count: int) -> int:
        """
        第3步：根据维度大小计算核心特征数
        
        规则：
        - 大维度（>50）：最多 20 条
        - 中维度（20-50）：40%
        - 小维度（<20）：至少 5 条
        
        Args:
            total_count: 有效特征总数
            
        Returns:
            应该保留的核心特征数
        """
        if total_count > 50:
            core_count = min(int(total_count * 0.4), 20)
            rule = "大维度（最多20）"
        elif total_count >= 20:
            core_count = int(total_count * 0.4)
            rule = "中维度（40%）"
        else:
            core_count = max(int(total_count * 0.4), 5)
            rule = "小维度（至少5）"
        
        logger.info(f"第3步 取前40%：{total_count} 条 → {core_count} 条 ({rule})")
        
        return core_count
    
    def extract_core_features(self, features: List[Dict]) -> List[Dict]:
        """
        执行完整的三步法特征筛选
        
        步骤：
        1. 按 TGI 降序排列
        2. 筛选 TGI ≥ 1.0
        3. 取前 40%（动态阈值）
        
        Args:
            features: 原始特征列表
            
        Returns:
            核心特征列表
        """
        logger.info("=== 开始三步法特征筛选 ===")
        
        # 步骤 1：排序
        sorted_features = self.sort_features(features)
        logger.info(f"排序完成：{len(sorted_features)} 条特征")
        
        # 步骤 2：筛选 TGI ≥ 1.0
        valid_features = self.filter_by_tgi(sorted_features)
        
        if not valid_features:
            logger.warning("筛选后无有效特征！")
            return []
        
        # 步骤 3：取前 40%
        core_count = self.calculate_core_feature_count(len(valid_features))
        core_features = valid_features[:core_count]
        
        logger.info(f"三步法筛选完成：{len(core_features)} 条核心特征")
        
        return core_features
    
    def identify_parallel_features(self, features: List[Dict]) -> Dict[int, List[Dict]]:
        """
        识别并列核心特征
        
        条件（3 个同时满足）：
        1. TGI 差异 ≤ 0.2
        2. 占比比例 < 1:1.5
        3. 均高于维度平均值
        
        Args:
            features: 特征列表（已排序）
            
        Returns:
            {group_idx: [features]} 的字典
        """
        if not features or len(features) < 2:
            return {}
        
        # 计算平均 TGI
        avg_tgi = sum(f.get('tgi', 0) for f in features) / len(features)
        
        parallel_groups = {}
        processed = set()
        
        for i in range(len(features)):
            if i in processed:
                continue
            
            group = [features[i]]
            processed.add(i)
            
            for j in range(i + 1, len(features)):
                if j in processed:
                    continue
                
                f1, f2 = features[i], features[j]
                
                # 条件 1：TGI 差异 ≤ 0.2
                tgi_diff = f1.get('tgi', 0) - f2.get('tgi', 0)
                if tgi_diff > self.parallel_tgi_diff:
                    break  # TGI 已差异过大，后续更大
                
                # 条件 2：占比比例 < 1:1.5
                cov1 = f1.get('coverage', 0)
                cov2 = f2.get('coverage', 0)
                if cov1 > 0 and cov2 > 0:
                    coverage_ratio = cov1 / cov2
                    if coverage_ratio >= 1.5:
                        continue  # 占比差异过大
                
                # 条件 3：均高于平均值
                if f2.get('tgi', 0) > avg_tgi:
                    group.append(f2)
                    processed.add(j)
            
            if len(group) > 1:
                parallel_groups[i] = group
                logger.info(f"并列特征组 {i}：{[f['name'] for f in group]}")
        
        return parallel_groups
    
    def handle_mutually_exclusive(self, features: List[Dict]) -> List[Dict]:
        """
        处理互斥特征：保留 TGI 更高者，排除 TGI 较低者
        
        Args:
            features: 特征列表
            
        Returns:
            已处理互斥关系的特征列表
        """
        features_to_remove = set()
        
        for feat1_keyword, feat2_keyword in self.mutually_exclusive_pairs:
            f1 = next((f for f in features if feat1_keyword in f['name']), None)
            f2 = next((f for f in features if feat2_keyword in f['name']), None)
            
            if f1 and f2 and f1['name'] != f2['name']:
                # 保留 TGI 较高的
                if f1['tgi'] > f2['tgi']:
                    features_to_remove.add(f2['name'])
                    logger.info(f"互斥处理：移除 {f2['name']} (TGI {f2['tgi']:.2f})，保留 {f1['name']} (TGI {f1['tgi']:.2f})")
                else:
                    features_to_remove.add(f1['name'])
                    logger.info(f"互斥处理：移除 {f1['name']} (TGI {f1['tgi']:.2f})，保留 {f2['name']} (TGI {f2['tgi']:.2f})")
        
        return [f for f in features if f['name'] not in features_to_remove]
    
    def remove_low_discrimination_features(self, features: List[Dict]) -> List[Dict]:
        """
        移除无区分度特征
        
        判断标准：同时满足
        1. TGI 比值 0.9-1.1
        2. 占比比值 0.9-1.1
        
        处理方式：同时排除两个（保守处理）
        
        Args:
            features: 特征列表
            
        Returns:
            已移除低区分度特征的列表
        """
        features_to_remove = set()
        
        for i in range(len(features)):
            for j in range(i + 1, len(features)):
                f1, f2 = features[i], features[j]
                
                tgi1, tgi2 = f1.get('tgi', 0), f2.get('tgi', 0)
                cov1, cov2 = f1.get('coverage', 0), f2.get('coverage', 0)
                
                if tgi1 == 0 or tgi2 == 0 or cov1 == 0 or cov2 == 0:
                    continue
                
                # 计算比值
                tgi_ratio = min(tgi1, tgi2) / max(tgi1, tgi2)
                coverage_ratio = min(cov1, cov2) / max(cov1, cov2)
                
                # 两个条件同时满足
                if 0.9 <= tgi_ratio <= 1.1 and 0.9 <= coverage_ratio <= 1.1:
                    features_to_remove.add(f1['name'])
                    features_to_remove.add(f2['name'])
                    logger.info(f"无区分度移除：{f1['name']} (TGI {tgi1:.2f}, cov {cov1:.2%}) 和 {f2['name']} (TGI {tgi2:.2f}, cov {cov2:.2%})")
        
        return [f for f in features if f['name'] not in features_to_remove]
    
    def extract_dimension_features(self, dimension_name: str, features: List[Dict]) -> Tuple[List[Dict], Dict]:
        """
        完整的维度特征提取流程
        
        Args:
            dimension_name: 维度名称
            features: 原始特征列表
            
        Returns:
            (核心特征列表, 统计信息)
        """
        logger.info(f"\n========== {dimension_name} 维度特征提取 ==========")
        
        # 步骤 1-3：三步法
        core_features = self.extract_core_features(features)
        
        if not core_features:
            return [], {'dimension': dimension_name, 'total': len(features), 'core': 0}
        
        # 步骤 4：识别并列特征
        parallel_groups = self.identify_parallel_features(core_features)
        
        # 步骤 5：处理互斥关系
        core_features = self.handle_mutually_exclusive(core_features)
        
        # 步骤 6：移除无区分度
        core_features = self.remove_low_discrimination_features(core_features)
        
        # 统计信息
        stats = {
            'dimension': dimension_name,
            'total': len(features),
            'valid': len([f for f in features if f.get('tgi', 0) >= self.min_tgi]),
            'core': len(core_features),
            'parallel_groups': len(parallel_groups),
            'avg_tgi': sum(f.get('tgi', 0) for f in core_features) / len(core_features) if core_features else 0,
            'max_tgi': max((f.get('tgi', 0) for f in core_features), default=0),
        }
        
        logger.info(f"维度特征提取完成：{len(core_features)} 条核心特征")
        logger.info(f"统计：总计 {stats['total']} → 有效 {stats['valid']} → 核心 {stats['core']}")
        
        return core_features, stats


# 使用示例
if __name__ == '__main__':
    import json
    
    # 配置日志
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    # 示例数据
    sample_features = [
        {'name': '母婴', 'tgi': 1.90, 'coverage': 0.12},
        {'name': '健康运动', 'tgi': 1.42, 'coverage': 0.08},
        {'name': '教育学习', 'tgi': 1.32, 'coverage': 0.09},
        {'name': '生活服务', 'tgi': 1.24, 'coverage': 0.07},
        {'name': '汽车', 'tgi': 1.23, 'coverage': 0.06},
        {'name': '旅游', 'tgi': 1.15, 'coverage': 0.05},
        {'name': '购物', 'tgi': 1.08, 'coverage': 0.10},
        {'name': '美食', 'tgi': 1.05, 'coverage': 0.09},
        {'name': '体育', 'tgi': 0.98, 'coverage': 0.04},
        {'name': '娱乐', 'tgi': 0.87, 'coverage': 0.03},
    ]
    
    # 创建提取器并执行
    extractor = FeatureExtractor()
    core_features, stats = extractor.extract_dimension_features('兴趣偏好', sample_features)
    
    print("\n=== 最终核心特征 ===")
    for i, feat in enumerate(core_features, 1):
        print(f"{i}. {feat['name']:15} | TGI: {feat['tgi']:.2f} | 占比: {feat['coverage']:.2%}")
    
    print("\n=== 统计信息 ===")
    print(json.dumps(stats, ensure_ascii=False, indent=2))
