---
name: byted-livesaas-master
description: 企业直播 / LiveSaaS 控播 Skill。支持通过 `bytedlive` CLI 操作直播间（创建/配置/状态）、评论、系统消息、观众管控，以及 OpenAPI 兜底调用。覆盖场景包括：直播间生命周期管理、直播数据与观众画像分析、商品卡片运营（上架/讲解）、营销互动工具（卡券）与连麦协同控制、媒资库运维及账号/权益信息查询。触发词：企业直播、控播、直播间、ActivityId、评论、弹幕、禁言、拉黑、踢人、商品卡片、直播数据、观众画像、火山引擎 livesaas。
version: 1.1.4
---

# byted-livesaas-master（企业直播控播）

## 0. 启动埋点

每次启用本 Skill 时，先 best-effort 执行一次埋点脚本，再继续处理用户请求；脚本失败、超时或接口不可达时不得中断任务。

```bash
node tools/report_usage.js
```

脚本根据 Skill **安装路径**自动识别 Agent（如 `~/.cursor/skills/` → `cursor`，`~/.codex/skills/` → `codex`）。**禁止**在未识别当前环境时硬编码 `--agent codex`。仅在自定义安装目录（`skills add --target`）或自动识别失败时，显式传入 `--agent cursor|codex|claude-code|trae|openclaw`；仍无法识别时使用 `unknown`。该脚本由 Node/CLI 发起 POST 上报，不支持浏览器页面跨域调用。

## 1. 适用范围

### When to use

当用户意图涉及以下任一场景时触发本 Skill：

- **直播间生命周期管理与管控**：创建/删除直播间，查询列表，修改基础配置（名称/时间/模式），控制状态（开播/锁定/恢复/下播/封禁）
- **直播数据分析与观众画像**：查询直播间观看时长分布统计、拉取观众用户画像明细用于洞察
- **商品库与卡片运营**：直播中对商品卡片进行上架、讲解态切换，查询商品状态或统计数据
- **评论治理与内容分析**：发送/查询/轮询评论，删除用户消息，配置敏感词，或获取评论的分析结果（含大模型分析）
- **账号基础信息与媒资库运维**：获取账号配置/全局权益额度信息，批量删除媒资库视频，检查文档库容量
- **营销互动与连麦控制**：创建直播间卡券等互动工具，管理网页直播连麦协同状态
- **系统消息**：向直播间推送系统定制消息
- **观众管控**：针对观众的禁言、拉黑、踢出
- **观看页外观**：切换主题（暗黑/清爽/经典/传统节庆）
- **OpenAPI 兜底**：上述未明确覆盖到的其余企业直播能力操控需求，通过调用企业直播OpenAPI来实现

### When NOT to use

- **推流/拉流/编码等底层媒体问题** → 不属于本 Skill
- **WebSDK 接入 / 小程序进房 / 观看端 Token** → 使用 **byted-livesaas-dev** Skill
- **账号计费 / 套餐管理** → 引导用户至火山引擎控制台
- **非企业直播产品**（如视频点播、RTC）→ 不属于本 Skill

## 2. 架构概览

```
用户意图 → Skill（路由 + 约束） → Agent 生成逻辑命令 → 解析可用 CLI 入口 → bytedlive / bytedlive-b CLI 执行
```

- **Skill 层**：定义意图到 CLI 子命令的映射 + 执行约束（不含可执行脚本）
- **Agent 层**：根据路由表与约束拼装逻辑命令，并按 §2.1 解析实际 CLI 入口后执行
- **CLI 层**：封装凭证管理、签名、请求发送、确认交互与 JSON 结果

> **唯一执行入口**：所有命令必须通过 `bytedlive` / `bytedlive-b` CLI，禁止手写 curl 或未文档化的 HTTP 请求。

### 2.1 CLI 入口解析与内外网降级

本 Skill 文档中的 `bytedlive ...` 均表示逻辑命令。Agent 真正执行前必须先解析可用入口：

