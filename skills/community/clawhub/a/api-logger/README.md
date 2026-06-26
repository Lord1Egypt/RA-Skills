# 🦞 API Logger — 龙虾 API 调用日志系统

透明拦截并记录所有发往 LLM API 的请求与响应，支持终端查看和飞书文档输出。

---

## 功能介绍

- **零侵入代理**：作为 HTTP 透明代理运行，不修改任何请求/响应内容
- **完整记录**：保存完整的 prompt（含 system prompt）、生成内容、token 用量
- **流式支持**：正确处理 SSE 流式响应，重建完整对话内容
- **API Key 脱敏**：自动对请求头中的认证信息打码，只保留首尾字符
- **按日存储**：每天一个 JSONL 文件，方便归档与检索
- **多维查看**：终端摘要、详情、统计、关键词搜索
- **飞书文档输出**：一键生成格式化的飞书文档，方便分享和存档

---

## 系统架构

```
┌─────────────────────────────────────────────────────┐
│                     你的程序                         │
│              (OpenClaw / 其他 AI 客户端)              │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP 请求
                       ▼
┌─────────────────────────────────────────────────────┐
│          🦞 Lobster API Proxy (proxy.py)             │
│          http://127.0.0.1:18790/anthropic            │
│                                                     │
│  ① 接收请求 → ② 记录请求体（脱敏）→ ③ 转发上游       │
│  ④ 接收响应 → ⑤ 记录响应体       → ⑥ 返回客户端      │
└──────────────────────┬──────────────────────────────┘
                       │ 转发至上游
                       ▼
┌─────────────────────────────────────────────────────┐
│             上游模型 API 服务器                       │
│         (e.g. http://model.mify.ai.srv/anthropic)    │
└─────────────────────────────────────────────────────┘
                       │
                       ▼ 日志写入
┌─────────────────────────────────────────────────────┐
│    ~/.openclaw/workspace/company/api-logs/           │
│    ├── 2026-03-10.jsonl                              │
│    ├── 2026-03-11.jsonl                              │
│    └── ...                                          │
└─────────────────────────────────────────────────────┘
                       │
                       ▼ 读取分析
┌─────────────────────────────────────────────────────┐
│          🔍 Log Viewer (log_viewer.py)               │
│          终端查看 / 飞书文档输出                      │
└─────────────────────────────────────────────────────┘
```

---

## 安装步骤

### 1. 运行安装脚本

```bash
bash ~/.openclaw/workspace/skills/api-logger/install.sh
```

脚本会自动完成：
- 复制 `proxy.py` 和 `log_viewer.py` 到 `~/.openclaw/workspace/company/api-proxy/`
- 创建日志目录 `~/.openclaw/workspace/company/api-logs/`
- 检查并安装 `aiohttp` 依赖
- 写入 LaunchAgent plist（`~/Library/LaunchAgents/com.lobster.api-proxy.plist`）
- 加载 plist，启动后台代理服务

### 2. 手动配置（重要！）

> ⚠️ **以下两项配置必须手动完成，脚本不会自动修改。**

#### 2.1 修改 openclaw.json 中的 baseUrl

文件路径：`~/.openclaw/openclaw.json`

找到你使用的模型 provider 配置，将 `baseUrl` 改为代理地址：

```json
"baseUrl": "http://127.0.0.1:18790/anthropic"
```

> ⚠️ **修改后需要重启 Gateway 才能生效。重启前请先与用户确认，不要擅自重启！**

#### 2.2 确认代理上游地址

文件路径：`~/.openclaw/workspace/company/api-proxy/proxy.py`

找到 `--upstream` 参数的默认值，改为你的实际上游 API 地址：

```python
parser.add_argument("--upstream", type=str, default="http://your-model-api.server/anthropic", ...)
```

修改后需要重新加载 LaunchAgent：

```bash
launchctl unload ~/Library/LaunchAgents/com.lobster.api-proxy.plist
launchctl load ~/Library/LaunchAgents/com.lobster.api-proxy.plist
```

### 3. 重启 Gateway（与用户确认后）

```bash
openclaw gateway restart
```

重启后，所有经过 OpenClaw 的 API 调用将自动被代理记录。

---

## 常用命令

