"""
方法验证指标计算模块

通用功能：检出限/定量限、回收率、不确定度传递等检验检测行业标准计算。
"""
import numpy as np


def calculate_lod_loq(calibration_data, method="pharmacopoeia"):
    """
    计算检出限（LOD）和定量限（LOQ）。
    
    Parameters
    ----------
    calibration_data : dict
        标定数据，包含:
        - "x": 浓度数组
        - "y": 响应值数组
        - "blank_sd": 空白标准偏差（可选）
        - "slope": 斜率（可选，不提供则自动计算）
    method : str
        "pharmacopoeia" — 药典法: LOD = 3.3 * Sy/x / slope, LOQ = 10 * Sy/x / slope
        "gbt27417" — GB/T 27417: LOD = 3 * Sy/x / slope, LOQ = 9 * Sy/x / slope (= 3 × LOD)
    
    Returns
    -------
    dict
        {"lod", "loq", "method", "syx", "slope", "intercept"}
    """
    x = np.array(calibration_data["x"], dtype=float)
    y = np.array(calibration_data["y"], dtype=float)
    
    # 线性回归求斜率和剩余标准偏差
    n = len(x)
    x_mean, y_mean = np.mean(x), np.mean(y)
    slope = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
    intercept = y_mean - slope * x_mean
    y_pred = slope * x + intercept
    residuals = y - y_pred
    syx = np.sqrt(np.sum(residuals ** 2) / (n - 2))
    
    # 检出限因子
    if method == "pharmacopoeia":
        lod_factor = 3.3
        loq_factor = 10
    elif method in ("gbt27417", "17417"):
        lod_factor = 3
        loq_factor = 9
    else:
        raise ValueError(
            f"不支持的方法: '{method}'。\n"
            "支持的方法：\n"
            "  'pharmacopoeia' — 药典法: LOD = 3.3×Sy/x / slope（默认）\n"
            "  'gbt27417'      — 国标法: LOD = 3×Sy/x / slope, LOQ = 9×Sy/x / slope\n"
            "建议：将 method 参数设为 'pharmacopoeia' 或 'gbt27417'"
        )
    
    lod = lod_factor * syx / slope if slope != 0 else float('inf')
    loq = loq_factor * syx / slope if slope != 0 else float('inf')
    
    return {
        "lod": lod,
        "loq": loq,
        "method": method,
        "syx": syx,
        "slope": slope,
        "intercept": intercept,
        "equation": f"y = {slope:.6f}x {'+ ' if intercept >= 0 else '- '}{abs(intercept):.6f}",
        "lod_expression": f"LOD = {lod_factor} × {syx:.4f} / {slope:.4f} = {lod:.4f}",
        "loq_expression": f"LOQ = {loq_factor} × {syx:.4f} / {slope:.4f} = {loq:.4f}",
    }


def calc_recovery(measured, spiked, blank=0):
    """
    加标回收率计算。
    
    Parameters
    ----------
    measured : array-like
        加标样测定值
    spiked : float or array-like
        加标浓度/量
    blank : float
        空白值
    
    Returns
    -------
    dict
        {"recovery_mean", "recovery_std", "recovery_rsd", "individual_recoveries"}
    """
    measured = np.array(measured, dtype=float)
    spiked_val = np.array(spiked, dtype=float) if isinstance(spiked, (list, np.ndarray)) else np.full_like(measured, float(spiked))
    
    recoveries = (measured - blank) / spiked_val * 100
    
    return {
        "recovery_mean": np.mean(recoveries),
        "recovery_std": np.std(recoveries, ddof=1),
        "recovery_rsd": np.std(recoveries, ddof=1) / np.mean(recoveries) * 100,
        "individual_recoveries": recoveries.tolist(),
        "n": len(recoveries),
    }


def uncertainty_propagation(calibration_data, sample_response, sample_count=1, 
                             std_curve_count=None, force_zero=False):
    """
    标准曲线不确定度传递计算。
    
    根据拟合校准曲线，计算样品测定结果的不确定度。
    
    Parameters
    ----------
    calibration_data : dict
        标定数据 {"x": 浓度, "y": 响应}
    sample_response : float or array-like
        样品的响应值
    sample_count : int
        样品测定次数
    std_curve_count : int, optional
        标曲测定点数
    force_zero : bool
        标曲是否强制过原点
    
    Returns
    -------
    dict
        {"relative_uncertainty", "combined_uncertainty", "components"}
    """
    x = np.array(calibration_data["x"], dtype=float)
    y = np.array(calibration_data["y"], dtype=float)
    
    n = len(x)
    p = sample_count
    
    # 回归统计
    if force_zero:
        slope = np.sum(x * y) / np.sum(x ** 2)
        intercept = 0.0
        y_pred = slope * x
        df = n - 1
    else:
        x_mean, y_mean = np.mean(x), np.mean(y)
        slope = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
        intercept = y_mean - slope * x_mean
        y_pred = slope * x + intercept
        df = n - 2
    
    residuals = y - y_pred
    syx = np.sqrt(np.sum(residuals ** 2) / df)
    
    # 样品浓度反推
    sample_y = np.array(sample_response, dtype=float)
    sample_x = (sample_y - intercept) / slope
    sample_x_mean = np.mean(sample_x)
    
    # 不确定度分量
    x_demeaned = x - np.mean(x)
    sxx = np.sum(x_demeaned ** 2)
    
    # 相对不确定度公式
    term1 = 1 / p
    term2 = 1 / n
    term3 = (sample_x_mean - np.mean(x)) ** 2 / sxx
    
    relative_u = (syx / slope) * np.sqrt(term1 + term2 + term3) / sample_x_mean if sample_x_mean != 0 else 0
    
    return {
        "sample_concentration": sample_x_mean,
        "relative_uncertainty": relative_u,
        "combined_uncertainty": relative_u * sample_x_mean,
        "syx": syx,
        "slope": slope,
        "intercept": intercept,
        "components": {
            "syx": syx,
            "sxx": sxx,
            "x_mean": np.mean(x),
            "n": n,
            "p": p,
        }
    }
