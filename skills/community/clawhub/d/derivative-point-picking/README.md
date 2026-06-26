<div align="center">

# 导数取点.skill

> *"零点不是靠趋近猜出来的，是靠取点证出来的。"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-blueviolet)](SKILL.md)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://docs.claude.com/en/docs/claude-code/skills)
[![Language](https://img.shields.io/badge/Language-中文-red.svg)](README.md)

<br>

导数压轴题的核心，常常不是求导本身，<br>
而是证明零点存在、判断零点个数、锁定参数范围。<br>
AI 会说“显然存在”“趋于无穷”，<br>
但阅卷需要看到：在哪个区间？哪两个点？为什么异号？<br>

**先用导数和极限探路，再用取点、异号和零点存在定理收束。**

<br>

面向导数压轴题中的零点存在性、零点个数、参数范围证明<br>
把“趋于”“显然”“值域可得”改写成**单调分区 + 具体取点 + 异号证明**<br>
让 AI 不只判断有几个零点，也讲清楚每个零点如何被证明存在

[为什么需要](#为什么需要这个-skill) · [能力范围](#能力范围) · [例题库](#例题库) · [安装](#安装) · [使用](#使用方式) · [例子](#例子) · [核心规则](#skill-的核心规则)

</div>

---

## 能力范围

| 场景 | 分析方式 | 最终写法 | 重点 |
|------|:-------:|:-------:|------|
| 零点存在性 | 连续性、极值、极限 | 取点异号 + 零点存在定理 | 证明“至少一个” |
| 零点个数 | 单调分区、极值比较 | 每段至多一个 + 至少一个 | 证明“恰有几个” |
| 参数范围 | 必要性、充分性 | 先排除，再构造 | 端点必须检查 |
| 取点构造 | 切线放缩、同构换元、泰勒估计 | 从目标不等式反推点 | 点不能凭空出现 |
| 指数对数混合 | 换元、放缩、主导项分析 | 简化后取点异号 | 解释为什么这样取 |
| 数列极限夹逼 | 极限探路 | 显式取足够大的项数 | 避免只靠极限语言 |

## 例题库

仓库内置了一个 `examples/` 文件夹，用来沉淀不同类型的取点方法：

| 文件 | 主题 |
|------|------|
| `01-root-existence-parameter-range.md` | 极值两侧取点，处理指数减一次项的两零点问题 |
| `02-exponential-positive-point.md` | 用指数函数替换弱项，反推出正值点 |
| `03-negative-interval-point.md` | 负半轴上利用指数函数小于 1 构造负值点 |
| `04-local-bound-derivative.md` | 先限制小区间，再统一放缩取点 |
| `05-sequence-explicit-n.md` | 把极限语言改写成显式取足够大的项数 |
| `06-log-transform-three-roots.md` | 用对数换元和同构思想处理三零点问题 |

## 为什么需要这个 Skill

很多 AI 在解导数零点题时，会这样写：

> 因为函数连续，且两端趋于正无穷，所以值域为某个区间。

这种写法在数学上可能能说通，但在高考解答中，尤其是证明“某区间存在零点”或“恰有几个零点”时，不一定足够稳妥。

更适合阅卷的写法通常是：

1. 先用导数划分单调区间，判断每段至多有几个零点；
2. 再用极值、极限和值域思想分析参数范围；
3. 最后把“存在性”改写为“具体取点，使函数值异号”；
4. 用零点存在定理或介值定理完成证明。

这个 Skill 就是把这种解题习惯固定下来。

## 安装

仓库地址：

```text
https://github.com/Jiuxiao-yunwai/derivative-point-picking
```

### Codex

Windows PowerShell：

```powershell
git clone https://github.com/Jiuxiao-yunwai/derivative-point-picking.git $env:USERPROFILE\.codex\skills\derivative-point-picking
```

macOS / Linux：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/Jiuxiao-yunwai/derivative-point-picking.git ~/.codex/skills/derivative-point-picking
```

### Claude Code

个人 Skill，所有项目可用。

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force -Path $env:USERPROFILE\.claude\skills | Out-Null
git clone https://github.com/Jiuxiao-yunwai/derivative-point-picking.git $env:USERPROFILE\.claude\skills\derivative-point-picking
```

macOS / Linux：

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/Jiuxiao-yunwai/derivative-point-picking.git ~/.claude/skills/derivative-point-picking
```

项目 Skill，只在当前项目可用：

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force -Path .claude\skills | Out-Null
git clone https://github.com/Jiuxiao-yunwai/derivative-point-picking.git .claude\skills\derivative-point-picking
```

macOS / Linux：

```bash
mkdir -p .claude/skills
git clone https://github.com/Jiuxiao-yunwai/derivative-point-picking.git .claude/skills/derivative-point-picking
```

## 使用方式

使用时可以这样说：

```text
用 $derivative-point-picking 解这道导数题，注意讲清楚取点来源。
```

或：

```text
用 $derivative-point-picking 把这道题改写成高考阅卷友好的证明。
```

## 例子

题目：

已知 $a,b\in\mathbb R$，函数

$$
f(x)=e^x-a\sin x,\qquad g(x)=b\sqrt{x}.
$$

若曲线 $y=f(x)$ 和 $y=g(x)$ 有公共点，当 $a=0$ 时，求 $b$ 的取值范围。

### 普通分析

当 $a=0$ 时，公共点条件为

$$
e^x=b\sqrt{x}.
$$

因为 $x=0$ 时左边为 $1$，右边为 $0$，所以公共点必须满足 $x>0$。

于是

$$
b=\frac{e^x}{\sqrt{x}}.
$$

设

$$
\varphi(x)=\frac{e^x}{\sqrt{x}},\qquad x>0.
$$

求导可得

$$
\varphi'(x)=\frac{e^x}{x\sqrt{x}}\left(x-\frac12\right).
$$

所以 $\varphi(x)$ 在 $(0,\frac12)$ 上单调递减，在 $(\frac12,+\infty)$ 上单调递增，最小值为

$$
\varphi\left(\frac12\right)=\sqrt{2e}.
$$

因此必要性为

$$
b\ge \sqrt{2e}.
$$

但如果只写“$\varphi(x)\to+\infty$，所以值域为 $[\sqrt{2e},+\infty)$”作为充分性，在高考书写中可能不够稳。

### 取点式证明

下面证明：当 $b\ge\sqrt{2e}$ 时，确实存在 $x>0$，使

$$
\frac{e^x}{\sqrt{x}}=b.
$$

令

$$
h(x)=\frac{e^x}{\sqrt{x}}-b,\qquad x>0.
$$

由前面的单调性可知，$h(x)$ 在 $x=\frac12$ 处取最小值，且

$$
h\left(\frac12\right)=\sqrt{2e}-b\le 0.
$$

接下来需要找一个点，使 $h(x)>0$。

取点不是凭空来的。我们希望

$$
\frac{e^x}{\sqrt{x}}>b.
$$

如果先让 $\sqrt{x}=\frac1b$，即

$$
x=\frac1{b^2},
$$

那么

$$
\frac{e^x}{\sqrt{x}}
=be^{1/b^2}>b.
$$

这就是取

$$
x=\frac1{b^2}
$$

的来源。

又因为 $b\ge\sqrt{2e}$，所以

$$
\frac1{b^2}\le\frac1{2e}<\frac12.
$$

于是

$$
h\left(\frac1{b^2}\right)
=be^{1/b^2}-b
=b\left(e^{1/b^2}-1\right)>0,
$$

而

$$
h\left(\frac12\right)\le0.
$$

由连续函数零点存在定理，$h(x)$ 在区间

$$
\left(\frac1{b^2},\frac12\right]
$$

内存在零点，即存在 $x_0>0$，使

$$
h(x_0)=0.
$$

因此

$$
e^{x_0}=b\sqrt{x_0},
$$

两曲线有公共点。

综上，

$$
\boxed{b\in[\sqrt{2e},+\infty)}.
$$

## Skill 的核心规则

这个 Skill 会尽量遵循以下原则：

- 可以用极限、图像、单调性先分析答案；
- 最终证明存在性时，优先使用具体取点；
- 取点必须解释来源，不能像“魔法点”一样突然出现；
- 参数范围题必须分必要性和充分性；
- 数列中的极限夹逼，尽量改写为显式取足够大的 $n$；
- 对学生讲解时，说明放缩、切线、泰勒估计、同构换元等取点依据。

## 适用题型

- 导数压轴题；
- 零点个数问题；
- 参数取值范围；
- 恒成立与存在性问题；
- 指数、对数、三角函数混合问题；
- 需要用取点证明充分性的高考题；
- AI 解答中出现“趋于”“显然存在”“值域显然为”但证明不够稳的题目。
