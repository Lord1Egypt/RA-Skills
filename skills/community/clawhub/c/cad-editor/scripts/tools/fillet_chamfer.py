"""圆角与倒角工具"""
import math
from typing import Tuple


class FilletChamfer:
    """圆角和倒角"""

    @staticmethod
    def fillet_two_lines(msp,
                         p_common: tuple,
                         p1_end: tuple,
                         p2_end: tuple,
                         radius: float,
                         layer='0', color=7):
        """
        两条线的公共顶点处做圆角（简化版：用弧替换尖角）
        
        Args:
            p_common: 两条线的公共交点
            p1_end: 第一条线的另一端
            p2_end: 第二条线的另一端
            radius: 圆角半径
        """
        from entities.curves import CurveEntities
        from entities.basic import BasicEntities
        
        # 计算两边的方向向量
        v1 = (p1_end[0] - p_common[0], p1_end[1] - p_common[1])
        v2 = (p2_end[0] - p_common[0], p2_end[1] - p_common[1])
        
        l1 = math.sqrt(v1[0]**2 + v1[1]**2)
        l2 = math.sqrt(v2[0]**2 + v2[1]**2)
        
        if l1 < 1e-6 or l2 < 1e-6 or radius < 1e-6:
            return None
            
        u1 = (v1[0]/l1, v1[1]/l1)
        u2 = (v2[0]/l2, v2[1]/l2)
        
        # 两向量的夹角
        dot = u1[0]*u2[0] + u1[1]*u2[1]
        angle = math.acos(max(-1, min(1, dot)))
        
        # 圆弧切点距公共点的距离
        tangent_dist = radius / math.tan(angle / 2)
        
        # 切点坐标
        t1 = (p_common[0] + u1[0] * tangent_dist, p_common[1] + u1[1] * tangent_dist)
        t2 = (p_common[0] + u2[0] * tangent_dist, p_common[1] + u2[1] * tangent_dist)
        
        # 圆弧中心（沿角平分线方向）
        bisect_x = u1[0] + u2[0]
        bisect_y = u1[1] + u2[1]
        bl = math.sqrt(bisect_x**2 + bisect_y**2)
        if bl < 1e-6:
            return None
            
        center_dist = radius / math.sin(angle / 2)
        cx = p_common[0] + (bisect_x/bl) * center_dist
        cy = p_common[1] + (bisect_y/bl) * center_dist
        
        # 确定圆弧起止角度
        a1 = math.degrees(math.atan2(t1[1]-cy, t1[0]-cx))
        a2 = math.degrees(math.atan2(t2[1]-cy, t2[0]-cx))
        
        # 绘制圆弧
        arc = CurveEntities.arc(msp, (cx, cy), radius, a1, a2, 
                                layer=layer, color=color)
        
        return {
            'arc': arc,
            'tangent_1': t1,
            'tangent_2': t2,
            'center': (cx, cy),
        }

    @staticmethod
    def chamfer_two_lines(p_common: tuple, p1_end: tuple, p2_end: tuple,
                          distance_a: float, distance_b: float = None):
        """
        两条线的公共顶点处做倒角
        
        Args:
            distance_a: 第一条线上的倒角距离
            distance_b: 第二条线上的倒角距离（None=等于a）
        
        Returns:
            (倒角点1, 倒角点2)
        """
        if distance_b is None:
            distance_b = distance_a
            
        import math
        
        v1 = (p1_end[0] - p_common[0], p1_end[1] - p_common[1])
        v2 = (p2_end[0] - p_common[0], p2_end[1] - p_common[1])
        
        l1 = math.sqrt(v1[0]**2 + v1[1]**2)
        l2 = math.sqrt(v2[0]**2 + v2[1]**2)
        
        if l1 < 1e-6 or l2 < 1e-6:
            return (None, None)
            
        c1 = (p_common[0] + v1[0]/l1 * distance_a,
              p_common[1] + v1[1]/l1 * distance_a)
        c2 = (p_common[0] + v2[0]/l2 * distance_b,
              p_common[1] + v2[1]/l2 * distance_b)
              
        return (c1, c2)

    @staticmethod
    def chamfer_polygon(msp, points: list, distance: float,
                        layer='0', color=7):
        """
        多边形所有顶点做倒角
        
        Returns:
            倒角后的新顶点列表
        """
        from entities.basic import BasicEntities
        
        n = len(points)
        new_points = []
        
        for i in range(n):
            prev_pt = points[i-1]
            curr_pt = points[i]
            next_pt = points[(i+1) % n]
            
            c1, c2 = FilletChamfer.chamfer_two_lines(
                curr_pt, prev_pt, next_pt, distance, distance
            )
            new_points.append(c2 if c2 else curr_pt)
            
        # 画倒角后的轮廓
        from entities.polyline import PolylineEntity
        return PolylineEntity.polygon(msp, new_points, layer=layer, color=color)
