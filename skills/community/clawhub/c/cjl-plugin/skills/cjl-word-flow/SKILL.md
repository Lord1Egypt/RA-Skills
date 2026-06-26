---
name: cjl-word-flow
description: "Word flow: deep-dive word analysis + infograph card in one go. Takes one or more English words, runs cjl-word (generates deep semantics analysis) then cjl-card -i (generates infograph PNG). Use when user says '词卡', 'word card', 'word flow', or provides English words wanting both analysis and visual card."
user_invocable: true
version: "1.0.1"
---

# cjl-word-flow: 词卡

一条命令完成：解词 → 铸信息图。支持多词并行。

## 模式

**强制 NATIVE 模式。** 本 workflow 是纯 skill 管道（cjl-word → cjl-card -i），不需要 Algorithm 的七步流程。直接按下方执行步骤调用 skill，不走 OBSERVE/THINK/PLAN/BUILD/EXECUTE/VERIFY/LEARN。

## 参数

直接传入一个或多个英文单词，空格分隔。

```
/cjl-word-flow Obstacle
/cjl-word-flow Serendipity Resilience Entropy
```

## 执行

### 1. 收集单词列表

从用户消息中提取所有英文单词。

### 2. 处理每个单词

对每个单词，串行执行两步：

**步骤 A — 解词（cjl-word）：**

调用 Skill tool 执行 `cjl-word`，传入单词。在对话中输出 Markdown 解析结果。

**步骤 B — 铸信息图（cjl-card -i）：**

以步骤 A 的解析内容为输入，调用 Skill tool 执行 `cjl-card -i`。生成 PNG 文件到 `~/Downloads/`。

### 3. 多词并行

多个单词时，每个单词启动一个 Agent subagent 并行处理（每个 subagent 内部 A→B 串行）。

### 4. 汇总报告

```
════ 词卡完成 ═══════════════════════
📖 {Word1}
   🖼️ ~/Downloads/{Word1}.png

📖 {Word2}
   🖼️ ~/Downloads/{Word2}.png
...
```

## 关键约束

- 先解词后铸卡，顺序不可逆
- cjl-word 和 cjl-card -i 各自的质量标准不变
- 信息图内容来自解词结果，不是字典释义
