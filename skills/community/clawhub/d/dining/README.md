<div align="center">

# 吃什么.skill

> *「在饥饿与纠结之间，算法替你决定」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-blueviolet)](https://claude.ai)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)
[![Version](https://img.shields.io/badge/version-2.1-blue)](SKILL.md)
[![Cuisines](https://img.shields.io/badge/cuisines-10-orange)](references/cuisine-profiles.md)
[![GitHub](https://img.shields.io/badge/GitHub-ChenChen913%2Fdining--skill-black?logo=github)](https://github.com/ChenChen913/dining-skill)

<br>

**一个帮你决定今天吃什么的 AI 技能。**

<br>

[快速开始](#快速开始) · [它解决了什么问题](#它解决了什么问题) · [能干什么](#能干什么) · [安装方式](#安装方式) · [文件结构](#文件结构)

<br>

**其他语言 / Other Languages：** [English](README_EN.md)

</div>

---

## 快速开始

装好之后，对你的 AI 助手说：

```
今天吃什么
3个人，下厨，不要辣
```

就行了。

---

## 它解决了什么问题

每个人每天都要面对一个问题：今天吃什么。

自己做饭的时候，不知道做什么菜。点外卖的时候，刷半小时不知道点啥。请客吃饭的时候，更不知道该做多少菜、做什么菜才有排面。减肥的时候，想吃又怕胖，纠结半天最后随便对付一口。

这不是你选择困难。行为经济学家管这个叫"选择悖论"：选项太多了，人的大脑会直接卡住。

这个 skill 就是帮你做这个决定的。你告诉它有多少人吃饭、想自己做还是点外卖、有什么忌口、有没有什么特别需求，它直接告诉你要吃什么。不给你一堆选项让你继续纠结，就给你确定的答案。

---

## 能干什么

**日常吃饭**

告诉它几个人、自己做还是点外卖、不吃什么，它给你两套菜单，每道菜都写得清清楚楚。如果自己做，还会告诉你先做哪个后做哪个，怎么安排时间最合理。

**特殊场景**

吃火锅：推荐锅底和涮菜清单。吃全素：推荐植物蛋白替代肉类的菜品。减肥期：推荐低卡高蛋白的搭配，标注卡路里。露营：推荐方便携带、不用冷藏的菜。

**请客聚餐**

家庭聚会、商务宴请、同学叙旧，它会根据场合调整菜品风格。家庭聚会偏温馨家常，商务宴请偏精致有排面，同学聚会偏下酒下饭。有小孩在场会自动加一道酸甜口的菜。

**记住你的口味**

你告诉它一次"我是四川人，喜欢吃辣"，下次它就记住了。你说"红烧肉只适合家庭聚餐，别的时候别推"，它就调整。用得越久，推荐越对你的胃口。

**有四个角色帮你把关**

每次推荐菜单的时候，系统会用四个角色的视角来审视：一个关注健康安全（比如痛风不能吃海鲜），一个关注营养均衡，一个关注健身目标，一个关注你的情绪和满足感。他们会从各自的角度给意见，比如健身的觉得方案二更低脂，但心理的觉得方案一今天更让你开心。

**外卖也懂**

不是所有菜都适合外卖。清蒸鱼送过来可能凉了，炸鸡送过来可能软了，面条会坨。这个 skill 知道哪些菜外卖友好、哪些菜建议堂食，点外卖的时候会自动避开容易翻车的菜。

---

## 安装方式

### 方式一：npx 安装（推荐）

```bash
npx skills add ChenChen913/dining-skill
```

### 方式二：GitHub 下载安装

```bash
git clone https://github.com/ChenChen913/dining-skill.git
cp -r dining-skill ~/.claude/skills/dining
```

或者从 [GitHub Releases](https://github.com/ChenChen913/dining-skill/releases) 下载 ZIP 包，解压后放到 AI 助手的 skills 目录。
- Claude Code：`~/.claude/skills/dining/`
- Reasonix Code：`~/.reasonix/skills/dining/`

### 方式三：告诉 AI 帮你装

把项目地址发给 AI 助手，让它自己操作：

```
帮我把 https://github.com/ChenChen913/dining-skill 克隆到本地，然后装到 skills 目录
```

---

## 文件结构

```
dining-skill/
├── SKILL.md                     # 主文件
├── references/                  # 规则和模板
│   ├── mode-routing.md
│   ├── algorithm-engine.md
│   ├── cuisine-profiles.md      # 十大菜系数据
│   ├── expert-cabinet.md
│   ├── memory-system.md
│   ├── output-schema.md
│   └── heuristics.md
├── assets/
│   └── dishes-reference.md      # 74道菜品速查表
├── README.md
└── README_EN.md
```

---

## License

MIT
