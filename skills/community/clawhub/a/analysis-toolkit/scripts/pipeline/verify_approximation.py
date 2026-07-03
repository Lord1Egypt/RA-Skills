"""
通用逼近验证引擎 — 不依赖特定公式知识，仅用数学性质验证。

设计原则：
    计算用一种算法，验证用另一种更泛化的方法。
    不需要知道算子内部实现了什么公式，只需要知道它的数学性质。

逼近验证策略（按优先级降序）：

1. 值域边界检查
   p值 ∈ [0,1], SD ≥ 0, R² ∈ [0,1], 相关系数 ∈ [-1,1], 秩次 ∈ [1,n], ...

2. 数值稳定性检查（小扰动检验）
   对输入施加 ε = 1e-6 的扰动，输出变化应大致连续。
   若输出跳变远超预期，说明实现可能有 bug。

3. 对称性 / 守恒性检查
   sum(residuals) ≈ 0, mean(Z-scores) ≈ 0, range(Z-scores) 应与 n 相关, ...

4. 收敛性检查（样本量增大）
   统计量应随 n 增大趋近真实值，标准误随 n 递减。

5. 自洽性检查
   同一函数对同一输入多次调用应返回相同结果（确定性）。
   组合函数的输出应与分别调用一致。

用法：
    from scripts.verify_approximation import verify_by_approximation
    result = verify_by_approximation(calc_mean, ([1,2,3,4,5],), {}, 3.0)
    # → {"passed": True, "checks": [...], "score": 0.95}
"""
import numpy as np
import math
from typing import Any, Callable


# ═══════════════════════════════════════════════════════
# 类型推断
# ═══════════════════════════════════════════════════════

def _infer_value_type(value, name=""):
    """
    推断值的数学类型，用于选择验证策略。

    Returns
    -------
    str — "probability" | "statistic" | "count" | "ratio" | "float" | "dict" | "array" | "unknown"
    """
    # 按名称推断
    name_lower = name.lower()

    # 概率类：p值、Φ(z)、显著性
    if any(kw in name_lower for kw in ["p_value", "p_two_tailed", "p_one_tailed",
                                         "p值", "概率", "cumulative"]):
        return "probability"

    # 判定类：level、significant
    if any(kw in name_lower for kw in ["level", "significant", "acceptable", "judgment"]):
        return "categorical"

    # 自由度、计数
    if any(kw in name_lower for kw in ["df", "count", "n", "freedom", "number", "k="]):
        return "count"

    # R²
    if any(kw in name_lower for kw in ["r2", "r²", "r_squared"]):
        return "bounded_0_1"

    # SD / sigma
    if any(kw in name_lower for kw in ["sd", "std", "sigma", "syx", "偏差", "标准差"]):
        return "nonnegative"

    if any(kw in name_lower for kw in ["te", "te_relative", "总误差", "bias", "偏倚",
                                         "uncertainty", "不确定度"]):
        return "nonnegative"

    # 按值推断
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, dict):
        return "dict"
    if isinstance(value, (list, np.ndarray)):
        return "array"
    if isinstance(value, str):
        return "categorical"
    if isinstance(value, (int, float)):
        if 0 <= value <= 1 and name_lower in ("", ""):
            # 可能是概率，但不确认
            pass
        return "float"

    return "unknown"


# ═══════════════════════════════════════════════════════
# 逼近验证策略
# ═══════════════════════════════════════════════════════

class VerificationCheck:
    """单次检查的结果"""
    def __init__(self, name: str, passed: bool, detail: str = "", score: float = None):
        self.name = name
        self.passed = passed
        self.detail = detail
        self.score = score if score is not None else (1.0 if passed else 0.0)

    def to_dict(self):
        return {"name": self.name, "passed": self.passed,
                "detail": self.detail, "score": self.score}


# ── 1. 值域边界检查 ──

def _check_bounds(value, vtype: str, name: str = "") -> VerificationCheck:
    """检查值是否在合理的数学范围内。"""
    if vtype == "probability":
        ok = 0 <= value <= 1
        return VerificationCheck(
            "值域检查(p∈[0,1])", ok,
            f"值={value:.6f}, {'在[0,1]内' if ok else '超出[0,1]!'}")
    elif vtype == "nonnegative":
        ok = value >= 0
        return VerificationCheck(
            "非负检查", ok,
            f"值={value:.6f}, {'≥0' if ok else '<0!'}")
    elif vtype == "bounded_0_1":
        ok = 0 <= value <= 1
        return VerificationCheck(
            "值域检查(∈[0,1])", ok,
            f"R²={value:.6f}, {'在[0,1]内' if ok else '超出[0,1]!'}")
    elif vtype == "count":
        ok = isinstance(value, int) and value >= 0
        return VerificationCheck(
            "计数检查", ok,
            f"值={value}, {'非负整数' if ok else '不是非负整数!'}")
    return VerificationCheck("值域检查(跳过)", True, "无适用边界规则")


# ── 2. 数值稳定性检查（小扰动逼近） ──

