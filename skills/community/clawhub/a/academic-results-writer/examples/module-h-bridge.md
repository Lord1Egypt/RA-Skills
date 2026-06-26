# Example: module-h-bridge

## Input

User provides a paper-results-reverse-engineer v3.0 output containing Module H, plus their own statistics:

> "下面是 paper-results-reverse-engineer v3.0 对目标文献生成的完整输出（含 Module H Writer Transfer Packet）。请用我的统计结果写 Results。"

*Module H fields provided:*
- H1: Target = Bolier et al. (2013), source = pasted Results, coverage = full
- H2: Axis 1 = Meta-analysis, match = High
- H3: Results blocks with Transfer/Partial/Do not transfer ratings
- H4: Paragraph patterns (opening → Figure → statistics → close)
- H5: Figure-first narrative, forest plot, funnel plot
- H6: ES/CI/p in Results; causal claims in Discussion
- H7: 5 risk flags (moderator combination, follow-up comparison, publication bias, study quality, non-significant moderator)
- H8: Recommended: target-paper adaptation, standard-depth, Source Ledger needed

## Expected Output

```
Source Ledger:
- Target source: Bolier et al. (2013) Results (pasted), coverage = full ✅
- User data source: [user-provided statistics] ✅
- User draft source: none
- Target accessible? Yes ✅
- At least 3 evidence points from target? Yes (H3 blocks, H4 patterns, H5 narrative) ✅
→ Gating rule passed; 8-section target-paper output enabled

【目标文献 Results 写法提取】
[Based on Module H: H3–H5]

【设计匹配与可迁移性判断】
[Based on Module H: H2 — High match — plus H7 risk flags marked as Do not transfer]

风险标注:
- Moderator combination → Do not transfer (G1 guardrail)
- Follow-up comparison without study-set check → Do not transfer (G2 guardrail)
- Publication bias wording → Transfer with caution (G6 guardrail)
- Study quality caveat → Transfer with caution
- Non-significant moderator → Transfer with caution (G8 guardrail)

【适配到本文的结果组织方案】
[Based on H3 template, with H7 Do-not-transfer items excluded]

【可直接使用的结果段】
[Standard-depth, using user's own meta-analysis data only, with H6 boundary applied]

【统计报告检查】
[With hard-self-checks for meta-analysis wording guardrails]

【结果与讨论边界提醒】
[Per H6: ES/CI/p in Results; causal claims in Discussion]

【与目标文献的相似点和差异】
[Similarities from transferable items; differences from Do-not-transfer + Transfer-with-caution items]

【可选替代表达】
[Alternative phrasings for caution items]

文件输出模式：是（输出较长，写入 Markdown 文件）
文件路径：~/Desktop/OpenClaw_Paper_Analysis/outputs_md/results_writer/Bolier_2013_[UserStudy]_Results_Adaptation.md

聊天框摘要：
1. Source Ledger: 目标文献可访问 (Module H, full coverage)
2. 设计匹配: 高 (同为元分析)，5 项风险标记已处理
3. 完整 adaptation 已写入 Markdown 文件
4. 自检: 8-section 完整 ✅ | 截断: 无 ✅ | 需人工复核: 2 项 (H7 风险)
```
