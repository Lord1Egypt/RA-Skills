"""
Case Retriever - 案例检索器
Author: Timo (miscdd@163.com)
License: MIT
"""

import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CaseResult:
    """案例检索结果"""
    case_id: str
    material: str
    dimensions: List[float]
    price: float
    similarity: float
    metadata: Dict


class CaseRetriever:
    """案例检索器 - 历史案例匹配"""
    
    def __init__(self, case_db_path: str = "cases.json"):
        """
        初始化案例检索器
        
        Args:
            case_db_path: 案例库路径
        """
        self.cases = self._load_cases(case_db_path)
        logger.info(f"✅ 案例检索器初始化完成，加载{len(self.cases)}个案例")
    
    def _load_cases(self, path: str) -> List[Dict]:
        """加载案例库"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # 返回示例案例
            return self._create_sample_cases()
    
    def _create_sample_cases(self) -> List[Dict]:
        """创建示例案例"""
        return [
            {
                "case_id": "CASE001",
                "material": "AL6061",
                "dimensions": [100, 50, 10],
                "surface": "anodize",
                "quantity": 10,
                "unit_price": 25.50,
                "lead_time": 5
            },
            {
                "case_id": "CASE002",
                "material": "SUS304",
                "dimensions": [80, 40, 8],
                "surface": "none",
                "quantity": 20,
                "unit_price": 45.00,
                "lead_time": 7
            }
        ]
    
    def search(
        self,
        material: str,
        dimensions: List[float],
        surface: str = "none",
        top_k: int = 5
    ) -> List[CaseResult]:
        """
        搜索相似案例
        
        Args:
            material: 材料牌号
            dimensions: 尺寸
            surface: 表面处理
            top_k: 返回结果数量
        
        Returns:
            相似案例列表
        """
        results = []
        
        for case in self.cases:
            # 计算相似度
            similarity = self._calculate_similarity(
                case, material, dimensions, surface
            )
            
            if similarity > 0.5:  # 相似度阈值
                results.append(CaseResult(
                    case_id=case["case_id"],
                    material=case["material"],
                    dimensions=case["dimensions"],
                    price=case["unit_price"],
                    similarity=similarity,
                    metadata=case
                ))
        
        # 按相似度排序
        results = sorted(results, key=lambda x: x.similarity, reverse=True)
        return results[:top_k]
    
    def _calculate_similarity(
        self,
        case: Dict,
        material: str,
        dimensions: List[float],
        surface: str
    ) -> float:
        """计算相似度"""
        score = 0.0
        
        # 材料匹配
        if case["material"] == material:
            score += 0.5
        
        # 尺寸相似度
        case_vol = case["dimensions"][0] * case["dimensions"][1] * case["dimensions"][2]
        query_vol = dimensions[0] * dimensions[1] * dimensions[2]
        vol_sim = 1 - abs(case_vol - query_vol) / max(case_vol, query_vol)
        score += vol_sim * 0.3
        
        # 表面处理匹配
        if case["surface"] == surface:
            score += 0.2
        
        return min(score, 1.0)


if __name__ == "__main__":
    retriever = CaseRetriever()
    results = retriever.search(
        material="AL6061",
        dimensions=[100, 50, 10],
        surface="anodize"
    )
    
    print("\n📊 相似案例:")
    for r in results:
        print(f"  {r.case_id}: {r.material} ¥{r.price} (相似度: {r.similarity:.2f})")
    
    print("\n🦫 海狸 (Beaver) | 靠得住、能干事、在状态")