# get-published-subject-resources

## 用途

返回某个已发布分析主题对外暴露的资源。

这个命令通常在 `get-entry-tree` 之后调用，输入使用选中节点的 `templateId`。

## CLI

```bash
finebi-cli get-published-subject-resources -t <publishTaskId>
```

## 输入契约

- `taskId`：已发布主题的 `templateId`，也就是 `publishTaskId`

## 返回契约

返回 `ToolResult<PublishedSubjectResource>`。

成功时类似：

```json
{
  "success": true,
  "data": {
    "id": "resource-group-id",
    "name": "resource-group-name",
    "resourceList": [
      {
        "id": "resource-id",
        "name": "resource-name",
        "itemType": 1,
        "tableType": 1
      }
    ]
  }
}
```

## 重要字段

### 展示字段

- `name`：资源包名称
- `resourceList[].name`：资源展示名称

### 工作流字段

- `id`：资源包 id
- `resourceList[].id`：后续资源动作需要的资源 id
- `resourceList[].itemType`：资源类别
- `resourceList[].tableType`：资源子类型

## 语义说明

- 这个命令的输入应来自 `get-entry-tree.data[].templateId`。
- 返回结果不是入口节点本身，而是该入口背后的已发布资源包。
- `resourceList[].id` 通常是后续资源动作最关键的工作流字段。

## 常见后续链路

1. 调用 `get-entry-tree`
2. 选择正确节点
3. 读取 `templateId`
4. 调用 `get-published-subject-resources`
5. 检查 `resourceList[]` 决定下一步动作

## 应该做

- 同时保留资源包级别的 `id` 和每个 `resourceList[].id`
- 向用户解释时优先展示 `name`

## 不要做

- 不要把入口节点 `id` 当成 `taskId`
- 不要默认 `resourceList` 里的所有资源都能走同一种后续处理
