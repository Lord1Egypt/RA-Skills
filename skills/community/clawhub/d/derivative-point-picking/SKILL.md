---
name: derivative-point-picking
description: Solve high-school or college-entrance-exam style derivative problems centered on root existence, root count, and parameter ranges. Use when a problem asks whether a function has roots/intersections, exactly how many roots it has, or which parameters make roots exist. The skill analyzes with derivatives, monotonic intervals, extrema, limits, and value ranges, then rewrites the final proof using concrete point selection, sign changes, continuity, and the intermediate value theorem. In teaching mode, explain where chosen points come from using tangent bounds, exponential/log inequalities, Taylor-style estimates, quadratic fitting, homomorphic transformations, or explicit threshold solving.
---

# Derivative Point Picking / 导数取点

## 中文说明

### 核心定位

这类导数题的核心通常不是“会不会求导”，而是：

- 怎样证明某个区间内存在零点；
- 怎样证明零点个数恰好为某个数；
- 怎样由零点存在性或零点个数反推参数范围；
- 怎样把极限、图像、值域直觉改写成阅卷友好的取点证明。

本 Skill 的目标是：先允许用极限、图像、单调性、值域思想探路，再把最终答案改写为“单调分区 + 具体取点 + 函数值异号 + 零点存在定理”的证明链条。

不要在最终证明中只写“趋于无穷”“显然存在”“值域可得”。这些语言可以用于分析，但最终要落到具体区间、具体点、具体符号。

### 解题流程

1. 将题目条件转化为函数零点、交点、方程、参数方程或值域问题。
2. 写清定义域，构造目标函数。
3. 求导，划分单调区间，判断每个区间内零点“至多几个”。
4. 找极值点或关键端点，得到必要条件或参数临界值。
5. 对参数范围题，分成必要性和充分性：
   - 必要性：由已有零点、极值比较或单调性推出参数必须满足什么；
   - 充分性：在每个需要零点的区间内构造异号点。
6. 取点时先明确目标：要让函数值大于零还是小于零。
7. 用切线放缩、泰勒估计、同构换元、局部限制、主导项比较等方法，把目标化成简单阈值。
8. 从阈值反推点，例如 $x\le -1/a$、$x>\ln(4/a)$、$x<-a/(2e)$。
9. 调用连续性、零点存在定理或介值定理，证明“至少一个”。
10. 结合单调性或导数符号，证明“至多一个”，从而得到“恰有一个”或“恰有若干个”。
11. 检查端点、定义域、等号成立情况。

### 零点存在性模板

当问题等价于证明存在 $x_0$ 使 $H(x_0)=0$：

1. 找一个连续区间 $I$；
2. 在区间内选两个点 $p,q$；
3. 证明 $H(p)H(q)<0$，或 $H(p)\le 0\le H(q)$ 且端点情况清楚；
4. 由零点存在定理得到至少一个零点；
5. 若需要唯一性，再由单调性证明该区间内至多一个零点。

不要只说“当 $x\to+\infty$ 时 $H(x)\to+\infty$，所以存在零点”。应改写为：由极限或放缩找到具体点 $q$，使 $H(q)>0$，再与另一个点形成异号。

### 零点个数模板

证明“恰有 $n$ 个零点”时，优先使用两步法：

1. 至多性：用导数符号、单调区间、极值结构证明每个区间内至多有几个零点。
2. 至少性：在对应区间内取点异号，逐段证明至少有一个零点。

常见写法：

- 若函数在某区间单调，则该区间至多一个零点；
- 若函数在极小值点处小于零，两侧各能取到正值，则两侧各有一个零点；
- 若函数在极大值点处大于零，两侧能取到负值，则两侧各有一个零点；
- 若换元后函数有明确的增减区间，则在每个单调段内分别讨论。

### 取点原则

- 取点必须服务于符号目标。先写“为使 $H(x)>0$，只需……”，再取点。
- 常见点 $0,1,2,e$ 可以直接作为端点、特殊点或比较点；参数相关点必须解释来源。
- 指数项强时，可考虑 $e^x\ge 1+x$、$e^x>x$、$e^x\ge ex$。
- 负半轴上指数项小，可用 $0<e^x<1$。
- 如果全局不好放缩，先限制区间。例如先令 $0<x<1$，再用 $(1+x)e^x<2e$。
- 指数、对数、多项式混合时，优先考虑同构化或换元，例如令 $u=\ln x$，把 $ae^u-u^2=0$ 转化为 $u^2e^{-u}=a$。
- 数列中若极限用于推出常数，应尽量改写成显式取足够大的项数。

### 常用取点来源

**极值两侧取点。** 若 $F$ 在 $c$ 处取极小值且 $F(c)<0$，要证明两个零点，就在 $c$ 两侧各找一个 $F>0$ 的点。

**弱项替换。** 若有 $ae^{2x}+(a-2)e^x-x$，可用 $x<e^x$，得到下界 $e^x(ae^x+a-3)$，再反推 $x>\ln((3-a)/a)$，最后取更干净的 $\ln(4/a)$。

**负半轴取点。** 若 $F(x)=e^x+ax$，其中 $x<0$、$a>0$，由 $e^x<1$ 得 $F(x)<1+ax$，于是取 $x\le -1/a$。

**局部统一放缩。** 若要让 $(1+x)e^x+a/x<0$ 且 $a<0$，先限制 $0<x<1$，用 $(1+x)e^x<2e$，再要求 $2e+a/x<0$。

### 书写风格

- 考试答案要简洁，学生讲解要补充取点来源。
- 每次取点前，最好说明“为了让某式大于零/小于零，只需……”
- 使用零点存在定理时，必须说明函数在对应区间连续。
- 证明个数时，必须同时写“至少”和“至多”。
- 参数范围题要检查端点能否取到。

