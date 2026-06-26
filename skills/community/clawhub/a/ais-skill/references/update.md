# KB Patch 修改指南

从这个技能执行命令时，把下面的 `kb ...` 命令字符串整体传给 `./scripts/kb_execute.py`。如果命令本身包含多行 patch，优先把完整命令写入本地 UTF-8 文本文件，再通过 `--command-file` 发送，避免 shell 转义破坏 patch 正文。

当你需要通过 `kb edit --patch` 对现有文档做精确修改时，读这个文件。

## 工作流

1. 先把目标定位到唯一文档；一旦拿到 `code`，优先使用 `code`。
2. 用 `kb cat` 读取当前内容。
3. 只编写满足需求的最小 patch。
4. 每次 patch 只做一个文件操作。
5. 如果最终答复需要指向该文档，结束前再补 `kb render`。

## 共享规则

- 修改现有文档时默认使用 `Update File`。
- 新建文档只有在确实需要 patch 语义时才用 `Add File`；普通新建优先用 `kb write`。
- patch 中新增或替换的正文必须是 HTML，并与 `kb cat` 返回结构保持一致。
- 如果目标是 `.pdf`、`.xlsx`、`.docx` 等不可直接编辑格式，默认不要对原文件打 patch；先读取内容作参考，再创建语义等价的 `.md` 文档，除非工具明确支持原格式编辑。
- patch 不负责删除和移动。
- 能局部改就局部改，不要默认整篇重写。

## Patch 基本形状

每个 patch 必须包含：

1. `*** Begin Patch`
2. 且只包含一个文件操作头
3. patch body
4. `*** End Patch`

允许的文件操作头：

- `*** Update File --name: <repo/path.md>`
- `*** Update File --code: <doc_code>`
- `*** Add File --name: <repo/path.md>`
- `*** Add File --code: <repo_or_code_path/new.md>`

禁止的操作：

- `*** Delete File ...`
- `*** Move to ...`

## Update 规则

- 第一个 chunk 可以省略 `@@`，第二个及后续 chunk 必须显式写 `@@`。
- 上下文要尽量稳定，保证 patch 能唯一匹配。
- patch 内容不会自动 trim；需要保留空格时就原样保留。
- 如果按路径定位可能重名，先把文档 `code` 找出来再改。

最小示例：

```text
./scripts/kb_execute.py --command-file /tmp/kb-patch.txt
```

多 chunk 示例：

```text
kb edit --patch
*** Begin Patch
*** Update File --code: DOC_12345
@@ intro
-<p>旧介绍</p>
+<p>新介绍</p>

@@ footer
-<p>旧结尾</p>
+<p>新结尾</p>
*** End Patch
```

## Add 规则

- `Add File` 之后的每一行都必须以 `+` 开头。
- 空行也必须写成 `+`。
- 新增内容必须是合法的 HTML 正文。

示例：

```text
kb edit --patch
*** Begin Patch
*** Add File --name: team-workspace/docs/process/new-guideline.md
+<h1>New Guideline</h1>
+
+<p>First version.</p>
*** End Patch
```

## 失败处理

- patch 失败后，不要假设有任何 hunk 已经生效。
- 重试前先重新读取当前文档。
- 如果目标不唯一，或者文档内容已经漂移，先重新定位，不要猜。

## 不在本文件覆盖的内容

- 查找仓库和读取文档
- 普通新建、建目录、移动、删除、发布

读取类操作看 [read.md](./read.md)，普通结构操作看 [write.md](./write.md)。
