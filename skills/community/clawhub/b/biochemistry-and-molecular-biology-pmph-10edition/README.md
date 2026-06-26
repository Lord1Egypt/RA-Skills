# 生物化学与分子生物学 Biochemistry-MolecularBiology-PMPH-10edition
<div align="center">

> *「21世纪医学生指南 · 生物化学与分子生物学」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> 基于人民卫生出版社《生物化学与分子生物学》第10版的AI技能合集 — 154 项核心技能
<br>
<br>

何必苦苦读一本书<br>
只需输入一个问题，自动从课本中找到解决方案

<br>

**其他语言 / Other Languages:**

[English](README_EN.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## 项目简介

本项目系统整合生物化学与分子生物学核心知识体系，涵盖 **154 项关键技能**，分为 16 大分类：

| 分类 | 技能数 | 说明 |
|------|--------|------|
| 🧬 分子生物学与基因表达调控 | 16 | DNA/RNA结构、转录、剪接、修饰 |
| 🔧 基因工程与重组DNA技术 | 8 | 克隆载体、限制酶、CRISPR、表达系统 |
| 🧪 基因组学与疾病基因分析 | 8 | GWAS、定位克隆、外显子测序、基因芯片 |
| 🏗️ 蛋白质结构与功能分析 | 7 | 一级结构、α-螺旋、构象病、磷酸化 |
| ⚗️ 代谢通路与调控 | 15 | 糖代谢、脂肪酸氧化、酮体、乙醇代谢 |
| 🧫 核酸与核苷酸代谢 | 7 | 嘌呤/嘧啶合成与分解、抗代谢药物 |
| 🫧 脂质与脂蛋白代谢 | 9 | LDL、HDL、胆汁酸、脂蛋白分类 |
| 📡 信号转导与细胞调控 | 10 | GPCR、离子通道、p53、PTEN、RB |
| 🧬 癌症生物学与精准医学 | 7 | 癌基因、多阶段致癌、精准医疗四层 |
| 🏥 临床生化与诊断 | 9 | OGTT、糖化血红蛋白、黄疸鉴别、脱水 |
| 🔬 酶学与分离技术 | 6 | 凝胶过滤、离子交换、P450、核酶 |
| 🦠 微生物与翻译机制 | 6 | 翻译起始、延伸、SRP、抗生素 |
| ⚡ 氧化还原与能量代谢 | 5 | 呼吸链、氧化磷酸化、P/O比、ATP |
| 🏋️ 内分泌与微量元素 | 4 | 碘双重功能、运动生理、肾上腺素 |
| 📚 医学教材与数字资源 | 6 | 教材修订原则、数字教材、元数据 |
| 🌟 其他特色技能 | 31 | 端粒酶、PCR、miRNA、组蛋白修饰等 |

**适用人群**：医学生、生物医学研究者、临床医师、生物化学教师、药学与生命科学专业人员

**参考教材**：人民卫生出版社《生物化学与分子生物学》第 10 版（ISBN: 978-7-117-36618-8）

**⚠️风险⚠️**：本技能内容基于教材整理，仅供教育学习参考。涉及临床诊断或治疗决策的内容须经合格临床医生审核。

## 项目结构

```
Biochemistry-MolecularBiology-PMPH-10edition/
├── SKILL.md                    # 核心配置 — 154 项技能注册表
├── README.md                   # 本文档 — 项目说明与使用指南（中文）
├── README_EN.md                # 说明（英文）
├── README_JP.md                # 说明（日文）
├── README_FR.md                # 说明（法文）
├── README_RU.md                # 说明（俄文）
├── index.md                    # 完整技能索引表
├── <skill-name>/               # 各项技能的详细定义
│   └── SKILL.md                #   技能详情（使用时机、执行步骤、参考文档）
├── assets/                     # 静态资源
├── scripts/                    # 可执行工具脚本
├── config/                     # 配置文件
└── tests/                      # 验证与测试
```

## 快速开始

### 安装

CLI：
```bash
openclaw skills install biochemistry-molecular-biology-pmph-10edition
```

### 使用方式

每个技能包含四部分内容：
1. **使用时机** — 何时触发该技能
2. **执行步骤** — 标准化操作流程
3. **注意事项** — 禁忌与警示
4. **参考文档** — 详细补充资料

### 提问策略

#### 1. **概念讲解**

问题：
```bash
请解释PFK-1在糖酵解中的调控机制
```
回答将包含：
```
## PFK-1（磷酸果糖激酶-1）的别构与激素调控

### 核心作用
PFK-1催化果糖-6-磷酸 → 果糖-1,6-二磷酸，是糖酵解的**最主要限速酶**

### 别构调控
| 效应物 | 作用 | 机制 |
|--------|------|------|
| ATP（高浓度） | 抑制 | 降低PFK-1对F-6-P的亲和力 |
| AMP/ADP | 激活 | 解除ATP的抑制效应 |
| 柠檬酸 | 抑制 | 增强ATP的抑制效应 |
| 果糖-2,6-二磷酸 | 强激活 | 增加PFK-1对F-6-P的亲和力（最关键激活剂）|

### 激素调控
- **胰岛素** → 激活PFK-2/FBPase-2（去磷酸化）→ 升高F-2,6-BP → 激活PFK-1 → 加快糖酵解
- **胰高血糖素** → 抑制PFK-2 → 降低F-2,6-BP → 抑制PFK-1 → 抑制糖酵解（促进糖异生）
```

#### 2. **临床案例分析**

问题：
```bash
分析LDL受体缺陷导致家族性高胆固醇血症的分子机制
```

#### 3. **实验设计**

问题：
```bash
设计一个在大肠杆菌中表达人源重组蛋白的实验方案
```

## 特色技能示例

| 技能 | 说明 |
|------|------|
| [crispr-cas9-targeted-gene-correction](crispr-cas9-targeted-gene-correction/SKILL.md) | 使用CRISPR-Cas9对已知致病点突变进行精确修复 |
| [precision-medicine-four-layer-system](precision-medicine-four-layer-system/SKILL.md) | 验证精准医疗项目是否覆盖四个必要层面 |
| [gwas-analysis-for-complex-diseases](gwas-analysis-for-complex-diseases/SKILL.md) | 执行全基因组关联分析以识别与复杂疾病相关的SNP位点 |
| [metabolomics-analysis-technology-selection](metabolomics-analysis-technology-selection/SKILL.md) | 根据代谢物性质和分析目标推荐合适的代谢组学技术组合 |
| [fatty-acid-beta-oxidation-and-energy-yield-calculation](fatty-acid-beta-oxidation-and-energy-yield-calculation/SKILL.md) | 计算特定脂肪酸经β-氧化产生的净ATP数量 |

## 关于作者

**小绿绿 xllgreen** — 九江学院临床医学院学生 · 科技极客

## 技术支持

PDF2App项目：https://pdf2app.cn  
Microsoft Visual Studio Code：https://code.visualstudio.com/  
Claude Code for VS Code：https://claude.com/  
© 2026 Anthropic PBC

DeepSeek API：https://platform.deepseek.com/  
© 2026 杭州深度求索人工智能基础技术研究有限公司

Xiaomi Mimo API：https://platform.xiaomimimo.com/  
Copyright © 2010 - 2026 Xiaomi. All Rights Reserved

## 许可证

本项目内容基于人民卫生出版社《生物化学与分子生物学》第10版整理，仅供学习参考。

[MIT License](LICENSE)

## Star History

<a href="https://www.star-history.com/?repos=xllgreen%2FBiochemistry-MolecularBiology-PMPH-10edition&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=xllgreen/Biochemistry-MolecularBiology-PMPH-10edition&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=xllgreen/Biochemistry-MolecularBiology-PMPH-10edition&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=xllgreen/Biochemistry-MolecularBiology-PMPH-10edition&type=date&legend=top-left" />
 </picture>
</a>
