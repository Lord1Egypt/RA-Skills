---
name: fosun-env-setup
description: 复星 OpenAPI 共享凭证 `fosun.env` 的独立生成与修复模块。覆盖首次开通/换设备/凭据丢失、apikey 过期续期、凭据无效重置；已开通回填须同时提供 apikey 与页面服务端公钥；验证通过才写入共享 `fosun.env`。
requires:
  bins:
    - python3
---

# fosun-env-setup

本模块只负责共享 `fosun.env` 的生成与修复，不执行实盘或模拟盘业务。

**凭据管理全流程（必读）**：处理开通 / 换设备 / 重置 / 续期 / `--api-key` 回填前，先阅读本 skill 内 [`reference/credential-management-flow.md`](reference/credential-management-flow.md)。关键不变量：`serverPubKey` 按 ticket 生成（每次不同），客户端私钥、服务端公钥、授权 url 三者属于**同一 ticket** 的原子单元，禁止跨 ticket 混用；回填被判 invalid 时**复用当前二维码、不轮换密钥**（见 reference §7）。

## 凭据模型

- 每个账户 ↔ 一个 OpenAPI apikey
- 每个 apikey ↔ 一对客户端密钥 + 服务端密钥；本地保存 apikey、客户端私钥、服务端公钥

## 三类场景（主流程）

| 场景 | 何时触发 | 命令 | URL | 轮换客户端密钥 | 用户须回填（页面复制） |
|------|----------|------|-----|----------------|------------------------|
| 1 首次/换机/丢失 | 无有效凭证，默认入口 | `ensure_fosun_env.py` | 普通开通页 | 无则生成 | 点了「忘记 API 参数」时：**apikey + 服务端公钥** |
| 2 过期续期 | 业务返回 40010，或主动续期 | `ensure_fosun_env.py --renew` | hash 带 `isExpired=1` | 否 | 否 |
| 3 无效/损坏 | 业务返回 40001/40015，或主动重置 | `ensure_fosun_env.py --reset-credentials` | 普通开通页 | **是** | **是**：**apikey + 服务端公钥** |

场景 1 与换设备/凭据丢失**无法区分**：返回 JSON 的 `user_message` / `operation_guide` 会引导——若曾开通过须在页面上点 **「忘记 API 参数」**，重置后把页面上 **apikey 与服务端公钥（PEM）** 一并发给 Agent；Agent 执行 `--api-key` 与 `--server-public-key` 回填，并把 pending 中本次 ticket 的客户端私钥晋升到正式 `fosun.env`，再验证。

> **不变式（最重要）**：已开通/忘记 API 参数场景，用户必须同时提供 **API Key + 服务端公钥**，Agent 凑齐后一次性执行 `--api-key` 与 `--server-public-key` 回填，**禁止只回填 apikey**（页面公钥与 ticket 临时公钥不同，见 reference）。首次开通仍回复「开通好了」即可；续期无需回填。

> **过期 × 换设备（易踩坑的交集）**：换新设备时本地没有 apikey，**无法直接 `--renew`**。正确顺序：① 默认入口签码；② 用户点「忘记 API 参数」后把 **apikey + 服务端公钥** 一并发给 Agent；③ `--api-key` 与 `--server-public-key` 写入 env；④ finalize 识别过期后自动转续期。

## 路径规则

- 默认路径：本模块父目录的 `fosun.env`，即与 `moni-trade-skill` 并列的共享凭证。
- `FOSUN_ENV_PATH` 可覆盖默认路径。
- `FOSUN_ENV_PATH` 是相对路径时，以总入口目录为基准解析，禁止依赖当前 shell 的工作目录。
- 验证通过的正式凭证会额外备份到 skill 目录之外的系统原生用户数据目录：macOS 使用 `~/Library/Application Support/fw-trade-skill/fosun-env-backups`，Linux 使用 `${XDG_DATA_HOME:-~/.local/share}/fw-trade-skill/fosun-env-backups`，Windows 使用 `%LOCALAPPDATA%\fw-trade-skill\fosun-env-backups`。
- `FOSUN_ENV_BACKUP_DIR` 可覆盖备份目录；相对路径以用户 home 为基准解析。

## 最小入口（场景 1：首次开通 / 换设备 / 凭据丢失）

```bash
python3 fosun-env-setup/code/ensure_fosun_env.py
```

**默认行为**：立即 TicketCreate 签发**新** ticket 并返回 JSON，含 `credential_scenario=setup`、`created_new_ticket=true`、`qr_media`、`exact_open_url`、`operation_guide`、`user_message`。每次进入 pending 对接流程都会调用 TicketCreate，**不会**复用本地缓存的旧 ticket/open_url（ticket 可能过期或失效）。用户已在 H5 完成开通并回复「开通好了」时，脚本会先尝试 finalize；成功则 `status=valid`，失败才签发新 ticket。

**二维码交付（一次多发 + 主动询问）**：

1. 脚本在脚本执行机生成 PNG，JSON 返回 `qr_media`、`qr_png_path`、`qr_image`、`show_qr_rule`
2. 模型按 `show_qr_rule` 一次多发二维码：
   - 必做：写 `exact_open_url` 进回复（用户随时可点击）
   - 必做：调用 `deliver_attachments` 发 `qr_png_path`（最广泛兼容），并在回复中提醒用户在附件中查看二维码
   - 可选：若平台支持 media，发 `qr_media.path`
   - 可选：若平台支持 Markdown data URI，发 `qr_image.data`
3. 发完必须问：「收到附件中的二维码了吗？如不能（只有链接/报错等），告诉我，我换方式重发」
4. 用户说看不到 → 问「看到了什么？」→ 换一种方式重试（不要重复已失败的方式）

