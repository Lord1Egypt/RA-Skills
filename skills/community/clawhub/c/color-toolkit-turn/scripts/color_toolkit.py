#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Color Toolkit - 专业颜色工具集
支持颜色编码转换、对比度计算、互补色生成等功能
"""

import math
import random
import re
import json
from dataclasses import dataclass, asdict
from typing import List, Union, Optional, Tuple, Dict, Any


# ============ 数据结构 ============

@dataclass
class RGB:
    r: int
    g: int
    b: int

    def __str__(self):
        return f"RGB(r={self.r}, g={self.g}, b={self.b})"

    def to_dict(self):
        return {"r": self.r, "g": self.g, "b": self.b}


@dataclass
class HSL:
    h: float  # 0-360
    s: float  # 0-100
    l: float  # 0-100

    def __str__(self):
        return f"HSL(h={self.h}, s={self.s}%, l={self.l}%)"

    def to_dict(self):
        return {"h": round(self.h, 1), "s": round(self.s, 1), "l": round(self.l, 1)}


@dataclass
class HSV:
    h: float  # 0-360
    s: float  # 0-100
    v: float  # 0-100

    def __str__(self):
        return f"HSV(h={self.h}, s={self.s}%, v={self.v}%)"

    def to_dict(self):
        return {"h": round(self.h), "s": round(self.s), "v": round(self.v)}


@dataclass
class CMYK:
    c: int  # 0-100
    m: int
    y: int
    k: int

    def __str__(self):
        return f"CMYK(c={self.c}, m={self.m}, y={self.y}, k={self.k})"

    def to_dict(self):
        return asdict(self)


@dataclass
class ColorInfo:
    name: str
    hex: str
    rgb: Dict[str, int]
    hsl: Dict[str, float]
    hsv: Dict[str, float]
    cmyk: Dict[str, int]
    luminance: str
    grayscale: int
    temperature: str
    family: str

    def to_dict(self):
        return asdict(self)


@dataclass
class ContrastEvaluation:
    level: str
    color: str
    description: str

    def to_dict(self):
        return asdict(self)


@dataclass
class ContrastResult:
    algorithmLabel: str
    displayValue: str
    evaluation: Dict[str, Any]
    contrastValue: Union[float, str]

    def to_dict(self):
        return {
            "algorithmLabel": self.algorithmLabel,
            "displayValue": self.displayValue,
            "evaluation": self.evaluation,
            "contrastValue": self.contrastValue
        }


# ============ 核心转换引擎 ============

class ColorCore:
    """颜色转换核心引擎"""

    # ---------- 基础转换 ----------

    @staticmethod
    def hex_to_rgb(hex_str: str) -> RGB:
        """将十六进制颜色字符串转换为RGB对象"""
        match = re.match(r'^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$', hex_str, re.I)
        if not match:
            # 尝试3位简写
            match = re.match(r'^#?([a-f\d])([a-f\d])([a-f\d])$', hex_str, re.I)
            if match:
                return RGB(
                    r=int(match.group(1) * 2, 16),
                    g=int(match.group(2) * 2, 16),
                    b=int(match.group(3) * 2, 16)
                )
            return RGB(0, 0, 0)
        return RGB(
            r=int(match.group(1), 16),
            g=int(match.group(2), 16),
            b=int(match.group(3), 16)
        )

    @staticmethod
    def rgb_to_hex(r: float, g: float, b: float) -> str:
        """将RGB值转换为十六进制颜色字符串"""
        return "#{:02x}{:02x}{:02x}".format(
            round(max(0, min(255, r))),
            round(max(0, min(255, g))),
            round(max(0, min(255, b)))
        )

    @staticmethod
    def rgb_to_hsl(r: float, g: float, b: float) -> HSL:
        """将RGB值转换为HSL对象"""
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0
        maxc = max(r_norm, g_norm, b_norm)
        minc = min(r_norm, g_norm, b_norm)
        l = (maxc + minc) / 2.0

        if maxc == minc:
            h = 0.0
            s = 0.0
        else:
            d = maxc - minc
            s = d / (2.0 - maxc - minc) if l > 0.5 else d / (maxc + minc)
            if maxc == r_norm:
                h = (g_norm - b_norm) / d + (6.0 if g_norm < b_norm else 0.0)
            elif maxc == g_norm:
                h = (b_norm - r_norm) / d + 2.0
            else:
                h = (r_norm - g_norm) / d + 4.0
            h /= 6.0

        return HSL(
            h=round(h * 360.0, 1),
            s=round(s * 100.0, 1),
            l=round(l * 100.0, 1)
        )

    @staticmethod
    def hsl_to_rgb(h: float, s: float, l: float) -> RGB:
        """将HSL值转换为RGB对象"""
        h_norm = h % 360.0
        s_norm = max(0.0, min(100.0, s)) / 100.0
        l_norm = max(0.0, min(100.0, l)) / 100.0

        def hue2rgb(p: float, q: float, t: float) -> float:
            tt = t
            if tt < 0.0:
                tt += 1.0
            if tt > 1.0:
                tt -= 1.0
            if tt < 1.0 / 6.0:
                return p + (q - p) * 6.0 * tt
            if tt < 1.0 / 2.0:
                return q
            if tt < 2.0 / 3.0:
                return p + (q - p) * (2.0 / 3.0 - tt) * 6.0
            return p

        if s_norm == 0.0:
            val = round(l_norm * 255.0)
            return RGB(r=val, g=val, b=val)
        else:
            q = l_norm * (1.0 + s_norm) if l_norm < 0.5 else l_norm + s_norm - l_norm * s_norm
            p = 2.0 * l_norm - q
            r = hue2rgb(p, q, h_norm / 360.0 + 1.0 / 3.0)
            g = hue2rgb(p, q, h_norm / 360.0)
            b = hue2rgb(p, q, h_norm / 360.0 - 1.0 / 3.0)

        return RGB(
            r=round(r * 255.0),
            g=round(g * 255.0),
            b=round(b * 255.0)
        )

    @staticmethod
    def rgb_to_hsv(r: float, g: float, b: float) -> HSV:
        """将RGB值转换为HSV对象"""
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0
        maxc = max(r_norm, g_norm, b_norm)
        minc = min(r_norm, g_norm, b_norm)
        d = maxc - minc

        if maxc == 0.0:
            s = 0.0
        else:
            s = d / maxc

        v = maxc

        if maxc == minc:
            h = 0.0
        else:
            if maxc == r_norm:
                h = (g_norm - b_norm) / d + (6.0 if g_norm < b_norm else 0.0)
            elif maxc == g_norm:
                h = (b_norm - r_norm) / d + 2.0
            else:
                h = (r_norm - g_norm) / d + 4.0
            h /= 6.0

        return HSV(
            h=round(h * 360.0),
            s=round(s * 100.0),
            v=round(v * 100.0)
        )

    @staticmethod
    def hsv_to_rgb(h: float, s: float, v: float) -> RGB:
        """将HSV值转换为RGB对象"""
        h_norm = h % 360.0
        s_norm = max(0.0, min(100.0, s)) / 100.0
        v_norm = max(0.0, min(100.0, v)) / 100.0

        if s_norm == 0.0:
            val = round(v_norm * 255.0)
            return RGB(r=val, g=val, b=val)

        i = int(h_norm / 60.0) % 6
        f = h_norm / 60.0 - i
        p = v_norm * (1.0 - s_norm)
        q = v_norm * (1.0 - f * s_norm)
        t = v_norm * (1.0 - (1.0 - f) * s_norm)

        i_mod = i % 6
        if i_mod == 0:
            return RGB(r=round(v_norm * 255), g=round(t * 255), b=round(p * 255))
        elif i_mod == 1:
            return RGB(r=round(q * 255), g=round(v_norm * 255), b=round(p * 255))
        elif i_mod == 2:
            return RGB(r=round(p * 255), g=round(v_norm * 255), b=round(t * 255))
        elif i_mod == 3:
            return RGB(r=round(p * 255), g=round(q * 255), b=round(v_norm * 255))
        elif i_mod == 4:
            return RGB(r=round(t * 255), g=round(p * 255), b=round(v_norm * 255))
        else:
            return RGB(r=round(v_norm * 255), g=round(p * 255), b=round(q * 255))

    @staticmethod
    def rgb_to_cmyk(r: float, g: float, b: float) -> CMYK:
        """计算CMYK值"""
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0
        k = 1.0 - max(r_norm, g_norm, b_norm)

        EPS = 1e-6
        if k > 1.0 - EPS:
            return CMYK(c=0, m=0, y=0, k=100)
        else:
            one_minus_k = 1.0 - k
            c = (1.0 - r_norm - k) / one_minus_k
            m = (1.0 - g_norm - k) / one_minus_k
            y = (1.0 - b_norm - k) / one_minus_k
            return CMYK(
                c=min(100, max(0, round(c * 100))),
                m=min(100, max(0, round(m * 100))),
                y=min(100, max(0, round(y * 100))),
                k=min(100, max(0, round(k * 100)))
            )

    @staticmethod
    def cmyk_to_rgb(c: float, m: float, y: float, k: float) -> RGB:
        """将CMYK值转换为RGB对象"""
        c_norm = max(0.0, min(100.0, c)) / 100.0
        m_norm = max(0.0, min(100.0, m)) / 100.0
        y_norm = max(0.0, min(100.0, y)) / 100.0
        k_norm = max(0.0, min(100.0, k)) / 100.0

        r = 255.0 * (1.0 - c_norm) * (1.0 - k_norm)
        g = 255.0 * (1.0 - m_norm) * (1.0 - k_norm)
        b = 255.0 * (1.0 - y_norm) * (1.0 - k_norm)
        return RGB(
            r=round(max(0, min(255, r))),
            g=round(max(0, min(255, g))),
            b=round(max(0, min(255, b)))
        )

    # ---------- 便捷转换 ----------

    @staticmethod
    def hex_to_hsl(hex_str: str) -> HSL:
        """将十六进制颜色字符串转换为HSL对象"""
        rgb = ColorCore.hex_to_rgb(hex_str)
        return ColorCore.rgb_to_hsl(rgb.r, rgb.g, rgb.b)

    @staticmethod
    def parse_color_input(color_str: str) -> RGB:
        """解析各种格式的颜色输入，返回RGB对象"""
        color_str = color_str.strip()

        # HEX格式
        if color_str.startswith('#') or re.match(r'^[a-f0-9]{3,6}$', color_str, re.I):
            if not color_str.startswith('#'):
                color_str = '#' + color_str
            return ColorCore.hex_to_rgb(color_str)

        # RGB格式
        rgb_match = re.match(r'rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', color_str, re.I)
        if rgb_match:
            return RGB(
                r=int(rgb_match.group(1)),
                g=int(rgb_match.group(2)),
                b=int(rgb_match.group(3))
            )

        # HSL格式
        hsl_match = re.match(r'hsl\s*\(\s*(\d+)\s*,\s*([\d.]+)%?\s*,\s*([\d.]+)%?\s*\)', color_str, re.I)
        if hsl_match:
            return ColorCore.hsl_to_rgb(
                float(hsl_match.group(1)),
                float(hsl_match.group(2)),
                float(hsl_match.group(3))
            )

        raise ValueError(f"无法解析颜色格式: {color_str}")

    # ---------- 亮度与灰度 ----------

    @staticmethod
    def calculate_luminance(r: float, g: float, b: float) -> str:
        """计算相对亮度，返回三位小数字符串"""
        def linearize(c: float) -> float:
            c_norm = c / 255.0
            if c_norm <= 0.03928:
                return c_norm / 12.92
            else:
                return ((c_norm + 0.055) / 1.055) ** 2.4

        rL = linearize(r)
        gL = linearize(g)
        bL = linearize(b)
        luminance = 0.2126 * rL + 0.7152 * gL + 0.0722 * bL
        return f"{luminance:.3f}"

    @staticmethod
    def calculate_grayscale(r: float, g: float, b: float) -> int:
        """计算灰度值 (0-255)"""
        return round(0.299 * r + 0.587 * g + 0.114 * b)

    # ---------- 颜色信息 ----------

    @staticmethod
    def get_color_temperature(r: float, g: float, b: float) -> str:
        """判断色温"""
        avg = (r + g + b) / 3.0
        if avg == 0:
            return "中性"
        r_ratio = r / avg
        b_ratio = b / avg
        if r_ratio > 1.2 and b_ratio < 0.8:
            return "暖色"
        elif b_ratio > 1.2 and r_ratio < 0.8:
            return "冷色"
        return "中性"

    @staticmethod
    def get_color_family(hsl: HSL) -> str:
        """根据HSL获取色系分类"""
        h = hsl.h
        s = hsl.s
        l = hsl.l

        if s < 10 or l < 5 or l > 95:
            return "灰色系"

        if 0 <= h < 15:
            return "红色系"
        elif 15 <= h < 30:
            return "橙红系"
        elif 30 <= h < 45:
            return "橙色系"
        elif 45 <= h < 60:
            return "橙黄系"
        elif 60 <= h < 75:
            return "黄色系"
        elif 75 <= h < 90:
            return "黄绿系"
        elif 90 <= h < 120:
            return "绿色系"
        elif 120 <= h < 150:
            return "青绿系"
        elif 150 <= h < 180:
            return "青色系"
        elif 180 <= h < 210:
            return "蓝绿系"
        elif 210 <= h < 240:
            return "蓝色系"
        elif 240 <= h < 270:
            return "靛蓝系"
        elif 270 <= h < 300:
            return "紫色系"
        elif 300 <= h < 330:
            return "紫红系"
        elif 330 <= h < 345:
            return "粉红系"
        else:
            return "红色系"

    @staticmethod
    def get_full_color_info(color_input: str, color_name: str = "颜色") -> ColorInfo:
        """获取完整的颜色信息"""
        rgb = ColorCore.parse_color_input(color_input)
        hex_str = ColorCore.rgb_to_hex(rgb.r, rgb.g, rgb.b)
        hsl = ColorCore.rgb_to_hsl(rgb.r, rgb.g, rgb.b)
        hsv = ColorCore.rgb_to_hsv(rgb.r, rgb.g, rgb.b)
        luminance = ColorCore.calculate_luminance(rgb.r, rgb.g, rgb.b)
        grayscale = ColorCore.calculate_grayscale(rgb.r, rgb.g, rgb.b)
        cmyk = ColorCore.rgb_to_cmyk(rgb.r, rgb.g, rgb.b)
        temperature = ColorCore.get_color_temperature(rgb.r, rgb.g, rgb.b)
        family = ColorCore.get_color_family(hsl)

        return ColorInfo(
            name=color_name,
            hex=hex_str,
            rgb=rgb.to_dict(),
            hsl=hsl.to_dict(),
            hsv=hsv.to_dict(),
            cmyk=cmyk.to_dict(),
            luminance=luminance,
            grayscale=grayscale,
            temperature=temperature,
            family=family
        )

    # ---------- 互补色与对比色 ----------

    @staticmethod
    def calculate_complementary_color(r: float, g: float, b: float) -> RGB:
        """计算互补色"""
        hsl = ColorCore.rgb_to_hsl(r, g, b)

        # 处理灰色
        if hsl.s <= 10:
            target_contrast = 4.5
            if hsl.l > 50:
                target_l = max(0.0, hsl.l - hsl.l * 0.7)
            else:
                target_l = min(100.0, hsl.l + (100.0 - hsl.l) * 0.7)
            return ColorCore.hsl_to_rgb(hsl.h, hsl.s, target_l)

        complementary_hue = (hsl.h + 180) % 360
        adjusted_s = hsl.s
        adjusted_l = hsl.l

        if hsl.s < 30:
            adjusted_s = min(100.0, hsl.s * 1.5)
        if hsl.l > 70:
            adjusted_l = max(30.0, hsl.l - 20)
        elif hsl.l < 30:
            adjusted_l = min(70.0, hsl.l + 20)

        return ColorCore.hsl_to_rgb(complementary_hue, adjusted_s, adjusted_l)

    @staticmethod
    def get_triadic_colors(r: float, g: float, b: float) -> List[str]:
        """获取三色组（120°间隔）"""
        hsl = ColorCore.rgb_to_hsl(r, g, b)
        hues = [(hsl.h + 120) % 360, (hsl.h + 240) % 360]
        colors = [ColorCore.rgb_to_hex(r, g, b)]
        for hue in hues:
            rgb = ColorCore.hsl_to_rgb(hue, hsl.s, hsl.l)
            colors.append(ColorCore.rgb_to_hex(rgb.r, rgb.g, rgb.b))
        return colors

    @staticmethod
    def get_tetradic_colors(r: float, g: float, b: float) -> List[str]:
        """获取四色组（90°间隔）"""
        hsl = ColorCore.rgb_to_hsl(r, g, b)
        hues = [(hsl.h + 90) % 360, (hsl.h + 180) % 360, (hsl.h + 270) % 360]
        colors = [ColorCore.rgb_to_hex(r, g, b)]
        for hue in hues:
            rgb = ColorCore.hsl_to_rgb(hue, hsl.s, hsl.l)
            colors.append(ColorCore.rgb_to_hex(rgb.r, rgb.g, rgb.b))
        return colors

    @staticmethod
    def get_analogous_colors(r: float, g: float, b: float, count: int = 3) -> List[str]:
        """获取类似色（指定数量）"""
        hsl = ColorCore.rgb_to_hsl(r, g, b)
        step = 30
        colors = []
        for i in range(count):
            offset = (i - count // 2) * step
            hue = (hsl.h + offset) % 360
            rgb = ColorCore.hsl_to_rgb(hue, hsl.s, hsl.l)
            colors.append(ColorCore.rgb_to_hex(rgb.r, rgb.g, rgb.b))
        return colors

    # ---------- 对比度计算 ----------

    @staticmethod
    def _sRGB_to_linear(c: float) -> float:
        """sRGB转线性RGB"""
        cc = c / 255.0
        if cc <= 0.04045:
            return cc / 12.92
        else:
            return ((cc + 0.055) / 1.055) ** 2.4

    @staticmethod
    def _calculate_relative_luminance(r: float, g: float, b: float) -> float:
        """计算相对亮度"""
        rL = ColorCore._sRGB_to_linear(r)
        gL = ColorCore._sRGB_to_linear(g)
        bL = ColorCore._sRGB_to_linear(b)
        return 0.2126729 * rL + 0.7151522 * gL + 0.0721750 * bL

    @staticmethod
    def calculate_wcag21_contrast(r1: float, g1: float, b1: float,
                                   r2: float, g2: float, b2: float) -> str:
        """计算WCAG 2.1对比度"""
        l1 = ColorCore._calculate_relative_luminance(r1, g1, b1)
        l2 = ColorCore._calculate_relative_luminance(r2, g2, b2)
        lighter = max(l1, l2)
        darker = min(l1, l2)
        ratio = (lighter + 0.05) / (darker + 0.05)
        return f"{ratio:.2f}"

    @staticmethod
    def calculate_apca_contrast(r1: float, g1: float, b1: float,
                                 r2: float, g2: float, b2: float) -> float:
        """计算APCA对比度 (Lc值)"""
        L1 = ColorCore._calculate_relative_luminance(r1, g1, b1)
        L2 = ColorCore._calculate_relative_luminance(r2, g2, b2)

        if L2 > L1:
            contrast = (L2 ** 0.68 - L1 ** 0.68) * 1.14
        else:
            contrast = (L1 ** 0.68 - L2 ** 0.68) * 1.14

        lc_value = abs(contrast) * 100
        if lc_value < 0.5:
            lc_value = 0.5
        if lc_value > 108:
            lc_value = 108
        return round(lc_value, 1)

    @staticmethod
    def _sRGB_to_XYZ(r: float, g: float, b: float) -> Tuple[float, float, float]:
        """sRGB转XYZ"""
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0

        r_linear = ((r_norm + 0.055) / 1.055) ** 2.4 if r_norm > 0.04045 else r_norm / 12.92
        g_linear = ((g_norm + 0.055) / 1.055) ** 2.4 if g_norm > 0.04045 else g_norm / 12.92
        b_linear = ((b_norm + 0.055) / 1.055) ** 2.4 if b_norm > 0.04045 else b_norm / 12.92

        x = r_linear * 0.4124564 + g_linear * 0.3575761 + b_linear * 0.1804375
        y = r_linear * 0.2126729 + g_linear * 0.7151522 + b_linear * 0.0721750
        z = r_linear * 0.0193339 + g_linear * 0.1191920 + b_linear * 0.9503041
        return (x * 100, y * 100, z * 100)

    @staticmethod
    def _XYZ_to_LAB(x: float, y: float, z: float) -> Tuple[float, float, float]:
        """XYZ转LAB"""
        refX = 95.047
        refY = 100.000
        refZ = 108.883
        xx = x / refX
        yy = y / refY
        zz = z / refZ

        xx = xx ** (1 / 3) if xx > 0.008856 else (7.787 * xx) + (16 / 116)
        yy = yy ** (1 / 3) if yy > 0.008856 else (7.787 * yy) + (16 / 116)
        zz = zz ** (1 / 3) if zz > 0.008856 else (7.787 * zz) + (16 / 116)

        L = 116 * yy - 16
        a = 500 * (xx - yy)
        b = 200 * (yy - zz)
        return (L, a, b)

    @staticmethod
    def calculate_cielab_delta_e(r1: float, g1: float, b1: float,
                                  r2: float, g2: float, b2: float) -> str:
        """计算CIELAB ΔE*ab 色差"""
        xyz1 = ColorCore._sRGB_to_XYZ(r1, g1, b1)
        xyz2 = ColorCore._sRGB_to_XYZ(r2, g2, b2)
        lab1 = ColorCore._XYZ_to_LAB(*xyz1)
        lab2 = ColorCore._XYZ_to_LAB(*xyz2)

        deltaL = lab1[0] - lab2[0]
        deltaA = lab1[1] - lab2[1]
        deltaB = lab1[2] - lab2[2]
        deltaE = math.sqrt(deltaL * deltaL + deltaA * deltaA + deltaB * deltaB)
        return f"{deltaE:.2f}"

    @staticmethod
    def calculate_ciede2000(r1: float, g1: float, b1: float,
                             r2: float, g2: float, b2: float) -> str:
        """计算CIEDE2000 ΔE00 色差"""
        xyz1 = ColorCore._sRGB_to_XYZ(r1, g1, b1)
        xyz2 = ColorCore._sRGB_to_XYZ(r2, g2, b2)
        lab1 = ColorCore._XYZ_to_LAB(*xyz1)
        lab2 = ColorCore._XYZ_to_LAB(*xyz2)

        L1, a1, b1_lab = lab1
        L2, a2, b2_lab = lab2

        C1 = math.sqrt(a1 * a1 + b1_lab * b1_lab)
        C2 = math.sqrt(a2 * a2 + b2_lab * b2_lab)
        C_avg = (C1 + C2) / 2.0
        G = 0.5 * (1.0 - math.sqrt(C_avg ** 7 / (C_avg ** 7 + 25 ** 7)))

        a1_prime = a1 * (1.0 + G)
        a2_prime = a2 * (1.0 + G)
        C1_prime = math.sqrt(a1_prime * a1_prime + b1_lab * b1_lab)
        C2_prime = math.sqrt(a2_prime * a2_prime + b2_lab * b2_lab)

        h1_prime = math.atan2(b1_lab, a1_prime)
        h2_prime = math.atan2(b2_lab, a2_prime)
        h1_prime = h1_prime if h1_prime >= 0 else h1_prime + 2 * math.pi
        h2_prime = h2_prime if h2_prime >= 0 else h2_prime + 2 * math.pi
        h1_prime_deg = h1_prime * 180.0 / math.pi
        h2_prime_deg = h2_prime * 180.0 / math.pi

        deltaL_prime = L2 - L1
        deltaC_prime = C2_prime - C1_prime

        if C1_prime * C2_prime == 0:
            delta_h_prime = 0.0
        else:
            delta_h_prime = h2_prime_deg - h1_prime_deg
            if delta_h_prime > 180:
                delta_h_prime -= 360
            elif delta_h_prime < -180:
                delta_h_prime += 360

        deltaH_prime = 2.0 * math.sqrt(C1_prime * C2_prime) * math.sin(math.radians(delta_h_prime) / 2.0)

        L_prime_avg = (L1 + L2) / 2.0
        C_prime_avg = (C1_prime + C2_prime) / 2.0

        if C1_prime * C2_prime == 0:
            h_prime_avg = 0.0
        else:
            h_prime_avg = (h1_prime_deg + h2_prime_deg) / 2.0
            if abs(h1_prime_deg - h2_prime_deg) > 180:
                h_prime_avg += 180
            if h_prime_avg > 360:
                h_prime_avg -= 360

        T = (1.0 - 0.17 * math.cos(math.radians(h_prime_avg - 30))
             + 0.24 * math.cos(math.radians(2 * h_prime_avg))
             + 0.32 * math.cos(math.radians(3 * h_prime_avg + 6))
             - 0.20 * math.cos(math.radians(4 * h_prime_avg - 63)))

        SL = 1.0 + (0.015 * (L_prime_avg - 50) ** 2) / math.sqrt(20 + (L_prime_avg - 50) ** 2)
        SC = 1.0 + 0.045 * C_prime_avg
        SH = 1.0 + 0.015 * C_prime_avg * T

        RC = 2.0 * math.sqrt(C_prime_avg ** 7 / (C_prime_avg ** 7 + 25 ** 7))
        deltaTheta = 30.0 * math.exp(-((h_prime_avg - 275) / 25.0) ** 2)
        RT = -math.sin(math.radians(2 * deltaTheta)) * RC

        deltaE00 = math.sqrt(
            (deltaL_prime / SL) ** 2
            + (deltaC_prime / SC) ** 2
            + (deltaH_prime / SH) ** 2
            + RT * (deltaC_prime / SC) * (deltaH_prime / SH)
        )
        return f"{deltaE00:.2f}"

    # ---------- 对比度评估 ----------

    @staticmethod
    def evaluate_wcag21(ratio: Union[str, float]) -> ContrastEvaluation:
        """评估WCAG 2.1对比度等级"""
        num = float(ratio)
        if num >= 7.0:
            return ContrastEvaluation("AAA级", "#4CAF50", "最高可访问性等级，适合小文本和所有用户")
        if num >= 4.5:
            return ContrastEvaluation("AA级", "#8BC34A", "标准可访问性要求，适合普通文本")
        if num >= 3.0:
            return ContrastEvaluation("大文本AA级", "#FFC107", "仅适合大文本（≥18pt或≥24px）")
        return ContrastEvaluation("不足", "#F44336", "不符合可访问性标准")

    @staticmethod
    def evaluate_apca(lc_value: float) -> ContrastEvaluation:
        """评估APCA对比度等级"""
        if lc_value >= 75:
            return ContrastEvaluation("优秀", "#4CAF50", "色块对比强烈，清晰可辨")
        if lc_value >= 60:
            return ContrastEvaluation("良好", "#8BC34A", "色块对比良好，易于区分")
        if lc_value >= 45:
            return ContrastEvaluation("合格", "#FFC107", "色块对比合格，基本可辨")
        if lc_value >= 30:
            return ContrastEvaluation("弱", "#FF9800", "色块对比偏弱，可能难以区分")
        return ContrastEvaluation("极弱", "#F44336", "色块对比极弱，难以区分")

    @staticmethod
    def evaluate_delta_e(deltaE_value: Union[str, float]) -> ContrastEvaluation:
        """评估ΔE色差等级"""
        num = float(deltaE_value)
        if num <= 2.0:
            return ContrastEvaluation("人眼不可辨", "#4CAF50", "颜色差异极小，人眼无法区分")
        if num <= 10.0:
            return ContrastEvaluation("微小差异", "#8BC34A", "颜色差异微小，仔细观察可辨")
        if num <= 49.0:
            return ContrastEvaluation("明显差异", "#FFC107", "颜色差异明显，易于区分")
        if num <= 100.0:
            return ContrastEvaluation("较大差异", "#FF9800", "颜色差异较大，对比强烈")
        return ContrastEvaluation("极大差异", "#F44336", "颜色差异极大，完全不同")

    # ---------- 综合对比度计算 ----------

    @staticmethod
    def calculate_all_contrasts(color1_input: str, color2_input: str) -> Dict[str, Any]:
        """计算两种颜色的所有对比度"""
        rgb1 = ColorCore.parse_color_input(color1_input)
        rgb2 = ColorCore.parse_color_input(color2_input)

        # WCAG 2.1
        wcag_ratio = ColorCore.calculate_wcag21_contrast(
            rgb1.r, rgb1.g, rgb1.b, rgb2.r, rgb2.g, rgb2.b
        )
        wcag_eval = ColorCore.evaluate_wcag21(wcag_ratio)

        # APCA
        apca_value = ColorCore.calculate_apca_contrast(
            rgb1.r, rgb1.g, rgb1.b, rgb2.r, rgb2.g, rgb2.b
        )
        apca_eval = ColorCore.evaluate_apca(apca_value)

        # CIELAB
        cielab_value = ColorCore.calculate_cielab_delta_e(
            rgb1.r, rgb1.g, rgb1.b, rgb2.r, rgb2.g, rgb2.b
        )
        cielab_eval = ColorCore.evaluate_delta_e(cielab_value)

        # CIEDE2000
        ciede2000_value = ColorCore.calculate_ciede2000(
            rgb1.r, rgb1.g, rgb1.b, rgb2.r, rgb2.g, rgb2.b
        )
        ciede2000_eval = ColorCore.evaluate_delta_e(ciede2000_value)

        return {
            "color1": color1_input,
            "color2": color2_input,
            "hex1": ColorCore.rgb_to_hex(rgb1.r, rgb1.g, rgb1.b),
            "hex2": ColorCore.rgb_to_hex(rgb2.r, rgb2.g, rgb2.b),
            "wcag2": {
                "value": f"{wcag_ratio}:1",
                "level": wcag_eval.level,
                "color": wcag_eval.color,
                "description": wcag_eval.description,
                "pass": float(wcag_ratio) >= 4.5
            },
            "apca": {
                "value": apca_value,
                "level": apca_eval.level,
                "color": apca_eval.color,
                "description": apca_eval.description,
                "pass": apca_value >= 45
            },
            "cielab": {
                "value": cielab_value,
                "level": cielab_eval.level,
                "color": cielab_eval.color,
                "description": cielab_eval.description,
                "pass": float(cielab_value) <= 10
            },
            "ciede2000": {
                "value": ciede2000_value,
                "level": ciede2000_eval.level,
                "color": ciede2000_eval.color,
                "description": ciede2000_eval.description,
                "pass": float(ciede2000_value) <= 5
            }
        }

    # ---------- 工具函数 ----------

    @staticmethod
    def is_valid_hex(color: str) -> bool:
        """验证十六进制颜色字符串是否有效"""
        if not isinstance(color, str):
            return False
        return bool(re.match(r'^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', color))

    @staticmethod
    def generate_random_color() -> str:
        """生成随机颜色"""
        h = random.random() * 360
        s = 50 + random.random() * 40
        l = 40 + random.random() * 30
        rgb = ColorCore.hsl_to_rgb(h, s, l)
        return ColorCore.rgb_to_hex(rgb.r, rgb.g, rgb.b)


# ============ 便捷函数 ============

def convert_color(color_input: str) -> Dict[str, Any]:
    """转换颜色到所有格式"""
    info = ColorCore.get_full_color_info(color_input)
    return info.to_dict()


def get_contrast(color1: str, color2: str, algorithm: str = "all") -> Dict[str, Any]:
    """计算对比度"""
    if algorithm == "all":
        return ColorCore.calculate_all_contrasts(color1, color2)
    elif algorithm == "wcag2":
        rgb1 = ColorCore.parse_color_input(color1)
        rgb2 = ColorCore.parse_color_input(color2)
        ratio = ColorCore.calculate_wcag21_contrast(rgb1.r, rgb1.g, rgb1.b, rgb2.r, rgb2.g, rgb2.b)
        eval_result = ColorCore.evaluate_wcag21(ratio)
        return {
            "algorithm": "WCAG 2.1",
            "value": f"{ratio}:1",
            "evaluation": eval_result.to_dict()
        }
    elif algorithm == "apca":
        rgb1 = ColorCore.parse_color_input(color1)
        rgb2 = ColorCore.parse_color_input(color2)
        value = ColorCore.calculate_apca_contrast(rgb1.r, rgb1.g, rgb1.b, rgb2.r, rgb2.g, rgb2.b)
        eval_result = ColorCore.evaluate_apca(value)
        return {
            "algorithm": "APCA",
            "value": value,
            "evaluation": eval_result.to_dict()
        }
    elif algorithm == "cielab":
        rgb1 = ColorCore.parse_color_input(color1)
        rgb2 = ColorCore.parse_color_input(color2)
        value = ColorCore.calculate_cielab_delta_e(rgb1.r, rgb1.g, rgb1.b, rgb2.r, rgb2.g, rgb2.b)
        eval_result = ColorCore.evaluate_delta_e(value)
        return {
            "algorithm": "CIELAB ΔE*ab",
            "value": value,
            "evaluation": eval_result.to_dict()
        }
    elif algorithm == "ciede2000":
        rgb1 = ColorCore.parse_color_input(color1)
        rgb2 = ColorCore.parse_color_input(color2)
        value = ColorCore.calculate_ciede2000(rgb1.r, rgb1.g, rgb1.b, rgb2.r, rgb2.g, rgb2.b)
        eval_result = ColorCore.evaluate_delta_e(value)
        return {
            "algorithm": "CIEDE2000",
            "value": value,
            "evaluation": eval_result.to_dict()
        }
    else:
        raise ValueError(f"不支持的算法: {algorithm}")


def get_complementary(color_input: str) -> Dict[str, Any]:
    """获取互补色"""
    rgb = ColorCore.parse_color_input(color_input)
    comp_rgb = ColorCore.calculate_complementary_color(rgb.r, rgb.g, rgb.b)
    return {
        "original": ColorCore.rgb_to_hex(rgb.r, rgb.g, rgb.b),
        "complementary": ColorCore.rgb_to_hex(comp_rgb.r, comp_rgb.g, comp_rgb.b),
        "original_rgb": rgb.to_dict(),
        "complementary_rgb": comp_rgb.to_dict()
    }


def get_palette(color_input: str, palette_type: str = "triadic") -> Dict[str, Any]:
    """获取调色板"""
    rgb = ColorCore.parse_color_input(color_input)
    if palette_type == "triadic":
        colors = ColorCore.get_triadic_colors(rgb.r, rgb.g, rgb.b)
    elif palette_type == "tetradic":
        colors = ColorCore.get_tetradic_colors(rgb.r, rgb.g, rgb.b)
    elif palette_type == "analogous":
        colors = ColorCore.get_analogous_colors(rgb.r, rgb.g, rgb.b)
    elif palette_type == "complementary":
        comp = ColorCore.calculate_complementary_color(rgb.r, rgb.g, rgb.b)
        colors = [ColorCore.rgb_to_hex(rgb.r, rgb.g, rgb.b),
                  ColorCore.rgb_to_hex(comp.r, comp.g, comp.b)]
    else:
        raise ValueError(f"不支持的调色板类型: {palette_type}")

    return {
        "type": palette_type,
        "colors": colors,
        "count": len(colors)
    }


if __name__ == "__main__":
    # 测试
    print("=== 颜色转换测试 ===")
    result = convert_color("#3498db")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print("\n=== 对比度计算测试 ===")
    contrast = get_contrast("#000000", "#ffffff")
    print(json.dumps(contrast, indent=2, ensure_ascii=False))
