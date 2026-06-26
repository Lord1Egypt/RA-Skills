# Example 04: 先局部化再统一放缩 / Localize Before Bounding

## Problem Pattern

在某些导数题中，需要找到 $x_0$，使

$$
(1+x_0)e^{x_0}+\frac{a}{x_0}<0,\qquad a<0.
$$

## Point Origin

中文：难点在 $(1+x)e^x$ 不容易全局控制。先把 $x$ 限制在 $(0,1)$，再使用统一上界。

English: The term $(1+x)e^x$ is hard to control globally. Restrict $x$ to $(0,1)$ first, then use a uniform upper bound.

## Construction

当 $0<x<1$ 时，

$$
1+x<2,\qquad e^x<e,
$$

所以

$$
(1+x)e^x<2e.
$$

因此若希望

$$
(1+x)e^x+\frac{a}{x}<0,
$$

只需保证

$$
2e+\frac{a}{x}<0.
$$

因为 $a<0$，这等价于

$$
x<-\frac{a}{2e}.
$$

同时还要 $0<x<1$，故令

$$
t=\min\left(1,-\frac{a}{2e}\right),
$$

取

$$
x_0=\frac{t}{2}.
$$

则 $0<x_0<1$，且 $x_0<-a/(2e)$，从而

$$
(1+x_0)e^{x_0}+\frac{a}{x_0}
<2e+\frac{a}{x_0}<0.
$$

This is a typical “localize first, then pick half of the safe threshold” construction.

