# Example: figure-to-results

## Input

User provides figure caption and related statistics:

> "Figure 2 caption: Mean recognition accuracy for negative, neutral, and positive images after sleep vs. wake retention. Error bars indicate ±1 SE.
>
> 统计结果：Group × Valence interaction F(2, 104) = 6.32, p = .003, ηp² = .11。
> Sleep > Wake for negative: t(52) = 3.12, p = .003, d = 0.84。
> Sleep > Wake for neutral: t(52) = 2.45, p = .018, d = 0.66。
> Positive: t(52) = 1.08, p = .285, d = 0.29。"

## Expected Output

```
【结果组织建议】
先总体趋势（sleep 总体上比 wake 好），再引 Figure 2，再报交互，再分别报告三种效价下的简单效应。

【可直接使用的结果段】
总体来看，睡眠组在情绪图片的再认正确率上优于清醒组。
图 2 展示了三种效价条件下两组正确率的均值及 ±1 SE。
2（组别）× 3（效价）方差分析显示交互作用显著，F(2, 104) = 6.32, p = .003, ηp² = .11。
进一步简单效应分析表明，睡眠组在负性图片（t(52) = 3.12, p = .003, d = 0.84）
和中性图片（t(52) = 2.45, p = .018, d = 0.66）上的正确率均显著高于清醒组；
而在正性图片上，组间差异未达到显著水平，t(52) = 1.08, p = .285, d = 0.29。

【统计报告检查】
- ✅ Figure 2 caption 写 error bars ±1 SE → 正文正确使用"均值及 ±1 SE"
- ✅ 交互显著后立即报 simple effects
- ✅ 不显著结果（positive: p = .285）正确使用"未达到显著水平"
- ⚠️ 缺少两组的 M/SD → 需用户补充描述统计
```
