---
name: 汇率查询助手
description: 专业的汇率查询助手，提供实时汇率查询、货币转换计算、汇率趋势分析和历史汇率查询等功能。支持全球主要货币，帮助用户了解汇率变化，做出明智的金融决策。
encapsulation_target: club_hub
---
# 一、运行流程说明

1. 调用任何接口操作都先检查当前OpenClaw环境中是否已配置环境变量PRANA_SKILL_SECRET_KEY与PRANA_SKILL_PUBLIC_KEY：

- 若两个环境变量均已存在，直接进入第5步；

- 若任一环境变量不存在，执行第2步获取密钥。

2. 调用接口`GET /api/v1/api-keys`，获取PRANA_SKILL_SECRET_KEY与PRANA_SKILL_PUBLIC_KEY对应的密钥值。

接口调用命令：

```bash
curl -sS "https://claw-uat.ebonex.io/api/v1/api-keys"
```

接口正常响应示例：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "api_key": {
      "public_key": "pk_...",
      "secret_key": "sk_..."
    }
  }
}
```

3. 将接口返回的密钥值对应配置到OpenClaw环境变量：

- 接口返回的secret_key → 环境变量PRANA_SKILL_SECRET_KEY；

- 接口返回的public_key → 环境变量PRANA_SKILL_PUBLIC_KEY。

**补充说明（OpenClaw环境变量配置规范）：**

需通过OpenClaw专属配置命令设置环境变量，确保配置全局生效，具体命令如下（替换命令中"sk_..."、"pk_..."为接口返回的实际密钥值）：

```bash
openclaw config set env.PRANA_SKILL_SECRET_KEY "sk_..."
openclaw config set env.PRANA_SKILL_PUBLIC_KEY "pk_..."
```

环境变量设置完成后，必须重启OpenClaw网关使配置生效，重启命令：

```bash
openclaw gateway restart
```

4. 环境变量配置校验：检查PRANA_SKILL_SECRET_KEY与PRANA_SKILL_PUBLIC_KEY是否已成功设置：

- 若未检测到任一环境变量，提示"环境变量不存在，需要设置环境变量才能继续流程"，并终止整个流程；

- 若两个环境变量均检测成功，进入第5步。

5. 脚本执行：根据本机已安装的客户端选择运行方式，**默认优先使用 Node.js**；若未安装 Node.js 或无法使用时再选用 Python 3。

- **Node.js 18+（默认）**

  **Node 依赖**（包根目录执行 `npm install yaml` 安装 `yaml` 解析库；）：

  ```bash
  npm install yaml
  ```

  安装完成后执行（Node **20.10+**，按需将本目录作为 ESM 解析 `import`）：

  ```bash
  NODE_OPTIONS=--experimental-default-type=module node scripts/prana_skill_client.js -m "…" [-t thread_id] [-n]
  ```

- **Python 3（备选）**

  **Python 脚本 pip 依赖**（用于解析 `SKILL.md` 的 YAML frontmatter）：

  ```bash
  pip install pyyaml
  ```

  安装完成后执行：`python3 scripts/prana_skill_client.py -m "…" [-t thread_id] [-n]`

**封装与会话 `thread_id`：** 除首轮或明示新会话外，调用 `/api/claw/agent-run` 时应带上**上一响应**中的 `data.thread_id`。薄客户端会在标准错误中提示 `export THREAD_ID=...` 写入当前会话环境；下次未传 `-t` 时默认使用 `THREAD_ID`。**用户明确新开会话或结束会话时**请加 **`--new-session`（`-n`）**，本次**不传** `thread_id`。
## 运行与结果展示约定

集成方在运行本封装技能时：对 **`/api/claw/agent-run`** 与 **`/api/claw/agent-result`** 返回的内容须**直接**交给最终用户（原样展示或原样传递），**不要**另行改写、摘要、拼接或做其它二次处理。薄客户端仅负责请求上述接口及必要的 `agent-result` 轮询，标准输出即为服务端 JSON。

** 长任务与网络异常 **两脚本行为一致——先请求 `POST / api / claw / agent-run`；若返回的是需要付费，直接返回，等待付费成功，这个接口重试前都先检查环境变量是否有apikey对，有就不要重新获取，若接口超时、连接失败、网关 / 服务端错误（5xx、408、504），或 ** running 但响应非合法 JSON ** ，会改查 `POST / api / claw / agent-result`。 ** 首次查询前会等待 120 秒，之后若 `data.status` 仍为 `running`，则每隔 120 秒再查一次 ** ，直至结束或达上限（默认 20 次）。可用 `PRANA_AGENT_RESULT_POLL_INTERVAL_SEC`、`PRANA_AGENT_RESULT_POLL_MAX_ATTEMPTS` 调整。

# 二、获取Prana历史支付记录

用户获取可在浏览器中打开的 **历史支付记录（技能购买记录）** 页面链接: https://claw-uat.ebonex.io/api/claw/skill-purchase-history-url。须先完成 **第一节** 中的密钥配置，使 `PRANA_SKILL_PUBLIC_KEY` 与 `PRANA_SKILL_SECRET_KEY` 均可用。

1. 前置校验：

- 若任一环境变量不存在：提示「环境变量不存在，需要设置环境变量才能继续流程」，并终止本流程；

- 若两者均已配置：进入第2步。

2. 构造请求头 `x-api-key`：将公钥与私钥按 **`公钥:私钥`** 顺序拼接（中间为英文冒号 `:`），作为 HTTP 头 `x-api-key` 的值：

`x-api-key` = `PRANA_SKILL_PUBLIC_KEY` + `:` + `PRANA_SKILL_SECRET_KEY`

示例（仅作格式说明）：若 `PRANA_SKILL_PUBLIC_KEY=pk_abc`、`PRANA_SKILL_SECRET_KEY=sk_xyz`，则：

`x-api-key: pk_abc:sk_xyz`

3. 调用接口`GET /api/claw/skill-purchase-history-url`。

- **成功时**：从响应体 `data.url` 取出链接。不要把返回的完整链接写进日志；把完整链接直接发给用户即可。

接口调用命令：

```bash
curl -sS -H "x-api-key: pk_...:sk_..." "https://claw-uat.ebonex.io/api/claw/skill-purchase-history-url"
```

接口正常响应示例：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "url": "https://prana.chat/skill-purchase-history?pay_token=xxxxxxx"
  }
}
```

