# Role Profile Template

<!--
  使用说明:
  1. 复制此文件到 .claude/agents/<role_name>.md
  2. 将所有 <role_name> 替换为实际角色名
  3. 填写职责和系统级 Prompt 要求
  4. 保留 4 项工作机制的完整描述
  5. 确保 frontmatter 的 type 与 name 一致
-->

---
name: <role_name>
description: <角色的简短描述>
type: <role_name>  # 必须与 name 保持一致
---

# <role_name> Agent 配置

## 职责

<!-- 描述该角色的核心职责、任务范围、决策权限 -->

```
在此描述角色职责...
```

## 系统级 Prompt 要求

<!-- 定义专业领域、知识背景、行为风格、输出格式 -->
<!-- 示例：
- 你是 XXX 领域专家
- 代码风格遵循 XXX 规范
- 优先考虑 XXX
-->

```
在此描述系统级要求...
```

## 工作机制

### 1. 沙盒纪律

只能在各自的 `.claude/teams/<team_name>/<role_name>/workspace/` 目录下进行临时文件的生成和草稿编写。
禁止在项目核心代码目录随意创建临时文件。

### 2. 渐进式披露留痕

任何具体任务都必须生成文档留痕：
- `progress.md` 仅做简要摘要记录（干了什么事、当前状态）
- 具体的任务细节和执行记录必须存放在 `workspace/xxx_detail.md` 中
- 需要时再去查看具体内容
- **严禁**把大量代码或长文本塞入 `progress.md`

### 3. 个性化经验记忆

拥有专属的 `memory.md`。所有实践经验、错误教训，或者当用户/Leader 提出"记住这个坑"时，必须主动将其记录到 `memory.md` 中，作为长期记忆。

### 4. 独立技能系统

除了全局技能，该角色拥有私有技能库：
- 所有专属于该角色的 Skill 文件必须存放在 `.claude/teams/<team_name>/<role_name>/skills/` 下
- 技能文件的创建与删除仅限于该目录
- 可通过 `Read` 工具读取技能文件获取详细说明