禁止：只发一种方式；用 Read 工具"展示"图片（用户看不到）；假设某平台一定支持某能力。

## 场景 2：apikey 过期续期

```bash
python3 fosun-env-setup/code/ensure_fosun_env.py --renew
```

或在实盘/模拟盘业务中命中 `40010` 时，由 `real-trade-skill` 分派到同一续期逻辑。URL hash 带 `isExpired=1`；**不**更换 apikey 与客户端私钥。用户扫码续期后直接重试原操作。

续期要求**本地已有 apikey 与服务端公钥**。换新设备（本地无 apikey）时不能直接续期，须先按上文「过期 × 换设备」交集流程：开通/重置签码 → 用户回填 **apikey + 服务端公钥** → 工具识别过期后自动转续期。

## 回填（已开通 / 「忘记 API 参数」）— 必须两项齐全

适用：场景 1 中用户点了「忘记 API 参数」、场景 3 重置扫码后、换设备凭据丢失等——凡需把**页面上已开通账号**的参数写入本地，均走本回填，**不是**首次开通（首次开通用户回复「开通好了」后重跑默认入口即可，无需本命令）。

**硬性要求（缺一不可）**：

1. **API Key**：用户在授权页复制的 `ak_...` 原文  
2. **服务端公钥**：同一页面展示的 `-----BEGIN PUBLIC KEY-----` … `-----END PUBLIC KEY-----` 全文  

禁止只执行 `--api-key`、禁止省略 `--server-public-key`。页面上的服务端公钥与 TicketCreate 返回的临时 `serverPubKey` **通常不同**，必须用页面那份；客户端私钥由本次 ticket 的 pending 自动晋升，无需用户发送。

```bash
python3 fosun-env-setup/code/ensure_fosun_env.py \
  --api-key '<页面 API Key>' \
  --server-public-key '<页面服务端公钥 PEM 全文>'
```

已 `install.sh` 时用 `$FOSUN_PY` 替代 `python3`。用户只发来 apikey 时，**先向用户索要同页的服务端公钥**，凑齐后一次性执行上述命令。

## 场景 3：凭据无效 / 损坏重置

```bash
python3 fosun-env-setup/code/ensure_fosun_env.py --reset-credentials
```

或在业务中命中 `40001` / `40015` 时由错误分派触发。脚本会**轮换客户端密钥对**并 TicketCreate；用户须在页面上点 **「忘记 API 参数」** 后，按上文 **「回填」** 节同时提供 apikey 与服务端公钥并执行回填命令。

> **回填被判 invalid 时不要重新扫码（防死循环）**：回填会写入 apikey 与公钥后再校验。若返回 `api_key_rejected=true`、`created_new_ticket=false`，**复用当前二维码**：让用户在同一页面再点「忘记 API 参数」，把页面上 **apikey + 服务端公钥** 一并发来，再次执行**完整回填命令**（`--api-key` 与 `--server-public-key` 都要有）。禁止重新签发 ticket 或轮换密钥。

首次开通（未点「忘记 API 参数」）无需回填命令，用户回复「开通好了」后再次运行默认入口即可。

## 结果含义

- `status=pending`：已通过 TicketCreate 签发新开通/续期/重置 URL（`created_new_ticket=true`）。须读 `credential_scenario` 与 `operation_guide`：用 media 发 `qr_media.path` 并转发 `exact_open_url`。授权中材料在 pending state，正式 `fosun.env` 不写 `pending` 凭证。场景 1 用户回复「开通好了」后再运行本脚本；需回填时按 **「回填」** 节执行 `--api-key` 与 `--server-public-key`。
- `status=valid`：共享凭证已可用，包含账户索引、本地客户端私钥、API Key 和服务端公钥。
- `status=error`：本地依赖、网络或认证接口失败，停止后续业务脚本。

如果 `fosun.env` 缺失或缺少完整密钥材料，脚本会先从用户级本地备份自动恢复并重新校验，恢复成功时 JSON 中会包含 `restored_from_backup`。

## 误删与备份恢复

**触发**：用户说删了或丢了 `fosun.env`；或默认入口/`--repair` 后仍未 `valid` 且没有 `restored_from_backup`。

**Agent 操作**：直接运行 `ensure_fosun_env.py`（或 `--repair`）。**禁止**手动拷贝备份文件、向用户索要客户端私钥，或尝试从服务端「找回私钥」——`FSOPENAPI_CLIENT_PRIVATE_KEY` 只能在本地生成。

**成功**：`status=valid` 且含 `restored_from_backup` → 告知已从用户级本地备份恢复（路径见 §路径规则），可继续业务；无需重新扫码开通。

**失败**：备份目录也无可用副本（用户连备份一起删了）→ 与换机/凭据丢失相同，走 **场景 1** 默认入口签码；若 apikey 仍无效则 **场景 3** `--reset-credentials` 后按 **「回填」** 节提供 apikey + 服务端公钥。验证通过后的正式凭证会继续写入 §路径规则中的备份目录。

## 其它参数

```bash
python3 fosun-env-setup/code/ensure_fosun_env.py --repair
python3 fosun-env-setup/code/ensure_fosun_env.py --force-new-ticket   # 跳过 finalize，立即签新 ticket
```

## 输出纪律

脚本只输出结构化 JSON。不要把 `fosun.env` 的密钥字段原样展示给用户。`status=pending` 时须汇报：`credential_scenario`、`user_message`、`operation_guide`、`qr_media`、`exact_open_url`、`next_action`。需要用户回填时（`requires_api_key_from_user` / `requires_server_public_key_on_backfill` 等）：**必须等用户同时提供 apikey 与页面服务端公钥**，再执行 `--api-key` 与 `--server-public-key`，禁止只回填 apikey。
