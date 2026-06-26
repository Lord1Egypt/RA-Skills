"""图元模块 - 基础图元（直线、点）"""
from typing import Tuple, Optional
import ezdxf


class BasicEntities:
    """基础图元操作"""

    @staticmethod
    def line(msp, 
             start: Tuple[float, float], 
             end: Tuple[float, float],
             layer: str = '0', 
             color: int = 7,
             lineweight: int = 35):
        """
        画直线
        
        Args:
            msp: 模型空间
            start: 起点坐标 (x, y)
            end: 终点坐标 (x, y)
            layer: 图层名
            color: ACI 颜色索引 (1-256)
            lineweight: 线重 (1/100 mm 单位，如 50=0.5mm)
        Returns:
            Line 实体
        """
        return msp.add_line(
            (start[0], start[1], 0),
            (end[0], end[1], 0),
            dxfattribs={
                'layer': layer,
                'color': color,
                'lineweight': lineweight,
            }
        )

    @staticmethod
    def lines(msp, 
              points: list,
              closed: bool = False,
              layer: str = '0', 
              color: int = 7,
              lineweight: int = 35):
        """连续画多条线段"""
        results = []
        for i in range(len(points) - 1):
            results.append(BasicEntities.line(msp, points[i], points[i+1], 
                                              layer, color, lineweight))
        if closed and len(points) >= 3:
            results.append(BasicEntities.line(msp, points[-1], points[0],
                                              layer, color, lineweight))
        return results

    @staticmethod
    def point(msp, 
              location: Tuple[float, float],
              layer: str = '0',
              color: int = 7):
        """画点"""
        return msp.add_point((location[0], location[1], 0),
                            dxfattribs={'layer': layer, 'color': color})

    @staticmethod
    def construction_line(msp, 
                          base_point: Tuple[float, float],
                          direction_vec: Tuple[float, float],
                          layer: str = '0'):
        """构造线（无限延伸的线）"""
        return msp.add_xline(
            (base_point[0], base_point[1], 0),
            (direction_vec[0], direction_vec[1], 0),
            dxfattribs={'layer': layer}
        )
