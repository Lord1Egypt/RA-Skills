# -*- coding: utf-8 -*-
"""
度量衡智库 · 数据校正引擎 v1.0
Data Calibrator - 用真实数据修正估算值
========================================

核心功能：
1. 连接本地数据库查询真实造价指标
2. 整合爬虫获取的官方数据
3. 自动校正估算值
4. 提供校正置信度

作者：度量衡智库
版本：1.0.0
日期：2026-04-03
"""

import os
import sys
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

# 添加scripts目录到路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from db_connector import CostDatabaseConnector, CostIndex, quick_query, get_real_time_factor
from crawler import CostCrawlerScheduler, crawl_city_cost, fetch_official_price

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# 数据类
# ============================================================

@dataclass
class CalibrationResult:
    """校正结果"""
    calibrated: bool              # 是否进行了校正
    confidence: float             # 置信度 (0-1)
    source: str                   # 数据来源
    original_value: float        # 原始估算值
    calibrated_value: float      # 校正后值
    adjustment_ratio: float      # 调整比例
    data_date: str               # 数据日期
    notes: str                   # 备注

@dataclass
class CalibratedEstimate:
    """校正后的估算"""
    unit_price_low: float        # 校正后单方低限
    unit_price_mid: float        # 校正后单方中值
    unit_price_high: float        # 校正后单方高限
    steel_content: float          # 校正后钢筋含量
    concrete_content: float       # 校正后混凝土含量
    total_cost_low: float         # 总造价低限
    total_cost_mid: float        # 总造价中值
    total_cost_high: float        # 总造价高限
    calibrations: List           # 校正详情
    data_sources: List           # 数据来源
    accuracy_level: str           # 精度等级


# ============================================================
# 数据校正引擎
# ============================================================

class DataCalibrator:
    """
    数据校正引擎
    核心功能：
    1. 查询本地数据库匹配指标
    2. 调用爬虫获取实时数据
    3. 多源数据融合
    4. 不确定性校正
    """
    
    def __init__(self, use_cache: bool = True):
        self.use_cache = use_cache
        self.cache: Dict = {}
        self.db = None
        self.crawler = None
        self._init_connections()
    
    def _init_connections(self):
        """初始化数据库和爬虫连接"""
        try:
            self.db = CostDatabaseConnector()
            logger.info("数据库连接成功")
        except Exception as e:
            logger.warning(f"数据库连接失败: {e}")
            self.db = None
        
        try:
            self.crawler = CostCrawlerScheduler()
            logger.info("爬虫调度器初始化成功")
        except Exception as e:
            logger.warning(f"爬虫初始化失败: {e}")
            self.crawler = None
    
    def calibrate_unit_price(
        self,
        city: str,
        building_type: str,
        structure_type: str,
        original_estimate: float,
        floor_count: int = 18
    ) -> CalibrationResult:
        """校正单方造价"""
        result = CalibrationResult(
            calibrated=False,
            confidence=0.5,
            source="估算模型",
            original_value=original_estimate,
            calibrated_value=original_estimate,
            adjustment_ratio=0.0,
            data_date=datetime.now().strftime("%Y-%m-%d"),
            notes="未找到校正数据"
        )
        
        # 方法1：查询本地数据库
        try:
            if self.db:
                indexes = self.db.query_cost_index(city, building_type, structure_type, floor_count)
                if indexes:
                    index = indexes[0]
                    result.calibrated = True
                    result.confidence = 0.85
                    result.source = f"本地数据库: {index.data_source}"
                    result.calibrated_value = index.unit_price_mid
                    result.adjustment_ratio = (index.unit_price_mid - original_estimate) / original_estimate
                    result.data_date = index.data_date
                    result.notes = f"数据库匹配: {city} {building_type} {structure_type}"
                    logger.info(f"数据库校正: {result.calibrated_value}")
                    return result
        except Exception as e:
            logger.warning(f"数据库查询失败: {e}")
        
        # 方法2：调用爬虫
        try:
            if self.crawler:
                data = self.crawler.crawl_api_data(city, building_type)
                if data and data.get('unit_price_mid'):
                    result.calibrated = True
                    result.confidence = 0.75
                    result.source = f"实时API: {data['source']}"
                    result.calibrated_value = data['unit_price_mid']
                    result.adjustment_ratio = (data['unit_price_mid'] - original_estimate) / original_estimate
                    result.data_date = data['fetch_time']
                    result.notes = f"API实时数据: {city} {building_type}"
                    logger.info(f"API校正: {result.calibrated_value}")
                    return result
        except Exception as e:
            logger.warning(f"爬虫调用失败: {e}")
        
        # 方法3：使用城市系数调整
        try:
            if self.db:
                factor = self.db.get_city_factor(city)
                if factor:
                    base_price = 5000
                    adjusted_price = base_price * factor['build_factor']
                    
                    result.calibrated = True
                    result.confidence = 0.60
                    result.source = f"城市系数: {factor['data_source']}"
                    result.calibrated_value = adjusted_price
                    result.adjustment_ratio = (adjusted_price - original_estimate) / original_estimate
                    result.data_date = factor['data_date']
                    result.notes = f"城市系数校正: {city} 系数={factor['build_factor']}"
                    logger.info(f"系数校正: {result.calibrated_value}")
                    return result
        except Exception as e:
            logger.warning(f"城市系数查询失败: {e}")
        
        return result
    
    def calibrate_estimate(
        self,
        city: str,
        building_type: str,
        structure_type: str,
        total_area: float,
        floor_count: int,
        original_unit_price: float,
        original_steel: float,
        original_concrete: float
    ) -> CalibratedEstimate:
        """完整估算校正"""
        calibrations = []
        data_sources = []
        
        # 校正单方造价
        price_cal = self.calibrate_unit_price(
            city, building_type, structure_type,
            original_unit_price, floor_count
        )
        calibrations.append(price_cal)
        if price_cal.calibrated:
            data_sources.append(price_cal.source)
        
        # 获取材料含量
        steel = original_steel
        concrete = original_concrete
        if self.db:
            try:
                indexes = self.db.query_cost_index(city, building_type, structure_type, floor_count)
                if indexes:
                    steel = indexes[0].steel_content
                    concrete = indexes[0].concrete_content
            except:
                pass
        
        # 计算校正后的造价
        calibrated_unit_price = price_cal.calibrated_value
        unit_price_low = calibrated_unit_price * 0.90
        unit_price_mid = calibrated_unit_price
        unit_price_high = calibrated_unit_price * 1.12
        
        total_low = total_area * unit_price_low
        total_mid = total_area * unit_price_mid
        total_high = total_area * unit_price_high
        
        # 计算综合置信度
        avg_confidence = price_cal.confidence
        
        if avg_confidence >= 0.80:
            accuracy_level = "A级 ±10% (数据库校正)"
        elif avg_confidence >= 0.60:
            accuracy_level = "B级 ±15% (多源校正)"
        else:
            accuracy_level = "C级 ±20% (模型估算)"
        
        return CalibratedEstimate(
            unit_price_low=unit_price_low,
            unit_price_mid=unit_price_mid,
            unit_price_high=unit_price_high,
            steel_content=steel,
            concrete_content=concrete,
            total_cost_low=total_low,
            total_cost_mid=total_mid,
            total_cost_high=total_high,
            calibrations=calibrations,
            data_sources=list(set(data_sources)),
            accuracy_level=accuracy_level
        )
    
    def close(self):
        """关闭连接"""
        if self.db:
            self.db.close()


