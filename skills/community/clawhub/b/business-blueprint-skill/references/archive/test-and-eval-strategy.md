# Schema重构测试与评估方案

**文档版本**：v1  
**创建日期**：2026-04-25  
**目标**：量化证明schema重构（意图解析 + 规则引擎）相比旧方案（硬编码关键词）的真实效果提升

---

## 一、核心问题：如何证明"效果提升"？

### 不能只看表面指标

❌ **错误做法**：
- 只看"strict validate多过了几条" → 不证明真实效果
- 只看"配置文件更灵活了" → 不证明用户体验改善
- 只看"代码重构完成了" → 不证明输出质量提升

✅ **正确做法**（借鉴标题优化协议）：
必须同时证明三件事：

1. **覆盖率提升**：新方案能正确处理旧方案无法处理的场景
2. **准确率提升**：新方案在相同场景下输出更准确
3. **用户体验改善**：新方案减少了用户的手动干预/配置负担

---

## 二、测试架构：三层验证体系

```
Layer 1: Structural Validation（结构正确性）
    ↓
Layer 2: Semantic Accuracy（语义准确性）
    ↓
Layer 3: User Experience（用户体验）
```

### Layer 1: Structural Validation

**目标**：证明新系统不破坏现有功能，迁移后输出结构稳定

**测试类型**：
- **Migration Consistency Test**：迁移后蓝图输出是否一致？
- **Backward Compatibility Test**：旧蓝图在新系统是否仍可用？
- **Golden Fixture Validation**：关键场景输出是否稳定？

### Layer 2: Semantic Accuracy

**目标**：证明新系统输出的分层结果更准确、更符合用户意图

**测试类型**：
- **Intent Inference Accuracy**：意图推断是否正确？
- **Layer Assignment Accuracy**：系统归属层级是否准确？
- **Conflict Resolution Accuracy**：冲突场景是否正确解决？
- **Industry Overlay Accuracy**：行业叠加是否正确？

### Layer 3: User Experience

**目标**：证明新系统减少了用户手动干预，提升了易用性

**测试类型**：
- **Auto-Selection Success Rate**：自动选择策略的成功率
- **Manual Intervention Reduction**：手动干预次数减少量
- **Review Load Reduction**：需复核场景减少量

---

## 三、测试数据集设计

### 数据集分类

```
test_data/
├── golden_fixtures/        # Golden标准集（迁移验证）
│   ├── product_blueprints/ # 产品蓝图（10个）
│   ├── technical_blueprints/ # 技术蓝图（5个）
│   └── industry_blueprints/ # 行业蓝图（金融5、制造5、零售5）
│
├── edge_cases/            # 边缘场景集（挑战性测试）
│   ├── conflicts/         # 冲突场景（支付风控网关、客服CRM系统等）
│   ├── ambiguous_goals/   # 模糊目标（"展示系统架构"）
│   └── multi_industry/    # 多行业混合（金融+制造）
│
├── user_scenarios/        # 用户场景集（用户体验测试）
│   ├── product_manager/   # 产品经理场景（5个）
│   ├── technical_lead/    # 技术负责人场景（5个）
│   └── industry_expert/   # 行业专家场景（5个）
│
└── regression_tests/      # 回归测试集
    └── all_blueprints/    # 所有历史蓝图（防止回归）
```

### 数据集来源

1. **Golden Fixtures**：
   - 从现有demos/目录选择代表性蓝图
   - 手动标注预期输出（意图、层级归属）
   - 用于迁移验证和基础准确率测试

2. **Edge Cases**：
   - 人工构造挑战性场景
   - 覆盖冲突、模糊、混合等边界
   - 用于压力测试新系统

3. **User Scenarios**：
   - 模拟真实用户工作流
   - 包含goals、scope、sourceRefs完整输入
   - 用于用户体验测试

4. **Regression Tests**：
   - 所有历史生成的蓝图
   - 用于防止系统更新后的回归

---

## 四、评估指标设计

### 指标分类（参考标题优化协议）

```
Primary Metrics（主要指标）
├── Intent Inference Accuracy
├── Layer Assignment Accuracy
└── Auto-Selection Success Rate
    │
Secondary Metrics（次要指标）
├── Conflict Resolution Correctness
├── Industry Overlay Accuracy
└── Manual Intervention Reduction
    │
Guardrail Metrics（护栏指标）
├── Migration Consistency Rate
├── Backward Compatibility Rate
└── Regression Test Pass Rate
```

