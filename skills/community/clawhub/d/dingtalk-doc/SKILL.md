---
name: dingtalk-doc
description: 钉钉文档管理技能。当用户发送的消息中包含 alidocs.dingtalk.com 链接、要求总结/读取/查看/更新钉钉文档或钉钉知识库文档，或当前上下文已明确对象是钉钉文档时使用。关键词：钉钉文档、钉钉知识库、alidocs、总结、读取、查看、更新、修改、文档、链接。
---

# 钉钉文档管理技能

通过钉钉开放平台 API 管理钉钉文档与钉钉知识库内文档。`SKILL.md` 只保留 agent 执行所需规则;配置细节、示例、API 背景见 `README.md`。

## 何时使用

### 触发关键词

只有在**已经确认对象是钉钉文档**时，同时消息包含以下**任一关键词**时，优先使用本 skill：

| 类别 | 关键词 |
|------|--------|
| **平台名** | 钉钉文档、钉钉知识库、alidocs |
| **读取类** | 总结、读取、查看、浏览、列出结构 |
| **修改类** | 更新、修改、追加、删除、覆写 |
| **对象** | 文档、链接、这篇、这个文档 |

**组合示例：**
- "总结一下这篇钉钉文档"
- "读取这个 alidocs 链接"
- "更新文档内容"
- "删除第三段"

### 触发场景（优先级从高到低）

| 场景 | 示例 | 动作 |
|------|------|------|
| **钉钉文档链接** | `alidocs.dingtalk.com/i/nodes/xxx` | 根据意图选择：元数据→`get-doc`，正文内容→`get-content` |
| **钉钉上下文 + 链接** | "总结 https://alidocs.dingtalk.com/..." | 调用 `get-content` 读取内容后总结 |
| **明确命令** | "总结这篇文档"、"读取这个 alidocs 链接" | 根据意图选择命令 |
| **已知上下文是钉钉文档** | 前文已给出 alidocs 链接，后续说"更新文档"、"删除某段"、"在第三段后追加" | 调用对应命令 |
| **结构查询** | "列出结构"、"这个 alidocs 有哪些章节" | 调用 `get-content` |
| **块级操作** | "删除第三段"、"修改这个段落"、"在这里插入一段" | 先用 `get-content` 获取 blockId 和位置，再调用 `delete-block`/`modify-block`/`insert-block` |

### 不触发的场景
- 查询本地文件、离线文档或普通文本内容，且不需要调用钉钉 API
- 没有文档链接、docKey、或明确钉钉文档上下文，却要求修改文档
- 用户只说"总结文档""更新这个链接"等泛化请求，但上下文无法确认对象是钉钉文档
- 与钉钉无关的文档系统，例如本地 Markdown、飞书文档、语雀、Google Docs

## 运行前提

### 环境变量

必须配置以下环境变量 (在 Gateway 环境中):

- `DINGTALK_CLIENTID` - 钉钉应用 Client ID (AppKey)
- `DINGTALK_CLIENTSECRET` - 钉钉应用 Client Secret (AppSecret)

可选环境变量:

- `OPENCLAW_SENDER_ID` / `DINGTALK_SENDER_ID` - 由 OpenClaw / 钉钉连接器注入的当前用户 sender_id；也可以通过命令行 `--senderId=` 显式传入
- `DINGTALK_DEBUG` - 设置为 `true` 启用调试模式；仅输出方法、路径（查询参数已脱敏）、状态码、requestId 等，不打印文档正文与完整请求体

### operatorId 获取方式

不需要在配置中指定!系统会自动从当前会话获取:

1. 从 `OPENCLAW_SENDER_ID` 或 `DINGTALK_SENDER_ID` 获取 sender_id
2. 调用钉钉 API 查询对应的 unionId
3. 使用 unionId 作为 operatorId

如果获取失败，会显示友好的错误提示。

## 执行规则

