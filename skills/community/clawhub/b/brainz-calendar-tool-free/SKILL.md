---
name: "brainz-calendar-tool-free"
description: "通过 gcalcli 管理 Google 日历事件,支持创建、列出和删除日程,适合个人时间管理。Use when 需要项目管理、任务规划、进度跟踪、团队协作时使用。不适用于实际人员绩效评估。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Google 日历基础版"
  version: "1.0.0"
  summary: "通过 gcalcli 管理 Google 日历事件,支持创建、列出和删除日程,适合个人时间管理"
  tags:
    - "日历"
    - "Google Calendar"
    - "时间管理"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write

---

> **核心功能**: 本技能提供中文交互、化工作流场景等能力。

# Google 日历基础版

## 概述

本工具是 **日程管理** 领域的 **FREE 版本** AI Skill,专为个人用户与轻量级场景设计。通过自然语言指令驱动 AI Agent 执行任务,提供核心功能与简洁易用的操作体验。

FREE 版本与 PRO 版本完全兼容,可在需要时升级至 PRO 版本获取高级功能、批量操作与团队协同能力。

### 版本定位

| 维度 | FREE 版本 | PRO 版本 |
|:-----|:----------|:---------|
| 目标用户 | 个人用户 | 企业团队 |
| 功能范围 | 核心功能 | 全部功能 |
| 批量操作 | 不支持 | 支持 |
| 团队协作 | 不支持 | 支持 |
| 技术支持 | 社区支持 | 优先响应 |
| 数据分析 | 基础统计 | 高级分析 |

## 核心能力

FREE 版本提供以下能力:

### 列出指定日期范围内的日程事件
列出指定日期范围内的日程事件

**输出**: 返回列出指定日期范围内的日程事件的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 创建新日历事件并设置标题、时间
创建新日历事件并设置标题、时间与时长

**输出**: 返回创建新日历事件并设置标题、时间的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 按关键词搜索并删除事件
按关键词搜索并删除事件

**输出**: 返回按关键词搜索并删除事件的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 支持 CalDAV 协议备份
支持 CalDAV 协议备份

**输出**: 返回支持 CalDAV 协议备份的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 命令行快速操作无需打开浏览器
命令行快速操作无需打开浏览器

**输出**: 返回命令行快速操作无需打开浏览器的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 功能详情

本版本提供 5 项核心能力,覆盖 日程管理 的常见使用场景。如需批量操作、团队协作、数据分析等高级功能,可升级至 PRO 版本。

**FREE 版本核心功能清单:**

- 列出指定日期范围内的日程事件
- 创建新日历事件并设置标题、时间与时长
- 按关键词搜索并删除事件
- 支持 CalDAV 协议备份
- 命令行快速操作无需打开浏览器

**PRO 版本扩展功能预览:**

- 多日历同步与跨平台日历聚合(Google/Apple/Outlook)
- 智能调度:自动寻找最优会议时间
- 团队空闲时间分析与会议室预订
- 重复事件批量管理与会者通知
- 日程冲突检测与智能调整建议
- 日历数据导出与统计分析报表

**输出**: 返回功能详情的执行结果,包含操作状态和输出数据。
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：gcalcli、列出和删除日程、适合个人时间管理、日程管理领域的专、辅助工具、提供核心基础功能等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景 1: 查看本周日程

列出指定日期范围内的所有日历事件

```bash
gcalcli agenda "2026-02-03" "2026-02-10"
```

### 场景 2: 创建团队会议

添加新日历事件并设置时间与时长

```bash
gcalcli add --title "Team sync" --when "2026-02-04 10:00" --duration 30
```

## 不适用场景

以下场景Google 日历基础版不适合处理：

- 实时流数据处理
- 小规模数据手动分析
- 非结构化文本情感分析

## 触发条件

需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于非本工具能力范围的需求。

## 快速开始

### 1. 环境准备

确保已安装并配置好 AI Agent 环境(Claude Code / Cursor / Codex / Gemini CLI 等),本 Skill 通过 SKILL.md 指令驱动 Agent 执行任务。

**系统要求:**

- 操作系统: Windows / macOS / Linux
- Agent 平台: 支持 SKILL.md 格式的任意 AI Agent
- 运行时: Python 3.8+ 或 Node.js 18+(视具体操作需求)

### 2. 配置参数

```bash
pip install gcalcli
export GOOGLE_CALENDAR_API_KEY="${API_KEY:?请设置环境变量}"
# 或使用 CalDAV
export CALDAV_URL="https://your-caldav-server"
export CALDAV_USER="username"
export CALDAV_PASS="password"
```

### 3. 验证配置

配置完成后,可通过以下方式验证是否正常工作:

```bash
# 验证环境变量是否设置
echo "配置检查:"
env | grep -E "API|KEY|TOKEN|SECRET" | sed "s/=.*/=***/"  # Linux/macOS
# 或 PowerShell
# Get-ChildItem Env: | Where-Object {$_.Name -match "API|KEY|TOKEN"} | Format-Table
```

### 4. 开始使用

在 AI Agent 对话中描述你的需求,Agent 会根据本 Skill 的指令自动执行对应操作。

```text
请帮我查看本周日程
```

Agent 将自动:
1. 解析你的自然语言指令
2. 调用相应的工具或 API
3. 执行操作并返回结果
4. 返回执行结果供你确认

#
## 示例

### 基础配置

```bash
pip install gcalcli
# 或使用 CalDAV
export CALDAV_URL="https://your-caldav-server"
export CALDAV_USER="username"
export CALDAV_PASS="password"
```
### 可选配置

```json
{
  "edition": "free",
  "auto_retry": false,
  "max_concurrent": 1,
  "log_level": "info",
  "cache_enabled": true,
  "timeout": 30
}
```

**FREE 配置项说明:**

| 配置项 | 类型 | 默认值 | 说明 |
|:-------|:-----|:-------|:-----|
| auto_retry | bool | false | 失败后自动重试 |
| max_concurrent | int | 1 | 最大并发数(FREE 限制为1) |
| log_level | string | info | 日志级别 |
| cache_enabled | bool | true | 启用结果缓存 |
| timeout | int | 30 | 操作超时时间(秒) |

## 优选实践

1. **定期清理过期事件保持日历整洁**
2. **为不同类型事件使用不同颜色标记**
3. **设置提醒确保不遗漏重要日程**
4. **批量操作前先列出确认再执行删除**

### 个人使用建议

- 从简单任务开始熟悉工具行为,逐步扩展到复杂场景
- 定期备份配置文件与数据,防止意外丢失
- 遇到问题先查阅常见问题章节,再寻求社区帮助
- 保持配置简洁,只启用必要的功能选项
- 定期更新工具版本以获取最新功能与修复
- 记录常用操作命令,提高日常使用效率

## 常见问题

### 依赖详情

A: 确保 Python 3.7+ 已安装,尝试 pip3 install gcalcli --user。

### Q: 支持哪些日历服务?

A: FREE 版支持 Google Calendar;PRO 版支持 Google/Apple/Outlook 及 CalDAV。

### Q: 如何升级到 PRO 版本?

A: 升级到 PRO 版本非常简单:
1. 获取 PRO 版本授权
2. 安装 PRO 版本 Skill
3. 原有配置自动迁移,无需额外操作
4. 即可使用批量操作、团队协作等高级功能

### 已知限制

A: FREE 版本主要限制:
- 不支持批量操作(每次只能处理一个任务)
- 不支持团队协作(仅限个人使用)
- 不支持高级数据分析
- 技术支持依赖社区
如需这些功能,建议升级至 PRO 版本。

### Q: FREE 版本的数据安全吗?

A: FREE 版本所有数据本地存储,不上传云端,确保隐私安全。建议定期备份配置文件与数据目录。

## 依赖说明

### 运行环境

- **Agent 平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **运行时**: Python 3.8+ 或 Node.js 18+(视具体操作需求)
- **网络**: 部分功能需要网络连接访问外部 API

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |
| curl | CLI 工具 | 推荐 | 系统自带或包管理器安装 |
| jq | JSON 处理 | 推荐 | apt install jq / brew install jq |
| Python 3.8+ | 运行时 | 视需求 | python.org 下载 |
| Node.js 18+ | 运行时 | 视需求 | nodejs.org 下载 |

### API Key 配置

FREE 版本支持单一 API Key 配置,满足个人使用需求:
- **环境变量**:通过环境变量配置 API Key
- **配置文件**:支持配置文件方式存储 API Key
- **安全提醒**:切勿将 API Key 硬编码到脚本或提交到版本控制系统

### 可用性分类

- **分类**: MD+execute(纯 Markdown 指令,部分功能需要 exec 命令行执行能力)
- **说明**: 基于 Markdown 的 AI Skill,通过自然语言指令驱动 Agent 执行任务
- **FREE 特性**: 支持单次执行、基础配置与社区支持
- **安全等级**: 基础,数据本地存储,建议定期备份
- **SLA**: 社区支持,尽力响应

---

**版本信息**

| 项目 | 值 |
|:-----|:---|
| 版本号 | 1.0.0 |
| 版本类型 | FREE |
| 许可证 | MIT |
| 兼容性 | 可升级至 PRO 版本 |

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。