### Primary Metrics（主要指标）

#### 1. Intent Inference Accuracy

**定义**：系统推断的意图与人工标注意图的匹配率

**计算**：
```python
def intent_accuracy(predicted_intent, ground_truth_intent):
    """计算意图推断准确率"""
    if predicted_intent["primary"] == ground_truth_intent["primary"]:
        base_score = 1.0
    else:
        base_score = 0.0

    # 如果有secondary，额外检查
    if ground_truth_intent.get("secondary"):
        if predicted_intent.get("secondary") == ground_truth_intent["secondary"]:
            return base_score + 0.2  # 完全匹配
        else:
            return base_score * 0.8  # primary对了，secondary错了
    
    return base_score

# 整体准确率
def overall_intent_accuracy(test_set):
    scores = [intent_accuracy(pred, truth) for pred, truth in test_set]
    return sum(scores) / len(scores)
```

**目标**：
- Phase 0（迁移）：>= 0.70（简单关键词推断）
- Phase 1（意图解析）：>= 0.85（关键词+启发式）
- Phase 4（语义分析）：>= 0.92（TF-IDF+语义）

#### 2. Layer Assignment Accuracy

**定义**：系统归属的层级与人工标注层级的匹配率

**计算**：
```python
def layer_accuracy(predicted_layers, ground_truth_layers):
    """计算层级归属准确率"""
    systems = ground_truth_layers.keys()
    correct = sum(
        predicted_layers.get(sys) == ground_truth_layers[sys]
        for sys in systems
    )
    return correct / len(systems)

# 层级距离惩罚（错分距离越远，惩罚越大）
def weighted_layer_accuracy(predicted_layers, ground_truth_layers, layer_order):
    """加权准确率：考虑层级距离"""
    total_score = 0
    for sys, truth_layer in ground_truth_layers.items():
        pred_layer = predicted_layers.get(sys)
        if pred_layer == truth_layer:
            total_score += 1.0
        else:
            # 错分惩罚：距离越远，惩罚越大
            pred_idx = layer_order.index(pred_layer)
            truth_idx = layer_order.index(truth_layer)
            distance = abs(pred_idx - truth_idx)
            penalty = min(distance / (len(layer_order) - 1), 0.8)
            total_score += 1.0 - penalty
    
    return total_score / len(ground_truth_layers)
```

**目标**：
- Phase 0（迁移）：>= 0.80（保持旧逻辑）
- Phase 1（规则引擎）：>= 0.88（typed signals）
- Phase 4（优化权重）：>= 0.95

#### 3. Auto-Selection Success Rate

**定义**：用户无需手动干预即可获得正确策略的比例

**计算**：
```python
def auto_selection_success(test_set):
    """计算自动选择成功率"""
    success_count = 0
    for test in test_set:
        # 系统自动选择策略
        auto_strategy = infer_strategy(test["goals"])
        
        # 正确策略（人工标注）
        correct_strategy = test["ground_truth_strategy"]
        
        # 用户是否满意（不需要手动干预）
        if auto_strategy == correct_strategy:
            success_count += 1
        elif test["confidence"] >= 0.75 and auto_strategy["primary"] == correct_strategy["primary"]:
            # primary对了，即使secondary不同，用户通常接受
            success_count += 0.8
        elif test["confidence"] < 0.75 and test["manual_correction"] == auto_strategy:
            # 低置信度追问后，用户确认正确
            success_count += 0.5  # 算半个成功（追问了但正确）
    
    return success_count / len(test_set)
```

**目标**：
- Phase 1（意图解析）：>= 0.70（产品经理场景）
- Phase 2（优化启发式）：>= 0.80
- Phase 4（语义分析）：>= 0.90

---

### Secondary Metrics（次要指标）

#### 4. Conflict Resolution Correctness

**定义**：冲突场景下，系统选择层级的合理性

