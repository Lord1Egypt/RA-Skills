# 04_recall_context — 回忆与上下文组装

**层级：L1（执行层规格）**
**依据：** L0 core_essence/04_data_model_essence.md

---

## 一、Recall 在循环中的位置

Recall 只发生在 COGNIZE 步。

COGNIZE reducer 接收 OBSERVE 的 Observation，然后结合 State(t) 和从 Block Store 的 recall，产出 Context(t)。

```
Recall: (Observation, State(t), Block Store) → recall_items
```

## 二、Recall 规则

### 2.1 召回层级

Recall 分为三级，优先级从高到低：

| 层级 | 触发条件 | 召回范围 | 上限 |
|------|---------|---------|------|
| L1 - 精确 | Observation 的 hash 前缀匹配 Block 的 ID | 精确匹配 | 3 条 |
| L2 - 语义 | Observation 的 intent 标签匹配 Block 的 Label | 同类标签 | 5 条 |
| L3 - 上下文 | State.emotion 类似的 block | 相近情感 | 5 条 |

### 2.2 召回结果格式

```
recall_items: list of {
  block_id: str           # Block 的 UUID
  label: str              # Block.label
  importance: float       # [0.0, 1.0] 从 Block 读取
  similarity: float       # [0.0, 1.0] 由召回方法计算
  content_preview: str    # Block.content 的摘要（不超过 200 字符）
}
```

### 2.3 召回引用方向

同一轮迭代中的 recall 结果只用于构建当前 COGNIZE 步的 Context。不反向写回 State，不修改 Block Store。

## 三、Context 组装

COGNIZE reducer 将 Observation 与 recall_items 合并为 Context：

```
Context(t) = {
  observation: Observation,
  recall_items: list[RecallItem],
  state_snapshot: State(t),  # 只读副本
  context_bundle: str         # 组合后的上下文内容摘要
}
```

Context(t) 不会出现在循环外部（不出现在 API 响应中、不持久化）。

## 四、Recall 失败处理

| 失败类型 | 行为 |
|---------|------|
| 无 recall results（空列表） | Context 中 recall_items = []，state_snapshot 保持 |
| recall 超时 | 跳过 L2/L3，只用 L1 recall（如果有） |
| recall 部分失败 | 保留成功召回的部分，失败部分标记为 None |

## 五、不在本文件范围内

| 概念 | 所属位置 |
|------|---------|
| 语义相似度的具体计算方法 | L2 或实现层 |
| hash 前缀的匹配长度（当前 4 字符） | L1 配置项（可调整） |
| Block Store 的存储实现 | 实现层细节 |
| 情感类似 Block 的匹配规则 | L1 cognize_reducer |
