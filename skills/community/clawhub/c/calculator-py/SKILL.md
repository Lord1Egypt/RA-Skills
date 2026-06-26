---
name: calculator
description: 高性能本地计算器技能，通过 Python 脚本提供数值计算能力。触发场景：(1) Agent 需要进行数学运算（四则、幂、三角、对数等）(2) 需要矩阵运算（乘法、求逆、行列式、特征值、SVD 等）(3) 需要统计分析（均值、标准差、回归、概率分布等）(4) 需要高精度/任意精度计算（大数运算、超越函数等）(5) 需要数值优化（求极值、求根）(6) 需要数值积分或微分方程求解 (7) 需要信号处理（FFT、卷积等）。当 Agent 自行计算可能出错或需要高性能计算库时应优先使用此技能。
---

# Calculator

## Overview

本地高性能计算器，通过 `calc.py` 统一脚本提供数值计算能力，基于 numpy、scipy、mpmath 实现。

## Prerequisites

确保以下库已安装：

```bash
pip3 install scipy mpmath
```

numpy 通常已预装。验证安装：

```bash
python3 -c "import numpy, scipy, mpmath"
```

## Decision Guide

根据计算需求选择子命令：

| 需求 | 子命令 | 示例 |
|------|--------|------|
| 日常数学运算（四则、三角、对数） | `eval` | `eval "sin(pi/4) + sqrt(2)"` |
| 结果可能超过 float64 精度（~15位） | `precision` | `precision "factorial(100)" --precision 50` |
| 大数、阶乘、特殊函数（gamma/zeta） | `precision` | `precision "zeta(3)" --precision 30` |
| 矩阵运算（乘法、求逆、特征值等） | `matrix` | `matrix det --matrix "[[1,2],[3,4]]"` |
| 统计分析（均值、回归、概率分布） | `stats` | `stats describe --data "[1,2,3,4,5]"` |
| 求函数极值或方程根 | `optimize` | `optimize minimize --expr "x**2" --bounds "[-5,5]"` |
| 定积分或微分方程 | `integrate` | `integrate definite --expr "sin(x)" --bounds "[0,pi]"` |
| 傅里叶变换、卷积 | `transform` | `transform fft --data "[1,0,1,0]"` |

**关键区分：** `eval` 用 numpy（float64 ≈15位精度），`precision` 用 mpmath（任意位数）。当 Agent 不确定精度需求时，默认用 `eval`；涉及大数、高精度或特殊数学函数时用 `precision`。

## Output Format

所有子命令的输出格式统一为：

```
=== <子命令> ===
<结果内容>
```

- 结果输出到 **stdout**，错误输出到 **stderr**
- 退出码：成功=0，错误=1 或 2（参数错误）
- 矩阵结果为 Python 列表格式：`[[1.0, 2.0], [3.0, 4.0]]`
- 统计描述为 key-value 对齐格式
- FFT 结果为索引+复数格式：`[0] 4`, `[1] 1 + -2.41421j`

## Quick Reference

```bash
SKILL_DIR=~/.config/opencode/skills/calculator

# 表达式求值
python3 $SKILL_DIR/scripts/calc.py eval "2**10 + sin(pi/4)"
python3 $SKILL_DIR/scripts/calc.py eval "pi" --precision 50

# 矩阵运算
python3 $SKILL_DIR/scripts/calc.py matrix det --matrix "[[1,2],[3,4]]"
python3 $SKILL_DIR/scripts/calc.py matrix inverse --matrix "[[1,2],[3,4]]"

# 统计分析
python3 $SKILL_DIR/scripts/calc.py stats describe --data "[1,2,3,4,5,6,7,8,9,10]"
python3 $SKILL_DIR/scripts/calc.py stats regression --data "[1,2,3]" --data2 "[2,4,6]"

# 任意精度
python3 $SKILL_DIR/scripts/calc.py precision "pi ** 100" --precision 100
python3 $SKILL_DIR/scripts/calc.py precision "factorial(1000)" --precision 50

# 数值优化
python3 $SKILL_DIR/scripts/calc.py optimize minimize --expr "x**2 + 2*x + 1" --bounds "[-10,10]"
python3 $SKILL_DIR/scripts/calc.py optimize root --expr "x**3 - 2*x - 5" --bounds "[1,3]"

# 数值积分
python3 $SKILL_DIR/scripts/calc.py integrate definite --expr "sin(x)" --bounds "[0,pi]"
python3 $SKILL_DIR/scripts/calc.py integrate ode --expr "dy/dx = -y" --bounds "[0,5]" --initial 1

# 信号处理
python3 $SKILL_DIR/scripts/calc.py transform fft --data "[1,0,0,0,0,0,0,0]"
python3 $SKILL_DIR/scripts/calc.py transform convolve --data "[1,2,3]" --data2 "[4,5]"
```

## Usage Guide

### eval — 表达式求值

```bash
calc.py eval <expression> [--precision N]
```