**计算**：
```python
def conflict_resolution_accuracy(conflict_cases):
    """计算冲突解决准确率"""
    correct_count = 0
    for case in conflict_cases:
        # 系统选择的层级
        resolved_layer = rule_engine.assign_layer(case["system"])
        
        # 合理层级（可能有多个合理选择）
        reasonable_layers = case["reasonable_layers"]  # ["risk-control", "gateway"]
        
        # 是否选择了一个合理层级
        if resolved_layer in reasonable_layers:
            # 如果有"最优层级"，检查是否选中
            if case.get("best_layer"):
                if resolved_layer == case["best_layer"]:
                    correct_count += 1.0  # 完美
                else:
                    correct_count += 0.8  # 合理但非最优
            else:
                correct_count += 0.9  # 合理选择
        else:
            correct_count += 0  # 错误选择
    
    return correct_count / len(conflict_cases)
```

**目标**：>= 0.85（Phase 1）

#### 5. Industry Overlay Accuracy

**定义**：行业叠加是否正确应用

**计算**：
```python
def overlay_accuracy(test_set):
    """计算行业叠加准确率"""
    correct_count = 0
    for test in test_set:
        if not test.get("expected_overlay"):
            continue  # 无行业叠加
        
        # 系统检测的行业overlay
        detected_overlay = detect_industry(test["goals"])
        
        # 预期overlay
        expected_overlay = test["expected_overlay"]
        
        if detected_overlay == expected_overlay:
            # overlay正确，检查调整是否正确
            adjustments = test["adjustments"]
            correct_adjustments = sum(
                1 for adj in adjustments
                if rule_engine.apply_overlay(adj) == adj["expected_result"]
            )
            correct_count += correct_adjustments / len(adjustments)
        else:
            correct_count += 0  # overlay检测错误
    
    return correct_count / len(test_set)
```

**目标**：>= 0.90（Phase 1）

#### 6. Manual Intervention Reduction

**定义**：相比旧方案，用户手动干预次数的减少量

**计算**：
```python
def intervention_reduction(old_system, new_system, test_set):
    """计算手动干预减少量"""
    old_interventions = 0
    new_interventions = 0
    
    for test in test_set:
        # 旧系统：用户需要手动指定策略
        if old_system.needs_manual_strategy(test):
            old_interventions += 1
        
        # 新系统：用户需要手动干预（低置信度追问或手动修正）
        if new_system.needs_manual_intervention(test):
            new_interventions += 1
    
    reduction_rate = (old_interventions - new_interventions) / old_interventions
    return reduction_rate
```

**目标**：>= 0.40（减少40%手动干预）

---

### Guardrail Metrics（护栏指标）

#### 7. Migration Consistency Rate

**定义**：迁移后蓝图输出与旧输出的一致性

**计算**：
```python
def migration_consistency(golden_fixtures):
    """计算迁移一致性"""
    consistent_count = 0
    for fixture in golden_fixtures:
        # 旧系统输出
        old_output = export_svg(fixture["old_blueprint"])
        
        # 迁移后蓝图 + 新系统输出
        migrated_blueprint = migrate(fixture["old_blueprint"])
        new_output = export_svg(migrated_blueprint)
        
        # 比对结构差异
        diff = compare_structure(old_output, new_output)
        
        # 允许的变更：分层逻辑改进（不超过20%系统换层）
        # 不允许：路由完全变化（泳道变成海报）
        if diff.route == old_output.route and diff.layer_changes < 0.2:
            consistent_count += 1
        elif diff.layer_changes >= 0.2:
            consistent_count += 0  # 回归：太多系统换层
        else:
            consistent_count += 0.5  # 部分一致
    
    return consistent_count / len(golden_fixtures)
```

**目标**：>= 0.95（95%一致性）

#### 8. Backward Compatibility Rate

**定义**：旧蓝图在新系统是否仍可用

**计算**：
```python
def backward_compatibility(old_blueprints):
    """计算向后兼容性"""
    compatible_count = 0
    for blueprint in old_blueprints:
        try:
            # 新系统处理旧蓝图
            output = export_svg(blueprint)
            
            # 检查是否有错误或异常
            if output and output.route in VALID_ROUTES:
                compatible_count += 1
        except Exception:
            compatible_count += 0
    
    return compatible_count / len(old_blueprints)
```

**目标**：>= 0.99（99%兼容）

#### 9. Regression Test Pass Rate

**定义**：所有历史蓝图在新系统的回归测试通过率

