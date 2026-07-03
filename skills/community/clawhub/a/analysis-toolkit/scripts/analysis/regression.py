"""
回归分析模块

通用功能：线性回归、多项式回归、回归统计量计算。
"""
import numpy as np
import matplotlib.pyplot as plt


def linear_regression(x, y, force_zero=False):
    """
    一元线性回归。
    
    Parameters
    ----------
    x : array-like
        自变量
    y : array-like
        因变量
    force_zero : bool
        是否强制过原点
        
    Returns
    -------
    dict
        {"slope", "intercept", "r2", "syx", "r", "n", "equation"}
    """
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    n = len(x)

    if n < 2:
        raise ValueError(f"数据点不足 (n={n})，线性回归至少需要2个数据点")

    if np.any(np.isnan(x)) or np.any(np.isnan(y)):
        raise ValueError("输入数据包含 NaN，请先清理数据")

    try:
        if force_zero:
            slope = np.sum(x * y) / np.sum(x ** 2)
            intercept = 0.0
            y_pred = slope * x
        else:
            x_mean, y_mean = np.mean(x), np.mean(y)
            slope = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
            intercept = y_mean - slope * x_mean
            y_pred = slope * x + intercept
    except (ZeroDivisionError, FloatingPointError) as e:
        raise ValueError(f"回归计算失败: {e}")
    
    # 统计量
    residuals = y - y_pred
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 0
    r = np.sign(slope) * np.sqrt(abs(r2)) if n > 1 else 0
    syx = np.sqrt(ss_res / (n - (1 if force_zero else 2))) if n > (1 if force_zero else 2) else 0
    
    return {
        "slope": slope,
        "intercept": intercept,
        "r2": r2,
        "r": r,
        "syx": syx,
        "n": n,
        "equation": f"y = {slope:.6f}x {'+ ' if intercept >= 0 else '- '}{abs(intercept):.6f}" if not force_zero else f"y = {slope:.6f}x",
        "y_pred": y_pred,
        "residuals": residuals,
    }


def polynomial_regression(x, y, degree=4):
    """
    多项式回归拟合。
    
    Parameters
    ----------
    x : array-like
    y : array-like
    degree : int
        多项式次数
    
    Returns
    -------
    dict
        {"coefficients", "r2", "equation", "y_pred", "residuals"}
    """
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    n = len(x)
    if n <= degree:
        raise ValueError(f"数据点 (n={n}) 不足，多项式拟合(n={degree})至少需要 {degree+1} 个点")

    try:
        coeffs = np.polyfit(x, y, degree)
        y_pred = np.polyval(coeffs, x)
    except np.linalg.LinAlgError as e:
        raise ValueError(f"多项式拟合失败: {e}")
    
    residuals = y - y_pred
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 0
    
    # 生成方程字符串
    terms = []
    for i, c in enumerate(coeffs):
        power = degree - i
        if power == 0:
            terms.append(f"{c:.6f}")
        elif power == 1:
            terms.append(f"{c:.6f}x")
        else:
            terms.append(f"{c:.6f}x^{power}")
    
    return {
        "coefficients": coeffs,
        "r2": r2,
        "equation": "y = " + " + ".join(terms),
        "y_pred": y_pred,
        "residuals": residuals,
    }


def regression_stats(x, y, model_result):
    """
    回归统计检验。
    
    Parameters
    ----------
    x : array-like
    y : array-like
    model_result : dict
        linear_regression 或 polynomial_regression 的结果
    
    Returns
    -------
    dict
        {"r2", "syx", "f_value", "p_value_proxy"}
    """
    n = len(x)
    k = len(model_result.get("coefficients", [2])) - 1  # 自由度参数
    
    residuals = model_result["residuals"]
    y_mean = np.mean(y)
    
    ss_res = np.sum(residuals ** 2)
    ss_reg = np.sum((model_result["y_pred"] - y_mean) ** 2)
    ss_tot = ss_res + ss_reg
    
    df_res = n - k - 1
    df_reg = k
    
    ms_res = ss_res / df_res if df_res > 0 else 0
    ms_reg = ss_reg / df_reg if df_reg > 0 else 0
    
    f_value = ms_reg / ms_res if ms_res > 0 else 0
    
    return {
        "r2": model_result["r2"],
        "r2_adjusted": 1 - (ss_res / df_res) / (ss_tot / (n - 1)) if df_res > 0 and n > 1 else model_result["r2"],
        "syx": np.sqrt(ms_res),
        "f_value": f_value,
        "df_reg": df_reg,
        "df_res": df_res,
        "ss_reg": ss_reg,
        "ss_res": ss_res,
        "ss_tot": ss_tot,
    }


def regression_plot(x, y, model_result, title="回归拟合图"):
    """
    回归拟合可视化。
    
    Returns
    -------
    matplotlib.figure.Figure
    """
    import matplotlib.pyplot as plt
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 拟合图
    x_sorted = np.argsort(x)
    ax1.scatter(x, y, color='#3498db', s=40, label='实际数据', zorder=5)
    ax1.plot(x[x_sorted], model_result["y_pred"][x_sorted], 
             color='#e74c3c', linewidth=2, label='拟合曲线')
    ax1.set_title(title)
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.legend()
    ax1.grid(alpha=0.3)
    
    # 残差图
    ax2.scatter(model_result["y_pred"], model_result["residuals"], 
                color='#2ecc71', s=40, alpha=0.7)
    ax2.axhline(0, color='red', linestyle='--', linewidth=1)
    ax2.set_title("残差分布")
    ax2.set_xlabel("拟合值")
    ax2.set_ylabel("残差")
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    return fig
