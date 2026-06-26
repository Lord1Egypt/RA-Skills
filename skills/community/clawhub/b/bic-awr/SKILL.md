---
name: bic-awr
description: 当用户需要分析数据库 AWR（或兼容）报告时使用。调用官方 API 需要有效凭据，详见正文 Setup
homepage: https://www.bic-qa.com
version: 1.0.0
---

## 概述

将数据库性能报告提交到 **BIC-Skills AWR 分析 API**（HTTPS），由服务端异步处理，分析结果通过邮件发送。

**Base URL（AWR）**：`https://api.bic-qa.com/skills/awr`

## Setup

> **Security note：** 本技能仅向 **BIC-QA 官方 API**（`api.bic-qa.com`）发送凭据，与官网账户体系一致。API Key 仅以 `Authorization: Bearer …` 形式出现在请求头中，不会写入其它域名、本地日志或随技能文件分发。

### 1. 注册并获取 API Key

按顺序完成（界面以官网实际为准）：

1. 打开 **BIC-QA 官网**：https://www.bic-qa.com  
2. **注册**账号（按页面提示填写邮箱/手机等并完成验证，若已有账号则直接登录）。  
3. 登录后进入 **用户中心 / 控制台 / API 管理** 等页面（具体名称以官网为准），找到 **API Key** 或 **访问令牌** 入口。  
4. **创建或查看** API Key，复制并妥善保存（仅自己可见，勿提交到公开仓库）。

官网提供免费 API Key；若页面有「重置 / 轮换」功能，更新后需同步修改本地或环境变量中的配置。

### 2. 存储 API Key（二选一）

集成层或 Agent 在发请求前需能读到 Key，并组装为 **`Authorization: Bearer <你的_API_Key>`**。

**方式 A — 配置文件（推荐）：**

```bash
mkdir -p ~/.bic/config
chmod 700 ~/.bic/config
echo "your_api_key_here" > ~/.bic/config/api_key
chmod 600 ~/.bic/config/api_key
```

**方式 B — 环境变量：**

```bash
export BIC_API_KEY="your_api_key_here"
```

Agent 会按优先级依次尝试：环境变量 → 配置文件。

## 凭证预检

每次调用 API 前，先确认 API Key 可用。若为空，停止调用并提示用户按 **Setup** 完成注册与配置。

```bash
# Load user-provisioned BIC-QA API key (used ONLY for api.bic-qa.com authentication)
BIC_QA_KEY="${BIC_API_KEY:-$(cat ~/.bic/config/api_key 2>/dev/null)}"
if [ -z "$BIC_QA_KEY" ]; then
  echo "缺少 BIC-QA API Key，请先在 https://www.bic-qa.com 注册获取，并按 Setup 配置 BIC_API_KEY 或 ~/.bic/config/api_key"
  exit 1
fi
```

## API 调用模板

AWR 接口为 **HTTP POST**，发往 **`https://api.bic-qa.com/skills/awr`**。支持 **multipart 上传文件**（推荐）或 **JSON + 服务端可访问路径**。

### 方式一：multipart 上传文件（推荐）

适合助手直接上传用户提供的报告文件；`Content-Type` 由客户端自动生成 boundary。

```bash
# All requests go ONLY to the official BIC-QA API (api.bic-qa.com)
curl -s -X POST "https://api.bic-qa.com/skills/awr" \
  -H "Authorization: Bearer ${BIC_QA_KEY}" \
  -F "dbtype=oracle" \
  -F "lang=zh" \
  -F "file=@/path/to/awr_report.html"
```

- 至少包含 **一个带文件名的文件字段**（字段名以实际客户端为准，常见为 `file` 等）。  
- `dbtype`（必填）：小写，须为服务端支持的库类型（常见如 `oracle`、`kingbase` 等，与 bic-skills 校验一致）。  
- `lang`（可选）：见下文「lang（语言）」。

### 方式二：JSON + 服务端可访问的本地路径

适用于 **运行 bic-skills 的环境能读取该路径** 的场景（例如代理与文件在同一机器）。公开云 API 若无法访问本机路径，请优先用 **方式一**。

```bash
curl -s -X POST "https://api.bic-qa.com/skills/awr" \
  -H "Authorization: Bearer ${BIC_QA_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"file":"/path/to/awr_report.html","dbtype":"oracle","lang":"zh"}'
```

| 字段     | 必填 | 说明 |
| -------- | ---- | ---- |
| `file`   | 是   | AWR 报告文件的**路径**（字符串） |
| `dbtype` | 是   | 数据库类型（小写） |
| `lang`   | 否   | 见下文「lang（语言）」 |

## lang（语言）

`lang` 表示分析结果/邮件侧重的界面语言，**应按用户当前交流语言选择**，而非固定写死：

| 用户语言环境 | 建议 `lang` |
| ------------ | ------------- |
| 中文（简体/繁体等中文交互） | `zh` |
| 英文（用户主要使用英文提问、界面为英文等） | `en` |

若无法判断，可依据用户本轮对话所用语言：中文对话用 `zh`，英文对话用 `en`。未传 `lang` 时由服务端默认处理（以实际接口行为为准）。

## 成功与失败

- 成功时响应体通常包含 `status: "success"` 及提示用户稍后查收邮件的 `message`。  
- 失败时根据返回的 `error` 或 `message` 向用户说明原因（文件缺失、类型不支持、未授权等）。  
- 分析为异步，**不要**承诺即时返回完整分析报告；应提示用户关注邮箱（含垃圾邮件文件夹）。

## 错误与未授权时的行为

- **401** 或缺少/无效 `Authorization`：不要假装已上传成功；用与用户一致的语言说明需前往 https://www.bic-qa.com 获取或更新 API Key，并在请求头使用 `Bearer` 方式携带。  
- **400** 等客户端错误：根据服务端信息提示修正 `dbtype`、文件或参数。  
- **5xx** 或其它错误：如实说明调用失败，可建议稍后重试。

## 隐私与安全

- AWR 文件可能含敏感信息，仅在用户明确需要上传时调用，并提醒在可信环境中操作。

## 工作流程建议

1. 确认用户意图为上传/分析 AWR（或兼容）报告，并确定 `dbtype` 与 `lang`。  
2. 使用已配置的 API Key，优先以 **multipart** 将文件提交至 `POST https://api.bic-qa.com/skills/awr`。  
3. 根据响应提示用户异步查收邮件，勿虚构即时完整报告内容。

## 相关资源

- 官网：https://www.bic-qa.com  
- 技术支持：support@dbaiops.com  
- Gitee：https://gitee.com/BIC-QA/BIC-QA  
- GitHub：https://github.com/BIC-QA/BIC-QA  
