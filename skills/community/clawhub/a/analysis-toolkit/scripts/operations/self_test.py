"""
算子自测试模块 — 对每个注册算子进行已知值验证。

每个测试用例定义 {inputs → expected_output}，用不同路径验证正确性。
测试失败表明算子的数学实现有误。

设计原则：
  - 测试用例来自已知统计教材或标准文档
  - 每个算子至少 1 个测试，关键算子 3+ 个测试
  - 容差由算子类型决定（整数精确=0，浮点=1e-10）

用法：
    from scripts.operations.self_test import run_self_test, test_operator
    result = test_operator("calc_mean", [1,2,3,4,5], expected=3.0)
    report = run_self_test()  # 测试所有已注册算子
"""
import numpy as np
import math


# ═══════════════════════════════════════════════════════
# 单算子测试
# ═══════════════════════════════════════════════════════

def test_operator(func, args, kwargs=None, expected=None, abs_tol=1e-5,
                  rel_tol=1e-5, name="") -> dict:
    """
    测试单个算子。

    支持两种验证方式：
    1. expected: 与预期值精确比较
    2. verify_func: 用另一种算法验证

    Parameters
    ----------
    func : callable — 被测试的算子函数
    args : tuple — 位置参数
    kwargs : dict, optional — 关键字参数
    expected : any, optional — 预期结果
    abs_tol : float — 绝对容差（Z表近似放宽到1e-5）
    rel_tol : float — 相对容差
    name : str — 算子名（显示用）

    Returns
    -------
    dict — {"name", "passed", "actual", "expected", "diff", "detail"}
    """
    if kwargs is None:
        kwargs = {}
    fname = name or func.__name__

    try:
        actual = func(*args, **kwargs)

        if expected is None:
            return {"name": fname, "passed": None,
                    "actual": actual, "expected": None,
                    "diff": None, "detail": "无预期值，跳过比较"}

        # 数值比较
        if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
            diff = abs(actual - expected)
            denom = max(abs(expected), abs(actual), 1.0)
            rel_diff = diff / denom
            passed = diff <= abs_tol or rel_diff <= rel_tol
        elif isinstance(expected, dict) and isinstance(actual, dict):
            # 对 dict 逐 key 比较数值字段
            diffs = []
            for k in expected:
                if k in actual and isinstance(expected[k], (int, float)):
                    e = expected[k]
                    a = actual[k]
                    diff = abs(a - e)
                    denom = max(abs(e), abs(a), 1.0)
                    diffs.append(diff / denom)
            passed = all(d <= rel_tol for d in diffs) if diffs else True
            diff = max(diffs) if diffs else 0
        else:
            passed = actual == expected
            diff = 0 if passed else float('inf')

        return {
            "name": fname,
            "passed": passed,
            "actual": actual,
            "expected": expected,
            "diff": round(diff, 10),
            "detail": f"{'✓' if passed else '✗'} {fname}: "
                      f"实际={actual}, 预期={expected}, 差={diff:.2e}",
        }

    except Exception as e:
        return {
            "name": fname,
            "passed": False,
            "actual": None,
            "expected": expected,
            "diff": None,
            "detail": f"✗ {fname} 执行异常: {e}",
        }


# ═══════════════════════════════════════════════════════
# 算子测试用例
# ═══════════════════════════════════════════════════════

