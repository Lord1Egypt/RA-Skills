# Calculator — High-Performance Local Calculator Skill

A local skill that provides AI Agents with reliable numerical computation capabilities. Instead of relying on its own reasoning for math, the Agent delegates computation to Python's high-performance libraries (numpy, scipy, mpmath) for accurate results.

## Features

- **7 subcommands** covering everything from basic arithmetic to signal processing
- **Dual-precision backends**: numpy (float64, daily use) and mpmath (arbitrary precision)
- **Safe expression parsing**: restricted math parser — no arbitrary code execution
- **Friendly errors**: clear error messages + fix suggestions, stderr/stdout separation
- **97 test cases**: covering all features, edge cases, and error paths

## Quick Start

### Install Dependencies

```bash
pip3 install scipy mpmath
```

> numpy is usually pre-installed. Verify: `python3 -c "import numpy, scipy, mpmath"`

### Basic Usage

```bash
SKILL_DIR=~/.config/opencode/skills/calculator

# Expression evaluation
python3 $SKILL_DIR/scripts/calc.py eval "2**10 + sin(pi/4)"        # → 1024 + sin(π/4)
python3 $SKILL_DIR/scripts/calc.py eval "pi" --precision 50         # → π to 50 digits

# Matrix operations
python3 $SKILL_DIR/scripts/calc.py matrix det --matrix "[[1,2],[3,4]]"           # → -2
python3 $SKILL_DIR/scripts/calc.py matrix eigen --matrix "[[4,1],[2,3]]"        # → eigenvalues & eigenvectors
python3 $SKILL_DIR/scripts/calc.py matrix solve --matrix "[[2,1],[5,3]]" --matrix2 "[11,27]"  # → [6, -1]

# Statistical analysis
python3 $SKILL_DIR/scripts/calc.py stats describe --data "[1,2,3,4,5,6,7,8,9,10]"
python3 $SKILL_DIR/scripts/calc.py stats regression --data "[1,2,3]" --data2 "[2,4,6]"
python3 $SKILL_DIR/scripts/calc.py stats pdf --data "chi2" --target 5 --params "[5]"

# Arbitrary precision
python3 $SKILL_DIR/scripts/calc.py precision "pi ** 100" --precision 100
python3 $SKILL_DIR/scripts/calc.py precision "zeta(3)" --precision 30           # → Apéry's constant
python3 $SKILL_DIR/scripts/calc.py precision "factorial(1000)" --precision 50

# Numerical optimization
python3 $SKILL_DIR/scripts/calc.py optimize minimize --expr "x**2 - 4*x + 4" --bounds "[-10,10]"  # → x=2, f=0
python3 $SKILL_DIR/scripts/calc.py optimize root --expr "x**3 - 2*x - 5" --bounds "[1,3]"        # → x≈2.0946

# Numerical integration
python3 $SKILL_DIR/scripts/calc.py integrate definite --expr "sin(x)" --bounds "[0,pi]"    # → 2
python3 $SKILL_DIR/scripts/calc.py integrate ode --expr "dy/dx = -2*y" --bounds "[0,3]" --initial 1

# Signal processing
python3 $SKILL_DIR/scripts/calc.py transform fft --data "[1,1,1,1,0,0,0,0]"
python3 $SKILL_DIR/scripts/calc.py transform convolve --data "[1,2,3]" --data2 "[4,5]"
```

## Subcommand Reference

### eval — Expression Evaluation

```bash
calc.py eval <expression> [--precision N]
```

| Category | Supported Functions |
|----------|-------------------|
| Trigonometric | sin, cos, tan, asin, acos, atan |
| Hyperbolic | sinh, cosh, tanh |
| Logarithmic | log (natural), log2, log10 |
| Other | sqrt, cbrt, exp, abs, floor, ceil |
| Constants | pi, e, inf, nan |

Specify `--precision N` to switch to the mpmath backend for high-precision results.

### matrix — Matrix Operations

```bash
calc.py matrix <operation> --matrix "<A>" [--matrix2 "<B>"]
```

| Operation | Description | Notes |
|-----------|-------------|-------|
| `multiply` | Matrix multiplication | Requires `--matrix2` |
| `inverse` | Matrix inverse | Square matrices only |
| `det` | Determinant | Square matrices only |
| `eigen` | Eigenvalues/eigenvectors | Square matrices only |
| `transpose` | Transpose | Any matrix |
| `svd` | Singular value decomposition | Any matrix |
| `rank` | Matrix rank | Any matrix |
| `solve` | Solve Ax=b | `--matrix2` is vector b |

