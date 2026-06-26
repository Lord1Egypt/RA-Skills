---
name: "ai-skill-creator-attach-info"
description: "创建技能后完善头部信息。触发场景：(1) 调用 skill-creator 技能创建新技能后；(2) 用户说'创建技能'、'新建技能'、'添加技能'时；(3) 完成 SKILL.md 文件创建后。必须在创建任何技能后立即调用此技能添加 Author、Date、BusinessSupportVersion 信息。"
Author: "邵瑞波"
Date: "2026-03-13"
BusinessSupportVersion: "2.0.5"
---

# Skill Creator Attach Info

## 职责

在创建任何新技能后，必须立即调用此技能，为新技能的 SKILL.md 文件添加头部元信息。

## 触发时机（重要）

**AI 必须主动识别以下场景并自动调用本技能：**

1. **直接触发**：用户说"创建技能"、"新建技能"、"添加技能"、"make a skill"等
2. **间接触发**：调用了 `skill-creator` 技能后
3. **文件创建后**：完成 `.trae/skills/xxx/SKILL.md` 文件写入后

**关键原则**：创建任何技能后，**必须立即**调用本技能添加 Author、Date、BusinessSupportVersion，不得跳过此步骤。

## 执行步骤

1. 获取当前用户名：`whoami`
2. 获取当前日期：`date +"%Y-%m-%d %H:%M:%S"`
3. 询问用户 BusinessSupportVersion（若用户未指定）
4. 编辑 SKILL.md 文件，在头部添加/更新以下字段：
   - `Author`: 获取的用户名
   - `Date`: 获取的日期
   - `BusinessSupportVersion`: 用户指定的版本号

## 示例

```yaml
---
name: "example-skill"
description: "这是一个示例技能..."
Author: "shaoruibo"
Date: "2026-03-13"
BusinessSupportVersion: "2.0.5"
---
```
