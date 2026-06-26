# Domain-Knowledge 扩展测试与 Eval 设计

**日期**: 2026-04-28
**关联**:
- 设计文档：`references/domain-knowledge-design-v2.md`
- 实施计划：`plans/2026-04-28-domain-knowledge-v2.md`

**核心论点**: v1 的"准确率 >80%、渲染评分 >8/10"是占位指标，没有可执行的 eval 框架。本文档定义**三层测试金字塔 + 五个事后可量化代理指标 + Ship Gate**，使"高质量蓝图"假设可被验证或证伪。

---

## 一、测试金字塔

| 层级 | 测什么 | 测法 | 频率 | 谁能跑 |
|------|--------|------|------|--------|
| **L1 单元测试** | validator 逻辑、diff 计算、clarifyRequests 强制 | pytest，机器可判 | 每次 commit | CI 自动 |
| **L2 提取 Eval** | AI 从原始文本能否抽出对的实体/关系 | Golden 数据集 + LLM-as-judge（跨模型） | 每个 PR | CI 自动（成本可控） |
| **L3 端到端 Eval** | 三件套是否真提升用户产出质量 | 真实场景剧本 + 五指标 | 阶段性手动 | 人工触发（成本高） |

**核心原则**:
- L1 越多越好（机器测）
- L2 是"AI 提取能力"的回归保证
- L3 是"质量驱动假设"的验证——**Ship Gate 在这里**

---

## 二、L1 单元测试

### 2.1 测试范围

由 plan v2 引导的实际单元测试：

| 测试文件 | 用例数 | 覆盖功能 |
|---------|-------|---------|
| `tests/test_clarify_required.py` | 3 | clarifyRequests 强制 ≥3 + 必须 target 现存实体 + architecture 蓝图无此约束 |
| `tests/test_refine_diff.py` | 4 | modify / add / delete / 多操作顺序 |
| `tests/test_validate_knowledge.py` | 10 | minimal pass / missing core fields / invalid type / dk missing intent / arch with knowledge / dk empty / relation missing from / user fields allowed / unknown relation type warn / arch backward compat |

**最低门槛**: 17 个用例，全过。

### 2.2 新增 L1 用例（除 plan 列出的之外）

#### 测试: detectedIntent 长度上限

```python
def test_detected_intent_too_long_warns():
    bp = _make_minimal_dk_blueprint()
    bp["meta"]["detectedIntent"] = "x" * 200  # over 80 chars
    result = validate_blueprint(bp)
    warnings = [i for i in result["issues"] if i["severity"] == "warning"]
    assert any("DETECTED_INTENT_TOO_LONG" in i["code"] for i in warnings)
```

#### 测试: refine diff 空 operations

```python
def test_refine_empty_operations_passes():
    """Empty diff is valid (means: no changes recommended)"""
    bp = {"library": {"knowledge": {"painPoints": []}}}
    diff = {"operations": []}
    result = apply_diff(bp, diff)
    assert result == bp
```

#### 测试: refine 应用后 validator 仍通过

```python
def test_refined_blueprint_still_validates():
    """End-to-end: apply refine diff -> result must validate"""
    bp = _make_minimal_dk_blueprint()
    diff = {
        "operations": [
            {"op": "add", "path": "library.knowledge.painPoints[]",
             "value": {"id": "pain-002", "name": "新痛点", "entityType": "painPoint"}}
        ]
    }
    result = apply_diff(bp, diff)
    val_result = validate_blueprint(result)
    errors = [i for i in val_result["issues"] if i["severity"] == "error"]
    assert len(errors) == 0
```

### 2.3 跑法

```bash
python -m pytest tests/ -v --tb=short
```

CI 集成于每次 commit。运行时间应 <5s。

---

## 三、L2 提取 Eval（Golden Dataset + LLM Judge）

### 3.1 数据集结构

