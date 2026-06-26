# Skill-Evaluator Adapter — 规格与边界

**版本**: v0.1  
**状态**: Phase 1 minimal integration 已完成，full adapter 规划中

---

## 概述

本文档集中描述 `skill-evaluator` adapter 的当前实现状态与未来规划，避免相关描述分散在多个文件中。

---

## Phase 1 Minimal Integration（已实现）

当前 `generic-skill` lane 的 Critic 已接入一层**轻量级 evaluator evidence adapter**：

### 已接线能力

1. **Rubric 证据引用**
   - 读取 `skill-evaluator` 定义的评估维度权重
   - 将 rubric 评分映射到 Critic 的 `score_components`

2. **Category Mapping**
   - 根据 candidate 的 `category` 字段（docs/reference/guardrail/prompt/workflow/tests）
   - 应用不同的风险边界和评分策略

3. **Boundary Evidence**
   - 输出 `evaluator_evidence` 字段，包含：
     - `rubric`: 评估维度与权重
     - `category`: 候选类别
     - `boundary`: 风险等级边界
     - `test_tracks`: 预留的测试轨道（当前为空）
     - `limitations`: 当前评估的局限性说明

4. **混合打分**
   - `evaluator_score`: 基于 rubric 的证据分
   - `heuristic_score`: 基于规则的启发式分
   - `final_score`: 加权混合（当前权重可配置）

### 调用方式

```bash
python scripts/run_critic.py \
  --input <candidate.json> \
  --use-evaluator-evidence
```

### 输出示例

```json
{
  "critic_mode": "rubric_assisted",
  "evaluator_evidence": {
    "rubric": {"clarity": 0.3, "correctness": 0.4, "maintainability": 0.3},
    "category": "reference",
    "boundary": "low_risk",
    "test_tracks": [],
    "limitations": ["未运行 frozen benchmark", "未执行 hidden tests"]
  },
  "score_components": {
    "evaluator_score": 0.75,
    "heuristic_score": 0.70,
    "final_score": 0.73
  }
}
```

---

## Full Adapter 规划（Phase 2）

未来 `skill-evaluator` full adapter 需要补充以下能力：

### 1. Frozen Benchmark 执行

```python
class SkillEvaluatorAdapter:
    def run_frozen_benchmark(self, skill_path: str) -> dict:
        """
        运行预定义的 frozen benchmark suite
        
        返回:
        - benchmark_name
        - total_tests
        - passed_tests
        - failure_details
        - regression_detected (bool)
        """
        pass
```

**要求**:
- Benchmark 必须版本化（frozen）
- 支持增量运行（只跑受影响测试）
- 输出 machine-readable 结果

### 2. Hidden Tests 执行

```python
    def run_hidden_tests(self, skill_path: str, proposer_visible: bool = False) -> dict:
        """
        运行 Proposer 不可见的 hidden tests
        
        参数:
        - proposer_visible: 是否对 Proposer 可见（默认 False）
        
        返回:
        - test_suite_name
        - results (pass/fail/skip)
        - coverage_delta
        """
        pass
```

**边界**:
- Hidden tests 对 Proposer 不可见，防止 overfitting
- 仅 Gate / 控制面可访问结果
- 支持回归检测

### 3. External Regression Callback

```python
    def check_external_regression(self, skill_path: str, change_spec: dict) -> dict:
        """
        检查对外部系统的回归影响
        
        返回:
        - affected_apis
        - affected_workflows
        - regression_risk (low/medium/high)
        - mitigation_required (bool)
        """
        pass
```

### 4. Human Spot-Check Interface

```python
    def request_human_review(self, candidate: dict, reason: str) -> str:
        """
        请求人工抽查，返回 review ticket ID
        
        返回:
        - review_ticket_id
        - status (pending/approved/rejected)
        """
        pass
```

**使用场景**:
- 高风险修改（代码/核心逻辑）
- 边界情况（medium risk + 复杂变更）
- 自动化评估置信度低

---

## 评估边界定义

### Frozen Benchmark

| 项目 | 当前状态 | Phase 2 目标 |
|------|---------|-------------|
| 测试套件定义 | ❌ 未定义 | ✅ 每个 skill 至少 3 个核心场景测试 |
| 版本锁定 | ❌ 未实现 | ✅ git-tagged benchmark versions |
| 自动执行 | ❌ 未接入 | ✅ Critic 自动调用 |
| 回归检测 | ❌ 未实现 | ✅ 与历史版本对比 |

### Hidden Tests

| 项目 | 当前状态 | Phase 2 目标 |
|------|---------|-------------|
| 测试生成 | ❌ 未定义 | ✅ 基于 skill 描述自动生成 |
| 隔离执行 | ❌ 未实现 | ✅ 独立于 Proposer 视野 |
| 结果消费 | ❌ 未接入 | ✅ Gate 决策依据之一 |

### External Regression

| 项目 | 当前状态 | Phase 2 目标 |
|------|---------|-------------|
| 依赖图谱 | ❌ 未建立 | ✅ skill 间依赖关系图 |
| 影响分析 | ❌ 未实现 | ✅ 变更传播分析 |
| 回调机制 | ❌ 未实现 | ✅ 受影响 skill 自动重测 |

### Human Spot-Check

| 项目 | 当前状态 | Phase 2 目标 |
|------|---------|-------------|
| 触发条件 | ⚠️ 仅规则判断 | ✅ 基于风险评分 + 置信度 |
| 工单系统 | ❌ 未建立 | ✅ review ticket 追踪 |
| 反馈闭环 | ❌ 未实现 | ✅ 人工结论回流到 evaluator |

---

## 与 Critic 的集成方式

### Phase 1（当前）

```
Proposer → Critic(heuristic + rubric evidence) → Executor → Gate
```

- Critic 使用 `evaluator_phase1.py` 生成证据
- 不执行真实测试，仅引用 rubric/category/boundary

### Phase 2（规划）

```
Proposer → Critic(heuristic + evaluator runtime) → Executor → Gate
                         ↓
              run_frozen_benchmark()
              run_hidden_tests()
              check_external_regression()
              request_human_review() [if needed]
```

- Critic 调用完整的 `skill-evaluator` adapter
- 真实执行测试和回归检查
- Gate 决策基于更丰富的证据

---

## 注意事项

1. **不要混淆 Phase 1 和 Phase 2**
   - Phase 1 是 rubric-assisted judge
   - Phase 2 才是 full evaluator runtime

2. **保持向后兼容**
   - `--use-evaluator-evidence` 标志保持可选
   - 默认模式仍是纯 heuristic

3. **测试优先**
   - Full adapter 落地前必须先定义 frozen benchmark
   - 没有测试的自动修改默认 `hold` 或 `reject`

---

## 相关文件

- `adapters.md`: Adapter 总体规格与导航
- `phases.md`: 路线图与里程碑
- `guardrails.md`: 风控策略与边界