**计算**：
```python
def regression_pass_rate(all_blueprints):
    """计算回归测试通过率"""
    passed_count = 0
    for blueprint in all_blueprints:
        # 新系统导出
        new_output = export_svg(blueprint)
        
        # 如果有历史输出，比对
        if blueprint.get("historical_output"):
            old_output = blueprint["historical_output"]
            diff = compare_structure(old_output, new_output)
            
            # 允许改进，不允许回归
            if diff.is_improvement or diff.is_equal:
                passed_count += 1
            else:
                passed_count += 0  # 回归
        else:
            # 无历史输出，检查基本正确性
            if validate_output(new_output):
                passed_count += 1
    
    return passed_count / len(all_blueprints)
```

**目标**：>= 0.98（98%通过）

---

## 五、测试流程设计

### Phase 0: 迁移验证测试

**流程**：
```python
def phase0_migration_test():
    """Phase 0测试：迁移验证"""
    
    # 1. 准备Golden Fixtures
    fixtures = load_golden_fixtures("test_data/golden_fixtures/")
    
    # 2. 迁移所有fixtures
    migrated = [migrate_blueprint_v1_to_v2(f) for f in fixtures]
    
    # 3. 双跑比对
    results = []
    for old_bp, new_bp in zip(fixtures, migrated):
        old_output = export_svg(old_bp)
        new_output = export_svg(new_bp)
        diff = compare_structure(old_output, new_output)
        results.append(diff)
    
    # 4. 计算Migration Consistency Rate
    consistency = migration_consistency(fixtures)
    
    # 5. 检查是否达标
    assert consistency >= 0.95, f"迁移一致性不达标：{consistency} < 0.95"
    
    # 6. 生成报告
    report = {
        "consistency_rate": consistency,
        "layer_changes": [r.layer_changes for r in results],
        "route_changes": [r.route_change for r in results],
        "failed_cases": [r for r in results if r.layer_changes >= 0.2]
    }
    
    return report
```

**成功标准**：
- ✅ Migration Consistency Rate >= 0.95
- ✅ 无路由完全变化案例
- ✅ 层级变化不超过20%（单个蓝图）

---

### Phase 1: 意图解析 + 规则引擎测试

**流程**：
```python
def phase1_accuracy_test():
    """Phase 1测试：意图解析和层级准确率"""
    
    # 1. 准备测试集
    test_set = load_test_set("test_data/user_scenarios/")
    edge_cases = load_test_set("test_data/edge_cases/")
    
    # 2. 意图推断测试
    intent_results = []
    for test in test_set:
        predicted_intent = intent_resolver.analyze_goals(test["goals"])
        ground_truth_intent = test["ground_truth_intent"]
        accuracy = intent_accuracy(predicted_intent, ground_truth_intent)
        intent_results.append({
            "test": test,
            "predicted": predicted_intent,
            "ground_truth": ground_truth_intent,
            "accuracy": accuracy
        })
    
    # 3. 层级归属测试
    layer_results = []
    for test in test_set:
        # 加载策略
        strategy = load_strategy(test["ground_truth_intent"]["primary"])
        overlay = load_overlay(test["ground_truth_intent"].get("secondary"))
        
        # 规则引擎分配层级
        predicted_layers = {
            sys["id"]: rule_engine.assign_layer(sys, strategy, overlay)["layer"]
            for sys in test["systems"]
        }
        
        ground_truth_layers = test["ground_truth_layers"]
        accuracy = weighted_layer_accuracy(predicted_layers, ground_truth_layers, strategy["layer_order"])
        
        layer_results.append({
            "test": test,
            "predicted": predicted_layers,
            "ground_truth": ground_truth_layers,
            "accuracy": accuracy
        })
    
    # 4. 自动选择测试
    auto_results = []
    for test in test_set:
        auto_strategy = infer_strategy(test["goals"])
        correct_strategy = test["ground_truth_strategy"]
        success = auto_selection_success([(auto_strategy, correct_strategy)])
        auto_results.append({
            "test": test,
            "auto_strategy": auto_strategy,
            "correct_strategy": correct_strategy,
            "success": success
        })
    
    # 5. 冲突场景测试
    conflict_results = []
    for case in edge_cases["conflicts"]:
        resolved_layer = rule_engine.assign_layer(case["system"])
        reasonable_layers = case["reasonable_layers"]
        correctness = conflict_resolution_accuracy([{
            "system": case["system"],
            "resolved_layer": resolved_layer,
            "reasonable_layers": reasonable_layers,
            "best_layer": case.get("best_layer")
        }])
        conflict_results.append({
            "case": case,
            "resolved": resolved_layer,
            "reasonabl": reasonable_layers,
            "correctness": correctness
        })
    
    # 6. 计算整体指标
    overall_intent_accuracy = sum(r["accuracy"] for r in intent_results) / len(intent_results)
    overall_layer_accuracy = sum(r["accuracy"] for r in layer_results) / len(layer_results)
    overall_auto_success = sum(r["success"] for r in auto_results) / len(auto_results)
    overall_conflict_correctness = sum(r["correctness"] for r in conflict_results) / len(conflict_results)
    
    # 7. 检查是否达标
    assert overall_intent_accuracy >= 0.85, f"意图准确率不达标：{overall_intent_accuracy} < 0.85"
    assert overall_layer_accuracy >= 0.88, f"层级准确率不达标：{overall_layer_accuracy} < 0.88"
    assert overall_auto_success >= 0.70, f"自动选择成功率不达标：{overall_auto_success} < 0.70"
    assert overall_conflict_correctness >= 0.85, f"冲突解决准确率不达标：{overall_conflict_correctness} < 0.85"
    
    # 8. 生成报告
    report = {
        "intent_accuracy": overall_intent_accuracy,
        "layer_accuracy": overall_layer_accuracy,
        "auto_success_rate": overall_auto_success,
        "conflict_correctness": overall_conflict_correctness,
        "failed_intent_cases": [r for r in intent_results if r["accuracy"] < 0.7],
        "failed_layer_cases": [r for r in layer_results if r["accuracy"] < 0.8]
    }
    
    return report
```

