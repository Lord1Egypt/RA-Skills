---
name: attachment-inject
description: "动态附件注入 — 在不修改system prompt的情况下注入动态内容。参考Claude Code的Attachment消息机制。"
metadata: {"openclaw":{"requires":["read","write"]}}
---

# Attachment Inject — 动态附件注入

参考 Claude Code 的 `attachments.ts`，将动态内容作为attachment消息注入而非嵌入system prompt。

## 问题
每次注入技能列表、Agent列表等动态内容到system prompt会：
1. 增加每次请求的token消耗
2. 内容变化时破坏prompt cache
3. 无法动态更新

## 解决方案

### 模式1: 按需读取（当前OpenClaw支持）
不预注入内容，而是在需要时读取：
```
用户提到"调度Agent" → 读 agents/*.md → 选择合适的Agent
用户提到"调试" → 读 skills/systematic-debugging/SKILL.md → 激活技能
```

### 模式2: 注册表文件（轻量注入）
维护一个注册表文件，包含名称+描述，不包含完整内容：
```
# agents/registry.md（自动生成）
| Agent | 描述 |
|-------|------|
| code-reviewer | 代码质量+安全审查 |
| planner | 实现规划（Opus） |
| chief-of-staff | 多渠道消息分诊 |
...

# skills/registry.md（自动生成）
| 技能 | 描述 |
|------|------|
| coordinator | 三层多Agent协调 |
| compact | 长会话压缩 |
...
```

### 模式3: 动态注入点
在AGENTS.md中定义占位符，每次会话开始时替换：
```
<!-- INJECT:SKILLS_REGISTRY -->
<!-- INJECT:AGENTS_REGISTRY -->
<!-- INJECT:MEMORY_SUMMARY -->
```

## 注册表生成脚本

```bash
# 生成技能注册表
for dir in skills/*/; do
  name=$(basename "$dir")
  desc=$(grep "^description:" "$dir/SKILL.md" 2>/dev/null | head -1 | sed 's/description: *//' | cut -c1-60)
  echo "| $name | $desc |"
done

# 生成Agent注册表
for f in agents/*.md; do
  name=$(grep "^name:" "$f" | head -1 | sed 's/name: *//')
  desc=$(grep "^description:" "$f" | head -1 | sed 's/description: *//' | cut -c1-60)
  echo "| $name | $desc |"
done
```

## 最佳实践

1. **注册表 < 500 token** — 只含名称和一行描述
2. **完整内容按需加载** — 匹配到任务时才读SKILL.md
3. **变化时只更新注册表** — 不动system prompt
4. **核心技能始终加载** — 9个核心技能的描述直接在AGENTS.md中