```bash
# 进入工具目录
cd ~/.openclaw/workspace/company/api-proxy/

# 查看今天所有 API 调用摘要
python3 log_viewer.py

# 查看最后 5 条调用
python3 log_viewer.py --last 5

# 查看第 3 条调用的完整详情（prompt + 回复）
python3 log_viewer.py --id 3

# 查看完整内容（不截断）
python3 log_viewer.py --id 3 --full

# 今日统计（token 用量、模型分布、成功率）
python3 log_viewer.py --stats

# 只看失败的请求（非 200）
python3 log_viewer.py --errors

# 搜索包含关键词的调用
python3 log_viewer.py --search "飞书文档"

# 查看昨天的日志
python3 log_viewer.py --date 2026-03-09

# 查看昨天最后 10 条
python3 log_viewer.py --date 2026-03-09 --last 10

# 生成飞书文档（列表形式）
python3 log_viewer.py --feishu
python3 log_viewer.py --last 10 --feishu

# 生成飞书文档（单条详情）
python3 log_viewer.py --id 3 --feishu
```

---

## 日志格式说明

每条日志存储为 JSONL 格式（一行一个 JSON 对象），字段如下：

| 字段 | 类型 | 说明 |
|------|------|------|
| `timestamp` | string | ISO 8601 时间（含时区，Asia/Shanghai） |
| `request_id` | string | 唯一请求 UUID |
| `method` | string | HTTP 方法（POST） |
| `path` | string | 请求路径（如 `/v1/messages`） |
| `streaming` | bool | 是否为流式请求 |
| `request_headers` | object | 请求头（认证字段已脱敏） |
| `request_body` | object | 完整请求体（含 model、system、messages） |
| `response_status` | int | HTTP 状态码 |
| `response_headers` | object | 响应头 |
| `response_body` | object | 非流式响应体（含 content、usage） |
| `response_body_parsed` | object | 流式响应解析结果（重建的完整响应） |
| `response_body_raw_stream` | string | 流式原始 SSE 数据（可选） |
| `duration_ms` | float | 请求耗时（毫秒） |
| `error` | string | 代理出错时的错误信息 |

### 示例日志条目

```json
{
  "timestamp": "2026-03-10T22:00:00.000000+08:00",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "method": "POST",
  "path": "/v1/messages",
  "streaming": true,
  "request_body": {
    "model": "claude-sonnet-4-6",
    "max_tokens": 4096,
    "system": "你是龙虾总经理...",
    "messages": [
      {"role": "user", "content": "帮我写一份报告"}
    ]
  },
  "response_status": 200,
  "response_body_parsed": {
    "content": [{"type": "text", "text": "好的，以下是报告..."}],
    "usage": {"input_tokens": 512, "output_tokens": 1024}
  },
  "duration_ms": 8432.5
}
```

---

## 注意事项

1. **不要擅自重启 Gateway**：修改 `openclaw.json` 后需要重启 Gateway，但重启会中断当前所有对话，务必先与用户确认再操作。

2. **上游地址配置**：`proxy.py` 中的默认上游地址是 `http://model.mify.ai.srv/anthropic`，如果你的上游地址不同，需要手动修改并重新加载 LaunchAgent。

3. **流式 token 统计**：流式调用的 token 用量保存在 `response_body_parsed.usage` 中。部分早期日志中该字段可能为 0（旧版解析逻辑限制）。

4. **飞书文档依赖**：`--feishu` 功能依赖 `feishu_write.py`（路径：`~/.openclaw/workspace/company/feishu_write.py`），需要确保该文件存在且飞书鉴权正常。

5. **日志大小**：流式请求会额外保存原始 SSE 数据（`response_body_raw_stream`），长对话的日志条目可能较大。

6. **端口冲突**：默认端口 18790，如需修改，同时更新 plist 和 `openclaw.json` 中的 `baseUrl`。

---

## 文件说明

```
skills/api-logger/
├── SKILL.md          # OpenClaw Skill 描述（OpenClaw 读取此文件）
├── proxy.py          # 透明代理服务（aiohttp）
├── log_viewer.py     # 日志查看/分析工具
├── install.sh        # 一键安装脚本
└── README.md         # 本文档
```

安装后的运行时文件：

```
~/.openclaw/workspace/company/api-proxy/
├── proxy.py          # 运行中的代理服务
└── log_viewer.py     # 日志查看工具

~/.openclaw/workspace/company/api-logs/
├── 2026-03-10.jsonl  # 按日存储的日志
├── proxy.stdout.log  # 代理服务标准输出
└── proxy.stderr.log  # 代理服务错误日志

~/Library/LaunchAgents/
└── com.lobster.api-proxy.plist  # 开机自启动配置
```

---

*🦞 Made with lobster energy. 龙虾公司出品。*