1. **公网优先**：优先执行 `bytedlive --version`；可用时默认使用 `bytedlive`。
2. **身份确认**：可执行 `bytedlive cli identity --pretty` 查看当前包名、版本、bin 列表与 `internal_bin`。若返回 `internal: true` 或 `internal_bin: "bytedlive-b"`，说明当前安装包具备内网入口。
3. **不可用降级**：当 `bytedlive` 不存在、业务子命令/全局选项不可用、返回 `unknown command` / `unknown option` / `command not found` / `Cannot find module` 等 CLI 能力缺失类错误时，不要直接失败；若本机存在 `bytedlive-b`，用相同参数改为 `bytedlive-b ...` 重试一次。
4. **BOE / 测试环境**：用户明确指定 BOE、测试环境或内网调试时，仍先尝试 `bytedlive --boe ...`；若 `--boe`、`boe` 子命令或相关选项不可用，再切换为 `bytedlive-b --boe ...` 或 `bytedlive-b boe ...`。
5. **安装顺序**：两者均不可用时，先安装公网包 `npm i -g bytedlive-cli` 并验证 `bytedlive --version`；若公网包安装失败、命令仍不可用，或当前网络/registry 无法获取公网包，再安装内网包 `npm i -g @byted-vcloud/bytedlive-cli --registry http://bnpm.byted.org` 并验证 `bytedlive-b --version`。
6. **命令展示**：除安装失败需要用户手动处理外，对用户只说明“正在尝试公网 CLI / 已切换内网 CLI”，不要暴露完整命令、AK/SK、请求体或 JSON 参数。

后续章节的命令示例默认写作 `bytedlive ...`；实际执行时必须按本节规则替换为已解析出的 `bytedlive` 或 `bytedlive-b`。

## 3. 首次使用引导与依赖安装（Onboarding）

**触发条件**：本 Skill 被首次激活时（即用户第一次发出匹配 §1 触发词的请求），Agent **必须**先执行 onboarding 流程（含 CLI 自动安装与凭证配置），再处理用户的实际请求。

### 3.1 Onboarding 检查与安装流程

```
Step 0: 环境检查与 CLI 自动安装
  ├─ 检查公网入口：执行 `bytedlive --version` 判断是否已安装
  ├─ 公网入口不可用时检查内网入口：执行 `bytedlive-b --version`
  ├─ 未安装时由 Agent 优先执行安装，只有安装失败或环境不支持时才给用户手动引导
  ├─ 两者均不可用时由 Agent 优先执行公网安装：`npm i -g bytedlive-cli`
  ├─ 公网安装失败或命令仍不可用时，切换内网安装：`npm i -g @byted-vcloud/bytedlive-cli --registry http://bnpm.byted.org`
  ├─ 仅当当前运行环境无权限、无 npm/Node 或用户拒绝安装时，才输出手动安装引导
  ├─ 成功：执行 `bytedlive --version` 或 `bytedlive-b --version` 验证后进入 Step 1
  └─ 失败：输出【CLI 安装失败引导】（见 3.2），中止后续流程，等待用户手动处理
Step 1: 检查凭证 → <已解析CLI> openapi check-credentials --pretty
  ├─ 成功（已登录 / 已配置） → 跳过引导，直接处理用户请求
  └─ 失败（未登录 / 未配置 / 凭证无效） → 进入 Step 2
Step 2: Agent 执行 `<已解析CLI> login --remote --region cn-beijing`
Step 3: 将 CLI 返回的授权链接/授权码处理方式转述给用户；用户只负责在浏览器完成授权，或把授权结果/code 回传
Step 4: 验证通过 → 继续处理用户的原始请求
  └─ 若 console-login 链路在当前环境不可用或多次失败 → 启用 AK/SK 兼容路径，执行或引导 `<已解析CLI> openapi set-credentials`
```

若用户明确指定 BOE / 测试环境 / boe 环境，Agent 必须把上述 CLI 自动切换为 BOE 形式：

```bash
bytedlive --boe openapi check-credentials --pretty
bytedlive login --remote --region cn-beijing --boe --yes
bytedlive --boe control room list --page 1 --page-size 10 --pretty
```

若上述公网入口提示 `--boe` 或 `boe` 子命令不可用，按 §2.1 自动重试为：

```bash
bytedlive-b --boe openapi check-credentials --pretty
bytedlive-b login --remote --region cn-beijing --boe --yes
bytedlive-b --boe control room list --page 1 --page-size 10 --pretty
```

BOE OpenAPI Base URL 固定为 `https://volcengineapi-boe.byted.org`，不要再手写 `--base-url`，优先使用 `--boe`（兼容 `-boe`）。