支持：四则运算、幂（`**`）、三角函数（sin/cos/tan/asin/acos/atan）、双曲函数（sinh/cosh/tanh）、对数（log=ln/log2/log10）、sqrt、cbrt、exp、abs、floor、ceil、常数 pi/e/inf/nan。

`--precision` 指定时切换到 mpmath 后端进行高精度计算。

### matrix — 矩阵运算

```bash
calc.py matrix <operation> --matrix "<A>" [--matrix2 "<B>"]
```

| operation | 说明 | 额外参数 |
|-----------|------|----------|
| `multiply` | 矩阵乘法 | `--matrix2` |
| `inverse` | 矩阵求逆 | — |
| `det` | 行列式 | — |
| `eigen` | 特征值/特征向量 | — |
| `transpose` | 转置 | — |
| `svd` | 奇异值分解 | — |
| `rank` | 矩阵秩 | — |
| `solve` | 解线性方程组 Ax=b | `--matrix2` (向量 b) |

矩阵输入使用 Python 字面量：`--matrix "[[1,2],[3,4]]"`

### stats — 统计分析

```bash
calc.py stats <operation> --data "<data>" [--data2 "<data2>"] [--target N]
```

| operation | 说明 | 额外参数 |
|-----------|------|----------|
| `describe` | 描述性统计 | — |
| `corr` | 相关系数 | `--data2` |
| `regression` | 线性回归 | `--data2` |
| `percentile` | 百分位数 | `--target` |
| `pdf` | 概率密度函数 | `--data` (分布名), `--target`, `--params` |
| `cdf` | 累积分布函数 | `--data` (分布名), `--target`, `--params` |

分布名支持：normal/gaussian, uniform, exponential, t, chi2, f

chi2/t/f 分布需要通过 `--params` 传入形状参数：

```bash
# chi2 自由度 df=5
calc.py stats pdf --data "chi2" --target 5 --params "[5]"

# t 分布自由度 df=10
calc.py stats cdf --data "t" --target 2 --params "[10]"

# F 分布 d1=5, d2=10
calc.py stats pdf --data "f" --target 3 --params "[5,10]"
```

### precision — 任意精度

```bash
calc.py precision "<expression>" --precision N
```

始终使用 mpmath 后端。额外支持：factorial, gamma, zeta, binomial（eval 不支持这些函数）。

典型场景：大数阶乘、超越函数高精度值、数论计算。

### optimize — 数值优化

```bash
calc.py optimize <operation> --expr="<expr>" --bounds="[lo,hi]"
```

表达式中的变量为 `x`。支持：minimize, maximize, root。

⚠️ **重要：** 当表达式以 `-` 开头时，必须使用 `=` 语法传参，否则 argparse 会将其误认为参数标志：

```bash
# 正确
calc.py optimize maximize --expr="-x**2+4" --bounds="[-3,3]"
# 错误（argparse 报错）
calc.py optimize maximize --expr "-x**2+4" --bounds "[-3,3]"
```

bounds 支持 pi、e 等数学常数。

### integrate — 数值积分

```bash
calc.py integrate <operation> --expr="<expr>" --bounds="[lo,hi]" [--initial N]
```

- `definite`：定积分，表达式为 f(x)
- `ode`：常微分方程，表达式为 `dy/dx = ...` 或直接写右端，需 `--initial` 指定初值

bounds 支持 pi、e 等数学常数。

### transform — 信号处理

```bash
calc.py transform <operation> --data "<data>" [--data2 "<data2>"]
```

支持：fft, ifft, convolve

## Caveats

- `--precision` 适用于 eval、optimize、integrate，触发 mpmath 后端
- 矩阵输入使用 Python 字面量语法 `[[1,2],[3,4]]`
- bounds 支持数学常数，如 `[0,pi]`、`[-e,e]`
- 表达式使用受限解析器，仅允许数学运算符和函数，不可执行任意代码
- 以 `-` 开头的表达式参数必须用 `--param="value"` 的 `=` 语法
- `matrix solve` 的 `--matrix2` 接受 1D 向量 `[5,6]` 或 2D 列向量 `[[5],[6]]`
- `precision` 独占函数（factorial, gamma, zeta, binomial）在 `eval` 中不可用
- chi2/t/f 分布的 pdf/cdf 需要通过 `--params` 传入形状参数，如 `--params "[5]"` 或 `--params "[3,10]"`

## scripts/

| 脚本 | 说明 |
|------|------|
| `calc.py` | 统一计算入口脚本，通过子命令分发到各计算模块 |
| `test_calc.py` | 测试套件（97 个用例），同时也是完整的用法参考——包含全部子命令的 CLI 入参和预期输出 |

运行测试：

```bash
python3 scripts/test_calc.py           # 运行全部 97 个测试
python3 scripts/test_calc.py --verbose # 显示每个测试的完整输出
python3 scripts/test_calc.py -f eval   # 只运行 eval 相关测试
```

不确定某个子命令的用法时，直接读取 `test_calc.py` 查看对应测试用例。
