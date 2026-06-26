---

## name: anyshare-mcp-skills
description: "AnyShare 智能知识管理技能。支持：搜索文件、上传/下载文件、分享链接读取、全文写作（生成大纲→确认→写正文）。触发词：AnyShare、asmcp、文档库、文件管理、知识库、anyshare.aishu.cn 分享链接。"
homepage: "[https://anyshare.aishu.cn](https://anyshare.aishu.cn)"
metadata: '{"openclaw":{"category":"productivity","emoji":"📁","requires":{"bins":["mcporter"]},"openclawSkillsEntryFile":"openclaw.skill-entry.json"}}'

# AnyShare MCP 技能

> **首次使用本技能时，按本文件「首次配置」章节执行。**

---

## ⚠️ 执行前必读

### 强制前置阅读（按需必读，否则跳过）


| 操作 | 必须先读 | 为何 |
| --- | --- | --- |
| 首次使用本技能 | **本 SKILL.md** → **「首次配置」** | 配置 MCP 服务地址 + 获取 Token；含步骤、用户确认话术 |
| 调用任何业务工具（file_search / upload / download 等）前 | **本 SKILL.md** → **「本技能工具与 mcporter 调用」**及对应场景步骤 | 参数格式（key=value）、固定字段、禁止传参 |
| 解析分享链接 | **本 SKILL.md** → **「本技能工具与 mcporter 调用」**→ `sharedlink_parse` 与 **「📎 分享链接（从 URL 到 docid）」** | **`link_id`**、**`item.id`**、顶层 **`id`**（见 C7） |
| **进入场景四（全文写作）前** | **本 SKILL.md** → 场景四 | 必须先获取 docid，否则禁止调用 smart_assistant |
| 排障 / 401 / 认证失败 | **[references/troubleshooting.md](references/troubleshooting.md)** | 错误码含义、常见现象与处理方式 |


### 硬卡点表


