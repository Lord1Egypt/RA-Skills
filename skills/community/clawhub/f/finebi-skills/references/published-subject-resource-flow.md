# 已发布主题资源流程

## 目标

找到某个已发布分析主题对外暴露的资源。

这个流程用于用户想知道某个目录节点背后实际发布了哪些资源的场景。

## 适用场景

当用户提出以下需求时使用：

- 查看某个目录节点下的资源
- 查看已发布主题资源
- 查看某个入口背后的 dashboard、widget 或资源包
- 确认某个已发布目录节点指向什么

## 必要命令

- `get-entry-tree`
- `get-published-subject-resources`

## 流程

### 第 1 步：读取入口树

优先从用户问题中提取目录名、栏目名、看板名或路径关键词，并带 `-k` 调用：

```bash
finebi-cli get-entry-tree -k "<keyword>"
```

只有没有任何可用关键词、且确实需要浏览目录树时，才调用：

```bash
finebi-cli get-entry-tree
```

预期结果：

- 当前用户可访问的入口节点列表

识别节点时优先使用：

- `text`
- `path`
- `fullParentName`

### 第 2 步：选择目标节点

找到与用户意图匹配的目录或已发布入口。

如果关键词过滤没有命中：

- 先换短关键词、同义词或路径片段重试。
- 不要马上拉取全量目录树。

如果存在多个近似候选：

- 展示 `text` 和 `path`
- 请用户确认

### 第 3 步：读取 `templateId`

从选中的节点上读取：

- `templateId`

这是下一步最关键的工作流字段。

### 第 4 步：读取已发布主题资源

调用：

```bash
finebi-cli get-published-subject-resources -t <templateId>
```

预期结果：

- 该入口背后的已发布资源包
- 一个可供后续动作使用的 `resourceList[]`

## 输出解释

### 用户展示字段

- 资源包 `name`
- `resourceList[].name`

### 工作流字段

- 资源包 `id`
- `resourceList[].id`
- `resourceList[].itemType`
- `resourceList[].tableType`

## 常见错误

### 错误 1：把入口节点 `id` 当成 `templateId`

不要这样做：

```text
get-entry-tree -> selectedNode.id -> get-published-subject-resources
```

正确流程：

```text
get-entry-tree -k <keyword> -> selectedNode.templateId -> get-published-subject-resources
```

### 错误 2：把 `templateId` 当成普通展示字段

`templateId` 不是普通元数据。

它就是下一条命令需要的发布任务 id。

### 错误 3：跳过消歧

如果有多个节点都像目标，不要猜测。

应基于 `text` 和 `path` 请用户确认。

### 错误 4：默认拉取全量目录树

`get-entry-tree` 的无过滤响应可能很大。用户提供了任何名称或路径线索时，应优先使用 `-k`。

## 推荐行为

1. 先确定入口节点。
2. 同时保留展示字段和工作流字段。
3. 下游查询必须使用 `templateId`。
4. 用 `resourceList[].name` 向用户解释结果。
5. 保留 `resourceList[].id` 供后续动作使用。

## 简写版本

```text
get-entry-tree -k <keyword>
-> 按 text/path 选节点
-> 读取 templateId
-> get-published-subject-resources(templateId)
-> 检查 resourceList
```
