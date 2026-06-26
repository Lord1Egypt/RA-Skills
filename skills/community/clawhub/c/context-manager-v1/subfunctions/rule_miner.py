#!/usr/bin/env python3
"""
Rule Miner - 规则提炼模块

从观察中提炼规则：observation → pattern → RULE
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
from collections import defaultdict


class RuleMiner:
    """规则提炼器"""
    
    def __init__(self, kb_path: str = "~/kb"):
        self.kb_path = Path(kb_path).expanduser()
        self.rules_path = self.kb_path / "rules.md"
        self.observations_path = self.kb_path / "_observations.json"
        
        # 加载观察记录
        self.observations = self._load_observations()
    
    def _load_observations(self) -> dict:
        """加载观察记录"""
        if self.observations_path.exists():
            return json.loads(self.observations_path.read_text())
        return {
            "observations": [],  # 观察记录
            "patterns": {}       # 识别出的模式 {pattern_hash: [observation_ids]}
        }
    
    def _save_observations(self):
        """保存观察记录"""
        self.observations_path.parent.mkdir(parents=True, exist_ok=True)
        self.observations_path.write_text(
            json.dumps(self.observations, indent=2, ensure_ascii=False)
        )
    
    def add_observation(self, 
                       category: str, 
                       description: str, 
                       context: dict = None,
                       lesson: str = None) -> str:
        """
        添加观察记录
        
        Args:
            category: 观察类别（如"未打标笔记找不到"）
            description: 观察描述
            context: 上下文信息
            lesson: 学到的教训
        
        Returns:
            observation_id
        """
        obs_id = f"obs-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        observation = {
            "id": obs_id,
            "category": category,
            "description": description,
            "context": context or {},
            "lesson": lesson,
            "created_at": datetime.now().isoformat(),
            "status": "new"  # new → pattern → rule → retired
        }
        
        self.observations["observations"].append(observation)
        
        # 归类到模式
        pattern_hash = hash(category)
        if pattern_hash not in self.observations["patterns"]:
            self.observations["patterns"][pattern_hash] = []
        self.observations["patterns"][pattern_hash].append(obs_id)
        
        # 保存
        self._save_observations()
        
        # 检查是否可以提炼规则
        pattern_count = len(self.observations["patterns"][pattern_hash])
        if pattern_count >= 3:
            self._try_create_rule(category, pattern_hash)
        
        return obs_id
    
    def _try_create_rule(self, category: str, pattern_hash: int):
        """尝试创建规则"""
        # 获取该模式下的所有观察
        obs_ids = self.observations["patterns"][pattern_hash]
        observations = [
            obs for obs in self.observations["observations"]
            if obs["id"] in obs_ids
        ]
        
        # 提取共同点
        lessons = [obs.get("lesson") for obs in observations if obs.get("lesson")]
        if not lessons:
            return
        
        # 如果教训一致，创建规则
        if len(set(lessons)) == 1:  # 所有教训都相同
            rule = self._create_rule(category, observations, lessons[0])
            self._add_to_rules_md(rule)
    
    def _create_rule(self, category: str, observations: List[dict], lesson: str) -> dict:
        """创建规则"""
        rule_id = f"RULE-{len(self.observations['patterns']) + 1:03d}"
        
        rule = {
            "id": rule_id,
            "category": category,
            "title": self._generate_title(category),
            "description": lesson,
            "observations_count": len(observations),
            "observation_ids": [obs["id"] for obs in observations],
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "review_date": self._calc_review_date(),
            "lifecycle": [
                {"event": "created", "date": datetime.now().isoformat()}
            ]
        }
        
        # 更新观察状态
        for obs in observations:
            obs["status"] = "rule_created"
        
        self._save_observations()
        
        return rule
    
    def _generate_title(self, category: str) -> str:
        """生成规则标题"""
        # 简化版：直接使用类别
        # 可以增强为 AI 生成
        titles = {
            "未打标笔记找不到": "知识必须打标",
            "孤立笔记无价值": "笔记必须建立连接",
            "收藏不行动": "只收藏会立即行动的内容",
            "无产出输入": "输入必须有产出",
        }
        return titles.get(category, f"规则：{category}")
    
    def _calc_review_date(self) -> str:
        """计算回顾日期（3 个月后）"""
        from datetime import timedelta
        review_date = datetime.now() + timedelta(days=90)
        return review_date.strftime("%Y-%m-%d")
    
    def _add_to_rules_md(self, rule: dict):
        """添加到 rules.md"""
        if not self.rules_path.exists():
            self.rules_path.write_text("# 知识管理规则\n\n")
            self.rules_path.write_text(self._get_rules_header())
        
        rule_md = self._rule_to_markdown(rule)
        
        content = self.rules_path.read_text()
        content += "\n" + rule_md
        
        self.rules_path.write_text(content)
    
    def _get_rules_header(self) -> str:
        """获取 rules.md 头部"""
        return """## 规则生命周期

