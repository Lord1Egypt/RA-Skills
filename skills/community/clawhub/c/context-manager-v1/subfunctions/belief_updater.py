#!/usr/bin/env python3
"""
Belief Updater - 信念更新模块

检测信念冲突，用数据推翻旧认知
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


class BeliefUpdater:
    """信念更新器"""
    
    def __init__(self, kb_path: str = "~/kb"):
        self.kb_path = Path(kb_path).expanduser()
        self.false_beliefs_path = self.kb_path / "false-beliefs.md"
        self.beliefs_index_path = self.kb_path / "_beliefs_index.json"
        
        # 加载信念索引
        self.beliefs_index = self._load_beliefs_index()
    
    def _load_beliefs_index(self) -> dict:
        """加载信念索引"""
        if self.beliefs_index_path.exists():
            return json.loads(self.beliefs_index_path.read_text())
        return {
            "beliefs": {},  # {belief_id: belief_info}
            "conflicts": []  # 检测到的冲突
        }
    
    def _save_beliefs_index(self):
        """保存信念索引"""
        self.beliefs_index_path.parent.mkdir(parents=True, exist_ok=True)
        self.beliefs_index_path.write_text(
            json.dumps(self.beliefs_index, indent=2, ensure_ascii=False)
        )
    
    def check_belief_conflict(self, 
                              belief: str, 
                              new_data: dict, 
                              old_belief_data: dict = None) -> Dict[str, Any]:
        """
        检查信念冲突
        
        Args:
            belief: 信念描述（如"收藏=掌握"）
            new_data: 新数据（如{收藏 100 篇，阅读<10 篇}）
            old_belief_data: 旧信念数据（如{收藏=掌握}）
        
        Returns:
            冲突检测结果
        """
        conflict = {
            "belief": belief,
            "detected_at": datetime.now().isoformat(),
            "new_data": new_data,
            "old_belief_data": old_belief_data or {},
            "conflict_score": self._calculate_conflict_score(new_data, old_belief_data),
            "status": "detected"  # detected → analyzing → updated → archived
        }
        
        # 如果冲突分数高，记录到索引
        if conflict["conflict_score"] >= 0.7:
            conflict_id = f"conflict-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            conflict["id"] = conflict_id
            self.beliefs_index["conflicts"].append(conflict)
            self._save_beliefs_index()
            
            # 自动触发信念更新
            self._update_belief(belief, new_data, conflict)
        
        return conflict
    
    def _calculate_conflict_score(self, new_data: dict, old_belief_data: dict) -> float:
        """
        计算冲突分数（0-1）
        
        分数越高，冲突越明显
        """
        # 简化版：基于数据差异
        # 可以增强为 AI 判断
        
        score = 0.0
        
        # 示例：收藏 vs 阅读
        if "collected" in new_data and "read" in new_data:
            collected = new_data.get("collected", 0)
            read = new_data.get("read", 0)
            
            if collected > 0:
                read_rate = read / collected
                if read_rate < 0.1:  # 阅读率<10%
                    score = 0.9
                elif read_rate < 0.3:
                    score = 0.7
                elif read_rate < 0.5:
                    score = 0.5
        
        return score
    
    def _update_belief(self, belief: str, new_data: dict, conflict: dict):
        """更新信念"""
        # 生成新信念
        old_belief = self._generate_old_belief(belief)
        new_belief = self._generate_new_belief(belief, new_data)
        
        # 添加到 false-beliefs.md
        self._add_to_false_beliefs(old_belief, new_belief, new_data, conflict)
    
    def _generate_old_belief(self, belief: str) -> str:
        """生成旧信念描述"""
        beliefs = {
            "收藏=掌握": "收藏的文章以后会读，读了就会掌握",
            "知识越多越好": "收藏更多知识就能变得更强",
            "完美才能发布": "必须做到完美才能发布内容",
            "一个人干所有事": "一人 CEO 就是一个人干所有事",
        }
        return beliefs.get(belief, f"旧信念：{belief}")
    
    def _generate_new_belief(self, belief: str, new_data: dict) -> str:
        """生成新信念描述"""
        beliefs = {
            "收藏=掌握": "只收藏会立即行动的内容",
            "知识越多越好": "知识在于应用，不在于数量",
            "完美才能发布": "完成比完美重要，先发布再迭代",
            "一个人干所有事": "一人 CEO 是用工具和 AI 放大个人能力",
        }
        return beliefs.get(belief, f"新信念：基于数据重新定义{belief}")
    
    def _add_to_false_beliefs(self, old_belief: str, new_belief: str, new_data: dict, conflict: dict):
        """添加到 false-beliefs.md"""
        if not self.false_beliefs_path.exists():
            self.false_beliefs_path.write_text("# 被推翻的信念\n\n")
            self.false_beliefs_path.write_text(self._get_beliefs_header())
        
        belief_md = self._belief_to_markdown(old_belief, new_belief, new_data, conflict)
        
        content = self.false_beliefs_path.read_text()
        content += "\n" + belief_md
        
        self.false_beliefs_path.write_text(content)
    
    def _get_beliefs_header(self) -> str:
        """获取 false-beliefs.md 头部"""
        return """## 信念更新机制

