# 仪表板 ID 解析流程

## 目标

在任何需要 `dashboardId` 的工作流里，先用正确来源解析出仪表板 id，再继续后续动作。

## 核心原则

- 不要把用户输入的名称直接当成 `dashboardId`。
- 优先从挂出目录或已发布入口查找仪表板。
- 挂出目录没有命中或不能唯一命中时，再从“我的分析”查找。
- 如果两条链路都有候选，展示候选并请用户确认。

## 两条来源链路

### 来源一：挂出目录或已发布入口

无论用户是否明确说明来源，都先走这条链路。用户提到以下信号时，更必须优先走这条链路：

- 挂出
- 发布
- 目录
- 门户
- 入口
- 节点
- 路径
- 某个栏目下的看板

推荐流程：

```text
从用户问题提取看板名/目录名/栏目名/路径关键词
-> get-entry-tree -k <keyword>
-> 按 text/path 匹配目标节点
-> 读取 templateId
-> get-published-subject-resources(templateId)
-> 在 resourceList 中定位 dashboard 资源
-> 解析 dashboardId
```

注意：

- `get-entry-tree` 响应可能很大；有关键词时必须先带 `-k` 过滤
- 关键词可来自看板名、目录名、栏目名、路径片段或用户问题里的业务词
- 如果关键词过滤没有命中，先换短关键词或同义词重试，再考虑无过滤调用
- `get-entry-tree` 本身不等于已经拿到 `dashboardId`
- 它首先解决的是“挂出节点定位”
- 后续通常还要经过 `templateId -> published resources` 这条链路

### 来源二：我的分析中的仪表板

默认顺序中，只有挂出目录链路没有命中或不能唯一命中时，才走这条链路。若用户明确限定“只查我的分析”，可以直接走这条链路：

- 我的分析
- 我做的看板
- 我自己的 dashboard
- 我这边有个看板
- 直接按看板名找

推荐流程：

```text
search-my-dashboards
-> 按名称匹配候选 dashboard
-> 读取 reportId
```

## 默认策略

如果用户没有明确说来源：

1. 先从用户问题中提取关键词，调用 `get-entry-tree -k "<keyword>"`，在挂出目录或已发布入口中匹配看板。
2. 如果目录候选唯一，继续 `get-published-subject-resources` 并解析 `dashboardId`。
3. 如果目录没有命中，先换短关键词或同义词重试；仍未命中再调用 `search-my-dashboards` 查“我的分析”。
4. 如果目录和“我的分析”都有候选，展示来源、名称和 id 字段，请用户确认。
5. 如果两条链路都不能唯一命中，再询问用户更准确的看板名或来源。

## 常见错误

### 错误 1：把用户输入名称直接当成 `dashboardId`

错误做法：

```text
用户说了看板名 -> 直接当成 dashboardId
```

正确做法：

```text
先查挂出目录 -> 未唯一命中再查我的分析 -> 解析 dashboardId
```

### 错误 2：来源不明确时直接搜我的分析

默认先查挂出目录。只有挂出目录没有唯一命中，才继续查“我的分析”。

### 错误 3：把 `get-entry-tree` 结果直接当成 dashboard 列表

`get-entry-tree` 返回的是入口节点，不是 dashboard 列表。

### 错误 4：有关键词时拉取全量目录树

不要在用户已经给出看板名、目录名或路径线索时直接调用无过滤的 `get-entry-tree`。

正确做法：

```text
提取关键词 -> get-entry-tree -k <keyword> -> 再匹配 text/path
```

## 推荐行为

1. 所有需要 `dashboardId` 的流程，先套用这份解析规则。
2. 先保留展示字段，再保留工作流字段。
3. 目录来源优先保留 `text`、`path`、`templateId`。
4. 我的分析来源优先保留 `name`、`reportId`。

## 简写版本

```text
需要 dashboardId
-> 先查挂出目录: get-entry-tree -k <keyword> -> templateId -> published resources -> dashboardId
-> 未唯一命中再查我的分析: search-my-dashboards -> reportId
-> 两边都有候选或都不唯一: 展示候选并消歧
```