```
tests/extraction_eval/
├── fixtures/
│   ├── 01-cross-border-roi/
│   │   ├── input.md              # 用户原始需求文本（50-200 字）
│   │   ├── industry.txt          # 行业标识：cross-border-ecommerce
│   │   ├── must_have.yaml        # 必含项规范
│   │   └── must_not_have.yaml    # 反向约束
│   ├── 02-cross-border-creative/ # 跨境电商-素材角度
│   ├── 03-retail-membership/
│   ├── 04-retail-stockout/
│   ├── 05-finance-credit/
│   └── 06-custom-entities/       # 用户自定义实体（caseStudies 等）
├── run_eval.py                   # 跑 AI 提取 + 比对
├── llm_judge.py                  # LLM-as-judge
└── reporter.py                   # 输出 markdown 报告
```

### 3.2 fixture 模板

#### `01-cross-border-roi/input.md`

```markdown
我们是跨境电商广告投放团队，主要在 Facebook 和 Google 投放美国市场。
最近 3 个月遇到的问题：
- ROAS 波动很大，有时能到 5.0，有时只有 1.5，无法稳定
- 素材投放一周后 CTR 就开始下降，但我们没有固定的迭代节奏
- 上个月被 Facebook 警告过一次，担心政策合规

需要做的：理清楚我们这个领域的 know-how，画一张大图给团队和客户讲明白。
```

#### `01-cross-border-roi/must_have.yaml`

```yaml
blueprintType: domain-knowledge

detectedIntent:
  must_contain_themes: ["跨境电商", "广告"]   # AI 抽取的意图必须涉及这些主题（语义判断，非字面匹配）
  max_chars: 80

painPoints:
  min_count: 3
  must_include_themes:                          # 主题级,LLM judge 判断
    - "ROAS 或 ROI 波动"
    - "素材效果衰减"
    - "平台合规或封号风险"

strategies:
  min_count: 2
  each_must_solve_painPoint: true               # 必须有 solves 关系

metrics:
  min_count: 1
  must_include_themes: ["ROAS"]

clarifyRequests:
  min_count: 3
  must_target_specific_entities: true            # targetEntityId 必须非空且存在

relations:
  must_have_types: ["solves"]                    # 至少出现一次 solves
  
selfCheck:
  entities_with_questions_ratio:                 # 至少 30% 实体有 _selfCheck.questions
    min: 0.3

industry: cross-border-ecommerce                 # 行业自动选择
```

#### `01-cross-border-roi/must_not_have.yaml`

```yaml
# Reject patterns: things that indicate misunderstood intent
painPoints:
  must_not_include_themes:
    - "缺乏 ROI 监控系统"     # 这是系统视角不是业务痛点
    - "数据库不稳定"           # 偏离业务上下文

strategies:
  must_not_include_themes:
    - "优化 ROI"             # 这是目标不是策略
    - "提升广告效果"           # 太抽象

blueprintType:
  not_equal: "architecture"   # 这个场景不应被识别为架构蓝图
```

### 3.3 LLM-as-judge 设计

#### 3.3.1 跨模型原则

- **提取**: 用 Claude Sonnet/Opus
- **评判**: 用 GPT-4 (或反过来)
- **理由**: 同模型自评会高估,跨模型 reduce same-model bias

#### 3.3.2 Judge prompt 模板

```
You are an evaluator for a business blueprint extraction system. Your job is to check whether the EXTRACTED BLUEPRINT correctly captures the themes specified in MUST_HAVE.

EXTRACTED BLUEPRINT:
{blueprint_json}

MUST_HAVE SPECIFICATION:
{must_have_yaml}

For each theme requirement, output:
- theme: the theme name
- found_in_entity: the entity ID where this theme is captured (or null)
- match_confidence: 0.0-1.0 (how confident the entity actually matches the theme semantically, not literal string match)
- reasoning: 1-sentence why

EVALUATION RULES:
- Match by semantic meaning, not by keyword. "ROAS 波动" matches an entity called "ROI 不稳" because they describe the same business problem.
- Do NOT reward literal keyword inclusion. Reward whether the business meaning is captured.
- Confidence <0.5 means the entity doesn't really capture the theme.

Output as JSON:
```json
{
  "theme_matches": [
    {"theme": "...", "found_in_entity": "pain-001", "match_confidence": 0.85, "reasoning": "..."},
    ...
  ],
  "extra_entities": ["list of entity IDs that don't match any required theme — they may be hallucinations"],
  "overall_score": 0.0-1.0
}
```

Output ONLY the JSON, no preamble.
```

