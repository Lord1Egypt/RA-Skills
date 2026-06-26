#!/usr/bin/env python3
"""
calc.py - High-performance calculator for AI Agents

Provides numerical computation via subcommands:
  eval, matrix, stats, precision, optimize, integrate, transform

Usage:
    python3 calc.py eval "2**10 + sin(pi/4)"
    python3 calc.py matrix det --matrix "[[1,2],[3,4]]"
    python3 calc.py stats describe --data "[1,2,3,4,5]"
    python3 calc.py precision "pi" --precision 50
"""

import argparse
import ast
import sys
import math
from typing import Any


# ============================================================
# Core Utilities
# ============================================================


def error_exit(msg: str, suggestion: str = "") -> None:
    """Print error to stderr and exit with code 1."""
    print(f"Error: {msg}", file=sys.stderr)
    if suggestion:
        print(f"  {suggestion}", file=sys.stderr)
    sys.exit(1)


def format_output(header: str, content: str) -> None:
    """Print formatted result to stdout."""
    print(f"=== {header} ===")
    print(content)


def safe_parse_literal(s: str) -> Any:
    """Safely parse a Python literal string (lists, dicts, numbers)."""
    try:
        return ast.literal_eval(s)
    except (SyntaxError, ValueError) as e:
        error_exit(f"Invalid input: {s}", f"Expected valid Python literal. {e}")


def parse_data_list(s: str) -> list:
    """Parse a comma/space-separated or Python list string into a list of numbers."""
    s = s.strip()
    try:
        result = ast.literal_eval(s)
        if isinstance(result, (list, tuple)):
            return [float(x) for x in result]
    except (SyntaxError, ValueError):
        pass
    try:
        if "," in s:
            return [float(x.strip()) for x in s.split(",")]
        else:
            return [float(x) for x in s.split()]
    except ValueError:
        error_exit(
            f"Cannot parse data: {s}",
            "Use Python list format like [1, 2, 3] or comma-separated numbers.",
        )


def _parse_bounds(s: str) -> tuple:
    """Parse bounds string like [-10,10] or [0,pi] into a tuple. Supports math constants."""
    try:
        data = ast.literal_eval(s)
    except (SyntaxError, ValueError):
        # Retry with math constants for expressions like [0,pi]
        safe_ns = {"pi": math.pi, "e": math.e, "inf": math.inf}
        try:
            data = eval(s, {"__builtins__": {}}, safe_ns)
        except Exception:
            error_exit(
                f"Invalid bounds: {s}", "Use format [lo,hi], e.g. [-10,10] or [0,pi]"
            )
    if isinstance(data, (list, tuple)) and len(data) == 2:
        return (float(data[0]), float(data[1]))
    error_exit(f"Invalid bounds: {s}", "Use format [lo,hi], e.g. [-10,10] or [0,pi]")


def _format_complex_array(arr) -> str:
    """Format a complex numpy array for readable output."""
    lines = []
    for i, val in enumerate(arr):
        re = val.real
        im = val.imag
        if abs(im) < 1e-10:
            lines.append(f"[{i}] {re:.6g}")
        elif abs(re) < 1e-10:
            lines.append(f"[{i}] {im:.6g}j")
        else:
            lines.append(f"[{i}] {re:.6g} + {im:.6g}j")
    return "\n".join(lines)


# ============================================================
# Expression Evaluators
# ============================================================


def _eval_numpy(expr: str) -> float:
    """Evaluate a math expression using numpy."""
    import numpy as np

    safe_ns = {
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "asin": np.arcsin,
        "acos": np.arccos,
        "atan": np.arctan,
        "sinh": np.sinh,
        "cosh": np.cosh,
        "tanh": np.tanh,
        "sqrt": np.sqrt,
        "cbrt": np.cbrt,
        "log": np.log,
        "log2": np.log2,
        "log10": np.log10,
        "exp": np.exp,
        "abs": np.abs,
        "floor": np.floor,
        "ceil": np.ceil,
        "round": np.round,
        "pi": np.pi,
        "e": np.e,
        "inf": np.inf,
        "nan": np.nan,
        "np": np,
    }
    try:
        result = eval(expr, {"__builtins__": {}}, safe_ns)
        return float(result)
    except Exception as e:
        error_exit(
            f"Expression evaluation failed: {e}",
            "Check expression syntax. Supported: sin, cos, tan, log, sqrt, exp, pi, e, etc.",
        )


