# 数据集查找与预览流程

## 目标

按正确顺序查找数据集，并预览数据集记录。

这个流程用于用户想定位某个数据集，并查看字段结构或样例数据的场景。

## 适用场景

当用户提出以下需求时使用：

- 查找某个数据集
- 按名称搜索数据集
- 预览数据集数据
- 查看字段结构
- 浏览样例记录

## 必要命令

- `search-my-datasets`
- `search-public-dataset`
- `preview-dataset-data`

## 流程

### 第 1 步：先查“我的分析”

调用：

```bash
finebi-cli search-my-datasets -k "<keyword>" -p 1
```

这应该是默认第一步。

预期结果：

- 来自“我的分析”的候选数据集

### 第 2 步：必要时再查公共目录

如果“我的分析”里没有找到目标数据集，再调用：

```bash
finebi-cli search-public-dataset -k "<keyword>" -p 1 -s 150
```

预期结果：

- 来自公共数据目录的候选数据集

### 第 3 步：确定数据集标识

从选中的结果里保留：

- 作为 `tableName` 使用的数据集标识
- 向用户解释时需要的展示字段

如果有多个候选：

- 展示名称
- 请用户确认正确的数据集

### 第 4 步：预览数据

调用：

```bash
finebi-cli preview-dataset-data -t <tableName> -p 1
```

预期结果：

- 字段元数据
- 样例记录
- 分页相关信息

### 第 5 步：需要时继续翻页

如果用户想看更多记录，保持相同的 `tableName`，只增加页码：

```bash
finebi-cli preview-dataset-data -t <tableName> -p 2
```

按需要继续增加 `pageIndex`。

## 常见错误

### 错误 1：跳过“我的分析”

不要默认一开始就用 `search-public-dataset`。

正确顺序：

```text
search-my-datasets
-> 如果没找到，再 search-public-dataset
-> preview-dataset-data
```

### 错误 2：还没确定数据集就直接预览

在拿到明确的 `tableName` 之前，不要调用 `preview-dataset-data`。

### 错误 3：翻页时换了数据集

分页预览时：

- 保持相同的 `tableName`
- 只改变 `pageIndex`

## 推荐行为

1. 先查“我的分析”。
2. 只有必要时才回退到公共目录。
3. 把选中的数据集标识保留为 `tableName`。
4. 用预览结果解释字段和样例记录。
5. 继续浏览时只调整 `pageIndex`。

## 简写版本

```text
search-my-datasets
-> 如果没找到，再 search-public-dataset
-> 确定 tableName
-> preview-dataset-data(tableName, pageIndex=1)
-> preview-dataset-data(tableName, pageIndex=2...)
```