#### 3.3.3 防作弊抽样

每次 eval 跑完后，**抽样 20% judge 结论由人工 verify**:

- 如果 judge 给 confidence 0.85，人工要打 ≥0.7 才算通过
- 不一致比例 >20% → 该次 eval 结果作废，需要修 prompt 重跑

### 3.4 跑法

```bash
python tests/extraction_eval/run_eval.py \
  --fixtures tests/extraction_eval/fixtures/ \
  --extractor claude \
  --judge gpt4 \
  --output reports/eval-2026-04-28.md
```

**输出报告示例**:

```markdown
# Extraction Eval Report 2026-04-28

| Fixture | painPoint Coverage | Strategy Coverage | Relations OK | Clarify OK | Overall |
|---------|-------------------|-------------------|--------------|------------|---------|
| 01-cross-border-roi | 3/3 ✅ | 2/2 ✅ | ✅ | 4 reqs ✅ | **PASS (0.92)** |
| 02-cross-border-creative | 2/3 ⚠️ | 2/2 ✅ | ✅ | 3 reqs ✅ | PASS (0.78) |
| 03-retail-membership | 1/3 ❌ | 1/2 ❌ | ✅ | 0 reqs ❌ | **FAIL (0.45)** |
...

## Summary
- 4/6 fixtures PASS
- Avg theme coverage: 76%
- Failed fixture analysis: retail hints 是 template-only,AI 提取困难,符合预期
```

### 3.5 Ship Gate (L2)

| 指标 | 门槛 | 失败处理 |
|------|------|----------|
| 跨境电商 fixture 主题覆盖率 | ≥80% | 修 SKILL.md 提取流程或跨境电商 hints |
| 其他 fixture 主题覆盖率 | ≥60% | 不阻塞（template-only hints 已知质量偏低） |
| clarifyRequests 必填校验 | 100% fixture 通过 | 修 validator 或 SKILL.md |
| 关系完整性 | 100% fixture relations 中 ID 存在 | 修 SKILL.md prompt |

---

## 四、L3 端到端 Eval（核心 Ship Gate）

### 4.1 设计目标

L3 是**"质量驱动假设是否成立"的最终验证**。不打主观分，全部用代理指标。

### 4.2 五个核心指标

#### 指标 1: 澄清击中率

**定义**:
```
澄清击中率 = 用户给出"实质回答"的 clarifyRequests 数 / 总 clarifyRequests 数
```

**实质回答**: 长度 >5 字 且不在 `["不知道", "随便", "都行", "你看着办"]` 列表

**门槛**: ≥60%

**数学表达**:
```
HitRate = | { req | len(answer(req)) > 5 ∧ answer(req) ∉ vacuous_set } | / | clarifyRequests |
```

**含义**: 如果 <60%,说明 AI 提的反问没击中真实空白,用户不愿/不能回答。改进方向: 优化 SKILL.md 中反问触发模式。

#### 指标 2: 二轮变更率

**定义**:
```
二轮变更率 = (新增实体数 + 修改实体数 + 删除实体数 + 新增关系数) / (第一版总实体+关系数)
```

**门槛**: 30% ≤ rate ≤ 80%
- <30%: 澄清回合没产生实质修改,价值低
- >80%: 第一版几乎被推翻,提取流程有大问题

**数学表达**:
```
ChangeRate = ( | E_v2 △ E_v1 | + | R_v2 △ R_v1 | ) / ( | E_v1 | + | R_v1 | )
其中 △ 是对称差
```

#### 指标 3: 自检指向准确率

**定义**:
```
准确率 = 第二轮被用户主动修改的实体 ∩ 第一轮 _selfCheck.questions 非空的实体 / _selfCheck.questions 非空的实体总数
```

**门槛**: ≥50%

**含义**: 如果 <50%,说明 AI 自检标黄的实体不是用户真正关心的,反问清单需要更新。

#### 指标 4: 修订接受率

**定义**:
```
接受率 = 用户 accept 的 diff operations / 总 operations
```