- 读取操作不受白名单限制
- 默认直接在白名单配置的`workspaceId`中尝试写入
- 写入操作必须通过白名单检查;未配置 workspace 或节点名不在白名单内时，一律拒绝!**没有任何方式可以绕过白名单检查!**
- `whitelist: ["/"]` 表示允许写入该 workspace 下的所有节点;更细粒度控制请配置具体文档名，例如 `"/三级目录测试文档.adoc"`
- 白名单配置文件 `config/whitelist.json` 只能由用户手动修改;AI 只能读取、解释、提示用户手动调整，不能替用户改
- 如果用户没有给出目标文档的 `nodeId` / `docKey`,先运行 `list-docs`、`search` 或 `get-doc` 确认目标

## URL 解析规则

当用户提供钉钉文档 URL 时，按以下规则提取 `nodeId`:

**URL 格式:** `https://alidocs.dingtalk.com/i/nodes/<nodeId>?...`

**提取方法:**
1. 从 URL 中提取 `nodes/` 和 `?` 之间的部分
2. 该部分即为 `nodeId`

**示例:**
```
URL: https://alidocs.dingtalk.com/i/nodes/oP0MALyR8kOd5BGacKv6NbxE83bzYmDO?utm_scene=team_space
nodeId: oP0MALyR8kOd5BGacKv6NbxE83bzYmDO
```

**提取到 nodeId 后的操作:**
1. **获取文档元数据**（名称、知识库 ID 等）：`get-doc --nodeId=<提取的 nodeId>`
2. **获取文档内容**（总结、读取正文）：`get-content --docKey=<提取的 nodeId>`
3. 注意：`get-doc` 只返回元数据，`get-content` 才返回正文内容

## 执行入口

- `scripts/index.js`:主入口
- `scripts/whitelist.js`:辅助检查白名单配置

**跨平台说明：**

- 本 skill 的脚本基于 Node.js 内置模块实现，Windows、Linux、macOS 只要安装了 `node` 并配置好环境变量，都可以运行
- 推荐优先使用相对路径执行：`node scripts/index.js ...`，这样最不容易受平台路径差异影响

**路径示例：**

Windows PowerShell 中 `~` 不会自动展开，建议使用以下方式之一：

```bash
# ✅ 使用 $env:USERPROFILE
node $env:USERPROFILE\.openclaw\skills\dingtalk-doc\scripts\index.js

# ✅ 或使用完整绝对路径
node C:\Users\zhenhuaixiu\.openclaw\skills\dingtalk-doc\scripts\index.js

# ❌ 错误（~ 不会展开）
node ~/.openclaw/skills/dingtalk-doc/scripts/index.js
```

Linux / macOS Shell 示例：

```bash
# ✅ 当前目录下直接运行（推荐）
node scripts/index.js list-workspaces

# ✅ 或使用完整绝对路径
node ~/.openclaw/skills/dingtalk-doc/scripts/index.js list-workspaces
```

## 命令映射

**路径说明：**

- Windows 示例中的 `$env:USERPROFILE\.openclaw` 会展开为 `C:\Users\<用户名>\.openclaw`
- Linux / macOS 示例中的 `~/.openclaw` 会展开为用户主目录下的 `.openclaw`
- 如果当前工作目录已经在 skill 根目录，直接使用 `node scripts/index.js ...` 即可

### 读取操作

| 命令 | 用途 | API 端点 |
|------|------|---------|
| `list-workspaces` | 获取知识库列表 | `GET /v2.0/wiki/mineWorkspaces` |
| `list-docs` | 获取知识库中文档列表 | `GET /v2.0/wiki/nodes` |
| `get-doc` | 获取**文档元数据**（名称、ID、创建者、字数等） | `GET /v2.0/wiki/nodes/{nodeId}` |
| `get-content` | 获取**文档正文内容**（段落、标题、列表等块结构） | `GET /v1.0/doc/suites/documents/{docKey}/blocks` |
| `search` | 搜索文档 | `GET /v1.0/doc/workspaces/{workspaceId}/docs` |

