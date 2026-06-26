#!/usr/bin/env python3
"""
test_calc.py — Calculator skill test suite

Runs all subcommands with comprehensive test data and validates outputs.
Serves as both regression test and living documentation of expected behavior.

Usage:
    python3 test_calc.py
    python3 test_calc.py --verbose    # show full output for each test
    python3 test_calc.py --filter eval # run only eval tests
"""

import subprocess
import sys
import os
import re
from pathlib import Path

CALC_PATH = Path(__file__).parent / "calc.py"

# ============================================================
# Test Case Format:
#   (name, args_list, expect_stdout_contains, expect_stderr_contains, expect_exit_code)
#
#   - name: human-readable test name
#   - args_list: list of CLI arguments to calc.py
#   - expect_stdout_contains: str to search in stdout (None = skip check)
#   - expect_stderr_contains: str to search in stderr (None = skip check)
#   - expect_exit_code: expected exit code (default 0)
# ============================================================

TESTS = [
    # ─────────────────────────────────────────────
    # eval — Expression Evaluation (numpy backend)
    # ─────────────────────────────────────────────
    ("eval: basic addition", ["eval", "2+3"], "5", None, 0),
    ("eval: subtraction", ["eval", "100-37"], "63", None, 0),
    ("eval: multiplication", ["eval", "7*8"], "56", None, 0),
    ("eval: division", ["eval", "22/7"], "3.142857", None, 0),
    ("eval: power", ["eval", "2**10"], "1024", None, 0),
    ("eval: large power", ["eval", "2**100"], "1.26765", None, 0),
    ("eval: sin", ["eval", "sin(pi/4)"], "0.7071", None, 0),
    ("eval: cos(0)", ["eval", "cos(0)"], "1", None, 0),
    ("eval: tan(pi/4)", ["eval", "tan(pi/4)"], "0.9999", None, 0),
    ("eval: asin(1)", ["eval", "asin(1)"], "1.5707", None, 0),
    ("eval: acos(1)", ["eval", "acos(1)"], "0", None, 0),
    ("eval: atan(1)", ["eval", "atan(1)"], "0.7853", None, 0),
    ("eval: sinh(1)", ["eval", "sinh(1)"], "1.1752", None, 0),
    ("eval: cosh(0)", ["eval", "cosh(0)"], "1", None, 0),
    ("eval: tanh(0)", ["eval", "tanh(0)"], "0", None, 0),
    ("eval: sqrt(2)", ["eval", "sqrt(2)"], "1.414", None, 0),
    ("eval: cbrt(27)", ["eval", "cbrt(27)"], "3", None, 0),
    ("eval: log(exp(5))", ["eval", "log(exp(5))"], "5", None, 0),
    ("eval: log2(1024)", ["eval", "log2(1024)"], "10", None, 0),
    ("eval: log10(1000)", ["eval", "log10(1000)"], "3", None, 0),
    ("eval: exp(0)", ["eval", "exp(0)"], "1", None, 0),
    ("eval: abs(-42)", ["eval", "abs(-42)"], "42", None, 0),
    ("eval: floor(3.7)", ["eval", "floor(3.7)"], "3", None, 0),
    ("eval: ceil(3.2)", ["eval", "ceil(3.2)"], "4", None, 0),
    ("eval: e constant", ["eval", "e"], "2.718", None, 0),
    ("eval: sin+sqrt combo", ["eval", "sin(pi/4) + sqrt(2)"], "2.1213", None, 0),
    # eval — mpmath backend (high precision)
    (
        "eval: pi precision 30",
        ["eval", "pi", "--precision", "30"],
        "3.14159265358979323846264338328",
        None,
        0,
    ),
    (
        "eval: e precision 20",
        ["eval", "e", "--precision", "20"],
        "2.7182818284590452354",
        None,
        0,
    ),
    ("eval: precision 0 test", ["eval", "0", "--precision", "50"], "0", None, 0),
    # eval — error cases
    (
        "eval: invalid expression",
        ["eval", "???"],
        None,
        "Expression evaluation failed",
        1,
    ),
    ("eval: division by zero", ["eval", "1/0"], None, "division by zero", 1),
    (
        "eval: security (builtins blocked)",
        ["eval", "__import__('os')"],
        None,
        "Expression evaluation failed",
        1,
    ),
    # ─────────────────────────────────────────────
    # matrix — Matrix Operations
    # ─────────────────────────────────────────────
    ("matrix: det 2x2", ["matrix", "det", "--matrix", "[[1,2],[3,4]]"], "-2", None, 0),
    (
        "matrix: det 3x3",
        ["matrix", "det", "--matrix", "[[1,2,3],[4,5,6],[7,8,9]]"],
        "0",
        None,
        0,
    ),
    ("matrix: det 1x1", ["matrix", "det", "--matrix", "[[5]]"], "5", None, 0),
    (
        "matrix: multiply",
        [
            "matrix",
            "multiply",
            "--matrix",
            "[[1,2],[3,4]]",
            "--matrix2",
            "[[5,6],[7,8]]",
        ],
        "[[19.0, 22.0], [43.0, 50.0]]",
        None,
        0,
    ),
    (
        "matrix: inverse 2x2",
        ["matrix", "inverse", "--matrix", "[[1,2],[3,4]]"],
        "-1.999",
        None,
        0,
    ),
    (
        "matrix: eigen 2x2",
        ["matrix", "eigen", "--matrix", "[[4,1],[2,3]]"],
        "Eigenvalues:",
        None,
        0,
    ),
    (
        "matrix: transpose",
        ["matrix", "transpose", "--matrix", "[[1,2,3],[4,5,6]]"],
        "[[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]",
        None,
        0,
    ),
    ("matrix: svd", ["matrix", "svd", "--matrix", "[[1,2],[3,4]]"], "S:", None, 0),
    (
        "matrix: rank full",
        ["matrix", "rank", "--matrix", "[[1,2],[3,4]]"],
        "2",
        None,
        0,
    ),
    (
        "matrix: rank deficient",
        ["matrix", "rank", "--matrix", "[[1,2,3],[4,5,6],[7,8,9]]"],
        "2",
        None,
        0,
    ),
    ("matrix: rank 1x1", ["matrix", "rank", "--matrix", "[[5]]"], "1", None, 0),
    (
        "matrix: solve",
        ["matrix", "solve", "--matrix", "[[2,1],[5,3]]", "--matrix2", "[11,27]"],
        "5.999",
        None,
        0,
    ),
    (
        "matrix: solve with 2D b",
        ["matrix", "solve", "--matrix", "[[1,0],[0,1]]", "--matrix2", "[[5],[6]]"],
        "[5.0, 6.0]",
        None,
        0,
    ),
    (
        "matrix: non-square multiply",
        [
            "matrix",
            "multiply",
            "--matrix",
            "[[1,2,3],[4,5,6]]",
            "--matrix2",
            "[[1,2],[3,4],[5,6]]",
        ],
        "[[22.0, 28.0], [49.0, 64.0]]",
        None,
        0,
    ),
    # matrix — error cases
    (
        "matrix: singular inverse",
        ["matrix", "inverse", "--matrix", "[[1,2],[2,4]]"],
        None,
        "Singular matrix",
        1,
    ),
    (
        "matrix: non-square det",
        ["matrix", "det", "--matrix", "[[1,2,3],[4,5,6]]"],
        None,
        "square matrix",
        1,
    ),
    (
        "matrix: shape mismatch multiply",
        ["matrix", "multiply", "--matrix", "[[1,2],[3,4]]", "--matrix2", "[[1,2,3]]"],
        None,
        "Shape mismatch",
        1,
    ),
    ("matrix: missing --matrix", ["matrix", "det"], None, "required", 2),
    # ─────────────────────────────────────────────
    # stats — Statistical Analysis
    # ─────────────────────────────────────────────
    (
        "stats: describe basic",
        ["stats", "describe", "--data", "[1,2,3,4,5,6,7,8,9,10]"],
        "mean:     5.5",
        None,
        0,
    ),
    (
        "stats: describe single element",
        ["stats", "describe", "--data", "[42]"],
        "mean:     42",
        None,
        0,
    ),
    (
        "stats: describe single std",
        ["stats", "describe", "--data", "[42]"],
        "N/A (need >1 value)",
        None,
        0,
    ),
    (
        "stats: corr perfect positive",
        ["stats", "corr", "--data", "[1,2,3,4,5]", "--data2", "[2,4,6,8,10]"],
        "1.000000",
        None,
        0,
    ),
    (
        "stats: corr perfect negative",
        ["stats", "corr", "--data", "[1,2,3,4,5]", "--data2", "[10,8,6,4,2]"],
        "-1.000000",
        None,
        0,
    ),
    (
        "stats: regression perfect",
        ["stats", "regression", "--data", "[1,2,3,4,5]", "--data2", "[2,4,6,8,10]"],
        "slope (m):     2",
        None,
        0,
    ),
    (
        "stats: regression R2",
        ["stats", "regression", "--data", "[1,2,3,4,5]", "--data2", "[2,4,6,8,10]"],
        "R²:            1.000000",
        None,
        0,
    ),
    (
        "stats: percentile",
        ["stats", "percentile", "--data", "[1,2,3,4,5,6,7,8,9,10]", "--target", "90"],
        "P90.0 = 9.1",
        None,
        0,
    ),
    (
        "stats: pdf normal",
        ["stats", "pdf", "--data", "normal", "--target", "1.96"],
        "0.05844",
        None,
        0,
    ),
    (
        "stats: cdf normal",
        ["stats", "cdf", "--data", "normal", "--target", "1.96"],
        "0.97500",
        None,
        0,
    ),
    (
        "stats: pdf exponential",
        ["stats", "pdf", "--data", "exponential", "--target", "1"],
        "0.367879",
        None,
        0,
    ),
    (
        "stats: pdf chi2 with params",
        ["stats", "pdf", "--data", "chi2", "--target", "5", "--params", "[3]"],
        "0.07322",
        None,
        0,
    ),
    (
        "stats: cdf t with params",
        ["stats", "cdf", "--data", "t", "--target", "2", "--params", "[10]"],
        "0.963306",
        None,
        0,
    ),
    (
        "stats: pdf f with params",
        ["stats", "pdf", "--data", "f", "--target", "3", "--params", "[5,10]"],
        "0.05582",
        None,
        0,
    ),
    # stats — error cases
    (
        "stats: missing --data2 for corr",
        ["stats", "corr", "--data", "[1,2,3]"],
        None,
        "requires --data2",
        1,
    ),
    (
        "stats: unknown distribution",
        ["stats", "pdf", "--data", "nonexistent", "--target", "1"],
        None,
        "Unknown distribution",
        1,
    ),
    # ─────────────────────────────────────────────
    # precision — Arbitrary Precision
    # ─────────────────────────────────────────────
    (
        "precision: pi 100 digits",
        ["precision", "pi", "--precision", "100"],
        "3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117068",
        None,
        0,
    ),
    (
        "precision: e 50 digits",
        ["precision", "e", "--precision", "50"],
        "2.7182818284590452353602874713526624977572470937",
        None,
        0,
    ),
    (
        "precision: zeta(3)",
        ["precision", "zeta(3)", "--precision", "30"],
        "1.20205690315959428539973816151",
        None,
        0,
    ),
    (
        "precision: factorial(100)",
        ["precision", "factorial(100)", "--precision", "50"],
        "9.3326215443944152681699238856266700490715968264382",
        None,
        0,
    ),
    (
        "precision: gamma(5)",
        ["precision", "gamma(5)", "--precision", "20"],
        "24",
        None,
        0,
    ),
    (
        "precision: binomial(10,3)",
        ["precision", "binomial(10,3)", "--precision", "20"],
        "120",
        None,
        0,
    ),
    (
        "precision: sqrt(2)",
        ["precision", "sqrt(2)", "--precision", "50"],
        "1.4142135623730950488016887242096980785696718753769",
        None,
        0,
    ),
    (
        "precision: log(2)",
        ["precision", "log(2)", "--precision", "30"],
        "0.693147180559945309417232121458",
        None,
        0,
    ),
    (
        "precision: sin(1)",
        ["precision", "sin(1)", "--precision", "30"],
        "0.84147098480789650665250232163",
        None,
        0,
    ),
    (
        "precision: large pi**1000",
        ["precision", "pi ** 1000", "--precision", "200"],
        "1.41212354451576481231043973288158763547596346158",
        None,
        0,
    ),
    # ─────────────────────────────────────────────
    # optimize — Numerical Optimization
    # ─────────────────────────────────────────────
    (
        "optimize: minimize parabola",
        ["optimize", "minimize", "--expr", "x**2 - 4*x + 4", "--bounds", "[-10,10]"],
        "x = 2",
        None,
        0,
    ),
    (
        "optimize: minimize result",
        ["optimize", "minimize", "--expr", "x**2 - 4*x + 4", "--bounds", "[-10,10]"],
        "f(x) = 0",
        None,
        0,
    ),
    (
        "optimize: maximize",
        ["optimize", "maximize", "--expr=-x**2+4", "--bounds=[-3,3]"],
        "f(x) = 4",
        None,
        0,
    ),
    (
        "optimize: root sqrt(2)",
        ["optimize", "root", "--expr", "x**2 - 2", "--bounds", "[1,2]"],
        "1.414213562",
        None,
        0,
    ),
    (
        "optimize: root cubic",
        ["optimize", "root", "--expr", "x**3 - 2*x - 5", "--bounds", "[1,3]"],
        "2.094",
        None,
        0,
    ),
    (
        "optimize: bounds with pi",
        ["optimize", "minimize", "--expr", "sin(x)", "--bounds", "[0,pi]"],
        "f(x) = 3.81959",  # sin(x) min on [0,pi] ≈ 0 at x=pi
        None,
        0,
    ),
    # optimize — error cases
    (
        "optimize: same-sign bounds root",
        ["optimize", "root", "--expr", "x**2+1", "--bounds", "[0,5]"],
        None,
        "opposite signs",
        1,
    ),
    # ─────────────────────────────────────────────
    # integrate — Numerical Integration
    # ─────────────────────────────────────────────
    (
        "integrate: sin from 0 to pi",
        ["integrate", "definite", "--expr", "sin(x)", "--bounds", "[0,pi]"],
        "= 2",
        None,
        0,
    ),
    (
        "integrate: x^2 from 0 to 1",
        ["integrate", "definite", "--expr", "x**2", "--bounds", "[0,1]"],
        "= 0.3333333333",
        None,
        0,
    ),
    (
        "integrate: 1/x from 1 to 10",
        ["integrate", "definite", "--expr", "1/x", "--bounds", "[1,10]"],
        "= 2.302585093",
        None,
        0,
    ),
    (
        "integrate: exp from 0 to 1",
        ["integrate", "definite", "--expr", "exp(x)", "--bounds", "[0,1]"],
        "= 1.718281828",
        None,
        0,
    ),
    (
        "integrate: ODE exponential decay",
        [
            "integrate",
            "ode",
            "--expr",
            "dy/dx = -2*y",
            "--bounds",
            "[0,3]",
            "--initial",
            "1",
        ],
        "ODE: dy/dx = -2*y",
        None,
        0,
    ),
    (
        "integrate: ODE result at x=3",
        [
            "integrate",
            "ode",
            "--expr",
            "dy/dx = -2*y",
            "--bounds",
            "[0,3]",
            "--initial",
            "1",
        ],
        "0.00248",
        None,
        0,
    ),
    (
        "integrate: ODE cos(x)",
        [
            "integrate",
            "ode",
            "--expr",
            "dy/dx = cos(x)",
            "--bounds",
            "[0,pi]",
            "--initial",
            "0",
        ],
        "ODE: dy/dx = cos(x)",
        None,
        0,
    ),
    # ─────────────────────────────────────────────
    # transform — Signal Processing
    # ─────────────────────────────────────────────
    (
        "transform: fft delta",
        ["transform", "fft", "--data", "[1,0,0,0,0,0,0,0]"],
        "[0] 1",
        None,
        0,
    ),
    (
        "transform: fft box",
        ["transform", "fft", "--data", "[1,1,1,1,0,0,0,0]"],
        "[0] 4",
        None,
        0,
    ),
    (
        "transform: fft single element",
        ["transform", "fft", "--data", "[1]"],
        "[0] 1",
        None,
        0,
    ),
    (
        "transform: ifft roundtrip",
        ["transform", "ifft", "--data", "[4,1,0,1,0,1,0,1]"],
        "[0] 1",
        None,
        0,
    ),
    (
        "transform: convolve basic",
        ["transform", "convolve", "--data", "[1,2,3]", "--data2", "[4,5]"],
        "[4.0, 13.0, 22.0, 15.0]",
        None,
        0,
    ),
    (
        "transform: convolve single+list",
        ["transform", "convolve", "--data", "[1]", "--data2", "[2,3]"],
        "[2.0, 3.0]",
        None,
        0,
    ),
    (
        "transform: convolve with decimals",
        ["transform", "convolve", "--data", "[1,2,3]", "--data2", "[0,1,0.5]"],
        "[0.0, 1.0, 2.5, 4.0, 1.5]",
        None,
        0,
    ),
]


