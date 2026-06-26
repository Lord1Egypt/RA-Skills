# Concept Explainer Template

## 概念: {{ concept_name }}
## 学生水平: {{ student_level }}
## 困难预测: {{ predicted_difficulty }}

---

## 教学策略设计

### 阶段 1: 直观感知 (Concrete)
**目标**: 建立几何直觉，不涉及符号

**活动**:
1. 调用 `generate_geogebra` 生成动态演示
   - concept: {{ concept_geogebra_type }}
   - interactive_elements: [{{ interactive_params }}]

2. 引导学生操作:
   - "请拖动 {{ slider_name }} 滑块，观察 {{ observation_target }} 的变化"
   - "你发现了什么规律？"

**关键提问**:
- 视觉上你看到了什么模式？
- 当 {{ param1 }} 变化时，{{ param2 }} 如何响应？

---

### 阶段 2: 数值探索 (Numerical)
**目标**: 通过计算验证直觉

**活动**:
1. 生成数值表格:
   ```
   | x       | f(x)    | |x-a|   | |f(x)-L| |
   |---------|---------|---------|----------|
   | 0.1     | ...     | 0.1     | ...      |
   | 0.01    | ...     | 0.01    | ...      |
   | 0.001   | ...     | 0.001   | ...      |
   ```

2. 观察趋势:
   - "当 x 越来越接近 {{ a }}，f(x) 越来越接近 {{ L }}"
   - 量化观察: "误差缩小了 10 倍"

---

### 阶段 3: 几何理解 (Visual Formalization)
**目标**: 连接数值与几何

**活动**:
1. 调用 `plot_interactive`:
   - type: {{ plot_type }}
   - 高亮关键区域
   - 动态标注

2. 多表征对应:
   - 数值表格中的列 ↔ 图形中的区域
   - 代数表达式 ↔ 几何度量

---

### 阶段 4: 代数形式化 (Abstract)
**目标**: 引入严格数学定义

**渐进形式化**:
1. **直观描述**: "f(x) 可以任意接近 L"
2. **半形式化**: "只要 x 足够接近 a，f(x) 就接近 L"
3. **量化**: "对于任意小的误差 ε..."
4. **严格定义**: "∀ε>0, ∃δ>0, ..."

**调用 `step_builder`**:
- derivation_type: {{ derivation_type }}
- 分步展示证明/推导过程

---

### 阶段 5: 即时检测 (Assessment)
**目标**: 验证理解，诊断误区

**调用 `generate_quiz`**:
- concept: {{ concept_name }}
- difficulty: {{ difficulty }}

**题目层次**:
1. **识别题**: 概念辨析（30分）
2. **应用题**: 直接计算/证明（40分）
3. **迁移题**: 变式/综合（30分）

---

### 阶段 6: 误区诊断 (Diagnosis)
**目标**: 识别并纠正错误理解

**调用 `diagnose_misconception`**:
- 分析学生回答
- 匹配常见误区库

**常见误区预警**:
{{ misconception_warnings }}

---

## 特殊处理

### 针对 {{ concept_name }} 的认知冲突设计

**反例 1**: {{ counter_example_1 }}
- 目的: 打破 {{ misconception_1 }}
- 可视化: {{ counter_viz_1 }}

**反例 2**: {{ counter_example_2 }}
- 目的: 打破 {{ misconception_2 }}
- 可视化: {{ counter_viz_2 }}

---

## 输出格式

### 1. 解释文本
```markdown
## {{ concept_name }} 的渐进理解

### 直观理解
[几何描述，配 GeoGebra 交互]

### 数值验证
[计算表格，展示趋势]

### 严格定义
[形式化定义，分步推导]

### 常见误区
[误区诊断与干预]
```

### 2. 工具调用清单
- [ ] generate_geogebra: {{ geogebra_params }}
- [ ] plot_interactive: {{ plot_params }}
- [ ] step_builder: {{ step_params }}
- [ ] generate_quiz: {{ quiz_params }}

### 3. 学生交互指令
1. 打开 GeoGebra 演示
2. 拖动 {{ param }} 滑块至 {{ value }}
3. 观察 {{ target }} 的变化
4. 记录你的发现
5. 完成 3 道检测题

---

## 评估标准

学生理解达标的标准:
- [ ] 能用自己的话解释概念（非背诵定义）
- [ ] 能在 GeoGebra 中操作验证条件
- [ ] 能识别错误表述（检测题正确率≥80%）
- [ ] 能解决变式问题（迁移题正确）

---

*模板版本: 1.0.0*
*作者: 代国兴*