**成功标准**：
- ✅ Intent Inference Accuracy >= 0.85
- ✅ Layer Assignment Accuracy >= 0.88
- ✅ Auto-Selection Success Rate >= 0.70
- ✅ Conflict Resolution Correctness >= 0.85

---

### Phase 2: 行业叠加测试

**流程**：
```python
def phase2_overlay_test():
    """Phase 2测试：行业叠加准确率"""
    
    # 1. 准备行业测试集
    industry_tests = load_test_set("test_data/golden_fixtures/industry_blueprints/")
    
    # 2. Overlay检测测试
    overlay_results = []
    for test in industry_tests:
        detected_overlay = intent_resolver.detect_industry_overlay(test["goals"])
        expected_overlay = test["expected_overlay"]
        
        # Overlay应用测试
        if detected_overlay == expected_overlay:
            strategy = load_strategy(test["ground_truth_intent"]["primary"])
            overlay = load_overlay(detected_overlay)
            
            # 检查调整是否正确
            adjustments_results = []
            for adjustment in test["adjustments"]:
                system = adjustment["system"]
                predicted_layer = rule_engine.assign_layer(system, strategy, overlay)["layer"]
                expected_layer = adjustment["expected_layer"]
                correct = predicted_layer == expected_layer
                adjustments_results.append({
                    "system": system,
                    "predicted": predicted_layer,
                    "expected": expected_layer,
                    "correct": correct
                })
            
            overlay_results.append({
                "test": test,
                "detected_overlay": detected_overlay,
                "expected_overlay": expected_overlay,
                "adjustments": adjustments_results,
                "overlay_correct": True
            })
        else:
            overlay_results.append({
                "test": test,
                "detected_overlay": detected_overlay,
                "expected_overlay": expected_overlay,
                "overlay_correct": False
            })
    
    # 3. 计算整体指标
    overlay_accuracy = sum(
        1 if r["overlay_correct"] else 0
        for r in overlay_results
    ) / len(overlay_results)
    
    adjustment_accuracy = sum(
        sum(1 if adj["correct"] else 0 for adj in r["adjustments"]) / len(r["adjustments"])
        for r in overlay_results if r["overlay_correct"]
    ) / len([r for r in overlay_results if r["overlay_correct"]])
    
    # 4. 检查是否达标
    assert overlay_accuracy >= 0.90, f"Overlay检测准确率不达标：{overlay_accuracy} < 0.90"
    assert adjustment_accuracy >= 0.85, f"调整准确率不达标：{adjustment_accuracy} < 0.85"
    
    # 5. 生成报告
    report = {
        "overlay_accuracy": overlay_accuracy,
        "adjustment_accuracy": adjustment_accuracy,
        "failed_overlay_cases": [r for r in overlay_results if not r["overlay_correct"]],
        "failed_adjustment_cases": [
            adj for r in overlay_results if r["overlay_correct"]
            for adj in r["adjustments"] if not adj["correct"]
        ]
    }
    
    return report
```

