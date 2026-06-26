# 中医学 Chinese Medicine-PMPH-10edition
<div align="center">

> *「21世纪中医学子指南」*

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)
[![ClawHub](https://img.shields.io/badge/ClawHub-Skill-orange)](https://clawhub.ai)

<br>
> 基于人民卫生出版社《中医学》第10版的临床技能手册 — 172 项核心中医临床技能
<br>
<br>
<img src="assets/Chinese Medicine-10edition.jpg" width="260px">
<br>

何必苦苦读一本书<br>
只需输入一个问题，自动从课本中找到解决方案

<br>

**其他语言 / Other Languages:**

[English](README_EN.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## 项目简介

本项目系统整合中医学基础理论、辨证论治、方药应用、针灸推拿、妇科儿科、温病伤寒、肿瘤调治、体质辨识及中西医结合等核心领域，涵盖 **172 项关键临床技能**，分为 20 大分类。

**适用人群**：中医师、中西医结合医师、医学生、中医药研究者、养生保健从业者

**参考教材**：人民卫生出版社《中医学》第 10 版（全国高等学校五年制本科临床医学专业规划教材）

**⚠️ 风险 ⚠️**：用户可将中医诊断、配方、针灸或涂油内容视为独立医疗建议。

缓解措施：仅将输出作为教育参考或合格临床医生审查材料，并核实建议是否符合当前官方指导和本地规范。

**⚠️ 风险 ⚠️**：可操作的程序或治疗指导可能不适合自我诊断、紧急情况、怀孕、出血、呼吸系统疾病、针灸、手法治疗、类手术程序或药物和实验室检查。

缓解措施：执行一项独立的医疗安全政策，阻止自我治疗，并将紧急、高风险或程序性情景转交给合格的专业监督。


## 项目结构

```
Chinese-Medicine-PMPH-10edition/
├── SKILL.md                    # 核心配置 — 172 项技能注册表
├── README.md                   # 本文档 — 项目说明与使用指南（多语言）
│   ├── README_EN.md            # 英文版
│   ├── README_JP.md            # 日文版
│   ├── README_FR.md            # 法文版
│   └── README_RU.md            # 俄文版
├── <skill-name>/               # 各项技能的详细定义
│   └── SKILL.md                #   技能详情（使用时机、执行步骤、参考文档）
├── index.md                    # 技能导航索引
└── assets/                     # 项目资源文件
```

## 技能分类一览

| 分类 | 技能数 | 说明 |
|------|--------|------|
| 🧬 中医基础理论 | 18 | 阴阳五行、脏腑经络、气血津液、体质 |
| 🔍 辨证论治通则 | 8 | 辨证核心原则、治则治法 |
| 🫀 脏腑经络与生理病理 | 13 | 心、肝、脾、肺、肾、经络功能与病理 |
| 🔬 诊法与四诊合参 | 6 | 舌诊、脉诊、望诊、小儿指纹 |
| 🌡️ 外感病证辨治 | 10 | 六淫、温病、伤寒辨证 |
| 🩺 内科杂病辨治 | 14 | 便秘、痔疮、眩晕、失眠、泄泻、痹证等 |
| 👩 妇科病证辨治 | 9 | 月经不调、带下、崩漏、产后缺乳 |
| 🚽 泌尿与淋证 | 3 | 淋证六型辨证、血淋尿血 |
| 💧 消渴与水肿 | 2 | 三消辨证、阳水阴水 |
| 🟡 黄疸与积聚 | 2 | 阳黄阴黄、聚星障 |
| 🩸 瘀血与出血证 | 3 | 血瘀证、血府逐瘀 |
| 💊 方剂学与药物应用 | 26 | 经方应用、中药配伍、毒性管理 |
| 📍 针灸疗法 | 8 | 毫针、灸法、耳穴、腧穴 |
| ✋ 推拿手法 | 5 | 八法、扳法、拍法、补泻 |
| 🫳 外治法与其他疗法 | 3 | 拔罐、金黄散、中药外治 |
| 🤝 中西医结合与现代应用 | 7 | 中西医协同、糖尿病前期干预 |
| 📚 经典文献与学术源流 | 4 | 四大经典、《新修本草》、葛洪 |
| 🎗️ 肿瘤与疑难重症 | 5 | 肿瘤辨证、扶正祛邪、癌性腹水 |
| 👶 儿科专病 | 1 | 性早熟 |
| ⚙️ 治法分类 | 4 | 下法、解表剂、温里剂、通降原则 |

## 快速开始

### 安装

CLI：
```bash
openclaw skills install chinese-medicine-10edition
```

Prompt（Claude Code）：
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "Chinese Medicine 10edition" (xllgreen/chinese-medicine-10edition) from ClawHub only after those checks pass.
Skill page: https://clawhub.ai/xllgreen/chinese-medicine-10edition
Keep the work scoped to this skill only.
After install, help me finish setup from verified skill metadata.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
```

### 使用方式

每个技能包含四部分内容：
1. **使用时机** — 何时触发该技能
2. **执行步骤** — 标准化操作流程
3. **注意事项** — 禁忌与警示
4. **参考文档** — 详细补充资料

### 提问策略

#### 1. **概念**
Question:
```bash
肝主疏泄的五大生理功能是什么
```
Answer:
```bash
根据「肝属疏泄五大生理功能」技能 — 肝主疏泄指肝气具有疏通、畅达全身气机的作用，具体包括：
1. **调畅气机**：疏通全身气机，使之通而不滞、散而不郁
2. **促进血液与津液运行**：气行则血行，气行则津行
3. **促进脾胃运化与胆汁分泌排泄**：协助脾胃气机升降
4. **调畅情志**：疏泄正常则气血和调、心情舒畅
5. **调节生殖功能**：与女子月经、男子排精密切相关
```

#### 2. **临床案例分析**
Question:
```bash
患者，男，45岁，胁肋胀痛反复发作3年，每因情志不遂而加重，伴胸闷喜太息、纳食减少、脘腹胀满，舌淡红、苔薄白、脉弦。请进行辨证分析。
```
Answer:
```bash
根据「肝气郁结证辨证」技能分析与治疗...
```

#### 3. **方剂应用**
Question:
```bash
患者发热、微恶风寒、头痛口渴、咽痛咳嗽、舌尖红、苔薄黄、脉浮数。请推荐方剂。
```
Answer:
根据「银翘散方剂应用」技能 — 诊断为风热感冒（温病初起卫分证），推荐银翘散加减...

#### 4. **针灸取穴**
Question:
```bash
患者胃脘疼痛反复发作，空腹尤甚，得食稍减，伴反酸、嗳气，请推荐针灸处方。
```
Answer:
```bash
根据「腧穴分类与主治规律」及「针灸选穴原则」技能...
```

## 技能索引

全部 172 项技能索引请参阅 [index.md](index.md)。

## 关于作者

**小绿绿 xllgreen(https://xllgreen.github.io)** — 九江学院临床医学院学生·科技极客

## 技术支持
<br>
PDF2App项目：https://pdf2app.cn
<br>
Microsoft Visual Studio Code：https://code.visualstudio.com/
<br>
Claude Code for VS Code：https://claude.com/
© 2026 Anthropic PBC
<br>
<br>
<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">
<br>DeepSeek API：https://platform.deepseek.com/
© 2026 杭州深度求索人工智能基础技术研究有限公司 版权所有
<br>
<br>
<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>Xiaomi Mimo API：https://platform.xiaomimimo.com/
Copyright © 2010 - 2026 Xiaomi. All Rights Reserved
<br>

## 许可证

本项目内容基于人民卫生出版社《中医学》第10版整理，仅供学习参考。

## Star History

<a href="https://www.star-history.com/?repos=xllgreen%2FChinese-Medicine-10edition&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=xllgreen/Chinese-Medicine-10edition&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=xllgreen/Chinese-Medicine-10edition&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=xllgreen/Chinese-Medicine-10edition&type=date&legend=top-left" />
 </picture>
</a>
