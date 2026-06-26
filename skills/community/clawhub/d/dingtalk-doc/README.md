# 钉钉文档管理技能 (dingtalk-doc)

> [https://clawhub.ai/shyzhen/dingtalk-doc](https://clawhub.ai/shyzhen/dingtalk-doc)
> 
> 是 [dingtalk-doc-enterprise](https://clawhub.ai/shyzhen/dingtalk-doc-enterprise) 的升级版(支持写入范围控制)

通过钉钉开放平台 API 读取和管理钉钉文档、钉钉知识库中的文档。本文件面向人类读者，重点说明配置、上手方式和排障思路；执行规则与触发策略见 `SKILL.md`。

## 能力概览

- 支持列出、搜索、读取钉钉文档
- 支持创建、更新、删除钉钉文档
- 支持多个 workspace 共用一份白名单配置
- 写入操作按 workspace + 节点名白名单控制，读取操作不受白名单限制
- 当前用户身份从钉钉连接器注入的 `sender_id` 自动解析

## 文档分工

- `SKILL.md`：给 agent 的执行手册，强调触发条件、命令映射和失败处理
- `README.md`：给人的配置说明、背景信息、排障参考

## 快速开始

### 1. 配置环境变量

本 skill 可运行在 Windows、Linux、macOS；核心要求只有：

- 安装 `node`
- 配置 `DINGTALK_CLIENTID` / `DINGTALK_CLIENTSECRET`

**编辑 `~/.openclaw/.env` 文件（推荐，优先级最高）**

OpenClaw 会在启动时自动加载此文件中的环境变量。

```bash
# ~/.openclaw/.env
DINGTALK_CLIENTID=dingxxxxxx
DINGTALK_CLIENTSECRET=your_secret
```

说明：

- `DINGTALK_CLIENTID`：钉钉应用 Client ID
- `DINGTALK_CLIENTSECRET`：钉钉应用 Client Secret
- `OPENCLAW_SENDER_ID` / `DINGTALK_SENDER_ID`：通常由 OpenClaw / 钉钉连接器自动注入；如需手工调用 CLI，也可以用 `--senderId=...`
- `DINGTALK_DEBUG=true`：可选，仅输出请求方法、接口路径、状态码、requestId 等调试信息，不再打印文档正文和请求体
- `operatorId` 不需要手工配置，脚本会优先从 `--senderId` 或 `OPENCLAW_SENDER_ID` / `DINGTALK_SENDER_ID` 解析当前钉钉用户

### 2. 确认 workspaceId

- 白名单配置：只支持 【钉钉文档 -> 知识库】下新建的根目录，也就是说可写范围必须在【知识库】中。
- 直接发一篇文档给你的钉钉机器人让他随便写入一段话，就会触发白名单检查，机器人会主动告知你当前文档的workspaceId，以及如何配置。

### 3. 配置白名单

说明：

- 读取操作不依赖白名单文件
- 写入操作才需要 `config/whitelist.json`
- 如果该文件不存在，写操作会被拒绝，并提示用户手动创建

在 `config/whitelist.json` 中声明允许写入的 workspace 和节点名：

```json
{
  "workspaces": [
    {
      "workspaceId": "eLvJDSRX3l4moO87",
      "workspaceName": "AI可写知识库一级目录",
      "allowRootWrite": false,
      "whitelist": ["/"]
    }
  ]
}
```

字段说明：

- `workspaceId`：知识库 ID，必填 （只支持【钉钉文档 -> 知识库】下的目录）
- `workspaceName`：可选，便于识别
- `allowRootWrite`：保留字段；当前写入校验主要使用 `whitelist`
- `whitelist`：允许写入的节点名（文档名）列表

白名单规则：

- 读取操作不检查白名单
- 写入操作必须命中白名单
- 未配置的 workspace 默认禁止写入
- `"/"` 表示允许写入当前 `workspaceId` 下的所有节点
- 细粒度白名单按节点名匹配，例如 `"/三级文档.adoc"`；当前已验证的节点详情接口不会返回完整父目录路径

## 常用命令

这里只保留几个面向人的常见示例；完整命令映射见 `SKILL.md`。

读取：

```bash
# 当前目录运行（跨平台通用）
node scripts/index.js list-workspaces
node scripts/index.js list-docs --workspaceId=OQ0xySj6ng7lX58B --parentNodeId=root
node scripts/index.js get-doc --nodeId=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz
node scripts/index.js get-content --nodeId=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz
node scripts/index.js get-content --docKey=真实docKey --nodeId=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz
```

写入：

```bash
# 当前目录运行（跨平台通用）
node scripts/index.js create-doc --workspaceId=OQ0xySj6ng7lX58B --name="新文档" --docType=DOC --parentNodeId=root
node scripts/index.js update-content --nodeId=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz --content="# 标题\n\n内容"
node scripts/index.js update-content --docKey=真实docKey --nodeId=YQBnd5ExVE0PDnezU2PK2RK6WyeZqMmz --content="# 标题\n\n内容"
```

白名单自检：

```bash
# 当前目录运行（跨平台通用）
node scripts/whitelist.js check "/三级文档.adoc"
```

`docType` 支持：

- `DOC`
- `WORKBOOK`
- `MIND`
- `FOLDER`

## 目录结构

```text
dingtalk-doc/
├── SKILL.md
├── README.md
├── package.json
├── config/
│   └── whitelist.json
└── scripts/
    ├── index.js
    ├── dingtalk-client.js
    └── whitelist.js
```

## 已知返回结构

以下结构来自实测文档 `https://alidocs.dingtalk.com/i/nodes/oP0MALyR8kOd5BGacKv6NbxE83bzYmDO?utm_scene=team_space`，文档名是“三级文档”，真实位于三级子目录中。

`get-doc --nodeId=...` / `GET /v2.0/wiki/nodes/{nodeId}` 返回的 `node` 里有 `workspaceId` 和 `name`，但没有返回完整父目录链路：

```json
{
  "node": {
    "name": "三级文档.adoc",
    "nodeId": "oP0MALyR8kOd5BGacKv6NbxE83bzYmDO",
    "workspaceId": "eLvJDSRX3l4moO87",
    "type": "FILE",
    "category": "ALIDOC",
    "url": "https://alidocs.dingtalk.com/i/nodes/oP0MALyR8kOd5BGacKv6NbxE83bzYmDO"
  }
}
```

容易犯错的点：

- 不要把白名单理解为真实目录路径；当前脚本只能可靠使用 `workspaceId + node.name` 做写入白名单。
- 即使文档在三级子目录中，节点详情也可能只返回 `"name": "三级文档.adoc"`，不会返回 `"/一级/二级/三级文档.adoc"`。
- `get-content --nodeId=...` / `GET /v1.0/doc/suites/documents/{docKey}/blocks` 返回的是块结构，例如 paragraph 的 `id`、`index`、`text`，不返回文档路径或父目录信息。
- `nodeId` 用于查询节点详情和校验真实 `workspaceId`；`docKey` 用于 suites/documents 内容读写接口。多数情况下可先用 `nodeId` 作为 `docKey` 尝试。
- `insert-block`、`modify-block`、`delete-block` 已在真实文档上测试通过；`append-text` 对应的 `paragraphs/{blockId}/text` 当前返回 `InvalidAction.NotFound`，不要依赖它。

## 权限与接口

常用接口：

- `POST /v1.0/doc/workspaces/{workspaceId}/docs`
- `GET /v2.0/wiki/nodes`
- `GET /v2.0/wiki/nodes/{nodeId}`
- `DELETE /v1.0/doc/workspaces/{workspaceId}/docs/{nodeId}`
- `GET /v1.0/doc/suites/documents/{docKey}/blocks`
- `POST /v1.0/doc/suites/documents/{docKey}/overwriteContent`
- `POST /v1.0/doc/suites/documents/{docKey}/blocks`
- `PUT /v1.0/doc/suites/documents/{docKey}/blocks/{blockId}`
- `DELETE /v1.0/doc/suites/documents/{docKey}/blocks/{blockId}`

常见所需权限：

- `Document.Workspace.Read`
- `Document.Workspace.Write`
- `Document.WorkspaceDocument.Read`
- `Document.WorkspaceDocument.Write`
- `Wiki.Node.Read`

## 常见问题

| 问题 | 原因 | 处理方式 |
|------|------|---------|
| 缺少 `sender_id` | 钉钉连接器未传递当前用户 ID | 检查是否注入了 `OPENCLAW_SENDER_ID` 或 `DINGTALK_SENDER_ID` |
| workspace 未配置白名单 | `config/whitelist.json` 没有对应 workspace | 补充对应 `workspaceId` 配置 |
| 节点名不在白名单内 | 写入目标节点名未命中规则 | 调整白名单节点名或使用 `"/"` 允许整个 workspace |
| `forbidden.accessDenied` | 应用权限不足或白名单不通过 | 检查钉钉应用权限和白名单 |
| `invalidRequest.workspaceNode.parentNotFound` | `parentNodeId` 错误 | 重新确认父节点 ID |

## 参考

- 钉钉开放平台文档：[knowledge-base-overview](https://open.dingtalk.com/document/development/knowledge-base-overview)
- API Explorer：[open-dev.dingtalk.com/apiExplorer](https://open-dev.dingtalk.com/apiExplorer)

### API 参考

钉钉知识库 API 分为两个系列：

#### doc_1.0 - 知识库管理

| API | 方法 | 路径 | 权限 |
|-----|------|------|------|
| 新建知识库 | POST | `/v1.0/doc/workspaces` | Document.Workspace.Write |
| 获取知识库 | GET | `/v1.0/doc/workspaces/{workspaceId}` | Document.Workspace.Read |
| 获取知识库列表 | GET | `/v1.0/doc/workspaces` | Document.Workspace.Read |
| 创建知识库文档 | POST | `/v1.0/doc/workspaces/{workspaceId}/docs` | Document.WorkspaceDocument.Write |
| 删除知识库文档 | DELETE | `/v1.0/doc/workspaces/{workspaceId}/docs/{nodeId}` | Document.WorkspaceDocument.Write |

#### wiki_2.0 - 目录树管理

| API | 方法 | 路径 | 权限 |
|-----|------|------|------|
| 获取节点 | GET | `/v2.0/wiki/nodes/{nodeId}` | Wiki.Node.Read |
| 获取节点列表 | GET | `/v2.0/wiki/nodes` | Wiki.Node.Read |
| 通过链接获取节点 | GET | `/v2.0/wiki/nodes/url` | Wiki.Node.Read |
| 复制文档 | POST | `/v2.0/wiki/nodes/{nodeId}/copy` | Document.WorkspaceDocument.Write |

#### suites/documents - 文档内容

| API | 方法 | 路径 | 权限 |
|-----|------|------|------|
| 查询块结构 | GET | `/v1.0/doc/suites/documents/{docKey}/blocks` | Document.WorkspaceDocument.Read |
| 覆写内容 | POST | `/v1.0/doc/suites/documents/{docKey}/overwriteContent` | Document.WorkspaceDocument.Write |
| 插入块 | POST | `/v1.0/doc/suites/documents/{docKey}/blocks` | Document.WorkspaceDocument.Write |
| 删除块 | DELETE | `/v1.0/doc/suites/documents/{docKey}/blocks/{blockId}` | Document.WorkspaceDocument.Write |


#### 所需权限清单

调用本 skill 需要开通以下钉钉应用权限：

- `Document.Workspace.Read` - 知识库读权限
- `Document.Workspace.Write` - 知识库写权限
- `Document.WorkspaceDocument.Read` - 文档读权限
- `Document.WorkspaceDocument.Write` - 文档写权限
- `Wiki.Node.Read` - 节点读权限

## 许可证

MIT
