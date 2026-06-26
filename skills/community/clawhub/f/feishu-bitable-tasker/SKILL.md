---
name: feishu-bitable-tasker
description: 基于飞书知识库多维表格和文档能力的任务管理技能。提供创建任务、创建任务关联文档、修改任务状态等功能，可与外部工具灵活集成。
---

# 飞书任务管理 Skill

## 路径约定

**所有命令路径均相对于本 skill 目录。** 执行命令前必须先 `cd` 到 skill 所在目录。

确定 skill 目录：从当前工作目录查找 `.agents/skills/feishu-bitable-tasker/` 或 `.claude/skills/feishu-bitable-tasker/`，以该目录为基准执行所有命令。

## 调用流程

### 1. 检查配置

```bash
cd <SKILL_DIR> && ls config/credentials.json config/.configured
```

- 两个文件都存在 → 跳到「可用命令」
- 不存在 → 进入「首次配置」

> **多应用支持：** `config/` 下可存放多个凭证文件（如 `team-a.json`、`team-b.json`）。检查配置时，如果默认的 `credentials.json` 不存在但有其他凭证文件，列出可用文件让用户选择。所有命令中的 `config/credentials.json` 均可替换为其他凭证文件路径。

### 2. 首次配置

> **注意：** 本 skill 纯 Node.js 原生模块实现，无需运行 `npm install`。

用一次 AskUserQuestion 收集以下信息（跳过已有有效值的部分）。**每个问题直接要求用户输入数据，不要提供"有/没有"之类的选择项**。引导提示放在问题描述中即可：

- **飞书应用凭证** — 要求输入 App ID 和 App Secret（用空格或逗号分隔）。问题中提示：如果还没有飞书应用，请先到飞书开放平台创建企业自建应用。
- **知识库多维表格链接** — 要求粘贴知识库中的多维表格 URL，格式 `https://xxx.feishu.cn/wiki/<node_token>`。问题中提示：**必须是知识库中的多维表格链接**（/wiki/ 格式），不支持独立的多维表格（/base/ 格式）。如果还没有，请先在飞书知识库中创建多维表格。
- **数据表名称（可选）** — 在多维表格中创建的数据表名称。问题中提示：留空则使用多维表格自身的名称作为默认值。
- **凭证文件名（可选）** — 如果用户需要管理多个飞书应用，可指定凭证文件名（如 `team-a`）。问题中提示：留空则使用默认的 `credentials`。最终写入 `config/<名称>.json`。

> 提醒用户：需要在知识库中的多维表格上添加应用（"..." → "更多" → "添加文档应用"），并将权限设置为**"可管理"**（默认"可编辑"权限不足）

收集完成后，写入 `config/credentials.json`（如果用户指定了凭证文件名，则写入 `config/<用户指定的名称>.json`），然后执行配置：

**执行配置**

```bash
cd <SKILL_DIR> && node scripts/admin.js config-from-links config/credentials.json "<知识库多维表格链接>" ["<数据表名称>"]
```

成功后自动创建数据表、添加字段、创建任务文档根节点、写入配置。

如果报权限错误（`permission denied` / `RolePermNotAllow`），提示用户去多维表格中添加应用权限后重试。

**第三步：验证**

```bash
cd <SKILL_DIR> && echo "n" | node scripts/validate.js config/credentials.json
```

全部通过即配置完成。

## 可用命令

> 以下所有命令均需先 `cd <SKILL_DIR>`。

### 创建任务

```bash
node scripts/task-manager.js config/credentials.json create "<标题>" [type=值] [status=值] [url=值]
```

- 所有参数均为可选，调用者按需指定
- 创建后返回 `record_id`，可用于后续创建文档

### 创建文档

```bash
node scripts/task-manager.js config/credentials.json create-doc "<record_id>"
```

在知识库中按「{表名}-任务文档 → 年月 → 日期 → 任务名」层级创建文档，自动复用已有的月/日节点。

### 查看统计

```bash
node scripts/task-manager.js config/credentials.json list
```

### 验证配置

```bash
echo "n" | node scripts/validate.js config/credentials.json
```

## 管理命令

```bash
# 列出表格字段
node scripts/admin.js list-fields config/credentials.json

# 检查权限
node scripts/admin.js check-permissions config/credentials.json
```

## 故障排查

遇到错误时先查阅 FAQ.md，其中记录了实际调试中验证过的解决方案。

快速参考：

| 错误                                 | 原因                           | 解决                                           |
| ------------------------------------ | ------------------------------ | ---------------------------------------------- |
| 认证失败                             | app_id/app_secret 错误         | 检查凭证，确认是企业自建应用                   |
| permission denied / RolePermNotAllow | 应用未添加到多维表格或权限不足 | 在知识库的多维表格中添加应用，权限设为"可管理" |
| NOTEXIST (91402)                     | app_token 或 table_id 无效     | 重新运行 config-from-links                     |
| 链接格式不正确                       | 提供了独立多维表格链接         | 必须使用知识库中的多维表格链接（/wiki/ 格式）  |

更多问题详见 FAQ.md。
