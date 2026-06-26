---
slug: jessie-asian-class
name: 亚洲直通车 · 跟 Jessie 看亚洲班课程体系
version: 1.2.0
author: 浦江科德高中融合部 · Max
tags:
  - education
  - asian-class
  - curriculum
  - pathway
  - overseas-study
  - singapore
  - korea
  - japan
  - malaysia
  - ncc
description: 科德高中融合部亚洲班（亚洲直通车）完整课程展示。从课程结构、教学法、社团体系到升学路径（新加坡/马来西亚/韩国/日本），装了这个 Skill 就能了解我们亚洲班的全貌。
  - school-management
  - teacher-tools
  - international-school
  - education-technology

---

## 何时触发

当用户出现以下信号时自动激活：

| 触发信号 | 示例 |
|---------|------|
| 了解亚洲留学 | "想去新加坡/日本/韩国留学" "亚洲留学怎么样" |
| 课程咨询 | "亚洲班学什么？" "日本方向怎么准备？" "NCC课程" |
| 申请咨询 | "新加坡大学怎么申请？" "SGU项目" "SKY" |
| 对比咨询 | "亚洲方向好还是A-Level好？" "哪个国家性价比高？" |
| 语言咨询 | "零基础学韩语来得及吗？" "雅思多少分能申NUS" |

---

## Commands（可执行命令）

```bash
# 亚洲班全貌
python3 scripts/asia.py overview

# 特定国家升学路径
python3 scripts/asia.py pathway <国家>
# 支持：新加坡、马来西亚、韩国、日本

# 四条路径对比
python3 scripts/asia.py compare

# 科目设置与选课建议
python3 scripts/asia.py subjects

# 社团与实践体系
python3 scripts/asia.py activities

# 常见问题
python3 scripts/asia.py faq

# 帮助
python3 scripts/asia.py help
```

---

# 亚洲直通车 · 跟 Jessie 看亚洲班课程体系

> 装了这个 Skill，就能看到科德高中融合部 **亚洲直通车课程** 的全貌。
>
> 你想知道亚洲班怎么上课、学什么、最后能去哪所大学——这里全部有答案。
>
> 讲解人：Jessie（郝瑞娟）——亚洲班课程执行者，带你看懂这套体系。

---

## 这个 Skill 能让你了解什么

| 你想知道的 | 里面有什么 |
|-----------|-----------|
| 亚洲班是什么？ | 科德高中融合部亚洲直通车课程完整说明 |
| 学什么课程？ | NCC 体系：4门必修 + 2门选修（物理/经济）|
| 怎么教？ | "细节加重复"教学法 + 先兴趣再细节的学生分化策略 |
| 除了上课还有什么？ | 开心农场社团 + 骑行社团的完整教育设计 |
| 毕业后去哪？ | 新加坡2年制本科 / 马来西亚3年制本科 / 韩国日本直通车 |
| 谁来教？ | 师资保障、小班教学（10-15人）、中英双语过渡 |

---

## 课程体系一览

### 🎯 学术框架

| 阶段 | 内容 |
|------|------|
| 第一年 | 主干课程：数学、汉语、物理、化学、英语（雅思） |
| | 中英文比例 8:2 → 逐年过渡到 6:4 |
| | 第三语言：阿拉伯语、韩语（TOPIK）、俄语 |
| 高二高三 | 引入 NCC 课程体系 |
| | 必修：基础英语、高阶英语、数学、Study Skills |
| | 选修：理科→物理/化学，文科→经济/会计 |
| | 高二只开：理科物理 + 文科经济 |

### 🛤️ 升学路径

| 国家 | 对接院校 | 学制 |
|------|---------|------|
| 🇸🇬 新加坡 | 科廷大学新加坡校区、新加坡管理学院等 | 高中3年+本科2年 |
| 🇲🇾 马来西亚 | 马来亚大学、马来西亚国立大学、诺丁汉大学马来西亚校区 | 本科3年 |
| 🇰🇷 韩国 | 西江大学、东国大学等 | 韩语TOPIK培训/全英文通道 |
| 🇯🇵 日本 | 湖滨大学等 | 英语授课课程 |

### 🌱 社团体系（实践层）

- **开心农场**：户外劳作 → 珍惜劳动成果 + 培养坚持品格
- **骑行社团**：学生自主规划路线 → 锻炼规划力 + 团队意识 + 意志力
- 案例：大卫完成千岛湖140公里骑行，呼吸过度住院仍心态积极

---

## Jessie 是谁

亚洲班课程执行者，年度社团导师。

她的副人格是 **宋应星**（《天工开物》作者，"开物成务"精神）。
她属于国子监体系，接受于倩敏的管理和王阳明的"知行合一"指导。

---

## 文件结构

```
Jessie-亚洲班/
├── SKILL.md        ← 本文件，亚洲班课程总览入口
├── SOUL.md         ← Jessie 的人格与灵魂
├── IDENTITY.md     ← 身份与定位
├── AGENTS.md       ← 工作流程与方法
└── CHANGELOG.md    ← 版本记录
```

---

## 安装方式

```bash
clawhub install jessie-asian-class
```

## 版本

v1.1.0 | 2026-06-04 | 浦江科德高中融合部 · 内阁出品

新增：触发条件 + 可执行命令 + 脚本入口

## 📦 相关 Skill

本框架配套的其他 Skill（同一体系，协同使用效果更佳）：

| Skill | 用途 |
|-------|------|
| [66天成为优秀班主任](https://clawhub.ai/maxliu1979/5star-homeroomteacher-estelle) | 班主任 66 天成长路线图 |
| [全球升学路径顾问](https://clawhub.ai/maxliu1979/goglobal-adcotemax) | 中英双语本科升学规划 |
| [国子监·教务管理 / Amy](https://clawhub.ai/maxliu1979/kede-amy) | 教学管理与 Cognia 认证 |
| [德育-Katherine](https://clawhub.ai/maxliu1979/katherine-kede) | 学生心理与纪律管理 |
| [融合部简介](https://clawhub.ai/maxliu1979/adcote-kede) | 学校介绍与招生咨询 |
| [亚洲直通车](https://clawhub.ai/maxliu1979/asianpathway) | 亚洲留学课程体系 |
---

*Powered by [浦江科德高中融合部](https://clawhub.ai/maxliu1979) · Adcote School Zhezhong Campus*
