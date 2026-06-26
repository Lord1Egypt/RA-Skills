"""引线标注与坐标标注"""
from typing import Tuple


class LeaderAnnotation:
    """引线和特殊标注"""

    @staticmethod
    def leader(msp,
               target: Tuple[float, float],
               end_point: Tuple[float, float],
               text: str = '',
               arrowhead: bool = True,
               layer: str = 'annotation',
               color: int = 7):
        """
        多段引线标注
        Args:
            target: 箭头指向的点
            end_point: 引线末端（文字位置）
            arrowhead: 是否带箭头
        """
        from entities.basic import BasicEntities
        from entities.text import TextEntity
        
        # 引线主体
        BasicEntities.line(msp, target, end_point, layer=layer, color=color)
        
        # 简化箭头（小三角）
        if arrowhead:
            import math
            dx = end_point[0] - target[0]
            dy = end_point[1] - target[1]
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 0.01:
                ux, uy = dx/dist, dy/dist
                arr_size = 1.5
                ax, ay = target
                p1 = (ax + arr_size*(ux*math.cos(math.radians(30)) + uy*math.sin(math.radians(30))),
                      ay + arr_size*(uy*math.cos(math.radians(30)) - ux*math.sin(math.radians(30))))
                p2 = (ax + arr_size*(ux*math.cos(-math.radians(30)) + uy*math.sin(-math.radians(30))),
                      ay + arr_size*(uy*math.cos(-math.radians(30)) - ux*math.sin(-math.radians(30))))
                BasicEntities.lines(msp, [target, p1, target, p2], 
                                   layer=layer, color=color, lineweight=18)
        
        # 文字
        if text:
            TextEntity.text(msp, text, end_point, height=2.0, 
                           layer=layer, color=color)
            
        return end_point

    @staticmethod
    def coordinate_x(msp, point: Tuple[float, float], 
                     offset: float = 3.0, decimals: int = 1,
                     layer='dimension', color=3):
        """X 坐标标注"""
        from entities.basic import BasicEntities
        from entities.text import TextEntity
        
        px, py = point
        BasicEntities.line(msp, (px, py), (px+offset, py), layer=layer, color=color)
        TextEntity.text(msp, f"X={px:.{decimals}f}", (px+offset, py+0.5),
                       height=1.8, layer=layer, color=color)

    @staticmethod
    def coordinate_y(msp, point: Tuple[float, float],
                     offset: float = 3.0, decimals: int = 1,
                     layer='dimension', color=3):
        """Y 坐标标注"""
        from entities.basic import BasicEntities
        from entities.text import TextEntity
        
        px, py = point
        BasicEntities.line(msp, (px, py), (px, py+offset), layer=layer, color=color)
        TextEntity.text(msp, f"Y={py:.{decimals}f}", (px+0.5, py+offset),
                       height=1.8, layer=layer, color=color)
