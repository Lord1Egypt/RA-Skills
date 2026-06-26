# KB 新建与结构操作

从这个技能执行命令时，把下面的 `kb ...` 命令字符串整体传给 `./scripts/kb_execute.py`，例如：`./scripts/kb_execute.py "kb write --name repo/path.md --content '<h1>Title</h1>'"`。如果正文 HTML 很长或包含复杂转义，优先把完整命令写入本地 UTF-8 文本文件，再通过 `--command-file` 发送。

当你需要新建文档、新建目录、移动内容、删除内容或发布内容时，读这个文件。

## 工作流

1. 先确认仓库、路径和目标对象。
2. 涉及已有文档时，先读当前内容再决定操作。
3. 选择能满足需求的最小变更。
4. 删除、移动、发布都按“用户明确要求才执行”处理。
5. 如果最终答复需要指向结果文档，再补 `kb render`。

## 共享规则

- `kb write` 只负责新建，不负责覆盖。
- 通过 `kb write` 写入的正文必须是 HTML。
- 用户要求 `.pdf`、`.xlsx`、`.docx` 等不可直接编辑格式时，先读取原内容作参考，再创建语义等价的 `.md`，正文用 HTML 表达；只有工具明确支持原格式编辑时，才直接改原文件。
- 如果目标可能已存在，先用读取类命令确认。
- 如果目标不唯一，不要猜，先确认。

## 命令卡片

### `kb write`

用于创建新文档。

- 常用写法：
  - `kb write --name <repo/path.md> --content '<html...>'`
  - `kb write --repo-code <code> --path <path.md> --content '<html...>'`
- 使用要求：
  - 只在确认目标文档不存在时使用。
  - 直接写 HTML，不要先写 Markdown 再转换。
  - 表格类内容使用 HTML 表格标签。
- 示例：

```text
kb write --name team-workspace/reports/q1-summary.md --content '<h1>Q1 Summary</h1><table><thead><tr><th>Region</th><th>Amount</th></tr></thead><tbody><tr><td>CN</td><td>120</td></tr></tbody></table>' --status publish
```

### `kb mkdir`

用于按需创建目录。

- 常用写法：
  - `kb mkdir <repo/dir/>`
  - `kb mkdir --repo-code <code> --path <dir/>`
- 常用参数：
  - `--parents`
  - `--exist-ok true|false`
- 示例：

```text
kb mkdir --repo-code TEAM_DOCS --path reports/2026/ --parents
```
### kb cp

用于复制知识库对象到目标位置。只有用户明确要求“复制/拷贝”时才使用。

- 常用写法：
    - `kb cp --from <repo/src.md> --to <repo/dst.md>`
    - `kb cp --doc-code <DOC_CODE> --to <repo/dst.md>`
    - `kb cp --from <repo/src_dir/> --to <repo/dst_dir/> --recursive true`
- 常用参数：
    - `--from <repo/path>`：按知识库路径指定复制源
    - `--doc-code <DOC_CODE>`：按元素编码指定复制源
    - `--to <repo/path>`：目标路径，必填
    - `--recursive true|false`：复制目录时是否连同子内容一起复制；默认 false
- 行为语义：
    - 复制不会删除或移动源对象。
    - 目标路径中的父目录不存在时，会自动补建目录。
    - 复制普通对象成功后，目标对象通常会生成新的 code。
    - 返回结果里的 type 目前是 element 或 directory。
- 限制与冲突策略：
    - 必须二选一提供 `--from` 或 `--doc-code`，不能同时传，也不能都不传。
    - 目录复制建议显式传 --recursive true。

示例：

```text
kb cp --doc-code DOC_12345 --to team-workspace/reports/q1-summary-copy.md

kb cp --from team-workspace/project-a/ --to archive/project-a/ --recursive true

```

### `kb mv`

用于移动或重命名文档、目录。只有用户明确要求时才使用。

- 常用写法：
  - `kb mv --from <src> --to <dst>`
  - `kb mv --doc-code <code> --to <dst>`
- 使用要求：
  - 执行前确认源和目标。
  - 不要把 `mv` 当成“修改内容”的替代品。
- 示例：

```text
kb mv --doc-code DOC_12345 --to team-workspace/archive/q1-summary.md
```

### `kb rm`

用于删除文档或空目录。只有用户明确要求时才使用。

- 常用写法：
  - `kb rm <repo/path.md>`
  - `kb rm --doc-code <code>`
- 使用要求：
  - 删除是高风险操作，必须确认目标无误。
  - 不要把“清理一下”“整理一下”自动理解成删除。
- 示例：

```text
kb rm --doc-code DOC_12345
```

### `kb publish`

用于发布文档，使内容生效。只有用户明确要求发布时才使用。

- 常用写法：
  - `kb publish --doc-code <code>`
  - `kb publish --name <repo/path.md>`
- 使用要求：
  - 不要默认发布。
  - 如果前面的写入或修改失败，先重新确认状态，再决定是否发布。
- 示例：

```text
kb publish --doc-code DOC_12345
```

## 不在本文件覆盖的内容

- 查找仓库和读取文档
- 基于 patch 的精确修改

读取类操作看 [read.md](./read.md)，精确修改看 [update.md](./update.md)。
