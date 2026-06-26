---
name: feishu-reading-task
description: |
  飞书待阅读任务自动创建技能。当用户说"加到待阅读任务"、"加入待读"、"mark as reading"等时，
  自动根据当前对话人员创建飞书任务，并挂到该人员的待阅读清单中。
  
  **触发词：** "加到待阅读任务"、"加入待读清单"、"mark as reading"、"待阅读"、"稍后阅读"
  
  **使用方式：**
  用户只需说："把这个加到待阅读任务" 或 "加入待读清单"
  技能会自动：
  1. 从对话上下文识别当前对话人员
  2. 提取要保存的内容（链接、文档、项目等）
  3. 创建飞书任务并指定该人员为负责人
  4. 记录到 memory 文件
---

# 飞书待阅读任务技能

## 功能
自动将内容添加到对话人员的飞书待阅读任务清单。

## 执行流程

1. **识别触发** - 检测用户消息中是否包含待阅读相关关键词
2. **获取对话人员** - 从消息上下文提取 sender_id (open_id)
3. **提取内容** - 从对话中提取要保存的链接、标题、描述
4. **创建任务** - 调用 feishu_task_task create API
5. **记录** - 写入 memory/YYYY-MM-DD.md

## 任务字段

- **summary**: 待阅读：{内容标题}
- **description**: 来源 + 链接 + 简要描述
- **members**: [{id: sender_id, role: assignee}]
- **current_user_id**: sender_id

## 示例

用户：把这个加到待阅读任务 https://example.com/article
助手：✅ 已添加到您的待阅读任务清单

## 依赖

- feishu_task_task (创建任务)
- 消息上下文 (获取对话人员 ID)
