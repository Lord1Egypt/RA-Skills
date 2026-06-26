"""裁剪与延伸工具"""
import math
from typing import Optional


class TrimTool:
    """裁剪与延伸"""

    @staticmethod
    def line_intersection(p1, p2, p3, p4) -> Optional[tuple]:
        """求两条直线段的交点"""
        x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
        
        denom = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
        if abs(denom) < 1e-10:
            return None  # 平行或重合
            
        t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / denom
        
        ix = x1 + t*(x2-x1)
        iy = y1 + t*(y2-y1)
        
        return (ix, iy)

    @staticmethod
    def trim_line_to_boundary(msp, line_start, line_end, 
                               boundary_points: list):
        """
        将直线裁剪到边界多边形（简化：找第一个交点并截断）
        
        Returns:
            裁剪后的新终点，或原终点如果无交点
        """
        for i in range(len(boundary_points)):
            b1 = boundary_points[i]
            b2 = boundary_points[(i+1) % len(boundary_points)]
            
            intersect = TrimTool.line_intersection(line_start, line_end, b1, b2)
            if intersect is not None:
                # 检查交点是否在线段上
                return intersect
                
        return line_end


class ExtendTool:
    """延长工具"""

    @staticmethod
    def extend_line(line_start, line_end, extend_length: float):
        """将直线从末端延长指定长度"""
        dx = line_end[0] - line_start[0]
        dy = line_end[1] - line_start[1]
        length = math.sqrt(dx*dx + dy*dy)
        if length < 1e-10:
            return line_end
            
        ux = dx / length
        uy = dy / length
        
        return (line_end[0] + ux * extend_length, line_end[1] + uy * extend_length)

    @staticmethod
    def extend_line_to_point(line_start, line_end, target_point):
        """延长直线直到经过目标点的垂足或交点"""
        # 计算目标点到直线的投影
        dx = line_end[0] - line_start[0]
        dy = line_end[1] - line_start[1]
        length_sq = dx*dx + dy*dy
        if length_sq < 1e-10:
            return target_point
            
        t = ((target_point[0]-line_start[0])*dx + (target_point[1]-line_start[1])*dy) / length_sq
        if t > 1.0:
            ext_x = line_start[0] + t * dx
            ext_y = line_start[1] + t * dy
            return (ext_x, ext_y)
        else:
            return line_end