Matrix input uses Python literal syntax: `--matrix "[[1,2],[3,4]]"`

### stats — Statistical Analysis

```bash
calc.py stats <operation> --data "<data>" [--data2 "<...>"] [--target N] [--params "[...]"]
```

| Operation | Description |
|-----------|-------------|
| `describe` | Descriptive statistics (mean, std, quartiles, etc.) |
| `corr` | Pearson correlation coefficient |
| `regression` | Linear regression (slope, intercept, R²) |
| `percentile` | Percentile value |
| `pdf` | Probability density function value |
| `cdf` | Cumulative distribution function value |

Supported distributions: normal/gaussian, uniform, exponential, t, chi2, f

chi2/t/f distributions require shape parameters via `--params`:

```bash
calc.py stats pdf --data "chi2" --target 5 --params "[5]"       # χ²(df=5) PDF at x=5
calc.py stats cdf --data "t" --target 2 --params "[10]"         # t(df=10) CDF at x=2
calc.py stats pdf --data "f" --target 3 --params "[5,10]"       # F(5,10) PDF at x=3
```

### precision — Arbitrary Precision

```bash
calc.py precision "<expression>" --precision N
```

Extends `eval` with additional functions: factorial, gamma, zeta, binomial.

```bash
calc.py precision "pi ** 100" --precision 100      # π¹⁰⁰ to 100 digits
calc.py precision "factorial(1000)" --precision 50 # 1000! to 50 digits
calc.py precision "zeta(3)" --precision 30         # Apéry's constant
calc.py precision "gamma(1/3)" --precision 40      # Γ(1/3)
calc.py precision "binomial(100,50)" --precision 20
```

### optimize — Numerical Optimization

```bash
calc.py optimize <operation> --expr="<expr>" --bounds="[lo,hi]"
```

| Operation | Description |
|-----------|-------------|
| `minimize` | Find minimum on bounded interval |
| `maximize` | Find maximum on bounded interval |
| `root` | Find equation root (brentq method, requires opposite signs at endpoints) |

> ⚠️ Expressions starting with `-` must use `=` syntax: `--expr="-x**2+4"`

Bounds support math constants: `[0,pi]`, `[-e,e]`

### integrate — Numerical Integration

```bash
calc.py integrate <operation> --expr="<expr>" --bounds="[lo,hi]" [--initial N]
```

| Operation | Description |
|-----------|-------------|
| `definite` | Definite integral (quad method) |
| `ode` | ODE numerical solution (solve_ivp) |

ODE examples:

```bash
# dy/dx = -2y, y(0) = 1, on interval [0, 3]
calc.py integrate ode --expr="dy/dx = -2*y" --bounds="[0,3]" --initial 1

# Or write the right-hand side directly
calc.py integrate ode --expr="-2*y" --bounds="[0,3]" --initial 1
```

### transform — Signal Processing

```bash
calc.py transform <operation> --data "<data>" [--data2 "<data2>"]
```

| Operation | Description |
|-----------|-------------|
| `fft` | Fast Fourier Transform |
| `ifft` | Inverse FFT |
| `convolve` | Discrete convolution |

## Output Format

All results follow a unified format:

```
=== <subcommand> ===
<result content>
```

- Results → **stdout** (exit code 0 on success)
- Errors → **stderr** (exit code 1 or 2 on failure)

## Testing

```bash
python3 scripts/test_calc.py           # Run all 97 tests
python3 scripts/test_calc.py --verbose # Show full output per test
python3 scripts/test_calc.py -f eval   # Run only eval tests
python3 scripts/test_calc.py -f matrix # Run only matrix tests
```

> `test_calc.py` is the best usage reference itself — it contains complete CLI arguments and expected outputs for all 7 subcommands.

## File Structure

```
calculator/
├── SKILL.md              # Skill document (for AI Agents)
├── README.md             # Project documentation (for humans)
└── scripts/
    ├── calc.py           # Unified calculator script (~760 lines)
    └── test_calc.py      # Test suite (97 cases)
```

## Dependencies

| Library | Version | Used By |
|---------|---------|---------|
| numpy | 2.4.3+ | eval, matrix, stats, transform |
| scipy | 1.17.1+ | stats (distributions), optimize, integrate, transform |
| mpmath | 1.4.1+ | precision, eval (high-precision mode) |


