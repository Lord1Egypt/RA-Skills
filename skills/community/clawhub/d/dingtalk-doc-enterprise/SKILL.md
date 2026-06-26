---
name: dingtalk-doc-enterprise
description: 钉钉文档操作技能。仅在消息明确包含 `alidocs.dingtalk.com`、`钉钉文档`、`钉钉知识库`、`alidocs`，或当前上下文已明确对象是钉钉文档时使用。支持 read/blocks/update/append-text/delete 命令，不支持 create。
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires":
          {
            "bins": ["node"],
            "env": ["DINGTALK_CLIENTID", "DINGTALK_CLIENTSECRET"],
          },
      },
  }
---

# 钉钉文档企业版

使用同目录脚本 `doc-enterprise.js` 调用钉钉文档企业 API。OpenClaw 不会因为目录里存在 `.js` 文件就自动执行它；当任务命中本 skill 时，应按下面规则主动调用脚本。

## 何时使用

### 🔑 触发关键词

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

### ✅ 触发场景（优先级从高到低）

| 场景 | 示例 | 动作 |
|------|------|------|
| **钉钉文档链接** | `alidocs.dingtalk.com/i/nodes/xxx` | 自动识别，调用 `read` 或 `blocks` |
| **钉钉上下文 + 链接** | "总结 https://alidocs.dingtalk.com/..." | 根据意图选择命令 |
| **明确命令** | "总结这篇文档"、"读取这个 alidocs 链接" | 根据意图选择命令 |
| **已知上下文是钉钉文档** | 前文已给出 alidocs 链接，后续说"更新文档"、"删除某段" | 调用对应命令 |
| **结构查询** | "列出结构"、"这个 alidocs 有哪些章节" | 调用 `blocks` |

### ❌ 不触发的场景

- 创建新文档（脚本未实现 `create`）
- 没有文档链接、docKey、或明确钉钉文档上下文，却要求修改文档
- 用户只说“总结文档”“更新这个链接”等泛化请求，但上下文无法确认对象是钉钉文档
- 与钉钉无关的文档系统，例如本地 Markdown、飞书文档、语雀、Google Docs

---

## 🔑 链接识别规则

支持以下格式的钉钉文档链接：

```
https://alidocs.dingtalk.com/i/nodes/<docKey>
https://alidocs.dingtalk.com/i/nodes/<docKey>?utm_scene=person_space
https://alidocs.dingtalk.com/i/nodes/<docKey>?utm_scene=team_space
alidocs.dingtalk.com/i/nodes/<docKey>  （无 https）
```

脚本会自动提取 `<docKey>` 部分。

## 运行前提

必需环境变量：

- `DINGTALK_CLIENTID`
- `DINGTALK_CLIENTSECRET`

可选环境变量：

- `DINGTALK_OPERATOR_ID`：默认操作人 unionId
- `OPENCLAW_SENDER_ID`：由 OpenClaw/连接器注入，用于自动识别当前发送者
- `OPENCLAW_SENDER_NAME`

脚本优先使用 `DINGTALK_OPERATOR_ID`。若未设置，则尝试使用 `OPENCLAW_SENDER_ID` 查询 unionId。

## 执行入口

脚本文件：`doc-enterprise.js`

执行时使用绝对路径，形式如下：

```bash
node /absolute/path/to/doc-enterprise.js <command> [args]
```

当本 skill 引用了相对路径文件时，将其相对于 `SKILL.md` 所在目录解析成绝对路径后再执行。

## 命令映射

### 1. 读取文档概览

适用：

- 用户只说“读取这篇文档”
- 用户贴了一个文档链接，想先快速看内容概况

执行：

```bash
node /absolute/path/to/doc-enterprise.js read <docKey-or-url>
```

说明：

- `read` 只输出块列表和部分预览文本
- 适合快速探测，不适合直接拿来做高质量总结

### 2. 获取完整结构或用于总结

适用：

- 用户要求“总结这篇文档”
- 用户要求“列出结构”
- 后续操作需要 `blockId`

执行：

```bash
node /absolute/path/to/doc-enterprise.js blocks <docKey-or-url>
```

说明：

- 优先用 `blocks` 获取更完整的块结构
- 做总结前，先读取 `blocks` 的结果，再基于结果总结
- 删除或追加前，如果用户没有给出 `blockId`，先运行 `blocks`

### 3. 覆写整篇文档

适用：

- 用户明确要求“更新整篇文档”
- 用户给出了新的 Markdown 内容

执行：

```bash
node /absolute/path/to/doc-enterprise.js update <docKey-or-url> <markdown>
```

说明：

- 这是整篇覆写，不是局部编辑
- 若用户只是想在末尾补一段，不要用 `update`

### 4. 追加文本到段落块

适用：

- 用户要求在某个已知段落块后追加文本
- 已经拿到了目标 `blockId`

执行：

```bash
node /absolute/path/to/doc-enterprise.js append-text <docKey-or-url> <blockId> <text>
```

说明：

- 如果没有 `blockId`，先运行 `blocks`
- 仅在目标块确实是段落块时使用
- “没有 `blockId`” 不代表不触发本 skill，而是先查结构再执行追加

### 5. 删除块元素

适用：

- 用户明确要求删除某一段或某个块
- 已经拿到了目标 `blockId`

执行：

```bash
node /absolute/path/to/doc-enterprise.js delete <docKey-or-url> <blockId>
```

说明：

- 删除前先确认目标块，避免误删
- 如果用户说“删除第 3 段”，先运行 `blocks` 找到对应 `blockId`
- “没有 `blockId`” 不代表不触发本 skill，而是先查结构再执行删除

## 工作流程

1. 从用户消息中提取文档链接或 docKey。
2. 先确认对象确实是钉钉文档，再判断是读取、总结、列结构、覆写、追加，还是删除。
3. 需要 `blockId` 时，先运行 `blocks`。
4. 读取概览用 `read`；做总结或定位块时优先用 `blocks`。
5. 执行脚本后，把结果用自然语言返回给用户。

## 错误处理

若脚本报以下错误，按对应方式处理：

- 缺少 `DINGTALK_CLIENTID` 或 `DINGTALK_CLIENTSECRET`：提示未配置钉钉应用凭证
- 缺少 `operatorId`：提示配置 `DINGTALK_OPERATOR_ID`，或确认连接器是否传入 `OPENCLAW_SENDER_ID`
- `forbidden.accessDenied`：提示当前用户对该文档无权限
- `docNotExist`：提示文档不存在，检查链接或 docKey
- `blockNotExist`：提示块不存在，先重新运行 `blocks` 核对
- `paramError`：提示参数格式错误，优先检查链接与文档 ID

## 限制

- 当前脚本未实现创建文档，不要承诺或尝试 `create`
- `read` 只适合概览，不足以替代完整正文提取
- 追加和删除依赖 `blockId`
- 覆写会直接替换整篇文档内容

## 参考

- 背景说明与人工阅读材料：`README.md`
- 实际执行脚本：`doc-enterprise.js`
