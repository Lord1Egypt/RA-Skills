"""结构图库 - 梁、板、柱、基础、钢筋"""
import math
from typing import Tuple


class StructuralTemplates:
    """结构施工图标准组件"""

    @staticmethod
    def beam_section(msp, position: tuple,
                     width: float = 250, height: float = 500,
                     rebar_top: list = None,   # [(dia, count), ...]
                     rebar_bot: list = None,
                     rebar_side: list = None,
                     stirrup_dia: int = 8,
                     stirrup_spacing: int = 150,
                     layer: str = 'outline',
                     hatch: bool = True):
        """
        梁断面（配筋详图）
        
        Args:
            rebar_top: 顶部纵筋列表，如 [(20,2)] = 2根直径20
            rebar_bot: 底部纵筋
            rebar_side: 腰筋/构造筋
        """
        from entities.basic import BasicEntities
        from entities.polyline import PolylineEntity
        from entities.curves import CurveEntities

        cx, cy = position; hw = width/2; hh = height/2
        ents = []

        # 外轮廓
        ents.append(PolylineEntity.rectangle_centered(msp, (cx,cy), width, height,
                                                  layer=layer, color=7, lineweight=50))

        # 混凝土填充
        if hatch:
            from hatch.patterns import HatchFill
            pts = [(cx-hw,cy-hh),(cx+hw,cy-hh),(cx+hw,cy+hh),(cx-hw,cy+hh)]
            HatchFill.industry_fill(msp, pts, material='concrete', scale=30, layer='hatch')

        # 箍筋（矩形）
        c = 25  # 保护层厚度
        sw, sh = width - 2*c, height - 2*c
        ents.append(PolylineEntity.rectangle_centered(msp, (cx,cy), sw, sh,
                                                  layer='rebar', color=1))

        # 纵筋（圆点表示）
        default_rebar = rebar_bot or [(16,3)]
        
        for rebars, y_pos in [
            (rebar_top or [], cy + hh - c),
            (default_rebar, cy - hh + c),
            (rebar_side or [], cy),
        ]:
            for dia, count in rebars:
                rd = dia / 1.5  # 显示放大比例
                if count == 1:
                    ents.append(CurveEntities.circle(msp, (cx,y_pos), rd, layer='rebar', color=1))
                else:
                    spacing_x = sw / (count + 1)
                    for i in range(1, count + 1):
                        rx = cx - sw/2 + i * spacing_x
                        ents.append(CurveEntities.circle(msp, (rx,y_pos), rd, layer='rebar', color=1))

        return ents

    @staticmethod
    def slab_reinforcement(msp, corner1: tuple, corner2: tuple,
                           thickness: float = 120,
                           rebar_bottom_X: str = '12@150',
                           rebar_bottom_Y: str = '10@200',
                           rebar_top_X: str = '',
                           rebar_top_Y: str = '',
                           layer: str = 'outline'):
        """
        楼板配筋平面图
        
        Args:
            rebar_bottom_X: 底部X向钢筋标注 "直径@间距"
        """
        from entities.basic import BasicEntities
        from entities.text import TextEntity
        from entities.curves import CurveEntities

        x1, y1 = corner1; x2, y2 = corner2
        mx, my = (x1+x2)/2, (y1+y2)/2; hw, hh = (x2-x1)/2, (y2-y1)/2
        ents = []

        # 板轮廓
        ents.append(BasicEntities.line(msp, (x1,y1),(x2,y1), layer=layer, color=7, lineweight=50))
        ents.append(BasicEntities.line(msp, (x1,y2),(x2,y2), layer=layer, color=7, lineweight=50))
        ents.append(BasicEntities.line(msp, (x1,y1),(x1,y2), layer=layer, color=7, lineweight=50))
        ents.append(BasicEntities.line(msp, (x2,y1),(x2,y2), layer=layer, color=7, lineweight=50))

        # 钢筋示意线（双向）
        line_offset = min(hw, hh) * 0.15
        # X向底部钢筋
        if rebar_bottom_X:
            ry = y1 + line_offset
            ents.append(BasicEntities.line(msp, (x1+30,ry), (x2-30,ry),
                                           layer='rebar', color=1, lineweight=35))
            # 钢筋弯钩
            hook_len = 40
            ents.append(CurveEntities.arc(msp, (x1+30,ry), hook_len, 90, 270, layer='rebar', color=1))
            ents.append(CurveEntities.arc(msp, (x2-30,ry), hook_len, -90, 90, layer='rebar', color=1))
            # 标注
            TextEntity.text(msp, f'{rebar_bottom_X}', (mx, ry-20),
                           height=min(x2-x1,y2-y1)*0.04,
                           halign='CENTER', layer='text')

        # Y向底部钢筋
        if rebar_bottom_Y:
            rx = x1 + line_offset
            ents.append(BasicEntities.line(msp, (rx,y1+30),(rx,y2-30),
                                           layer='rebar', color=1, lineweight=35))
            hook_len = 40
            ents.append(CurveEntities.arc(msp, (rx,y1+30), hook_len, 0, 180, layer='rebar', color=1))
            ents.append(CurveEntities.arc(msp, (rx,y2-30), hook_len, 180, 360, layer='rebar', color=1))
            TextEntity.text(msp, f'{rebar_bottom_Y}', (rx-30,my),
                           height=min(x2-x1,y2-y1)*0.04,
                           halign='CENTER', valign='MIDDLE', layer='text',
                           rotation=90)

        # 板厚标注
        th_text = f't={thickness}'
        ents.append(TextEntity.text(msp, th_text, (x2-hh*0.5, y2-hh*0.3),
                                    height=min(x2-x1,y2-y1)*0.05, layer='text'))

        return ents

    @staticmethod
    def foundation_strip(msp, start: tuple, end: tuple,
                         top_width: float = 1000,
                         bottom_width: float = 1400,
                         depth: float = 800,
                         rebar_main: str = '20@120',
                         rebar_distribute: str = '12@200',
                         layer: str = 'outline'):
        """
        条形基础剖面图
        
        Returns:
            基础轮廓 + 配筋实体
        """
        from entities.polyline import PolylineEntity
        from entities.basic import BasicEntities
        from entities.text import TextEntity
        from hatch.patterns import HatchFill

        sx, sy = start; ex, ey = end
        dx, dy = ex-sx, ey-sy
        length = math.sqrt(dx*dx+dy*dy)
        ux, uy = dx/length, dy/length
        nx, ny = -uy, ux
        tw = top_width/2; bw = bottom_width/2

        # 梯形截面顶点（从左到右：左上→左下→右下→右上）
        pts = [
            (sx-nx*tw, sy-ny*tw),           # 左上（顶面左侧）
            (sx-nx*bw, sy-ny*(tw+(bw-tw)*depth/(depth))),  # 左下
            (ex-nx*bw, ey-ny*(tw+(bw-tw)*depth/(depth))),  # 右下
            (ex-nx*tw, ey-ny*tw),             # 右上（顶面右侧）
        ]
        # 简化：垂直方向向下延伸深度
        base_y = sy - depth if abs(uy) < 0.9 else sy
        profile_pts = [
            (sx-nx*tw, sy-ny*tw),
            (sx-nx*bw, sy-depth),
            (ex-nx*bw, ey-depth),
            (ex-nx*tw, ey-ny*tw),
        ]

        ents = [PolylineEntity.polygon(msp, profile_pts, layer=layer, color=7)]

        # 混凝土填充
        HatchFill.industry_fill(msp, profile_pts, material='concrete', scale=50, layer='hatch')

        # 底部受力筋（粗横线）
        bar_c = 50  # 保护层
        bar_y = sy - depth + bar_c
        bar_len = bw * 2 - 2 * bar_c
        ents.append(BasicEntities.line(msp,
            (sx-nx*(bw-bar_c), bar_y), (ex-nx*(bw-bar_c), bar_y),
            layer='rebar', color=1, lineweight=45))
        # 弯钩
        from entities.curves import CurveEntities
        hlen = 80
        ents.extend([
            CurveEntities.arc(msp, (sx-nx*(bw-bar_c), bar_y), hlen, 180, 360, layer='rebar', color=1),
            CurveEntities.arc(msp, (ex-nx*(bw-bar_c), bar_y), hlen, 0, 180, layer='rebar', color=1),
        ])

        # 分布筋（竖向短线）
        dist_count = max(int(length / 300), 3)
        for i in range(dist_count + 1):
            t = i / dist_count
            px = sx + t*dx; py = sy + t*dy
            dbar_h = depth * 0.6
            ents.append(BasicEntities.line(msp,
                (px, py-dbar_h), (px, py-depth+bar_c+hlen),
                layer='thin', color=5))

        # 标注
        mid_x = (sx+ex)/2; mid_y = (sy+ey)/2
        ents.append(TextEntity.text(msp, rebar_main, (mid_x, sy-depth+80),
                                   height=footing_depth*0.03, halign='CENTER', layer='text'))
        ents.append(TextEntity.text(msp, f'⌀{bottom_width}',
                                   (mid_x, sy-depth-30),
                                   height=footing_depth*0.02, halign='CENTER', layer='text'))

        return ents

    @staticmethod
    def column_footing(msp, center: tuple,
                       column_size: tuple = (500, 500),
                       footing_size: tuple = (2000, 2000),
                       footing_depth: float = 600,
                       step_count: int = 1,
                       layer: str = 'outline'):
        """
        独立基础（柱下扩展基础）平面图 + 简化剖面
        """
        from entities.polyline import PolylineEntity
        from entities.basic import BasicEntities
        from entities.text import TextEntity
        from entities.curves import CurveEntities
        from hatch.patterns import HatchFill

        cx, cy = center
        cw, ch = column_size; fw, fh = footing_size
        ents = []

        # 基础底板外轮廓（平面）
        ents.append(PolylineEntity.rectangle_centered(msp, (cx,cy), fw, fh,
                                                  layer=layer, color=7, lineweight=50))
        # 柱截面
        ents.append(PolylineEntity.rectangle_centered(msp, (cx,cy), cw, ch,
                                                  layer='column', color=2, lineweight=50))

        # 台阶式（如果有）
        if step_count >= 1:
            s1_w = fw * 0.75; s1_h = fh * 0.75
            ents.append(PolylineEntity.rectangle_centered(msp, (cx,cy), s1_w, s1_h,
                                                      layer=layer, color=7, lineweight=35))
            HatchFill.industry_fill(msp, [
                (-s1_w/2,-s1_h/2),(s1_w/2,-s1_h/2),(s1_w/2,s1_h/2),(-s1_w/2,s1_h/2)
            ], material='concrete', scale=50, layer='hatch')

        # 轴线标记
        tick = fw * 0.08
        ents.append(BasicEntities.line(msp, (cx-fw/2-tick,cy), (cx+cw/2+tick,cy),
                                       layer='axis', color=1, lineweight=13))
        ents.append(BasicEntities.line(msp, (cx,cy-fh/2-tick), (cx,cy+ch/2+tick),
                                       layer='axis', color=1, lineweight=13))

        # 尺寸标注文字
        ents.append(TextEntity.text(msp, f'{fw}×{fh}', (cx, cy+fh/2+50),
                                   height=fw*0.02, halign='CENTER', layer='text'))
        ents.append(TextEntity.text(msp, f'{cw}×{ch}', (cx, cy-ch/2-20),
                                   height=cw*0.025, halign='CENTER', layer='text'))

        return ents
