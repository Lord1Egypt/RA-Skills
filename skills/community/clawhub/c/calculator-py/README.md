# Calculator — 高性能本地计算器技能

为 AI Agent 提供可靠数值计算能力的本地技能。当 Agent 面临数学运算时，无需依赖自身推理，而是通过 Python 高性能计算库（numpy、scipy、mpmath）获得精确结果。

## 特性

- **7 个子命令**，覆盖从基础运算到信号处理的完整计算场景
- **双精度后端**：numpy（float64，日常计算）与 mpmath（任意精度，高精度需求）
- **安全解析**：受限数学表达式解析器，不执行任意代码
- **友好错误**：清晰的错误信息 + 修正建议，stderr/stdout 分离
- **97 个测试用例**：覆盖全部功能、边界场景和错误路径

## 快速开始

### 安装依赖

```bash
pip3 install scipy mpmath
```

> numpy 通常已预装。验证：`python3 -c "import numpy, scipy, mpmath"`

### 基本用法

```bash
SKILL_DIR=~/.config/opencode/skills/calculator

# 表达式求值
python3 $SKILL_DIR/scripts/calc.py eval "2**10 + sin(pi/4)"        # → 1024 + sin(π/4)
python3 $SKILL_DIR/scripts/calc.py eval "pi" --precision 50         # → π 精确到 50 位

# 矩阵运算
python3 $SKILL_DIR/scripts/calc.py matrix det --matrix "[[1,2],[3,4]]"           # → -2
python3 $SKILL_DIR/scripts/calc.py matrix eigen --matrix "[[4,1],[2,3]]"        # → 特征值与特征向量
python3 $SKILL_DIR/scripts/calc.py matrix solve --matrix "[[2,1],[5,3]]" --matrix2 "[11,27]"  # → [6, -1]

# 统计分析
python3 $SKILL_DIR/scripts/calc.py stats describe --data "[1,2,3,4,5,6,7,8,9,10]"
python3 $SKILL_DIR/scripts/calc.py stats regression --data "[1,2,3]" --data2 "[2,4,6]"
python3 $SKILL_DIR/scripts/calc.py stats pdf --data "chi2" --target 5 --params "[5]"

# 任意精度
python3 $SKILL_DIR/scripts/calc.py precision "pi ** 100" --precision 100
python3 $SKILL_DIR/scripts/calc.py precision "zeta(3)" --precision 30           # → 阿培里常数
python3 $SKILL_DIR/scripts/calc.py precision "factorial(1000)" --precision 50

# 数值优化
python3 $SKILL_DIR/scripts/calc.py optimize minimize --expr "x**2 - 4*x + 4" --bounds "[-10,10]"  # → x=2, f=0
python3 $SKILL_DIR/scripts/calc.py optimize root --expr "x**3 - 2*x - 5" --bounds "[1,3]"        # → x≈2.0946

# 数值积分
python3 $SKILL_DIR/scripts/calc.py integrate definite --expr "sin(x)" --bounds "[0,pi]"    # → 2
python3 $SKILL_DIR/scripts/calc.py integrate ode --expr "dy/dx = -2*y" --bounds "[0,3]" --initial 1

# 信号处理
python3 $SKILL_DIR/scripts/calc.py transform fft --data "[1,1,1,1,0,0,0,0]"
python3 $SKILL_DIR/scripts/calc.py transform convolve --data "[1,2,3]" --data2 "[4,5]"
```

## 子命令参考

### eval — 表达式求值

```bash
calc.py eval <expression> [--precision N]
```

| 函数类别 | 支持的函数 |
|---------|-----------|
| 三角函数 | sin, cos, tan, asin, acos, atan |
| 双曲函数 | sinh, cosh, tanh |
| 对数 | log (自然对数), log2, log10 |
| 其他 | sqrt, cbrt, exp, abs, floor, ceil |
| 常数 | pi, e, inf, nan |

指定 `--precision N` 时自动切换到 mpmath 后端。

### matrix — 矩阵运算

```bash
calc.py matrix <operation> --matrix "<A>" [--matrix2 "<B>"]
```

| 操作 | 说明 | 示例 |
|------|------|------|
| `multiply` | 矩阵乘法 | 需要 `--matrix2` |
| `inverse` | 矩阵求逆 | 仅方阵 |
| `det` | 行列式 | 仅方阵 |
| `eigen` | 特征值/特征向量 | 仅方阵 |
| `transpose` | 转置 | 任意矩阵 |
| `svd` | 奇异值分解 | 任意矩阵 |
| `rank` | 矩阵秩 | 任意矩阵 |
| `solve` | 解 Ax=b | `--matrix2` 为向量 b |

