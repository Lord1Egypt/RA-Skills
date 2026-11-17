# Conventions Rubric — Discussion 学术规范评分

## 用途
本文件是 `discussion-conventions-diagnosis` 的官方评分标准。

## 评分维度（共 6 项）

### 维度 CO1: Contribution Type Identification（贡献类型识别）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | 显式 claim 1+ 种 contribution type（method / results / impact / application）|
| **4 - Good** | Contribution type 隐式但可识别 |
| **3 - Acceptable** | 部分 contribution claim |
| **2 - Needs Work** | Contribution claim 模糊 |
| **1 - Critical Fail** | 无 contribution claim |

#### 4 种 Contribution 类型
1. **Method**（方法型）：用改进/新方法得到结果
2. **Results**（结果型）：获得更好/更精确的结果
3. **Impact**（影响型）：改变研究方向/颠覆先前工作
4. **Application**（应用型）：发现新的应用场景

---

### 维度 CO2: Happy Words Appropriateness（Happy Words 恰当性）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | Happy words 适度（每 Discussion 2-3 个）；与 claim 强度匹配 |
| **4 - Good** | 偶尔略多；与 claim 匹配 |
| **3 - Acceptable** | 偶尔过度 |
| **2 - Needs Work** | happy words 过多 |
| **1 - Critical Fail** | 炫耀性语言（"groundbreaking revolution"）|

#### 反模式
- ❌ "We provide novel insights into..."（空洞 happy words）
- ✅ "Our results suggest that LWA both exists and predicts..."（具体 contribution）

---

### 维度 CO3: Achievement-Contribution Distinction（成就与贡献区分）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | Achievement（做了什么）和 Contribution（对 field 价值）清晰区分 |
| **4 - Good** | 大体区分 |
| **3 - Acceptable** | 部分区分；部分混合 |
| **2 - Needs Work** | Achievement 和 Contribution 混合 |
| **1 - Critical Fail** | 完全无区分 |

#### 测试
- 是否描述了"做了什么"（achievement）？
- 是否描述了"对 field 的价值"（contribution）？
- 两者是否清晰分工？

---

### 维度 CO4: Limitations Completeness（局限性完整性）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | 3+ 具体 limitations + 部分有反驳证据 |
| **4 - Good** | 2-3 具体 limitations |
| **3 - Acceptable** | 1-2 具体 limitations |
| **2 - Needs Work** | 1 个 generic limitation（"Our study has limitations"）|
| **1 - Critical Fail** | 无 limitations 段 |

#### Limitations 类型
- **Sample**（样本）
- **Design**（设计：cross-sectional, correlational 等）
- **Measure**（测量）
- **Generalisability**（推广性）
- **Method**（方法）

每个 limitation 应具体（不只是"sample is small"）

---

### 维度 CO5: Future Work Specificity（未来方向具体性）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | Future work 包含 what / where / method / variable 4 元素 |
| **4 - Good** | 3 元素 |
| **3 - Acceptable** | 2 元素 |
| **2 - Needs Work** | 1 元素 |
| **1 - Critical Fail** | "More research is needed" 单独成句 |

#### 4 元素
- **What**: 具体研究方向
- **Where**: 样本/地点
- **Method**: 研究方法
- **Variable**: 关注的变量

---

### 维度 CO6: Operational Specificity（操作具体性）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | Recommendation 是 operational（"if you encounter X, do Y using Z"）|
| **4 - Good** | 大体 operational |
| **3 - Acceptable** | 部分 operational |
| **2 - Needs Work** | 多处 abstract recommendation |
| **1 - Critical Fail** | 全部 abstract |

#### Operational recommendation 模式
- ✅ "Researchers should compare networks based on polychoric with Spearman..."
- ❌ "Researchers should be careful..."

---

## 总分计算

**总分 = (CO1 + CO2 + CO3 + CO4 + CO5 + CO6) / 6 × 20** （满分 100）

| 总分区间 | 评级 |
|---|---|
| 90-100 | Excellent |
| 75-89 | Good |
| 60-74 | Acceptable |
| 40-59 | Needs Work |
| <40 | Critical |

---

## 相关 example 文件

- `examples/good_midgley_2020_three_contributions.md` — CO1 范例
- `examples/good_costello_2021_results_contribution.md` — CO1/CO3 范例
- `examples/good_ebert_2020_limitations_future.md` — CO4/CO5 范例
- `examples/good_epskamp_2018_method_contribution.md` — CO1/CO6 范例
- `examples/bad_synthetic_no_limitations.md` — CO4 反例
- `examples/bad_synthetic_vague_achievement.md` — CO1/CO2 反例