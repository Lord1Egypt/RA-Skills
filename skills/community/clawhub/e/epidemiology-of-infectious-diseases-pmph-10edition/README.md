# 传染病学 Infectious-Disease-PMPH-10edition
<div align="center">

> *「21世纪医学生指南」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>

> 基于人民卫生出版社《传染病学》第10版的临床技能手册 — 涵盖 **80+ 项传染病核心临床技能**，8 大分类

<br>

何必苦苦读一本书<br>
只需输入一个问题，自动从课本中找到解决方案

<br>

**其他语言 / Other Languages:**

[English](README_EN.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## 项目简介

本项目系统整合传染病学中病毒性、细菌性、真菌性及寄生虫性感染的临床诊疗核心领域，涵盖 **80+ 项关键临床技能**，分为 8 大分类。

**适用人群**：感染科医师、医学生、公共卫生工作者、感控人员、重症医护团队

**参考教材**：人民卫生出版社《传染病学》第 10 版

**⚠️ 风险 ⚠️**：该技能涵盖传染病诊断、用药剂量、急诊治疗、隔离措施及公共卫生管理等内容，可能被误用为独立医疗建议。

**缓解措施**：仅将输出作为教育或临床医生审核的参考资料，并根据当前官方指南、本地方案和合格的传染病专家核实建议。

**⚠️ 风险 ⚠️**：源内容并不始终严格执行仅限临床医生的安全界限。

**缓解措施**：部署系统级医疗安全政策，要求升级至合格临床医生进行诊断、开具处方、剂量分配、急诊护理及自我治疗决策。

## 项目结构

```
Infectious-Disease-PMPH-10edition/
├── SKILL.md                          # 核心配置 — 80+ 项技能注册表
├── README.md                         # 本文档 — 项目说明与使用指南
├── <skill-category>/                 # 各技能分类目录
│   └── <skill-name>/                 #   各项技能的详细定义
│       └── SKILL.md                  #     技能详情（适用场景、执行流程、参考文档）
└── README_EN.md / README_JP.md / ... # 多语言说明
```

## 技能分类一览

| 分类 | 技能数 | 说明 |
|------|--------|------|
| 🦠 病毒性感染 | 27 | 新冠、流感、HIV/AIDS、肝炎、出血热、乙脑、手足口病等 |
| 🧫 细菌性感染 | 19 | 流脑、伤寒、痢疾、霍乱、白喉、炭疽、鼠疫、结核等 |
| 🌀 螺旋体、立克次体与真菌感染 | 5 | 钩体病、梅毒、莱姆病、曲霉病、隐球菌病等 |
| 🪱 寄生虫感染 | 15 | 疟疾、钩虫、蛔虫、绦虫、华支睾吸虫、弓形虫、黑热病等 |
| 🐾 人畜共患病与特殊感染 | 2 | 布鲁菌病、肉毒中毒、生物武器病原体分类 |
| 🏥 感染控制与医院管理 | 6 | 消毒隔离、院感诊断、临床分类管理 |
| 🚑 急危重症与综合管理 | 6 | 脓毒症、器官支持、抗菌药物管理、血清学解读 |
| 🌐 其他感染性疾病 | 1 | 脊灰、重症手足口病等综合管理 |

**总计：80+ 项临床技能**

## 快速开始

### 安装

CLI：
```bash
openclaw skills install infectious-disease-pmph-10edition
```

Prompt：
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "Infectious-Disease-PMPH-10edition" from ClawHub only after those checks pass.
Skill page: https://clawhub.ai/<publisher>/infectious-disease-pmph-10edition
Keep the work scoped to this skill only.
After install, help me finish setup from verified skill metadata.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
```

### 使用方式

每个技能包含三部分内容：
1. **适用场景** — 何时触发该技能
2. **执行流程** — 标准化操作步骤
3. **约束条件** — 禁忌与适用范围

### 提问策略

#### 1. 概念查询
Question:
```bash
简述肾综合征出血热的五期经过
```
Answer:
```bash
## 《传染病学》肾综合征出血热（HFRS）五期经过

| 分期 | 持续时间 | 核心表现 |
|------|---------|---------|
| **① 发热期** | 3-7天 | 急起发热（39-40℃）、三痛（头痛、腰痛、眼眶痛）、三红（颜面、颈部、胸部潮红）、出血点 |
| **② 低血压休克期** | 1-3天 | 热退后血压下降，休克程度与病情严重性相关 |
| **③ 少尿期** | 2-5天 | 尿量 < 400ml/日，氮质血症、高血容量、电解质紊乱 |
| **④ 多尿期** | 7-14天 | 尿量 > 2000ml/日，易脱水、电解质丢失 |
| **⑤ 恢复期** | 1-3月 | 尿量逐渐恢复正常，体力逐步恢复 |

> **核心考点**：发热期→低血压期→少尿期是 HFRS 最危险的**三重打击**，三期可有重叠，少尿期是病情最严重阶段。
```

#### 2. 临床案例题
Question:
```bash
患者，男，35岁，农民，8月就诊。持续发热12天，伴相对缓脉、玫瑰疹。最可能的诊断是？
```
Answer:
```bash
## 病例分析

| 项目 | 表现 |
|------|------|
| 年龄/职业 | 35岁，农民（不洁饮食/饮水接触机会多） |
| 季节 | 8月（夏秋季，伤寒高发期） |
| 热程 | 持续发热12天（>1周，符合伤寒自然病程） |
| 相对缓脉 | 伤寒特征性体征之一 |
| 玫瑰疹 | 伤寒特征性皮疹（病程第7-13天，胸腹部淡红色斑丘疹） |

### 最可能的诊断
**伤寒（肠热症）**

### 诊断依据
1. 流行病学史 + 夏秋季 + 农民（水源/食物污染风险）
2. 持续高热 > 1周
3. **相对缓脉**（体温↑而心率不相应↑）= 伤寒典型表现
4. **玫瑰疹** = 伤寒特征性皮疹

### 鉴别要点
| 疾病 | 鉴别点 |
|------|--------|
| 斑疹伤寒 | 有蜱/虱叮咬史，发热急起，皮疹更广泛 |
| 疟疾 | 周期性寒战高热，无相对缓脉 |
| 败血症 | 热型不规则，皮疹多样，多有毒血症表现 |

### 确诊检查
- 血培养（病程第1-2周阳性率最高）
- 肥达反应（O抗体 ≥ 1:80，H抗体 ≥ 1:160）
- 骨髓培养（阳性率最高，尤其已使用抗生素者）
```

#### 3. 考试题目
Question:
```bash
HIV主要侵犯的细胞是（  ）。
A. CD8+ T淋巴细胞
B. CD4+ T淋巴细胞
C. B淋巴细胞
D. NK细胞
E. 巨噬细胞
```
Answer:
```bash
**答案：B. CD4+ T淋巴细胞**

**依据：**
HIV 通过表面 gp120 与靶细胞表面的 **CD4 分子** 结合，同时与辅助受体（CXCR4 或 CCR5）相互作用，介导病毒进入细胞。CD4+ T 淋巴细胞是 HIV 最主要的靶细胞。

**临床相关性：**
- HIV 感染后 CD4+ T 细胞进行性减少 → 细胞免疫功能缺陷
- CD4 计数 < 200/μL → AIDS 期，易发机会性感染
- ART 治疗目标 → 重建 CD4+ T 细胞数量

**其他选项解析：**
| 选项 | 说明 |
|------|------|
| A. CD8+ T 细胞 | 主要发挥抗病毒 CTL 作用，非 HIV 主要靶细胞 |
| C. B 淋巴细胞 | 可间接受影响，但非 HIV 直接靶细胞 |
| D. NK 细胞 | 天然免疫细胞，不受 HIV 直接损害 |
| E. 巨噬细胞 | 可被 HIV 感染，但不是主要靶细胞 |

> 注意：CD4+ 细胞包括 T 淋巴细胞、单核/巨噬细胞、树突状细胞等，但以 CD4+ T 细胞为主。
```

**其他示例：**
- "请制定一名确诊 HIV 感染孕妇的 ART 方案及母婴阻断策略。"
- "依据「乙脑流行病学」技能，分析某地区乙脑暴发疫情的控制措施。"
- "参考「医院感染诊断」技能，判定一名机械通气 72 小时后发热的患者是否符合 VAP 诊断标准。"

## 关于作者

**xllgreen** — 九江学院临床医学院学生 · 科技极客

## 技术支持

PDF2App 项目：https://pdf2app.cn

Microsoft Visual Studio Code：https://code.visualstudio.com/

Claude Code for VS Code：https://claude.com/
© 2026 Anthropic PBC

<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">
<br>DeepSeek API：https://platform.deepseek.com/
© 2026 杭州深度求索人工智能基础技术研究有限公司 版权所有

<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>Xiaomi Mimo API：https://platform.xiaomimimo.com/
Copyright © 2010 - 2026 Xiaomi. All Rights Reserved

## 许可证

本项目内容基于人民卫生出版社《传染病学》第10版整理，仅供学习参考。

## Star History

<a href="https://www.star-history.com/">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=&type=date" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=&type=date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=&type=date" />
 </picture>
</a>
