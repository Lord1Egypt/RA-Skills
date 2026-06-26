# 状态剪枝规范（State Pruning Spec — v4.1 新增）

> 解决 S 级问题中 ToT 多路径 + 多 Agent 导致的上下文膨胀问题

---

## 问题背景

S 级问题走 ToT 3 条推理路径（每条 ~10K tokens）+ 5 个领域 Agent 中间结果（每个 ~5K tokens），总计 50K+ tokens。这会触发：
- **Lost in the Middle** 现象：大模型对中间位置的信息注意力显著下降
- **Step 6 综合质量崩盘**：输入过长导致综合时遗漏关键发现、混淆不同路径的结论

## 方案

在 Step 5 → Step 6 之间插入 **Summarizer**，将原始推理压缩为核心断言集。

## 压缩规则

### ToT 路径压缩

每条推理路径压缩为以下结构：

```
[路径名] 断言集：
  断言 1: [结论性语句，≤30 字]
    - 证据: [数据/条款号/关键事实]
    - 置信度: [高/中/低]
  断言 2: ...
  断言 3: ...
```

**最多 3 个断言/路径**，超过的优先级最低的断言丢弃。

### 领域 Agent 压缩

每个领域 Agent 输出压缩为：

```
[Agent 名] 核心发现：
  发现 1: [结论性语句，≤30 字]
    - 证据: [数据/条款号/关键事实]
    - 置信度: [高/中/低]
  发现 2: ...
```

**最多 2 个发现/Agent**，超过的优先级最低的发丢弃。

### 辩论结果压缩

交叉辩论的结果压缩为：

```
辩论结果：
  共识: [1 句话概括]
  分歧: [Agent A 认为 X vs Agent B 认为 Y，1 句话]
  盲点: [1 句话]
```

### 总长度限制

剪枝后总输出 **≤ 3K tokens**（约 1500 汉字）。

## 禁止行为

- ❌ 将 ToT 原始推理日志传递到 Step 6
- ❌ 将 Agent 辩论全文传递到 Step 6
- ❌ 保留推理过程、中间试探、自我质疑等过程性内容
- ❌ 压缩后超过 3K tokens

## DiagnosisState 字段

| 字段 | 写入者 | 说明 |
|------|--------|------|
| `tot_paths_raw` | Step 2-5 | 完整原始推理（仅存储，不传递） |
| `step5_assertions` | Summarizer | 压缩后的断言集（Step 6 的唯一输入） |
| `pruning_applied` | Summarizer | 是否执行了剪枝（true/false） |

## 执行流程

```
Step 5 完成
    ↓
检查是否触发 S 级
    ├── 是 → 执行 Summarizer → 写入 step5_assertions → 标记 pruning_applied=true
    └── 否 → 直接使用 Step 5 输出作为 Step 6 输入 → 标记 pruning_applied=false
    ↓
Step 6 读取 step5_assertions（S 级）或 Step 5 输出（A/B 级）
```
