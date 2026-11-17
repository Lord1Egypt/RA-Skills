---
name: dawn-memory-system
description: "换个会话，AI 就把你忘了？曙光记忆系统给它装上长期记忆：长短期记忆 + 主动代理 + 向量检索 + 对话压缩，跨会话回忆、自动归档、越用越懂你。触发词：长期记忆、跨会话记忆、记忆管理、向量检索、主动代理、对话压缩、自我进化。"
routes:
  memory-arch: '#三层存储'
  proactive: '#主动代理'
  code-master: '#代码规范'
  handoff: '#会话收尾'
  vecdb: '#向量数据库'
  compressor: '#对话压缩'
  speculative: '#预执行'
  summarize: '#总结'
  self-improve: '#自我进化'
  storage-analyzer: '#存储分析'
---

# dawn-memory-system

曙光记忆系统 v2.0 — 整合自11个独立技能。

## 三层存储

详见 memory/core/ 结构化数据（identity.json, lessons.json, preferences.json, strategies.json）
- MEMORY.md — 中央索引
- memory/core/ — 结构化事实
- 本地向量DB — 语义检索

## 主动代理

启动自动执行 boot sync、读结构化数据、交易日资金流扫描。

## 代码规范

PEP-8 / TypeScript Strict / PowerShell 最佳实践。

## 会话收尾

每次会话结束或用户说"收尾"时：
1. 盘点本次会话文件变更
2. 判断活文档/快照
3. 联动检查（改A强制想B）
4. 更新CHANGELOG → 活文档 → 记忆

## 向量数据库

本地 LanceDB + sentence-transformers + BM25 混合搜索，纯离线。

## 对话压缩

语义压缩长对话历史，保留关键信息。

## 预执行

预测并预加载上下文，加速后续操作。

## 总结

自动总结内容要点。

## 自我进化

记录学习笔记、错误、修正，持续改进。

## 存储分析

磁盘/文件系统使用分析。
