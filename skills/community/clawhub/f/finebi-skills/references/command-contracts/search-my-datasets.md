# search-my-datasets

## 用途

在“我的分析”中搜索数据集。

当用户要查找某个自己创建、维护或最近常用的数据集时，应把这个命令视为第一步。

## CLI

```bash
finebi-cli search-my-datasets -k "<keyword>" -p 1
```

## 输入契约

- `keyword`：数据集搜索关键字
- `pageIndex`：结果页码
- `searchType`：搜索类型，CLI 默认值是 `3`
- `filterType`：过滤类型，CLI 默认值是 `1`

## 返回契约

返回 `ToolResult<any>`，其中包含 FineBI “我的分析”搜索接口返回的原始载荷。

具体结构会因 FineBI 版本不同而变化。

## 重要字段

### 展示字段

- 数据集展示名称，如 `name`、`text` 或等价标题字段
- 文件夹或路径类字段

### 工作流字段

- 后续传给 `preview-dataset-data` 的数据集标识
- 用于区分候选数据集的内部标识

## 语义说明

- 查数据集时应优先使用这个命令，而不是先走 `search-public-dataset`。
- 这个命令只搜索“我的分析”，不搜索公共数据目录。
- 如果这里没有找到目标数据集，再回退到 `search-public-dataset`。

## 常见后续链路

1. 调用 `search-my-datasets`
2. 如果找到了目标数据集，提取可作为 `tableName` 的标识
3. 调用 `preview-dataset-data -t <tableName>`
4. 如果没找到，再回退到 `search-public-dataset`

## 应该做

- 把这个命令作为数据集查找的默认第一步
- 如果有多个候选，使用展示字段帮助用户消歧

## 不要做

- 当用户意图是“我的数据集”时，不要直接跳到 `search-public-dataset`
- 在没有明确数据集标识时，不要直接预览
