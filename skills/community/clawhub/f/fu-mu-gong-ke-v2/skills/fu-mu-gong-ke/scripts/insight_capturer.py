#!/usr/bin/env python3
"""
洞察沉淀机制 - Insight Capturer
从对话中提取育儿洞察，沉淀为技能知识库

版本: 1.0.0
创建: 2026-05-29
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 配置
INSIGHT_DIR = Path(__file__).parent.parent / "data" / "insights"
INSIGHT_DIR.mkdir(parents=True, exist_ok=True)

PUNCHLINE_FILE = Path(__file__).parent.parent / "references" / "punch-lines.md"

class InsightCapturer:
    """洞察捕获器"""
    
    def __init__(self):
        self.insights = self._load_existing()
    
    def _load_existing(self) -> list:
        """加载现有洞察"""
        insight_file = INSIGHT_DIR / "insights.json"
        if insight_file.exists():
            with open(insight_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def capture(self, 
                scenario: str, 
                insight: str, 
                punch_line: str = None,
                source: str = "conversation",
                effectiveness: int = None) -> dict:
        """
        捕获一个洞察
        
        Args:
            scenario: 场景类型（如 "撒谎", "不听话"）
            insight: 洞察内容（发生了什么，为什么有效）
            punch_line: 强心剂句子（如果有的话）
            source: 来源（conversation/self-reflection/research）
            effectiveness: 有效性评分 1-5（如果有的话）
        
        Returns:
            创建的洞察记录
        """
        record = {
            "id": len(self.insights) + 1,
            "scenario": scenario,
            "insight": insight,
            "punch_line": punch_line,
            "source": source,
            "effectiveness": effectiveness,
            "created_at": datetime.now().isoformat(),
            "usage_count": 0
        }
        
        self.insights.append(record)
        self._save()
        
        return record
    
    def capture_from_dialogue(self, dialogue_summary: dict) -> list:
        """
        从对话摘要中批量捕获洞察
        
        Args:
            dialogue_summary: {
                "parent_state": str,  # 父母状态
                "child_behavior": str,  # 孩子行为
                "root_cause": str,  # 根源
                "key_insight": str,  # 核心洞察
                "punch_line_used": str,  # 使用的刺穿句
                "parent_reaction": str,  # 父母反应
                "effectiveness": int  # 效果评分
            }
        
        Returns:
            创建的洞察记录列表
        """
        records = []
        
        # 洞察记录
        if dialogue_summary.get("key_insight"):
            record = self.capture(
                scenario=dialogue_summary.get("child_behavior", "unknown"),
                insight=dialogue_summary["key_insight"],
                punch_line=dialogue_summary.get("punch_line_used"),
                source="conversation",
                effectiveness=dialogue_summary.get("effectiveness")
            )
            records.append(record)
        
        # 如果效果好，加入强心剂库候选
        if dialogue_summary.get("effectiveness", 0) >= 4:
            self._add_to_punchline_candidates(
                scenario=dialogue_summary.get("child_behavior", "unknown"),
                punch_line=dialogue_summary.get("punch_line_used"),
                parent_reaction=dialogue_summary.get("parent_reaction")
            )
        
        return records
    
    def _add_to_punchline_candidates(self, scenario: str, punch_line: str, parent_reaction: str):
        """将有效的刺穿句加入候选库"""
        candidate_file = INSIGHT_DIR / "punchline_candidates.md"
        
        entry = f"""
### 新候选 ({datetime.now().strftime('%Y-%m-%d')})
- **场景**: {scenario}
- **刺穿句**: {punch_line}
- **父母反应**: {parent_reaction}
- **待验证**: 是

---
"""
        
        with open(candidate_file, 'a', encoding='utf-8') as f:
            f.write(entry)
    
    def search(self, scenario: str = None, keyword: str = None, min_effectiveness: int = None) -> list:
        """
        搜索洞察
        
        Args:
            scenario: 场景类型
            keyword: 关键词
            min_effectiveness: 最低有效性评分
        
        Returns:
            匹配的洞察列表
        """
        results = self.insights
        
        if scenario:
            results = [i for i in results if i.get("scenario") == scenario]
        
        if keyword:
            results = [i for i in results if keyword.lower() in i.get("insight", "").lower()]
        
        if min_effectiveness:
            results = [i for i in results if (i.get("effectiveness") or 0) >= min_effectiveness]
        
        return results
    
    def get_statistics(self) -> dict:
        """获取洞察统计"""
        if not self.insights:
            return {"total": 0, "scenarios": {}, "avg_effectiveness": 0}
        
        scenarios = {}
        effectiveness_sum = 0
        effectiveness_count = 0
        
        for insight in self.insights:
            scenario = insight.get("scenario", "unknown")
            scenarios[scenario] = scenarios.get(scenario, 0) + 1
            
            if insight.get("effectiveness"):
                effectiveness_sum += insight["effectiveness"]
                effectiveness_count += 1
        
        return {
            "total": len(self.insights),
            "scenarios": scenarios,
            "avg_effectiveness": effectiveness_sum / effectiveness_count if effectiveness_count > 0 else 0
        }
    
    def _save(self):
        """保存洞察到文件"""
        insight_file = INSIGHT_DIR / "insights.json"
        with open(insight_file, 'w', encoding='utf-8') as f:
            json.dump(self.insights, f, ensure_ascii=False, indent=2)
    
    def export_for_review(self) -> str:
        """导出洞察供定期审阅"""
        stats = self.get_statistics()
        
        output = f"""# 洞察审阅报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 统计
- 总洞察数: {stats['total']}
- 平均有效性: {stats['avg_effectiveness']:.1f}/5

## 场景分布
"""
        for scenario, count in sorted(stats['scenarios'].items(), key=lambda x: -x[1]):
            output += f"- {scenario}: {count}条\n"
        
        output += "\n## 高有效性洞察（≥4分）\n\n"
        
        high_effectiveness = self.search(min_effectiveness=4)
        for insight in high_effectiveness[-10:]:  # 最近10条
            output += f"""### {insight['scenario']} (有效性: {insight['effectiveness']}/5)
- 洞察: {insight['insight']}
- 刺穿句: {insight.get('punch_line', 'N/A')}
- 来源: {insight['source']}
- 日期: {insight['created_at'][:10]}

"""
        
        return output


def main():
    """命令行入口"""
    import sys
    
    capturer = InsightCapturer()
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  insight_capturer.py stats          - 显示统计")
        print("  insight_capturer.py search <关键词> - 搜索洞察")
        print("  insight_capturer.py export          - 导出审阅报告")
        return
    
    command = sys.argv[1]
    
    if command == "stats":
        stats = capturer.get_statistics()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    elif command == "search" and len(sys.argv) > 2:
        keyword = sys.argv[2]
        results = capturer.search(keyword=keyword)
        for r in results:
            print(f"[{r['scenario']}] {r['insight']}")
    
    elif command == "export":
        report = capturer.export_for_review()
        print(report)
    
    else:
        print("未知命令")


if __name__ == "__main__":
    main()