**门槛**: ≥70%

**含义**: 如果 <70%,说明 refine prompt 生成的 diff 质量差,用户大量拒绝。改进方向: refine prompt 结构或反馈解析。

#### 指标 5: 回归零破坏

**定义**:
```
现有 architecture 蓝图通过 validator 数 / 现有 architecture 蓝图总数 = 100%
现有蓝图导出 SVG 与 baseline 结构化 diff 通过率 = 100%
```

**门槛**: 100% 必过

**测法**: 见 §6 回归测试。

### 4.3 场景剧本结构

```
tests/e2e_eval/
├── scenarios/
│   ├── 01-pitch-cross-border/
│   │   ├── round1_input.md          # 用户首轮输入
│   │   ├── round1_clarify_answers.md # 用户对澄清回合的回答（脚本化）
│   │   ├── round2_feedback.md       # 用户对第一版的反馈（给 --refine 用）
│   │   ├── refine_decisions.yaml    # 用户对 diff operations 的 accept/reject
│   │   └── expected_metrics.yaml    # 五指标预期范围
│   ├── 02-retail-template-only/     # 已知 hints 质量低,验证 disclaimer 起作用
│   ├── 03-finance-template-only/
│   ├── 04-cross-border-deep/        # 长输入(>500 字),验证粒度
│   ├── 05-mixed-architecture-knowledge/  # 混合需求,验证 detectedIntent
│   └── 06-custom-entities/           # 用户自定义实体类型
├── run_scenario.py
└── metrics.py                        # 五指标计算
```

### 4.4 场景剧本示例

#### `01-pitch-cross-border/round1_input.md`

```markdown
我们是跨境电商投放团队，需要画一张广告领域的 know-how 大图，
用于客户 pitch。重点突出我们的专业度。
```

#### `01-pitch-cross-border/round1_clarify_answers.md`

```markdown
[clr-001] (target: pain-001 "ROI 不稳")
ROI 不稳是症状,根因是创意疲劳和受众饱和

[clr-002] (target: str-001 "测款节奏策略")
测款节奏策略对应 ROI 不稳和素材疲劳两个痛点

[clr-003] (target: str-001 "测款节奏策略")
通过 ROAS 衡量,目标 >3.0
```

#### `01-pitch-cross-border/round2_feedback.md`

```markdown
策略部分还可以加上动态出价和受众分层。
另外 "ROI 不稳"应该拆成 ROAS 波动和获客成本上升两个痛点,粒度更准确。
```

#### `01-pitch-cross-border/refine_decisions.yaml`

```yaml
# 模拟用户对 diff operations 的决策
operations:
  - op_index: 0  # 拆分 ROI 不稳为 ROAS 波动
    decision: accept
  - op_index: 1  # 新增获客成本上升痛点
    decision: accept
  - op_index: 2  # 新增动态出价策略
    decision: accept
  - op_index: 3  # 新增受众分层策略
    decision: accept
  - op_index: 4  # AI 主动建议删除某 pitfall（用户认为不该删）
    decision: reject
```

#### `01-pitch-cross-border/expected_metrics.yaml`

```yaml
clarification_hit_rate:
  min: 0.6
  expected: 1.0  # 这个场景设计了 3 个实质答案

second_round_change_rate:
  min: 0.3
  max: 0.8
  expected_range: [0.4, 0.6]  # 拆分痛点 + 新增策略,应有约 50% 变更

self_check_targeting:
  min: 0.5
  expected: 0.7  # 用户修改了 ROI 不稳痛点（标黄）+ 加了策略

refine_acceptance_rate:
  min: 0.7
  expected: 0.8  # 5 个 operations 接受 4 个

regression_pass: true  # 现有 architecture 蓝图必须 0 破坏
```

### 4.5 跑法

```bash
python tests/e2e_eval/run_scenario.py \
  --scenarios tests/e2e_eval/scenarios/ \
  --output reports/e2e-eval-2026-04-28.md \
  --extractor claude \
  --refiner claude \
  --judge gpt4
```

#### 跑法详细流程（`run_scenario.py`）

