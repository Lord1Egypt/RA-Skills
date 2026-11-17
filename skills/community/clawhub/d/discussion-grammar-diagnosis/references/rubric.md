# Grammar Rubric — Discussion 语法评分

## 用途
本文件是 `discussion-grammar-diagnosis` 的官方评分标准。

## 评分维度（共 7 项）

### 维度 G1: Tense-Claim Alignment（时态与立场匹配）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | 全部时态与 epistemic stance 完美匹配 |
| **4 - Good** | 多数匹配；偶尔有 minor 不一致 |
| **3 - Acceptable** | 时态选择基本合理；个别 claim 时态略弱 |
| **2 - Needs Work** | 时态选择混乱；present/past 频繁错位 |
| **1 - Critical Fail** | 时态完全混乱；多处错位 |

#### 时态-立场对应表（Unit 4.2.2）
| Claim 类型 | 推荐时态 | 例子 |
|---|---|---|
| Permanent / general claim | Present Simple | "Social media comparisons **occur** frequently" |
| 本研究方法（已做）| Past Simple | "We **used** exploratory test construction" |
| 本研究结果（已发现）| Past Simple | "I **found** that..." |
| 本研究结论（claim 是永久）| Present Simple + modal | "Our results **suggest** that X **causes** Y" |
| 既有研究 | Present Perfect | "Several authors **have mounted** arguments" |
| 建议 / 期望 | Modal + bare infinitive | "Researchers **should compare**..." |

---

### 维度 G2: Tense Consistency（时态一致性）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | 段内/段间时态一致（除非有 epistemic 理由切换）|
| **4 - Good** | 基本一致；个别切换有理由 |
| **3 - Acceptable** | 有 1-2 处无理由切换 |
| **2 - Needs Work** | 多处无理由切换 |
| **1 - Critical Fail** | 完全不一致 |

#### 反模式
- ❌ 同一段内 5 个 verb，"tested / showed / find / suggested / conclude" 无理由切换
- ❌ Past 研究突然切到 Present claim（无 justification）

---

### 维度 G3: Epistemic Stance Precision（立场精确度）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | 时态精确反映 claim 的 confidence 程度 |
| **4 - Good** | 大多数精确 |
| **3 - Acceptable** | 偶尔 claim 强度与时态不匹配 |
| **2 - Needs Work** | 多数 claim 强度模糊 |
| **1 - Critical Fail** | 无 epistemic 精确度 |

---

### 维度 G4: Modal Verb Forms（情态动词形式）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | 所有 modal + bare infinitive 形式正确 |
| **4 - Good** | 偶尔小错 |
| **3 - Acceptable** | 1-2 处 modal 形式错误 |
| **2 - Needs Work** | 多处 modal 形式错误 |
| **1 - Critical Fail** | modal 形式普遍错误 |

#### 常见错误
- ❌ "should looks"（应该 "should look"）
- ❌ "may not be not"（双重否定结构错）
- ✅ "may not be" / "should look" / "could provide"

---

### 维度 G5: Modal Variety（情态动词多样性）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | 5+ 种 modal verbs（may, might, could, should, would, will）|
| **4 - Good** | 4 种 |
| **3 - Acceptable** | 3 种 |
| **2 - Needs Work** | 全用 "can" 或全用 "may" |
| **1 - Critical Fail** | 无 modal；纯陈述 |

#### Modal 选词对应
| Confidence | Modal |
|---|---|
| 强 confident | will / would |
| 中 | should / can |
| 弱 | may / might / could |

---

### 维度 G6: Subject-Verb Agreement（主谓一致）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | 全部主谓一致（包括长主语）|
| **4 - Good** | 1-2 处小错 |
| **3 - Acceptable** | 几处错 |
| **2 - Needs Work** | 多处错 |
| **1 - Critical Fail** | 普遍错误 |

#### 常见错误
- ❌ "The results **suggests**..."（单数主语 + 复数 verb 不一定错，但要检查）
- ❌ "We **was** expecting..."（we + was 错）
- ❌ "Meta-analyses **suggests**..."（复数主语 + 单数 verb）

---

### 维度 G7: Active/Passive Voice Appropriateness（语态恰当性）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | Active voice 主导；passive 仅在合适处使用 |
| **4 - Good** | 大体恰当 |
| **3 - Acceptable** | 偶尔 passive 过度 |
| **2 - Needs Work** | 被动语态过多 |
| **1 - Critical Fail** | 全文大量 passive，agent 模糊 |

#### 反模式
- ❌ "It was found by us that..."（过度被动）
- ❌ "The data was collected by the researchers"（agent 模糊）
- ✅ "We **found** that..."（主动）
- ✅ "The data **were collected** using..."（passive 突出 tool/动作）

---

## 总分计算

**总分 = (G1 + G2 + G3 + G4 + G5 + G6 + G7) / 7 × 20** （满分 100）

| 总分区间 | 评级 |
|---|---|
| 90-100 | Excellent |
| 75-89 | Good |
| 60-74 | Acceptable |
| 40-59 | Needs Work |
| <40 | Critical |

---

## 相关 example 文件

- `examples/good_midgley_2020_tense_alignment.md` — G1/G3 范例
- `examples/good_costello_2021_present_past_switch.md` — G2 范例
- `examples/good_epskamp_2018_modal_present.md` — G4/G5 范例
- `examples/good_schmidt_2016_active_passive_balance.md` — G7 范例
- `examples/bad_synthetic_tense_confusion.md` — G1 全错反例
- `examples/bad_synthetic_tense_consistency.md` — G2 反例