# get-entry-tree

## 用途

返回当前用户可访问的FineBI目录树节点。
在多数时候，当用户意图检索仪表板名称的时候，已发布目录节点的text即等同于仪表板名称。
这个命令主要用于定位已发布的目录节点，并提取后续命令需要的 `templateId`。需要根据这个`templateId`才可以获取到真正的仪表板id

## CLI

优先使用关键字过滤：

```bash
finebi-cli get-entry-tree -k "<keyword>"
```

只有在用户没有提供任何看板名、目录名、栏目名或路径关键词，且确实需要浏览目录树时，才不带 `-k` 调用：

```bash
finebi-cli get-entry-tree
```

## 输入契约

- `keyword`：可选，但应尽量提供。用于按节点 `text` 过滤目录树，减少响应体大小。

## 返回契约

返回 `ToolResult<EntryTreeNode[]>`。

成功时类似：

```json
{
  "success": true,
  "data": [
    {
      "id": "node-id",
      "text": "display name",
      "path": "/path/to/node",
      "isParent": true,
      "templateId": "publish-task-id"
    }
  ]
}
```

## 重要字段

### 展示字段

- `text`：节点展示名称
- `path`：节点展示路径
- `fullParentName`：完整父级名称
- `parentNames`：父级名称链路

### 工作流字段

- `id`：当前入口节点 id
- `templateId`：该入口背后已发布主题的发布任务 id
- `isParent`：是否还有子节点

## 语义说明

- `get-entry-tree` 的无过滤响应可能很大。
- 当用户问题中包含看板名、目录名、栏目名、路径片段或其他可检索关键词时，必须优先带 `-k`。
- 如果关键词过滤没有命中，再换同义词、短关键词或路径片段重试；不要立刻拉取全量目录树。
- `templateId` 是这个命令最重要的工作流字段。
- 不要把 `templateId` 当成普通展示元数据。
- 如果下一步要查已发布主题资源，应把 `templateId` 作为 `get-published-subject-resources` 的输入。
- 不要把入口节点的 `id` 传给 `get-published-subject-resources`。

## 常见后续链路

1. 从用户问题中提取看板名、目录名、栏目名或路径关键词
2. 调用 `get-entry-tree -k "<keyword>"`
3. 通过 `text` 或 `path` 找到目标节点
4. 读取该节点的 `templateId`
5. 调用 `get-published-subject-resources -t <templateId>`

## 应该做

- 用 `text` 和 `path` 帮助用户识别正确节点
- 用 `templateId` 做下一步已发布资源查询
- 先用 `-k` 缩小目录树结果，再做候选匹配

## 不要做

- 不要猜测 `templateId`
- 不要在有关键词可用时直接调用无过滤的 `get-entry-tree`
- 不要在需要发布任务 id 的地方误用节点 `id`
- 不要把内部字段直接暴露给用户，除非它确实有助于后续流程