```python
for scenario_dir in scenarios:
    # 阶段 1: 第一轮提取
    input_text = read(scenario_dir / "round1_input.md")
    blueprint_v1 = run_skill_plan(input_text)
    
    # 阶段 2: 模拟用户回答澄清
    answers = parse(scenario_dir / "round1_clarify_answers.md")
    blueprint_v1["context"]["clarifications"] = answers
    
    # 阶段 3: 第二轮提取(基于 clarifications)
    blueprint_v2 = run_skill_plan(input_text, prior_blueprint=blueprint_v1)
    
    # 阶段 4: 模拟用户反馈 + refine
    feedback = read(scenario_dir / "round2_feedback.md")
    diff = run_skill_refine(blueprint_v2, feedback)
    
    # 阶段 5: 模拟用户对 diff 的决策
    decisions = parse(scenario_dir / "refine_decisions.yaml")
    diff_filtered = filter_diff(diff, decisions)
    blueprint_v3 = apply_diff(blueprint_v2, diff_filtered)
    
    # 计算五指标
    metrics = {
        "clarification_hit_rate": compute_hit_rate(blueprint_v1, answers),
        "second_round_change_rate": compute_change_rate(blueprint_v1, blueprint_v2),
        "self_check_targeting": compute_targeting(blueprint_v1, blueprint_v2),
        "refine_acceptance_rate": compute_accept_rate(diff, decisions),
        "regression_pass": run_regression_suite(),
    }
    
    # 与 expected 对比
    expected = parse(scenario_dir / "expected_metrics.yaml")
    write_report(scenario_dir.name, metrics, expected)
```

### 4.6 Ship Gate (L3)

**P0 完工 Ship Gate**: 6 个场景全跑,必须满足:

| 指标 | 必过场景数 |
|------|-----------|
| 澄清击中率 ≥60% | 5/6 (容忍一个因脚本设计原因失败) |
| 二轮变更率 30%-80% | 5/6 |
| 自检指向准确率 ≥50% | 4/6 (要求略低,因为模拟答案的不确定性大) |
| 修订接受率 ≥70% | 5/6 |
| 回归零破坏 | 6/6 |

**任一指标在跨境电商深度场景(01)失败 → STOP, 改设计**, 因为这是黄金标准场景。

template-only 行业场景(02-03)允许指标偏低, 但 disclaimer 必须出现在 detectedIntent 中。

---

## 五、回归测试

### 5.1 基线生成

```bash
# 在合并到 master 之前,在 master 分支生成基线
git checkout master
python tests/regression/generate_baseline.py \
  --demos demos/ \
  --output tests/regression/baseline/
```

每个现有 architecture 蓝图生成:
- `<demo>.validator.json` (validator 输出)
- `<demo>.svg` (导出 SVG)
- `<demo>.metrics.json` (节点数、边数、文件大小、导出耗时)

### 5.2 diff 策略

#### 5.2.1 Validator diff

```python
def diff_validator_output(baseline: dict, current: dict) -> list[str]:
    """Compare validator outputs. Allow new warnings, reject new errors."""
    differences = []
    
    base_errors = {i["code"] for i in baseline["issues"] if i["severity"] == "error"}
    curr_errors = {i["code"] for i in current["issues"] if i["severity"] == "error"}
    
    # New errors are unacceptable
    new_errors = curr_errors - base_errors
    if new_errors:
        differences.append(f"NEW ERRORS: {new_errors}")
    
    # Removed errors are also suspicious (validator weakened?)
    removed_errors = base_errors - curr_errors
    if removed_errors:
        differences.append(f"REMOVED ERRORS (validator weakened?): {removed_errors}")
    
    return differences
```

#### 5.2.2 SVG 结构化 diff（不做 pixel diff）