**成功标准**：
- ✅ Overlay Accuracy >= 0.90
- ✅ Adjustment Accuracy >= 0.85

---

### Phase 3: 回归测试

**流程**：
```python
def phase3_regression_test():
    """Phase 3测试：防止回归"""
    
    # 1. 加载所有历史蓝图
    all_blueprints = load_all_blueprints("demos/", "test_data/")
    
    # 2. 批量导出
    results = []
    for blueprint in all_blueprints:
        try:
            output = export_svg(blueprint)
            
            # 如果有历史输出，比对
            if blueprint.get("historical_output"):
                diff = compare_structure(blueprint["historical_output"], output)
                passed = diff.is_improvement or diff.is_equal
            else:
                passed = validate_output(output)
            
            results.append({
                "blueprint": blueprint,
                "output": output,
                "passed": passed
            })
        except Exception as e:
            results.append({
                "blueprint": blueprint,
                "error": str(e),
                "passed": False
            })
    
    # 3. 计算通过率
    pass_rate = sum(1 if r["passed"] else 0 for r in results) / len(results)
    
    # 4. 检查是否达标
    assert pass_rate >= 0.98, f"回归测试通过率不达标：{pass_rate} < 0.98"
    
    # 5. 生成报告
    report = {
        "pass_rate": pass_rate,
        "failed_cases": [r for r in results if not r["passed"]],
        "error_cases": [r for r in results if r.get("error")]
    }
    
    return report
```

**成功标准**：
- ✅ Regression Test Pass Rate >= 0.98
- ✅ 无新增错误案例

---

## 六、A/B对比实验设计

### 实验目的

**证明新系统相比旧系统的真实提升**：
- 不是看"代码重构完成了"，而是看"输出质量是否改善"
- 不是看"配置更灵活了"，而是看"用户体验是否提升"

### 实验设计