**示例：**
```bash
# Linux / macOS
node ~/.openclaw/skills/dingtalk-doc/scripts/index.js list-workspaces
node ~/.openclaw/skills/dingtalk-doc/scripts/index.js list-docs --workspaceId=YRBGvyxxx --parentNodeId=root
node ~/.openclaw/skills/dingtalk-doc/scripts/index.js get-doc --nodeId=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz
node ~/.openclaw/skills/dingtalk-doc/scripts/index.js get-content --docKey=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz
node ~/.openclaw/skills/dingtalk-doc/scripts/index.js search --workspaceId=YRBGvyxxx --keyword="需求"

# Windows PowerShell
node $env:USERPROFILE\.openclaw\skills\dingtalk-doc\scripts\index.js list-workspaces
node $env:USERPROFILE\.openclaw\skills\dingtalk-doc\scripts\index.js list-docs --workspaceId=YRBGvyxxx --parentNodeId=root
node $env:USERPROFILE\.openclaw\skills\dingtalk-doc\scripts\index.js get-doc --nodeId=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz
node $env:USERPROFILE\.openclaw\skills\dingtalk-doc\scripts\index.js get-content --docKey=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz
node $env:USERPROFILE\.openclaw\skills\dingtalk-doc\scripts\index.js search --workspaceId=YRBGvyxxx --keyword="需求"
```

### 写入操作

```bash
# Linux / macOS
node ~/.openclaw/skills/dingtalk-doc/scripts/index.js create-doc --workspaceId=YRBGvyxxx --name="新文档" --docType=DOC --parentNodeId=root
node ~/.openclaw/skills/dingtalk-doc/scripts/index.js update-content --nodeId=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz --content="# 标题\n\n内容"
node ~/.openclaw/skills/dingtalk-doc/scripts/index.js update-content --nodeId=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz --docKey=真实docKey --content="# 标题\n\n内容"
node ~/.openclaw/skills/dingtalk-doc/scripts/index.js delete-doc --workspaceId=YRBGvyxxx --nodeId=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz

# Windows PowerShell
# 创建文档
node $env:USERPROFILE\.openclaw\skills\dingtalk-doc\scripts\index.js create-doc --workspaceId=YRBGvyxxx --name="新文档" --docType=DOC --parentNodeId=root
# 返回：{ "docKey": "abc123", "nodeId": "xyz789", ... }

# 更新文档内容（整篇覆写，替换全部内容）
# ✅ 推荐：只用 nodeId（大多数情况够用）
node $env:USERPROFILE\.openclaw\skills\dingtalk-doc\scripts\index.js update-content --nodeId=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz --content="# 标题\n\n内容"

# ✅ 备选：如果上面失败，传入真实的 docKey
node $env:USERPROFILE\.openclaw\skills\dingtalk-doc\scripts\index.js update-content --nodeId=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz --docKey=真实 docKey --content="# 标题\n\n内容"

# 删除文档
node $env:USERPROFILE\.openclaw\skills\dingtalk-doc\scripts\index.js delete-doc --workspaceId=YRBGvyxxx --nodeId=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz
```

### 块级操作（精细修改单个段落/元素）

说明：

- `insert-block`、`modify-block`、`delete-block` 已通过真实文档测试
- `append-text` 对应的公开 API 当前返回 `InvalidAction.NotFound`，不要再调用或承诺
- 如果用户要“追加内容”，优先改成“插入一个新段落”或“读取原段落后使用 `modify-block` 整块替换”