def run_test(
    name: str,
    args: list,
    expect_stdout: str | None,
    expect_stderr: str | None,
    expect_exit: int,
    verbose: bool,
) -> tuple[bool, str]:
    """Run a single test case. Returns (passed, message)."""
    cmd = [sys.executable, str(CALC_PATH)] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        return False, f"TIMEOUT after 30s"
    except Exception as e:
        return False, f"EXECUTION ERROR: {e}"

    errors = []

    # Check exit code
    if result.returncode != expect_exit:
        errors.append(f"exit={result.returncode}, expected={expect_exit}")

    # Check stdout
    if expect_stdout is not None and expect_stdout not in result.stdout:
        errors.append(f"stdout missing '{expect_stdout}'")
        if verbose:
            errors.append(f"  got stdout: {result.stdout.strip()!r}")

    # Check stderr
    if expect_stderr is not None and expect_stderr not in result.stderr:
        errors.append(f"stderr missing '{expect_stderr}'")
        if verbose:
            errors.append(f"  got stderr: {result.stderr.strip()!r}")

    if errors:
        return False, "; ".join(errors)

    if verbose:
        return True, result.stdout.strip()
    return True, "OK"


def main():
    args_parser = __import__("argparse").ArgumentParser(
        description="Calculator skill test suite"
    )
    args_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show full output"
    )
    args_parser.add_argument(
        "--filter", "-f", default=None, help="Run only tests matching this substring"
    )
    cli_args = args_parser.parse_args()

    if not CALC_PATH.exists():
        print(f"Error: calc.py not found at {CALC_PATH}", file=sys.stderr)
        sys.exit(1)

    # Filter tests
    tests = TESTS
    if cli_args.filter:
        keyword = cli_args.filter.lower()
        tests = [t for t in tests if keyword in t[0].lower()]

    if not tests:
        print(f"No tests match filter '{cli_args.filter}'")
        sys.exit(0)

    print(f"Calculator Test Suite")
    print(f"=====================")
    print(f"Total: {len(tests)} tests\n")

    passed = 0
    failed = 0
    failures = []

    for name, cmd_args, expect_out, expect_err, expect_exit in tests:
        ok, msg = run_test(
            name, cmd_args, expect_out, expect_err, expect_exit, cli_args.verbose
        )
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
            if cli_args.verbose:
                print(f"  ✓ {name}: {msg}")
            else:
                print(f"  ✓ {name}")
        else:
            failed += 1
            failures.append((name, msg, cmd_args))
            print(f"  ✗ {name}: {msg}")

    print(f"\n{'=' * 50}")
    print(f"  PASSED: {passed} / {len(tests)}")
    if failed:
        print(f"  FAILED: {failed}")
        print(f"\nFailed tests:")
        for name, msg, cmd_args in failures:
            cmd_str = " ".join(cmd_args)
            print(f"  ✗ {name}")
            print(f"    cmd: python3 calc.py {cmd_str}")
            print(f"    err: {msg}")
    print(f"{'=' * 50}")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