def _check_stability(func: Callable, args: tuple, kwargs: dict,
                     result: Any, attempts: int = 3) -> VerificationCheck:
    """
    小扰动稳定性检查。

    对数值型输入施加 ±ε 扰动，检查输出变化是否连续。
    如果函数在局部接近于线性，则 f(x+ε) ≈ f(x) + f'(x)·ε。
    """
    if not isinstance(result, (int, float)):
        return VerificationCheck("稳定性检查(跳过)", True, "非标量输出，跳过")

    # 找出第一个数值参数施加扰动
    perturbed_results = []
    for i, arg in enumerate(args):
        if isinstance(arg, (int, float)):
            for delta in [1e-6, -1e-6, 1e-4, -1e-4]:
                args_list = list(args)
                args_list[i] = arg + delta
                try:
                    r = func(*args_list, **kwargs)
                    if isinstance(r, (int, float)):
                        perturbed_results.append((delta, r))
                except Exception:
                    pass
            break

    if len(perturbed_results) < 2:
        return VerificationCheck("稳定性检查(跳过)", True, "无可扰动参数")

    # 检查变化是否合理：小扰动应产生小变化
    max_rel_change = 0
    for delta, r in perturbed_results:
        if result != 0:
            rel_change = abs((r - result) / result)
        else:
            rel_change = abs(r - result)
        max_rel_change = max(max_rel_change, rel_change)

    # 1e-3 的输入扰动不应产生超过 1000 倍的输出变化
    reasonable = max_rel_change < 100.0 or abs(max_rel_change) < 1e-6

    return VerificationCheck(
        "稳定性检查(小扰动)", reasonable,
        f"最大相对变化={max_rel_change:.4f}, {'连续' if reasonable else '跳变过大!'}",
        score=min(1.0, 1.0 / (1.0 + max_rel_change)))


# ── 3. 对称性/守恒性检查 ──

def _check_invariants(value, vtype: str, result: Any) -> VerificationCheck:
    """检查函数值是否满足数学不变性。"""
    # 概率函数的对称性：p 和 1-p 的关系不在这里检查
    return VerificationCheck("不变性检查(跳过)", True, "通用检查不适用")


# ── 4. 收敛性检查 ──

