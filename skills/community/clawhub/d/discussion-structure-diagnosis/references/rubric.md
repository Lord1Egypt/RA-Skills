# Structure Rubric — Discussion 结构完整性评分

## 用途
本文件是 `discussion-structure-diagnosis` 的官方评分标准。配合 SKILL.md 的诊断信号使用。

## 评分维度（共 7 项，对应 Generic Discussion Model A-G）

### 维度 S1: Move Coverage（动作覆盖度）

#### 评分标准（5 级）

| 分数 | 标准 | 典型表现 |
|---|---|---|
| **5 - Excellent** | A-G 全部 7 个 moves 都有 | 顶刊论文标准模式 |
| **4 - Good** | 6 个 moves 有；其中 F (contribution) 必须存在 | 缺 1 个但不影响 narrative |
| **3 - Acceptable** | 5 个 moves 有；F 必须存在；D (limitations) 必须存在 | F+D 都在，其他可缺 |
| **2 - Needs Work** | ≤4 个 moves 有；或缺 F/D 等关键 move | 明显缺失 |
| **1 - Critical Fail** | ≤3 个 moves 有；或 F 完全缺失 | Discussion 不成形 |

#### 关键判定
- **F (Achievement/Contribution)** 是**必须的**——缺失就是 critical
- **D (Limitations)** 是**强烈推荐**的——缺失算 major
- 其他 moves 可根据论文类型灵活调整

---

### 维度 S2: Move Ordering（动作顺序合理性）

#### 评分标准

| 分数 | 标准 | 典型表现 |
|---|---|---|
| **5 - Excellent** | Opening → A → B → C → D → E 的逻辑链清晰 | 顶刊论文标准模式 |
| **4 - Good** | 大体符合；个别段顺序可微调 | 主流顶刊 |
| **3 - Acceptable** | 顺序基本合理但有 1-2 处微乱 | "Our results are consistent with..." 在 results 前出现 |
| **2 - Needs Work** | 顺序混乱；narrative wrap 中断 | F 段在最后才出现（应早期） |
| **1 - Critical Fail** | 完全无序；Results 与 Discussion 混在一起 | 不可救药 |

#### 反模式识别
- ❌ F (contribution) 放最后 — 应在 opening 或 early
- ❌ D (limitations) 放最前 — 通常在 results → literature 之后
- ❌ "Our results are consistent with..." 在 "Our results showed..." 之前
- ❌ Conclusion 内容混入 Discussion

---

### 维度 S3: Intro-Discussion Symmetry（首尾对称性）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | Intro 4 blocks ↔ Discussion A/B/C/D/E/F 全部对齐 |
| **4 - Good** | 大部分对齐；个别 block 未显式回应 |
| **3 - Acceptable** | 主要 blocks 对齐；细节未对称 |
| **2 - Needs Work** | Intro 和 Discussion 几乎独立，缺少呼应 |
| **1 - Critical Fail** | 完全无对称 |

#### 对应关系（重要）
| Intro Block | Discussion 对应 |
|---|---|
| Block 1 (establish importance) | Closing (exit, broader implications) |
| Block 2 (research map) | B (map to literature) |
| Block 3 (gap/problem) | A (your response to gap) |
| Block 4 (describe present paper) | F (your contribution) |

---

### 维度 S4: Opening Move Quality（开篇质量）

#### 评分标准

| 分数 | 标准 | 标志词 |
|---|---|---|
| **5 - Excellent** | Achievement opening or strong reboot | "To our knowledge, this is the first..." / "These findings demonstrate..." |
| **4 - Good** | Reboot（重述 aim/gap）| "The aim of the present study was to..."（与 Intro 呼应）|
| **3 - Acceptable** | 弱 reboot + 弱 contribution 混合 | "In this section, we discuss the implications..." |
| **2 - Needs Work** | "In this study, we..." anti-pattern | 弱开头 |
| **1 - Critical Fail** | 与 Intro 完全重复 / 完全无开头 | 直接进入 results 重复 |

#### 反模式
- ❌ "In this study, we investigated..." → 弱
- ❌ 与 Intro 重复同一段 → Critical
- ✅ "Taken together, these studies provide..." → 强

---

### 维度 S5: Take-Home Message Persistence（核心信息一致性）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | Take-home 在每段都有体现；closing 重申 |
| **4 - Good** | Take-home 清晰；closing 有体现 |
| **3 - Acceptable** | Take-home 可识别；closing 部分体现 |
| **2 - Needs Work** | Take-home 不清晰；closing 无关 |
| **1 - Critical Fail** | 无 take-home；每段独立 |

#### 测试方法
- 读第一段能否概括 take-home？
- 读最后一段是否呼应？
- 中间段落是否一致？

---

### 维度 S6: Limitations Quality（局限性段质量）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | 3+ 具体 limitations + 部分有反驳证据 |
| **4 - Good** | 2-3 具体 limitations |
| **3 - Acceptable** | 1-2 limitations 但具体 |
| **2 - Needs Work** | 1 个 generic limitation（"Our study has limitations"）|
| **1 - Critical Fail** | 无 limitations 段 |

---

### 维度 S7: Future Work Specificity（未来方向具体性）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | Future work 包含 what / where / method / variable 4 元素 |
| **4 - Good** | 3 元素 |
| **3 - Acceptable** | 2 元素（方向 + 某具体元素）|
| **2 - Needs Work** | 1 元素（仅"more research is needed"）|
| **1 - Critical Fail** | 无 future work |

---

## 总分计算

**总分 = (S1 + S2 + S3 + S4 + S5 + S6 + S7) / 7 × 20** （满分 100）

| 总分区间 | 评级 | 行动建议 |
|---|---|---|
| 90-100 | **Excellent** | 接近投稿水平 |
| 75-89 | **Good** | 小幅修改可投稿 |
| 60-74 | **Acceptable** | 需要结构性修改 |
| 40-59 | **Needs Work** | 重大结构问题 |
| <40 | **Critical** | 重写 Discussion |

---

## 相关 example 文件

- `examples/good_midgley_2020_narrative_wrap.md` — S5 take-home 范例
- `examples/good_costello_2021_reboot_opening.md` — S4 reboot 范例
- `examples/good_schmidt_2016_contribution_opening.md` — S4 achievement 范例
- `examples/good_ayanian_2020_limitation_rebuttal.md` — S6 limitations 范例
- `examples/good_ebert_2020_future_directions.md` — S7 future work 范例
- `examples/bad_synthetic_no_limitations.md` — S6 反例
- `examples/bad_synthetic_misordered_moves.md` — S2 反例