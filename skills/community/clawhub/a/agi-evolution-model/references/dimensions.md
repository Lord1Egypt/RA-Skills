# 五维智力模型（Dimensions）

> **合并说明（2026-08-13）**：本文件由 `dimension_definitions.md`（五维智力模型定义）+ `dimension_data_structure.md`（五维智力模型数据结构定义）合并而成。原两份已归档至 `_deprecated_backup/`。**本文件为五维智力模型的唯一权威**。

## 目录

- [1. 五维智力模型定义](#1-五维智力模型定义)
  - [1.1 核心理念](#1-1-核心理念)
  - [1.2 五个维度定义](#1-2-五个维度定义)
  - [1.3 维度之间的关系](#1-3-维度之间的关系)
  - [1.4 升维机制](#1-4-升维机制)
  - [1.5 强度分级](#1-5-强度分级)
  - [1.6 使用指南](#1-6-使用指南)
- [2. 数据结构定义](#2-数据结构定义)
  - [2.1 数据结构设计原则](#2-1-数据结构设计原则)
  - [2.2 维度标签数据结构](#2-2-维度标签数据结构)
  - [2.3 升维建议数据结构](#2-3-升维建议数据结构)
  - [2.4 升维历史数据结构](#2-4-升维历史数据结构)
  - [2.5 完整记录数据结构](#2-5-完整记录数据结构)
  - [2.6 查询响应数据结构](#2-6-查询响应数据结构)
  - [2.7 错误响应数据结构](#2-7-错误响应数据结构)
  - [2.8 数据结构验证规则](#2-8-数据结构验证规则)
  - [2.9 使用示例](#2-9-使用示例)
  - [2.10 扩展性设计](#2-10-扩展性设计)
- [3. 相关脚本（五维智力工具箱）](#3-相关脚本-五维智力工具箱)

---

## 1. 五维智力模型定义

### 1.1 核心理念

五维智力模型是一个认知工具箱，包含五种不同的认知透镜。维度之间相互交叉、彼此协作，共同支持智能体的升维思考。

### 1.2 五个维度定义

#### 第一维：算法智力 (Algorithmic Intelligence)

**核心能力：** 模式识别与逻辑运算

**处理问题类型：** 确定性问题（规则明确、目标单一、封闭系统）

**典型表现：**
- 解数学题
- 写代码
- 下棋
- 通过标准化考试
- 路径规划
- 逻辑推理

**适用场景：**
- 封闭系统，规则明确
- 目标单一，可以精确定义
- 需要精确计算和逻辑推理
- 可以用数学模型描述

**潜在陷阱：**
- 将现实世界误认为封闭系统
- 忽视系统的复杂性和不确定性
- 成为"高分低能"的书呆子

**边界情况：**
- 如果同时涉及系统思考，应该标记为"算法智力 + 系统智力"
- 如果同时涉及意义构建，应该标记为"算法智力 + 叙事智力"

**识别标志：**
- 使用了逻辑推理步骤
- 进行了数学计算
- 识别了模式或规律
- 应用了明确的规则

---

#### 第二维：叙事智力 (Narrative Intelligence)

**核心能力：** 构建意义与情感共鸣

**处理问题类型：** 共识性问题（需要凝聚人心、建立信任、共同目标）

**典型表现：**
- 讲一个动人的故事
- 创作艺术
- 领导一个团队
- 凝聚共识
- 激励他人
- 建立信任

**适用场景：**
- 需要激励、说服
- 需要建立信任和共同目标
- 涉及人际关系和情感连接
- 需要意义构建

**潜在陷阱：**
- 沉迷于故事的华丽，忽略事实和逻辑
- 成为"画饼大师"，只说不做
- 过度依赖情感说服，忽视理性分析

**边界情况：**
- 如果同时涉及逻辑推理，应该标记为"叙事智力 + 算法智力"
- 如果同时涉及系统思考，应该标记为"叙事智力 + 系统智力"

**识别标志：**
- 构建了故事或叙事框架
- 涉及情感共鸣或意义构建
- 需要凝聚共识或建立信任
- 使用了比喻、隐喻等修辞手法

---

#### 第三维：系统智力 (Systemic Intelligence)

**核心能力：** 洞察要素间的动态关系

**处理问题类型：** 关联性问题（复杂、开放、相互关联的系统）

**典型表现：**
- 理解生态平衡
- 分析公司政治
- 预判政策的连锁反应
- 识别系统瓶颈
- 评估全局影响

**适用场景：**
- 复杂、开放、相互关联的系统问题
- 需要考虑多个变量的相互影响
- 需要预判连锁反应
- 需要"全局视角"

**潜在陷阱：**
- 分析过度导致"瘫痪"
- 成为只想不做的"空谈战略家"
- 过度关注细节，忽略关键问题

**边界情况：**
- 如果同时涉及逻辑推理，应该标记为"系统智力 + 算法智力"
- 如果同时涉及叙事，应该标记为"系统智力 + 叙事智力"

**识别标志：**
- 考虑了多个变量的相互影响
- 评估了连锁反应或全局影响
- 识别了系统瓶颈或关键节点
- 使用了系统思维或整体分析

---

#### 第四维：执行智力 (Execution Intelligence)

**核心能力：** 将思想转化为现实结果

**处理问题类型：** 能动性问题（时间紧迫、资源有限、结果导向）

**典型表现：**
- 项目管理
- 危机处理
- 在信息不完备时果断决策
- 克服阻力，推进实施
- 高效利用资源

**适用场景：**
- 时间紧迫
- 资源有限
- 结果导向
- 需要将想法转化为现实

**潜在陷阱：**
- 成为没头没脑的"行动派"
- 用战术勤奋掩盖战略懒惰
- 忽视长期影响，只关注短期结果

**边界情况：**
- 执行智力通常与其他维度配合使用
- 如果纯执行（无思考），应该标记为"执行智力"（但这种情况较少）

**识别标志：**
- 进行了具体的行动或实施
- 需要克服阻力或障碍
- 涉及资源分配和利用
- 关注结果和产出

---

#### 第五维：元智力 (Meta Intelligence)

**核心能力：** 对自身思维模式的觉察与调控

**处理问题类型：** 反思性问题（需要自我突破和成长）

**典型表现：**
- 反思"我为什么这么想"
- 识别偏见
- 主动切换认知透镜
- 评估自己的思维质量
- 调节自己的认知策略

**适用场景：**
- 任何想要实现自我突破和成长的时刻
- 需要自我反思或自我觉察
- 需要切换认知策略
- 需要评估自己的思维质量

**潜在陷阱：**
- 过度内省导致自我怀疑
- 陷入"我思故我在"的虚无
- 过度反思，导致行动瘫痪

**特殊性质：**
- 元智力是特殊维度，全程激活
- 元智力不参与具体问题解决，而是监控和调节其他维度
- 元智力可以察觉其他维度的局限性，并建议升维

**识别标志：**
- 进行了自我反思或自我觉察
- 识别了自己的思维模式或偏见
- 主动切换了认知策略
- 评估了自己的思维质量

### 1.3 维度之间的关系

#### 相互交叉

维度之间不是完全独立的，存在重叠和交叉：

- **算法智力 + 系统智力**：系统智力可能包含算法智力（识别系统中的模式）
- **叙事智力 + 元智力**：元智力可能包含叙事智力（反思自己的叙事模式）
- **执行智力 + 其他维度**：任何维度的思考都需要执行智力来落实

#### 彼此协作

解决问题时，需要多个维度协同工作：

- **串行协作**：先调用算法智力，再调用系统智力，最后调用执行智力
- **并行协作**：同时调用多个维度（算法智力 + 系统智力）
- **动态协作**：根据问题复杂度动态调整维度组合

#### 相互增强

维度之间相互增强，不是简单的叠加：

- **算法智力 + 系统智力**：系统智力指导算法智力的优化方向
- **叙事智力 + 系统智力**：系统智力指导叙事智力的策略调整
- **执行智力 + 其他维度**：执行智力的反馈影响其他维度的规划

### 1.4 升维机制

#### 升维的本质

随着问题深入，逐步激活更多维度，维度之间相互增强

#### 升维路径

```
┌─────────────┐      ┌──────────────────┐      ┌──────────────────────┐
│  算法智力    │  →   │ 算法 + 系统智力  │  →   │ 算法+系统+叙事智力   │
│ （初始阶段） │      │ （问题深入）      │      │ （问题更深入）        │
│ 逻辑推理即可 │      │ 需要系统思考     │      │ 需要意义构建         │
└─────────────┘      └──────────────────┘      └──────────────────────┘
        ↑                       ↑                         ↑
        └────── 元智力全程监控：觉察何时升维，引入哪个维度 ──────┘
```

#### 交叉升维

维度之间相互增强：

- **算法智力 + 系统智力**：系统智力增强了算法智力的全局视角
- **叙事智力 + 系统智力**：系统智力指导叙事智力的策略调整
- **执行智力 + 其他维度**：执行智力的反馈影响其他维度的规划

### 1.5 强度分级

维度强度的离散分级：

- **high（高）**：该维度在当前任务中起主导作用
- **medium（中）**：该维度在当前任务中起辅助作用
- **low（低）**：该维度在当前任务中起轻微作用
- **none（无）**：该维度在当前任务中未激活

### 1.6 使用指南

#### 识别维度

当分析一个任务或决策时，问自己：

1. 这个任务主要调用了哪些维度？
2. 每个维度在其中的作用是什么？
3. 维度之间是如何协作的？

#### 升维思考

当遇到困难或瓶颈时，问自己：

1. 我当前主要使用了哪些维度？
2. 是否有其他维度可以帮助我？
3. 维度之间是否可以相互增强？

#### 自我诊断

当陷入困境时，问自己：

"我在调用哪个维度的智力？是否用错了工具？"

- 如果你写了一份逻辑严密的报告（算法智力），但老板不买账，可能需要调用叙事智力
- 如果你发现团队效率低下，一头扎进去救火，可能需要切换到系统智力
- 如果你总在同一个地方跌倒，必须启动元智力，审视那个让你跌倒的行为模式

---

## 2. 数据结构定义

### 2.1 数据结构设计原则

1. **模型中心**：数据结构设计要符合模型的操作习惯
2. **简洁易用**：避免过度复杂，保持简洁
3. **标准化**：所有数据结构都要标准化，便于存储和查询
4. **可扩展**：预留扩展空间，便于未来增强

### 2.2 维度标签数据结构

#### 完整数据结构

```json
{
  "dimension_tags": {
    "current_dimensions": {
      "active": ["algorithmic", "systemic", "meta"],
      "primary": "algorithmic",
      "secondary": ["systemic"],
      "intensity": {
        "algorithmic": "high",
        "systemic": "medium",
        "meta": "high",
        "narrative": "none",
        "execution": "none"
      }
    },
    "relationships": [
      {
        "type": "enhance",
        "source": "systemic",
        "target": "algorithmic",
        "description": "系统智力增强算法智力的全局视角"
      }
    ],
    "confidence": {
      "overall": 0.85,
      "algorithmic": 0.9,
      "systemic": 0.8
    }
  }
}
```

#### 字段说明

**current_dimensions（当前维度状态）**

| 字段 | 类型 | 说明 | 示例 |
|-----|------|------|------|
| active | List[str] | 当前激活的维度列表 | ["algorithmic", "systemic", "meta"] |
| primary | str | 主维度 | "algorithmic" |
| secondary | List[str] | 辅助维度列表 | ["systemic"] |
| intensity | Dict[str, str] | 各维度的强度 | {"algorithmic": "high", "systemic": "medium"} |

**强度等级：**
- "high"（高）：主导作用
- "medium"（中）：辅助作用
- "low"（低）：轻微作用
- "none"（无）：未激活

**relationships（维度关系）**

| 字段 | 类型 | 说明 | 示例 |
|-----|------|------|------|
| type | str | 关系类型 | "enhance", "support", "collaborate" |
| source | str | 源维度 | "systemic" |
| target | str | 目标维度 | "algorithmic" |
| description | str | 关系描述 | "系统智力增强算法智力的全局视角" |

**关系类型：**
- "enhance"（增强）：源维度增强目标维度
- "support"（支持）：源维度支持目标维度
- "collaborate"（协作）：维度相互协作
- "complement"（互补）：维度互补

**confidence（置信度）**

| 字段 | 类型 | 说明 | 示例 |
|-----|------|------|------|
| overall | float | 整体置信度（0.0-1.0） | 0.85 |
| {dimension} | float | 各维度的置信度（0.0-1.0） | {"algorithmic": 0.9, "systemic": 0.8} |

### 2.3 升维建议数据结构

#### 完整数据结构

```json
{
  "elevation_suggestion": {
    "should_elevate": true,
    "reason": "当前问题涉及连锁反应，算法智力无法处理系统复杂性",
    "suggested_action": "add_dimensions",
    "suggested_dimensions": ["systemic"],
    "expected_effect": "引入系统智力后，可以评估连锁反应，避免'手术成功，病人死了'",
    "confidence": 0.9,
    "alternatives": [
      {
        "action": "add_dimensions",
        "dimensions": ["systemic", "narrative"],
        "reason": "同时引入系统智力和叙事智力，既评估连锁反应，又凝聚共识"
      }
    ]
  }
}
```

#### 字段说明

| 字段 | 类型 | 说明 | 示例 |
|-----|------|------|------|
| should_elevate | bool | 是否建议升维 | true |
| reason | str | 升维理由 | "当前问题涉及连锁反应..." |
| suggested_action | str | 建议的动作类型 | "add_dimensions", "remove_dimensions", "replace_dimensions" |
| suggested_dimensions | List[str] | 建议的维度列表 | ["systemic"] |
| expected_effect | str | 预期效果 | "引入系统智力后..." |
| confidence | float | 置信度（0.0-1.0） | 0.9 |
| alternatives | List[Dict] | 替代方案 | [{"action": "add_dimensions", "dimensions": ["systemic", "narrative"]}] |

**动作类型：**
- "add_dimensions"：添加维度
- "remove_dimensions"：移除维度
- "replace_dimensions"：替换维度

### 2.4 升维历史数据结构

#### 完整数据结构

```json
{
  "elevation_history": [
    {
      "timestamp": "2024-01-01T10:00:00Z",
      "action": "add_dimension",
      "dimension": "systemic",
      "before": ["algorithmic"],
      "after": ["algorithmic", "systemic"],
      "trigger": "detected system complexity",
      "effect": "positive",
      "effect_details": {
        "efficiency_improvement": 0.2,
        "quality_improvement": 0.15
      },
      "confidence": 0.9
    },
    {
      "timestamp": "2024-01-01T11:00:00Z",
      "action": "add_dimension",
      "dimension": "narrative",
      "before": ["algorithmic", "systemic"],
      "after": ["algorithmic", "systemic", "narrative"],
      "trigger": "need consensus building",
      "effect": "unknown",
      "confidence": 0.85
    }
  ]
}
```

#### 字段说明

| 字段 | 类型 | 说明 | 示例 |
|-----|------|------|------|
| timestamp | str | 时间戳（ISO 8601格式） | "2024-01-01T10:00:00Z" |
| action | str | 升维动作 | "add_dimension", "remove_dimension" |
| dimension | str | 涉及的维度 | "systemic" |
| before | List[str] | 升维前的维度列表 | ["algorithmic"] |
| after | List[str] | 升维后的维度列表 | ["algorithmic", "systemic"] |
| trigger | str | 升维触发原因 | "detected system complexity" |
| effect | str | 升维效果 | "positive", "negative", "neutral", "unknown" |
| effect_details | Dict | 效果详情 | {"efficiency_improvement": 0.2} |
| confidence | float | 置信度（0.0-1.0） | 0.9 |

**效果类型：**
- "positive"：正面效果
- "negative"：负面效果
- "neutral"：无明显效果
- "unknown"：未知（尚未评估）

### 2.5 完整记录数据结构

```json
{
  "record_id": "record-2024-01-01-001",
  "timestamp": "2024-01-01T10:00:00Z",
  "task_description": "优化团队协作效率",
  "dimension_tags": { ... },
  "elevation_suggestion": { ... },
  "elevation_history": [],
  "raw_data": {
    "intentionality": { "desire_intensity": 0.8, "target": "优化团队协作" },
    "mathematical": { "reasoning_steps": 10, "accuracy": 0.9 },
    "iteration": { "evolution_step": 3, "optimization_effect": 0.7 }
  },
  "cross_references": {
    "markdown_record_id": "markdown-2024-01-01-001",
    "error_wisdom_id": "error-2024-01-01-001"
  },
  "metadata": {
    "version": "1.0",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z",
    "created_by": "model"
  }
}
```

**字段说明：**

| 字段 | 类型 | 说明 |
|-----|------|------|
| record_id | str | 记录ID |
| timestamp | str | 时间戳 |
| task_description | str | 任务描述 |
| dimension_tags | Dict | 维度标签（见 §2.2） |
| elevation_suggestion | Dict | 升维建议（见 §2.3） |
| elevation_history | List[Dict] | 升维历史（见 §2.4） |
| raw_data | Dict | 原始数据（三顶点运行数据） |
| cross_references | Dict | 跨轨关联（JSON轨 / Markdown轨 / 错误智慧库轨之间的交叉引用；"双轨"为历史字段名） |
| metadata | Dict | 元数据 |

### 2.6 查询响应数据结构

**查询当前维度状态：**

```json
{
  "query_response": {
    "status": "success",
    "data": {
      "current_dimensions": {
        "active": ["algorithmic", "systemic", "meta"],
        "primary": "algorithmic",
        "secondary": ["systemic"],
        "intensity": {
          "algorithmic": "high",
          "systemic": "medium"
        }
      }
    }
  }
}
```

**查询升维历史：**

```json
{
  "query_response": {
    "status": "success",
    "data": {
      "elevation_history": [
        { "timestamp": "2024-01-01T10:00:00Z", "action": "add_dimension", "dimension": "systemic", "effect": "positive" }
      ]
    }
  }
}
```

**查询维度组合分布：**

```json
{
  "query_response": {
    "status": "success",
    "data": {
      "dimension_combinations": [
        { "combination": ["algorithmic"], "count": 10, "percentage": 0.25 },
        { "combination": ["algorithmic", "systemic"], "count": 15, "percentage": 0.375 },
        { "combination": ["algorithmic", "systemic", "narrative"], "count": 20, "percentage": 0.5 }
      ]
    }
  }
}
```

### 2.7 错误响应数据结构

```json
{
  "error_response": {
    "status": "error",
    "error_code": "INVALID_INPUT",
    "error_message": "输入数据格式错误",
    "details": {
      "field": "raw_data",
      "reason": "missing required field 'mathematical'"
    }
  }
}
```

**错误代码：**
- "INVALID_INPUT"：输入数据格式错误
- "MODEL_ERROR"：模型识别失败
- "STORAGE_ERROR"：存储错误
- "CONSISTENCY_ERROR"：数据一致性错误

### 2.8 数据结构验证规则

**维度名称验证**：有效的维度名称：`algorithmic` / `narrative` / `systemic` / `execution` / `meta`

**强度验证**：有效的强度值：`high` / `medium` / `low` / `none`

**置信度验证**：0.0 ≤ confidence ≤ 1.0

**关系类型验证**：`enhance` / `support` / `collaborate` / `complement`

**动作类型验证**：`add_dimensions` / `remove_dimensions` / `replace_dimensions`

**效果类型验证**：`positive` / `negative` / `neutral` / `unknown`

### 2.9 使用示例

**生成维度标签：**

**输入：**
```json
{
  "task_description": "优化团队协作效率",
  "raw_data": {
    "intentionality": { "desire_intensity": 0.8 },
    "mathematical": { "reasoning_steps": 10 }
  }
}
```

**输出：**
```json
{
  "dimension_tags": {
    "current_dimensions": {
      "active": ["algorithmic", "meta"],
      "primary": "algorithmic",
      "intensity": { "algorithmic": "high", "meta": "high" }
    },
    "confidence": { "overall": 0.85 }
  }
}
```

**获取升维建议：**

**输入：**
```json
{
  "current_dimensions": {
    "active": ["algorithmic"],
    "intensity": { "algorithmic": "high" }
  },
  "current_task": {
    "description": "优化团队协作效率",
    "complexity": "high"
  }
}
```

**输出：**
```json
{
  "elevation_suggestion": {
    "should_elevate": true,
    "suggested_dimensions": ["systemic", "narrative"],
    "reason": "团队协作涉及系统复杂性和共识构建",
    "confidence": 0.9
  }
}
```

### 2.10 扩展性设计

- **预留字段**：所有主要数据结构都预留了扩展字段（`extensions`），便于未来增强
- **版本管理**：所有数据结构都包含版本信息（`metadata.version`）
- **兼容性**：未来版本将保持向后兼容，旧版本的数据结构仍然支持

---

## 3. 相关脚本（五维智力工具箱）

| 脚本 | 职责 |
|------|------|
| `scripts/dimension_tagger.py` | 维度标签生成器（`generate_dimension_tags`） |
| `scripts/elevation_advisor.py` | 升维建议器（`generate_elevation_suggestion`） |
| `scripts/dimension_storage.py` | 维度存储管理器 |

**应用流程**：模型主导识别维度与升维决策；工具提供存储与查询。维度标签嵌入原始数据，由模型自主识别与标记。

---

*合并完成：2026-08-13 · 原两份文档归档于 `_deprecated_backup/` · 本文件为五维智力模型唯一权威*