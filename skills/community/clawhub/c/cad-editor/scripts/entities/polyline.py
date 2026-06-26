"""多段线 - 折线、矩形、多边形、带宽度多段线"""
from typing import Tuple, List, Optional


class PolylineEntity:
    """多段线操作"""

    @staticmethod
    def polyline(msp,
                 points: List[Tuple[float, float]],
                 closed: bool = False,
                 layer: str = '0',
                 color: int = 7,
                 lineweight: int = 35,
                 start_width: float = 0,
                 end_width: float = 0,
                 const_width: float = 0):
        """
        优化多段线 (LWPOLYLINE)
        
        Args:
            points: 顶点坐标列表 [(x,y), ...]
            closed: 是否闭合
            const_width: 全局恒定宽度（覆盖 start/end_width）
        """
        if len(points) < 2:
            raise ValueError("至少需要2个点")
        
        if const_width > 0:
            start_width = const_width
            end_width = const_width
        
        dxfattribs = {
            'layer': layer,
            'color': color,
            'lineweight': lineweight,
        }
        
        pts_2d = [(p[0], p[1]) for p in points]
        pline = msp.add_lwpolyline(pts_2d, format='xy', close=closed,
                                   dxfattribs=dxfattribs)
        
        if start_width > 0 or end_width > 0:
            try:
                pline.set_const_width(const_width) if const_width > 0 else None
                pline.set_start_width(start_width)
                pline.set_end_width(end_width)
            except Exception:
                pass
                
        return pline

    @staticmethod
    def rectangle(msp,
                  corner1: Tuple[float, float],
                  corner2: Tuple[float, float],
                  layer: str = '0',
                  color: int = 7,
                  filled: bool = False,
                  **kwargs):
        """
        矩形（闭合多段线）
        
        Args:
            corner1: 左下角 (x, y)
            corner2: 右上角 (x, y)
        """
        x1, y1 = corner1
        x2, y2 = corner2
        points = [
            (x1, y1), (x2, y1), (x2, y2), (x1, y2)
        ]
        return PolylineEntity.polyline(msp, points, closed=True,
                                        layer=layer, color=color)

    @staticmethod
    def rectangle_centered(msp,
                           center: Tuple[float, float],
                           width: float,
                           height: float,
                           layer: str = '0',
                           color: int = 7,
                           **kwargs):
        """以中心点画矩形"""
        x, y = center
        hw, hh = width / 2, height / 2
        return PolylineEntity.rectangle(msp, (x-hw, y-hh), (x+hw, y+hh),
                                         layer=layer, color=color)

    @staticmethod
    def polygon(msp,
                points: List[Tuple[float, float]],
                layer: str = '0',
                color: int = 7,
                **kwargs):
        """任意多边形（自动闭合）"""
        if len(points) < 3:
            raise ValueError("至少需要3个点构成多边形")
        return PolylineEntity.polyline(msp, points, closed=True,
                                        layer=layer, color=color)

    @staticmethod
    def regular_polygon(msp,
                        center: Tuple[float, float],
                        radius: float,
                        sides: int,
                        rotation: float = 0,
                        layer: str = '0',
                        color: int = 7):
        """
        正多边形
        
        Args:
            sides: 边数 (3=三角形, 4=正方形, 5=五边形, 6=六边形...)
            rotation: 初始旋转角（度），0=第一个点在右侧
        """
        import math
        if sides < 3:
            raise ValueError("边数必须>=3")
        points = []
        for i in range(sides):
            angle = math.radians(rotation + i * 360 / sides)
            px = center[0] + radius * math.cos(angle)
            py = center[1] + radius * math.sin(angle)
            points.append((px, py))
        return PolylineEntity.polygon(msp, points, layer=layer, color=color)

    @staticmethod
    def slot(msp,
             center: Tuple[float, float],
             length: float,       # 长度方向总长
             width: float,        # 端部圆直径
             angle: float = 0,    # 旋转角（度）
             layer: str = '0',
             color: int = 7):
        """
        键槽形（跑道形）
        由两条平行线+两个半圆组成
        """
        import math
        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        half_len = length / 2 - width / 2
        r = width / 2
        
        # 计算四个关键点（相对于中心，已旋转）
        def rotate(px, py):
            rx = px * cos_a - py * sin_a + center[0]
            ry = px * sin_a + py * cos_a + center[1]
            return (rx, ry)
        
        p1 = rotate(-half_len, -r)
        p2 = rotate(-half_len, r)
        p3 = rotate(half_len, r)
        p4 = rotate(half_len, -r)
        
        # 用多段线画出整个轮廓
        from .curves import CurveEntities
        entities = []
        entities.append(PolylineEntity.polyline(msp, [p1, p4], layer=layer, color=color))
        entities.append(CurveEntities.arc(msp, rotate(half_len, 0), r, -90, 90, layer=layer, color=color))
        entities.append(PolylineEntity.polyline(msp, [p3, p2], layer=layer, color=color))
        entities.append(CurveEntities.arc(msp, rotate(-half_len, 0), r, 90, 270, layer=layer, color=color))
        return entities