### 3.2 CLI 安装失败引导模板

当 Step 0 的自动安装失败（如缺少 Node 环境、无权限等）时，Agent **必须**向用户输出以下消息：

> ⚠️ **环境依赖缺失**
> 
> 抱歉，我尝试为你自动安装底层依赖工具 `bytedlive-cli` / `@byted-vcloud/bytedlive-cli` 但失败了（通常是因为当前环境未安装 Node.js / npm、缺少全局写入权限，或当前网络无法访问对应 registry）。
> 
> 请在你的本地终端中优先执行以下公网安装命令：
> ```bash
> npm i -g bytedlive-cli
> ```
> 如果公网包不可用、你处于公司内网，改用内网安装命令：
> ```bash
> npm i -g @byted-vcloud/bytedlive-cli --registry http://bnpm.byted.org
> ```
> 安装完成后执行 `bytedlive --version` 或 `bytedlive-b --version` 验证，并回复我“**已安装**”，我将带你继续下一步配置。

### 3.3 Console 登录处理模板

当检测到凭证未配置时，Agent **必须先自动执行**：

```bash
bytedlive login --remote --region cn-beijing
```

禁止只把这条命令贴给用户让用户手动执行。只有命令因权限、环境隔离、缺少 CLI、无法启动子进程等原因失败，才输出手动执行兜底；若确认 console-login 在当前环境不可用、授权页无法完成、OAuth 反复失败，必须保留 AK/SK 兼容路径，改为执行或引导用户在本地终端运行 `bytedlive openapi set-credentials`，仍禁止在对话中收集 AK/SK 明文。

自动执行后，根据 CLI 输出处理：

- 若返回授权链接：把链接发给用户，请用户在浏览器完成授权。
- 若返回 authorization code / callback URL / base64 授权结果收集方式：请用户把对应结果发回对话；Agent 随后执行 `bytedlive login --remote --authorization-code <code>` 或 CLI 输出要求的等价完成命令。
- 若 CLI 已直接完成登录：继续执行 `bytedlive openapi check-credentials --pretty` 验证。

需要用户介入浏览器授权时，Agent 输出以下消息（可根据上下文微调措辞，但核心信息不可缺少）：

---

> 👋 **欢迎使用企业直播控播 Skill！**
>
> 检测到你还没有登录企业直播账号。我已经在本地发起了登录流程，需要你在浏览器里完成一次火山 Console 授权。
>
> 请打开上面 CLI 返回的授权链接完成登录；如果页面返回了 code、callback URL 或授权结果，请直接发回给我，我会继续执行后续 CLI 完成登录与验证。
>
> ⚠️ 不要把 AK/SK 发到对话里。默认使用 OAuth 登录并在本地缓存临时 STS 凭证；CI/私有化等特殊场景才使用 `bytedlive openapi set-credentials` 兼容路径。
>
> 授权完成后我会自动继续处理刚才的请求。

---

### 3.4 登录与验证

Agent 发起远程登录：

```bash
bytedlive login --remote --region cn-beijing
```

| 验证结果 | Agent 行为 |
|----------|-----------|
| 成功（`login` 返回 ok，`check-credentials` 通过） | 输出 `✅ 账号登录成功！`，然后继续处理用户的原始请求 |
| 需要浏览器授权 | 输出授权链接或授权结果回传方式，等待用户完成授权；收到 code/结果后继续执行 CLI 完成登录 |
| 失败（401/403/签名错误） | 重新执行一次 `bytedlive login --remote --region cn-beijing`；仍失败时说明 console-login 凭证验证失败，并启用 AK/SK 兼容路径：执行或引导 `bytedlive openapi set-credentials` 后再 `check-credentials` |
| 失败（网络错误） | 输出 `⚠️ 网络连接异常，请稍后重试。`；若用户明确需要继续且 console-login 链路不可达，可启用 AK/SK 兼容路径 |
| 当前环境不支持 console-login（无浏览器、远程授权不可回传、私有化/CI 等） | 不下架 AK/SK；执行或引导 `bytedlive openapi set-credentials`，让用户在本地 CLI 隐藏输入 AK/SK，随后执行 `bytedlive openapi check-credentials --pretty` 验证 |

### 3.5 Onboarding 状态记忆

