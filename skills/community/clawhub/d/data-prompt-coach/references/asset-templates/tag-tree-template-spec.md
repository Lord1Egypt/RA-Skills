# JSON 标签树模板规格

> 适用场景：5 批量分类标注
> 配套方法论：M5（两级标签体系）+ M6（分批处理，>1000 条时）+ M2（防幻觉三招）

## 触发场景

仅场景 5 使用。用户提交标签体系后或让 AI 协助设计标签树时，按此规格输出。

## 模板结构（JSON）

```json
{
  "version": "1.0",
  "tag_system_name": "{标签体系名称}",
  "created_at": "{日期}",
  "description": "{体系用途说明}",
  "level_1_tags": [
    {
      "id": "L1-{编号}",
      "name": "{一级标签名}",
      "description": "{标签定义}",
      "boundary": "{与其他标签的边界说明}",
      "examples": ["{样例1}", "{样例2}"],
      "level_2_tags": [
        {
          "id": "L2-{编号}",
          "name": "{二级标签名}",
          "description": "{标签定义}",
          "boundary": "{边界说明}",
          "examples": ["{样例1}"],
          "parent": "L1-{编号}"
        }
      ]
    }
  ],
  "overlap_rules": [
    {
      "tags": ["L1-1", "L1-2"],
      "rule": "{重叠时的处理规则}",
      "priority": "high|medium|low"
    }
  ],
  "multi_label_strategy": "single|multi_with_primary|multi_all",
  "confidence_threshold": 0.7,
  "uncertain_handling": "mark_for_review|skip|force_best_guess"
}
```

## 生成规则

### Step 1: 从访谈快照提取标签体系

读取 SKILL.md Step A2 的 5 要素完备快照：
- 标签体系来源（已有 / 让 AI 生成 / 一起设计）
- 标签粒度（一级 + 二级）
- 数据量级（决定是否需要 M6 分批）
- 置信度要求
- 不确定时处理策略

### Step 2: 应用 M5 两级标签体系四要素

每个标签（一级和二级）必须包含 4 个要素：

| 要素 | 必填 | 说明 |
|------|------|------|
| `name` | ✅ | 标签名 |
| `description` | ✅ | 标签定义（一句话说清"什么样的内容归这里"） |
| `boundary` | ✅ | 边界说明（与其他标签如何区分） |
| `examples` | ✅ | 至少 2 个样例（正面样例） |

### Step 3: 注入防幻觉元素

1. **`overlap_rules`**：必须列出所有可能重叠的标签对，明确优先级
2. **`multi_label_strategy`**：明确多标签策略
   - `single`：只允许一个一级标签
   - `multi_with_primary`：允许多个，但必须标主标签
   - `multi_all`：允许全部列出
3. **`confidence_threshold`**：低于阈值的进入 `uncertain_handling` 流程
4. **`uncertain_handling`**：明确不确定时的处理方式

### Step 4: 标签冲突决策树

标签树生成后，必须同步生成冲突决策树（YAML 描述）：

```yaml
conflict_decision_tree:
  - condition: "{场景描述，如'内容同时匹配 L1-1 和 L1-2'}"
    action: "选择 {优先级高的标签}"
    priority: ["L1-1", "L1-2"]
    reason: "{理由}"
  - condition: "{另一场景}"
    action: "标记为 uncertain"
    reason: "{理由}"
```

### Step 5: 与 M6 分批处理联动

数据量级 > 1000 时，标签树必须包含分批标注建议：

```json
{
  "batch_strategy": {
    "enabled": true,
    "batch_size": 100,
    "alignment_method": "前 10 条人工标注作为基准，后续对齐",
    "checkpoint_every": 5,
    "drift_detection": "每 5 批检查标签分布是否漂移"
  }
}
```

## 示例输出（场景 5 用户反馈分类）

```json
{
  "version": "1.0",
  "tag_system_name": "用户反馈分类体系",
  "created_at": "2026-07-22",
  "description": "对用户反馈进行多维度分类，支持产品改进决策",
  "level_1_tags": [
    {
      "id": "L1-1",
      "name": "功能问题",
      "description": "产品功能不符合预期或存在缺陷",
      "boundary": "与'体验问题'区分：功能问题指功能不可用或行为错误，体验问题指能用但难用",
      "examples": ["点击按钮无响应", "支付失败", "搜索结果错误"],
      "level_2_tags": [
        {
          "id": "L2-1",
          "name": "功能失效",
          "description": "核心功能完全无法使用",
          "boundary": "与'功能异常'区分：失效是完全不能用，异常是偶发或部分场景",
          "examples": ["登录不上去", "提交订单报错"],
          "parent": "L1-1"
        },
        {
          "id": "L2-2",
          "name": "功能异常",
          "description": "功能可用但偶发错误或部分场景失效",
          "boundary": "见 L2-1",
          "examples": ["偶尔闪退", "特定机型支付失败"],
          "parent": "L1-1"
        }
      ]
    },
    {
      "id": "L1-2",
      "name": "体验问题",
      "description": "功能可用但用户体验差",
      "boundary": "见 L1-1",
      "examples": ["操作步骤太多", "找不到入口", "加载太慢"],
      "level_2_tags": [
        {
          "id": "L2-3",
          "name": "交互问题",
          "description": "操作流程或界面交互不合理",
          "examples": ["按钮位置不直观", "返回逻辑混乱"],
          "parent": "L1-2"
        }
      ]
    },
    {
      "id": "L1-3",
      "name": "建议需求",
      "description": "用户提出的新功能或改进建议",
      "boundary": "与'体验问题'区分：建议是用户主动提出的增量，体验问题是已有功能的不满",
      "examples": ["希望能加夜间模式", "建议支持导出 PDF"],
      "level_2_tags": []
    }
  ],
  "overlap_rules": [
    {
      "tags": ["L1-1", "L1-2"],
      "rule": "功能问题优先于体验问题（功能失效比体验差更严重）",
      "priority": "high"
    },
    {
      "tags": ["L1-2", "L1-3"],
      "rule": "如果是已有功能的不满 → L1-2；如果是新增诉求 → L1-3",
      "priority": "medium"
    }
  ],
  "multi_label_strategy": "multi_with_primary",
  "confidence_threshold": 0.7,
  "uncertain_handling": "mark_for_review",
  "batch_strategy": {
    "enabled": true,
    "batch_size": 100,
    "alignment_method": "前 10 条人工标注作为基准",
    "checkpoint_every": 5,
    "drift_detection": "每 5 批检查标签分布"
  }
}
```

## 与其他模块的接口

| 接口 | 调用方 | 依赖 |
|------|--------|------|
| 上游 | tag-taxonomy-analyzer.md | 自动识别用户提交的标签体系 |
| 上游 | SKILL.md Step A4 | 5 要素完备快照 |
| 下游 | json-schema-spec.md | 标签作为 enum 来源 |
| 下游 | verify-template-spec.md | 验真脚本检查标签合法性 |
| 关联方法论 | M5 两级标签体系 | 四要素 + 边界 |
| 关联方法论 | M6 分批处理 | batch_strategy 段落 |
| 关联方法论 | M2 防幻觉三招 | confidence_threshold + uncertain_handling |
