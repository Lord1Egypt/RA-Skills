#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNC智能报价系统 - 核心引擎
Author: Timo (miscdd@163.com)
License: MIT
"""

import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class QuoteResult:
    """报价结果"""
    material: str
    unit_price: float
    total_price: float
    lead_time: int
    risks: List[str]


class CNCQuoteEngine:
    """CNC智能报价引擎"""
    
    def __init__(self, config_path: str = "config.json"):
        """初始化报价引擎
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.materials = self._load_materials()
        logger.info(f"✅ CNC报价引擎初始化完成，支持{len(self.materials)}种材料")
    
    def _load_config(self, path: str) -> Dict:
        """加载配置"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"配置文件不存在: {path}，使用默认配置")
            return {}
    
    def _load_materials(self) -> Dict:
        """加载材料库（示例数据）"""
        return {
            "AL6061": {"density": 2.7, "price_per_kg": 25, "machining_factor": 1.0},
            "SUS304": {"density": 7.93, "price_per_kg": 35, "machining_factor": 1.5},
            "STEEL45": {"density": 7.85, "price_per_kg": 15, "machining_factor": 1.2},
        }
    
    def calculate(
        self,
        material: str,
        dimensions: List[float],
        surface: str = "none",
        quantity: int = 1
    ) -> QuoteResult:
        """计算报价
        
        Args:
            material: 材料牌号
            dimensions: 尺寸 [长, 宽, 高] mm
            surface: 表面处理
            quantity: 数量
        
        Returns:
            报价结果
        """
        # 验证材料
        if material not in self.materials:
            raise ValueError(f"不支持的材料: {material}")
        
        mat = self.materials[material]
        
        # 计算体积和重量
        volume = dimensions[0] * dimensions[1] * dimensions[2] / 1e9  # m³
        weight = volume * mat["density"] * 1000  # kg
        
        # 计算材料成本
        material_cost = weight * mat["price_per_kg"]
        
        # 计算加工成本
        machining_cost = material_cost * mat["machining_factor"] * 0.5
        
        # 计算表面处理成本
        surface_cost = self._calculate_surface_cost(surface, dimensions)
        
        # 计算总价
        unit_price = material_cost + machining_cost + surface_cost
        total_price = unit_price * quantity
        
        # 估算交期
        lead_time = self._estimate_lead_time(quantity, surface)
        
        # 风险评估
        risks = self._assess_risks(unit_price, material, surface)
        
        return QuoteResult(
            material=material,
            unit_price=round(unit_price, 2),
            total_price=round(total_price, 2),
            lead_time=lead_time,
            risks=risks
        )
    
    def _calculate_surface_cost(self, surface: str, dimensions: List[float]) -> float:
        """计算表面处理成本"""
        surface_prices = {
            "none": 0,
            "anodize": 50,
            "chrome": 100,
            "paint": 30,
        }
        area = 2 * (dimensions[0]*dimensions[1] + dimensions[1]*dimensions[2] + dimensions[0]*dimensions[2])
        return area * surface_prices.get(surface, 0) / 1e6
    
    def _estimate_lead_time(self, quantity: int, surface: str) -> int:
        """估算交期"""
        base_days = 3
        if quantity > 50:
            base_days += 2
        if surface != "none":
            base_days += 2
        return base_days
    
    def _assess_risks(self, price: float, material: str, surface: str) -> List[str]:
        """评估风险"""
        risks = []
        if price < 50:
            risks.append("⚠️ 价格偏低，建议复核")
        return risks


# 主入口
if __name__ == "__main__":
    engine = CNCQuoteEngine()
    
    # 示例报价
    result = engine.calculate(
        material="AL6061",
        dimensions=[100, 50, 10],
        surface="anodize",
        quantity=10
    )
    
    print(f"\n📊 CNC报价结果:")
    print(f"  材料: {result.material}")
    print(f"  单价: ¥{result.unit_price}")
    print(f"  总价: ¥{result.total_price}")
    print(f"  交期: {result.lead_time}天")
    if result.risks:
        print(f"  风险: {', '.join(result.risks)}")
    
    print("\n🦫 海狸 (Beaver) | 靠得住、能干事、在状态")