"""镜像工具"""
import math


class MirrorTool:
    """镜像操作"""

    @staticmethod
    def mirror_point(point: tuple, axis_p1: tuple, axis_p2: tuple) -> tuple:
        """计算一个点关于轴的镜像点"""
        px, py = point
        x1, y1 = axis_p1
        x2, y2 = axis_p2
        
        dx = x2 - x1
        dy = y2 - y1
        d_sq = dx*dx + dy*dy
        
        if d_sq < 1e-10:
            return point  # 退化情况
            
        # 投影
        t = ((px-x1)*dx + (py-y1)*dy) / d_sq
        proj_x = x1 + t * dx
        proj_y = y1 + t * dy
        
        # 镜像点 = 对称位置
        mx = 2*proj_x - px
        my = 2*proj_y - py
        
        return (mx, my)

    @staticmethod
    def mirror_points(points: list, axis_p1: tuple, axis_p2: tuple) -> list:
        """批量镜像点集"""
        return [MirrorTool.mirror_point(p, axis_p1, axis_p2) for p in points]

    @staticmethod
    def mirror_entity(msp, entity_func, original_params: dict,
                      axis_p1: tuple, axis_p2: tuple, **kwargs):
        """
        绘制某个图元的镜像副本
        
        Args:
            entity_func: 图元绘制函数 (如 BasicEntities.line)
            original_params: 原始参数字典（包含坐标参数）
            axis_p1, axis_p2: 镜像轴的两个点
            kwargs: 其他固定参数（layer, color等）
        
        Returns:
            镜像后的实体
        """
        mirrored_params = {}
        
        for key, val in original_params.items():
            if isinstance(val, tuple) and len(val) >= 2:
                # 这是一个坐标点，需要镜像
                mirrored_params[key] = MirrorTool.mirror_point(val, axis_p1, axis_p2)
            elif isinstance(val, list) and len(val) > 0:
                if isinstance(val[0], tuple):
                    mirrored_params[key] = MirrorTool.mirror_points(val, axis_p1, axis_p2)
                else:
                    mirrored_params[key] = val
            else:
                mirrored_params[key] = val
                
        return entity_func(msp, **mirrored_params, **kwargs)
