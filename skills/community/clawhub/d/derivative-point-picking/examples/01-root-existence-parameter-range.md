# Example 01: 极值两侧取点 / Points Around an Extremum

## Problem

已知 $a>0$，函数

$$
f(x)=e^x-ax
$$

有两个零点，求 $a$ 的取值范围。

## Key Pattern

中文：先由极小值判断必要性，再在极小值两侧各找一个正值点。取点不是随便取，而是为了和极小值点形成异号。

English: First use the minimum for necessity, then find positive values on both sides of the minimum. The chosen points are selected to create sign changes with the minimum.

## Solution Sketch

求导：

$$
f'(x)=e^x-a.
$$

当 $x<\ln a$ 时，$f'(x)<0$；当 $x>\ln a$ 时，$f'(x)>0$。故

$$
f_{\min}=f(\ln a)=a-a\ln a=a(1-\ln a).
$$

若有两个零点，必须有

$$
a(1-\ln a)<0,
$$

即

$$
a>e.
$$

反过来，若 $a>e$，则

$$
f(\ln a)<0.
$$

左侧取 $x=0$，这是自然端点式特殊点：

$$
f(0)=1>0.
$$

所以在 $(0,\ln a)$ 内有一个零点。

右侧需要找 $x>\ln a$ 使 $f(x)>0$。思路是：指数项最终压过一次项，但最终书写不能只写“趋于无穷”。可以用更强的放缩构造点，例如取足够大的整数 $n$，使 $n>\ln a$ 且 $e^n>an$，于是

$$
f(n)=e^n-an>0.
$$

这里的 $n$ 来自目标不等式 $e^x>ax$，不是凭空取点。由连续性，在 $(\ln a,n)$ 内有另一个零点。

综上：

$$
a>e.
$$

