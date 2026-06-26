"""偏移工具 - 平行复制曲线"""
import math
from typing import Tuple, List


class OffsetTool:
    """图元偏移操作"""

    @staticmethod
    def offset_line(msp,
                    start: tuple,
                    end: tuple,
                    distance: float,
                    side: str = 'left',
                    layer='0', color=7):
        """
        直线偏移（生成平行线）
        
        Args:
            start, end: 原线段端点
            distance: 偏移距离
            side: 'left' 或 'right'（沿起点到终点的方向看）
        
        Returns:
            新线的 (start, end) 坐标
        """
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.sqrt(dx*dx + dy*dy)
        if length < 1e-10:
            return None
        
        # 单位法向量
        nx = -dy / length
        ny = dx / length
        
        if side == 'right':
            nx, ny = -nx, -ny
            
        new_start = (start[0] + nx * distance, start[1] + ny * distance)
        new_end = (end[0] + nx * distance, end[1] + ny * distance)

        from entities.basic import BasicEntities
        BasicEntities.line(msp, new_start, new_end, layer=layer, color=color)
        return (new_start, new_end)

    @staticmethod
    def offset_polyline(msp,
                        points: list,
                        distance: float,
                        side: str = 'outside',
                        layer='0', color=7):
        """
        多段线偏移（简化实现：对每条边分别偏移后连接）
        
        注意：这是简化版本，不处理自交和角点修圆
        """
        from entities.basic import BasicEntities
        import math

        n = len(points)
        if n < 3:
            return []
            
        result_pts = []
        
        for i in range(n):
            p1 = points[i]
            p2 = points[(i+1) % n]
            
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            length = math.sqrt(dx*dx + dy*dy)
            if length < 1e-10:
                continue
                
            # 法向量
            nx = -dy / length
            ny = dx / length
            if side == 'inside':
                nx, ny = -nx, -ny
                
            result_pts.append((p1[0] + nx*distance, p1[1] + ny*distance))

        # 画结果多段线
        from entities.polyline import PolylineEntity
        return PolylineEntity.polyline(msp, result_pts, closed=True,
                                       layer=layer, color=color)