```python
def ab_comparison_experiment():
    """A/B对比实验：旧系统 vs 新系统"""
    
    # 1. 准备测试集（覆盖各场景）
    test_set = load_test_set("test_data/user_scenarios/")
    
    # 2. 旧系统（硬编码关键词推断）
    old_system_results = []
    for test in test_set:
        # 旧系统：硬编码推断层级
        old_intent = infer_legacy_intent(test["goals"])  # 简单关键词
        old_layers = infer_legacy_layers(test["systems"])  # 硬编码关键词表
        old_output = export_with_legacy_logic(test["blueprint"])
        
        # 用户满意度（模拟）
        user_satisfied = (
            old_intent == test["ground_truth_intent"] and
            compare_layers(old_layers, test["ground_truth_layers"]) >= 0.8
        )
        
        old_system_results.append({
            "test": test,
            "intent": old_intent,
            "layers": old_layers,
            "output": old_output,
            "user_satisfied": user_satisfied
        })
    
    # 3. 新系统（意图解析 + 规则引擎）
    new_system_results = []
    for test in test_set:
        # 新系统：意图解析 + typed signals + score
        new_intent = intent_resolver.analyze_goals(test["goals"])
        new_layers = rule_engine.assign_layers(
            test["systems"],
            load_strategy(new_intent["primary"]),
            load_overlay(new_intent.get("secondary"))
        )
        new_output = export_with_new_logic(test["blueprint"], new_intent)
        
        # 用户满意度（模拟）
        user_satisfied = (
            new_intent["primary"] == test["ground_truth_intent"]["primary"] and
            compare_layers(new_layers, test["ground_truth_layers"]) >= 0.9 and
            new_intent["confidence"] >= 0.75  # 高置信度
        )
        
        new_system_results.append({
            "test": test,
            "intent": new_intent,
            "layers": new_layers,
            "output": new_output,
            "user_satisfied": user_satisfied
        })
    
    # 4. 对比分析
    comparison = {
        "intent_accuracy": {
            "old": sum(1 if r["intent"]["primary"] == r["test"]["ground_truth_intent"]["primary"] for r in old_system_results) / len(old_system_results),
            "new": sum(1 if r["intent"]["primary"] == r["test"]["ground_truth_intent"]["primary"] for r in new_system_results) / len(new_system_results)
        },
        "layer_accuracy": {
            "old": sum(compare_layers(r["layers"], r["test"]["ground_truth_layers"]) for r in old_system_results) / len(old_system_results),
            "new": sum(compare_layers(r["layers"], r["test"]["ground_truth_layers"]) for r in new_system_results) / len(new_system_results)
        },
        "user_satisfaction": {
            "old": sum(1 if r["user_satisfied"] else 0 for r in old_system_results) / len(old_system_results),
            "new": sum(1 if r["user_satisfied"] else 0 for r in new_system_results) / len(new_system_results)
        },
        "manual_intervention": {
            "old": sum(1 if r["intent"]["confidence"] < 0.5 else 0 for r in old_system_results),  # 旧系统无置信度，全部算手动
            "new": sum(1 if r["intent"]["confidence"] < 0.75 else 0 for r in new_system_results)  # 新系统低置信度需追问
        }
    }
    
    # 5. 计算提升幅度
    improvement = {
        "intent_accuracy_lift": comparison["intent_accuracy"]["new"] - comparison["intent_accuracy"]["old"],
        "layer_accuracy_lift": comparison["layer_accuracy"]["new"] - comparison["layer_accuracy"]["old"],
        "user_satisfaction_lift": comparison["user_satisfaction"]["new"] - comparison["user_satisfaction"]["old"],
        "manual_intervention_reduction": comparison["manual_intervention"]["old"] - comparison["manual_intervention"]["new"]
    }
    
    # 6. 检查是否达标
    assert improvement["intent_accuracy_lift"] >= 0.10, f"意图准确率提升不足：{improvement['intent_accuracy_lift']} < 0.10"
    assert improvement["layer_accuracy_lift"] >= 0.08, f"层级准确率提升不足：{improvement['layer_accuracy_lift']} < 0.08"
    assert improvement["user_satisfaction_lift"] >= 0.15, f"用户满意度提升不足：{improvement['user_satisfaction_lift']} < 0.15"
    
    # 7. 生成对比报告
    report = {
        "comparison": comparison,
        "improvement": improvement,
        "statistical_significance": calculate_p_value(old_system_results, new_system_results),
        "confidence_interval": calculate_confidence_interval(improvement)
    }
    
    return report
```

**成功标准**：
- ✅ Intent Accuracy提升 >= 10%
- ✅ Layer Accuracy提升 >= 8%
- ✅ User Satisfaction提升 >= 15%
- ✅ 统计显著性 p < 0.05

---

## 七、测试自动化与CI集成

### 测试脚本结构

```
scripts/business_blueprint/tests/
├── phase0_migration_test.py
├── phase1_accuracy_test.py
├── phase2_overlay_test.py
├── phase3_regression_test.py
├── ab_comparison_experiment.py
├── test_utils.py          # 工具函数
├── metrics.py             # 指标计算
└── generate_report.py     # 报告生成
```

### CI流程集成

```yaml
# .github/workflows/schema_test.yml

name: Schema Refactor Tests

on:
  push:
    paths:
      - 'scripts/business_blueprint/**'
      - 'references/**'
      - 'test_data/**'

jobs:
  migration_test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Phase 0 - Migration Test
        run: python scripts/business_blueprint/tests/phase0_migration_test.py
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: phase0-report
          path: reports/phase0_migration_report.json

  accuracy_test:
    needs: migration_test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Phase 1 - Accuracy Test
        run: python scripts/business_blueprint/tests/phase1_accuracy_test.py
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: phase1-report
          path: reports/phase1_accuracy_report.json

  overlay_test:
    needs: accuracy_test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Phase 2 - Overlay Test
        run: python scripts/business_blueprint/tests/phase2_overlay_test.py
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: phase2-report
          path: reports/phase2_overlay_report.json

  regression_test:
    needs: overlay_test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Phase 3 - Regression Test
        run: python scripts/business_blueprint/tests/phase3_regression_test.py
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: phase3-report
          path: reports/phase3_regression_report.json

  ab_comparison:
    needs: regression_test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: A/B Comparison Experiment
        run: python scripts/business_blueprint/tests/ab_comparison_experiment.py
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: ab-report
          path: reports/ab_comparison_report.json
```

