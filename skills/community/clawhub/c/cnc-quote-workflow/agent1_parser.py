#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent1: 输入解析Agent
接收文本/STEP描述 → 调用hybrid_retriever
Author: Timo (miscdd@163.com)
License: MIT
"""

import re
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ParsedQuery:
    """解析后的查询"""
    material: str
    dimensions: List[float]
    surface: str
    quantity: int
    deadline: Optional[str]
    special_requirements: List[str]
    raw_input: str


class Agent1Parser:
    """输入解析Agent"""
    
    def __init__(self):
        self.material_keywords = {
            "铝合金": "AL6061", "铝": "AL6061", "6061": "AL6061",
            "不锈钢": "SUS304", "304": "SUS304",
            "钢": "STEEL45", "45号钢": "STEEL45",
            "黄铜": "BRASS_H59", "铜": "BRASS_H59",
        }
        
        self.surface_keywords = {
            "阳极氧化": "anodize", "氧化": "anodize",
            "镀铬": "chrome", "镀铬": "chrome",
            "喷漆": "paint", "喷漆": "paint",
            "抛光": "polish",
            "淬火": "quench",
        }
    
    def parse(self, user_input: str) -> ParsedQuery:
        """解析用户输入
        
        Args:
            user_input: 用户输入的文本描述
            
        Returns:
            ParsedQuery: 解析后的结构化查询
        """
        logger.info(f"📥 解析输入: {user_input}")
        
        # 提取各字段
        material = self._extract_material(user_input)
        dimensions = self._extract_dimensions(user_input)
        surface = self._extract_surface(user_input)
        quantity = self._extract_quantity(user_input)
        deadline = self._extract_deadline(user_input)
        special_requirements = self._extract_special_requirements(user_input)
        
        query = ParsedQuery(
            material=material,
            dimensions=dimensions,
            surface=surface,
            quantity=quantity,
            deadline=deadline,
            special_requirements=special_requirements,
            raw_input=user_input
        )
        
        logger.info(f"✅ 解析完成: 材料={material}, 尺寸={dimensions}, 表面={surface}")
        return query
    
    def _extract_material(self, text: str) -> str:
        """提取材料牌号"""
        for keyword, material in self.material_keywords.items():
            if keyword in text:
                return material
        return "AL6061"  # 默认铝合金
    
    def _extract_dimensions(self, text: str) -> List[float]:
        """提取尺寸 [长, 宽, 高] mm"""
        # 匹配 "100x50x10" 或 "100*50*10" 或 "100×50×10"
        pattern = r'(\d+)\s*[x×*]\s*(\d+)\s*[x×*]\s*(\d+)'
        match = re.search(pattern, text)
        
        if match:
            return [float(match.group(1)), float(match.group(2)), float(match.group(3))]
        
        # 匹配单独的数字
        numbers = re.findall(r'\d+', text)
        if len(numbers) >= 3:
            return [float(n) for n in numbers[:3]]
        
        return [100.0, 50.0, 10.0]  # 默认尺寸
    
    def _extract_surface(self, text: str) -> str:
        """提取表面处理"""
        for keyword, surface in self.surface_keywords.items():
            if keyword in text:
                return surface
        return "none"
    
    def _extract_quantity(self, text: str) -> int:
        """提取数量"""
        # 匹配 "10件" 或 "数量10" 或 "10个"
        patterns = [
            r'(\d+)\s*件',
            r'数量\s*(\d+)',
            r'(\d+)\s*个',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return int(match.group(1))
        
        return 1  # 默认1件
    
    def _extract_deadline(self, text: str) -> Optional[str]:
        """提取截止日期"""
        # 匹配 "下周" "明天" "3天内" 等
        if "下周" in text:
            return "next_week"
        elif "明天" in text:
            return "tomorrow"
        elif re.search(r'(\d+)天内', text):
            match = re.search(r'(\d+)天内', text)
            return f"{match.group(1)}_days"
        
        return None
    
    def _extract_special_requirements(self, text: str) -> List[str]:
        """提取特殊要求"""
        requirements = []
        
        if "急" in text or "加急" in text:
            requirements.append("urgent")
        if "精密" in text or "高精度" in text:
            requirements.append("high_precision")
        if "样品" in text:
            requirements.append("sample")
        
        return requirements


if __name__ == "__main__":
    # 测试
    parser = Agent1Parser()
    
    test_cases = [
        "铝合金6061，100x50x10mm，表面阳极氧化，10件",
        "不锈钢304板，200*100*5，镀铬，加急，5件",
        "45号钢，80x40x8，淬火处理，下周要货",
    ]
    
    for test in test_cases:
        result = parser.parse(test)
        print(f"\n输入: {test}")
        print(f"解析: 材料={result.material}, 尺寸={result.dimensions}, 表面={result.surface}, 数量={result.quantity}")
    
    print("\n🦫 海狸 (Beaver) | 靠得住、能干事、在状态")