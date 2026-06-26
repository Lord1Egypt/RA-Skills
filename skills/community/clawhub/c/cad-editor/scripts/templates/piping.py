"""管道图库 - 弯头、三通、阀门、法兰、管件"""
import math
from typing import Tuple


class PipingTemplates:
    """管道/暖通制图标准组件"""

    @staticmethod
    def pipe_straight(msp, start: tuple, end: tuple,
                      diameter: float = 50,
                      layer: str = 'pipe',
                      color: int = 2,
                      show_centerline: bool = True):
        """
        直管段（双线表示）
        
        Args:
            diameter: 管外径
        """
        from entities.basic import BasicEntities
        dx, dy = end[0]-start[0], end[1]-start[1]
        length = math.sqrt(dx*dx+dy*dy)
        r = diameter / 2
        ux, uy = dx/length, dy/length
        nx, ny = -uy, ux

        ents = [
            BasicEntities.line(msp, (start[0]+nx*r, start[1]+ny*r),
                               (end[0]+nx*r, end[1]+ny*r), layer=layer, color=color),
            BasicEntities.line(msp, (start[0]-nx*r, start[1]-ny*r),
                               (end[0]-nx*r, end[1]-ny*r), layer=layer, color=color),
        ]
        if show_centerline:
            cl_offset = diameter * 0.02
            ents.append(BasicEntities.line(msp, start, end,
                                           layer='center', color=1, lineweight=13))
        return ents

    @staticmethod
    def elbow_90(msp, center: tuple, radius: float = 100,
                 diameter: float = 50, angle_dir: str = 'NE',
                 layer: str = 'fitting'):
        """
        90度弯头
        
        Args:
            center: 弯曲中心
            angle_dir: 走向方向 'NE'/'NW'/'SE'/'SW'（从哪个方向来，到哪个方向去）
        Returns:
            双线弯头实体列表
        """
        from entities.curves import CurveEntities
        r = diameter / 2
        R = radius

        dir_angles = {
            'NE': (-180, -90), 'NW': (-90, 0), 'SE': (90, 180), 'SW': (0, 90),
        }
        a_start, a_end = dir_angles.get(angle_dir, (-180,-90))
        ents = []

        # 外弧和内弧
        Ro = R + r; Ri = max(R - r, 1)
        try:
            ents.append(CurveEntities.arc(msp, center, Ro, a_start, a_end, layer=layer, color=5))
            ents.append(CurveEntities.arc(msp, center, Ri, a_start, a_end, layer=layer, color=5))

            # 连接线（端部封口）
            rad_s = math.radians(a_start); rad_e = math.radians(a_end)
            from entities.basic import BasicEntities
            ents.append(BasicEntities.line(msp,
                (center[0]+Ro*math.cos(rad_s), center[1]+Ro*math.sin(rad_s)),
                (center[0]+Ri*math.cos(rad_s), center[1]+Ri*math.sin(rad_s)),
                layer=layer, color=5))
            ents.append(BasicEntities.line(msp,
                (center[0]+Ro*math.cos(rad_e), center[1]+Ro*math.sin(rad_e)),
                (center[0]+Ri*math.cos(rad_e), center[1]+Ri*math.sin(rad_e)),
                layer=layer, color=5))
        except Exception:
            pass
        return ents

    @staticmethod
    def tee(msp, junction: tuple,
            main_dia: float = 50,
            branch_dia: float = 30,
            orientation: str = 'T',    # 'T'(垂直分支) 或 '+'(十字四通)
            main_direction: str = 'H', # 'H'=水平主管 / 'V'=垂直主管
            layer: str = 'valve'):
        """三通/四通接头"""
        from entities.basic import BasicEntities
        from entities.polyline import PolylineEntity

        jx, jy = junction
        rm = main_dia/2; rb = branch_dia/2
        L = max(main_dia, branch_dia) * 2  # 短臂长度
        ents = []

        if main_direction == 'H':
            # 水平主管
            ents.extend([
                BasicEntities.line(msp, (jx-L,jy-rm), (jx+L,jy-rm), layer=layer, color=5),
                BasicEntities.line(msp, (jx-L,jy+rm), (jx+L,jy+rm), layer=layer, color=5),
            ])
            # 垂直支管
            ents.extend([
                BasicEntities.line(msp, (jx-rb,jy), (jx+rb,jy), layer=layer, color=5),
                BasicEntities.line(msp, (jx-rb,jy-L), (jx+rb,jy-L), layer=layer, color=5),
                BasicEntities.line(msp, (jx-rb,jy), (jx-rb,jy-L), layer=layer, color=5),
                BasicEntities.line(msp, (jx+rb,jy), (jx+rb,jy-L), layer=layer, color=5),
            ])
        else:
            # 垂直主管
            ents.extend([
                BasicEntities.line(msp, (jx-rm,jy-L), (jx-rm,jy+L), layer=layer, color=5),
                BasicEntities.line(msp, (jx+rm,jy-L), (jx+rm,jy+L), layer=layer, color=5),
            ])
            ents.extend([
                BasicEntities.line(msp, (jx,jy-rb), (jx,jy+rb), layer=layer, color=5),
                BasicEntities.line(msp, (jx-L,jy-rb), (jx-L,jy+rb), layer=layer, color=5),
                BasicEntities.line(msp, (jx,jy-rb), (jx-L,jy-rb), layer=layer, color=5),
                BasicEntities.line(msp, (jx,jy+rb), (jx-L,jy+rb), layer=layer, color=5),
            ])

        if orientation == '+':
            # 四通：另一侧也有支管
            sign = -1
            opp_L = L
            if main_direction == 'H':
                ents.extend([
                    BasicEntities.line(msp, (jx-rb,jy), (jx+rb,jy), layer=layer, color=5),
                    BasicEntities.line(msp, (jx-rb,jy+opp_L), (jx+rb,jy+opp_L), layer=layer, color=5),
                    BasicEntities.line(msp, (jx-rb,jy), (jx-rb,jy+opp_L), layer=layer, color=5),
                    BasicEntities.line(msp, (jx+rb,jy), (jx+rb,jy+opp_L), layer=layer, color=5),
                ])

        return ents

    @staticmethod
    def valve_gate(msp, position: tuple,
                   pipe_diameter: float = 50,
                   valve_type: str = 'gate',
                   layer: str = 'valve'):
        """
        阀门符号（简化画法）
        
        Args:
            valve_type: 'gate'闸阀 / 'globe'截止阀 / 'check'止回阀 / 'ball'球阀 / 'butterfly'蝶阀
        """
        from entities.basic import BasicEntities
        from entities.polyline import PolylineEntity

        px, py = position; d = pipe_diameter; hw = d * 0.8; hh = d
        ents = []

        if valve_type == 'gate':
            # 闸阀：双线管道 + 内部两个三角形（闸板）
            rm = d/2
            L = d * 0.6
            ents.extend([
                BasicEntities.line(msp, (px-L,py-rm), (px+L,py-rm), layer=layer, color=5),
                BasicEntities.line(msp, (px-L,py+rm), (px+L,py+rm), layer=layer, color=5),
            ])
            # 阀体轮廓
            vhw = d * 0.3; vhh = d * 0.6
            ents.extend([
                PolylineEntity.polygon(msp,
                    [(px-vhw,py-vhh),(px+vhw,py-vhh),(px+vhw,py+vhh),(px-vhw,py+vhh)],
                    layer=layer, color=5),
            ])
            # 手轮/阀杆
            stem_len = d * 0.5
            ents.append(BasicEntities.line(msp, (px,py+vhh), (px,py+vhh+stem_len),
                                           layer=layer, color=5, lineweight=25))
            wheel_r = d * 0.25
            from entities.curves import CurveEntities
            ents.append(CurveEntities.arc(msp, (px,py+vhh+stem_len), wheel_r,
                                          -90, 270, layer=layer, color=5))

        elif valve_type == 'globe':
            # 截止阀：S形阀体 + 波浪线近似
            rm = d/2; L = d * 0.5
            ents.extend([
                BasicEntities.line(msp, (px-L,py-rm), (px+L,py-rm), layer=layer, color=5),
                BasicEntities.line(msp, (px-L,py+rm), (px+L,py+rm), layer=layer, color=5),
            ])
            # S形波纹（用折线近似）
            wave_amp = rm * 0.4
            for y_off in [-rm*0.3, rm*0.3]:
                pts = [(px-wave_amp, py+y_off), (px, py+y_off-wave_amp),
                       (px+wave_amp, py+y_off)]
                ents.extend(BasicEntities.lines(msp, pts, layer=layer, color=5))

        elif valve_type == 'check':
            # 止回阀：箭头 + 弹簧示意
            rm = d/2; L = d * 0.4
            ents.extend([
                BasicEntities.line(msp, (px-L,py-rm), (px+L,py-rm), layer=layer, color=5),
                BasicEntities.line(msp, (px-L,py+rm), (px+L,py+rm), layer=layer, color=5),
            ])
            # 三角形箭头
            arr_size = d * 0.35
            ents.append(PolylineEntity.polygon(msp,
                [(px,arr_size),(px+arr_size,0),(px,-arr_size)],
                layer=layer, color=5))

        elif valve_type == 'ball':
            # 球阀：圆形阀体 + T形手柄
            from entities.curves import CurveEntities
            rm = d/2; L = d * 0.4
            ents.extend([
                BasicEntities.line(msp, (px-L,py-rm), (px+L,py-rm), layer=layer, color=5),
                BasicEntities.line(msp, (px-L,py+rm), (px+L,py+rm), layer=layer, color=5),
                ents.append(CurveEntities.circle(msp, (px,py), rm*1.2, layer=layer, color=5)) if False else None,
            ])
            # 补充球体
            ents.append(CurveEntities.circle(msp, (px,py), rm*1.1, layer=layer, color=5))

        elif valve_type == 'butterfly':
            # 蝶阀：短圆柱 + 圆盘手柄
            rm = d/2; body_len = d * 0.2
            ents.extend([
                BasicEntities.line(msp, (px-body_len,py-rm), (px+body_len,py-rm), layer=layer, color=5),
                BasicEntities.line(msp, (px-body_len,py+rm), (px+body_len,py+rm), layer=layer, color=5),
            ])
            handle_len = d * 0.8
            handle_wid = d * 0.08
            ents.append(PolylineEntity.rect_centered(msp,
                (px+handle_len/2, py+rm+d*0.3), handle_len, handle_wid, layer=layer, color=5))

        return ents

    @staticmethod
    def flange(msp, position: tuple,
               diameter: float = 50,
               thickness: float = 10,
               bolt_count: int = 4,
               layer: str = 'fitting'):
        """法兰盘（端面视图）"""
        from entities.curves import CurveEntities
        from entities.basic import BasicEntities

        cx, cy = position
        ro = diameter/2 + thickness
        ri = diameter/2 - thickness
        rb = diameter/2
        ents = [
            CurveEntities.circle(msp, (cx,cy), ro, layer=layer, color=5, linewidth=40),
            CurveEntities.circle(msp, (cx,cy), ri, layer=layer, color=5, linewidth=25),
            CurveEntities.circle(msp, (cx,cy), rb, layer=layer, color=5),
        ]

        # 螺栓孔
        bolt_r = thickness * 0.6
        bolt_circle_r = (ro + ri) / 2
        for i in range(bolt_count):
            a = 2 * math.pi * i / bolt_count
            bx = cx + bolt_circle_r * math.cos(a)
            by = cy + bolt_circle_r * math.sin(a)
            ents.append(CurveEntities.circle(msp, (bx,by), bolt_r, layer='thin', color=5))

        return ents

    @staticmethod
    def reducer(msp, start: tuple, end: tuple,
                dia_large: float = 80,
                dia_small: float = 50,
                layer: str = 'fitting'):
        """大小头（异径管）渐缩段"""
        from entities.basic import BasicEntities
        dx, dy = end[0]-start[0], end[1]-start[1]
        length = math.sqrt(dx*dx+dy*dy)
        rl = dia_large/2; rs = dia_small/2
        ux, uy = dx/length, dy/length
        nx, ny = -uy, ux

        return [
            BasicEntities.line(msp,
                (start[0]+nx*rl, start[1]+ny*rl),
                (end[0]+nx*rs, end[1]+ny*rs), layer=layer, color=5),
            BasicEntities.line(msp,
                (start[0]-nx*rl, start[1]-ny*rl),
                (end[0]-nx*rs, end[1]-ny*rs), layer=layer, color=5),
        ]

    @staticmethod
    def cap(msp, position: tuple, diameter: float = 50,
            direction: tuple = None,
            layer: str = 'fitting'):
        """管帽/盲板"""
        from entities.curves import CurveEntities
        from entities.basic import BasicEntities
        cx, cy = position; r = diameter/2

        if direction is None:
            # 端面视图：圆
            return [CurveEntities.circle(msp, (cx,cy), r, layer=layer, color=5, linewidth=40)]

        # 侧视：直线封口
        dx, dy = direction
        length = math.sqrt(dx*dx+dy*dy)
        ux, uy = dx/length, dy/length
        nx, ny = -uy, ux
        return [BasicEntities.line(msp,
            (cx+nx*r, cy+ny*r), (cx-nx*r, cy-ny*r),
            layer=layer, color=5, linewidth=40)]
