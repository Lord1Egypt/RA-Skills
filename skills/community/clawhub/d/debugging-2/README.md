# Systematic Debugging / 系统化调试

> A four-phase debugging discipline that enforces root-cause investigation before any fix. / 四阶段调试纪律：没有根因调查，就不允许修复。

**English** | [中文说明](#中文说明)

## What it is

An AI agent skill for finding the **root cause of any bug before attempting fixes**. The Iron Law: `NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.` Symptom fixes are failure.

It walks through four strict phases, each completed before the next:

1. **Root cause investigation** — read error messages completely, reproduce consistently, check recent changes, add diagnostic instrumentation at component boundaries, trace bad values to their origin
2. **Pattern analysis** — find working examples in the same codebase, compare against reference implementations, list every difference
3. **Hypothesis testing** — form a single specific hypothesis, test minimally, one variable at a time
4. **Implementation** — create a failing test first, apply a single fix, verify nothing else broke

## Key features

- **Iron Law / 铁律** — no fixes without root-cause investigation first; "try changing X and see" is banned
- **Escalation rule / 升级规则** — after 3 failed fixes, STOP and question the architecture instead of attempting fix #4
- **Evidence-first multi-component debugging** — log data at every component boundary (CI → build → signing; API → service → DB) to locate the failing layer before proposing anything
- **Backward tracing / 反向追踪** — walk up the call stack from the error site to the origin of the bad value; fix at the source, not the symptom
- **Red flags & anti-rationalizations / 红旗与反借口** — "quick fix now, investigate later", "emergency, no time for process" and similar shortcuts are explicitly countered
- **Cross-platform command table / 跨平台命令表** — diagnostic commands for macOS / Linux / Windows
- **Zero dependencies / 零依赖** — works in any repo or no-repo directory, no tooling required

## Usage

Drop the folder into your agent's skills directory. Triggers on "bug", "broken", "not working", "why", "出错", "挂了", "失败", "有问题" — especially under time pressure, when guessing is most tempting.

## Repository structure

```
└── SKILL.md    # Complete four-phase methodology / 完整四阶段方法论
```

## License

MIT

---

# 中文说明

## 这是什么

一个 AI 智能体技能：**尝试修复之前，先找到 Bug 的根因**。铁律：`没有根因调查，就不能修复。` 症状修复等于失败。

## 四个阶段（必须按顺序完成）

1. **根因调查**——完整读错误信息、稳定复现、检查最近变更、在组件边界加诊断埋点、把错误值反向追到源头
2. **模式分析**——在同一代码库找工作中相似代码，与参考实现逐项对比，列出每个差异
3. **假设测试**——单一明确假设、最小化测试、一次只改一个变量
4. **实施**——先建失败测试用例、单一修复、验证没有破坏其他测试

## 核心特性

- **铁律**：先查根因再修，禁止「改 X 试试」
- **升级规则**：3 次修复失败 → 停下来质疑架构，而不是做第 4 次尝试
- **多组件证据优先**：在每个组件边界记录数据进出，先定位失败的层，再提修复
- **反向追踪**：沿调用栈从错误点追到坏值的起源，在源头修
- **红旗与反借口**：戳破「先快速修，之后查」「紧急，没时间走流程」等经典借口
- **跨平台命令对照**：macOS / Linux / Windows 诊断命令表
- **零依赖**：任何仓库、无仓库目录都能用

## 使用方式

放入智能体 skills 目录。用户说 "bug"、"broken"、"not working"、"出错"、"挂了" 时触发——尤其是时间压力大、最想瞎猜的时候。

## 许可

MIT
