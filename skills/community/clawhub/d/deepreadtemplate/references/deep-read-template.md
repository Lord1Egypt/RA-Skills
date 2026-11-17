# Literature Deep-Read Report — Template & Extraction Prompts

Copy this scaffold for every paper. Fill each bracket from the paper text; mark inferences with "（推断）" and missing data with "未报告". The HTML report is the primary deliverable; the markdown mirrors the same sections.

## Step 0 — Get the full text

Do not stop at the abstract. Priority:

1. Local PDF → `pypdf` / `pdfplumber` extract text.
2. DOI/arXiv/PubMed → download the PDF; if paywalled, find a public preprint (OSF, ResearchGate, WRAP).
3. Title only → web search for the PDF, confirm with the user.

Only degrade to abstract-based when the full text is truly unavailable (then mark it explicitly).

## Report Template

```
# [第一作者 et al., 年份] 《[论文标题]》精读报告

## 一句话贡献 (One-line Contribution)
[一句话：用什么方法，解决什么未知，得出什么核心结论。]

## 1. 背景 (Background)
- 研究空白 + 悖论/缺口：[如 Rabin 2000 悖论]。
- 研究问题 / 假设：[H1、H2…]。
- 理论/现实动机。
（提取提示：读 Introduction 的 gap 陈述与 General Discussion。）

## 2. 变量 (Variables)
- 自变量 (IV)：[名称]，操作化：[如何操纵/测量]。
- 因变量 (DV)：[名称]，操作化：[如何测量，单位]。
- 参数映射表（计算建模论文必填）：[参数 ↔ 心理机制 ↔ 预期方向]。
（提取提示：Methods 的 Participants / Measures / Design，保留原文术语，括号加中文。）

## 3. 范式方法 (Paradigm / Method)
- 总体范式：[如 RL-DDM、fMRI、行为实验]。
- 建模/分析路径：[trial-by-trial 更新、参数恢复、模型比较]。
- 工具：[Python/R、HDDM、psychoPy 等，如文中给出]。
- 机制示意图：用 inline SVG 画出核心范式（如 DDM 的起点偏移 vs 漂移率）。
（提取提示：Methods 的 Computational Modeling / Analysis Plan。）

## 4. 任务流程 (Task Flow)
按时间顺序，写"被试视角"：知情同意 → 任务（每 trial 刺激-选择-反馈）→ 操纵 → 测后 → debrief。
（提取提示：重排 Methods 的 Procedure。）

## 5. 设计细节 (Design Details)
- 设计类型 + 因子：[被试间/内 × A×B]。
- 样本：[N=__，招募渠道，排除标准，power 分析__]。
- 刺激与试次：[试次数、block、平衡/随机化、激励]。
- 关键参数：[学习率、损失厌恶 η+ / η−、边界 β、起点 z 等]。
（提取提示：Methods 的 Participants、Stimuli、Procedure、Parameters。）

## 6. 统计分析 (Statistical Analysis)
- 估计方法：[层级贝叶斯、HDDM、MLE 等 + 采样细节（链数、burn-in、thinning）]。
- 模型比较：[DIC/ΔDIC、BIC/AIC、WAIC、BF；比较"完整 vs 受限模型"]。
- 后验预测/行为标记：[如有]。
- 个体差异：[参数与行为的相关 / 回归]。
- 每个检验回答的问题：[检验 → 对应假设]。
（提取提示：Analysis / Results 的统计段落；抄精确统计量与判据。）

## 7. 主要结果 (Main Results)
- 结果 1：[估计/效应量，95% CI，p=__，对应假设]。
- 结果 2 / 3：[…]。
- 模型比较结论：[哪个机制贡献最大，ΔDIC 等]。
- 解释：[结果如何支持/反驳假设]。
（提取提示：Results + Discussion；务必抄原文数字。）

## 8. 局限与可复现性 (Limitations & Reproducibility)
- 局限：[样本代表性、因果方向、测量误差、未控制变量]。
- 可复现：[是否公开数据/代码，OSF / preprint 链接]。

## 9. 对本研究者的启示 (Implications for the Reader's Research)
- 3-5 条可落地建议：把本文的方法/结论映射到读者自己的研究（如：别默认 X=Y、加某个参数、用某行为标记做三角验证、用某模型比较纪律）。
```

## Worked Example (deep) — Zhao, Walasek & Bhatia (2020), loss-aversion DDM decomposition

Fill live per paper. Skeleton with real numbers (verify at run time):

- 一句话贡献: 用 DDM 把损失厌恶分解为 λ（损失权重）、α（固定偏差）、γ（估值前偏差），证明 γ 才是主导机制。
- 背景: 前景理论以 λ>1 解释损失厌恶；Rabin(2000) 指出单靠风险厌恶无法解释小额混合博弈高拒绝率。
- 变量: IV=混合赌博 gain/loss 金额 + payoff 分布操纵；DV=接受/拒绝 + RT；参数映射 v=α+βG·G−βL·L，λ=βL/βG，γ=起点偏移。
- 范式方法: DDM 分解三机制；HDDM 层级贝叶斯；DIC 模型比较；后验预测；行为标记（短 RT 拒绝更多）。
- 任务流程: 对 200 个混合赌博按键接受/拒绝（4 block×50），记录选择+RT，随机抽一 trial 抛硬币兑现。
- 设计细节: Exp1 N=49（22.6±6.1 岁，67.3% 女），200 trials，1 token=$0.10；Exp2 N=101（HP 52/LP 49），payoff 分布操纵。
- 统计分析: HDDM 50,000 样本/25,000 burn-in；DIC 比较 full vs 受限（γ=0 / βG=βL / α=0）。
- 主要结果: 拒绝率 71.5%；λ=1.88、α=−0.03、γ=−0.20；ΔDIC：去 γ=957 > 去 λ=364 > 去 α=188；γ 与接受率 r=0.88（λ 不显著 r=−0.11）；Exp2 共享赌博接受率 HP 13.3% vs LP 34.6% → γ 可独立操纵。
- 局限: 二元小额博弈外部效度有限；未控制风险厌恶；大学样本。
- 启示（示例，供映射到读者自己的 RL-DDM 损失敏感性研究）: 别默认"损失厌恶=λ"，纳入起始点参数；经济困难可能通过先验期望（γ）而非损失权重起作用；短 RT 拒绝率是免费的三角验证标记；用 DIC/ΔDIC 做机制相对重要性论证。
