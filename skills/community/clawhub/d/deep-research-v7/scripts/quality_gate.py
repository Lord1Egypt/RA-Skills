#!/usr/bin/env python3
"""
quality_gate.py - 质量门禁（简化版v1.0）
自动计算卡片质量分，决定"通过/警告/跳过"
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple


class QualityGate:
    """质量门禁"""
    
    def __init__(self, card: Dict[str, Any]):
        self.card = card
    
    def evaluate(self) -> Dict[str, Any]:
        """计算质量分 + 决策建议"""
        completeness = self._score_completeness()
        credibility = self._score_credibility()
        format_quality = self._score_format()
        
        total = completeness * 0.4 + credibility * 0.3 + format_quality * 0.3
        
        if total >= 0.8:
            status, action = "verified", "include"
        elif total >= 0.6:
            status, action = "needs_review", "include_with_warning"
        else:
            status, action = "skipped", "exclude"
        
        return {
            "quality_score": round(total, 2),
            "subscores": {
                "completeness": round(completeness, 2),
                "credibility": round(credibility, 2),
                "format": round(format_quality, 2)
            },
            "status": status,
            "action": action,
            "reasons": self._generate_reasons(completeness, credibility, format_quality, total)
        }
    
    def _score_completeness(self) -> float:
        """完整性评分"""
        score = 0.0
        checks = []
        
        source = self.card.get("source", {})
        if source.get("title"):
            checks.append(True)
        if source.get("author"):
            checks.append(True)
        if self.card.get("content", {}).get("word_count", 0) > 500:
            checks.append(True)
        
        return len(checks) / 3.0
    
    def _score_credibility(self) -> float:
        """可信度评分"""
        score = 0.0
        
        source_type = self.card.get("source", {}).get("type", "")
        if source_type in ["pdf", "arxiv"]:
            score += 0.4
        
        word_count = self.card.get("content", {}).get("word_count", 0)
        if word_count > 5000:
            score += 0.3
        elif word_count > 2000:
            score += 0.2
        
        if self.card.get("source", {}).get("published_date"):
            score += 0.3
        
        return min(1.0, score)
    
    def _score_format(self) -> float:
        """格式质量评分"""
        score = 0.0
        
        url = self.card.get("source", {}).get("url", "")
        if url and url.startswith("http"):
            score += 0.3
        
        key_quote = self.card.get("key_quote", {})
        if key_quote and key_quote.get("quote"):
            score += 0.4
        
        suggestions = self.card.get("verification_status", {}).get("suggestions", [])
        if suggestions:
            score += 0.3
        
        return score
    
    def _generate_reasons(self, comp, cred, fmt, total) -> List[str]:
        reasons = []
        if comp < 0.7:
            reasons.append("字段不完整")
        if cred < 0.7:
            reasons.append("可信度不足")
        if fmt < 0.7:
            reasons.append("格式待优化")
        if not reasons:
            reasons.append("质量达标")
        return reasons


def main():
    import argparse
    parser = argparse.ArgumentParser(description="质量门禁")
    parser.add_argument("input", help="输入卡片JSON文件")
    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        card = json.load(f)
    
    gate = QualityGate(card)
    result = gate.evaluate()
    
    print(f"📊 质量分: {result['quality_score']:.2f}")
    print(f"🎯 状态: {result['status']}")
    print(f"💡 原因: {', '.join(result['reasons'])}")


if __name__ == "__main__":
    main()
