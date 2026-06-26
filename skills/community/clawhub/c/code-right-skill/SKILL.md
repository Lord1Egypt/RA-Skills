---
name: code-right
title: Code-Right — 软著材料自动生成
description: >
  自动生成软件著作权申报全套材料（Word 文档+截图）。输入系统名称和邮箱，
  Code-Right 自动完成：系统功能描述撰写、模块分析、真实浏览器截图、
  格式合规的申报文档生成、打包 ZIP 邮件发送。
  纯 AI 搞不定的排版和截图，由工具链自动完成。
version: 0.1.0
author: gambo
license: MIT
metadata:
  hermes:
    tags: [软著, software-copyright, 知识产权, document-generation, 材料生成, cma, 申报]
    homepage: https://softcraft.cloud
    related_skills: [pdf-generation, ocr-and-documents]
---

# Code-Right — 软著材料自动生成

## 这是什么

**Code-Right** 是一个软件著作权申报材料自动生成工具。你只需输入系统名称和邮箱，它就能生成一整套符合官方格式的申报材料。

### 它能做什么

- ✍️ **AI 生成系统功能描述** — 根据系统名称自动撰写
- 🧩 **模块分析** — 自动拆解系统功能模块
- 📸 **真实浏览器截图** — Playwright 自动化截图，不是 AI 生成的假图
- 📄 **Word 文档输出** — 符合软著申报格式的 docx，带页眉页脚、截图嵌入
- 📦 **ZIP 打包 + 邮件发送** — 完成后自动发下载链接到邮箱

### 什么时候用

- 需要申请软件著作权，不想手工整理 60 页材料
- 有多份软著要批量申请，想自动化整个流程
- 你的 Agent（Hermes / Claude Code / OpenClaw）接到"帮我申请软著"的任务时，调用这个 skill 一键创建任务

## 与纯 AI 方案的区别

| | 纯 AI（直接问 LLM） | Code-Right this skill |
|--|-------------------|---------------------|
| 文档格式合规 | ❌ LLM 生成的 Word 格式不可控 | ✅ docxtpl 模板引擎，精确控制 |
| 截图 | ❌ 无法生成真实截图 | ✅ Playwright 真实浏览器截图 |
| 多轮生成 | ❌ 上下文窗口限制 | ✅ 异步任务，后台跑完通知 |
| 材料完整性 | ❌ 容易遗漏章节 | ✅ 固定工作流，每步校验 |
| 批量处理 | ❌ 一次只能做一份 | ✅ 可并行创建多个任务 |

## 使用方式

### 从 Hermes 直接调用

```bash
# 安装 skill
hermes skills install code-right

# 然后在会话中使用（Hermes 会自动加载）
# 只需说：帮我的 "智慧仓储管理系统" 生成软著材料，发到 admin@example.com
```

### 通过 Python 脚本

```bash
python scripts/create_task.py \
  --system-name "智慧仓储管理系统" \
  --notify-email "admin@example.com"
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--system-name` | ✅ | 软件系统名称（如 "智慧仓储管理系统"） |
| `--notify-email` | ✅ | 接收材料下载链接的邮箱 |
| `--access-token` | ❌ | 会话 token，用于任务列表过滤和下载鉴权 |

### 输出示例

成功时返回：
```json
{"taskId": 42, "status": "pending"}
```

之后系统会自动处理，完成后发送邮件到指定邮箱，内含下载链接。

## 工作流程

```
用户输入系统名称
    ↓
AI 生成系统概览（功能描述、技术架构）
    ↓
AI 分析系统模块（逐模块生成详情）
    ↓
Playwright 真实浏览器截图（登录页 × 功能页）
    ↓
docxtpl 渲染 Word 文档（含截图嵌入）
    ↓
ZIP 打包 → 邮件发送下载链接
```

## 技术栈

- 后端: Python Flask + LangChain + LangGraph
- AI: 通义千问 / DeepSeek
- 截图: Playwright
- 文档: python-docx + docxtpl
- 数据库: MySQL
- 部署: Docker

## 注意事项

- 首次提交请确保 `softcraft.cloud` 可访问
- 材料生成需要 3-5 分钟，完成后邮件通知
- 支持同时创建多个任务，后台并行处理
