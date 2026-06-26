# Statistical Reporting Templates — Full Specification

Moved from main SKILL.md §6.

## 6.1 Descriptive Statistics

**中文:** 描述统计结果显示，A 条件下的 [变量] 平均值为 M = xx, SD = xx；B 条件下为 M = xx, SD = xx。

**English:** Descriptive statistics showed that [outcome] was [higher/lower] in the A condition (M = xx, SD = xx) than in the B condition (M = xx, SD = xx).

## 6.2 Correlation

**中文:** Pearson 相关分析显示，X 与 Y 呈显著正相关，r = xx, p = xx, 95% CI [xx, xx]。

**Boundary:** 相关不能写成因果。不要写"X 影响 Y"。推荐写"X 与 Y 相关 / 关联 / 呈正相关"。

## 6.3 t-test

**中文:** 独立样本 t 检验显示，A 组在 [变量] 上显著高于 B 组，t(df) = xx, p = xx, Cohen's d = xx。

**不显著:** 组间差异未达到显著水平，t(df) = xx, p = xx。该结果表明，在当前样本和测量条件下，尚未观察到可靠的组间差异。

**禁止:** "没有差异" / "证明两组相同"

## 6.4 ANOVA

**中文:** 方差分析显示，[因素] 的主效应显著，F(df1, df2) = xx, p = xx, ηp² = xx。

**交互:** 更重要的是，[因素A] × [因素B] 的交互作用显著，F(df1, df2) = xx, p = xx, ηp² = xx。简单效应分析进一步表明……

**Derived Marginal Mean Rule:** 如果用户未提供 estimated marginal means，仅提供了 cell means：
- 默认不写推算的边际均值
- 推荐定性方向描述主效应
- 若确需写入推算值，必须明确标注为推算
- 【统计报告检查】中不得写"所有统计量均来自用户输入"

## 6.5 Regression

**中文:** 回归分析显示，在控制 [协变量] 后，X 仍能显著预测 Y，β = xx, SE = xx, t = xx, p = xx。模型解释了 Y 的 xx% 方差，R² = xx。

**横断面提醒:** 这里的"预测"是统计预测，不代表时间先后或因果关系。

## 6.6 Mediation / Moderation / Moderated Mediation

Must distinguish **statistical effect term** from **causal claim**.

**推荐:** 中介分析显示，X 与 Y 的关联可部分通过 M 的统计间接效应解释，indirect effect = xx, 95% CI [xx, xx]。

**禁止:** "X 通过 M 导致 Y" / "M 证明了 X 影响 Y 的机制"

**Bootstrap Count Source Rule:** 当用户只提供 BootSE 和 BootCI 但未提供 bootstrap resampling 次数时，不写具体次数（如 5000/10000）。推荐："Bootstrap 置信区间显示……若原始输出报告了 bootstrap 次数，可在正式稿中补充；当前输入未提供，因此不写具体次数。"

**Proportion/Magnitude Wording Rule:** 当用户未提供 proportion mediated 或 standardized indirect effect 时，不写"相当部分""很大一部分""主要通过"。默认保守措辞："存在一条经由 M 的显著统计间接路径。"

## 6.7 Linear Mixed Model

**中文:** 线性混合模型显示，[固定效应] 显著预测 [因变量]，estimate = xx, SE = xx, t/z = xx, p = xx。

**LMM Dummy-Coding Rule:** 在含交互项的模型中，若用户提供 dummy coding，不得把 lower-order coefficients 简单写为"main effect"。必须说明：Condition coefficient = 参考时间点下的条件差异；Time coefficient = 参考条件下的时间差异；Interaction coefficient = 条件间的时间变化斜率差异。

**Marginal Simple-Slope Rule:** p 在 .05–.10 范围时，不写"but not in condition X" / "no change"。推荐："did not reach the conventional significance threshold" / "approached significance"。

**Predicted-Effect Wording Guardrail:** 用户未明确给出假设方向时，不写"the predicted interaction" / "as expected"。推荐："a significant Condition × Time interaction"。

## 6.8 Chi-Square

**中文:** 卡方检验显示，[变量A] 与 [变量B] 的分布存在显著关联，χ²(df) = xx, p = xx, Cramér's V = xx。

## 6.9 Meta-Analysis

**中文:** 随机效应模型显示，[干预/变量] 对 [结局] 具有小到中等的合并效应，Hedges' g = xx, 95% CI [xx, xx], p = xx。异质性为 I² = xx%, τ² = xx。

**边界提醒:** 不要把异质性忽略；不要把 pooled effect 写成单一研究证明；moderator 不能直接组合成最佳方案。

**Trim-and-Fill Adjusted Effect Rule (硬性自检):** adjusted effect 无 p 值时，不得写"校正后效应仍显著"。推荐："校正后效应的 95% CI 未跨 0"。

**Robustness Wording Caution (硬性自检):** I² ≥ 50% 时，不得写"结果稳健/结论稳定"。推荐："主分析与敏感性分析方向一致"。

**Q-Test Rule (硬性自检):** 不得写"Q 检验显著，因此选择随机效应模型"。推荐："Q 检验显著，提示研究间效应量存在变异；随机效应模型的使用与该异质性水平相匹配。"

## 6.10 Sleep EEG / Memory Behavior

**Supporting analyses:** SO power, spindle density, spindle amplitude, SO-spindle coupling, memory accuracy, recognition/recall/sequence reconstruction, old/new/lure recognition, pre-sleep vs post-sleep change.

**Must distinguish:** 相关 vs 因果；行为结果 vs 神经振荡结果；探索性分析 vs 预注册主分析。

Full guardrails: `docs/sleep-eeg-guardrails.md`

## 6.11 fMRI / EEG / Cognitive Neuroscience

**Supporting analyses:** activation, ROI, whole-brain correction, RSA/pattern similarity, MVPA/classifier accuracy, brain-behavior correlation, ERP amplitude/latency.

**Must specify:** correction method, ROI pre-definition status, neural evidence ≠ behavioral mechanism proof.

## 6.12 Qualitative Results

**模板:** 访谈资料显示，参与者围绕 [主题] 形成了三个主要经验模式。首先，…… 代表性引语为："……"。

**禁止:** 不写 p 值、不写显著性、不把主题写成统计因果路径。
