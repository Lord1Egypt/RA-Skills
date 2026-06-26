# Example 03: 负半轴取点 / Picking a Point on a Negative Interval

## Problem

已知

$$
f(x)=e^x+ax,\qquad a>0.
$$

证明 $f(x)$ 在 $(-\infty,0)$ 上有一个零点。

## Point Origin

中文：在负半轴上，指数项 $e^x$ 很小，线性项 $ax$ 为负且可控。为了找负值点，用 $e^x<1$。

English: On the negative interval, $e^x$ is small while $ax$ is negative. To find a negative value, use $e^x<1$.

## Solution

先注意

$$
f'(x)=e^x+a>0.
$$

所以 $f(x)$ 在 $(-\infty,0)$ 上单调递增，零点至多一个。

又

$$
f(0)=1>0.
$$

接下来找 $x_0<0$，使 $f(x_0)<0$。当 $x<0$ 时，

$$
0<e^x<1,
$$

故

$$
f(x)=e^x+ax<1+ax.
$$

只需

$$
1+ax\le 0,
$$

即

$$
x\le -\frac1a.
$$

取

$$
x_0=-\frac1a.
$$

则

$$
f(x_0)<1+a\left(-\frac1a\right)=0.
$$

由连续性，$f(x)$ 在 $(x_0,0)$ 内有零点；由单调性，零点唯一。

