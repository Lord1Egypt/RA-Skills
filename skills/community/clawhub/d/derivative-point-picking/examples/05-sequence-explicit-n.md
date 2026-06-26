# Example 05: 数列中显式取足够大的 $n$ / Explicit Large-$n$ Choice

## Problem Pattern

已知对任意 $n\ge 2$，有

$$
2-\frac{3}{2^{n-1}+1}<q<2+\frac{3}{2^{n-1}-1}.
$$

证明 $q=2$。

## Why Not Only Use Limits

中文：直接令 $n\to\infty$ 得 $q=2$ 很快，但在一些高考书写中，可以把它改成反证 + 显式取 $n$，避免只依赖极限语言。

English: Taking $n\to\infty$ is fast, but in exam-style writing it can be rewritten as contradiction with an explicit large $n$.

## Explicit Proof

若 $q>2$，则希望右端

$$
2+\frac{3}{2^{n-1}-1}
$$

小于或等于 $q$，从而与原不等式矛盾。

只需

$$
\frac{3}{2^{n-1}-1}\le q-2.
$$

即

$$
2^{n-1}\ge \frac{3}{q-2}+1.
$$

因此可取

$$
n=\left[\log_2\left(\frac{3}{q-2}+1\right)\right]+2.
$$

此时原不等式右边不成立，矛盾。

同理，若 $q<2$，只需让

$$
\frac{3}{2^{n-1}+1}\le 2-q,
$$

取足够大的 $n$ 即可推出左边不成立，矛盾。

故只能有

$$
q=2.
$$

The selected $n$ is the threshold needed to break the inequality, not a vague “large enough” gesture.

