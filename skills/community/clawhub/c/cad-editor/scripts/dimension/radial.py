"""径向标注 - 半径、直径、角度"""
import math


class RadialDimension:
    """径向/角度标注"""

    @staticmethod
    def radius(msp,
               center: tuple,
               point_on_arc: tuple,
               text: str = '',
               leader_angle: float = 45,
               layer: str = 'dimension',
               color: int = 3):
        """
        半径标注 (简化实现：画圆心标记+引线+R文字)
        """
        from entities.basic import BasicEntities
        from entities.text import TextEntity
        
        cx, cy = center
        px, py = point_on_arc
        r = math.sqrt((px-cx)**2 + (py-cy)**2)
        
        # 圆心十字标记
        cross_size = min(r * 0.15, 3)
        BasicEntities.line(msp, (cx-cross_size, cy), (cx+cross_size, cy), 
                           layer=layer, color=color, lineweight=13)
        BasicEntities.line(msp, (cx, cy-cross_size), (cx, cy+cross_size),
                           layer=layer, color=color, lineweight=13)
        
        # 引线方向
        rad = math.atan2(py-cy, px-cx)
        text_dist = r + r * 0.3
        tx = cx + text_dist * math.cos(rad)
        ty = cy + text_dist * math.sin(rad)
        
        # 引线
        BasicEntities.line(msp, (px, py), (tx, ty), layer=layer, 
                          color=color, lineweight=18)
        
        # 文字 Rxx
        label = f"R{r:.1f}" if not text else text
        TextEntity.text(msp, label, (tx, ty), height=r*0.12+1.5,
                       layer=layer, color=color)

    @staticmethod
    def diameter(msp,
                 center: tuple,
                 point_on_arc: tuple,
                 text: str = '',
                 layer: str = 'dimension',
                 color: int = 3):
        """
        直径标注 (简化实现：穿过圆心的标注线+⌀文字)
        """
        from entities.basic import BasicEntities
        from entities.text import TextEntity
        
        cx, cy = center
        px, py = point_on_arc
        dx, dy = px - cx, py - cy
        r = math.sqrt(dx*dx + dy*dy)
        d = r * 2
        
        # 直径线两端延伸
        ext = r * 0.15
        ux, uy = dx/r, dy/r  # 单位向量
        x1, y1 = cx - ux*(r+ext), cy - uy*(r+ext)
        x2, y2 = cx + ux*(r+ext), cy + uy*(r+ext)
        
        # 直径线
        BasicEntities.line(msp, (x1,y1), (x2,y2), layer=layer, color=color, lineweight=25)
        
        # 端部短划线
        tick = r * 0.05
        BasicEntities.line(msp, (x1-tick*uy, y1+tick*ux), (x1+tick*uy, y1-tick*ux),
                           layer=layer, color=color, lineweight=25)
        BasicEntities.line(msp, (x2-tick*uy, y2+tick*ux), (x2+tick*uy, y2-tick*ux),
                           layer=layer, color=color, lineweight=25)
        
        # 文字
        label = f"⌀{d:.1f}" if not text else text
        TextEntity.text(msp, label, (cx, cy+r*0.35), height=r*0.14+1.8,
                       layer=layer, color=color, halign='CENTER')

    @staticmethod
    def angular_3pt(msp,
                    center: tuple,
                    p1: tuple,
                    p2: tuple,
                    arc_radius: float = 10,
                    text: str = '',
                    layer: str = 'dimension',
                    color: int = 3):
        """三点角度标注"""
        import math
        from entities.curves import CurveEntities
        from entities.text import TextEntity
        
        a1 = math.degrees(math.atan2(p1[1]-center[1], p1[0]-center[0]))
        a2 = math.degrees(math.atan2(p2[1]-center[1], p2[0]-center[0]))
        
        # 角度弧
        CurveEntities.arc(msp, center, arc_radius, a1, a2, 
                         layer=layer, color=color)
        
        # 角度文字
        am = (a1 + a2) / 2
        rad_am = math.radians(am)
        tx = center[0] + (arc_radius + arc_radius*0.3) * math.cos(rad_am)
        ty = center[1] + (arc_radius + arc_radius*0.3) * math.sin(rad_am)
        
        angle_val = abs(a2 - a1)
        if angle_val > 180:
            angle_val = 360 - angle_val
            
        label = f"{angle_val:.1f}°" if not text else text
        TextEntity.text(msp, label, (tx, ty), height=2.0, layer=layer, color=color)
