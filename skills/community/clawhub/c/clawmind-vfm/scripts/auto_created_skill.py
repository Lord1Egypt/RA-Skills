#!/usr/bin/env python3
"""
auto_created_skill.py — ClawMind Skill 自创建引擎
基于 Hermes Agent 的 Autonomous Skill Creation 机制

触发条件：
1. 复杂任务完成 → 自动创建 Skill
2. 同一类型问题出现 3 次以上 → 创建 Skill
3. 用户明确要求 → 创建 Skill
"""

import os, json, re
from datetime import datetime

SKILLS_DIR = "/home/node/.openclaw/workspace/skills/auto_created/"
os.makedirs(SKILLS_DIR, exist_ok=True)

# ==================== 数据结构 ====================

class AutoCreatedSkill:
    def __init__(self, name, trigger, prompt, tools, examples, created_from, description=""):
        self.name = name
        self.description = description
        self.trigger = trigger
        self.prompt = prompt
        self.tools = tools
        self.examples = examples
        self.created_from = created_from
        self.improvement_count = 0
        self.last_used = None
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "trigger": self.trigger,
            "prompt": self.prompt,
            "tools": self.tools,
            "examples": self.examples,
            "created_from": self.created_from,
            "improvement_count": self.improvement_count,
            "last_used": self.last_used,
            "created_at": self.created_at,
        }

    def to_markdown(self):
        """导出为 ClawMind Skill 的 SKILL.md 格式"""
        examples_md = ""
        for i, ex in enumerate(self.examples, 1):
            examples_md += f"### 示例 {i}\n{ex.get('description', '')}\n\`\`\`\n{ex.get('prompt', '')}\n\`\`\`\n\n"

        return f"""# {self.name}

> Auto-created skill | Created: {self.created_at}
> Source: {self.created_from}

## 描述

{self.description}

## 触发条件

{chr(10).join(f"- {t}" for t in self.trigger)}

## 系统提示词

{self.prompt}

## 所需工具

{', '.join(self.tools) if self.tools else '无特定工具'}

## 使用示例

{examples_md or '暂无示例'}

---

*此 Skill 由 ClawMind 自动创建，详情：ClawMind Skill Creation Engine v1.0*
"""

    def save(self):
        """保存 Skill 到 skills/auto_created/ 目录"""
        path = os.path.join(SKILLS_DIR, f"{self.name}.skill")
        meta_path = os.path.join(SKILLS_DIR, f"{self.name}.meta.json")
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.to_markdown())
        return path


# ==================== Skill 创建引擎 ====================

class SkillCreationEngine:
    def __init__(self, state):
        self.state = state
        self.history = []  # 追踪最近的任务历史

    def check_should_create(self, task_completed: dict) -> bool:
        """
        判断是否应该创建 Skill
        返回: bool
        """
        name = task_completed.get("task", "")
        context = task_completed.get("context", "")

        # 条件1：复杂任务完成（context 超过一定长度）
        if len(context) > 500:
            self.history.append({"type": "complex", "task": name, "context": context[:200]})
            return True

        # 条件2：同一类型问题出现3次以上
        task_names = [h["task"] for h in self.history[-10:] if h.get("task") == name]
        if len(task_names) >= 3:
            return True

        return False

    def create_skill(self, task_completed: dict) -> AutoCreatedSkill | None:
        """
        从完成的任务中创建 Skill
        """
        if not self.check_should_create(task_completed):
            return None

        name = task_completed.get("task", "untitled")
        context = task_completed.get("context", "")
        trigger = task_completed.get("trigger_keywords", [])

        # 生成 Skill 名称
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)[:50]

        # 生成系统提示词
        prompt = self._generate_prompt(task_completed)

        # 生成触发词
        if not trigger:
            trigger = self._extract_keywords(name, context)

        skill = AutoCreatedSkill(
            name=f"auto-{safe_name}",
            description=f"自动创建的 Skill，来源任务：{name}",
            trigger=trigger,
            prompt=prompt,
            tools=task_completed.get("tools_used", []),
            examples=[],
            created_from=task_completed.get("task", ""),
        )

        skill.save()
        return skill

    def _generate_prompt(self, task: dict) -> str:
        """生成 Skill 的系统提示词"""
        name = task.get("task", "")
        context = task.get("context", "")
        return f"""你擅长处理以下任务：{name}

背景：{context[:500]}

当遇到类似任务时，按以下步骤处理：
1. 理解任务目标
2. 识别需要的工具
3. 制定执行计划
4. 按计划执行
5. 验证结果"""

    def _extract_keywords(self, name: str, context: str) -> list:
        """从任务名称和上下文中提取触发关键词"""
        words = re.findall(r'[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}', f"{name} {context[:300]}")
        # 过滤停用词
        stopwords = {"的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这", "that", "the", "is", "to", "and", "of", "in", "for", "on", "with"}
        keywords = [w for w in words if w not in stopwords and len(w) >= 2]
        return list(set(keywords))[:10]


# ==================== 用户模型（参考 Hermes USER.md）====================

USER_PROFILE_PATH = "/home/node/.openclaw/workspace/USER.md"

def update_user_profile(key: str, value: str):
    """
    更新用户画像
    参考 Hermes Agent 的 USER.md 机制
    """
    with open(USER_PROFILE_PATH, 'a', encoding='utf-8') as f:
        f.write(f"\n## {datetime.now().strftime('%Y-%m-%d')} 更新\n")
        f.write(f"- **{key}**: {value}\n")


def get_user_profile() -> str:
    """读取用户画像"""
    try:
        with open(USER_PROFILE_PATH, encoding='utf-8') as f:
            return f.read()
    except:
        return ""