### stats — 统计分析

```bash
calc.py stats <operation> --data "<data>" [--data2 "<...>"] [--target N] [--params "[...]"]
```

| 操作 | 说明 |
|------|------|
| `describe` | 描述性统计（均值、标准差、分位数等） |
| `corr` | Pearson 相关系数 |
| `regression` | 线性回归（斜率、截距、R²） |
| `percentile` | 百分位数 |
| `pdf` | 概率密度函数值 |
| `cdf` | 累积分布函数值 |

支持分布：normal/gaussian, uniform, exponential, t, chi2, f

chi2/t/f 分布需通过 `--params` 传入形状参数：

```bash
calc.py stats pdf --data "chi2" --target 5 --params "[5]"       # χ²(df=5) 在 x=5 的 PDF
calc.py stats cdf --data "t" --target 2 --params "[10]"         # t(df=10) 在 x=2 的 CDF
calc.py stats pdf --data "f" --target 3 --params "[5,10]"       # F(5,10) 在 x=3 的 PDF
```

### precision — 任意精度

```bash
calc.py precision "<expression>" --precision N
```

在 eval 基础上额外支持：factorial, gamma, zeta, binomial。

```bash
calc.py precision "pi ** 100" --precision 100      # π¹⁰⁰ 精确到 100 位
calc.py precision "factorial(1000)" --precision 50 # 1000! 精确到 50 位
calc.py precision "zeta(3)" --precision 30         # 阿培里常数
calc.py precision "gamma(1/3)" --precision 40      # Γ(1/3)
calc.py precision "binomial(100,50)" --precision 20
```

### optimize — 数值优化

```bash
calc.py optimize <operation> --expr="<expr>" --bounds="[lo,hi]"
```

| 操作 | 说明 |
|------|------|
| `minimize` | 有界区间内求最小值 |
| `maximize` | 有界区间内求最大值 |
| `root` | 求方程根（brentq 法，要求端点异号） |

> ⚠️ 表达式以 `-` 开头时必须用 `=` 语法：`--expr="-x**2+4"`

bounds 支持数学常数：`[0,pi]`、`[-e,e]`

### integrate — 数值积分

```bash
calc.py integrate <operation> --expr="<expr>" --bounds="[lo,hi]" [--initial N]
```

| 操作 | 说明 |
|------|------|
| `definite` | 定积分（quad 法） |
| `ode` | 常微分方程数值解（solve_ivp） |

ODE 示例：

```bash
# dy/dx = -2y, y(0) = 1，求解区间 [0, 3]
calc.py integrate ode --expr="dy/dx = -2*y" --bounds="[0,3]" --initial 1

# 也支持直接写右端
calc.py integrate ode --expr="-2*y" --bounds="[0,3]" --initial 1
```

### transform — 信号处理

```bash
calc.py transform <operation> --data "<data>" [--data2 "<data2>"]
```

| 操作 | 说明 |
|------|------|
| `fft` | 快速傅里叶变换 |
| `ifft` | 逆傅里叶变换 |
| `convolve` | 离散卷积 |

## 输出格式

所有结果统一格式：

```
=== <子命令> ===
<结果内容>
```

- 结果 → **stdout**（成功退出码 0）
- 错误 → **stderr**（失败退出码 1 或 2）

## 测试

```bash
python3 scripts/test_calc.py           # 运行全部 97 个测试
python3 scripts/test_calc.py --verbose # 显示每个测试的完整输出
python3 scripts/test_calc.py -f eval   # 只运行 eval 相关测试
python3 scripts/test_calc.py -f matrix # 只运行 matrix 相关测试
```

> `test_calc.py` 本身就是最好的用法参考——包含全部 7 个子命令的完整 CLI 入参和预期输出。

## 文件结构

```
calculator/
├── SKILL.md              # 技能主文档（面向 AI Agent）
├── README.md             # 项目文档（面向人类）
└── scripts/
    ├── calc.py           # 统一计算脚本（~760 行）
    └── test_calc.py      # 测试套件（97 用例）
```

## 依赖

| 库 | 版本 | 用途 |
|----|------|------|
| numpy | 2.4.3+ | eval、matrix、stats、transform |
| scipy | 1.17.1+ | stats（分布）、optimize、integrate、transform |
| mpmath | 1.4.1+ | precision、eval（高精度模式） |