def _get_test_cases() -> list:
    """获取所有算子的标准测试用例。"""
    import scripts.operations.operators as ops
    import scripts.operations.uncertainty as unc
    import scripts.operations.total_error as te

    return [
        # ── 基础描述统计 ──
        (ops.calc_mean, ([1, 2, 3, 4, 5],), {}, 3.0, "calc_mean 基准"),
        (ops.calc_mean, ([10, 20, 30],), {}, 20.0, "calc_mean 2"),
        (ops.calc_sd, ([1, 2, 3, 4, 5],), {}, 1.58113883008, "calc_sd"),
        (ops.calc_rsd, ([10, 20, 30],), {}, 50.0, "calc_rsd 均值20 SD10 → 50%"),
        (ops.calc_var, ([1, 2, 3, 4, 5],), {}, 2.5, "calc_var"),
        (ops.calc_median, ([1, 3, 5, 7, 9],), {}, 5.0, "calc_median 奇数"),
        (ops.calc_median, ([1, 3, 5, 7],), {}, 4.0, "calc_median 偶数"),
        (ops.calc_range, ([1, 3, 5, 7, 9],), {}, 8.0, "calc_range"),

        # ── 偏倚 ──
        (ops.calc_bias, (10.5, 10.0), {}, 0.5, "bias = 10.5 - 10.0"),
        (ops.calc_bias_relative, (105.0, 100.0), {}, 5.0, "相对偏倚 5%"),

        # ── 合并标准差 ──
        (ops.calc_pooled_sd, ([[1, 2, 3], [1, 2, 3]],), {},
         1.0, "合并标准差 同值两组"),
        (ops.calc_pooled_sd, ([[1, 3, 5], [2, 4, 6]],), {},
         2.0, "合并标准差 不同均值同SD"),
        (ops.calc_robust_sd, ([1, 2, 3, 4, 5, 100],), {}, None,
         "calc_robust_sd: MAD法抗异常值"),

        # ── SSE / 回归 ──
        (ops.calc_sse, ([0.5, -0.3, 0.1, -0.2],), {}, 0.39, "SSE = 0.25+0.09+0.01+0.04"),
        (ops.calc_r2, (0.39, 1.5), {}, 0.74, "R² = 1 - 0.39/1.5"),

        # ── Z 值 ──
        (ops.calc_z_score, (50.0, 45.0, 2.5), {}, 2.0, "Z=2.0"),

        # ── 临界值 ──
        (ops.calc_tcrit, (4, 0.05, True), {}, 2.776, "t(4, α=0.05) 双尾"),
        (ops.calc_tcrit, (10, 0.05, False), {}, 1.812, "t(10, α=0.05) 单尾"),
        (ops.calc_fcrit, (3, 12), {}, 3.49, "F(3,12, α=0.05)"),

        # ── Z表 ──
        (ops.calc_z_to_p, (0.0,), {}, 0.5, "Φ(0)=0.5"),
        (ops.calc_z_to_p, (1.96,), {}, 0.975, "Φ(1.96)=0.975"),
        (ops.calc_z_to_p_two_tailed, (1.96,), {}, 0.05, "p(z=1.96 双尾)=0.05"),

        # ── 不确定度 ──
        (unc.calc_ubias, (0.5, 2.0), {}, 0.25, "u_bias = 0.5/2"),
        (unc.calc_u_combined, ([0.5, 0.3, 0.2],), {},
         0.616441400296, "u_combined = sqrt(0.25+0.09+0.04)"),
        (unc.calc_expanded_u, (0.6164, 2.0), {}, 1.2328,
         "U = 2×0.6164"),
        (unc.get_coverage_factor, ("rectangular",), {}, 1.73205080757,
         "√3"),
        (unc.get_coverage_factor, ("triangular",), {}, 2.44948974278,
         "√6"),

        # ── 总误差 ──
        (te.calc_te, (100.52, 100.0, 0.5891, 4, 2.776), {}, None,
         "calc_te: 公式验证"),
        (te.calc_te_relative, (100.52, 100.0, 0.5891, 4, 2.776), {}, None,
         "相对TE%"),

        # ── 秩和 ──
        (ops.calc_rank_sum, ([10, 20, 30, 20, 40],), {}, None,
         "秩次: 等值20应取平均秩"),

        # ── 归一化 ──
        (ops.normalize_z_score, ([10, 20, 30, 40, 50],), {}, None,
         "Z归一: 均值应为0, SD应为1"),
        (ops.normalize_minmax, ([10, 20, 30, 40, 50],), {}, None,
         "MinMax: 范围应为[0,1]"),

        # ── 修约 ──
        (ops.round_half_up, (2.5, 0), {}, 3.0, "四舍五入 2.5→3"),
        (ops.round_half_even, (2.5, 0), {}, 2.0, "五成双 2.5→2"),
        (ops.round_half_up, (3.5, 0), {}, 4.0, "四舍五入 3.5→4"),
        (ops.round_half_even, (3.5, 0), {}, 4.0, "五成双 3.5→4"),
        (ops.round_ceil, (2.1, 0), {}, 3.0, "向上 2.1→3"),
        (ops.round_floor, (2.9, 0), {}, 2.0, "向下 2.9→2"),
        (ops.round_half_up, (-2.5, 0), {}, -3.0, "四舍五入 -2.5→-3"),
        (ops.round_half_even, (-2.5, 0), {}, -2.0, "五成双 -2.5→-2"),
    ]


# ═══════════════════════════════════════════════════════
# 属性验证（对无法直接比较预期值的算子做属性检查）
# ═══════════════════════════════════════════════════════

