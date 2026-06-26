# Example 02: 弱项替换取正值 / Replacing a Weak Term

## Problem

已知

$$
f(x)=ae^{2x}+(a-2)e^x-x,\qquad 0<a<1.
$$

寻找一点 $x_0$，使 $f(x_0)>0$。

## Point Origin

中文：因为 $x$ 相比指数项是弱项，可用 $x<e^x$ 把 $-x$ 放大为 $-e^x$，从而得到一个更容易控制的下界。

English: Since $x$ is weaker than exponential terms, use $x<e^x$ to replace $-x$ by the smaller $-e^x$, creating a manageable lower bound.

## Solution

由 $x<e^x$，得

$$
f(x)>ae^{2x}+(a-2)e^x-e^x
=e^x(ae^x+a-3).
$$

只需让

$$
ae^x+a-3>0.
$$

即

$$
e^x>\frac{3-a}{a}.
$$

所以可以要求

$$
x>\ln\frac{3-a}{a}.
$$

为了取点更干净，取

$$
x_0=\ln\frac4a.
$$

因为 $0<a<1$，有

$$
\frac4a>\frac{3-a}{a}.
$$

于是

$$
ae^{x_0}+a-3=a\cdot\frac4a+a-3=a+1>0.
$$

从而

$$
f(x_0)>0.
$$

The point $x_0=\ln(4/a)$ is not arbitrary; it is a clean over-solution of the threshold $x>\ln((3-a)/a)$.