```bash
# Linux / macOS
node ~/.openclaw/skills/dingtalk-doc/scripts/index.js delete-block --nodeId=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz --blockId=blk123
node ~/.openclaw/skills/dingtalk-doc/scripts/index.js modify-block --nodeId=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz --blockId=blk123 --element='{"blockType":"paragraph","paragraph":{"text":"新内容"}}'
node ~/.openclaw/skills/dingtalk-doc/scripts/index.js insert-block --nodeId=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz --element='{"blockType":"paragraph","paragraph":{"text":"插入的内容"}}' --position=3

# Windows PowerShell
# 删除块元素（删除某个段落/标题/列表项）
node $env:USERPROFILE\.openclaw\skills\dingtalk-doc\scripts\index.js delete-block --nodeId=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz --blockId=blk123

# 修改块元素（替换单个块的内容，不影响其他部分）
node $env:USERPROFILE\.openclaw\skills\dingtalk-doc\scripts\index.js modify-block --nodeId=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz --blockId=blk123 --element='{"blockType":"paragraph","paragraph":{"text":"新内容"}}'

# 插入块元素（在指定位置插入新段落/标题等）
node $env:USERPROFILE\.openclaw\skills\dingtalk-doc\scripts\index.js insert-block --nodeId=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz --element='{"blockType":"paragraph","paragraph":{"text":"插入的内容"}}' --position=3
```

### 参数说明

- `docType`: `DOC`(文字) | `WORKBOOK`(表格) | `MIND`(脑图) | `FOLDER`(文件夹)
- `nodeId`: **必填**，节点 ID（用于白名单检查）
  - 从文档链接 `alidocs.dingtalk.com/i/nodes/xxx` 提取 `xxx` 部分
  - 通过 `get-doc --nodeId=xxx` 或 `get-content --docKey=xxx` 确认
- `docKey`: **可选**，真实的文档标识符（用于实际写入 API）
  - 如果不传，默认使用 `nodeId` 代替
  - 仅在 `nodeId` 作为 `docKey` 写入失败时，才需要传入真实的 `docKey`
  - 真实 `docKey` 可通过 createDoc 返回值或钉钉 API Explorer 获取
- `blockId`: 块 ID，通过 `get-content` 获取文档结构后得到（块级操作必需）
- `element`: 块元素 JSON 对象（**会自动解析**，直接传 JSON 字符串即可）
  - 示例：`--element='{"blockType":"paragraph","paragraph":{"text":"新内容"}}'`
- `position`: 插入位置（可选），数字，**支持 0**（表示插到最前面）
- `workspaceId`: 知识库 ID（可选）
  - 注意：写入操作会通过 `nodeId` 查询节点真实 `workspaceId`，传入 `--workspaceId` 时只能作为一致性校验，不能跳过查询
  - 适用场景：已知 `workspaceId` 且想显式校验目标文档属于该知识库，但 `nodeId` 仍必需

### 命令选择指南

| 需求 | 使用命令 | 说明 |
|------|---------|------|
| 重写整篇文档 | `update-content --nodeId=xxx --content="..."` | 替换全部内容 |
| 只修改某个段落 | `modify-block --nodeId=xxx --blockId=blk --element='{...}'` | 只影响单个块 |
| 在当前位置新增一段 | `insert-block --nodeId=xxx --element='{...}' --position=3` | 插入一个新块，更适合“追加一段”的需求 |
| 删除某一段/标题 | `delete-block --nodeId=xxx --blockId=blk` | 删除块 |
| 插入新段落/标题 | `insert-block --nodeId=xxx --element='{...}' --position=3` | 在指定位置插入 |

## 常见问题

1. **"无法获取文档信息"错误**: 
   - 确保传入的是 `nodeId`（从文档链接 `/i/nodes/xxx` 提取）
   - `--workspaceId` 不能替代 `nodeId`，只能作为额外一致性校验
   
2. **"paramError" / JSON 解析失败**: 
   - `--element` 必须是合法的 JSON 格式，检查引号转义
   - PowerShell 中用单引号包裹：`--element='{"type":"paragraph"}'`
   
3. **更新失败（nodeNotExist 等）**: 
   - 尝试传入真实的 `docKey`：`update-content --nodeId=xxx --docKey=真实 docKey --content="..."`
   - createDoc 返回的 `docKey` 和 `nodeId` 可能不同

4. **nodeId 和 docKey 到底有什么区别？**
   - `nodeId`: 目录树节点 ID（wiki_2.0 API 用），用于定位文档、获取 workspaceId 和节点名、执行白名单检查
   - `docKey`: 文档内容标识符（suites/documents API 用），用于实际读写内容
   - 经验：大多数情况下 `nodeId` 可直接用作 `docKey`，少数情况需要真实 `docKey`