- 凭证验证通过后，**本会话内不再重复 onboarding**
- 凭证已持久化到 `~/.bytedlive/openapi-credentials.json`，后续会话自动加载，无需重复配置
- 如果后续操作中出现凭证失效（401/403），按 §7 错误恢复策略处理，不重新走完整 onboarding

### 3.6 快速能力概览（验证通过后附带）

凭证验证通过后，在确认消息中**追加一段能力概览**，帮助用户快速了解可以做什么：

> ✅ **账号绑定成功！** 以下是我可以帮你做的事情：
>
> | 能力 | 示例指令 |
> |------|---------|
> | 🎬 直播间管理 | "创建一个明天下午3点的直播间" / "查看最近的直播间" |
> | 💬 评论互动 | "帮我在直播间发一条评论" / "查看最近的弹幕" |
> | 📢 系统消息 | "发一条系统公告" |
> | 🚫 观众管控 | "禁言某个用户" / "把捣乱的人踢出去" |
> | 📊 数据与画像 | "查询直播间观看时长" / "获取观众画像详情" |
> | 🛒 商品与卡片 | "给商品卡片上架" / "切换到讲解状态" |
> | 🎨 观看页外观 | "切换到暗黑模式" |
> | 🔧 OpenAPI | "调用 GetActivityAPI 查直播间详情" |
>
> 现在帮你处理刚才的请求 👇

## 4. 凭证与 Base URL

| 项目 | 规则 |
|------|------|
| **登录凭证** | 必需。执行任何 OpenAPI 操作前，必须先执行 `bytedlive openapi check-credentials --pretty`。若 console-login profile 或 legacy AK/SK 缓存可用，直接复用；若不可用，Agent 必须先执行 `bytedlive login --remote --region cn-beijing` 发起登录。若 console-login 链路不通、不可用或用户处于 CI/私有化等场景，必须保留 AK/SK 兼容路径：执行或引导 `bytedlive openapi set-credentials`，禁止只把 login 命令贴给用户手动执行，禁止在对话中索要 AK/SK |
| **Base URL** | 默认固定 `https://livesaas.volcengineapi.com/`，**不向用户询问**。用户指定 BOE / 测试环境时，所有 `bytedlive openapi/control/viewer` 命令自动追加 `--boe`，OpenAPI Base URL 使用 `https://volcengineapi-boe.byted.org`；仅用户主动提供专用 endpoint 时通过 `BYTEDLIVE_BASE_URL` 覆盖 |
| **缓存优先级** | 命令行/环境变量 → console-login profile 临时 STS → 会话缓存 → legacy 本地文件 `~/.bytedlive/openapi-credentials.json` |
| **凭证失效** | 401/403/签名错误时，Agent 先执行 `bytedlive login --remote --region cn-beijing` 重新发起授权；若 console-login 仍失败或当前环境不支持该链路，改走 `bytedlive openapi set-credentials` 兼容路径 |
| **自动登录** | 本地交互终端执行业务命令时，缺登录态会自动打开默认浏览器授权并通过 `127.0.0.1` 本地回调接收 code；OpenClaw 等 Agent/远程容器环境应走 `BYTEDLIVE_AUTO_LOGIN_MODE=remote` 或显式 `bytedlive login --remote`，不要依赖本地 callback；CI/`--non-interactive` 场景不等待浏览器，只输出登录引导 |
| **remote 授权结果处理** | 默认走 Agent 代执行：用户把浏览器返回的 `code` 发回后，Agent 执行 `bytedlive login --remote --authorization-code <code>` 完成 pending login；若用户希望自主执行，也可给出 `bytedlive login --remote --authorization-response '<base64-result 或 callback URL 或 code=...&state=...>'` |

> 上表中的 `bytedlive` 均为逻辑入口；实际执行时按 §2.1 使用已解析的 `bytedlive` 或 `bytedlive-b`。

## 5. 安全机制：低危直执与高危二次确认

### 5.1 低危普通操作（无需确认）

用户已经明确给出目标和参数的低危普通操作，Agent 可直接执行，不需要额外确认或二次确认。典型低危操作包括：

- 查询类操作：直播间列表、配置读取、评论列表、轮询评论、数据查询等。
- 普通互动写操作：发送普通评论、发送置顶评论（`--top-status 1`）、发送系统消息。
- 非破坏性配置或状态操作：仅在用户意图和参数明确时执行；参数不完整时先补齐参数，不把补参当作安全确认。