---

## 八、评估报告模板

### 报告结构

```json
{
  "test_phase": "Phase 1",
  "test_date": "2026-04-25",
  "test_set": {
    "total_cases": 30,
    "product_scenarios": 10,
    "technical_scenarios": 5,
    "industry_scenarios": 15
  },
  "primary_metrics": {
    "intent_inference_accuracy": 0.88,
    "layer_assignment_accuracy": 0.90,
    "auto_selection_success_rate": 0.75
  },
  "secondary_metrics": {
    "conflict_resolution_correctness": 0.87,
    "industry_overlay_accuracy": 0.92,
    "manual_intervention_reduction": 0.45
  },
  "guardrail_metrics": {
    "migration_consistency_rate": 0.96,
    "backward_compatibility_rate": 0.99,
    "regression_test_pass_rate": 0.98
  },
  "failed_cases": [
    {
      "test_id": "product-007",
      "reason": "goals模糊：'展示系统架构'，无法判定primary",
      "predicted_intent": {"primary": "product", "confidence": 0.65},
      "ground_truth_intent": {"primary": "technical"},
      "improvement_suggestion": "添加追问机制：'您的蓝图更侧重产品能力还是技术调用链路？'"
    }
  ],
  "improvement_analysis": {
    "intent_accuracy_lift": 0.12,
    "layer_accuracy_lift": 0.09,
    "user_satisfaction_lift": 0.18,
    "statistical_significance": {
      "p_value": 0.023,
      "confidence_level": "95%"
    }
  },
  "next_phase_recommendation": {
    "pass_phase1": true,
    "issues_to_fix": ["goals模糊场景追问机制"],
    "phase2_prerequisites": "修复追问机制后，进入Phase 2测试"
  }
}
```

---

## 九、成功标准总表

| Phase | 主要指标 | 目标值 | 护栏指标 | 目标值 |
|-------|---------|-------|---------|-------|
| **Phase 0** | Migration Consistency | >= 0.95 | Backward Compatibility | >= 0.99 |
| **Phase 1** | Intent Accuracy | >= 0.85 | Regression Pass Rate | >= 0.98 |
|  | Layer Accuracy | >= 0.88 |  |  |
|  | Auto-Selection Success | >= 0.70 |  |  |
|  | Conflict Correctness | >= 0.85 |  |  |
| **Phase 2** | Overlay Accuracy | >= 0.90 |  |  |
|  | Adjustment Accuracy | >= 0.85 |  |  |
| **A/B对比** | Intent Lift | >= 10% | 统计显著性 p < 0.05 |  |
|  | Layer Lift | >= 8% |  |  |
|  | Satisfaction Lift | >= 15% |  |  |

---

## 十、总结：如何确保"真正提升效果"

### 三层验证体系

```
Layer 1: 结构正确性
    → 确保不破坏现有功能（Migration Consistency >= 0.95）

Layer 2: 语义准确性
    → 确保输出质量改善（Intent Accuracy >= 0.85, Layer Accuracy >= 0.88）

Layer 3: 用户体验
    → 确保易用性提升（Auto-Selection Success >= 0.70, Manual Intervention Reduction >= 40%）
```

### A/B对比证明

```
Old System（硬编码关键词）
    ↓
vs
    ↓
New System（意图解析 + 规则引擎）

结果：Intent Accuracy提升 >= 10%, User Satisfaction提升 >= 15%
统计显著性：p < 0.05
```

### 持续验证机制

```
每次代码变更 → 自动运行Phase 0-3测试
    ↓
指标达标 → 通过CI，允许合并
    ↓
指标不达标 → 阻止合并，输出失败案例和修复建议
```

---

**文档创建日期**：2026-04-25  
**下一步**：实施测试脚本 + CI集成