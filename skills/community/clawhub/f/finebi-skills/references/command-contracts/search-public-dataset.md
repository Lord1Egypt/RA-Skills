# search-public-dataset

## 用途

按关键字搜索公共数据目录中的 FineBI 数据集。

这个命令是 `search-my-datasets` 之后的回退步骤，用于“我的分析”里没有找到目标数据集时继续在公共目录中查找。

## CLI

```bash
finebi-cli search-public-dataset -k "<keyword>" -p 1 -s 150
```

## 输入契约

- `keyword`：数据集搜索关键字
- `pageIndex`：结果页码
- `pageSize`：结果页大小

## 返回契约

这个命令返回一个 `ToolResult<any>`，其中包含原始公共数据集搜索结果。

具体结构会因 FineBI 版本不同而变化，但应当把它视作候选数据集列表。

## 重要字段

### 展示字段

- 数据集名称字段，如 `name`、`text` 或等价标题字段
- 描述类字段

### 工作流字段

- 后续传给 `preview-dataset-data` 的数据集标识，也就是 `tableName`
- 用于区分候选数据集的内部标识

## 语义说明

- 不要把这个命令当成默认第一步。
- 查数据集时应优先调用 `search-my-datasets`，只有没找到时再调用 `search-public-dataset`。
- 这个命令最重要的输出是后续 `preview-dataset-data` 所需的数据集标识。
- 在很多 FineBI 返回里，数据集的名称类字段也可能就是表标识。当前仓库工作流默认会把选中的数据集 id 或名称传给 `preview-dataset-data` 作为 `tableName`。
- 如果有多个候选，应基于展示字段请用户确认，再保留被选中的工作流标识。

## 常见后续链路

1. 调用 `search-my-datasets`
2. 如果没找到，再调用 `search-public-dataset`
3. 找到正确的公共数据集候选
4. 提取作为 `tableName` 使用的数据集标识
5. 调用 `preview-dataset-data -t <tableName>`

## 应该做

- 把这个命令作为公共目录回退步骤
- 用搜索结果缩小到唯一候选
- 请用户消歧时，优先展示名称和描述

## 不要做

- 当“我的分析”应先检查时，不要直接从这个命令开始
- 在没有明确数据集标识时，不要直接预览
- 如果有多个近似结果，不要默认第一个就是正确的
