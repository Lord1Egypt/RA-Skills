"""线性尺寸标注"""
from typing import Tuple
import ezdxf


class LinearDimension:
    """线性标注操作"""

    @staticmethod
    def horizontal(msp,
                   p1: Tuple[float, float],
                   p2: Tuple[float, float],
                   offset: float = 5.0,
                   text: str = '',
                   layer: str = 'dimension',
                   color: int = 3):
        """
        水平尺寸标注（只测量 X 方向距离）
        
        Args:
            p1, p2: 测量点（自动对齐到同一Y值）
            offset: 标注线偏移距离
            text: 自定义文字（空=自动测量值）
        """
        y = max(p1[1], p2[1]) + offset
        
        dim = msp.add_linear_dim(
            base=(p1[0], y),
            p1=(p1[0], p1[1]),
            p2=(p2[0], p2[1]),
            dimstyle='EZDXF',
            override={
                'dimtxsty': 'STANDARD',
                'dimtxt': 2.0,
                'dimclrt': color,
                'dimclrd': color,
                'dimclre': color,
            }
        )
        
        if dim:
            try:
                dim.render()
            except Exception:
                pass
                
        return dim

    @staticmethod
    def vertical(msp,
                 p1: Tuple[float, float],
                 p2: Tuple[float, float],
                 offset: float = 5.0,
                 text: str = '',
                 layer: str = 'dimension',
                 color: int = 3):
        """
        垂直尺寸标注（只测量 Y 方向距离）
        """
        x = max(p1[0], p2[0]) + offset

        dim = msp.add_linear_dim(
            base=(x, p1[1]),
            p1=p1,
            p2=p2,
            angle=90,
            dimstyle='EZDXF',
            override={'dimtxt': 2.0}
        )
        
        if dim:
            try:
                dim.render()
            except Exception:
                pass
        return dim

    @staticmethod
    def aligned(msp,
                p1: Tuple[float, float],
                p2: Tuple[float, float],
                distance: float = 5.0,
                text: str = '',
                layer: str = 'dimension',
                color: int = 3):
        """
        对齐尺寸标注（沿两点连线方向测量）
        
        Args:
            distance: 标注线到测量线的垂直偏移
        """
        import math
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        length = math.sqrt(dx*dx + dy*dy)
        if length < 1e-6:
            return None
            
        # 计算偏移方向（法向量）
        nx = -dy / length
        ny = dx / length
        
        # 标注线位置
        mx = (p1[0] + p2[0]) / 2 + nx * distance
        my = (p1[1] + p2[1]) / 2 + ny * distance

        dim = msp.add_linear_dim(
            base=(mx, my),
            p1=p1,
            p2=p2,
            dimstyle='EZDXF',
            override={'dimtxt': 2.0, 'dimclrt': color}
        )
        
        if dim:
            try:
                dim.render()
            except Exception:
                pass
        return dim

    @staticmethod
    def chain_horizontal(msp, points: list, offset: float = 5.0,
                         layer='dimension', color=3):
        """连续水平标注（链式）"""
        results = []
        for i in range(len(points) - 1):
            d = LinearDimension.horizontal(msp, points[i], points[i+1],
                                           offset=offset, layer=layer, color=color)
            results.append(d)
        return results

    @staticmethod
    def chain_vertical(msp, points: list, offset: float = 5.0,
                       layer='dimension', color=3):
        """连续垂直标注（链式）"""
        results = []
        for i in range(len(points) - 1):
            d = LinearDimension.vertical(msp, points[i], points[i+1],
                                          offset=offset, layer=layer, color=color)
            results.append(d)
        return results

    @staticmethod
    def baseline_horizontal(msp, base_point: list, other_points: list,
                            offset: float = 5.0, layer='dimension', color=3):
        """基线水平标注（所有点从同一个基准开始）"""
        results = []
        for pt in other_points:
            d = LinearDimension.horizontal(msp, base_point, pt,
                                           offset=offset, layer=layer, color=color)
            results.append(d)
        return results
