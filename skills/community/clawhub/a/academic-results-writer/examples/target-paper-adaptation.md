# Example: target-paper-adaptation

## Input

User uploads a target paper and provides their own data:

> "我上传了一篇目标文献 PDF（睡眠记忆 fMRI 研究）和我的统计结果（横断面问卷中介）。请先提取目标文献 Results 的组织结构，再根据我的数据写 Results。"

## Expected Output (Partial)

```
【目标文献 Results 写法提取】
目标文献 Results 结构：
1. 睡眠结构参数（描述性）
2. 行为记忆巩固效应（ANOVA + 相关）
3. fMRI ROI 激活结果
4. 脑-行为相关
5. 结果收束与 Discussion 过渡

【设计匹配与可迁移性判断】
⚠️ 设计不兼容：目标文献为 fMRI 实验，用户研究为横断面问卷中介。
- 可迁移：先主分析后补充、图表先行、统计报告顺序、谨慎措辞
- 不可迁移：whole-brain / ROI activation / brain-behavior correlation / RSA
- 用户 Results 应改写为：描述统计 → 相关矩阵 → 中介模型 → 边界声明

【适配到本文的结果组织方案】
本文组织由用户数据和通用 Results 规范驱动，不由目标文献结构驱动：
1. 描述统计与信度
2. 变量间相关
3. 中介模型（主分析）
4. 条件间接效应（补充分析）
5. 边界声明

【可直接使用的结果段】
[standard Results output using user's own mediation data, with statistical-effect prefix rule applied]

【与目标文献的相似点和差异】
相似点：均先行为数据后深入分析；图表引导句相似；谨慎措辞一致
差异：本文无神经数据模块；统计方法为 PROCESS/SEM 而非 ANOVA；设计从实验变为横断面

【可选替代表达】
（提供替代措辞选项）
```

## Key Points

- Design incompatibility explicitly acknowledged
- fMRI-specific sections marked as non-transferable
- User Results written from user data only
- Cross-sectional mediation statistical-effect prefix applied
- Source Ledger distinguishes target source from user data source