def _eval_mpmath(expr: str, precision: int) -> str:
    """Evaluate a math expression using mpmath for arbitrary precision."""
    import mpmath

    mpmath.mp.dps = precision

    safe_ns = {
        "sin": mpmath.sin,
        "cos": mpmath.cos,
        "tan": mpmath.tan,
        "asin": mpmath.asin,
        "acos": mpmath.acos,
        "atan": mpmath.atan,
        "sinh": mpmath.sinh,
        "cosh": mpmath.cosh,
        "tanh": mpmath.tanh,
        "sqrt": mpmath.sqrt,
        "log": mpmath.log,
        "log2": mpmath.log2,
        "log10": mpmath.log10,
        "exp": mpmath.exp,
        "abs": abs,
        "floor": mpmath.floor,
        "ceil": mpmath.ceil,
        "pi": mpmath.pi,
        "e": mpmath.e,
        "factorial": mpmath.factorial,
        "gamma": mpmath.gamma,
        "zeta": mpmath.zeta,
        "binomial": mpmath.binomial,
        "mp": mpmath.mp,
    }
    try:
        result = eval(expr, {"__builtins__": {}}, safe_ns)
        return mpmath.nstr(result, precision)
    except Exception as e:
        error_exit(
            f"Expression evaluation failed: {e}",
            "Check expression syntax. mpmath supports: sin, cos, log, sqrt, factorial, gamma, zeta, etc.",
        )


# ============================================================
# Subcommand: eval
# ============================================================


def cmd_eval(args: argparse.Namespace) -> None:
    if args.precision is not None and args.precision > 0:
        result = _eval_mpmath(args.expression, args.precision)
        format_output(f"eval ({args.precision} digits)", str(result))
    else:
        result = _eval_numpy(args.expression)
        if result == int(result) and abs(result) < 1e15:
            format_output("eval", str(int(result)))
        else:
            format_output("eval", f"{result}")


# ============================================================
# Subcommand: matrix
# ============================================================


