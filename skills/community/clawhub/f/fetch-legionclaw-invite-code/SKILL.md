---
name: fetch-legionclaw-invite-code
description: >-
  Fetches Tongfudun LegionClaw usage-permission invite codes by POSTing JSON
  with userId set to the agentid (second colon-delimited segment) parsed from
  a LegionClaw session handle. Obtain the session handle from runtime injection
  or by querying the LegionClaw host or model; do not default to asking the user
  to paste it. Handles long session-handle forms (e.g. agent, agentid,
  openai-user, user suffix). Supports multiple codes per request by calling the
  API repeatedly; returns all codes in chat by default (files only if user explicitly
  asks). Designed for LegionClaw-hosted
  agents. Use when the user needs Tongfudun LegionClaw access invite codes, asks for
  fetch-legionclaw-invite-code, or says things like 邀请码, 要邀请码, 获取邀请码,
  申请邀请码, 生成邀请码, 给我邀请码, 帮我生成邀请码, 发我邀请码, 多个邀请码,
  LegionClaw 邀请码, 通付盾邀请码, or LegionClaw 使用权限.
disable-model-invocation: false
---

# 通付盾 LegionClaw 权限邀请码

## 目标

调用固定接口，获取**通付盾 LegionClaw 使用权限**对应的邀请码。传入 JSON **`{"userId":"..."}`**。其中字段 **`userId`** 取值为 LegionClaw **会话标识串**（规范格式见「[从会话标识解析 agentid](#从会话标识解析-agentid)」）按 `:` 拆分后的**第二段 `agentid`**（不要把第二段误称为「会话 id」——整串是会话相关标识，第二段是代理 id）。解析规则见下文。成功后在遵守保密与合规的前提下，**按固定模板**在对话正文中向用户展示邀请码（见「[回复用户的格式](#回复用户的格式)」）。

**数量**：接口**不限制**「每个用户只能领一个」；用户要 **N 个**邀请码时，用同一 **`userId`（agentid）** **连续调用接口 N 次**（每次一次 `POST`），将各次成功得到的 `data.inviteCode` **汇总后一次性**回复给用户。未指定数量时默认 **1 次**。

**交付方式（默认）**：在对话消息中输出 Markdown 文本，便于用户复制；**默认不要**写入本地/临时文件，**不要**以附件、下载链接或「请打开某文件查看」等形式交付邀请码。**例外**：仅当用户**明确要求**需要文件（如导出 txt、保存到文件、发附件等）时，再生成并交付文件；仍可在消息正文中同时给出便于复制的邀请码。

**常见触发说法**（不限于此）：申请邀请码、生成邀请码、给我邀请码、帮我生成邀请码、发我邀请码、要邀请码、获取/领取邀请码、要 3 个邀请码、多个邀请码、LegionClaw 或通付盾邀请码等。

## LegionClaw 运行约定

本技能面向 **在 LegionClaw 内执行的 Agent**：邀请码与当前任务所绑定的 **agentid**（会话标识第二段）对应，用于开通/校验 **LegionClaw 侧权限**，不是通用「在请求体中随意填写 **`userId`**」的开放接口封装。

- **会话形态**：语义为 `agent:<agentid>:<渠道>:<用户 id>`。**渠道为空时**为三段 `agent:<agentid>:<用户 id>`（**无** `::`）；**有渠道时**为四段起。拆段后 **请求体字段 `userId` 的值仅允许为第 2 段 `agentid`**（由会话串解析得到）；三段形态下**勿**把第 3 段（用户 id）误当 `agentid`。更短的历史形态仍适用「第二段为 agentid」。
- **成功判定**：LegionClaw 侧必须以响应 JSON 的 **`code == "000000"`** 且 **`data.inviteCode` 非空** 为准；**HTTP 状态码为 2xx 不代表业务成功**（仍可能 `code != "000000"`）。
- **执行位置**：`curl` 或等价请求须在 **LegionClaw 下发任务时的运行环境**中发起（该环境需能访问通付盾接口域名）；网络类报错对用户说明「当前运行环境无法访问服务器」即可，**不要**在对外文案中写具体域名、IP、端口（见下文安全要求）。
- **对用户输出**：正常成功路径在消息正文中输出问候语 + 邀请码（单个或多个）；**勿**默认回显完整会话标识串或内部 `agentid`，除非用户明确要求排查；**默认勿**生成或引用文件，**除非**用户明确要求需要文件。

## 接口

- **URL**: `https://legion.tongfudun.com/userInvite/claimIndustryInviteCode`
- **方法**: `POST`
- **Content-Type**: `application/json`
- **请求头**: `Web-RedPackage: webRedPackage`
- **请求体**:

```json
{ "userId": "<agentid，与下表第二列相同>" }
```

### 成功响应体（HTTP 2xx）

响应为 JSON，按以下结构解析：

| 字段 | 含义 |
|------|------|
| `code` | 业务状态码；成功体中为字符串 **`"000000"`** 表示成功；其他值或**数值型** `code`（如 `404`）表示失败（见下文错误体） |
| `message` | 业务提示信息（失败时优先用于友好提示；部分错误体使用 `msg` 见下文） |
| `data.inviteCode` | 邀请码 |
| `data.userName` | 用户名（用于问候语） |

示例：

```json
{
  "code": "000000",
  "message": "成功",
  "data": {
    "inviteCode": "INV-QP-TEST04",
    "userName": "18762097213",
    "expireTime": "2027-12-31 23:59:59",
    "id": 4,
    "industryType": 1
  }
}
```

### 回复用户的格式

在响应 JSON 中 **`code == "000000"`** 且 **`data.inviteCode` 非空**时，在**同一条用户可见消息**中输出问候语与邀请码；**默认不要**写文件、不要附 `.txt`/`.md` 等路径（用户**明确要求**要文件时除外）。

**邀请码片段写法**（单个与多个共用）：`**` + 反引号 + `inviteCode` 的值 + 反引号 + `**`（粗体等宽，便于拖选复制）。

#### 单个邀请码

结构为：`{userName}您好，邀请码已获取，请妥善保管：` + 上述邀请码片段。

- 将**最后一次成功响应**中的 **`data.userName`** 原样填入称呼（勿改写）；将 **`data.inviteCode`** 作为邀请码。若多次调用且 `userName` 一致，用最后一次即可。
- **完整示例**（勿再附加整段原始 JSON，除非用户明确要求调试信息）：

```markdown
张三您好，邀请码已获取，请妥善保管：**`A12345678`**
```

- 若 **`data.userName` 缺失或为空字符串**：以「您好」开头，即：`您好，邀请码已获取，请妥善保管：` 后接邀请码片段。

#### 多个邀请码

用户明确要求数量 **N**（或「多个」「再来几个」等且可推断为 **N > 1**）时：对同一 `userId` **调用接口 N 次**；每次成功则收集一个 `data.inviteCode`。全部成功调用结束后**一条消息**汇总回复：

1. 首行问候（与单个相同，用最后一次成功的 `data.userName`，缺失则用「您好」）。
2. 说明共 **N** 个（实际成功个数若少于 N，按实际成功数说明，并单独说明失败次数与原因，仍遵守失败口径）。
3. **每个邀请码独占一行**，格式为：`1. **` + 邀请码 + `**`（序号从 1 递增；每行仅一个码，便于逐条复制）。

**多码示例**（3 个）：

```markdown
张三您好，邀请码已获取，共 3 个，请妥善保管：

1. **`INV-001`**
2. **`INV-002`**
3. **`INV-003`**
```

- 若 **`code` 不为字符串 `"000000"`**（含数值型 `code`）、或 **`data.inviteCode` 缺失/为空**：该次调用按下文失败口径处理；若批量请求中部分失败，已成功码仍按上表格式列出，并对失败次数给出简短说明（不暴露 URL/IP/端口）。

### 失败返回口径（统一规则）

出现以下任一情况时，按以下优先级返回（**对用户不要暴露 URL/IP/端口**，见文末安全要求）：

1. **无权限等价形态（固定结构）**：若响应 JSON 同时满足：
   - 顶层 **`code` 为数值 `404`**，或可规范为 `404` 的字符串（如 `"404"`）；
   - **`data` 为 `null`**；
   - 存在 **`msg`** 字段且 **`msg` 为非空字符串**（例如 `Unexpected error occurred`）；  
   则**一律按「无权限」判定**，**不要**把 `msg` 里的英文技术短句当作对外结论的唯一依据。对用户输出与「无权限」**同一类**友好说明（可与下方示例同向，如「当前账号暂无操作权限，请联系管理员处理」或「暂无领取邀请码权限，请联系管理员」）。

2. 若响应中存在非空 **`message`** 字段，且**未命中**上一条：基于 `message` 原意做简短、友好的用户提示（可适度润色，但不得改变事实含义）。

3. 若**未命中**第 1 条，且存在非空 **`msg`** 而无可用 **`message`**：可基于 `msg` 原意做简短友好提示（不改变含义）。

4. 若无可用 **`message`** 与 **`msg`**（或二者均无法用于提示）：返回固定回复 `获取邀请码失败，请联系管理员。`

适用场景包括但不限于：

- 返回值格式错误（例如非 JSON、JSON 解析失败、缺少关键字段）
- `code` 不为 `"000000"` 的业务失败（含字符串错误码与数值型 `code`）
- `code == "000000"` 但 `data.inviteCode` 缺失、为空或不可用

错误返回示例（`message` 字段）：

```json
{
  "code": "500",
  "message": "无权限",
  "data": null
}
```

**无权限等价形态**示例（**按上条第 1 款处理，等同无权限**）：

```json
{
  "code": 404,
  "msg": "Unexpected error occurred",
  "crypto": false,
  "data": null
}
```

友好化示例（仅示例，不限此模板）：

- 原始 `message`：`无权限`
- 对用户提示：`当前账号暂无操作权限，请联系管理员处理。`
- 命中 **404 + `msg` + `data:null`** 时：优先采用与上句**同向**的权限类说明，**避免**仅以 `Unexpected error occurred` 作为最终话术。

## 获取会话标识串

**不要依赖用户手动粘贴整串会话标识**作为默认流程。

1. **优先**：使用运行时已注入的「当前会话标识」或等价字段（环境变量、LegionClaw 任务/会话上下文字段等；名称以实际平台为准，例如 `OPENCLAW_SESSION_ID`）。
2. **主路径**：若上下文中没有该串，**通过 LegionClaw 宿主侧能力获取**——例如调用 LegionClaw 提供的会话/元数据查询接口，或**与当前 LegionClaw 大模型（宿主）交互**，让其返回**当前会话标识串**（完整 `agent:...`）。**不要**把「请用户手动粘贴整串会话标识」作为默认或首选步骤。
3. **例外**：仅当用户**主动**提供 **agentid** 或与后端一致的 `userId` 值时，校验非空后可直接作为请求体 `userId`（不要求 `agent:` 前缀）；这不替代从 LegionClaw 自动取会话标识的常规流程。

## 从会话标识解析 agentid

LegionClaw **会话标识串**的语义为：

`agent:<agentid>:<渠道>:<用户 id>`

**渠道省略（为空）时**，实际传输格式为**三段**（**不会**用 `::` 占位），第三段**直接**是用户 id：

`agent:<agentid>:<用户 id>`

**有渠道时**为**四段**（第三段为渠道名，第四段为用户 id），例如：

`agent:<agentid>:openai-user:<用户 id>`

按英文冒号 `:` 拆段后：

| 形态 | 段数（典型） | 第 1 段 | 第 2 段 **`agentid`（= `userId`）** | 第 3 段 | 第 4 段 |
|------|-------------|---------|-----------------------------------|---------|---------|
| 有渠道 | 4 | `agent` | **`agentid`**，只取此段 | 渠道 | 用户 id |
| 无渠道 | 3 | `agent` | **`agentid`**，只取此段 | 用户 id（**不是**渠道占位） | — |

**与旧规则一致**：无论三段或四段，**`agentid` 一律为拆段后的第 2 段**；不要把第 3 段（无渠道时的用户 id）误当 `agentid`。

**典型示例**（有渠道，四段）：

- 整串：`agent:fe535f475db6471d81cf0a1fcd5566bd1684487565205:openai-user:703f56dd37f84fa682266a8471f26984`
- **`agentid`（= 请求体 `userId`）**：`fe535f475db6471d81cf0a1fcd5566bd1684487565205`

**渠道为空**（三段，**无双冒号**）：

- 整串：`agent:fe535f475db6471d81cf0a1fcd5566bd1684487565205:703f56dd37f84fa682266a8471f26984`
- **`agentid`（= 请求体 `userId`）**：`fe535f475db6471d81cf0a1fcd5566bd1684487565205`

**解析规则**：将整串按 `:` 拆分；若第一段为 `agent` 且**至少两段**（`NF >= 2`）且第二段非空，则 **`agentid` = 第二段**，请求体里 **`userId` 字段填该 agentid 字符串**（JSON 中须为 **`userId`**，大小写与后端一致）。否则视为无效格式，不要猜测；应**重新按「[获取会话标识串](#获取会话标识串)」**从 LegionClaw 侧取得合法串后再解析。若用户主动提供了可与 `userId` 同用的 **agentid** 值，校验非空后可直接用作请求体（不再要求 `agent:` 前缀）。

**更多示例**:

| 会话标识串（整串） | agentid（= 请求体 `userId`） |
|-------------------|------------------------------|
| `agent:fe535f475db6471d81cf0a1fcd5566bd1684487565205:openai-user:703f56dd37f84fa682266a8471f26984` | `fe535f475db6471d81cf0a1fcd5566bd1684487565205` |
| `agent:fe535f475db6471d81cf0a1fcd5566bd1684487565205:703f56dd37f84fa682266a8471f26984` | `fe535f475db6471d81cf0a1fcd5566bd1684487565205` |
| `agent:test_001:main` | `test_001` |
| `agent:alice:worker` | `alice` |

## 执行步骤

1. 按「[获取会话标识串](#获取会话标识串)」取得整串；若用户主动提供了 **agentid** 或已与后端约定一致的 **`userId` 取值**（即同一串 agentid），可直接采用。再按上文规则解析出 **agentid**，作为 JSON 里的 **`userId`** 发送。
2. 确定调用次数 **`COUNT`**：用户未说明数量时为 **1**；说明要 **N 个**（或等价表述）时为 **N**（`N` 为正整数；若表述含糊，按用户意图取合理正整数，必要时可确认一次）。
3. 对 `i = 1 .. COUNT`，各执行一次下方 `curl`（同一 `AGENTID`）。单次 `curl` 示例（将 `AGENTID` 替换为解析结果；若含 `"` 或 `\` 等字符，需先做 JSON 字符串转义）：

```bash
curl -sS -X POST "https://legion.tongfudun.com/userInvite/claimIndustryInviteCode" \
  -H "Content-Type: application/json" \
  -H "Web-RedPackage: webRedPackage" \
  -d "{\"userId\":\"${AGENTID}\"}"
```

可用一行从环境变量中的会话标识串解析 **agentid**（示例变量名 `OPENCLAW_SESSION_ID`，以实际运行时提供的变量名为准；若变量名不同，以从 LegionClaw 取到的整串为准）：

```bash
AGENTID=$(echo "${OPENCLAW_SESSION_ID}" | awk -F: '$1=="agent" && NF>=2 && length($2)>0 {print $2; exit}')
```

4. 根据**每一次**调用的 HTTP 与业务结果处理：
   - **HTTP 非 2xx**：不要向用户回显原始 URL；用简短说明（如无法访问服务器、服务暂时不可用），并按「[失败返回口径（统一规则）](#失败返回口径统一规则)」在无可用 `message`/`msg` 时使用固定文案。
   - **HTTP 2xx 且 body 为 JSON**：先判断是否命中 **404 + `msg` + `data:null`** 形态（见「[失败返回口径（统一规则）](#失败返回口径统一规则)」）；命中则按**无权限等价**输出。否则：若 **`code` 为字符串 `"000000"`** 且 **`data.inviteCode` 非空**，记入成功列表；否则按失败口径记录该次结果。
   - 单次失败时**继续**后续次数（除非用户明确要求「一个失败就停止」）。
5. 全部 **`COUNT`** 次调用结束后：若仅 1 个成功码，按「[单个邀请码](#单个邀请码)」回复；若多个成功码，按「[多个邀请码](#多个邀请码)」在**一条消息**中汇总输出。**默认**不把结果写入文件或作为附件交付；用户**明确要求**要文件时再生成。

## 错误处理

- **连接失败 / 超时**：提示检查**当前 LegionClaw 运行环境**到**服务器**的网络与防火墙（不要在用户可见报错中暴露具体 IP、端口或完整请求 URL）。
- **会话标识格式不对**：不要先让用户粘贴核对；应再次从 LegionClaw 运行时或宿主大模型侧获取会话标识串，确认拆段后第一段为 `agent`、第二段非空。若用户主动提供的 **agentid** / `userId` 仍无效，再说明语义格式为 `agent:<agentid>:<渠道>:<用户 id>`；**渠道为空时线上为三段** `agent:<agentid>:<用户 id>`（**无** `::`），**不要**把第 3 段用户 id 当成 `agentid`。
- **400/422**：对照后端要求检查请求体 `userId`（实为 agentid）是否为空或含非法字符。
- **返回值格式错误、业务失败或无邀请码**：按「[失败返回口径（统一规则）](#失败返回口径统一规则)」处理（含 **404 + `msg` + `data:null` 按无权限等价**、`message`/`msg` 友好化、固定文案）。

通用安全输出要求：

- 任何服务报错场景下，用户可见文案中**不要出现具体 IP 地址、端口或完整请求 URL**；统一使用「服务器」等泛化称呼。

## 变更接口时

若 URL、字段名、成功响应 JSON 结构或会话标识格式变更，请同步更新本文件，避免 agent 与真实服务不一致。
