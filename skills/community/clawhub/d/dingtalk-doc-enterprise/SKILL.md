---
name: dingtalk-doc-enterprise
description: 操作用户通过 URL 指定且有权限访问的已有钉钉文档。仅在消息明确包含 `alidocs.dingtalk.com`、`钉钉文档`、`钉钉知识库`、`alidocs`，或当前上下文已确认对象是钉钉文档时使用。支持读取、覆写，以及插入、修改、删除文档内容块；严禁创建文档，包括空白文档。
metadata: {"openclaw":{"emoji":"📄","requires":{"bins":["node"],"env":["DINGTALK_CLIENTID","DINGTALK_CLIENTSECRET"]}}}
---

# 钉钉文档企业版

使用同目录的 `doc-enterprise.js` 操作用户通过 URL 指定的已有钉钉文档。

## 能力边界

- 只操作已有文档；只接受钉钉文档 URL 或明确的 docKey。
- 允许读取、整篇覆写，以及插入、修改、删除内容块。
- `insert` 是向已有文档插入内容块，属于修改文档，不是创建文档。
- `delete` 是删除内容块，不删除文档实体。
- 不列出或搜索用户的文档。
- 严禁创建文档，包括空白文档；也不得创建知识库、文件夹或文档副本。
- 不得自行拼接、调用或建议任何未在“命令映射”中列出的创建接口。
- 用户要求创建或新建时，直接说明本 skill 不支持，不要用其他命令模拟创建。

## 身份和权限

必需环境变量：

- `DINGTALK_CLIENTID`
- `DINGTALK_CLIENTSECRET`

线上身份按以下优先级解析：

1. `OPENCLAW_SENDER_ID`
2. `DINGTALK_SENDER_ID`
3. `DINGTALK_OPERATOR_ID`，仅作为本地调试回退；线上不要配置

将 sender_id 查询为 unionId，并将其作为 API 的 `operatorId`。钉钉 API 依据当前用户对目标文档的实际权限决定操作是否成功；不要把“可以读取”解释为“必然可以修改或删除”。

## 执行入口

将相对路径按 `SKILL.md` 所在目录解析，并使用脚本绝对路径：

```bash
node /absolute/path/to/doc-enterprise.js <command> [args]
```

支持以下链接形式：

```text
https://alidocs.dingtalk.com/i/nodes/<docKey>
https://alidocs.dingtalk.com/i/nodes/<docKey>?utm_scene=person_space
alidocs.dingtalk.com/i/nodes/<docKey>
```

## 命令映射

### 读取概览

```bash
node /absolute/path/to/doc-enterprise.js read <docKey-or-url>
```

只在用户要求快速查看时使用。需要总结、定位内容块或执行块级操作时使用 `blocks`。

### 获取完整块结构

```bash
node /absolute/path/to/doc-enterprise.js blocks <docKey-or-url>
```

用于总结正文、获取 `blockId`/`id` 和 `position`/`index`，以及在修改或删除前确认目标。

### 覆写整篇内容

```bash
node /absolute/path/to/doc-enterprise.js update <docKey-or-url> <markdown>
```

仅在用户明确要求替换整篇内容，并且新内容完整明确时使用。此操作会替换已有正文。

### 插入段落块

```bash
node /absolute/path/to/doc-enterprise.js insert <docKey-or-url> <position> <text>
```

- `position` 必须是大于或等于 0 的整数。
- 用户要求“追加一段”时，先运行 `blocks` 确认末尾位置，再插入新的段落块。
- 不要调用 `paragraphs/{blockId}/text` 的 append-text 接口。

### 修改段落块

```bash
node /absolute/path/to/doc-enterprise.js modify <docKey-or-url> <blockId> <text>
```

先运行 `blocks`，确认目标是段落块且 `blockId` 正确。该命令用新文本替换目标段落块。

### 删除内容块

```bash
node /absolute/path/to/doc-enterprise.js delete <docKey-or-url> <blockId>
```

- 用户说“删除第 3 段”时，先运行 `blocks` 定位并确认第 3 段，再删除对应内容块。
- 用户要求清空内容时，先运行 `blocks`，逐个删除可删除的正文块；不要删除文档实体，也不要创建空白文档替换原文档。
- 目标存在歧义时，先向用户确认，不要猜测 blockId。

## 工作流程

1. 从当前消息或已确认的上下文提取钉钉文档 URL/docKey。
2. 拒绝任何创建文档、空白文档、知识库、文件夹或副本的请求。
3. 读取概览用 `read`；总结、定位、修改或删除前用 `blocks`。
4. 根据意图只调用 `update`、`insert`、`modify` 或 `delete`。
5. 对覆写和删除操作复述目标；目标不明确时先确认。
6. 返回实际执行结果，不把 API 拒绝描述成操作成功。

## 错误处理

- 缺少应用凭证：提示配置 `DINGTALK_CLIENTID` 和 `DINGTALK_CLIENTSECRET`。
- 缺少当前用户身份：检查连接器是否传入 `OPENCLAW_SENDER_ID`；仅本地调试时使用 `DINGTALK_OPERATOR_ID`。
- `forbidden.accessDenied`：说明当前用户没有执行该操作所需的文档权限，或应用缺少相应权限。
- `docNotExist` / `nodeNotExist`：检查 URL/docKey，说明文档不存在或标识不正确。
- `blockNotExist`：重新运行 `blocks` 并核对内容块 ID。
- `paramError`：优先检查 URL/docKey、blockId 和 position。

## 参考

- 人工配置与能力说明：`README.md`
- 执行脚本：`doc-enterprise.js`
