# Prana 封装技能（共享包）

本目录为从 Prana 封装下载的**轻量技能包**：不含业务实现代码，含根目录 **`SKILL.md`**、**薄客户端**与 **`skill.yaml`**。frontmatter 中 **`skill_key`** 为公开包标识（Prana 源 `skill_key` + 后缀 **`_public`**），**`original_skill_key`** 为 Prana 上实际执行的专业技能 key。

## 目录说明

封装包**包含** 根目录 **`skill.yaml`**（OpenClaw / Claw Hub 等入口描述，与 `SKILL.md` 配套）。

| 文件/目录 | 说明 |
|-----------|------|
| `SKILL.md` | frontmatter 含 **`skill_key`**（=`{源 skill_key}_public`）、**`original_skill_key`**（= Prana 源技能 key）、`name`、`description` 及可选 `input_format` 等；薄客户端对 **`/api/claw/agent-run` 使用 `original_skill_key`** |
| `skill.yaml` | 含 **`skill_key`**、**`original_skill_key`**（含义同上）及 OpenClaw 字段（`entryPoint` → `scripts/prana_skill_client.py`），封装时生成 |
| `scripts/prana_skill_client.py` | 调用 Prana API 的入口脚本（无业务逻辑） |
| `config/api_key.txt` 或 `config/api_key.json` | 存放 GET /api/v1/api-keys/ 返回的凭证（勿提交到公开仓库） |

公开包自身的标识为 **`{源 skill_key}_public`**（仅用于包名/元数据）；**调用远端时仍使用 `SKILL.md` 中的 `skill_key`（源 key）**。

## `skill.yaml` 说明（不是 `SKILL.yaml`）

根目录文件名为**小写** **`skill.yaml`**，由 **Prana 服务端在封装时自动生成**（调用 `/api/skill/encapsulate/run` 或 `/download` 打入 tar.gz），**无需、也不应**手工编写。

| 项目 | 说明 |
|------|------|
| **作用** | 给 OpenClaw / Claw Hub 等渠道读的**技能清单**：名称、版本、`entryPoint` 指向 `scripts/prana_skill_client.py` |
| **生成来源** | 基于源技能目录的 `SKILL.md`（名称、描述、`trigger`→keywords、`license` 等）+ 当前**上线版本号** |
| **主要字段** | `skill_key`（公开包）、`original_skill_key`（Prana 源技能）、`name`、`version`、`description`、`entryPoint` 等 |
| **可选** | 若源 `SKILL.md` frontmatter 有 `trigger`，会写入 `triggers.keywords` |
| **与 `SKILL.md` 分工** | 两者字段一致；运行时 **`agent-run` 的 `skill_key` 取自 `original_skill_key`** |

## 快速开始

1. **获取 API Key**（首次无本地凭证时）  
   调用 `GET /api/v1/api-keys/`。  
   **可选**查询参数：`account_id`、`phone`、`email`。  
   - **`account_id`**：已有账户 UUID 时传入，可为该账户获取或创建 Key。  
   - **沙盒**：环境变量 **`ACCOUNT_ID`** 由沙盒注入当前账户；若已设置，请求时带上 `?account_id=<ACCOUNT_ID>`；**读不到或未设置则不要传** `account_id`。  

   示例（有 `ACCOUNT_ID` 时）：

   ```bash
   curl -sS "${NEXT_PUBLIC_URL}/api/v1/api-keys/?account_id=${ACCOUNT_ID}"
   ```

   无 `ACCOUNT_ID` 时直接请求根路径即可（仍可用 `phone` / `email` 等，见服务端约定）。

   响应示例：

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

   将 **`data.api_key`** 中的 `public_key`、`secret_key` 保存为：  
   - **`config/api_key.json`**：粘贴完整 JSON（含 `code`/`data` 均可，脚本会解析）；或  
   - **`config/api_key.txt`**：单行 `public_key:secret_key`（中间一个英文冒号）。

2. **调用技能**

   脚本请求 `POST /api/claw/agent-run` 与（必要时）`POST /api/claw/agent-result` 时，会在请求头加入 **`x-api-key: public_key:secret_key`**（**body 不传 `api_key`**）。  
   - **agent-run** body：`skill_key`（= **`original_skill_key`**，Prana 源技能）、`question`（由 frontmatter 参数说明与用户消息组装）、`thread_id`、`request_id`。  
   - **agent-result** body：仅 `request_id`。  
   `request_id` 不在 `content` 字符串内。

   ```bash
   export NEXT_PUBLIC_URL=https://你的-prana-域名   # 可选，有默认值时请按文档修改
   python3 scripts/prana_skill_client.py -m "用户说的话或任务描述" -t ""
   ```

   第二轮起传入上次响应中的 `thread_id`（若接口返回）：`-t <thread_id>`。

   **长任务与网络异常**：脚本先请求 `POST /api/claw/agent-run`（带 `x-api-key`）；若超时、连接失败、或网关/服务端错误（5xx、408、504），或 200 但响应非合法 JSON，会自动再请求 `POST /api/claw/agent-result`，同样带 `x-api-key`，Body 仅 `request_id`。成功经此路径返回的 JSON 会带 `_recovered_via: "agent-result"` 字段。

3. **环境变量**（可选）

   - `NEXT_PUBLIC_URL`：Prana API 根 URL  
   - `PRANA_SKILL_PUBLIC_KEY` + `PRANA_SKILL_SECRET_KEY`：优先于配置文件  
   - `PRANA_SKILL_API_KEY`：整段 JSON，或单行 `public_key:secret_key`

## 与渠道的集成

各渠道 LLM（Cursor、OpenClaw 等）应在运行本技能时：

1. 检查本地是否已配置 `public_key`/`secret_key`；若无则先 `GET /api/v1/api-keys/`（见 `skill.yaml` / 服务端约定的 create_key 路径）再写入 `api_key.json` 或单行 `api_key.txt`。  
2. 将用户消息作为 `-m` 传入，维护 `thread_id` 实现多轮对话。  
3. 若返回付费链接（HTTP 402 等），按文档引导用户完成支付后重试。

## 安全说明

- 勿将 `config/api_key.txt` 提交到公开 Git 仓库。  
- 本包内**不包含**专业技能实现脚本，知识产权保留在 Prana 服务端。
