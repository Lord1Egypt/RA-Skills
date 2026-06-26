# Skill 集成示例

## 与现有 Skills 的数据流

### 数据输入 (Input Skills)

- calculus-concept-visualizer → 学生可视化交互记录 → active-memory-calculus
- derivation-animator → 推导动画观看行为 → active-memory-calculus
- error-analyzer → 错误分析结果 → active-memory-calculus
- exam-problem-generator → 做题正确率/用时 → active-memory-calculus

### 数据输出 (Output Skills)

- active-memory-calculus → 个性化参数 → calculus-concept-visualizer
- active-memory-calculus → 难度调整建议 → exam-problem-generator
- active-memory-calculus → 薄弱点定位 → smart-review
- active-memory-calculus → 学习路径 → personal-learning

## 集成代码示例

### 示例1: Concept Visualizer 接收记忆参数

```python
async def visualize_concept(concept: str, student_id: str):
    # 1. 查询 active-memory-calculus 获取学生偏好
    memory_context = await active_memory_calculus.memory_apply(
        query=f"讲解{concept}",
        student_id=student_id,
        apply_modes=["personalization"]
    )

    # 2. 根据记忆调整可视化参数
    if memory_context.suggested_visualization == "geogebra_animation":
        return await create_geogebra_animation(concept, speed="normal")
    elif memory_ctx.pace_adjustment == "slow_detailed":
        return await create_step_by_step_visualization(concept, steps=10)
    else:
        return await create_static_diagram(concept)
```

### 示例2: Exam Problem Generator 接收难度调整

```python
async def generate_problem(topic: str, student_id: str):
    profile = await active_memory_calculus.get_student_profile(student_id)
    mastery = profile.get("concept_mastery", {}).get(topic, {})
    level = mastery.get("level", "unknown")

    if level == "proficient":
        return await create_advanced_problem(topic, variants=True)
    elif level == "struggling":
        return await create_foundation_problem(topic, hints=True)
    else:
        return await create_standard_problem(topic)
```

## 完整教学场景集成

```python
async def teach_definite_integral_application(student_id: str):
    # Step 1: 应用记忆获取个性化上下文
    memory_ctx = await active_memory_calculus.memory_apply(
        query="定积分应用 - 计算曲线围成面积",
        student_id=student_id,
        apply_modes=["personalization", "difficulty", "warning"]
    )

    # Step 2: 根据记忆选择讲解方式
    if "visual" in memory_ctx.personalization_hints:
        visualization = await calculus_concept_visualizer.create(
            topic="area_under_curve",
            style="animated",
            pace=memory_ctx.pace_adjustment or "normal"
        )

    # Step 3: 检查是否有相关错误模式需要预警
    if memory_ctx.warnings:
        warning_msg = "\n".join(memory_ctx.warnings)
        await show_warning(warning_msg)

    # Step 4: 生成适合的练习题
    problem = await exam_problem_generator.generate(
        topic="definite_integral_area",
        difficulty=memory_ctx.difficulty_adjustment,
        student_id=student_id
    )

    return {"visualization": visualization, "problem": problem}
```