```python
def diff_svg_structural(baseline_svg: str, current_svg: str) -> list[str]:
    """Compare SVG structure, ignoring layout coordinates."""
    differences = []
    
    base = parse_svg(baseline_svg)
    curr = parse_svg(current_svg)
    
    # Node count
    if abs(len(base.nodes) - len(curr.nodes)) > 0:
        differences.append(f"Node count changed: {len(base.nodes)} -> {len(curr.nodes)}")
    
    # Edge count
    if abs(len(base.edges) - len(curr.edges)) > 0:
        differences.append(f"Edge count changed: {len(base.edges)} -> {len(curr.edges)}")
    
    # Text content (entity names should not change)
    base_texts = {n.text for n in base.nodes}
    curr_texts = {n.text for n in curr.nodes}
    text_diff = base_texts ^ curr_texts
    if text_diff:
        differences.append(f"Entity names changed: {text_diff}")
    
    # 允许 layout 微调: 不比较 x/y 坐标
    
    return differences
```

#### 5.2.3 性能 diff（±15% 容忍）

```python
def diff_performance(baseline: dict, current: dict) -> list[str]:
    """Performance must stay within ±15% of baseline."""
    differences = []
    
    for metric in ["export_time_ms", "validator_time_ms", "svg_size_bytes"]:
        base_val = baseline[metric]
        curr_val = current[metric]
        ratio = curr_val / base_val if base_val > 0 else float('inf')
        
        if not (0.85 <= ratio <= 1.15):
            differences.append(f"{metric}: {base_val} -> {curr_val} ({ratio:.2f}x)")
    
    return differences
```

### 5.3 跑法

```bash
python tests/regression/compare.py \
  --baseline tests/regression/baseline/ \
  --output reports/regression-2026-04-28.md
```

**Ship Gate**: validator diff 必须 0 新 error, SVG 结构 diff 必须 0(不允许 entity 增减或重命名), 性能 diff 必须在 ±15% 内。

---

## 六、CI 集成

### 6.1 工作流配置

```yaml
# .github/workflows/test.yml (示意,需根据现有 CI 调整)

on: [push, pull_request]

jobs:
  l1-unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pip install -e .[dev]
      - run: python -m pytest tests/test_*.py -v --tb=short
      - run: python -m pytest tests/test_*.py --cov --cov-fail-under=85
  
  regression:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pip install -e .[dev]
      - run: python tests/regression/compare.py --baseline tests/regression/baseline/
  
  l2-extraction-eval:
    runs-on: ubuntu-latest
    needs: [l1-unit]
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v3
      - run: pip install -e .[dev]
      - env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python tests/extraction_eval/run_eval.py --output reports/l2-eval.md
      - uses: actions/upload-artifact@v3
        with:
          name: l2-eval-report
          path: reports/l2-eval.md
  
  # L3 是手动触发,不放 CI
```

### 6.2 触发频率与成本

| 测试 | 频率 | 单次时长 | 单次成本 |
|------|------|---------|---------|
| L1 单测 | 每次 commit | <5s | $0 |
| 回归 | 每次 PR | ~10s | $0 |
| L2 提取 eval | 每次 PR | 1-2 min | ~$2 (LLM 调用) |
| L3 端到端 eval | 阶段性手动 (每 Phase 完成) | 5-10 min | ~$15 (6 场景 × $2.5) |

### 6.3 Ship Gate 决策树

```
PR 提交
  ↓
L1 单测 + 回归测试
  ↓ pass
L2 提取 eval (跨境电商深度 ≥80%, 其他 ≥60%)
  ↓ pass
合并到 master
  ↓
Phase 0/1/2 完工节点
  ↓
L3 端到端 eval (六场景五指标)
  ↓ pass (除一个例外)
Ship 给真实用户

  ↓ fail any
Stop. Diagnose:
- L1 fail → 修代码
- 回归 fail → 修代码,可能是 backward-compat 破坏
- L2 fail → 修 SKILL.md 提取流程,或行业 hints
- L3 fail → 改设计,可能整个三件套机制需要调整
```

---

## 七、人工 Verify 流程

### 7.1 抽样比例

| Eval 层 | 抽样比例 | Verify 内容 |
|---------|---------|------------|
| L1 | 不抽样（机器可判） | - |
| L2 | 20% LLM judge 结论 | 人工判断 confidence 是否合理 |
| L3 | 100% 失败场景 + 30% 通过场景 | 看 metrics 是否反映真实质量 |

### 7.2 Verify 工具

写一个简单 CLI 让人工 verify L2:

```bash
python tests/extraction_eval/verify_judge.py \
  --report reports/l2-eval-2026-04-28.md \
  --sample-rate 0.2
```

工具会:
1. 随机抽 20% judge 结论
2. 显示 entity 内容 + judge 给的 confidence
3. 让人工输入自己的 confidence (0-1)
4. 计算 judge vs human 的相关系数

**门槛**: Pearson correlation ≥0.7,否则 judge 不可信,该次 eval 作废。

---

## 八、Golden 数据集冷启动方案

### 8.1 第一版数据集如何构建

**问题**: 没有领域专家时怎么搭建 Golden Dataset?

**方案**: 三步走

#### Step 1: Self-annotation (你/我手工标注)

- 每个 fixture 由 v2 设计者写 input.md + must_have.yaml
- 跨境电商 fixture 内容来自 v2 设计中已深度验证的 hints
- 其他 fixture 用 plan v2 中的 template hints 反推

#### Step 2: Calibration run (校准跑)

- 用第一版 fixture 跑 L2 eval
- 看哪些 fixture 的判定波动大(同样输入跑 3 次,judge 结论差异 >30%)
- 这些 fixture 修订 must_have 表述,降低歧义

#### Step 3: Real-user feedback (真实用户回流)

- 真实用户跑过几个蓝图后,选 2-3 个有代表性的(用户认为效果好的、不好的各一)
- 标注成新的 fixture,加入数据集
- 数据集随时间增长,质量持续提升

### 8.2 数据集版本管理

```
tests/extraction_eval/fixtures/
├── _meta.yaml          # 数据集版本号、构建时间、贡献者
├── 01-cross-border-roi/
│   ├── _meta.yaml      # fixture 级别 meta（来源、信任度）
│   ├── input.md
│   ├── must_have.yaml
│   └── ...
```

`_meta.yaml`:

```yaml
fixture_id: "01-cross-border-roi"
source: "v2 designer self-annotation"
trust_level: "high"          # high / medium / low
last_calibrated: "2026-04-28"
known_volatility: "low"      # judge 跑 3 次结论波动小
notes: "跨境电商核心场景,基于深度验证的 hints"
```

---

## 九、工时与成本估算

### 9.1 工时

| 项 | 工时 |
|----|------|
| L1 单元测试（plan v2 已包含） | 包含在 plan |
| L2 框架（fixture loader + judge wrapper + reporter） | 3-4h |
| L2 数据集首版（6 fixture × ~40 min/fixture） | 4-5h |
| L3 框架（场景 runner + 五指标计算 + 报告生成） | 4-5h |
| L3 场景剧本首版（6 场景 × ~30 min/场景） | 3-4h |
| 回归基线生成 + diff 工具 | 2-3h |
| 人工 verify 工具 | 1-2h |
| CI 集成 | 1-2h |
| **合计 (eval 框架增量)** | **18-25h** |

### 9.2 运行成本

| 频率 | 单次成本 | 月度估算 |
|------|---------|---------|
| L1 commit (每天 5 commit) | $0 | $0 |
| L2 PR (每天 2 PR) | $2 | ~$120/月 |
| L3 阶段性 (每月 2 次) | $15 | ~$30/月 |
| **月度总计** | - | **~$150/月** |

预算可控。LLM API 调用是主要成本,可以通过缓存或本地模型(如 Ollama + Llama)进一步压低。

---

## 十、关键决策记录

### 决策 1: 不做主观打分

**问题**: v1 用"渲染评分 >8/10"这种主观打分,谁来打、怎么打都没说。

**决策**: 全部用代理指标(behaviorally-grounded metrics),例如"用户在第二轮主动修改的实体数"。

**理由**: 代理指标可重复、可自动化、防止打分者偏见。

### 决策 2: LLM-as-judge 必须跨模型

**问题**: 同模型自评偏高(因为风格相似)。

**决策**: 提取用 Claude,评判用 GPT-4(或反过来)。

**理由**: 减少 same-model bias。重要结论 20% 人工抽样 verify。

### 决策 3: L3 是 Ship Gate, L2 不是

**问题**: 在哪里画 ship 红线?

