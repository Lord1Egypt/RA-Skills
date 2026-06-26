# Meta-Analysis Guardrails — Hard Self-Check Level

Moved from main SKILL.md §6.9. All rules are **hard-self-check** level: output flagged as failing if violations detected.

## Trim-and-Fill Adjusted Effect Significance Wording Rule

When trim-and-fill adjusted effect only provides 95% CI but NO p-value:

❌ "校正后效应仍显著" / "adjusted effect remained significant"

✅ "校正后效应的 95% CI 未跨 0" / "校正后效应方向与主分析一致" / "校正后合并效应有所减小，但 95% CI 仍不包含 0"

Only write "p = xx" when user provides adjusted effect p-value.

**⚠️ Hard check:** If adjusted effect has no p-value but "significant" is written, output is automatically failing.

## Robustness Wording Caution (I² ≥ 50%)

When I² ≥ 50% (moderate to high heterogeneity):

❌ "结果稳健" / "结论非常稳定" / "证明干预有效"

✅ "主分析与敏感性分析方向一致" / "偏倚校正后总体结论未发生方向性改变" / "但需结合异质性水平谨慎解释"

**⚠️ Hard check:** If I² ≥ 50% and "结果稳健/结论稳定" is written, output is automatically failing.

## Q-Test and Random-Effects Wording Rule

❌ "Q 检验显著，因此选择随机效应模型" / "Q 检验证明应使用随机效应模型" / "Q 检验支持选用随机效应模型"

✅ "Q 检验显著，提示研究间效应量存在变异；随机效应模型的使用与该异质性水平相匹配。" / "随机效应模型的选择通常应由研究问题、研究间预期差异和分析计划共同决定，而不应仅由 Q 检验事后决定。"

**⚠️ Hard check:** If any Q-test-based model selection wording appears, output is automatically failing.