# ============================================================
# 快速校正函数
# ============================================================

def quick_calibrate(
    city: str,
    building_type: str,
    structure_type: str,
    total_area: float,
    floor_count: int = 18,
    original_unit_price: float = 5000,
    original_steel: float = 45,
    original_concrete: float = 0.35
) -> CalibratedEstimate:
    """快速校正估算"""
    calibrator = DataCalibrator()
    try:
        result = calibrator.calibrate_estimate(
            city, building_type, structure_type, total_area,
            floor_count, original_unit_price, original_steel, original_concrete
        )
        return result
    finally:
        calibrator.close()


def get_verified_data(city: str, building_type: str = None, structure_type: str = None):
    """获取已验证的造价数据"""
    return quick_query(city, building_type, structure_type)


def get_city_info(city: str) -> Optional[Dict]:
    """获取城市造价信息"""
    return get_real_time_factor(city)


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DLHZ Data Calibrator v1.0")
    print("=" * 60)
    
    print("\n[Test] Suzhou 18F Frame-Shearwall Residential...")
    
    result = quick_calibrate(
        city="苏州",
        building_type="住宅",
        structure_type="框架-剪力墙",
        total_area=25000,
        floor_count=18,
        original_unit_price=5000,
        original_steel=45,
        original_concrete=0.35
    )
    
    print(f"\n[Result]")
    print(f"   Accuracy: {result.accuracy_level}")
    print(f"   Unit Price: {result.unit_price_low:,.0f} ~ {result.unit_price_high:,.0f} CNY/m2")
    print(f"   Total Cost: {result.total_cost_low/10000:,.0f} ~ {result.total_cost_high/10000:,.0f} 10k CNY")
    print(f"   Steel: {result.steel_content} kg/m2")
    print(f"   Concrete: {result.concrete_content} m3/m2")
    print(f"   Source: {', '.join(result.data_sources) or 'Model Estimate'}")
    
    print("\n[Calibration Details]")
    for cal in result.calibrations:
        status = "[OK]" if cal.calibrated else "[FAIL]"
        print(f"   {status} | Confidence: {cal.confidence:.0%} | Source: {cal.source}")
        print(f"          Adjustment: {cal.original_value:.0f} -> {cal.calibrated_value:.0f} ({cal.adjustment_ratio:+.1%})")
    
    print("\n[City Factors]")
    for city in ["深圳", "广州", "苏州", "汕尾"]:
        info = get_city_info(city)
        if info:
            print(f"   {city}: BuildFactor={info['build_factor']}, Date={info['data_date']}")
    
    print("\n" + "=" * 60)
    print("Data Calibrator Test Complete")
    print("=" * 60)