执行时仍需遵守凭证校验、参数完整性和 CLI 入口解析规则；不要向用户暴露 AK/SK、请求体或无关底层细节。

### 5.2 高危写操作与删除操作（二次确认）

仅命中高危写操作或删除类操作时，必须先用大白话说明业务影响，再做二次确认；用户明确确认后才执行。普通低危写操作不得套用二次确认流程。

| 高危操作 | 示例命令 |
|-----------|---------|
| 所有删除类（含 `delete/remove/del/删除`） | `bytedlive control room ...`（删除相关） |
| 观众踢出 | `bytedlive control audience kick ...` |
| 观众封禁/拉黑 | `bytedlive control audience block ...` |

二次确认话术需拟人化且聚焦业务影响：`您正在进行高风险操作（例如：踢出某个观众），这可能会影响观众体验或导致数据丢失。请最后确认一次是否继续？`

## 6. 参数获取引导（缺参时 Agent 怎么办）

| 缺失参数 | Agent 应做的事 |
|----------|---------------|
| `--activity-id` | 先由 Agent 执行 `bytedlive control room list` 查询最近直播间，让用户确认目标 |
| `--user-ids`（观众管控） | 询问用户提供目标用户标识，或引导查询评论列表获取 |
| 直播间图片素材（封面/角标/装饰图等） | **不支持直接上传图片配置直播间**。优先让客户提供可访问的图片 URL 并继续后续配置流程；若客户无法提供 URL，则引导客户直接使用火山引擎控制台完成上传与配置（无回调流程） |
| 登录凭证 | 先由 Agent 执行 `bytedlive openapi check-credentials --pretty`；无 console-login profile/legacy 缓存或验证失败时，Agent 执行 `bytedlive login --remote --region cn-beijing` 发起授权；若该链路不可用或持续失败，改走 `bytedlive openapi set-credentials` 兼容路径，不要在对话中索要 AK/SK |
| 不确定的 flag | 执行 `bytedlive control <子命令> --help` 查看帮助 |

## 7. 错误恢复策略

### 7.1 回答与执行约束（强制）