| # | 规则 | 关联场景 |
| --- | --- | --- |
| C1 | 搜索文件**只用 `file_search`**，禁止 RAG 类工具或目录树展开 | 场景一 |
| C2 | 展示搜索/列目录结果前，**必须先调 `file_convert_path` 再输出**（禁止跳过） | 场景一、[分享链接](#分享链接从-url-到-docid) |
| C3 | 上传/下载前，**必须用户明确回复"是"确认 docid**，禁止代选 | 场景二、场景三 |
| **C4** | **大纲未确认前禁止调用 `__大纲写作__1`**（大纲门闩） | 场景四 |
| **C5** | `source_ranges[].id` **必须传 id**（docid 最后一段），**禁止传完整 docid** | 场景四 |
| **C6** | 用 **`sharedlink_parse(link_id)`** 解析分享链；**`link_id`** 从用户 URL 中 **`/link/`** 路径段之后**原样提取** | [分享链接](#分享链接从-url-到-docid) |
| **C7** | **`docid`** = 响应 **`item.id`**（`gns://…`）；顶层 **`id`** 为分享链自身 id，**不等于** `item.id` | [分享链接](#分享链接从-url-到-docid) |
| **C8** | **进入全文写作前**须已定位目标文档：**至少掌握 docid（`gns://…`）或能唯一推出 `source_ranges[].id`（docid 最后一段）**。尚无则须先 **`file_search`** / [分享链接](#分享链接从-url-到-docid) / 用户提供 **docid** 等，禁止无文档锚点即调用 `smart_assistant` 或对话内代写 | 场景四 |
| **C9** | **在场原则**：持有 docid 后，必须使用 AnyShare 工具链，**禁止下载到本地用外部工具处理**（场景三用户明确要求下载除外） | 所有含 docid 的场景 |
| **C10** | **全文写作**：取得 id 后**必须直接调用 smart_assistant**，禁止先下载再写 | 场景四 |
| **C11** | **禁止**调用 **`file_upload`**（即使 `mcporter list asmcp` 仍列出该工具也不得使用）。上传**仅**允许 **`file_osbeginupload` → 按返回的 `authrequest` 对对象存储 HTTP PUT 文件体 → `file_osendupload`**；**PUT 未成功则禁止调用 `file_osendupload`** | 场景二 |


---

## 🔄 完整执行流程

> **分支优先级**：用户消息里若出现 **`https://…/link/…`**（或文档域下等价分享 URL），**先走「分享链接」分支**，再判断书写类、搜索等；避免把「带链接 + 让写稿」误判为纯全文写作而跳过解析。

```
用户输入
  │
  ▼
① 首次使用？── 是 ──→ 执行「首次配置」章节
  │                   → 向用户汇报 asmcp.url + 连通性
  │                   → 确认是否为**本企业**正式端点
  否
  ▼
② 凭证检查（自动）── headers.Authorization 未设置或 token 失效 ──→ **提示用户重新配置凭证**（按 **「首次配置」Step 4 获取 Token → 写入 headers → 重启 daemon）──→ 重试至可用
  │                                           │
  │ 通过 ◀────────────────────────────────────┘
  ▼
③ 意图识别
  │
  ├─ 含 `/link/` 的分享 URL？── 是 ──→ 「📎 分享链接（从 URL 到 docid）」：`sharedlink_parse` → docid / id
  │
  ├─ 书写类诉求？（生成/撰写/改写/续写/润色/文章/报告/文案/大纲/材料）── 是 ──→ 确认全文写作？
  │                                                                         │
  │                                                    是 ◀─────────────────┘
  │                                                    ▼
  │                                              ⚠️ C8 强制预检：
  │                                              "是否已掌握 docid 及 source_ranges 所用 id？"
  │                                              否 ──→ 场景一（关键词搜索）获取 docid
  │                                              │        或「分享链接（从 URL 到 docid）」流程获取 docid
  │                                              │        获取后返回此节点重新判断
  │                                              是
  │                                              ▼
  │                                              场景四：全文写作
  │                                              ① docid/id → ② 大纲 → ③ 确认 → ④ 正文
  │
  │                                              否 ──→ 非书写类：按场景一～三分流，或结束本技能（若本句仍含 `/link/`，应先满足上行分享链接分支）
  │
  ├─ 搜索 / 查看文件 ──→ 场景一
  │
  ├─ 上传文件 ──→ 场景二
  │
  └─ 下载文件 ──→ 场景三
```

## 🚀 首次配置

> **用户首次使用本技能时，Agent 必须直接执行以下步骤，不要先问用户"要不要配置"。**

### 术语说明

| 术语 | 含义 |
|------|------|
| **文档域** | 你访问 AnyShare 的站点域名（如 `xxx.aishu.cn` 或企业自有域名） |
| **MCP 服务地址** | MCP 网关的完整 URL，格式如 `https://<文档域>/mcp`（路径以贵司运维为准） |
| **MCP 授权凭证** | AnyShare 用户设置中的访问令牌，用于身份认证 |

### Step 1: 配置 MCP 服务地址

**1.1 读取或创建 mcporter 配置**

```bash
mkdir -p ~/.mcporter
cat ~/.mcporter/mcporter.json 2>/dev/null || echo '{"mcpServers":{}}'
```

**1.2 写入 asmcp 配置**

将以下内容合并到 `~/.mcporter/mcporter.json` 的 `mcpServers` 中（勿删除其他 server）。`<token>` 为占位符，Step 4 中替换为实际令牌：

```json
"asmcp": {
  "enabled": true,
  "url": "https://anyshare.aishu.cn/asmcp",
  "transportType": "streamable-http",
  "headers": {
    "Authorization": "Bearer <token>"
  }
}
```

**1.3 验证注册**

```bash
mcporter list
```

应能看到 `asmcp`。若看不到，执行：

```bash
mcporter daemon restart
mcporter list
```

### Step 2: 配置 OpenClaw 运行时超时（10 分钟）

> **目的**：让 `smart_assistant`（全文写作）等长耗时调用能等待 10 分钟。

读取 `~/.openclaw/openclaw.json`，确保存在 `skills.entries` 对象：

- 若 `entries["anyshare-mcp-skills"]` 已存在：在其下合并 `"env": {"MCPORTER_CALL_TIMEOUT": "600000"}`
- 若不存在：添加整段

```json
{
  "skills": {
    "entries": {
      "anyshare-mcp-skills": {
        "env": {
          "MCPORTER_CALL_TIMEOUT": "600000"
        }
      }
    }
  }
}
```

### Step 3: 向用户确认 MCP 服务地址

**Agent 必须向用户汇报以下内容**（无论连接成功与否）：

> 当前尝试使用的 **MCP 服务地址**为：`https://anyshare.aishu.cn/asmcp`
>
> **说明**：上方为线上默认地址。私有化部署的企业通常以贵司的**文档域**（访问 AnyShare 的站点域名）为主机前缀，再加 `/asmcp` 路径。具体地址请向贵司 IT/运维确认。
>
> 请确认这是否是**贵司的正式 MCP 服务地址**？如果不是，请提供贵司的正确 URL，我会更新配置并重新验证。

**用户回复后的处理：**

1. **用户确认是正式地址** → 进入 Step 4 获取 Token
2. **用户提供新地址** → 修改 `~/.mcporter/mcporter.json` 中的 `url`，执行 `mcporter daemon restart`，重新验证
3. **用户表示仅网络/认证问题** → 先排查，完成后进入 Step 4

### Step 4: 获取 Token 并写入配置

**4.1 向用户获取 Token（固定话术）**

> 请在 AnyShare Web端 **登录后**，点击右上角头像进入 **「MCP授权凭证」**；在此可**管理、赋值**凭证。复制令牌后，**在本对话中粘贴**。

**4.2 写入 headers.Authorization**

用户粘贴 token 后，Agent 将 `~/.mcporter/mcporter.json` 中 `asmcp.headers.Authorization` 更新为：

```json
"Authorization": "Bearer <用户粘贴的token>"
```

**4.3 重启 daemon 并验证**

```bash
mcporter daemon restart
mcporter call asmcp.doc_lib_owned
```

返回文档库列表即表示认证成功。若返回 **401 / 未授权**，提示用户重新获取 token 并重复 4.1 → 4.2 → 4.3。

**Token 过期时**：重复 4.1 → 4.2 → 4.3（更新配置文件中的 token 值后重启 daemon）。

---

## 📌 核心概念

### docid 与 id

| 字段 | 是什么 | 示例 |
| --- | --- | --- |
| **docid** | 完整路径，gns:// 开头 | `gns://E6D15886/.../2DDD46B195F24BCEB238DB59151CD15E` |
| **id** | docid 的最后一段 | `2DDD46B195F24BCEB238DB59151CD15E` |

**传参规则：**

| 工具 | 参数 | 传什么 |
| --- | --- | --- |
| `smart_assistant` | `source_ranges[].id` | **id**（最后一段） |
| `folder_sub_objects` | `id` | **完整 docid** |
| `file_osdownload` | `docid` | **完整 docid** |
| `file_osbeginupload` | `docid` | **完整 docid**（目标目录） |
| `file_osendupload` | `docid`、`rev` | 取自 begin 响应 |
| `file_convert_path` | `docid` | **完整 docid** |
| `file_search` | — | 不需手动拼接 |
| `doc_lib_owned` | `{}` | 取返回的 `id` |

### sharedlink

分享链接格式：`https://<文档域>/link/<link_id>`。解析步骤见 **「📎 分享链接」** 章节。

### namepath

`file_convert_path` 返回的路径，仅供展示，**不能当 docid 传参**。

### 文件 vs 文件夹

看 `size = -1` 即为文件夹。

### skill_name

- `__全文写作__3` — 生成大纲
- `__大纲写作__1` — 生成正文

---

## 🔧 本技能工具与 mcporter 调用

> **参数与响应体结构以 `mcporter list asmcp` 返回的 schema 为准**，本节仅标注业务约束（固定字段、关键卡点、特殊规则）。

### mcporter 调用规范

**参数格式**：`key=value`，**不是** `--key value`

- ✅ `mcporter call asmcp.file_search keyword="文档" type="doc" start=0 rows=25`
- ❌ `mcporter call asmcp.file_search --keyword 文档`

**超时配置**：`smart_assistant`（场景四全文写作）需要 10 分钟超时，在 `~/.openclaw/openclaw.json` 的 `skills.entries["anyshare-mcp-skills"].env` 中设置 `MCPORTER_CALL_TIMEOUT=600000`（毫秒）。兜底：单次 `mcporter call` 末尾加 `--timeout 600000`。

### file_search

**固定字段**（不许改）：`type="doc"`, `dimension=["basename"]`, `model="phrase"`

**动态字段**：仅 `keyword`、`start`、`rows`、`range`（4 个）

**不传字段**：`condition`、`custom`、`delimiter` 等可能导致服务端报错，一律不传

**返回结构**：响应内容在 `result.files` 数组，每项含 `basename`、`size`、`extension`、`doc_id`、`parent_path`、`highlight` 等。

**分页**：`rows` 上限 25；下一页将 `start` 设为上次响应的 `next` 值。

### folder_sub_objects

**传完整 docid**，不传 id（最后一段）。

### doc_lib_owned

查询当前用户拥有的文档库列表（含**个人文档库**等）。

**输出**：JSON 数组，每项含 `id`（文档库根 **docid**）、`name`、`type`（如 `user_doc_lib` 表示个人文档库）等；字段以实际返回为准。

**典型场景**：用户说「上传到**我的个人文档库**」并给出本地文件路径时，可先调本工具列出文档库，用 **`type`** 为 **`user_doc_lib`**（或用户点名的库名对应项）的 **`id`** 作为 **`file_osbeginupload`** 的 **`docid`**（目标目录），再按场景二走 **`file_convert_path`** 确认（C3）与分步上传。**不要**用用户本机路径当 AnyShare 知识库 docid。

### file_osdownload

**场景四（全文写作）**：取得 **`source_ranges`** 所需 **id** 后**不要**用本工具「先拉全文再写」——下一步应直接 **`smart_assistant`**（**C10**）。本工具用于 **场景三** 等**明确下载**诉求。

### file_osbeginupload

初始化直传。**`name`**、**`length`** 须与实际上传文件一致（`length` 为字节数，>0）。**目标目录**为 **C3** 用户确认后的 **`docid`**。

**返回**：含 **`authrequest`**（字符串数组）、**`docid`**（上传后的新文件 docid）、**`name`**、**`rev`** 等。

### 对象存储直传 PUT

`authrequest`：**第 0 项**为 HTTP 方法（如 `PUT`），**第 1 项**为对象存储 URL，**第 2 项起**为请求头，形如 `Header-Name: value`。**请求体**为待上传文件的**原始字节**。此步**不是** MCP 工具调用；须在 **运行环境能读取该文件字节** 的前提下完成（例如本机终端 `curl`、脚本等）。**PUT 返回成功（通常 2xx）后**才能调用 **`file_osendupload`**（**C11**）。若调用方文件与执行 PUT 的环境**不在同一可访问路径**，无法单靠本技能完成直传，须向用户说明并改用可达方式（如将文件放到执行环境可读位置、或使用企业提供的其它上传通道）。

### file_osendupload

确认上传完成。**`docid`**、**`rev`** 必须使用 **`file_osbeginupload`** 响应中的值（新文件 docid，勿误用仅作为上传目标的父目录 docid）。

**说明**：**禁止**使用 **`file_upload`**（**C11**）。

### file_convert_path

**仅用于展示 namepath**，不替代其它工具的 docid 传参。详见上文「**核心概念**」→ **namepath** 与 **传参规则**。

### file_share_path

获取文件分享链接（若不存在会自动创建）。**`docid`**：完整 gns 路径。

**返回**：`link_url`（分享链接）、`file_name`、`file_path_anyshare`、`namepath` 等。

### sharedlink_parse

解析分享链接详情。**`link_id`**：分享 URL 中 **`/link/`** 路径段之后。

**返回结构**：响应含 `type`（如 `realname` / `anonymous`）、顶层 `id`（**分享链** id）、`item` 对象。`item` 内：**`item.id`** 为完整 **docid**（`gns://…`）；**`item.type`** 为 `file` / `folder` 等。进入场景四后，`smart_assistant` 的 `source_ranges[].id` 取 **`item.id`** 最后一段，不传完整 docid（见 C5）。

### smart_assistant（全文写作 · 生成大纲）

**skill_name**：`__全文写作__3`

**`source_ranges[].id`** 传 **id**（docid 最后一段），**禁止传完整 docid**（C5）。

```json
// ✅ 正确：传 id（最后一段）
"source_ranges": [{ "id": "2DDD46B195F24BCEB238DB59151CD15E", "type": "doc" }]

// ❌ 错误：传完整 docid
"source_ranges": [{ "id": "gns://E6D15886/.../2DDD46B195F24BCEB238DB59151CD15E", "type": "doc" }]
```

`version`、`temporary_area_id` **不要传**。

**成功返回**：

- **`streaming_answer`**：流式阶段正文级累加，**大纲/要点**以此为准 → **向用户展示并请其确认（C4）**。
- **`completion_answer`**：流式结束 `completed` 时解析，**多为提示语、按钮引导**，**不作为**大纲正文。
- **`conversation_id`**：下一调用（「基于大纲生成正文」）必传。
```

### smart_assistant（全文写作 · 基于大纲生成正文）

**skill_name**：`__大纲写作__1`

**本步返回：** 最终成稿正文以 **`streaming_answer`** 为准；**`completion_answer`** 多为收尾说明。

### 工具列表查询（诊断用）

```bash
mcporter list asmcp
```

---

## 📂 场景一：文件/关键词搜索

> **说明**：`file_search` 固定字段、返回与分页见 **[上文「本技能工具与 mcporter 调用」→ file_search](#file_search)**。

### 步骤

**第 1 步：`file_search`**

入参、出参 JSON 与 **mcporter 示例**见 **[上文 file_search](#file_search)**。

> ⚠️ `dimension: ["basename"]` + `model: "phrase"` **必须固定**，不随关键词变化。省略会导致正文/多字段命中，而非按名匹配。

**第 2 步：展示结果（必须含三要素）**

对每条结果：**先调 `file_convert_path`** → 再展示：

- **名称**：`basename`
- **大小**：`size = -1` → 目录；`size ≥ 0` → 实际字节数
- **AnyShare 知识库路径**：`namepath`（来自 `file_convert_path` 返回）

> ⚠️ **C1 + C2**：禁止跳过 `file_convert_path`；禁止用 docid/序号代替 namepath 展示。

**第 3 步：用户确认 docid（如需操作）**

**分页提示（hits ≥ 25 时强制显示）：**

> 找到 X 条（已展示前 25 条），是否：
>
> 1. **查看更多**（翻页）  2. **更换关键词**  3. **缩小范围**（加 range）

**搜索结果为空时：**

> 未找到匹配文件。可尝试：
> 1. **更换关键词**（去掉修饰词，保留核心词）
> 2. **放宽范围**（不指定 range，或扩大 range）
> 3. **换搜索引擎**（type="all" 综合搜索）

请选择或输入新关键词。

**按文件夹名查看子文件：**

1. 搜索结果中找 `size = -1` 且 basename 一致的项
2. 对该 docid 先调 `file_convert_path` 展示目录 namepath（C2）
3. 再调 **[folder_sub_objects](#folder_sub_objects)** 列出子文件

> **Agent 话术示例 - Agent 展示搜索结果**：
> ```
> 找到 5 个结果：
>
> 1. 年度报告2024.docx - 2.3MB - 知识库/财务部/2024/
> 2. 季度总结Q3.pdf - 1.1MB - 知识库/运营部/2024/
> 3. 项目计划书.docx - 850KB - 知识库/项目部/文档/
> 4. 会议纪要.docx - 120KB - 知识库/综合办/2024/
> 5. 技术方案.docx - 3.2MB - 知识库/技术部/方案/
>
> 请输入序号选择，或输入"更多"查看下一页。
> ```

> **Agent 话术示例 - 用户选择后确认**：
> ```
> 已选择「年度报告2024.docx」
> - docid: gns://E6D15886/A51FA4844/2DDD46B195F24BCEB238DB59151CD15E
> - 知识库路径: 知识库/财务部/2024/
>
> 请确认是否继续操作？回复"是"继续，回复其他重新选择。
> ```

---

## 📂 场景二：上传文件

### 步骤

**第 1 步：确定目标目录 docid**（**必须 C3**）

- **一般情况**：`file_search` + `file_convert_path` 搜索并展示目录，用户确认。
- **用户明确要传到「个人文档库」**：可先 **`doc_lib_owned`**（见 **[上文 doc_lib_owned](#doc_lib_owned)**）取列表，选中个人文档库项的 **`id`**（`gns://…`）作为目标目录，再 **`file_convert_path`** 展示 `namepath` 供用户确认。本地文件路径（如 `/Users/…/file.zip`）仅用于后续 **PUT** 读文件，**不是** `docid`。

**展示确认模板：**

> 即将上传到：
>
> - 文件名：`<本地文件名>`
> - AnyShare 知识库路径：`file_convert_path` 返回的 `namepath`
> - docid：`gns://...`
>
> 确认继续？回复"是"，或提供其他目标路径。

**第 2 步：用户回复"是"后锁定 docid（C3）**

**第 3 步：分步上传（`file_osbeginupload` → PUT → `file_osendupload`，必须 C11）**

1. 调用 **`file_osbeginupload`**：`docid` 为已确认的目标**目录**；`name`、`length` 与待传文件一致（由用户提供或仅在执行环境可读时从本地取得）。**begin 返回信息有 15 分钟有效期**。
2. 根据响应中的 **`authrequest`**，对对象存储 URL 执行 **HTTP PUT**（请求体为文件字节）。**非 MCP 工具**。
3. **PUT 失败**：从 **Step 1** 重新开始（begin 上传信息已过期，需重新获取）。
4. 调用 **`file_osendupload`**：**`docid`**、**`rev`** 取自 **begin 响应**（新文件 docid）。

**第 4 步：汇报**

1. 对新文件 docid 调 **`file_share_path`** 获取分享链接
2. 展示链接、文件名、文件路径

> **Agent 话术示例 - Agent 上传完成后汇报**：
> ```
> ✅ 文件上传成功！
>
> - 分享链接：https://anyshare.aishu.cn/link/XXXXXXXXXXXXXXXX
> - 文件名：项目计划书v2.docx
> - 文件路径：AnyShare://文档库/项目计划书v2.docx
>
> 可点击链接直接访问或下载。
> ```

---

## 📂 场景三：下载文件

### 步骤

**第 1 步：搜索目标文件**（`file_search` + `file_convert_path`，**必须 C3**）

**展示确认模板：**

> 即将下载：
>
> - 文件名：`<basename>`
> - 大小：`<size> 字节`
> - AnyShare 知识库路径：`file_convert_path` 返回的 `namepath`
> - docid：`gns://...`
>
> 确认继续？回复"是"，或选择其他文件。

**第 2 步：用户回复"是"后锁定 docid（C3）**

**第 3 步：`file_osdownload`**

入参、出参 JSON 见 **[上文 file_osdownload](#file_osdownload)**。

> **Agent 话术示例 - Agent 下载完成后汇报**：
> ```
> ✅ 文件下载成功！
>
> - 文件名：年度报告2024.docx
> - 保存位置：/Users/jerrychen/Downloads/年度报告2024.docx
> - 大小：2.3MB
>
> 文件已保存到本地。
> ```

---

## 📂 场景四：全文写作

> **说明**：**`smart_assistant`** 两阶段（大纲 / 正文）的完整入参、返回字段与 JSON 示例见 **[上文「本技能工具与 mcporter 调用」](#本技能工具与-mcporter-调用)** 中 **「smart_assistant（全文写作 · 生成大纲）」** 与 **「smart_assistant（全文写作 · 基于大纲生成正文）」**。

**入口**：用户已确认走全文写作流程。

> ⚠️ **硬卡点**：进入前须掌握 docid 与 id（见硬卡点表 C8）；取得 id 后禁止先下载（见 C10）；大纲未确认禁止生成正文（见 C4）。

### 步骤

**第 1 步：确认文档 id（已在 C8 取得 docid / id）**

- 分享链接 → 按 **[📎 分享链接（从 URL 到 docid）](#分享链接从-url-到-docid)** 得到 **id**
- 关键词 → `file_search` 确认文档 id

确认 **id** 后 **直接进入第 2 步**，**勿**先 **`file_osdownload`**（**C10**）。

**第 2 步：生成大纲（`__全文写作__3`）**

入参、返回字段与 JSON 示例见 **[上文「本技能工具与 mcporter 调用」→ smart_assistant（全文写作 · 生成大纲）](#本技能工具与-mcporter-调用)**。向用户展示并请其确认（**C4**）的稿，以返回 **`streaming_answer`** 为准；**`completion_answer`** 多为收尾/提示，**不作为**大纲正文。第 3 步需传入的 **`conversation_id`** 取自本步返回。

→ 将 **`streaming_answer`** 展示给用户 → **等待用户确认或修改后再进入第 3 步**（C4）。

**第 3 步：生成正文（`__大纲写作__1`）**

仅在 **C4** 确认后调用。入参、返回字段与 JSON 示例见 **[上文「本技能工具与 mcporter 调用」→ smart_assistant（全文写作 · 基于大纲生成正文）](#本技能工具与-mcporter-调用)**。**`selection`** 通常取第 2 步 **`streaming_answer`** 全文（用户改稿后以其最终稿为准）；**`conversation_id`** 用第 2 步返回。

→ 正文生成完成后，**向用户展示并请其确认**，确认后再进入第 4 步。

**第 4 步：导出**（保存本地 / 上传至 AnyShare 复用场景二）

> ⚠️ **C5**：`source_ranges[].id` 必须传 id（docid 最后一段），**禁止传完整 docid**。

> **Agent 话术示例 - Agent 展示大纲并请求确认**：
> ```
> 已生成大纲，请确认：
>
> 一、项目背景与目标
>    1.1 项目概述
>    1.2 建设目标
>
> 二、系统架构设计
>    2.1 总体架构
>    2.2 技术选型
>
> 三、实施计划
>    3.1 阶段划分
>    3.2 关键里程碑
>
> 四、预算估算
>
> 请确认大纲是否OK，或提出修改意见。确认后我将生成正文。
> ```

> **Agent 话术示例 - 用户确认大纲后生成正文**：
> ```
> 好的，开始基于大纲生成正文，预计需要几分钟...
> （正文生成完成）
> ```
>
> **正文生成后，必须向用户展示并确认**：
> ```
> ✅ 正文生成完成！以下是开头部分：
>
> 一、项目背景与目标
>
> 1.1 项目概述
> 本项目旨在构建一套企业级知识管理平台，...
>
> （因篇幅原因省略中间部分）
>
> 请确认正文是否OK，或提出修改意见。确认后我将保存到 AnyShare。
> ```

---

## 📎 分享链接（从 URL 到 docid）

> **任务入口**：用户粘贴 `https://…/link/…` 时，先读本节再调工具；**`sharedlink_parse`** 的入参、返回字段见上文 **「本技能工具与 mcporter 调用」** 小节中的 **`sharedlink_parse`**。需已具备 MCP 认证（已按 **「首次配置」** 完成 token 写入）；未授权按 [references/troubleshooting.md](references/troubleshooting.md) 处理。

**触发**：用户提供文档域下的分享 URL（任意 `…/link/<link_id>` 形态）。

**第 1 步：提取 `link_id`**  
取路径 **`/link/`** 之后的一段。示例：`https://anyshare.aishu.cn/link/AR85DF4473697974F48EDDB4967AEA2B61` → `link_id` = `AR85DF4473697974F48EDDB4967AEA2B61`。（**C6**）

**第 2 步：调用 `sharedlink_parse`**  
入参 JSON 见上文 **「本技能工具与 mcporter 调用」** 中 **`sharedlink_parse`**（仅 `link_id`）。

**第 3 步：解析后分流（C7、C5）**

- **`docid`** = **`item.id`**（`gns://…`）；响应**顶层 `id`** 为分享链自身 id，**≠** `item.id`（**C7**）。
- **`item.type` = `folder`** → **`file_convert_path`**（`docid` = `item.id`）展示 `namepath`（**C2**）→ **`folder_sub_objects`** 列子项。
- **`file` / 其他** → 取 **`item.id`** 最后一段为 **id**，进入 **「场景四：全文写作」** 调用 `smart_assistant`（**C5**）。

---

## 📖 补充资料（权威来源）


| 文件 | 权威内容 | 用于 |
| --- | --- | --- |
| **本 SKILL.md** → **「🚀 首次配置」** | asmcp.url、daemon、企业地址确认、token 写入 headers | 首次配置（**唯一权威**） |
| **本 SKILL.md** → **「📌 核心概念」** | docid、id、sharedlink、namepath、传参、skill_name | 概念 |
| **本 SKILL.md** → **「📎 分享链接（从 URL 到 docid）」** | `link_id`、folder/file 分流（C6/C7） | 用户粘贴 `/link/` URL |
| **本 SKILL.md** → **「🔧 本技能工具与 mcporter 调用」** | 工具 JSON、mcporter、auth、诊断 | 工具调用 |
| [references/troubleshooting.md](references/troubleshooting.md) | 错误码、常见处理 | 排障 |
| [SECURITY.md](SECURITY.md) | 安全约束、敏感信息 | 安全审计 |