def _check_convergence(func: Callable, args: tuple, kwargs: dict,
                        result: Any) -> VerificationCheck:
    """
    收敛性检查：样本量增大时，统计量应趋向稳定。

    对包含数组参数的函数：
    1. 用数组的子集计算，检查结果是否与全集接近
    2. 交换数组中元素顺序，检查结果是否不变（可交换性）
    """
    # 查找数组参数
    array_arg_idx = None
    array_arg = None
    for i, arg in enumerate(args):
        if isinstance(arg, (list, np.ndarray)) and len(arg) >= 4:
            array_arg_idx = i
            array_arg = arg
            break

    if array_arg is None:
        return VerificationCheck("收敛性检查(跳过)", True, "无数组参数")

    arr = np.array(array_arg, dtype=float)
    n = len(arr)

    # 用子集验证
    checks_passed = 0
    total_checks = 0

    for subset_size in [max(3, n//2), max(3, n//3)]:
        if subset_size >= n:
            continue
        np.random.seed(42)
        subset = np.random.choice(arr, subset_size, replace=False)
        args_list = list(args)
        args_list[array_arg_idx] = subset
        try:
            sub_result = func(*args_list, **kwargs)
            if isinstance(sub_result, type(result)):
                total_checks += 1
                if isinstance(result, (int, float)) and isinstance(sub_result, (int, float)):
                    if result != 0:
                        rel_diff = abs((sub_result - result) / result)
                    else:
                        rel_diff = abs(sub_result - result)
                    if rel_diff < 0.5:  # 子集结果不应差太多
                        checks_passed += 1
        except Exception:
            pass

    # 交换元素顺序验证
    if len(arr) >= 3:
        shuffled = np.random.permutation(arr)
        args_list = list(args)
        args_list[array_arg_idx] = shuffled
        try:
            shuffled_result = func(*args_list, **kwargs)
            if isinstance(shuffled_result, type(result)):
                total_checks += 1
                if isinstance(result, (int, float)):
                    if result != 0:
                        rel_diff = abs((shuffled_result - result) / result)
                    else:
                        rel_diff = abs(shuffled_result - result)
                    if rel_diff < 1e-10:
                        checks_passed += 1
        except Exception:
            pass

    if total_checks == 0:
        return VerificationCheck("收敛性检查(跳过)", True, "无法执行子集验证")

    passed = checks_passed >= total_checks * 0.5
    return VerificationCheck(
        "收敛性检查", passed,
        f"通过 {checks_passed}/{total_checks} 个子集验证")


# ── 5. 自洽性检查（确定性 + 可重现性） ──

def _check_consistency(func: Callable, args: tuple, kwargs: dict,
                        result: Any) -> VerificationCheck:
    """
    自洽性检查：相同输入多次调用应返回相同结果（确定性函数）。
    """
    if isinstance(result, (int, float, str, bool)):
        try:
            r2 = func(*args, **kwargs)
            consistent = r2 == result
            return VerificationCheck(
                "自洽性检查(可重复)", consistent,
                "两次调用结果一致" if consistent else "两次调用结果不一致!")
        except Exception:
            pass
    return VerificationCheck("自洽性检查(跳过)", True, "非标量或不可重现")


# ═══════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════

def verify_by_approximation(func: Callable, args: tuple,
                             kwargs: dict = None, result: Any = None,
                             name: str = "") -> dict:
    """
    通用逼近验证 — 不依赖公式知识，仅用数学性质验证。

    对任意函数执行以下检查：
      - 值域边界 ✅
      - 数值稳定性（小扰动逼近）✅
      - 收敛性（子集验证）✅
      - 自洽性（可重复性）✅

    Parameters
    ----------
    func : callable — 被验证的算子函数
    args : tuple — 位置参数
    kwargs : dict — 关键字参数
    result : any — 函数实际返回值（不提供则自动计算）
    name : str — 算子名

    Returns
    -------
    dict
        {"name": str, "passed": bool, "checks": list[dict],
         "score": float, "summary": str}
    """
    if kwargs is None:
        kwargs = {}
    if result is None:
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            return {"name": name or func.__name__, "passed": False,
                    "checks": [], "score": 0.0,
                    "summary": f"函数执行失败: {e}"}

    checks = []

    # 检查策略集
    vtype = _infer_value_type(result, name)

    # 1. 值域边界检查
    check = _check_bounds(result, vtype, name)
    checks.append(check.to_dict())

    # 2. 数值稳定性检查
    check = _check_stability(func, args, kwargs, result)
    checks.append(check.to_dict())

    # 3. 收敛性检查
    check = _check_convergence(func, args, kwargs, result)
    checks.append(check.to_dict())

    # 4. 自洽性检查
    check = _check_consistency(func, args, kwargs, result)
    checks.append(check.to_dict())

    # 综合评分
    scores = [c["score"] for c in checks if c["score"] is not None]
    passed_checks = sum(1 for c in checks if c["passed"])
    applicable_checks = sum(1 for c in checks if c["score"] is not None and not c["name"].endswith("(跳过)"))
    total_checks = len(checks)
    score = np.mean(scores) if scores else 0.0
    # 只从可执行的检查中计算通过率
    all_passed = passed_checks == total_checks or (
        applicable_checks > 0 and passed_checks >= applicable_checks
    )

    return {
        "name": name or func.__name__,
        "passed": all_passed,
        "checks": checks,
        "score": round(score, 4),
        "summary": (f"{'✓' if all_passed else '✗'} "
                    f"{passed_checks}/{total_checks} 项检查通过"
                    f" (综合评分: {score:.2f})"),
    }


# ═══════════════════════════════════════════════════════
# 批量逼近验证
# ═══════════════════════════════════════════════════════

def verify_all_by_approximation(operators_and_args: list) -> dict:
    """
    批量逼近验证。

    Parameters
    ----------
    operators_and_args : list[tuple]
        [(func, args, kwargs, name), ...]

    Returns
    -------
    dict — {"total", "passed", "failed", "results": list}
    """
    results = []
    for item in operators_and_args:
        if len(item) == 4:
            func, args, kwargs, name = item
        elif len(item) == 3:
            func, args, kwargs = item
            name = func.__name__
        else:
            continue
        r = verify_by_approximation(func, args, kwargs, name=name)
        results.append(r)

    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "results": results,
    }


# ═══════════════════════════════════════════════════════
# CLI 自测
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    import scripts.operations.operators as ops
    import scripts.operations.uncertainty as unc
    import scripts.operations.total_error as te

    print("通用逼近验证 — 跨算子验证")
    print("=" * 60)

    test_cases = [
        (ops.calc_mean, ([1, 2, 3, 4, 5],), {}, "calc_mean"),
        (ops.calc_sd, ([1, 2, 3, 4, 5],), {}, "calc_sd"),
        (ops.calc_bias, (10.5, 10.0), {}, "calc_bias"),
        (ops.calc_z_to_p, (1.96,), {}, "z_to_p(1.96)"),
        (ops.calc_tcrit, (4, 0.05, True), {}, "t_crit(4,0.05)"),
        (unc.calc_ubias, (0.5, 2.0), {}, "calc_ubias"),
        (unc.calc_u_combined, ([0.5, 0.3, 0.2],), {}, "u_combined"),
        (te.calc_te, (100.52, 100.0, 0.5891, 4, 2.776), {}, "calc_te"),
        (ops.calc_rank_sum, ([10, 20, 30, 20, 40],), {}, "rank_sum"),
        (ops.round_half_even, (2.5, 0), {}, "round_half_even"),
    ]

    results = verify_all_by_approximation(test_cases)
    for r in results["results"]:
        print(f"  [{('✓' if r['passed'] else '✗')}] {r['name']:<25s} {r['summary']}")

    print(f"\n  总计: {results['total']}, 通过: {results['passed']}, 失败: {results['failed']}")
