# 诊断学 Diagnostic Medicine-PMPH-10edition
<div align="center">

> *「21世纪医学生诊断技能指南」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> 基于人民卫生出版社《诊断学》第10版的临床技能手册 — 183 项核心诊断技能
<br>
<br>
<img src="/assets/Diagnostics.png" width="260px">
<br>

何必苦苦读一本书<br>
只需输入一个问题，自动从课本中找到解决方案

<br>

**其他语言 / Other Languages:**

[English](README_EN.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## 项目简介

本项目系统整合临床诊断学核心领域，涵盖 **183 项关键诊断技能**，分为 14 大分类。基于人民卫生出版社国家级规划教材《诊断学》第 10 版系统整理，覆盖病史采集、体格检查、实验室检验解读、心电图与影像分析、常见症状鉴别诊断、专科操作规范及临床推理方法。

**适用人群**：临床医师、医学生、住院医师规范化培训学员、检验与影像技术人员、护理及公共卫生工作者

**参考教材**：人民卫生出版社《诊断学》第 10 版（ISBN: 978-7-117-35276-8）

**⚠️风险声明⚠️**
- 本项目仅供**教育参考**和**临床培训**使用，不可替代专业医疗判断。
- 所有诊断决策必须结合患者具体情况，由具备执业资格的临床医师做出。
- 源内容可能不持续更新至最新临床指南，使用时应与当前权威指南、本地方案和专科医师意见进行交叉验证。
- 部署系统级医疗安全策略，要求将诊断、用药、急诊处理等决策升级至合格临床医师。

## 项目结构

```
Diagnostic-Medicine-PMPH-10edition/
├── SKILL.md              # 核心配置 — 183 项技能注册表
├── README.md             # 本文档 — 项目说明与使用指南
├── <skill-name>/         # 各项技能的详细定义
│   └── SKILL.md          #   技能详情（使用时机、执行步骤、注意事項、参考文档）
├── scripts/              # 可执行工具脚本
├── config/               # 配置文件
└── tests/                # 验证与测试
```

## 技能分类一览

| 分类 | 技能数 | 说明 |
|------|--------|------|
| 📋 病史采集与临床沟通 | 8 | 结构化问诊、重点问诊、医患沟通、病历书写、病程记录时限与合规 |
| 🩺 体格检查技术 | 22 | 全身体检、四大基本检查法、特殊人群适应、各系统专项检查 |
| ❤️ 心血管系统诊断 | 16 | 心电图分期与定位、心音分析、心律失常、运动负荷试验、心肌标志物 |
| 🫁 呼吸系统诊断 | 7 | 异常呼吸音、叩诊音辨读、支气管镜术前准备、肺功能与血气分析 |
| 🫃 消化系统与腹部评估 | 10 | 腹部肿块、腹痛机制、呕吐物分析、肠梗阻、Murphy 征、腹壁静脉 |
| 🩸 血液与凝血系统 | 21 | 贫血分级与形态分类、骨髓铁染色、凝血因子、溶血筛查、PNH 流式 |
| ⚖️ 内分泌与代谢 | 11 | 水肿鉴别、营养评估、血糖与 OGTT、甲状腺功能、先天性黄疸综合征 |
| 🫘 肝胆胰肾与泌尿系统 | 15 | 黄疸鉴别、肝酶模式、血氨、尿红细胞形态、肾小管酸中毒试验 |
| 🦠 感染与免疫 | 14 | 药敏试验、耐药机制、梅毒血清学、结核 PPD、补体与自身抗体 |
| 🧠 神经与精神系统 | 4 | 眩晕分类、抑郁识别、视盘水肿测量、眼底全身性疾病征象 |
| 🔬 实验室检验与质量控制 | 10 | 标本采集、参考区间解读、质控体系、粪便与精液检验、阴道清洁度 |
| 🏥 专科操作与穿刺技术 | 10 | 腹穿、胸穿、腰穿、肝穿、淋巴结穿刺、导尿、胃镜与结肠镜准备 |
| 🧩 临床推理与诊断方法 | 11 | 四步诊断法、假设演绎推理、诊断思维原则、症状鉴别、病理生理分类 |
| 📚 教材与资源使用 | 5 | 版本验证、修订指南、数字资源访问、诊断学核心框架 |

> **总计：183 项技能**，覆盖从基础到进阶的完整诊断能力体系。

## 快速开始

### 安装

CLI：
```bash
openclaw skills install diagnostics-pmph-10edition
```

Prompt（适用于 AI 助手）：
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "Diagnostic-Medicine-PMPH-10edition" (xllgreen/diagnostics-pmph-10edition) from ClawHub only after those checks pass.
Skill page: https://clawhub.ai/xllgreen/diagnostics-pmph-10edition
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

#### 1. **概念查询**
Question:
```text
什么是奔马律？有哪些类型？
```

#### 2. **临床案例分析**
Question:
```text
男性，65 岁，胸骨后压榨性疼痛 2 小时，向左肩放射，伴大汗、恶心。心电图示 V₁-V₄ 导联 ST 段弓背向上抬高 0.3-0.5mV，cTnI 升高。最可能的诊断是什么？
```

#### 3. **鉴别诊断**
Question:
```text
患者女性，28 岁，全身水肿伴泡沫尿 1 周。尿常规：蛋白 (+++)，24h 尿蛋白 4.5g，血浆白蛋白 25g/L。最可能的诊断及需鉴别的疾病是？
```

**其他示例：**
- "请使用 **acute-myocardial-infarction-ecg-staging** 技能分析该患者心电图。"
- "依据 **mcv-rdw-anemia-classification** 对该贫血病例进行实验室分型。"
- "参考 **clinical-diagnostic-four-step-method** 推理该发热患者的可能病因。"
- "运用 **bilirubin-metabolism-and-jaundice-classification** 分析黄疸患者的病因。"

## 关于作者

**小绿绿 xllgreen** ([xllgreen.github.io](https://xllgreen.github.io)) — 九江学院临床医学院学生 · 科技极客

## 技术支持

<br>
PDF2App 项目：https://pdf2app.cn
<br>
Microsoft Visual Studio Code：https://code.visualstudio.com/
<br>
Claude Code for VS Code：https://claude.com/
<br>
© 2026 Anthropic PBC
<br>
<br>
<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">
<br>DeepSeek API：https://platform.deepseek.com/
<br>
© 2026 杭州深度求索人工智能基础技术研究有限公司 版权所有
<br>
<br>
<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>Xiaomi Mimo API：https://platform.xiaomimimo.com/
<br>
Copyright © 2010 - 2026 Xiaomi. All Rights Reserved
<br>

## 许可证

本项目内容基于人民卫生出版社《诊断学》第 10 版整理，仅供学习参考。

## Star History

<a href="https://www.star-history.com/#xllgreen%2FDiagnostic-Medicine-PMPH-10edition&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=xllgreen/Diagnostic-Medicine-PMPH-10edition&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=xllgreen/Diagnostic-Medicine-PMPH-10edition&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=xllgreen/Diagnostic-Medicine-PMPH-10edition&type=Date" />
 </picture>
</a>
