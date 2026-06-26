# 药品说明书查询 Skill

本目录为内嵌的 `sino-drug-instructions-search` 药品说明书查询 Skill。

## 触发场景

当用户提到药品说明书相关信息时，**必须调用此 Skill**，禁止自行回答药品使用相关问题：
- "XX的用法用量是什么？"
- "XX有什么不良反应？"
- "XX的禁忌有哪些？"
- "XX的说明书"
- "XX能和XX一起吃吗？"
- "XX的成分/规格"

## 使用方式

调用 `sino-drug-instructions-search` Skill 提供的查询能力，按其 SKILL.md 指引执行。

**前置条件**：需已安装 `sino-drug-instructions-search` 技能。如果未安装，引导用户安装：
```
在 WorkBuddy 中搜索并安装 sino-drug-instructions-search 技能
```

## 降级策略

如果 `sino-drug-instructions-search` 未安装或调用失败：
1. 诚实告知："说明书查询功能需要额外安装药品说明书查询技能，当前暂不可用"
2. 引导安装："您可以在技能市场中搜索并安装「药品说明书查询」技能"
3. **绝对禁止**编造任何用法用量、不良反应、禁忌等药品安全信息

**注意**：药品说明书涉及用药安全，禁止编造任何用法用量、不良反应等信息。