def cmd_matrix(args: argparse.Namespace) -> None:
    import numpy as np

    def parse_matrix(s: str) -> np.ndarray:
        data = safe_parse_literal(s)
        if not isinstance(data, (list, np.ndarray)):
            error_exit(
                "Matrix must be a list of lists", "Use format like [[1,2],[3,4]]"
            )
        arr = np.array(data, dtype=float)
        if arr.ndim != 2:
            error_exit("Matrix must be 2-dimensional", "Use format like [[1,2],[3,4]]")
        return arr

    A = parse_matrix(args.matrix)
    op = args.operation

    try:
        if op == "multiply":
            if args.matrix2 is None:
                error_exit("multiply requires --matrix2", "Provide a second matrix")
            B = parse_matrix(args.matrix2)
            if A.shape[1] != B.shape[0]:
                error_exit(
                    f"Shape mismatch: {A.shape} x {B.shape}",
                    "Matrix A columns must equal Matrix B rows",
                )
            result = A @ B
            format_output("matrix/multiply", str(result.tolist()))

        elif op == "inverse":
            if A.shape[0] != A.shape[1]:
                error_exit("Inverse requires a square matrix", f"Got shape {A.shape}")
            result = np.linalg.inv(A)
            format_output("matrix/inverse", str(result.tolist()))

        elif op == "det":
            if A.shape[0] != A.shape[1]:
                error_exit(
                    "Determinant requires a square matrix", f"Got shape {A.shape}"
                )
            result = np.linalg.det(A)
            if abs(result - round(result)) < 1e-9:
                format_output("matrix/det", str(int(round(result))))
            else:
                format_output("matrix/det", f"{result}")

        elif op == "eigen":
            if A.shape[0] != A.shape[1]:
                error_exit(
                    "Eigenvalue requires a square matrix", f"Got shape {A.shape}"
                )
            eigenvalues, eigenvectors = np.linalg.eig(A)
            lines = [
                "Eigenvalues:",
                str(eigenvalues.tolist()),
                "",
                "Eigenvectors:",
                str(eigenvectors.tolist()),
            ]
            format_output("matrix/eigen", "\n".join(lines))

        elif op == "transpose":
            result = A.T
            format_output("matrix/transpose", str(result.tolist()))

        elif op == "svd":
            U, S, Vt = np.linalg.svd(A)
            lines = [
                "U:",
                str(U.tolist()),
                "",
                "S:",
                str(S.tolist()),
                "",
                "Vt:",
                str(Vt.tolist()),
            ]
            format_output("matrix/svd", "\n".join(lines))

        elif op == "rank":
            result = np.linalg.matrix_rank(A)
            format_output("matrix/rank", str(result))

        elif op == "solve":
            if args.matrix2 is None:
                error_exit(
                    "solve requires --matrix2 (vector b)",
                    "Provide b as a list like [5,6]",
                )
            b_raw = safe_parse_literal(args.matrix2)
            b = np.array(b_raw, dtype=float).flatten()
            if A.shape[0] != b.shape[0]:
                error_exit(
                    f"Shape mismatch: A is {A.shape}, b has {b.shape[0]} elements",
                    "A rows must equal b length",
                )
            result = np.linalg.solve(A, b)
            format_output("matrix/solve", str(result.tolist()))

    except np.linalg.LinAlgError as e:
        error_exit(
            f"Linear algebra error: {e}", "Matrix may be singular or ill-conditioned"
        )


# ============================================================
# Subcommand: stats
# ============================================================