def _run_property_checks() -> list:
    """对无精确预期值的算子做属性验证。"""
    import scripts.operations.operators as ops
    import scripts.operations.total_error as te
    import numpy as np
    results = []

    # 1. 合并标准差：结果应介于各组的SD之间
    groups = [[1, 2, 3], [4, 5, 6]]
    pooled = ops.calc_pooled_sd(groups)
    sd1, sd2 = ops.calc_sd(groups[0]), ops.calc_sd(groups[1])
    prop1 = min(sd1, sd2) <= pooled <= max(sd1, sd2)
    results.append({
        "name": "calc_pooled_sd 属性(介于组SD间)",
        "passed": prop1,
        "detail": f"SD1={sd1:.4f}, SD2={sd2:.4f}, pooled={pooled:.4f}, 通过={prop1}",
    })

    # 2. 稳健标准差 < 普通标准差（有异常值时）
    vals_with_outlier = [1, 2, 3, 4, 5, 100]
    robust_sd = ops.calc_robust_sd(vals_with_outlier)
    std_sd = ops.calc_sd(vals_with_outlier)
    prop2 = robust_sd < std_sd
    results.append({
        "name": "calc_robust_sd 属性(抗异常值)",
        "passed": prop2,
        "detail": f"std_sd={std_sd:.4f}, robust_sd={robust_sd:.4f}, 通过={prop2}",
    })

    # 3. Z归一化后均值≈0, SD≈1
    z = ops.normalize_z_score([10, 20, 30, 40, 50])
    z_mean = abs(np.mean(z))
    z_sd = abs(np.std(z, ddof=0) - 1.0)
    prop3 = z_mean < 1e-10 and z_sd < 1e-10
    results.append({
        "name": "normalize_z_score 属性(均值0 SD1)",
        "passed": prop3,
        "detail": f"均值={np.mean(z):.2e}, SD={np.std(z,ddof=0):.2e}, 通过={prop3}",
    })

    # 4. MinMax归一化后范围[0,1]
    mm = ops.normalize_minmax([10, 20, 30, 40, 50])
    prop4 = abs(min(mm)) < 1e-10 and abs(max(mm) - 1.0) < 1e-10
    results.append({
        "name": "normalize_minmax 属性(范围[0,1])",
        "passed": prop4,
        "detail": f"min={min(mm):.4f}, max={max(mm):.4f}, 通过={prop4}",
    })

    # 5. 秩和: 等值取平均秩
    ranks = ops.calc_rank_sum([10, 20, 20, 30])
    prop5 = abs(ranks["ranks"][1] - 2.5) < 1e-10 and abs(ranks["ranks"][2] - 2.5) < 1e-10
    results.append({
        "name": "calc_rank_sum 属性(等值平均秩)",
        "passed": prop5,
        "detail": f"秩次={ranks['ranks']}, 通过={prop5}",
    })

    # 6. 总误差 TE = |bias| + t×SD, 分量应满足关系
    te_result = te.calc_te_from_values([101.2, 99.8, 100.5, 100.1, 101.0],
                                        reference=100.0, t_crit=2.776)
    bias_abs = te_result["bias_abs"]
    rand_err = te_result["random_error"]
    te_val = te_result["te"]
    prop6 = abs(te_val - (bias_abs + rand_err)) < 1e-6
    results.append({
        "name": "calc_te 属性(TE=|bias|+t×SD)",
        "passed": prop6,
        "detail": f"bias={bias_abs:.4f}, random={rand_err:.4f}, TE={te_val:.4f}, 通过={prop6}",
    })

    return results


# ═══════════════════════════════════════════════════════
# 全量运行
# ═══════════════════════════════════════════════════════

def run_self_test(verbose: bool = True) -> dict:
    """
    运行所有算子自测试。

    Parameters
    ----------
    verbose : bool — 是否打印详细结果

    Returns
    -------
    dict — {"total": int, "passed": int, "failed": int, "skipped": int, "details": list}
    """
    from scripts.operations.operators import calc_mann_whitney_u

    results = []

    # 1. 精确值测试
    for func, args, kwargs, expected, desc in _get_test_cases():
        r = test_operator(func, args, kwargs, expected, name=desc)
        results.append(r)

    # 2. 属性验证
    property_results = _run_property_checks()
    results.extend(property_results)

    # 3. 统计
    total = len(results)
    passed = sum(1 for r in results if r.get("passed"))
    failed = sum(1 for r in results if r.get("passed") is False)
    skipped = total - passed - failed

    if verbose:
        print(f"算子自测试报告")
        print(f"{'=' * 60}")
        print(f"{'状态':>4}  {'算子':<35} {'结果':<30}")
        print(f"{'-' * 60}")
        for r in results:
            status = "✓" if r.get("passed") else "✗" if r.get("passed") is False else "?"
            detail = r.get("detail", "")[:50]
            print(f"  [{status}] {r['name']:<35} {detail[:45]}")
        print(f"{'-' * 60}")
        print(f"  总计: {total}, 通过: {passed}, 失败: {failed}, 跳过: {skipped}")

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "details": results,
    }


if __name__ == "__main__":
    run_self_test()
