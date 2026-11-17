# Reference：Harness 层强制契约（反 AP-13）

> 解决 AP-13（纯软约束不变量）：Skill 声明了关键不变量，但只在 prompt 层用文字写。
> **原则：prompt 层声明 ≠ 强制。** 下表逐条给出等效的 harness 层强制机制。

## 不变量 → 强制机制对照

| 不变量（prompt 层声明） | harness 层强制机制 | 状态 |
|------------------------|-------------------|------|
| G1 一页结论前置 | `scripts/check_gates.py` G1 | 已强制（可 CI） |
| G2 量化陈述带证据标签 | `scripts/check_gates.py` G2 | 已强制（可 CI） |
| G3 信息缺口清单非空 | `scripts/check_gates.py` G3 | 已强制（可 CI） |
| G4 预测先于结论登记（含锁定时点） | `scripts/check_gates.py` G4 | 已强制（可 CI） |
| G5 至少一个最小成本证伪实验 | `scripts/check_gates.py` G5 | 已强制（可 CI） |
| G6 综合判断明确 | `scripts/check_gates.py` G6 | 已强制（可 CI） |
| 预测登记不可篡改（锁定时点后不得改写） | `scripts/guard_predictions.py`（hash 校验）+ PreToolUse hook | 已提供，需部署 hook |
| 四轮审查不得合并 | 无 harness 机制（同模型同上下文，不可机械判定） | **声明为软约束** |
| 反合理化（不得无证据翻盘） | 无 harness 机制（依赖对话语义） | **声明为软约束** |

## 部署方式

### 1. 门禁校验（CI）

```bash
python3 scripts/check_gates.py <output.md>        # 人类可读
python3 scripts/check_gates.py <output.md> --json # CI 管线
```

### 2. 预测台账守卫（PreToolUse hook）

在宿主平台 hooks 配置中加入（路径按实际调整）：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command",
            "command": "python3 scripts/guard_predictions.py predictions/ledger.md || exit 1" }
        ]
      }
    ]
  }
}
```

合法登记新预测后，重新封存：`python3 scripts/guard_predictions.py predictions/ledger.md --seal`

## 诚实声明

- **未部署 hook 时**，"预测不可篡改" 降级为 prompt 层软约束。此时不得在任何输出中宣称该不变量"已强制"。
- **四轮审查与反合理化** 无法在本架构内机械强制——它们依赖对话语义，属于软约束。Skill 正文已明确标注其失效模式（见 [SKILL.md](../SKILL.md#已知失效模式)），此处不再伪装为已强制。