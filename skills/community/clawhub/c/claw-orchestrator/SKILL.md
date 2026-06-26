---
name: claw-orchestrator
description: CC Agent 分析 + WBClaw 执行协作编排器。将任务发送给 Claude Code Agent 做前置分析设计，再由 WorkBuddy Claw 执行落地，自动生成执行报告。适用于需要深度分析+工程执行的多步骤任务。
agent_created: true
version: 1.0.0
---

# Claw Orchestrator — 多 Agent 协作编排器

CC Agent (claude-sonnet-4.6) 分析/生成 → WBClaw (deepseek-v4-pro) 预览/报告/记忆。

## 触发方式

```
用户: "用协作模式做XXX"
用户: "让CC帮我生成XXX然后预览"
用户: "/orchestrate 任务描述"
```

## 工作流（已实战验证）

```
Step 1: WBClaw 发起 CC Agent 调用
  npx claude -p "任务" \
    --allowedTools "Read,Write" \
    --permission-mode bypassPermissions \
    --max-turns 5

Step 2: CC Agent 执行
  ├─ 分析任务需求
  ├─ 调用 Write 工具 → 输出文件（HTML/Python/MD等）
  └─ 输出摘要到 stdout

Step 3: WBClaw 接力
  ├─ 验证 CC 产出的文件 ✅
  ├─ 打开预览 (HTML文件自动预览)
  ├─ 生成 task_report.md 执行报告
  └─ 更新 MEMORY.md 日志

Step 4: 输出通知
  🧠 CC Agent | claude-sonnet-4.6 @ OpenRouter | X.Xs
  🔧 WBClaw   | deepseek-v4-pro | X.Xs
  📦 产出: file1.html, file2.md, ...
```

## 已验证可工作的 CC Agent 调用

```bash
# 生成代码文件 ✅
npx claude -p "Write a clean HTML tool to output.html: ..." \
  --allowedTools "Read,Write" \
  --permission-mode bypassPermissions \
  --max-turns 5

# 分析+写报告 ✅
npx claude -p "Read project files and write analysis to report.md" \
  --allowedTools "Read,Write" \
  --permission-mode bypassPermissions \
  --max-turns 5
```

## 输出报告格式

每次协作完成后输出：

```
🧠 CC Agent  | 模型: claude-sonnet-4.6 @ OpenRouter | 耗时: X.Xs
   ├─ 分析任务并生成代码
   ├─ 写入: output.html (4990B)
   └─ 状态: ✅

🔧 WBClaw    | 模型: deepseek-v4-pro | 耗时: X.Xs
   ├─ 验证文件 ✅
   ├─ 打开预览 ✅
   └─ 写入报告 task_report.md

📋 任务总结: (一句话)
```

## 文件约定

| 文件 | 由谁写 | 内容 |
|------|:--:|------|
| `task_report.md` | WBClaw | 执行报告 |
| `*.html / *.py / *.md` | CC Agent | 任务产出文件 |
| `MEMORY.md` | 共享 | 长期记忆 |
| `YYYY-MM-DD.md` | 共享 | 每日日志 |

## 限制与注意事项

- CC Agent 在 Python subprocess 内调用时可能有限制，**直接从 WBClaw PowerShell 调用最稳定**
- `--permission-mode auto` 仅对 WebFetch 有效，文件写入必须用 `bypassPermissions`
- 单次 CC Agent 调用约 $0.01-0.05，取决于工具调用次数
- 冷启动 ~3s
