---
name: api-logger
description: |
  LLM API 调用日志记录、分析与可视化。透明代理拦截所有 LLM API 调用，记录完整 prompt/generation/token 用量，
  附带零依赖网页日志查看器（支持多维过滤、完整对话展示、token 成本统计）。
  适用场景：分析 API 调用成本、调试 prompt、查看历史对话记录、排查慢请求/失败请求。
  包含：proxy.py（代理服务）、log_viewer.py（终端查看器）、log-viewer.html（网页查看器）。
license: MIT
metadata:
  openclaw:
    emoji: "📊"
    tags:
      - api-logging
      - llm-debug
      - token-usage
      - cost-tracking
      - prompt-debug
      - log-viewer
      - proxy
    requires:
      bins: ["python3"]
---

# API Logger 🦞📊

LLM API 调用日志完整解决方案。透明代理拦截所有请求，零侵入记录，配套终端和网页两种查看方式。

---

## 🌐 网页日志查看器（推荐）

**文件：** `log-viewer.html`（skill 目录内）

### 使用方法

1. 把 `log-viewer.html` 复制到任意位置，双击用浏览器打开
2. 点击「⬆ 选择日志文件」，选择 `.jsonl` 日志文件（支持多文件合并）
3. 也可以直接把日志文件拖拽到页面

### 功能一览

- **统计卡片**：总调用数 / 成功率 / 平均耗时 / 总 Token 消耗
- **7种过滤条件**（实时响应，无需点搜索）：
  - 全文搜索（搜索 prompt + response 内容）
  - 模型筛选（自动提取日志中所有模型）
  - 状态筛选（全部 / 成功 2xx / 失败）
  - 最小耗时过滤（找慢请求）
  - 一键重置
- **日志列表**：时间 | 模型 | 状态 | 耗时 | Token | 用户输入，耗时>2s 自动标红
- **详情面板**（点击任意行展开）：
  - **对话内容**：完整 system prompt + 多轮对话，user/assistant 分色展示
  - **请求信息**：Request ID、模型、时间、耗时、状态、Token 用量
  - **原始 JSON**：完整日志记录，语法高亮，一键复制
- **快捷键**：`Esc` 关闭详情，`↑↓` 切换上下条
- **零依赖**：纯原生 JS，无需网络，离线可用

---

## 💻 终端日志查看器

```bash
# 进入日志查看器目录
cd ~/.openclaw/workspace/company/api-proxy/

# 今日摘要列表
python3 log_viewer.py

# 最后 N 条
python3 log_viewer.py --last 5

# 某条完整详情
python3 log_viewer.py --id 3 --full

# 今日统计（token 用量、成本估算）
python3 log_viewer.py --stats

# 今日统计 + 生成飞书文档
python3 log_viewer.py --stats --feishu

# 搜索关键词
python3 log_viewer.py --search "关键词"

# 只看失败请求
python3 log_viewer.py --errors

# 生成飞书文档（超300条自动截断明细）
python3 log_viewer.py --feishu

# 指定日期
python3 log_viewer.py --date 2026-03-10 --feishu
```

---

## 📦 安装

```bash
bash ~/.openclaw/workspace/skills/api-logger/install.sh
```

安装脚本将：
1. 创建 `~/.openclaw/workspace/company/api-proxy/`
2. 复制 `proxy.py` 和 `log_viewer.py`
3. 创建日志目录 `~/.openclaw/workspace/company/api-logs/`
4. 写入 macOS LaunchAgent plist（开机自启动）
5. 启动代理服务

### 配置（安装后手动完成）

**修改 openclaw.json 的 baseUrl：**
```json
"baseUrl": "http://127.0.0.1:18790/anthropic"
```

**修改上游地址（proxy.py 中的 `--upstream` 默认值）：**
```python
parser.add_argument("--upstream", default="https://your-actual-api-endpoint/anthropic", ...)
```

> ⚠️ 修改 openclaw.json 后需重启 Gateway 才生效，重启前请与用户确认。

---

## 📁 文件说明

| 文件 | 用途 |
|------|------|
| `proxy.py` | 透明代理服务（Python asyncio + aiohttp）|
| `log_viewer.py` | 终端查看器（彩色输出，支持飞书文档）|
| `log-viewer.html` | 网页查看器（零依赖，双击打开）|
| `install.sh` | 一键安装脚本 |

---

## 📊 日志字段说明

| 字段 | 说明 |
|------|------|
| `timestamp` | ISO 时间（含时区）|
| `request_id` | UUID |
| `streaming` | 是否流式请求 |
| `request_body` | 完整请求（model、system、messages）|
| `response_status` | HTTP 状态码 |
| `response_body_parsed` | 解析后的响应（content、usage）|
| `duration_ms` | 耗时（毫秒）|

---

## 注意事项

- 流式调用的 token 用量在 `response_body_parsed.usage` 中
- API Key 自动脱敏（保留前8位后4位）
- 飞书文档写入超时设为 120s，失败自动重试 3 次
- 日志按天切割，单文件通常 < 50MB，网页端可流畅处理
