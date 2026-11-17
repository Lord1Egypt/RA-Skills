# 五维智力模型数据结构定义

## 概述

本文档定义了五维智力模型使用的所有数据结构，包括维度标签、升维建议、维度关系等。

## 数据结构设计原则

1. **模型中心**：数据结构设计要符合模型的操作习惯
2. **简洁易用**：避免过度复杂，保持简洁
3. **标准化**：所有数据结构都要标准化，便于存储和查询
4. **可扩展**：预留扩展空间，便于未来增强

---

## 1. 维度标签数据结构

### 1.1 完整数据结构

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

### 1.2 字段说明

#### current_dimensions（当前维度状态）

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

#### relationships（维度关系）

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

#### confidence（置信度）

| 字段 | 类型 | 说明 | 示例 |
|-----|------|------|------|
| overall | float | 整体置信度（0.0-1.0） | 0.85 |
| {dimension} | float | 各维度的置信度（0.0-1.0） | {"algorithmic": 0.9, "systemic": 0.8} |

---

## 2. 升维建议数据结构

### 2.1 完整数据结构

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

### 2.2 字段说明

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

---

## 3. 升维历史数据结构

### 3.1 完整数据结构

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

### 3.2 字段说明

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

---

## 4. 完整记录数据结构

### 4.1 完整数据结构

```json
{
  "record_id": "record-2024-01-01-001",
  "timestamp": "2024-01-01T10:00:00Z",
  "task_description": "优化团队协作效率",

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
  },

  "elevation_suggestion": {
    "should_elevate": true,
    "reason": "当前问题涉及连锁反应，算法智力无法处理系统复杂性",
    "suggested_action": "add_dimensions",
    "suggested_dimensions": ["systemic"],
    "expected_effect": "引入系统智力后，可以评估连锁反应，避免'手术成功，病人死了'",
    "confidence": 0.9
  },

  "elevation_history": [],

  "raw_data": {
    "intentionality": {
      "desire_intensity": 0.8,
      "target": "优化团队协作"
    },
    "mathematical": {
      "reasoning_steps": 10,
      "accuracy": 0.9
    },
    "iteration": {
      "evolution_step": 3,
      "optimization_effect": 0.7
    }
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

### 4.2 字段说明

| 字段 | 类型 | 说明 |
|-----|------|------|
| record_id | str | 记录ID |
| timestamp | str | 时间戳 |
| task_description | str | 任务描述 |
| dimension_tags | Dict | 维度标签（参见第1节） |
| elevation_suggestion | Dict | 升维建议（参见第2节） |
| elevation_history | List[Dict] | 升维历史（参见第3节） |
| raw_data | Dict | 原始数据（三顶点运行数据） |
| cross_references | Dict | 跨轨关联（JSON轨 / Markdown轨 / 错误智慧库轨之间的交叉引用；"双轨"为历史字段名） |
| metadata | Dict | 元数据 |

---

## 5. 查询响应数据结构

### 5.1 查询当前维度状态

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

### 5.2 查询升维历史

```json
{
  "query_response": {
    "status": "success",
    "data": {
      "elevation_history": [
        {
          "timestamp": "2024-01-01T10:00:00Z",
          "action": "add_dimension",
          "dimension": "systemic",
          "effect": "positive"
        }
      ]
    }
  }
}
```

### 5.3 查询维度组合分布

```json
{
  "query_response": {
    "status": "success",
    "data": {
      "dimension_combinations": [
        {
          "combination": ["algorithmic"],
          "count": 10,
          "percentage": 0.25
        },
        {
          "combination": ["algorithmic", "systemic"],
          "count": 15,
          "percentage": 0.375
        },
        {
          "combination": ["algorithmic", "systemic", "narrative"],
          "count": 20,
          "percentage": 0.5
        }
      ]
    }
  }
}
```

---

## 6. 错误响应数据结构

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

---

## 7. 数据结构验证规则

### 7.1 维度名称验证

有效的维度名称：
- "algorithmic"（算法智力）
- "narrative"（叙事智力）
- "systemic"（系统智力）
- "execution"（执行智力）
- "meta"（元智力）

### 7.2 强度验证

有效的强度值：
- "high"
- "medium"
- "low"
- "none"

### 7.3 置信度验证

置信度范围：
- 0.0 ≤ confidence ≤ 1.0

### 7.4 关系类型验证

有效的关系类型：
- "enhance"
- "support"
- "collaborate"
- "complement"

### 7.5 动作类型验证

有效的动作类型：
- "add_dimensions"
- "remove_dimensions"
- "replace_dimensions"

### 7.6 效果类型验证

有效的效果类型：
- "positive"
- "negative"
- "neutral"
- "unknown"

---

## 8. 使用示例

### 8.1 生成维度标签

**输入：**
```json
{
  "task_description": "优化团队协作效率",
  "raw_data": {
    "intentionality": {
      "desire_intensity": 0.8
    },
    "mathematical": {
      "reasoning_steps": 10
    }
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
      "intensity": {
        "algorithmic": "high",
        "meta": "high"
      }
    },
    "confidence": {
      "overall": 0.85
    }
  }
}
```

### 8.2 获取升维建议

**输入：**
```json
{
  "current_dimensions": {
    "active": ["algorithmic"],
    "intensity": {
      "algorithmic": "high"
    }
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

---

## 9. 扩展性设计

### 9.1 预留字段

所有主要数据结构都预留了扩展字段，便于未来增强：

```json
{
  "dimension_tags": {
    "current_dimensions": {...},
    "relationships": [...],
    "confidence": {...},
    "extensions": {}  // 预留扩展字段
  }
}
```

### 9.2 版本管理

所有数据结构都包含版本信息：

```json
{
  "metadata": {
    "version": "1.0",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
  }
}
```

### 9.3 兼容性

未来版本将保持向后兼容，旧版本的数据结构仍然支持。
