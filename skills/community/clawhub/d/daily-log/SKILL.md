---
name: daily-log
version: 1.3.0
description: 每日日记生成技能。触发时机：每次会话结束前或完成重要任务后。输出位置：memory/daily/YYYY-MM/YYYY-MM-DD.md。使用方法：加载 skill 后读取 references/spec.md 获取详细规范。
---

# Daily Log

按规范写日记，供后续知识提取。**只记录当前会话中自己做的事**，不要记录其他 agent 或人的工作内容。

## 输出位置

`memory/daily/YYYY-MM/YYYY-MM-DD.md`（带 YYYY-MM 子目录）

> ⚠️ **历史路径约定变更**：早期版本（clawhub v1.1.0 / 本地 v1.2.0 及以前）使用扁平路径 `memory/daily/YYYY-MM-DD.md`。diary-organizer 已把历史文件迁移到子目录，但 SKILL.md 没跟着改，导致多次出现"同一日期写多份"问题（最近一次：2026-06-22）。v1.3.0 起强制使用子目录路径。
>
> **子目录会自动创建**，无需手动 mkdir。**先检查文件是否已存在再写**，避免重复。

## 核心流程

1. 读取 references/spec.md 获取详细规范
2. 读取当前日记（如已存在）
3. 按规范生成/整合日志
4. 写文件
5. 自检

## 触发时机

- 会话结束前
- 完成重要任务后
- 用户明确要求时

## 为什么要写日记

日记是记忆系统的核心输入：
- cron memory-review 扫描日记生成知识提案
- 没有日记，知识沉淀链条断裂
- 详细日记 → 更多可提取知识

## 常见错误

- 只写结果不写过程 → 无法提取经验
- 事后概括 → 丢失细节
- 过于简略 → 扫不出东西

## 与 Memory Review 联动

日记是记忆系统的核心输入：
- **daily-log** 负责写日记
- **memory-review** 负责扫描日记生成知识提案
- 两者配合：详细日记 → 更多可提取知识

详见 `skills/memory-review/SKILL.md`
