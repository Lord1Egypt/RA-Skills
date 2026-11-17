---
name: feishu-archive
description: 飞书文档归档与管理。Use when needing to save analysis results, meeting notes, or documents to Feishu cloud docs, organize files in Feishu drive, or sync local content to Feishu for team sharing. Supports creating docs, uploading files, and setting permissions.
---

# 飞书文档归档

## 典型场景

1. 分析完成后，将结果归档到飞书文档
2. 将本地文件上传到飞书云盘
3. 设置文档权限给团队成员
4. 将群聊中的重要内容存档

## 工作流程

### 创建飞书文档

使用 feishu-doc skill：
1. 读取 feishu-doc SKILL.md 获取 API 用法
2. 创建文档并写入内容
3. 返回文档链接

### 上传文件到飞书云盘

使用 feishu-drive skill：
1. 读取 feishu-drive SKILL.md
2. 上传文件到指定文件夹
3. 返回文件链接

### 设置权限

使用 feishu-perm skill：
1. 读取 feishu-perm SKILL.md
2. 设置协作者权限（编辑/阅读）
3. 确认权限生效

## 归档规范

### 文档命名

格式：`[日期] [主题] - [版本]`
示例：`20260706 宠物卡留学卡策略分析 - v1`

### 文件夹结构

```
📁 江苏银行项目
  📁 需求分析
  📁 竞品调研
  📁 策略方案
  📁 会议纪要
  📁 周报
```

### 权限默认值

- 项目成员：可编辑
- 利益相关方：可阅读
- 外部人员：不共享

## 注意事项

- 大文档建议分章节创建，避免单文档过大
- 敏感数据（定价、市场份额等）注意权限控制
- 归档后发送文档链接到群聊通知
