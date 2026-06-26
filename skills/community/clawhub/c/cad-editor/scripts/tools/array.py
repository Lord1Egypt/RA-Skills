"""阵列工具 - 矩形阵列和环形阵列"""
import math
from typing import List, Tuple


class ArrayTool:
    """阵列操作"""

    @staticmethod
    def rectangular(msp,
                   base_entities_func,
                   base_point: tuple,
                   rows: int = 1,
                   cols: int = 1,
                   row_spacing: float = 100,
                   col_spacing: float = 100):
        """
        矩形阵列
        
        Args:
            base_entities_func: callable(msp, insert_point) -> [实体列表]
                                在给定位置绘制一组基础图元的函数
            base_point: 阵列起始位置（左下角）
            rows: 行数
            cols: 列数
            row_spacing: 行间距（Y方向）
            col_spacing: 列间距（X方向）
        
        Returns:
            所有生成的实体的扁平列表
        """
        all_results = []
        bx, by = base_point
        
        for r in range(rows):
            for c in range(cols):
                px = bx + c * col_spacing
                py = by + r * row_spacing
                entities = base_entities_func(msp, (px, py))
                if entities:
                    all_results.extend(entities)
                    
        return all_results

    @staticmethod
    def polar(msp,
              base_entities_func,
              center: tuple,
              count: int,
              radius: float,
              start_angle: float = 0,
              total_angle: float = 360):
        """
        环形阵列（极坐标阵列）
        
        Args:
            center: 阵列中心点
            count: 实例数量（含原始位置）
            radius: 分布半径
            start_angle: 起始角度（度），0=右侧水平
            total_angle: 总覆盖角度（度），360=整圆
        """
        all_results = []
        cx, cy = center
        
        for i in range(count):
            angle_deg = start_angle + (total_angle * i / max(count-1, 1))
            angle_rad = math.radians(angle_deg)
            
            px = cx + radius * math.cos(angle_rad)
            py = cy + radius * math.sin(angle_rad)
            
            entities = base_entities_func(msp, (px, py))
            if entities:
                all_results.extend(entities)
                
        return all_results

    @staticmethod
    def path_array(msp,
                   base_entities_func,
                   path_points: list,
                   spacing: float = 50):
        """
        沿路径阵列
        
        Args:
            path_points: 路径控制点 [(x,y), ...]
            spacing: 实例之间的距离
        """
        all_results = []
        
        # 计算路径总长度
        total_len = 0
        segments = []
        for i in range(len(path_points)-1):
            dx = path_points[i+1][0] - path_points[i][0]
            dy = path_points[i+1][1] - path_points[i][1]
            seg_len = math.sqrt(dx*dx + dy*dy)
            segments.append((path_points[i], path_points[i+1], seg_len))
            total_len += seg_len
            
        # 沿路径放置实例
        dist = 0
        while dist <= total_len:
            # 找当前距离所在的线段
            accum = 0
            for p1, p2, slen in segments:
                if accum + slen >= dist:
                    t = (dist - accum) / max(slen, 1e-10)
                    px = p1[0] + t*(p2[0]-p1[0])
                    py = p1[1] + t*(p2[1]-p1[1])
                    entities = base_entities_func(msp, (px, py))
                    if entities:
                        all_results.extend(entities)
                    break
                accum += slen
                    
            dist += spacing
            
        return all_results
