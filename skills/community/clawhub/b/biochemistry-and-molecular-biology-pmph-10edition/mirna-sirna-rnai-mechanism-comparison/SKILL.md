---
name: miRNA与siRNA介导的RNA干扰机制比较
description: 比较miRNA和siRNA在真核细胞中介导RNA干扰（RNAi）的生成路径、作用机制及功能差异。当用户需要区分两类小RNA的来源、结构、靶标识别方式或生物学效应（如翻译抑制 vs mRNA降解）时使用本技能。
---

# miRNA与siRNA介导的RNA干扰机制比较

## 何时使用
- 需要解释miRNA与siRNA在基因沉默中的不同角色
- 分析实验中观察到的翻译抑制或mRNA降解现象
- 设计RNA干扰实验（如选择使用miRNA模拟物或siRNA）
- 理解发育调控（miRNA）与抗病毒防御（siRNA）的分子基础

## 核心执行流程

### 1. 判断小RNA类型
- 若来源于内源基因转录的发夹结构前体 → **miRNA**
- 若来源于外源或内源长双链RNA（如病毒RNA、人工dsRNA） → **siRNA**

### 2. 分析加工与加载过程
- **miRNA**：pri-miRNA →（核内加工）→ pre-miRNA →（Dicer切割）→ 成熟单链miRNA → 加载至RISC
- **siRNA**：长dsRNA →（Dicer切割）→ 21–23 bp双链siRNA → 解旋后引导链加载至RISC

### 3. 判断靶标作用模式
- **miRNA**：与mRNA 3'-UTR **不完全互补**配对 → **抑制翻译起始**，通常不降解mRNA
- **siRNA**：与靶mRNA **完全互补**配对 → **引导RISC介导的mRNA降解**

### 4. 推断生物学效应
- **miRNA主导**：发育时序调控、组织特异性基因表达微调
- **siRNA主导**：抗病毒免疫、转座子沉默、外源核酸防御

## 关键共性
- 均依赖Dicer酶加工
- 最终长度均约20–24 nt
- 均通过RISC复合体执行基因沉默
- 均作用于mRNA的3'-UTR区域

> 注意：植物中机制存在差异（如siRNA可参与DNA甲基化），本技能默认适用于动物真核细胞。