5. **为什么没有 append-text？**
   - 当前公开接口 `POST /v1.0/doc/suites/documents/{docKey}/paragraphs/{blockId}/text` 在真实测试中返回 `InvalidAction.NotFound`
   - 因此本 skill 不再承诺 `append-text`，请使用 `insert-block` 或 `modify-block`

## 推荐流程

1. 先确认凭证和 sender_id 是否可用。
2. 需要定位文档所在知识库时先跑 `list-workspaces`。
3. 需要定位文档时先跑 `list-docs`、`search`、`get-doc`。
4. 执行写操作前，默认假设会触发白名单校验，不要跳过读取确认步骤。
5. 如果写入被拒绝，只说明是哪个 workspace / 节点名未通过白名单，并提示用户手动调整 `config/whitelist.json`。

## 常见失败

- 缺少 sender_id:检查钉钉连接器是否注入 `OPENCLAW_SENDER_ID` / `DINGTALK_SENDER_ID`
- `forbidden.accessDenied`:检查应用权限或白名单
- `invalidRequest.workspaceNode.parentNotFound`:检查 `parentNodeId`
- `权限拒绝：知识库 xxx 未配置白名单`:让用户手动补充 `config/whitelist.json`
- `nodeNotExist`(更新内容时):**尝试使用 nodeId 代替 docKey** - 钉钉 API 中 createDoc 返回的 docKey 和 overwriteContent 需要的 docKey 可能不一致
- `blockNotExist`(块级操作时):先用 `get-content` 获取文档结构，确认 blockId 正确
- `paramError`(modify-block/insert-block):检查 `--element` 参数是否是合法的 JSON 格式

## 重要提示

### get-doc vs get-content

| 命令 | 用途 | 返回内容 | 何时使用 |
|------|------|---------|---------|
| `get-doc` | 获取**文档元数据** | `data.node`：名称、ID、创建者、修改时间、字数、workspaceId | 确认文档存在、获取文档基本信息、定位知识库 |
| `get-content` | 获取**文档正文** | `data.result.data[]`：段落、标题、列表等块结构 | 总结内容、读取正文、准备修改文档 |

**关键区别：**
- `get-doc` → `GET /v2.0/wiki/nodes/{nodeId}` → **不包含正文内容**
- `get-content` → `GET /v1.0/doc/suites/documents/{docKey}/blocks` → **包含正文块结构**
- **总结、读取内容时，始终使用 `get-content`，不要用 `get-doc`**

### docKey vs nodeId

- `nodeId`: 目录树节点 ID（wiki_2.0 API 用），用于定位文档、获取 workspaceId 和节点名、执行白名单检查
- `docKey`: 文档内容标识符（suites/documents API 用），用于实际读写内容
- `create-doc` 返回的 `docKey` 和 `nodeId` 可能是不同的值
- `update-content`、`get-content` 等命令**优先使用 `nodeId`** 作为 `--docKey` 参数
- 如果使用 `docKey` 更新失败 (`nodeNotExist`),请改用 `nodeId`
- 经验：大多数情况下 `nodeId` 可直接用作 `docKey`，少数情况需要真实 `docKey`

**示例:**

```bash
# 创建文档后，使用返回的 nodeId 进行更新
node .../index.js create-doc --workspaceId=xxx --name="新文档"
# 返回:{ "docKey": "abc123", "nodeId": "xyz789", ... }

# ✅ 正确：使用 nodeId 更新
node .../index.js update-content --docKey=xyz789 --content="..."

# ❌ 可能失败：使用 docKey 更新
node .../index.js update-content --docKey=abc123 --content="..."
```

## 参考

- 详细说明见 `README.md`
- 钉钉开放平台文档:[knowledge-base-overview](https://open.dingtalk.com/document/development/knowledge-base-overview)
- API Explorer:[open-dev.dingtalk.com/apiExplorer](https://open-dev.dingtalk.com/apiExplorer)
