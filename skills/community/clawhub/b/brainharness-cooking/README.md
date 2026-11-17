<div align="center">

# BrainHarness · 做饭

> 不知道吃什么，就先把冰箱和嘴说清楚。

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Agent Skill](https://img.shields.io/badge/Skill-Cooking-green)](#)
[![Status](https://img.shields.io/badge/status-v0.2.0-orange)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个会先问你两句、再给出可执行菜谱的做饭 Skill。  
默认以中式家常菜为核心，吸收大厨技法和美食区的讲法，但不做夸张模仿。

[快速安装](#安装) · [使用](#使用) · [示例](#示例) · [项目结构](#项目结构) · [Changelog](CHANGELOG.md) · [Releases](https://github.com/zning1994/brainharness-cooking/releases)

**Other Languages / 其他语言：**

[English](README_EN.md) · [日本語](README_JA.md) · [Español](README_ES.md) · [Deutsch](README_DE.md) · [한국어](README_KO.md) · [Português](README_PT.md) · [Русский](README_RU.md)

</div>

---

## 这是什么

`brainharness-cooking` 不是单纯的菜谱列表，也不是只会整活的美食区段子号。

它的目标是：

- 用户说“今晚吃啥”时，先补两句关键条件，再给更像样的推荐
- 用户说“家里有鸡腿土豆洋葱”时，优先利用现有食材出方案
- 用户问“牛肉怎么炒嫩一点”时，直接给技法，不绕弯
- 输出既能看得下去，也真的能下锅做

默认知识基础：

- 中式家常菜
- 家庭厨房常见设备
- 大厨技法的家用简化版
- 轻松自然、但不过度表演的表达

## 它不是什么

- 不是精确营养和热量管理工具
- 不是大型宴席规划器
- 不是西餐 / 烘焙的完整知识库
- 不是只会抖机灵的做饭段子机器人

---

## 它会做什么

### 1. 帮你决定做什么

支持两类常见入口：

- `想吃什么`
- `家里有什么`

它会尽量自动判断，不要求用户记命令格式。

### 2. 先问最少的问题

默认只在必要时追问两句：

1. `几个人吃`
2. `有没有不能吃、不会做、或者家里没有的条件`

如果你已经说清楚了，它就不重复问。

### 3. 给一份能真做的答案

默认输出包括：

- 推荐做什么
- 为什么推荐这道
- 需要什么食材
- 怎么做
- 关键点
- 翻车提醒
- 替代方案 / 补救办法

---

## 安装

### 通用安装

```bash
npx skills add zning1994/brainharness-cooking
```

### OpenClaw / ClawHub

```bash
npx clawhub@0.23.3 install brainharness-cooking
```

### Claude Code / 手动安装

在当前项目安装：

```bash
mkdir -p .claude/skills
git clone https://github.com/zning1994/brainharness-cooking .claude/skills/brainharness-cooking
```

或安装到全局：

```bash
git clone https://github.com/zning1994/brainharness-cooking ~/.claude/skills/brainharness-cooking
```

## 最适合 / 暂时不适合

### 最适合

- 中式家常菜
- 下班回家做一顿正常晚饭
- 看冰箱现有食材出菜
- 问一道菜的关键做法
- 问常见救场和替代方案

### 暂时不适合

- 精细化减脂营养规划
- 大型多道宴席编排
- 完整西餐体系
- 烘焙甜点

---

## 使用

在 Claude Code 中，你可以直接说：

```text
今晚吃啥
冰箱里有鸡腿土豆洋葱能做什么
两个人吃，想吃点热乎的
牛肉怎么炒嫩一点
没有料酒怎么办
```

这个 Skill 会自动判断你属于哪种需求：

- `想吃什么`
- `家里有什么`
- `指定菜 / 指定技法`

---

## 效果示例

仓库内还有两份更适合快速浏览的示例：

- [基础流转示例](examples/basic-flows.md)
- [Demo Prompts](examples/demo-prompts.md)

### 场景一：不知道吃啥

```text
用户       > 今晚想吃点下饭的

brainharness-cooking > 几个人吃？
用户       > 两个人

brainharness-cooking > 有没有不能吃、不会做、或者家里没有的条件？
用户       > 不吃太辣，别太复杂

brainharness-cooking > 那就直接做土豆烧鸡腿最稳。
              > 原因很简单：它够下饭，做法不飘，家常厨房也容易控住。
              > 先把鸡腿煎出点颜色，再下土豆和料头，加生抽老抽和水焖到土豆发软。
              > 最容易翻车的是水放太多，最后变成一锅寡淡鸡汤土豆。
```

### 场景二：看冰箱出菜

```text
用户       > 家里有番茄鸡蛋挂面

brainharness-cooking > 你这个条件别硬整花活，番茄鸡蛋面就对了。
              > 先把鸡蛋炒到刚凝固就盛出来，番茄单独炒出汁，再加水下面，
              > 最后把鸡蛋回锅。关键不是调多少料，是番茄汁一定要先出来。
```

### 场景三：问技法

```text
用户       > 牛肉怎么炒嫩一点

brainharness-cooking > 先别想着靠一堆调料救它，重点是切法和火候。
              > 逆纹切薄片，先用一点生抽、淀粉和油抓匀。
              > 热锅快炒到刚变色就先盛出来，别恋战。
              > 你要是一直炒到“看起来很熟”，基本就已经老了。
```

---

## 项目结构

```text
brainharness-cooking/
├── SKILL.md
├── README.md
├── README_EN.md
├── README_JA.md
├── README_ES.md
├── README_DE.md
├── README_KO.md
├── README_PT.md
├── README_RU.md
├── agents/
│   └── openai.yaml
├── examples/
│   ├── basic-flows.md
│   └── demo-prompts.md
├── evals/
│   └── evals.json
└── references/
    ├── high-frequency-answers.md
    ├── dish-coverage.md
    ├── sauces.md
    ├── style-guide.md
    ├── cooking-framework.md
    └── techniques.md
```

其中：

- `SKILL.md`：主入口，定义触发方式、追问逻辑和输出格式
- `examples/`：给第一次看仓库的人快速理解 skill 怎么工作
- `evals/`：给后续迭代留的轻量评测锚点
- `high-frequency-answers.md`：高频技法/救场/替代问答模板
- `dish-coverage.md`：常见家用食材组合到菜品的稳定映射
- `sauces.md`：高频味型与汁水比例基线
- `style-guide.md`：语气规则，不做明显模仿
- `cooking-framework.md`：出菜逻辑和问答结构
- `techniques.md`：技法、翻车点和补救方案

---

## 当前范围

当前版本重点支持：

- 中式家常菜
- 家庭厨房的现实做法
- 快速推荐和技法答疑

后续可以继续扩展：

- 西餐 / 烘焙
- 酱汁与比例库
- 面食 / 汤类专题
- meal prep / 备菜流

当前能力层重点参考：

- `references/high-frequency-answers.md`
- `references/dish-coverage.md`
- `references/sauces.md`

---

## 设计原则

- 先有用，再有味道
- 先给结论，再讲原因
- 少问废话，多给能做的方案
- 有点人味，但不表演

---

## License

MIT
