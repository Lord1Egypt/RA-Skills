"""建筑图库 - 墙体、门窗、柱子、楼梯、卫浴"""
import math
from typing import Tuple


class ArchitecturalTemplates:
    """建筑制图标准组件"""

    @staticmethod
    def wall(msp, points: list, thickness: float = 240,
             layer: str = 'wall', color: int = 1):
        """建筑墙体（双线表示墙厚）"""
        from entities.basic import BasicEntities
        half_t = thickness / 2
        results = []
        for i in range(len(points) - 1):
            p1, p2 = points[i], points[i + 1]
            dx, dy = p2[0] - p1[0], p2[1] - p1[1]
            length = math.sqrt(dx*dx + dy*dy)
            if length < 1e-6:
                continue
            nx, ny = -dy/length, dx/length
            results.append(BasicEntities.line(msp,
                (p1[0]+nx*half_t, p1[1]+ny*half_t),
                (p2[0]+nx*half_t, p2[1]+ny*half_t), layer=layer, color=color))
            results.append(BasicEntities.line(msp,
                (p1[0]-nx*half_t, p1[1]-ny*half_t),
                (p2[0]-nx*half_t, p2[1]-ny*half_t), layer=layer, color=color))
        return results

    @staticmethod
    def door_single(msp, position: tuple, width: float = 900,
                    direction: str = 'right', open_angle: float = 90,
                    layer: str = 'door', color: int = 3):
        """单扇平开门"""
        from entities.basic import BasicEntities
        from entities.curves import CurveEntities

        px, py = position; hw = width / 2
        entities = []

        dir_map = {
            'right': ((px, py-hw), (px, py+hw), -90),
            'left':  ((px, py+hw), (px, py-hw), 270),
            'up':    ((px-hw, py), (px+hw, py), 180),
            'down':  ((px+hw, py), (px-hw, py), 0),
        }
        hinge_pt, latch_pt, base_a = dir_map.get(direction, dir_map['right'])

        entities.append(BasicEntities.line(msp, hinge_pt, latch_pt,
                                           layer='door', color=color))
        sign = -1 if direction in ('left','up') else 1
        end_a = base_a + open_angle * sign

        try:
            arc = CurveEntities.arc(msp, hinge_pt, width,
                                    min(base_a, end_a), max(base_a, end_a),
                                    layer=layer, color=color)
            if arc: entities.append(arc)
        except Exception: pass

        rad_e = math.radians(end_a)
        door_end = (hinge_pt[0] + width*math.cos(rad_e),
                    hinge_pt[1] + width*math.sin(rad_e))
        entities.append(BasicEntities.line(msp, hinge_pt, door_end,
                                           layer=layer, color=color))
        return entities

    @staticmethod
    def double_door(msp, center: tuple, total_width: float = 1500,
                    layer: str = 'door'):
        """双开门"""
        cx, cy = center; hw = total_width / 2
        e1 = ArchitecturalTemplates.door_single(msp, (cx,cy), hw, 'right', layer=layer)
        e2 = ArchitecturalTemplates.door_single(msp, (cx,cy), hw, 'left', layer=layer)
        return (e1 or []) + (e2 or [])

    @staticmethod
    def window(msp, corner1: tuple, corner2: tuple,
               frame_width: float = 60, has_sill: bool = True,
               sill_depth: float = 100, layer: str = 'window', color: int = 4):
        """窗户（四线表示窗洞）"""
        from entities.basic import BasicEntities

        x1, y1 = corner1; x2, y2 = corner2
        ents = [
            BasicEntities.line(msp, (x1,y1),(x2,y1), layer=layer, color=color),
            BasicEntities.line(msp, (x1,y2),(x2,y2), layer=layer, color=color),
            BasicEntities.line(msp, (x1,y1),(x1,y2), layer=layer, color=color),
            BasicEntities.line(msp, (x2,y1),(x2,y2), layer=layer, color=color),
        ]

        w, h = x2-x1, y2-y1
        if w > 1200:
            mx = (x1+x2)/2
            ents.append(BasicEntities.line(msp, (mx, y1+20), (mx, y2-20), layer=layer, color=color))
        if h > 900:
            my = (y1+y2)/2
            ents.append(BasicEntities.line(msp, (x1+20, my), (x2-20, my), layer=layer, color=color))

        if has_sill:
            ents.append(BasicEntities.line(msp, (x1-sill_depth, y1), (x2+sill_depth, y1),
                                           layer=layer, color=color, lineweight=35))
        return ents

    @staticmethod
    def column(msp, center: tuple, size=(400,400),
               layer: str = 'column', color: int = 2,
               hatch_pattern: str = 'concrete'):
        """结构柱子"""
        from entities.polyline import PolylineEntity
        from hatch.patterns import HatchFill

        sx, sy = size; hx, hy = sx/2, sy/2
        cx, cy = center
        pts = [(cx-hx,cy-hy),(cx+hx,cy-hy),(cx+hx,cy+hy),(cx-hx,cy+hy)]
        PolylineEntity.polygon(msp, pts, layer=layer, color=color)
        HatchFill.industry_fill(msp, pts, material=hatch_pattern, scale=50, layer=layer)

    @staticmethod
    def stair_straight(msp, bottom_center: tuple, step_count: int = 12,
                       step_width: float = 280, total_width: float = 1200,
                       direction: str = 'up-right',
                       layer: str = 'stair', color: int = 4):
        """直跑楼梯平面图"""
        from entities.basic import BasicEntities
        from entities.text import TextEntity

        bx, by = bottom_center; tw = total_width / 2
        entities = []; is_v = direction == 'up-up'
        go_r = 'right' in direction

        for i in range(step_count):
            if is_v:
                y1, y2 = by+i*step_width, by+(i+1)*step_width
                ents = [BasicEntities.line(msp, (bx-tw,y1),(bx+tw,y1), layer=layer, color=color)]
                if i == step_count-1:
                    ents.append(BasicEntities.line(msp, (bx-tw,y2),(bx+tw,y2), layer=layer, color=color))
            else:
                x1 = (bx-tw+i*step_width) if go_r else (bx+tw-i*step_width)
                x2 = (bx-tw+(i+1)*step_width) if go_r else (bx+tw-(i+1)*step_width)
                ents = [BasicEntities.line(msp, (x1,by-tw),(x1,by+tw), layer=layer, color=color)]
                if i == step_count-1:
                    ents.append(BasicEntities.line(msp, (x2,by-tw),(x2,by+tw), layer=layer, color=color))
            entities.extend(ents)

        # 折断线
        mid_i = step_count // 2
        if is_v:
            my = by + mid_i * step_width
            entities.append(BasicEntities.lines(msp, [(bx-tw-20,my-30),(bx+tw+20,my+30)],
                                                layer=layer, color=color))

        arrow_text = '上 ↑' if is_v else ('上 →' if go_r else '上 ←')
        top_y = by + step_count * step_width + 200
        TextEntity.text(msp, arrow_text, (bx, top_y), height=150,
                       halign='CENTER', layer=layer, color=color)

        return entities

    @staticmethod
    def balcony(msp, start: tuple, end: tuple, depth: float = 1200,
                rail_offset: float = 50, layer: str = 'balcony'):
        """阳台"""
        from entities.basic import BasicEntities
        from entities.polyline import PolylineEntity

        sx, sy = start; ex, ey = end
        dx, dy = ex-sx, ey-sy
        length = math.sqrt(dx*dx+dy*dy)
        nx, ny = -dy/length, dx/length

        # 外轮廓
        outer_pts = [
            (sx, sy),
            (sx + nx*depth, sy + ny*depth),
            (ex + nx*depth, ey + ny*depth),
            (ex, ey)
        ]
        PolylineEntity.polygon(msp, outer_pts, layer=layer, color=5, lineweight=25)

        # 栏杆线
        rail_start = (sx + nx*rail_offset, sy + ny*rail_offset)
        rail_end   = (ex + nx*rail_offset, ey + ny*rail_offset)
        BasicEntities.line(msp, rail_start, rail_end, layer=layer, color=5)

        # 滑门符号
        mx = (sx+ex)/2 + nx*rail_offset
        my = (sy+ey)/2 + ny*rail_offset
        door_w = min(length/3, 800)
        d_half = door_w/2
        BasicEntities.line(msp, (mx-d_half, my), (mx+d_half, my), layer='door', color=3)
