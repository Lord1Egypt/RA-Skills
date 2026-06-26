#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
curve_data.py — 1D curve data model and processing mode definitions
一维曲线数据模型与处理模式定义

Defines the core data structures for 1D curve processing in BGsub:
  - ProcessMode: three independent processing modes
  - Curve1D: lightweight immutable-style container for x/y + metadata
  - CurveMetadata: descriptive metadata attached to each curve
"""

from __future__ import annotations

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

import numpy as np


# ---------------------------------------------------------------------------
# Processing modes / 处理模式
# ---------------------------------------------------------------------------


class ProcessMode(Enum):
    """
    Three independent processing modes for 1D curve pipeline.
    三种独立的 1D 曲线处理模式。

    MORPH_1D           – Load existing 1D curve, morphological background estimation,
                         subtract and output.
                         加载已有 1D 曲线，形态学背景估计后扣除输出。
    FIT_1D             – Load existing 1D curve, polynomial fitting background
                         estimation, subtract and output.
                         加载已有 1D 曲线，多项式拟合背景估计后扣除输出。
    T_BG_SUBTRACT      – Load sample/background 1D curves and apply
                         transmission-corrected subtraction.
                         加载样品/背景 1D 曲线并执行透过率修正后的扣除。
    PHYS_FIT           – Load existing 1D curve, physics-based attenuation simulation
                         (air + optional sample absorption), scale and subtract.
                         加载已有 1D 曲线，物理衰减仿真（空气+可选样品吸收），缩放后扣除。
    """

    MORPH_1D = "morph_1d"
    FIT_1D = "fit_1d"
    T_BG_SUBTRACT = "t_bg_subtract"
    PHYS_FIT = "phys_fit"


# ---------------------------------------------------------------------------
# Metadata / 元数据
# ---------------------------------------------------------------------------


@dataclass
class CurveMetadata:
    """
    Descriptive metadata for a 1D curve.
    一维曲线的描述性元数据。

    Attributes / 属性
    -----------------
    source_file : str
        Original file path or identifier / 原始文件路径或标识符
    source_type : str
        '1d_curve' / 数据来源类型
    x_label : str
        Axis label for x (e.g. 'q (A^-1)', '2theta (deg)')
        x 轴标签
    y_label : str
        Axis label for y (e.g. 'I', 'Intensity')
        y 轴标签
    x_unit : str
        Unit of x axis / x 轴单位
    process_mode : Optional[ProcessMode]
        Which mode produced this curve / 产生该曲线的处理模式
    extra : dict
        Arbitrary extra key-value metadata / 任意附加键值元数据
    """

    source_file: str = ""
    source_type: str = ""
    x_label: str = "x"
    y_label: str = "I"
    x_unit: str = ""
    process_mode: Optional[ProcessMode] = None
    extra: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Curve1D data container / 一维曲线数据容器
# ---------------------------------------------------------------------------


@dataclass
class Curve1D:
    """
    Lightweight container for a single 1D curve.
    单条一维曲线的轻量容器。

    Design notes / 设计说明:
      - Stores x and y as numpy arrays; does NOT copy on construction
        to keep overhead minimal.
      - ``metadata`` carries provenance information for downstream
        consumers (GUI, export).
      - ``background`` and ``subtracted`` are optionally populated by
        processing steps; callers should check for ``None``.

    Attributes / 属性
    -----------------
    x : np.ndarray
        Radial / angular axis values (float64) / 径向/角度轴值
    y : np.ndarray
        Intensity values (float64) / 强度值
    metadata : CurveMetadata
        Provenance metadata / 来源元数据
    background : np.ndarray or None
        Estimated background (set by processor) / 估计的背景（由处理器填充）
    subtracted : np.ndarray or None
        Background-subtracted result / 扣除背景后的结果
    """

    x: np.ndarray
    y: np.ndarray
    metadata: CurveMetadata = field(default_factory=CurveMetadata)
    background: Optional[np.ndarray] = None
    subtracted: Optional[np.ndarray] = None

    def __post_init__(self):
        """
        Validate array consistency and convert to float64.
        校验数组一致性并转为 float64。
        """
        self.x = np.asarray(self.x, dtype=np.float64)
        self.y = np.asarray(self.y, dtype=np.float64)
        if self.x.shape != self.y.shape:
            raise ValueError(
                f"x and y must have the same shape, got {self.x.shape} vs {self.y.shape}"
            )

    @property
    def n_points(self) -> int:
        """Number of data points / 数据点数"""
        return self.x.shape[0]

    @property
    def x_range(self) -> tuple:
        """(min, max) of x axis / x 轴范围"""
        return float(self.x.min()), float(self.x.max())

    @property
    def y_range(self) -> tuple:
        """(min, max) of y axis / y 轴范围"""
        finite = self.y[np.isfinite(self.y)]
        if finite.size == 0:
            return (0.0, 0.0)
        return float(finite.min()), float(finite.max())

    def copy(self) -> Curve1D:
        """
        Return a deep copy of this curve (arrays copied).
        返回此曲线的深拷贝（数组已复制）。
        """
        metadata = CurveMetadata(
            source_file=self.metadata.source_file,
            source_type=self.metadata.source_type,
            x_label=self.metadata.x_label,
            y_label=self.metadata.y_label,
            x_unit=self.metadata.x_unit,
            process_mode=self.metadata.process_mode,
            extra=self.metadata.extra.copy(),
        )
        return Curve1D(
            x=self.x.copy(),
            y=self.y.copy(),
            metadata=metadata,
            background=self.background.copy() if self.background is not None else None,
            subtracted=self.subtracted.copy() if self.subtracted is not None else None,
        )

    def memory_bytes(self) -> int:
        """
        Estimated memory footprint in bytes.
        估算内存占用字节数。
        """
        total = self.x.nbytes + self.y.nbytes
        if self.background is not None:
            total += self.background.nbytes
        if self.subtracted is not None:
            total += self.subtracted.nbytes
        return total

    def __repr__(self) -> str:
        return (
            f"Curve1D(n={self.n_points}, "
            f"x_range={self.x_range}, "
            f"source='{self.metadata.source_file}')"
        )