def cmd_stats(args: argparse.Namespace) -> None:
    import numpy as np

    op = args.operation

    try:
        if op in ("describe", "corr", "regression", "percentile"):
            data = np.array(parse_data_list(args.data))

        if op == "describe":
            std_val = np.std(data, ddof=1) if len(data) > 1 else float("nan")
            std_str = (
                f"{std_val:.4g}" if not np.isnan(std_val) else "N/A (need >1 value)"
            )
            lines = [
                f"count:    {len(data)}",
                f"mean:     {np.mean(data):.4g}",
                f"std:      {std_str}",
                f"min:      {np.min(data):.4g}",
                f"25%:      {np.percentile(data, 25):.4g}",
                f"50%:      {np.median(data):.4g}",
                f"75%:      {np.percentile(data, 75):.4g}",
                f"max:      {np.max(data):.4g}",
            ]
            format_output("stats/describe", "\n".join(lines))

        elif op == "corr":
            if args.data2 is None:
                error_exit("corr requires --data2", "Provide a second dataset")
            data2 = np.array(parse_data_list(args.data2))
            if len(data) != len(data2):
                error_exit(
                    "Datasets must have equal length",
                    f"Got {len(data)} vs {len(data2)}",
                )
            result = np.corrcoef(data, data2)[0, 1]
            format_output("stats/corr", f"{result:.6f}")

        elif op == "regression":
            if args.data2 is None:
                error_exit(
                    "regression requires --data2", "Provide a second dataset (y values)"
                )
            data2 = np.array(parse_data_list(args.data2))
            if len(data) != len(data2):
                error_exit(
                    "Datasets must have equal length",
                    f"Got {len(data)} vs {len(data2)}",
                )
            A_mat = np.vstack([data, np.ones(len(data))]).T
            m, b = np.linalg.lstsq(A_mat, data2, rcond=None)[0]
            r = np.corrcoef(data, data2)[0, 1]
            lines = [
                f"slope (m):     {m:.6g}",
                f"intercept (b): {b:.6g}",
                f"y = {m:.6g}x + {b:.6g}",
                f"R²:            {r**2:.6f}",
            ]
            format_output("stats/regression", "\n".join(lines))

        elif op == "percentile":
            if args.target is None:
                error_exit(
                    "percentile requires --target", "Provide a percentile value (0-100)"
                )
            result = np.percentile(data, args.target)
            format_output("stats/percentile", f"P{args.target} = {result:.6g}")

        elif op == "pdf":
            from scipy import stats as sp_stats

            if args.target is None:
                error_exit("pdf requires --target", "Provide a value to evaluate")
            dist_name = args.data.strip().lower()
            dist_map = {
                "normal": "norm",
                "gaussian": "norm",
                "uniform": "uniform",
                "exponential": "expon",
                "t": "t",
                "chi2": "chi2",
                "f": "f",
            }
            scipy_name = dist_map.get(dist_name, dist_name)
            try:
                dist = getattr(sp_stats, scipy_name)
            except AttributeError:
                error_exit(
                    f"Unknown distribution: {dist_name}",
                    f"Supported: {', '.join(sorted(set(dist_map.values())))}",
                )
            params = safe_parse_literal(args.params) if args.params else ()
            if not isinstance(params, (list, tuple)):
                params = (params,)
            result = dist.pdf(args.target, *params)
            params_str = f", params={args.params}" if args.params else ""
            format_output(
                "stats/pdf", f"{dist_name}({args.target}{params_str}) = {result:.6g}"
            )

        elif op == "cdf":
            from scipy import stats as sp_stats

            if args.target is None:
                error_exit("cdf requires --target", "Provide a value to evaluate")
            dist_name = args.data.strip().lower()
            dist_map = {
                "normal": "norm",
                "gaussian": "norm",
                "uniform": "uniform",
                "exponential": "expon",
                "t": "t",
                "chi2": "chi2",
                "f": "f",
            }
            scipy_name = dist_map.get(dist_name, dist_name)
            try:
                dist = getattr(sp_stats, scipy_name)
            except AttributeError:
                error_exit(
                    f"Unknown distribution: {dist_name}",
                    f"Supported: {', '.join(sorted(set(dist_map.values())))}",
                )
            params = safe_parse_literal(args.params) if args.params else ()
            if not isinstance(params, (list, tuple)):
                params = (params,)
            result = dist.cdf(args.target, *params)
            params_str = f", params={args.params}" if args.params else ""
            format_output(
                "stats/cdf", f"{dist_name}({args.target}{params_str}) = {result:.6g}"
            )

    except Exception as e:
        error_exit(f"Statistics error: {e}")


# ============================================================
# Subcommand: precision
# ============================================================


def cmd_precision(args: argparse.Namespace) -> None:
    try:
        result = _eval_mpmath(args.expression, args.precision)
        format_output(f"precision ({args.precision} digits)", str(result))
    except ImportError:
        error_exit("mpmath is not installed", "Install with: pip3 install mpmath")


# ============================================================
# Subcommand: optimize
# ============================================================


def cmd_optimize(args: argparse.Namespace) -> None:
    from scipy import optimize as sp_optimize

    bounds = _parse_bounds(args.bounds)
    expr_str = args.expr

    def f(x):
        ns = {
            "x": float(x),
            "pi": math.pi,
            "e": math.e,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "sqrt": math.sqrt,
            "log": math.log,
            "exp": math.exp,
            "abs": abs,
        }
        return eval(expr_str, {"__builtins__": {}}, ns)

    op = args.operation
    try:
        if op == "minimize":
            result = sp_optimize.minimize_scalar(f, bounds=bounds, method="bounded")
            format_output(
                "optimize/minimize", f"x = {result.x:.10g}\nf(x) = {result.fun:.10g}"
            )

        elif op == "maximize":

            def neg_f(x):
                return -f(x)

            result = sp_optimize.minimize_scalar(neg_f, bounds=bounds, method="bounded")
            format_output(
                "optimize/maximize", f"x = {result.x:.10g}\nf(x) = {f(result.x):.10g}"
            )

        elif op == "root":
            fa, fb = f(bounds[0]), f(bounds[1])
            if fa * fb > 0:
                error_exit(
                    "f(a) and f(b) must have opposite signs",
                    f"f({bounds[0]}) = {fa}, f({bounds[1]}) = {fb}",
                )
            result = sp_optimize.brentq(f, bounds[0], bounds[1])
            format_output("optimize/root", f"x = {result:.10g}\nf(x) = {f(result):.2e}")

    except ImportError:
        error_exit("scipy is not installed", "Install with: pip3 install scipy")
    except Exception as e:
        error_exit(f"Optimization error: {e}")


