---
name: deep-digest
description: "Extracts cognitive patterns, key insights, and action signals from any text input (messages, notes, articles, conversations). Turns raw content into structured, actionable digests."
read_when:
  - User needs to distill raw information into structured insights
  - Processing chat logs, meeting notes, articles, or research material
  - Looking for hidden patterns or cognitive shifts in content
---

# deep-digest — 深度内容萃取

把任何文本（聊天记录、文章、笔记、对话）转化成一个结构化的认知快照。

## 核心能力

输入一段文本，输出三样东西：

### 1. 事实层（发生了什么）
- 时间线摘要
- 关键人物/角色
- 事件/论点序列
- 数据或引用（如有）

### 2. 模式层（真正的模式是什么）
- 重复出现的主题
- 隐性假设
- 认知转变（世界观被敲碎或重塑的瞬间）
- 行为模式或决策模式
- **这是最值钱的部分** — 不是摘要，是模式识别

### 3. 信号层（跟我有什么关系）
- 可操作的建议
- 需要进一步深挖的方向
- 风险信号
- 优先行动项

## 用法

```bash
openclaw skill run deep-digest --input "你的文本内容"
```

支持管道输入：
```bash
cat long-notes.txt | openclaw skill run deep-digest
```

## 输出格式

Markdown 结构，三区清晰分隔：

```
## 📋 事实摘要
...

## 🧠 模式发现
- **发现1**: [模式描述]
- **发现2**: [模式描述]

## ⚡ 信号与行动
- [ ] **立即**: ...
- [ ] **跟进**: ...
- [ ] **观察**: ...
```

## 适用场景

- 群聊精华提取（从大量消息中提取价值）
- 会议记录总结（结构化行动项）
- 文章深度分析（不只是摘要，找出作者的隐性假设）
- 个人日记/笔记回顾（发现自己的思维模式）
- 竞品分析（从公开信息中提取策略信号）