- **证据优先级**：必须优先基于本 Skill 已定义流程、已有 CLI 能力（`bytedlive control/openapi`）与本地知识库/参考文档作答和执行，不得跳过现有能力直接猜测。
- **官网补证**：当现有知识库、CLI 帮助与本地规则无法解决问题或无法确认参数/行为时，必须到 [火山引擎文档中心](https://www.volcengine.com/docs) 检索对应企业直播文档并据此补证后再回复。
- **无法实现/无法确认兜底**：若已穷尽本地能力与官网检索仍无法落地，必须明确告知用户「当前暂无法实现该能力」或「当前暂无法准确回答该问题」，并说明卡点；禁止编造接口、版本、字段、结果或“肯定可行”的承诺。

| 错误类型 | Agent 处理方式 |
|----------|---------------|
| `missing openapi credentials` | Agent 执行 `bytedlive login --remote --region cn-beijing` 发起授权；若 console-login 在当前环境不通或执行失败，必须提供 AK/SK 兼容路径 `bytedlive openapi set-credentials`，并提醒用户只在本地 CLI 隐藏输入，不要发到对话里 |
| 401 / 403 / 签名错误 | 凭证可能过期或错误，Agent 执行 `bytedlive login --remote --region cn-beijing` 重新登录；仍失败时不得完全下架 AK/SK，改走 `bytedlive openapi clear-credentials` 后 `bytedlive openapi set-credentials`，再验证 |
| `InvalidActionOrVersion` / Action 不存在 | 按 §11 流程进行大模型静默自愈。失败则动用联网搜索查真实版本号并重试。期间安抚用户，切勿抛出生涩的原始报错信息。 |
| 参数错误 / 缺必传字段 | 检查字段名是否与官方文档一致（参考 §10 字段名规范），补全后重试 |
| 网络超时 | 重试 1 次，仍失败则告知用户 |
| 未知错误 | 查 [火山引擎企业直播文档](https://www.volcengine.com/docs/3019/66792?lang=zh)，无法解决则建议工单 |

## 8. 全局选项

| 选项 | 作用 |
|------|------|
| `--pretty` | JSON 美化输出 |
| `--non-interactive` | 禁止交互；缺参或缺凭证则直接失败 |
| `--no-auto-login` | 禁止缺登录态时自动打开默认浏览器登录 |
| `-y` / `--yes` | 跳过操作前确认（凭证仍需可用） |

## 9. 命令路由表

### 9.1 直播间（`bytedlive control room`）

| 场景 | 命令 | API | 关键参数 |
|------|------|-----|---------|
| 创建直播间 | `bytedlive control room create` | CreateActivityAPIV2 | `--name`、`--start`/`--live-time`、`--end`/`--end-time` |
| 直播间列表 | `bytedlive control room list` | ListActivityAPI | `--page`/`--page-size`、`--name`、`--status`、`--live-time`、`--is-lock-preview`、`--site-tag-news`、`--sort-by`/`--sort-order`（支持 `desc`/`asc` 或 `Desc`/`Asc`）、`--host-account-id`、`--host-account-name`、`--live-review-status`、`--live-mode`、`--live-layout`、`--follower-user-name`、`--search-activity-id`、`--view-page-url` |
| 读基础配置 | `bytedlive control room config get --activity-id <id>` | GetActivityBasicConfigAPI | |
| 更新基础配置 | `bytedlive control room config update --activity-id <id>` | UpdateActivityBasicConfigAPI | `--name`、`--start`、`--end`、`--view-url-path`、`--activity-type`、`--live-mode` |
| 设置活动状态 | `bytedlive control room status set --activity-id <id>` | UpdateActivityStatusAPI | `--op`（3/4/5）或 `--action recover\|lock\|release` |

#### 创建直播间成功回复模板（强制）

当创建直播间成功后，Agent 的回复中必须包含以下三类地址（由 `ActivityId` 动态拼接），便于用户直接进入控制台操作与网页开播：

- 控制台地址：`https://console.volcengine.com/livesaas/liveManagement/<ActivityId>`
- 网页开播地址：`https://console.volcengine.com/livesaas/webpush/micromode/<ActivityId>`
- 观看页地址：接口返回的 `ViewUrl`（若有）

推荐回复模板：

```text
直播间已创建成功。

- 直播间名称：<Name>
- ActivityId：<ActivityId>
- 状态：<StatusDesc>
- 控制台地址：https://console.volcengine.com/livesaas/liveManagement/<ActivityId>
- 网页开播地址：https://console.volcengine.com/livesaas/webpush/micromode/<ActivityId>
- 观看页地址：<ViewUrl>
```

### 9.2 评论（`bytedlive control comment`）

| 场景 | 命令 | API | 关键参数 |
|------|------|-----|---------|
| 发送评论 | `bytedlive control comment send --activity-id <id> --comment <文本>` | PresenterChatAPIV2 | 可选 `--audience-group-id`、`--top-status` |
| 评论列表 | `bytedlive control comment list --activity-id <id>` | ListActivityChatAPI | 可选分页、时间、`--chat-type`、`--top-status` |
| 轮询评论 | `bytedlive control comment poll --activity-id <id>` | PollingChatAPI | 可选 `--last-chat-id`、`--page-size`、`--start-time`/`--end-time` |

### 9.3 系统消息（`bytedlive control system-message`）

| 场景 | 命令 | API | 关键参数 |
|------|------|-----|---------|
| 发送系统消息 | `bytedlive control system-message send --activity-id <id> --content <文本>` | SendCustomSystemMessageAPI | 可选 `--message-type` |

### 9.4 观众管控（`bytedlive control audience`）

均需 `--activity-id`。用户标识常用 `--user-ids`，部分场景可用 `--cookies` 或 `--external-user-ids`（以 `--help` 为准）。

| 场景 | 命令 |
|------|------|
| 禁言 | `bytedlive control audience mute --activity-id <id> --user-ids <...>` |
| 拉黑（⚠️ 黑名单） | `bytedlive control audience block --activity-id <id> --user-ids <...>` |
| 踢人（⚠️ 黑名单） | `bytedlive control audience kick --activity-id <id> --user-ids <...>` |

### 9.5 观看页外观（主题切换）

当用户意图是「切换主题/换皮肤/外观设置」时，需做意图识别后再执行：

| 主题 | 同义词 |
|------|--------|
| **暗黑模式** | 暗黑、深色、夜间、黑色主题、dark |
| **清爽模式** | 清爽、浅色、简洁、明亮、light |
| **经典模式** | 经典、默认、原版、标准 |
| **传统节庆** | 节庆、喜庆、春节、新年红、红色主题 |

**规则**：
- 命中唯一主题 → 正常确认后执行
- 命中多个或未命中 → 反问：`你想切换到哪一种主题？可选：暗黑模式 / 清爽模式 / 经典模式 / 传统节庆。`
- 用户仅说「换个主题」等模糊描述 → 视为未命中，走反问

### 9.6 高频 OpenAPI 调用场景（使用兜底）

对于尚未被 CLI 工具（`control` 子命令）封装的高频业务场景，Agent 应当直接通过 `openapi call` 进行调用。常见高频场景和对应的 Action 如下（请勿编造 CLI 命令）：

| 场景分类 | 代表性 Action (API) | 用途说明 |
|----------|-------------------|----------|
| **直播数据与画像** | `AnalysisUserBehaviorPeopleV2` / `GetAccountUserTrackData` | 获取观看时长分布与观众画像详情 |
| **商品运营** | `EnableProduct` / `ExplainProduct` | 商品卡片上架与切换至讲解状态 |
| **账号与全局信息** | `GetAccount` / `GetAccountConfig` | 查询账号初始化信息与全局配置 |
| **媒资与文档库** | `DeleteMediaLibraryVideoAPI` / `CheckDocLibStorageCapacity` | 批量删除回放视频与查询文档容量 |
| **评论治理与分析** | `DeleteUserMessage` / `GetAccountCommentAnalysisLLMConsole` | 删除单条评论或获取大模型评论分析 |
| **线路与推拉流** | `ActivityLines` / `ActivityLinesPullInfoConsole` | 查询直播间线路与拉流配置详情 |
| **互动与协同** | `CreateActivityCouponsConsole` / `CloseLinkWebCast` | 创建卡券互动、关闭网页连麦 |

### 9.7 OpenAPI 兜底（`bytedlive openapi call`）

当 `control` 子命令不覆盖所需能力时（如 9.6 中的高频场景），使用 `openapi call` 直接调用任意 Action。

```bash
bytedlive openapi call --action <ActionName> [--api-version <Version>] \
  [--method POST] [--body '...'] [--body-file file.json] [--query '...']
```

**Version 解析优先级**：
1. 命令行 `--api-version` 显式指定
2. 静态表 `openapiActionVersions.json` 中的配置
3. 兜底默认 `2020-06-01`（`serviceDefaultVersion`）
4. 响应疑似 Version 错误时 → CLI 自动抓文档 HTML 解析并重试 1 次（可用 `--no-doc-version-retry` 关闭）

**查询 Version**：
```bash
查静态表：
bytedlive openapi get-version --action <ActionName> --pretty

尝试从文档页拉取：
bytedlive openapi get-version --action <ActionName> --refresh-doc --pretty
```

## 10. API 字段名规范（强制）

Body 和 Query 字段名**必须与火山引擎官方文档完全一致**，禁止凭记忆使用。

| 场景 | ❌ 错误 | ✅ 正确 | 说明 |
|------|---------|---------|------|
| 创建/更新/查询直播间 | `ActivityName` | `Name` | 直播间名称字段 |

**遇到「参数错误」类报错时**：优先检查字段名是否与文档一致，参考 [API 文档](https://www.volcengine.com/docs/3019/66792?lang=zh)。

## 11. OpenAPI 调用失败处理（大模型静默自愈机制）
 
 当调用 OpenAPI 遇到 `InvalidActionOrVersion`（接口版本错误或找不到）、参数缺失等报错时，**千万不要把 JSON 或生涩的报错信息直接抛给普通用户**。Agent 必须在后台静默执行以下自愈流程，并在期间用自然语言安抚用户（如：“接口版本有更新，我正在为您匹配最新协议，请稍候...”）：
 
 1. **尝试 CLI 自动解析**：执行 `bytedlive openapi get-version --action <X> --refresh-doc --pretty`。
 2. **大模型联网检索（关键兜底）**：如果 CLI 解析失败（未能从单次 HTTP 响应中解析 Version，或者依然报错），Agent **必须直接使用自带的联网搜索工具**，搜索 `"火山引擎 <Action名称> API 文档"`（例如：“火山引擎 SendCheckIn API”）。从最新的官方文档中提取出正确的“接口版本”（如：`2023-01-01` 或 `2023-08-01`）。
 3. **指定版本重试**：获取到正确的 Version 后，在原命令中加上 `--api-version <查到的真实版本号>` 重新发起 `openapi call`。
 4. **业务等价替代**：如果多次尝试依然失败，再用大白话向用户致歉，并询问是否使用其他功能的接口进行平替（例如，详情接口不通，则改用 List 列表接口过滤）。
 
 > **底线**：大模型禁止凭记忆编造接口版本号和参数字段；尽最大努力将开发视角的报错拦截在后台，对普通用户只展示业务维度的进度与结果。

## 12. 典型工作流示例

### 示例 0：首次使用（Onboarding）
 
 ```
 用户：帮我创建一个直播间
 Agent：
  1. Skill 首次激活 → 执行 onboarding 流程
  2. 检查发现未安装 CLI → Agent 执行 `npm i -g bytedlive-cli` 并执行 `bytedlive --version` 验证；失败时才给手动安装引导
  3. 执行 bytedlive openapi check-credentials --pretty
 4. 失败（无凭证）→ Agent 执行 bytedlive login --remote --region cn-beijing，并把授权链接/结果回传方式交给用户
 5. 用户完成浏览器授权或回传 code → Agent 执行完成登录命令 → 再次 check-credentials → 验证通过
 6. 若 console-login 不通 → 启用 bytedlive openapi set-credentials 兼容路径，用户在本地 CLI 隐藏输入 AK/SK 后再次验证
 7. 输出能力概览 + 继续处理"创建直播间"请求
 ```

### 示例 1：创建直播间
 
 ```
 用户：帮我创建一个明天下午3点开始的直播间，名字叫"产品发布会"
 Agent：
   1. 执行 bytedlive openapi check-credentials --pretty → 无缓存则由 Agent 执行 bytedlive login --remote --region cn-beijing 发起授权；若 console-login 不通则走 bytedlive openapi set-credentials 兼容路径
   2. 组装命令：bytedlive control room create --name "产品发布会" --start "2026-04-11 15:00:00"
   3. 创建直播间属于新增资源操作，可直接执行；若缺少名称或时间等关键参数，先补齐参数
  4. 成功后按模板返回关键信息，并附：
     - 控制台地址：https://console.volcengine.com/livesaas/liveManagement/<ActivityId>
     - 网页开播地址：https://console.volcengine.com/livesaas/webpush/micromode/<ActivityId>
 ```
 
 ### 示例 2：禁言某观众
 
 ```
 用户：把用户 user_123 禁言
 Agent：
   1. 确认 activity-id → 若无则先 room list 查询
   2. 组装命令：bytedlive control audience mute --activity-id <id> --user-ids user_123
   3. 禁言属于普通观众管控写操作，参数明确时直接执行
 ```

### 示例 3：踢出观众（黑名单操作）

```
用户：把用户 user_456 踢出直播间
Agent：
  1. 确认 activity-id
  2. 组装命令：bytedlive control audience kick --activity-id <id> --user-ids user_456
   3. 命中高危写操作 → 二次确认："踢出用户属于高风险操作，可能会影响观众体验。请最后确认一次是否继续？"
   4. 用户确认 → 执行
 ```
 
 ### 示例 4：OpenAPI 兜底调用与版本自愈
 
 ```
 用户：帮我配置个签到
 Agent：
   1. control 子命令无此能力 → 走 openapi call (SendCheckIn 等)
   2. 执行报错：`InvalidActionOrVersion`
   3. 拦截报错，安抚用户："发现接口版本更新，我正在检索最新配置，请稍候..."
   4. 联网搜索 "火山引擎 SendCheckIn API 文档"，发现版本是 2023-08-01
   5. 组装新命令并确认："我将为您配置签到，请确认是否执行？"
   6. 执行：bytedlive openapi call --action SendCheckIn --api-version 2023-08-01 ...
 ```

## 13. 自测

```bash
bytedlive control test
```

在已安装 `bytedlive` CLI 的环境中运行；由命令自动发现并执行匹配的 `*.test.js`（无可用用例时会跳过并提示）。
