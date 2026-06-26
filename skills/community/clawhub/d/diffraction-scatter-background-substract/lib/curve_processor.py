#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
curve_processor.py — Three processing modes for 1D curves
三种一维曲线处理模式

Implements the core processing logic for each mode:
  1. MORPH_1D       – 1D curve → morphological bg estimate → subtract → Curve1D
  2. FIT_1D         – 1D curve → polynomial fit bg estimate → subtract → Curve1D
  3. T_BG_SUBTRACT  – sample curve / (T/100) - background curve

Adapts bg_math algorithms for 1D.
适配 bg_math 算法到 1D。
"""

from __future__ import annotations

import logging
import os
from typing import Optional, Tuple, List, Dict, Any

import numpy as np
from scipy import ndimage
from scipy.ndimage import minimum_filter1d, maximum_filter1d

from .curve_data import Curve1D, CurveMetadata, ProcessMode

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# NaN / Inf cleaning / NaN / Inf 清洗
# ---------------------------------------------------------------------------


def clean_curve_data(
    x: np.ndarray,
    y: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Remove NaN and Inf values from x/y arrays, keeping only finite points.
    去除 x/y 数组中的 NaN 和 Inf 值，仅保留有效数据点。

    If leading/trailing points are removed, the arrays are trimmed.
    If NaN/Inf appear in the middle, those points are dropped
    (no interpolation — the user requested cleaning, not repair).

    Parameters / 参数
    -----------------
    x, y : np.ndarray
        Input arrays / 输入数组

    Returns / 返回
    --------------
    (x_clean, y_clean) : Tuple[np.ndarray, np.ndarray]
        Cleaned arrays / 清洗后的数组
    """
    finite_mask = np.isfinite(x) & np.isfinite(y)
    n_removed = int((~finite_mask).sum())
    if n_removed > 0:
        logger.info(
            "数据清洗：移除 %d 个无效点（NaN/Inf），保留 %d / %d",
            n_removed,
            finite_mask.sum(),
            len(finite_mask),
        )
    return x[finite_mask], y[finite_mask]


# ---------------------------------------------------------------------------
# 1D background estimation algorithms / 1D 背景估计算法
# ---------------------------------------------------------------------------


def morphological_background_1d(
    y: np.ndarray,
    radius: int = 50,
    iterations: int = 1,
) -> np.ndarray:
    """
    Estimate background of a 1D curve using morphological opening.
    使用形态学开运算估计 1D 曲线的背景。

    1D equivalent of bg_math.morphological_background.
    """
    size = 2 * radius + 1
    result = y.astype(np.float64).copy()
    for _ in range(iterations):
        eroded = minimum_filter1d(result, size=size, mode="nearest")
        result = maximum_filter1d(eroded, size=size, mode="nearest")
    return np.minimum(result, y)


