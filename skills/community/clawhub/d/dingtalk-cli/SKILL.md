---
name: dingtalk-cli
description: 当用户提到钉钉知识库、钉钉文档、读取/写入文档、知识库目录、文档成员、`.axls` 表格、workbook、dingtalk doc、wiki workspace 时使用。通过本地 `dingtalk-cli` 命令调用钉钉开放平台 API，适合 agent 直接执行。
---

# dingtalk-cli

`dingtalk-cli` 是面向 agent 的钉钉文档 CLI，覆盖：

- 知识库列表与详情
- 节点查询、URL 反查
- 文档创建、正文读取、Markdown 覆盖写入、删除
- `.axls` 钉钉表格的 workbook/sheet/range 读取
- 文档成员添加、更新、移除

## 安装

```bash
pip install dingtalk-cli
```

如需从源码开发安装：

```bash
pip install -e .
```

## 启动前配置

优先使用命令保存配置：

```bash
dingtalk-cli auth setup \
  --app-key <APP_KEY> \
  --app-secret <APP_SECRET> \
  --operator-union-id <UNION_ID>
```

如果只有 `userId`：

```bash
dingtalk-cli auth setup \
  --app-key <APP_KEY> \
  --app-secret <APP_SECRET> \
  --operator-user-id <USER_ID>
```

配置会写到 `~/.dingtalk-cli/config.json`。也可用环境变量覆盖：

- `DINGTALK_APP_KEY`
- `DINGTALK_APP_SECRET`
- `DINGTALK_OPERATOR_ID`
- `DINGTALK_CLI_CONFIG_DIR`

注意：

- 写操作必须带真实用户身份 `operatorId`，且应为 `unionId`
- 输出中不会打印完整凭证，只显示脱敏值

## 常用命令

```bash
# 看知识库
dingtalk-cli workspace list --all

# 用 URL 反查节点
dingtalk-cli node resolve-url "https://alidocs.dingtalk.com/i/nodes/xxx"

# 读取文档正文
dingtalk-cli doc read --url "https://alidocs.dingtalk.com/i/nodes/xxx"

# 覆盖写入文档
dingtalk-cli doc overwrite --doc-key <DOC_KEY> --content-file /abs/path/content.md --yes

# 若立即删除刚创建的文档，优先使用 create 返回的 workspace_id + node_id
dingtalk-cli doc delete --workspace-id <WORKSPACE_ID> --node-id <NODE_ID> --yes

# 读取 .axls 表格
dingtalk-cli workbook read --node-id <NODE_ID> --range A1:Z80

# 添加成员
dingtalk-cli member add --node-id <NODE_ID> --member-id <USER_ID> --role editor
```

## Agent 使用约定

- 优先使用 `--json`
- 对破坏性命令显式传 `--yes`
- 读取普通文档用 `doc`
- 读取 `.axls` 用 `workbook`
- 若 `doc read` 返回“目标节点是 `.axls`”，不要重试同一命令，直接切到 `workbook`
- 对创建命令返回的结果，立即读写时优先使用 `doc_key`
- 对创建后立即删除的场景，优先使用返回的 `workspace_id + node_id`

## 错误提示

- `MissingoperatorId`：未配置 operator unionId
- `paramError`：把 userId 当成 unionId 传了
- `Forbidden.AccessDenied.AccessTokenPermissionDenied`：应用权限不够
- `Target document should be doc.`：目标不是普通文档，通常应改走 `workbook`
