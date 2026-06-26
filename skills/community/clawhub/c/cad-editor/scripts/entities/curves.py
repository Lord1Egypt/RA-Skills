"""曲线图元 - 圆、圆弧、椭圆、样条曲线"""
from typing import Tuple, Optional
import math


class CurveEntities:
    """曲线类图元操作"""

    # ━━━━━━━━━ 圆 ━━━━━━━━━

    @staticmethod
    def circle(msp,
               center: Tuple[float, float],
               radius: float,
               layer: str = '0',
               color: int = 7,
               lineweight: int = 35):
        """
        画圆
        
        Args:
            msp: 模型空间
            center: 圆心坐标 (x, y)
            radius: 半径
        """
        return msp.add_circle(
            (center[0], center[1], 0), radius,
            dxfattribs={'layer': layer, 'color': color, 'lineweight': lineweight}
        )

    @staticmethod
    def circle_2p(msp, p1: Tuple[float, float], p2: Tuple[float, float],
                  layer: str = '0', color: int = 7):
        """两点定圆（两点为直径两端）"""
        cx = (p1[0] + p2[0]) / 2
        cy = (p1[1] + p2[1]) / 2
        radius = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) / 2
        return CurveEntities.circle(msp, (cx, cy), radius, layer, color)

    @staticmethod
    def circle_3p(msp, p1, p2, p3, layer='0', color=7):
        """三点定圆"""
        ax, ay = p1; bx, by = p2; cx, cy = p3
        D = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        if abs(D) < 1e-10:
            raise ValueError("三点共线，无法确定圆")
        ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / D
        uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / D
        r = math.sqrt((ax - ux)**2 + (ay - uy)**2)
        return CurveEntities.circle(msp, (ux, uy), r, layer, color)

    @staticmethod
    def concentric_circles(msp, center, radii: list, layer='0', color=7):
        """同心圆组"""
        return [CurveEntities.circle(msp, center, r, layer, color) for r in radii]

    # ━━━━━━━━━ 弧 ━━━━━━━━━

    @staticmethod
    def arc(msp,
            center: Tuple[float, float],
            radius: float,
            start_angle: float,   # 度
            end_angle: float,     # 度
            layer: str = '0',
            color: int = 7,
            lineweight: int = 35):
        """
        画圆弧
        
        Args:
            start_angle: 起始角度（度）
            end_angle: 终止角度（度）
        """
        return msp.add_arc(
            (center[0], center[1], 0), radius,
            start_angle, end_angle,
            dxfattribs={'layer': layer, 'color': color, 'lineweight': lineweight}
        )

    # ━━━━━━━━━ 椭圆 ━━━━━━━━━

    @staticmethod
    def ellipse(msp,
                center: Tuple[float, float],
                major_axis: Tuple[float, float],  # 长轴端点向量
                ratio: float,                     # 短轴与长轴比 (0-1)
                start_angle: float = 0,
                end_angle: float = 360,
                layer: str = '0',
                color: int = 7):
        """
        画椭圆
        
        Args:
            major_axis: 从圆心到长轴端点的向量
            ratio: 短轴/长轴比例
        """
        return msp.add_ellipse(
            (center[0], center[1], 0),
            (major_axis[0], major_axis[1], 0),
            ratio, start_angle, end_angle,
            dxfattribs={'layer': layer, 'color': color}
        )
