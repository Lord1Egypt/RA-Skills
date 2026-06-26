"""机械图库 - 螺钉、齿轮、轴承、键槽、弹簧、标准件"""
import math
from typing import Tuple


class MechanicalTemplates:
    """机械制图标准组件"""

    @staticmethod
    def bolt_top_view(msp, center: tuple, diameter: float,
                      head_type: str = 'hex',
                      layer: str = 'outline', color: int = 7):
        """
        螺栓头俯视图
        Args:
            head_type: 'hex'六角 / 'phillips'十字 / 'slot'一字
        """
        from entities.basic import BasicEntities
        from entities.curves import CurveEntities
        from entities.polyline import PolylineEntity

        cx, cy = center; d = diameter; r = d/2
        ents = []

        if head_type == 'hex':
            # 六角头（正六边形）
            for i in range(6):
                a1 = math.radians(60 * i)
                a2 = math.radians(60 * (i+1))
                p1 = (cx + r*math.cos(a1), cy + r*math.sin(a1))
                p2 = (cx + r*math.cos(a2), cy + r*math.sin(a2))
                ents.append(BasicEntities.line(msp, p1, p2, layer=layer, color=color))

            # 内切圆
            ents.append(CurveEntities.circle(msp, center, r*0.866,
                                              layer='thin', color=5))

            # 中心十字线
            tick = r * 0.15
            ents.append(BasicEntities.line(msp, (cx-tick,cy),(cx+tick,cy),
                                           layer='center', color=1, lineweight=13))
            ents.append(BasicEntities.line(msp, (cx,cy-tick),(cx,cy+tick),
                                           layer='center', color=1, lineweight=13))

        elif head_type == 'phillips':
            # 十字槽圆头
            ents.append(CurveEntities.circle(msp, center, r, layer=layer, color=color))
            slot_len = r * 0.8
            for angle in [0, 45]:
                rad = math.radians(angle)
                sx = slot_len * math.cos(rad); sy = slot_len * math.sin(rad)
                ents.append(BasicEntities.line(msp,
                    (cx-sx, cy-sy), (cx+sx, cy+sy),
                    layer='thin', color=5, lineweight=25))

        elif head_type == 'slot':
            # 一字槽圆头
            ents.append(CurveEntities.circle(msp, center, r, layer=layer, color=color))
            ents.append(BasicEntities.line(msp, (cx-r*0.7, cy), (cx+r*0.7, cy),
                                           layer='thin', color=5, lineweight=25))

        return ents

    @staticmethod
    def gear_profile(msp, center: tuple,
                     teeth: int = 20,
                     outer_diameter: float = 100,
                     root_diameter: float = 80,
                     bore_diameter: float = 20,
                     layer: str = 'outline', color: int = 7):
        """齿轮轮廓（端面视图）"""
        from entities.polyline import PolylineEntity
        from entities.curves import CurveEntities

        cx, cy = center
        ro = outer_diameter / 2; rr = root_diameter / 2; rb = bore_diameter / 2
        tooth_angle = 360.0 / teeth
        ents = []

        # 齿顶圆
        ents.append(CurveEntities.circle(msp, center, ro, layer=layer, color=color, lineweight=50))
        # 齿根圆
        ents.append(CurveEntities.circle(msp, center, rr, layer=layer, color=color, lineweight=35))
        # 轴孔
        ents.append(CurveEntities.circle(msp, center, rb, layer='hidden', color=2, lineweight=25))

        # 简化的齿形表示（径向线）
        for i in range(teeth):
            a = math.radians(i * tooth_angle)
            px = cx + ro * math.cos(a)
            py = cy + ro * math.sin(a)
            from entities.basic import BasicEntities
            ents.append(BasicEntities.line(msp, (cx,cy), (px,py),
                                           layer='thin', color=5, lineweight=18))

        return ents

    @staticmethod
    def bearing(msp, center: tuple,
               outer_dia: float = 60,
               inner_dia: float = 30,
               width: float = 15,
               view: str = 'side',
               layer: str = 'outline'):
        """轴承简化画法"""
        from entities.basic import BasicEntities
        from entities.curves import CurveEntities

        cx, cy = center; ro = outer_dia/2; ri = inner_dia/2; rm = (ro+ri)/2
        ents = []

        if view == 'side':
            # 剖面视图：矩形外圈 + 内圈 + 滚子
            hw = width/2
            # 外圈
            ents.extend([
                BasicEntities.line(msp, (cx-hw, cy-ro), (cx+hw, cy-ro), layer=layer, color=7, linewidth=50),
                BasicEntities.line(msp, (cx-hw, cy-rm), (cx+hw, cy-rm), layer=layer, color=7, linewidth=35),
                BasicEntities.line(msp, (cx-hw, cy-ri), (cx+hw, cy-ri), layer=layer, color=7, linewidth=50),
                BasicEntities.line(msp, (cx-hw, cy-ro), (cx-hw, cy-ri), layer=layer, color=7, linewidth=50),
                BasicEntities.line(msp, (cx+hw, cy-ro), (cx+hw, cy-ri), layer=layer, color=7, linewidth=50),
            ])
            # 滚动体示意（小圆）
            ball_r = (ro - rm) / 2.5
            n_balls = max(int(width / (ball_r*4)), 3)
            for i in range(n_balls):
                bx = cx - hw + width*(i+0.5)/n_balls
                ents.append(CurveEntities.circle(msp, (bx, cy-rm-ball_r), ball_r,
                                                  layer='thin', color=5))
        else:
            # 端面视图：同心圆
            ents.append(CurveEntities.circle(msp, center, ro, layer=layer, color=7, lineweight=50))
            ents.append(CurveEntities.circle(msp, center, rm, layer='thin', color=5))
            ents.append(CurveEntities.circle(msp, center, ri, layer=layer, color=7, lineweight=50))

        return ents

    @staticmethod
    def keyway_side_view(msp, shaft_center: tuple,
                         shaft_dia: float = 30,
                         key_width: float = 8,
                         key_length: float = 20,
                         key_depth: float = 4,
                         layer: str = 'outline'):
        """轴和键槽的侧面视图"""
        from entities.basic import BasicEntities
        from entities.curves import CurveEntities
        from entities.polyline import PolylineEntity

        cx, cy = shaft_center; rs = shaft_dia/2; kl = key_length; kw = key_width
        ents = []

        # 轴的外轮廓
        half_kl = kl / 2
        ents.append(BasicEntities.line(msp, (cx-half_kl, cy-rs), (cx+half_kl, cy-rs),
                                       layer=layer, color=7, linewidth=50))
        ents.append(BasicEntities.line(msp, (cx-half_kl, cy+rs), (cx+half_kl, cy+rs),
                                       layer=layer, color=7, linewidth=50))
        # 键槽（底部开口的矩形）
        kh = key_depth
        ents.extend([
            BasicEntities.line(msp, (cx-half_kl, cy+rs-kh), (cx+half_kl, cy+rs-kh),
                               layer=layer, color=7),
            BasicEntities.line(msp, (cx-half_kl, cy+rs-kh), (cx-half_kl, cy+rs),
                               layer=layer, color=7),
            BasicEntities.line(msp, (cx+half_kl, cy+rs-kh), (cx+half_kl, cy+rs),
                               layer=layer, color=7),
        ])
        return ents

    @staticmethod
    def spring_compression(msp, start: tuple, end: tuple,
                           wire_dia: float = 2,
                           coil_outer_dia: float = 16,
                           active_coils: float = 6,
                           end_coils: float = 2,
                           layer: str = 'outline', color: int = 7):
        """压缩弹簧（侧视，锯齿线表示）"""
        from entities.basic import BasicEntities
        import numpy as np

        sx, sy = start; ex, ey = end
        dx, dy = ex-sx, ey-sy
        length = math.sqrt(dx*dx + dy*dy)

        total_coils = active_coils + end_coils
        pitch = length / total_coils
        amp = coil_outer_dia / 2 - wire_dia / 2

        # 单位方向向量
        ux, uy = dx/length, dy/length
        nx, ny = -uy, ux  # 法向

        pts_per_coil = 12
        n_pts = int(total_coils * pts_per_coil)
        points = []
        for i in range(n_pts + 1):
            t = i / n_pts * length
            phase = (i / pts_per_coil) * 2 * math.pi
            offset = amp * math.sin(phase)
            px = sx + ux*t + nx*offset
            py = sy + uy*t + ny*offset
            points.append((px, py))

        return BasicEntities.lines(msp, points, closed=False,
                                   layer=layer, color=color)

    @staticmethod
    def washer(msp, center: tuple,
              outer_dia: float = 10,
              inner_dia: float = 5.5,
              thickness: float = 1.6,
              layer: str = 'thin'):
        """垫圈"""
        from entities.curves import CurveEntities
        return [
            CurveEntities.circle(msp, center, outer_dia/2, layer=layer, color=7),
            CurveEntities.circle(msp, center, inner_dia/2, layer=layer, color=7),
        ]

    @staticmethod
    def nut_hex(msp, center: tuple,
                size_across_flats: float = 10,
                thickness: float = 5,
                thread_dia: float = 9,
                layer: str = 'outline'):
        """六角螺母"""
        from entities.polyline import PolylineEntity
        s = size_across_flats; t = thickness
        cx, cy = center
        apothem = s * 0.866  # 边心距

        pts = []
        for i in range(6):
            a = math.radians(30 + i * 60)
            pts.append((cx + apothem * math.cos(a), cy + apothem * math.sin(a)))

        return [PolylineEntity.polygon(msp, pts, layer=layer, color=7, lineweight=50)]

    @staticmethod
    def pin_cylindrical(msp, start: tuple, end: tuple,
                        dia: float = 4,
                        layer: str = 'thin'):
        """圆柱销"""
        from entities.basic import BasicEntities
        r = dia/2
        dx, dy = end[0]-start[0], end[1]-start[1]
        length = math.sqrt(dx*dx+dy*dy)
        ux, uy = dx/length, dy/length; nx, ny = -uy, ux

        return [
            BasicEntities.line(msp,
                (start[0]+nx*r, start[1]+ny*r),
                (end[0]+nx*r, end[1]+ny*r), layer=layer, color=7),
            BasicEntities.line(msp,
                (start[0]-nx*r, start[1]-ny*r),
                (end[0]-nx*r, end[1]-ny*r), layer=layer, color=7),
        ]
