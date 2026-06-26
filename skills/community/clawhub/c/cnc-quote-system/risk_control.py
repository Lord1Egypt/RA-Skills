"""
Risk Control - 风险控制器
Author: Timo (miscdd@163.com)
License: MIT
"""

import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """风险等级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RiskAssessment:
    """风险评估结果"""
    level: RiskLevel
    risks: List[str]
    recommendations: List[str]
    score: float  # 0-100, 越高越安全


class RiskController:
    """风险控制器 - 价格异常检测与预警"""
    
    def __init__(self):
        """初始化风险控制器"""
        self.price_history = {}
        self.thresholds = {
            "low_price": 50,      # 低于50元预警
            "high_price": 10000,  # 高于10000元预警
            "price_deviation": 0.3  # 价格偏差30%预警
        }
        logger.info("✅ 风险控制器初始化完成")
    
    def assess(
        self,
        quote_result: Dict,
        historical_prices: Optional[List[float]] = None
    ) -> RiskAssessment:
        """
        评估报价风险
        
        Args:
            quote_result: 报价结果
            historical_prices: 历史价格列表
        
        Returns:
            风险评估结果
        """
        risks = []
        recommendations = []
        score = 100.0  # 初始满分
        
        unit_price = quote_result.get("unit_price", 0)
        material = quote_result.get("material", "")
        surface = quote_result.get("surface", "none")
        
        # 检查低价风险
        if unit_price < self.thresholds["low_price"]:
            risks.append(f"⚠️ 价格偏低: ¥{unit_price} < ¥{self.thresholds['low_price']}")
            recommendations.append("建议复核材料和工艺")
            score -= 20
        
        # 检查高价风险
        if unit_price > self.thresholds["high_price"]:
            risks.append(f"⚠️ 价格偏高: ¥{unit_price} > ¥{self.thresholds['high_price']}")
            recommendations.append("建议拆分订单或寻找替代方案")
            score -= 10
        
        # 检查材料-表面处理兼容性
        if material == "AL6061" and surface == "chrome":
            risks.append("⚠️ 铝合金镀铬需特殊工艺")
            recommendations.append("建议改用阳极氧化")
            score -= 15
        
        # 检查历史价格偏差
        if historical_prices and len(historical_prices) > 0:
            avg_price = sum(historical_prices) / len(historical_prices)
            deviation = abs(unit_price - avg_price) / avg_price
            
            if deviation > self.thresholds["price_deviation"]:
                risks.append(f"⚠️ 价格偏差过大: {deviation:.1%} > {self.thresholds['price_deviation']:.1%}")
                recommendations.append("建议核实参数或更新知识库")
                score -= deviation * 100
        
        # 确定风险等级
        if score >= 80:
            level = RiskLevel.LOW
        elif score >= 60:
            level = RiskLevel.MEDIUM
        elif score >= 40:
            level = RiskLevel.HIGH
        else:
            level = RiskLevel.CRITICAL
        
        return RiskAssessment(
            level=level,
            risks=risks,
            recommendations=recommendations,
            score=max(score, 0)
        )
    
    def check_material_availability(self, material: str) -> bool:
        """检查材料可用性"""
        available_materials = ["AL6061", "SUS304", "STEEL45", "BRASS_H59"]
        return material in available_materials
    
    def check_surface_compatibility(self, material: str, surface: str) -> bool:
        """检查表面处理兼容性"""
        compatibility = {
            "AL6061": ["none", "anodize", "paint", "chrome"],
            "SUS304": ["none", "paint", "polish"],
            "STEEL45": ["none", "chrome", "paint", "quench"]
        }
        
        allowed = compatibility.get(material, ["none"])
        return surface in allowed


if __name__ == "__main__":
    controller = RiskController()
    
    # 测试风险评估
    assessment = controller.assess({
        "unit_price": 35.0,
        "material": "AL6061",
        "surface": "anodize"
    })
    
    print(f"\n🛡️ 风险评估结果:")
    print(f"  等级: {assessment.level.value}")
    print(f"  安全分: {assessment.score:.1f}/100")
    
    if assessment.risks:
        print(f"  风险:")
        for r in assessment.risks:
            print(f"    {r}")
    
    if assessment.recommendations:
        print(f"  建议:")
        for r in assessment.recommendations:
            print(f"    {r}")
    
    print("\n🦫 海狸 (Beaver) | 靠得住、能干事、在状态")