旧信念 → 新数据 → 冲突检测 → 更新信念

## 信念列表

"""
    
    def _belief_to_markdown(self, old_belief: str, new_belief: str, new_data: dict, conflict: dict) -> str:
        """信念转为 Markdown"""
        conflict_id = conflict.get("id", "unknown")
        
        return f"""### 信念 {conflict_id}：{old_belief.split('：')[-1] if '：' in old_belief else old_belief}

**旧信念**：{old_belief}

**新数据**：
""" + "\n".join([f"- {k}: {v}" for k, v in new_data.items()]) + f"""

**冲突**：旧信念与新数据严重不符

**新信念**：{new_belief}

**行动**：
- [ ] 取消收藏功能
- [ ] 改为"行动清单"
- [ ] 只添加会立即执行的内容

**更新时间**：{conflict['detected_at'][:10]}

**冲突分数**：{conflict['conflict_score']:.1%}

---

"""
    
    def get_beliefs(self) -> List[dict]:
        """获取所有信念"""
        # 从 false-beliefs.md 解析（简化版）
        # 可以从 conflicts 中提取
        return self.beliefs_index.get("conflicts", [])
    
    def get_active_conflicts(self) -> List[dict]:
        """获取活跃冲突"""
        conflicts = self.get_beliefs()
        return [c for c in conflicts if c.get("status") == "detected"]
    
    def get_updated_beliefs(self) -> List[dict]:
        """获取已更新的信念"""
        conflicts = self.get_beliefs()
        return [c for c in conflicts if c.get("status") == "updated"]


def main():
    """测试信念更新"""
    updater = BeliefUpdater("/home/admin/kb")
    
    # 测试 1：收藏=掌握的信念冲突
    print("测试 1：收藏=掌握")
    conflict = updater.check_belief_conflict(
        belief="收藏=掌握",
        new_data={
            "collected": 100,
            "read": 8,
            "applied": 2
        }
    )
    print(f"冲突分数：{conflict['conflict_score']:.1%}")
    print(f"状态：{conflict['status']}")
    
    # 测试 2：知识越多越好的信念冲突
    print("\n测试 2：知识越多越好")
    conflict = updater.check_belief_conflict(
        belief="知识越多越好",
        new_data={
            "notes_count": 500,
            "used_notes": 10,
            "usage_rate": 0.02
        }
    )
    print(f"冲突分数：{conflict['conflict_score']:.1%}")
    print(f"状态：{conflict['status']}")
    
    # 获取结果
    beliefs = updater.get_beliefs()
    print(f"\n共检测到 {len(beliefs)} 个信念冲突")
    
    updated = updater.get_updated_beliefs()
    print(f"已更新 {len(updated)} 个信念")


if __name__ == "__main__":
    main()