## English Guide

### Core Focus

These derivative problems are usually not about differentiating itself. The real challenge is:

- proving that a root exists in a given interval;
- proving the exact number of roots;
- deriving parameter ranges from root existence or root count;
- rewriting limit or graph intuition into a grading-safe point-selection proof.

This skill allows limits, graphs, monotonicity, and value-range intuition during analysis, but the final answer should be written as a chain of monotonic partition, concrete point selection, sign change, continuity, and the intermediate value theorem.

Do not leave the final proof at “it tends to infinity”, “obviously exists”, or “the range is clear”. Those phrases can guide analysis, but the final proof needs concrete intervals, points, and signs.

### Workflow

1. Convert the condition into a root, intersection, equation, parameter equation, or value-range problem.
2. State the domain and define the target function.
3. Differentiate, split monotonic intervals, and determine how many roots each interval can have at most.
4. Locate extrema or critical endpoints to obtain necessary conditions or parameter thresholds.
5. For parameter ranges, separate necessity and sufficiency:
   - Necessity: derive restrictions from existing roots, extrema, or monotonicity;
   - Sufficiency: construct sign-changing points in every interval where a root is needed.
6. Before choosing a point, identify the sign target: positive or negative.
7. Use tangent bounds, Taylor-style estimates, homomorphic transformations, local restrictions, or dominance comparisons to reduce the target to a simple threshold.
8. Choose the point from that threshold, such as $x\le -1/a$, $x>\ln(4/a)$, or $x<-a/(2e)$.
9. Invoke continuity and the intermediate value theorem to prove at least one root.
10. Use monotonicity or derivative signs to prove at most one root, hence exactly one or exactly several roots.
11. Check endpoints, domains, and equality cases.

### Root Existence Pattern

When the problem is equivalent to proving that some $x_0$ satisfies $H(x_0)=0$:

1. Find a continuity interval $I$.
2. Choose two points $p,q$ in that interval.
3. Prove $H(p)H(q)<0$, or a controlled weak sign change with endpoints handled.
4. Apply the intermediate value theorem to get at least one root.
5. If uniqueness is needed, prove that the interval contains at most one root by monotonicity.

Do not merely say “as $x\to+\infty$, $H(x)\to+\infty$, so a root exists”. Convert the limit or bound into a concrete point $q$ with $H(q)>0$, then pair it with another point of opposite sign.

### Root Count Pattern

To prove “exactly $n$ roots”, use a two-part proof:

1. At most: use derivative signs, monotonic intervals, and extrema to show each interval has at most a certain number of roots.
2. At least: choose sign-changing points in the required intervals to prove that roots actually exist.

Common forms:

- A monotonic interval contains at most one root.
- If a minimum value is negative and positive values can be found on both sides, then each side contains a root.
- If a maximum value is positive and negative values can be found on both sides, then each side contains a root.
- If a substitution reveals monotonic intervals, discuss each interval separately.

### Point Selection Rules

- A selected point must serve a sign target. Write “to make $H(x)>0$, it suffices to…” before choosing the point.
- Standard points like $0,1,2,e$ may be used as endpoints, special points, or comparison points; parameter-dependent points need an explanation.
- When exponential growth is dominant, consider $e^x\ge 1+x$, $e^x>x$, or $e^x\ge ex$.
- On negative intervals, use $0<e^x<1$.
- If a global bound is hard, restrict the interval first. For example, force $0<x<1$, then use $(1+x)e^x<2e$.
- For mixed exponential, logarithmic, and polynomial expressions, consider transformations such as $u=\ln x$, rewriting $ae^u-u^2=0$ as $u^2e^{-u}=a$.
- In sequence arguments, replace a pure limit step with an explicit sufficiently large index whenever possible.

### Common Sources of Points

**Around an extremum.** If $F$ has a minimum at $c$ and $F(c)<0$, prove two roots by finding positive values on both sides of $c$.

**Replacing a weak term.** For $ae^{2x}+(a-2)e^x-x$, use $x<e^x$ to get the lower bound $e^x(ae^x+a-3)$, solve $x>\ln((3-a)/a)$, and choose a cleaner point such as $\ln(4/a)$.

**Negative interval.** If $F(x)=e^x+ax$, with $x<0$ and $a>0$, then $e^x<1$ gives $F(x)<1+ax$, so choose $x\le -1/a$.

**Local uniform bound.** To make $(1+x)e^x+a/x<0$ with $a<0$, first force $0<x<1$, use $(1+x)e^x<2e$, then require $2e+a/x<0$.

### Writing Style

- Keep exam answers concise; add the origin of selected points in teaching explanations.
- Before choosing a point, explain the sign target.
- When using the intermediate value theorem, state continuity on the relevant interval.
- For root count, prove both “at least” and “at most”.
- For parameter ranges, check endpoint cases.

## Example Library

Load these files only when the user asks for examples, teaching materials, or a similar pattern:

- `examples/01-root-existence-parameter-range.md`: two roots around an extremum.
- `examples/02-exponential-positive-point.md`: replacing a weak term by an exponential bound.
- `examples/03-negative-interval-point.md`: choosing a point on a negative interval.
- `examples/04-local-bound-derivative.md`: localizing first, then applying a uniform bound.
- `examples/05-sequence-explicit-n.md`: replacing limit language with an explicit large index.
- `examples/06-log-transform-three-roots.md`: logarithmic substitution and three-root structure.

These examples are pattern libraries, not scripts. Adapt the local idea to the user’s exact problem rather than copying an example mechanically.