# ============================================================
# Subcommand: integrate
# ============================================================


def cmd_integrate(args: argparse.Namespace) -> None:
    from scipy import integrate as sp_integrate

    bounds = _parse_bounds(args.bounds)
    expr_str = args.expr

    def f(x):
        ns = {
            "x": float(x),
            "pi": math.pi,
            "e": math.e,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "sqrt": math.sqrt,
            "log": math.log,
            "exp": math.exp,
            "abs": abs,
        }
        return eval(expr_str, {"__builtins__": {}}, ns)

    op = args.operation
    try:
        if op == "definite":
            result, error = sp_integrate.quad(f, bounds[0], bounds[1])
            format_output(
                "integrate/definite",
                f"∫ f(x) dx from {bounds[0]} to {bounds[1]}\n= {result:.10g}\n(error ≈ {error:.2e})",
            )

        elif op == "ode":
            if args.initial is None:
                error_exit(
                    "ode requires --initial", "Provide initial value, e.g. --initial 1"
                )
            ode_expr = expr_str.strip()
            if "=" in ode_expr:
                ode_expr = ode_expr.split("=")[-1].strip()

            def ode_f(x, y):
                ns = {
                    "x": float(x),
                    "y": float(y[0]),
                    "pi": math.pi,
                    "e": math.e,
                    "sin": math.sin,
                    "cos": math.cos,
                    "tan": math.tan,
                    "sqrt": math.sqrt,
                    "log": math.log,
                    "exp": math.exp,
                    "abs": abs,
                }
                return [eval(ode_expr, {"__builtins__": {}}, ns)]

            x_span = (bounds[0], bounds[1])
            x_eval = [bounds[0] + (bounds[1] - bounds[0]) * i / 20 for i in range(21)]
            sol = sp_integrate.solve_ivp(ode_f, x_span, [args.initial], t_eval=x_eval)

            lines = [f"ODE: dy/dx = {ode_expr}, y({bounds[0]}) = {args.initial}", ""]
            lines.append(f"{'x':>12}  {'y':>12}")
            lines.append("-" * 28)
            for xi, yi in zip(sol.t, sol.y[0]):
                lines.append(f"{xi:>12.6g}  {yi:>12.6g}")
            format_output("integrate/ode", "\n".join(lines))

    except ImportError:
        error_exit("scipy is not installed", "Install with: pip3 install scipy")
    except Exception as e:
        error_exit(f"Integration error: {e}")


# ============================================================
# Subcommand: transform
# ============================================================


def cmd_transform(args: argparse.Namespace) -> None:
    import numpy as np

    op = args.operation

    try:
        if op in ("fft", "ifft"):
            data = np.array(parse_data_list(args.data), dtype=complex)
            if op == "fft":
                result = np.fft.fft(data)
                format_output("transform/fft", _format_complex_array(result))
            else:
                result = np.fft.ifft(data)
                format_output("transform/ifft", _format_complex_array(result))

        elif op == "convolve":
            if args.data2 is None:
                error_exit("convolve requires --data2", "Provide a second dataset")
            data1 = np.array(parse_data_list(args.data))
            data2 = np.array(parse_data_list(args.data2))
            result = np.convolve(data1, data2)
            format_output("transform/convolve", str(result.tolist()))

    except Exception as e:
        error_exit(f"Transform error: {e}")


# ============================================================
# Argument Parser
# ============================================================