**决策**: L3 五指标全过(除一个容忍例外)才 Ship Phase 0,L1+L2+回归是常规质量保证。

**理由**: L3 直接验证"质量驱动假设"(三件套是否真有效),如果 L3 不达,功能再完整也没意义。

### 决策 4: 跨境电商场景是黄金标准

**问题**: template-only 行业 fixture 注定指标偏低,怎么 ship gate?

**决策**: 跨境电商场景在 L2 必过 80%、L3 五指标全过;其他行业允许偏低,但 disclaimer 必须出现。

**理由**: 跨境电商是 v2 设计的标杆场景,必须证明三件套对它有效。其他行业 hints 质量不可控,不强求。

### 决策 5: 不做 pixel-level SVG diff

**问题**: 渲染优化可能让 SVG 像素变了但内容不变。

**决策**: 只做结构化 diff(节点数、边数、文本内容)。

**理由**: 像素 diff 太敏感,会拦截无害的 layout 微调。结构化 diff 抓真实回归。

---

## 十一、与设计/Plan 的对照

| 设计 v2 章节 | Test/Eval 覆盖 |
|-------------|---------------|
| §四 三件套机制 | L3 指标 1 (澄清击中率) + 指标 4 (修订接受率) |
| §四.2 自检反问 | L3 指标 3 (自检指向准确率) |
| §五 Schema 极简 | L1 unit + L2 fixture must_have |
| §六 意图抽取 | L2 fixture detectedIntent.must_contain_themes |
| §七 hints 诚实化 | L3 场景 02/03 (template-only) 验证 disclaimer |
| §八 Validator 极简 | L1 unit (test_validate_knowledge.py 全部 10 用例) |
| §九 Render 极简 | 视觉验收（人工抽样 L3 场景的导出 SVG） |
| §十 Phase 3 推迟项 | 不在 eval 范围 |
| §十一 风险评估 | L3 五指标分别对应风险（澄清差→指标1、refine 差→指标4等） |
| §十二 向后兼容 | 回归测试 100% 通过 |

---

## 十二、后续迭代

### 12.1 Eval 数据集演进

每收集 5-10 个真实用户蓝图,选 1-2 个标注成新 fixture,数据集随时间扩大。

### 12.2 指标精度提升

如果某指标的"通过/失败"边界总是模糊（例如澄清击中率徘徊在 55-65%）,考虑：
- 提高门槛(从 60% 提到 70%)
- 增加更细粒度子指标（如"反问是否引用了具体实体名" vs "反问是否产生了实质修改"）

### 12.3 人工 verify 自动化

如果人工 verify 数据积累足够（>500 条 judge vs human 对照），可以训练一个轻量分类器自动识别"judge 失控"的 case，减少人工成本。

---

## 十三、自我审查清单

### Placeholder 扫描
✅ 无 TBD/TODO

### 可执行性
✅ L1 单测:plan v2 已包含具体代码
✅ L2 框架:fixture 模板 + judge prompt 完整
✅ L3 框架:场景剧本结构 + 五指标数学定义完整

### 客观性
✅ 全部用代理指标(behavioral)
✅ LLM judge 跨模型 + 人工抽样 verify
✅ Ship Gate 边界清晰

### Scope
✅ 只覆盖 v2 三件套 + 极简 schema 的验证
✅ Phase 3 推迟项不在 eval 范围

---

## 十四、下一步

1. 用户审查本测试设计
2. 批准后,Phase 0 实施同时启动 L1 测试
3. Phase 0 完工后跑 L2 + L3,Ship Gate 决定是否进 Phase 1
4. Phase 1/2 完工后跑全套(L1+L2+L3+回归),最终 Ship 给真实用户
5. 真实使用观察 ≥4 周,收集反馈,决定是否启动 Phase 3

---

**文档完成日期**: 2026-04-28
**关联文档**:
- 设计 v2: `references/domain-knowledge-design-v2.md`
- 实施 plan v2: `plans/2026-04-28-domain-knowledge-v2.md`
- (历史) 设计 v1: `references/domain-knowledge-entities-extension-design.md`
- (历史) 评审报告: `references/domain-knowledge-design-adversarial-review.md`
