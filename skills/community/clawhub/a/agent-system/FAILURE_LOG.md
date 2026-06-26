# Agent 失败日志

## 历史失败记录（JSON格式）

```json
[
  {
    "timestamp": "2026-04-02T10:30:00+08:00",
    "level": "ERROR",
    "module": "planner",
    "event": "placeholder_not_replaced",
    "details": {
      "placeholder": "{output}",
      "action": "filled_default_value",
      "status": "recovered"
    }
  },
  {
    "timestamp": "2026-04-02T10:30:00+08:00",
    "level": "ERROR",
    "module": "planner",
    "event": "prohibited_question_detected",
    "details": {
      "pattern": "请提供",
      "action": "stripped_from_output",
      "status": "recovered"
    }
  },
  {
    "timestamp": "2026-04-02T10:30:00+08:00",
    "level": "WARNING",
    "module": "reviewer",
    "event": "placeholder_detected",
    "details": {
      "score": 45,
      "is_valid": false,
      "triggered_heal": true
    }
  },
  {
    "timestamp": "2026-04-02T10:30:00+08:00",
    "level": "ERROR",
    "module": "heal",
    "event": "strategy_repeated",
    "details": {
      "retry_count": 2,
      "action": "switched_to_alternative_strategy",
      "status": "recovered"
    }
  }
]
```

---

## 失败模式清单

| 模式ID | 描述 | 严重度 | 状态 |
|--------|------|--------|------|
| P1-1 | 模板占位符未填充 | P1 | ✅ 已修复 |
| P1-2 | Planner 输出包含"请提供" | P1 | ✅ 已修复 |
| P1-3 | 自愈流程策略重复 | P1 | ✅ 已修复 |
| P2-1 | 输出置信度未标注 | P2 | 监控中 |
| P2-2 | complexity 判断偏差 | P2 | 监控中 |
| P2-3 | heal_trigger_count 过高 | P2 | 监控中 |

---

*最后更新：2026-04-02*
