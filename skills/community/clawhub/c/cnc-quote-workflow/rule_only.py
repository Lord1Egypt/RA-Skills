#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rule-Only兜底模式
工业稳定铁律：当复杂模式失败时，自动降级到纯规则模式
Author: Timo (miscdd@163.com)
License: MIT
"""

import logging
from typing import Dict, List
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class RuleOnlyQuote:
    """纯规则报价结果"""
    unit_price: float
    total_price: float
    lead_time: int
    confidence: float
    mode: str = "rule_only"


class RuleOnlyEngine:
    """纯规则报价引擎（兜底模式）
    
    工业稳定原则：
    1. 无外部依赖
    2. 纯数学计算
    3. 100%稳定运行
    """
    
    # 材料价格表（元/kg）
    MATERIAL_PRICES = {
        "AL6061": 25.0,
        "SUS304": 35.0,
        "STEEL45": 20.0,
        "BRASS_H59": 40.0,
    }
    
    # 表面处理系数
    SURFACE_FACTORS = {
        "none": 1.0,
        "anodize": 1.15,
        "chrome": 1.30,
        "paint": 1.10,
        "polish": 1.05,
        "quench": 1.20,
    }
    
    # 批量折扣
    QUANTITY_DISCOUNTS = {
        1: 1.0,
        10: 0.95,
        50: 0.85,
        100: 0.75,
    }
    
    def calculate(self, material: str, dimensions: List[float], 
                  surface: str, quantity: int) -> RuleOnlyQuote:
        """纯规则计算报价
        
        Args:
            material: 材料牌号
            dimensions: 尺寸 [长,宽,高] mm
            surface: 表面处理
            quantity: 数量
            
        Returns:
            RuleOnlyQuote: 报价结果
        """
        logger.info(f"🔧 Rule-Only兜底模式启动: {material}")
        
        # 1. 计算体积 (cm³)
        volume_cm3 = (dimensions[0] * dimensions[1] * dimensions[2]) / 1000
        
        # 2. 计算重量 (kg) - 铝合金密度2.7g/cm³
        density_map = {
            "AL6061": 2.7,
            "SUS304": 7.9,
            "STEEL45": 7.8,
            "BRASS_H59": 8.5,
        }
        density = density_map.get(material, 2.7)
        weight_kg = volume_cm3 * density / 1000
        
        # 3. 材料成本
        material_price = self.MATERIAL_PRICES.get(material, 25.0)
        material_cost = weight_kg * material_price
        
        # 4. 加工费 (基础50元 + 体积因子)
        machining_cost = 50 + volume_cm3 * 0.5
        
        # 5. 表面处理成本
        surface_factor = self.SURFACE_FACTORS.get(surface, 1.0)
        
        # 6. 批量折扣
        discount = 1.0
        for threshold, factor in sorted(self.QUANTITY_DISCOUNTS.items(), reverse=True):
            if quantity >= threshold:
                discount = factor
                break
        
        # 7. 最终价格
        base_price = (material_cost + machining_cost) * surface_factor
        unit_price = base_price * discount
        total_price = unit_price * quantity
        
        # 8. 交期计算
        lead_time = 5  # 基础5天
        if surface != "none":
            lead_time += 2
        if quantity > 50:
            lead_time += 2
        
        result = RuleOnlyQuote(
            unit_price=round(unit_price, 2),
            total_price=round(total_price, 2),
            lead_time=lead_time,
            confidence=0.95,  # 规则模式高置信度
            mode="rule_only"
        )
        
        logger.info(f"✅ Rule-Only报价完成: ¥{unit_price}/件")
        return result


if __name__ == "__main__":
    # 测试
    engine = RuleOnlyEngine()
    
    test_cases = [
        ("AL6061", [100, 50, 10], "anodize", 10),
        ("SUS304", [200, 100, 5], "chrome", 50),
        ("STEEL45", [80, 40, 8], "quench", 1),
    ]
    
    for material, dims, surface, qty in test_cases:
        result = engine.calculate(material, dims, surface, qty)
        print(f"\n{material}: ¥{result.unit_price}/件 x {qty} = ¥{result.total_price}")
    
    print("\n🦫 海狸 (Beaver) | 靠得住、能干事、在状态")