observation（观察）→ pattern（模式识别）→ RULE（规则提炼）→ under review（定期回顾）→ retired（过时规则）

## 规则列表

"""
    
    def _rule_to_markdown(self, rule: dict) -> str:
        """规则转为 Markdown"""
        return f"""### {rule['id']}：{rule['title']}

**类别**：{rule['category']}

**描述**：{rule['description']}

**验证次数**：{rule['observations_count']} 次

**状态**：{rule['status']}

**创建时间**：{rule['created_at'][:10]}

**回顾时间**：{rule['review_date']}

**相关观察**：{', '.join(rule['observation_ids'])}

---

"""
    
    def get_rules(self) -> List[dict]:
        """获取所有规则"""
        # 从 rules.md 解析（简化版）
        # 可以从 observations 中提取
        rules = []
        for pattern_hash, obs_ids in self.observations["patterns"].items():
            if len(obs_ids) >= 3:
                observations = [
                    obs for obs in self.observations["observations"]
                    if obs["id"] in obs_ids
                ]
                lesson = observations[0].get("lesson", "")
                if lesson:
                    rule = self._create_rule(observations[0]["category"], observations, lesson)
                    rules.append(rule)
        return rules
    
    def get_active_rules(self) -> List[dict]:
        """获取活跃规则"""
        rules = self.get_rules()
        return [r for r in rules if r["status"] == "active"]
    
    def check_rule_lifecycle(self) -> List[dict]:
        """检查规则生命周期（回顾到期）"""
        rules = self.get_rules()
        today = datetime.now().strftime("%Y-%m-%d")
        
        due_reviews = []
        for rule in rules:
            if rule["review_date"] <= today and rule["status"] == "active":
                due_reviews.append(rule)
        
        return due_reviews


def main():
    """测试规则提炼"""
    miner = RuleMiner()
    
    # 添加观察
    miner.add_observation(
        category="未打标笔记找不到",
        description="2026-04-14，用户找不到 note-001，因为没有打标",
        context={"note_id": "note-001", "issue": "not_found"},
        lesson="所有新笔记必须有主题 + 场景 + 行动标签"
    )
    
    miner.add_observation(
        category="未打标笔记找不到",
        description="2026-04-14，用户找不到 note-002，因为没有打标",
        context={"note_id": "note-002", "issue": "not_found"},
        lesson="所有新笔记必须有主题 + 场景 + 行动标签"
    )
    
    miner.add_observation(
        category="未打标笔记找不到",
        description="2026-04-14，用户找不到 note-003，因为没有打标",
        context={"note_id": "note-003", "issue": "not_found"},
        lesson="所有新笔记必须有主题 + 场景 + 行动标签"
    )
    
    # 检查规则
    rules = miner.get_rules()
    print(f"提炼了 {len(rules)} 条规则")
    for rule in rules:
        print(f"- {rule['id']}: {rule['title']}")


if __name__ == "__main__":
    main()
