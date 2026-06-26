"""电气图库 - 开关、插座、灯具、线路符号"""
import math
from typing import Tuple


class ElectricalTemplates:
    """电气制图标准组件"""

    @staticmethod
    def switch_single_pole(msp, position: tuple,
                           orientation: str = 'vertical',
                           size: float = 200,
                           layer: str = 'symbol', color: int = 1):
        """单极开关（标准符号）"""
        from entities.basic import BasicEntities
        from entities.curves import CurveEntities

        cx, cy = position; s = size; hs = s/2; qs = s*0.15
        ents = []

        is_v = orientation == 'vertical'

        # 圆（触点）
        ents.append(CurveEntities.circle(msp, (cx,cy), qs*2, layer=layer, color=color))

        if is_v:
            # 上引线
            ents.append(BasicEntities.line(msp, (cx,cy+qs*2), (cx,cy+hs), layer='wire', color=7))
            # 下引线
            ents.append(BasicEntities.line(msp, (cx,cy-qs*2), (cx,cy-hs), layer='wire', color=7))
            # 动触点杆（倾斜45°）
            ents.append(BasicEntities.line(msp, (cx,cy-qs*2), (cx+hs*0.3, cy+hs*0.1),
                                           layer=layer, color=color))
        else:
            ents.append(BasicEntities.line(msp, (cx-qs*2,cy), (cx-hs,cy), layer='wire', color=7))
            ents.append(BasicEntities.line(msp, (cx+qs*2,cy), (cx+hs,cy), layer='wire', color=7))
            ents.append(BasicEntities.line(msp, (cx+qs*2,cy), (cx+hs*0.1, cy+hs*0.3),
                                           layer=layer, color=color))

        return ents

    @staticmethod
    def socket_power(msp, position: tuple,
                     type: str = 'three_hole',
                     size: float = 150,
                     layer: str = 'device'):
        """电源插座"""
        from entities.basic import BasicEntities
        from entities.curves import CurveEntities

        cx, cy = position; s = size; hs = s/2
        ents = []

        # 外框半圆或方框
        if type == 'three_hole':
            # 半圆弧 + 底线（两孔+三孔通用外形）
            ents.append(CurveEntities.arc(msp, (cx,cy-s*0.2), hs,
                                          -90, 270, layer=layer, color=3))
            ents.append(BasicEntities.line(msp, (cx-hs,cy-s*0.2), (cx+hs,cy-s*0.2),
                                           layer=layer, color=3))
            # 孔位示意：上二下一（三孔）
            hole_r = s * 0.08
            gap = s * 0.25
            ents.append(CurveEntities.circle(msp, (cx-gap, cy+s*0.05), hole_r, layer=layer, color=7))
            ents.append(CurveEntities.circle(msp, (cx+gap, cy+s*0.05), hole_r, layer=layer, color=7))
            ents.append(CurveEntities.circle(msp, (cx, cy-s*0.12), hole_r, layer=layer, color=7))
        else:
            # 两孔方形插座
            from entities.polyline import PolylineEntity
            PolylineEntity.rect_centered(msp, (cx,cy), s*0.9, s*0.65, layer=layer, color=3)

        return ents

    @staticmethod
    def lamp_ceiling(msp, position: tuple,
                    lamp_type: str = 'downlight',
                    size: float = 120,
                    layer: str = 'device'):
        """灯具符号"""
        from entities.basic import BasicEntities
        from entities.curves import CurveEntities

        cx, cy = position; r = size/2
        ents = []

        types_map = {
            'downlight':   ('circle', 1),
            'ceiling_lamp':('circle_cross', 1),
            'fluorescent': ('rect', 2),     # 长条灯
            'wall_lamp':   ('half_circle', 1),  # 壁灯
            'track':       ('track', 1),      # 轨道射灯
        }

        shape = types_map.get(lamp_type, ('circle', 1))[0]

        if shape == 'circle':
            ents.append(CurveEntities.circle(msp, (cx,cy), r, layer=layer, color=3))
        elif shape == 'circle_cross':
            ents.append(CurveEntities.circle(msp, (cx,cy), r, layer=layer, color=3))
            tick = r * 0.6
            ents.append(BasicEntities.line(msp, (cx-tick,cy),(cx+tick,cy), layer=layer, color=3))
            ents.append(BasicEntities.line(msp, (cx,cy-tick),(cx,cy+tick), layer=layer, color=3))
        elif shape == 'rect':
            from entities.polyline import PolylineEntity
            w = size * 2; h = size * 0.35
            ents.append(PolylineEntity.rect_centered(msp, (cx,cy), w, h, layer=layer, color=3))
        elif shape == 'half_circle':
            ents.append(CurveEntities.arc(msp, (cx,cy), r, 0, 180, layer=layer, color=3))
            ents.append(BasicEntities.line(msp, (cx-r,cy), (cx+r,cy), layer=layer, color=3))

        return ents

    @staticmethod
    def wire_line(msp, start: tuple, end: tuple,
                  phases: int = 3,
                  spacing: float = 30,
                  layer: str = 'wire'):
        """多相导线组（平行线表示）"""
        from entities.basic import BasicEntities

        dx, dy = end[0]-start[0], end[1]-start[1]
        length = math.sqrt(dx*dx + dy*dy)
        ux, uy = dx/length, dy/length
        nx, ny = -uy, ux

        half_gap = spacing * (phases - 1) / 2
        ents = []
        for i in range(phases):
            offset = -half_gap + i * spacing
            ox, oy = offset * nx, offset * ny
            ents.append(BasicEntities.line(msp,
                (start[0]+ox, start[1]+oy),
                (end[0]+ox, end[1]+oy),
                layer=layer, color=7, lineweight=18))
        return ents

    @staticmethod
    def distribution_box(msp, center: tuple,
                         width: float = 400,
                         height: float = 300,
                         label: str = '',
                         layer: str = 'device'):
        """配电箱/控制箱"""
        from entities.polyline import PolylineEntity
        from entities.text import TextEntity

        cx, cy = center; hw, hh = width/2, height/2
        ents = [PolylineEntity.rect_centered(msp, (cx,cy), width, height,
                                             layer=layer, color=3, lineweight=40)]
        if label:
            ents.append(TextEntity.text(msp, label, (cx, cy),
                                       height=min(width,height)*0.18,
                                       halign='CENTER', valign='MIDDLE',
                                       layer=layer, color=7))
        return ents

    @staticmethod
    def circuit_breaker(msp, position: tuple,
                        orientation: str = 'horizontal',
                        poles: int = 1,
                        layer: str = 'device'):
        """断路器符号"""
        from entities.basic import BasicEntities

        cx, cy = position; s = 150
        ents = []

        for p in range(poles):
            offset_y = p * s * 1.5
            px, py = cx, cy + offset_y

            is_h = orientation != 'vertical'
            line_len = s * 0.6

            if is_h:
                ents.append(BasicEntities.line(msp, (px-line_len,py), (px-line_len*0.2,py),
                                               layer='wire', color=7))
                ents.append(BasicEntities.line(msp, (px+line_len*0.2,py), (px+line_len,py),
                                               layer='wire', color=7))
                # 断开触点
                ents.append(BasicEntities.line(msp, (px-line_len*0.2,py),
                                               (px+line_len*0.2, py+s*0.2),
                                               layer='device', color=3))
                # 触点圆
                from entities.curves import CurveEntities
                ents.append(CurveEntities.circle(msp, (px-line_len*0.2, py), s*0.04,
                                                  layer='device', color=3))

        return ents