def polynomial_background_1d(
    x: np.ndarray,
    y: np.ndarray,
    degree: int = 4,
    quantile: Optional[float] = None,
    n_segments: int = 1,
) -> np.ndarray:
    """
    Estimate background of a 1D curve using polynomial fitting.
    使用多项式拟合估计 1D 曲线的背景。

    Optionally fits only to data below a quantile threshold
    to avoid peak contributions.
    """
    if n_segments <= 1:
        return _polyfit_segment(x, y, degree, quantile)

    seg_len = max(1, len(x) // n_segments)
    bg = np.zeros_like(y, dtype=np.float64)
    for i in range(n_segments):
        start = i * seg_len
        end = (i + 1) * seg_len if i < n_segments - 1 else len(x)
        bg[start:end] = _polyfit_segment(x[start:end], y[start:end], degree, quantile)
    return bg


def _polyfit_segment(
    x: np.ndarray,
    y: np.ndarray,
    degree: int,
    quantile: Optional[float],
) -> np.ndarray:
    if len(x) <= degree:
        return np.full_like(y, np.median(y), dtype=np.float64)

    if quantile is not None and 0 < quantile < 1:
        threshold = np.quantile(y, quantile)
        mask = y <= threshold
        if mask.sum() > degree:
            coeffs = np.polyfit(x[mask], y[mask], degree)
        else:
            coeffs = np.polyfit(x, y, degree)
    else:
        coeffs = np.polyfit(x, y, degree)

    bg = np.polyval(coeffs, x)
    return np.minimum(bg, y)


def summarize_curve_quality(
    curve: Curve1D,
    background: np.ndarray,
    subtracted: np.ndarray,
    method: str,
) -> Dict[str, Any]:
    """
    Summarize non-fatal quality signals for logging/UI.
    汇总用于日志/UI 的非致命质量信号。
    """
    y = np.asarray(curve.y, dtype=np.float64)
    bg = np.asarray(background, dtype=np.float64)
    sub = np.asarray(subtracted, dtype=np.float64)

    warnings: List[str] = []
    finite_bg_ratio = float(np.isfinite(bg).sum()) / float(bg.size) if bg.size else 0.0
    finite_sub_ratio = float(np.isfinite(sub).sum()) / float(sub.size) if sub.size else 0.0
    zero_fraction = float(np.mean(np.isclose(sub, 0.0, atol=1e-12))) if sub.size else 0.0
    bg_ratio = 0.0
    y_mean = float(np.mean(np.abs(y))) if y.size else 0.0
    if y_mean > 1e-12:
        bg_ratio = float(np.mean(np.abs(bg))) / y_mean

    if finite_bg_ratio < 1.0:
        warnings.append("background_contains_non_finite_values")
    if finite_sub_ratio < 1.0:
        warnings.append("subtracted_contains_non_finite_values")
    if zero_fraction >= 0.98:
        warnings.append("subtracted_nearly_all_zero")
    if method == "poly" and bg_ratio >= 0.98:
        warnings.append("poly_background_almost_matches_raw")
    if method in {"morph", "rolling_ball"} and bg_ratio <= 0.02:
        warnings.append("background_estimate_nearly_zero")

    return {
        "quality_method": method,
        "quality_bg_ratio": round(bg_ratio, 6),
        "quality_zero_fraction": round(zero_fraction, 6),
        "quality_finite_bg_ratio": round(finite_bg_ratio, 6),
        "quality_finite_sub_ratio": round(finite_sub_ratio, 6),
        "quality_warnings": warnings,
    }


def rolling_ball_background_1d(
    y: np.ndarray,
    radius: float = 50.0,
) -> np.ndarray:
    """
    Estimate background of a 1D curve using rolling ball method.
    使用滚球法估计 1D 曲线的背景。
    """
    y_f = y.astype(np.float64)
    size = max(3, int(2 * radius + 1))
    if size % 2 == 0:
        size += 1

    bg = minimum_filter1d(y_f, size=size, mode="nearest")
    if radius > 2:
        bg = ndimage.gaussian_filter1d(bg, sigma=max(1, radius / 4.0))
    return np.minimum(bg, y_f)


# ---------------------------------------------------------------------------
# CurveProcessorConfig / 曲线处理器配置
# ---------------------------------------------------------------------------


class CurveProcessorConfig:
    """Configuration for CurveProcessor. 曲线处理器配置。"""

    def __init__(
        self,
        process_mode: ProcessMode = ProcessMode.MORPH_1D,
        transmission: float = 100.0,
        morph_radius: int = 50,
        morph_iterations: int = 1,
        poly_degree: int = 4,
        poly_quantile: Optional[float] = 0.3,
        poly_n_segments: int = 1,
        rolling_ball_radius: float = 50.0,
        bg_method_1d: str = "morph",
        phys_formula: str = "",
        phys_density: float = 1.0,
        phys_thickness_mm: float = 1.0,
        phys_sd_mm: float = 200.0,
        phys_energy_eV: float = 12700.0,
        phys_wavelength_A: float = 0.976,
        phys_sample_abs_on: bool = False,
        phys_unit: str = "q",
        phys_scale_mode: str = "auto",
        phys_scale_factor: float = 1.0,
    ):
        self.process_mode = process_mode
        self.transmission = transmission
        self.morph_radius = morph_radius
        self.morph_iterations = morph_iterations
        self.poly_degree = poly_degree
        self.poly_quantile = poly_quantile
        self.poly_n_segments = poly_n_segments
        self.rolling_ball_radius = rolling_ball_radius
        self.bg_method_1d = bg_method_1d
        self.phys_formula = phys_formula
        self.phys_density = phys_density
        self.phys_thickness_mm = phys_thickness_mm
        self.phys_sd_mm = phys_sd_mm
        self.phys_energy_eV = phys_energy_eV
        self.phys_wavelength_A = phys_wavelength_A
        self.phys_sample_abs_on = phys_sample_abs_on
        self.phys_unit = phys_unit
        self.phys_scale_mode = phys_scale_mode
        self.phys_scale_factor = phys_scale_factor


# ---------------------------------------------------------------------------
# CurveProcessor / 曲线处理器
# ---------------------------------------------------------------------------


class CurveProcessor:
    """
    Main processor implementing the three 1D curve processing modes.
    实现三种一维曲线处理模式的主处理器。
    """

    def __init__(self, config: Optional[CurveProcessorConfig] = None):
        self.config = config or CurveProcessorConfig()

    def estimate_background_1d(self, curve: Curve1D) -> np.ndarray:
        """Estimate background of a 1D curve using configured method."""
        method = self.config.bg_method_1d
        if method == "morph":
            return morphological_background_1d(
                curve.y,
                radius=self.config.morph_radius,
                iterations=self.config.morph_iterations,
            )
        elif method == "poly":
            return polynomial_background_1d(
                curve.x,
                curve.y,
                degree=self.config.poly_degree,
                quantile=self.config.poly_quantile,
                n_segments=self.config.poly_n_segments,
            )
        elif method == "rolling_ball":
            return rolling_ball_background_1d(
                curve.y,
                radius=self.config.rolling_ball_radius,
            )
        else:
            raise ValueError(f"Unknown 1D bg method: {method}")

    def apply_background_subtraction(self, curve: Curve1D) -> Curve1D:
        """
        Estimate and subtract background from a 1D curve.
        Returns a new Curve1D with background and subtracted populated.
        """
        bg = self.estimate_background_1d(curve)
        sub = np.maximum(curve.y - bg, 0.0)
        result = Curve1D(
            x=curve.x.copy(),
            y=curve.y.copy(),
            metadata=curve.metadata,
            background=bg,
            subtracted=sub,
        )
        result.metadata.extra.update(
            summarize_curve_quality(result, bg, sub, self.config.bg_method_1d)
        )
        return result

    def process_morph_1d(self, curve: Curve1D) -> Curve1D:
        """
        Mode 3: Morphological background estimation on 1D curve.
        模式 3：对 1D 曲线进行形态学背景估计。
        """
        result = self.apply_background_subtraction(curve)
        result.metadata.process_mode = ProcessMode.MORPH_1D
        result.metadata.extra["morph_radius"] = self.config.morph_radius
        result.metadata.extra["morph_iterations"] = self.config.morph_iterations
        return result

    def process_fit_1d(self, curve: Curve1D) -> Curve1D:
        """
        Mode 4: Polynomial fitting background estimation on 1D curve.
        模式 4：对 1D 曲线进行多项式拟合背景估计。
        """
        bg = polynomial_background_1d(
            curve.x,
            curve.y,
            degree=self.config.poly_degree,
            quantile=self.config.poly_quantile,
            n_segments=self.config.poly_n_segments,
        )
        sub = np.maximum(curve.y - bg, 0.0)
        result = Curve1D(
            x=curve.x.copy(),
            y=curve.y.copy(),
            metadata=curve.metadata,
            background=bg,
            subtracted=sub,
        )
        result.metadata.process_mode = ProcessMode.FIT_1D
        result.metadata.extra["poly_degree"] = self.config.poly_degree
        result.metadata.extra["poly_quantile"] = self.config.poly_quantile
        result.metadata.extra.update(summarize_curve_quality(result, bg, sub, "poly"))
        return result

    def process_t_bg_subtract(
        self,
        sample: Curve1D,
        background: Curve1D,
        transmission_percent: float,
    ) -> Curve1D:
        """
        Apply transmission-corrected reference subtraction on 1D curves.
        对 1D 曲线执行透过率修正的参考背景扣除。
        """
        if transmission_percent <= 0:
            raise ValueError("Transmission percent must be > 0")

        transmission_ratio = transmission_percent / 100.0
        subtracted = sample.y / transmission_ratio - background.y
        result = sample.copy()
        result.background = background.y.copy()
        result.subtracted = subtracted
        result.metadata.process_mode = ProcessMode.T_BG_SUBTRACT
        result.metadata.extra["transmission_percent"] = transmission_percent
        result.metadata.extra["background_source_file"] = background.metadata.source_file
        result.metadata.extra.update(
            summarize_curve_quality(result, background.y, subtracted, "t_bg")
        )
        return result

    def process_phys_fit(self, curve: Curve1D) -> Curve1D:
        """
        Physics-based attenuation simulation: use air (and optional sample)
        absorption to generate a simulated background curve.
        物理衰减仿真：利用空气（和可选样品）吸收生成仿真背景曲线。
        """
        # phys_fit module requires full BGsub package installation
        # phys_fit 模块需要完整安装 BGsub 包
        from BGsub.core.phys_fit import (
            simulate_phys_curve,
            auto_scale_factor,
        )

        I_sim, info = simulate_phys_curve(
            x=curve.x,
            unit=self.config.phys_unit,
            energy_eV=self.config.phys_energy_eV,
            wavelength_A=self.config.phys_wavelength_A,
            sd_mm=self.config.phys_sd_mm,
            formula=self.config.phys_formula,
            density=self.config.phys_density,
            thickness_mm=self.config.phys_thickness_mm,
            sample_abs_on=self.config.phys_sample_abs_on,
        )

        if self.config.phys_scale_mode == "auto":
            scale = auto_scale_factor(curve.y, I_sim)
        else:
            scale = self.config.phys_scale_factor

        bg = scale * I_sim
        sub = np.maximum(curve.y - bg, 0.0)
        result = Curve1D(
            x=curve.x.copy(),
            y=curve.y.copy(),
            metadata=curve.metadata,
            background=bg,
            subtracted=sub,
        )
        result.metadata.process_mode = ProcessMode.PHYS_FIT
        result.metadata.extra["phys_scale_factor"] = scale
        result.metadata.extra["phys_scale_mode"] = self.config.phys_scale_mode
        result.metadata.extra.update(info)
        result.metadata.extra.update(summarize_curve_quality(result, bg, sub, "phys_fit"))
        return result

    def process(self, input_data: Curve1D) -> Curve1D:
        """
        Dispatch to the correct processing mode based on config.
        NaN/Inf points are cleaned before processing.
        根据配置分发到正确的处理模式。处理前清洗 NaN/Inf 数据点。

        Parameters / 参数
        -----------------
        input_data : Curve1D
            1D curve to process / 要处理的一维曲线
        """
        x_clean, y_clean = clean_curve_data(input_data.x, input_data.y)
        if len(x_clean) < 3:
            raise ValueError(f"清洗后仅剩 {len(x_clean)} 个有效数据点，不足以处理")
        cleaned = Curve1D(
            x=x_clean,
            y=y_clean,
            metadata=input_data.metadata,
        )

        mode = self.config.process_mode

        if mode == ProcessMode.MORPH_1D:
            return self.process_morph_1d(cleaned)

        elif mode == ProcessMode.FIT_1D:
            return self.process_fit_1d(cleaned)

        elif mode == ProcessMode.PHYS_FIT:
            return self.process_phys_fit(cleaned)

        elif mode == ProcessMode.T_BG_SUBTRACT:
            raise ValueError(
                "T_BG_SUBTRACT requires sample/background curves; use process_t_bg_subtract()"
            )

        else:
            raise ValueError(f"Unknown process mode: {mode}")
