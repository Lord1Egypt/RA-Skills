---
id: gamma/feishu-supertoolkit
owner_id: gamma-agent
name: Feishu SuperToolkit
description: 飞书超级工具包 - 集成文件发送（含音频卡片）、日历、审批、多维表格、通讯录、考勤六大模块
version: 1.0.0
icon: "\U0001F680"
author: Gamma (based on OpenClaw-CN feishu-toolkit + feishu-file-sender)
metadata:
  clawdbot:
    emoji: "\U0001F680"
    requires:
      bins:
        - uv
        - python
        - pip
        - ffmpeg
      env:
        - FEISHU_APP_ID
        - FEISHU_APP_SECRET
      python_packages:
        - requests
        - requests_toolbelt
    primaryEnv: FEISHU_APP_ID
    install:
      - id: brew
        kind: brew
        formula: uv
        bins:
          - uv
        label: Install uv via Homebrew
      - id: python-packages
        kind: pip
        packages:
          - requests
          - requests_toolbelt
        label: Install Python dependencies
---

# 🚀 Feishu SuperToolkit

*飞书超级工具包 - 文件发送 + 办公自动化一体化解决方案*

基于 `official/feishu-toolkit` 和 `feishu-file-sender` 合并增强，集成 **文件发送（含音频卡片）**、**日历管理**、**审批流程**、**多维表格**、**通讯录查询**、**考勤管理** 六大核心模块。

## ✨ 功能亮点

| 模块 | 能力 | 示例指令 |
|------|------|----------|
| 📎 **文件发送** | 图片预览、音频卡片（内嵌播放器）、视频封面、文档发送 | "把这首哈萨克语歌曲用卡片形式发到飞书" |
| 📅 日历 | 日程 CRUD、会议室预约、忙闲查询 | "帮我预约明天下午的 8 楼大会议室" |
| ✅ 审批 | 发起/查询/同意/拒绝/转交审批 | "帮我发起一个出差审批" |
| 📊 多维表格 | 表格创建、记录增删改查 | "在项目跟踪表中新增一条任务" |
| 👥 通讯录 | 用户/部门查询、组织架构浏览 | "查一下市场部有哪些成员" |
| ⏰ 考勤 | 打卡记录、补卡查询、考勤组管理 | "查看我这周的打卡记录" |

## 🆕 增强特性

### 🎵 音频卡片支持
- 自动转换为 OPUS 格式
- 内嵌播放器（进度条 + 时间显示）
- 飞书客户端 V7.49+ 支持

### 🖼️ 图片预览
- 直接预览显示，无需点击

### 🌐 UTF-8 编码机制
- 所有文本内容自动使用 UTF-8 编码
- 支持中文、哈萨克语、阿拉伯语等多语言
- 避免乱码问题

## 📦 安装

```bash
claw skill install gamma/feishu-supertoolkit
```

## ⚙️ 配置

### 1. 设置环境变量

```bash
export FEISHU_APP_ID="cli_a93078949238dbb3"
export FEISHU_APP_SECRET="AVJVZYEdlVIPtF8G50aDPdiXIiJXmWyX"
```

### 2. 启动服务

```bash
cd server/
uv venv && uv pip install -e ".[dev]"
uv run --env-file .env uvicorn feishu_supertoolkit.main:app --host 127.0.0.1 --port 8002
```

### 3. 验证

```bash
curl http://127.0.0.1:8002/ping
# {"message": "pong"}
```

## 🔐 权限清单

| 模块 | 权限标识 | 说明 |
|------|----------|------|
| 文件发送 | `im:message:send_as_bot` | 发送消息 |
| 文件发送 | `im:file:upload` | 上传文件 |
| 日历 | `calendar:calendar` | 读写日历及日程 |
| 日历 | `vc:room:readonly` | 查询会议室 |
| 审批 | `approval:approval` | 读写审批信息 |
| 审批 | `approval:task` | 审批人操作 |
| 多维表格 | `bitable:app` | 读写多维表格 |
| 多维表格 | `drive:drive` | 访问云空间 |
| 通讯录 | `contact:contact.base:readonly` | 读取通讯录 |
| 考勤 | `attendance:task:readonly` | 导出打卡数据 |

## 📖 详细文档

- [文件发送](references/file-sender.md)
- [日历与会议室](references/calendar.md)
- [审批](references/approval.md)
- [多维表格](references/bitable.md)
- [通讯录](references/contacts.md)
- [考勤](references/attendance.md)

## 🔗 相关资源

- [飞书开放平台](https://open.feishu.cn/)
- [飞书开发者文档](https://open.feishu.cn/document/)
- [API 调试台](https://open.feishu.cn/api-explorer)

## 📝 更新日志

- **v1.0.0** (2026-03-26) - 初始版本
  - 合并 `official/feishu-toolkit` 和 `feishu-file-sender`
  - 增强消息模块（音频卡片、图片预览）
  - 添加 UTF-8 编码机制
  - 支持多语言（中文、哈萨克语、阿拉伯语）