def build_parser() -> argparse.ArgumentParser:
    """Build the main argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="calc.py",
        description="High-performance calculator for AI Agents",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- eval ---
    p_eval = subparsers.add_parser("eval", help="Evaluate a math expression")
    p_eval.add_argument("expression", help="Math expression to evaluate")
    p_eval.add_argument(
        "--precision", type=int, default=None, help="Precision in digits (uses mpmath)"
    )

    # --- matrix ---
    p_matrix = subparsers.add_parser("matrix", help="Matrix operations")
    p_matrix.add_argument(
        "operation",
        choices=[
            "multiply",
            "inverse",
            "det",
            "eigen",
            "transpose",
            "svd",
            "rank",
            "solve",
        ],
        help="Matrix operation to perform",
    )
    p_matrix.add_argument(
        "--matrix", required=True, help="Matrix A as Python literal, e.g. [[1,2],[3,4]]"
    )
    p_matrix.add_argument(
        "--matrix2", default=None, help="Matrix B (for multiply/solve)"
    )

    # --- stats ---
    p_stats = subparsers.add_parser("stats", help="Statistical analysis")
    p_stats.add_argument(
        "operation",
        choices=["describe", "corr", "regression", "percentile", "pdf", "cdf"],
        help="Statistical operation",
    )
    p_stats.add_argument(
        "--data", required=True, help="Data as Python list or comma-separated"
    )
    p_stats.add_argument(
        "--data2", default=None, help="Second dataset (for corr, regression)"
    )
    p_stats.add_argument(
        "--target",
        type=float,
        default=None,
        help="Target value (for percentile, pdf, cdf)",
    )
    p_stats.add_argument(
        "--params",
        default=None,
        help="Distribution parameters as Python list, e.g. '[5]' for chi2(df=5) or '[3,10]' for f(d1=3,d2=10)",
    )

    # --- precision ---
    p_prec = subparsers.add_parser("precision", help="Arbitrary precision computation")
    p_prec.add_argument("expression", help="Math expression (mpmath)")
    p_prec.add_argument(
        "--precision", type=int, default=50, help="Precision in digits (default: 50)"
    )

    # --- optimize ---
    p_opt = subparsers.add_parser("optimize", help="Numerical optimization")
    p_opt.add_argument("operation", choices=["minimize", "root", "maximize"])
    p_opt.add_argument(
        "--expr", required=True, help="Expression in variable x, e.g. x**2 + 2*x + 1"
    )
    p_opt.add_argument(
        "--bounds", required=True, help="Bounds as [lo,hi], e.g. [-10,10]"
    )
    p_opt.add_argument(
        "--precision", type=int, default=None, help="Precision in digits"
    )

    # --- integrate ---
    p_int = subparsers.add_parser("integrate", help="Numerical integration")
    p_int.add_argument("operation", choices=["definite", "ode"])
    p_int.add_argument("--expr", required=True, help="Expression or ODE definition")
    p_int.add_argument("--bounds", required=True, help="Integration bounds as [lo,hi]")
    p_int.add_argument(
        "--initial", type=float, default=None, help="Initial value (for ODE)"
    )
    p_int.add_argument(
        "--precision", type=int, default=None, help="Precision in digits"
    )

    # --- transform ---
    p_trans = subparsers.add_parser("transform", help="Signal processing")
    p_trans.add_argument("operation", choices=["fft", "ifft", "convolve"])
    p_trans.add_argument("--data", required=True, help="Data as Python list")
    p_trans.add_argument("--data2", default=None, help="Second data (for convolve)")

    return parser


# ============================================================
# Main
# ============================================================


def main():
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        "eval": cmd_eval,
        "matrix": cmd_matrix,
        "stats": cmd_stats,
        "precision": cmd_precision,
        "optimize": cmd_optimize,
        "integrate": cmd_integrate,
        "transform": cmd_transform,
    }

    handler = dispatch.get(args.command)
    if handler:
        handler(args)
    else:
        error_exit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
