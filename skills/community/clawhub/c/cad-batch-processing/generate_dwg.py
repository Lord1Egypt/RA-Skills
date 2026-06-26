#!/usr/bin/env python3
"""
生成DWG/DXF
功能：按指令画墙、门窗、标注，生成平面/立面
"""

import os
import sys
import ezdxf
from ezdxf.math import Vec3
from typing import List, Tuple, Dict, Any

class CADGenerator:
    def __init__(self):
        self.doc = ezdxf.new('R2018', setup=True)
        self.msp = self.doc.modelspace()
        # 创建默认图层
        self._setup_layers()
    
    def _setup_layers(self):
        """创建常用图层"""
        self.doc.layers.add('WALL', color=7)        # 墙 - 灰色
        self.doc.layers.add('WINDOW', color=5)     # 窗 - 蓝色
        self.doc.layers.add('DOOR', color=2)       # 门 - 黄色
        self.doc.layers.add('DIM', color=1)        # 标注 - 红色
        self.doc.layers.add('TEXT', color=6)       # 文字 - 品红
        self.doc.layers.add('FURNITURE', color=3) # 家具 - 绿色
    
    def add_wall(self, start: Tuple[float, float], end: Tuple[float, float], thickness: float = 240):
        """
        添加墙线
        start: (x, y) 起点
        end: (x, y) 终点
        thickness: 墙厚 (mm) 默认240mm
        """
        # 计算矩形四个点
        import math
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.sqrt(dx*dx + dy*dy)
        if length == 0:
            return
        
        # 单位化方向向量
        dx /= length
        dy /= length
        
        # 垂直方向
        perp_dx = -dy * thickness/2
        perp_dy = dx * thickness/2
        
        points = [
            (start[0] + perp_dx, start[1] + perp_dy),
            (end[0] + perp_dx, end[1] + perp_dy),
            (end[0] - perp_dx, end[1] - perp_dy),
            (start[0] - perp_dx, start[1] - perp_dy),
        ]
        
        # 创建闭合多段线
        vertices = [Vec3(p[0], p[1], 0) for p in points]
        vertices.append(Vec3(points[0][0], points[0][1], 0))
        self.msp.add_lwpolyline(vertices, dxfattribs={'layer': 'WALL'})
    
    def add_window(self, start: Tuple[float, float], width: float, height: float = 2400, sill_height: float = 900):
        """
        添加窗
        start: 左下角坐标
        width: 窗宽
        height: 窗高
        """
        x1, y1 = start
        points = [
            (x1, y1),
            (x1 + width, y1),
            (x1 + width, y1 + height),
            (x1, y1 + height),
        ]
        vertices = [Vec3(p[0], p[1], 0) for p in points]
        vertices.append(Vec3(points[0][0], points[0][1], 0))
        self.msp.add_lwpolyline(vertices, dxfattribs={'layer': 'WINDOW'})
        
        # 添加中线表示窗
        self.msp.add_line(Vec3(x1, y1 + height/2), Vec3(x1 + width, y1 + height/2), dxfattribs={'layer': 'WINDOW'})
    
    def add_door(self, start: Tuple[float, float], width: float, height: float = 2100, is_open: bool = True):
        """
        添加门
        start: 门轴坐标
        width: 门宽
        height: 门高
        """
        x0, y0 = start
        # 门线
        self.msp.add_line(Vec3(x0, y0), Vec3(x0, y0 + height), dxfattribs={'layer': 'DOOR'})
        
        if is_open:
            # 门开启弧线
            from ezdxf.math import arc_angles_from_start_end_angle
            center = Vec3(x0, y0)
            radius = width
            start_angle = 0
            end_angle = 90
            self.msp.add_arc(center, radius, start_angle, end_angle, dxfattribs={'layer': 'DOOR'})
    
    def add_dimension_linear(self, start: Tuple[float, float], end: Tuple[float, float], offset: float):
        """
        添加线性标注
        """
        dim = self.msp.add_linear_dim(
            base=Vec3(start[0], start[1] - offset),
            p1=Vec3(start[0], start[1]),
            p2=Vec3(end[0], end[1]),
            dimstyle='EZDXF',
            layer='DIM'
        )
        dim.render()
    
    def add_text(self, text: str, position: Tuple[float, float], height: float = 100, layer: str = 'TEXT'):
        """添加文字"""
        self.msp.add_text(text, dxfattribs={
            'insert': Vec3(position[0], position[1], 0),
            'height': height,
            'layer': layer
        })
    
    def save(self, output_path: str):
        """保存DXF文件"""
        self.doc.saveas(output_path)
        print(f"✅ DXF生成完成，保存到: {output_path}")


def main():
    # 示例：生成一个简单的一室平面
    if len(sys.argv) < 2:
        print("Usage: python generate_dwg.py <output.dxf>")
        print("示例：生成一个简单的一室平面")
        output = "example_plane.dxf"
    else:
        output = sys.argv[1]
    
    gen = CADGenerator()
    
    # 画外墙
    wall_thickness = 240
    gen.add_wall((0, 0), (6000, 0), wall_thickness)       # 下墙
    gen.add_wall((0, 0), (0, 4000), wall_thickness)       # 左墙
    gen.add_wall((6000, 0), (6000, 4000), wall_thickness) # 右墙
    gen.add_wall((0, 4000), (6000, 4000), wall_thickness) # 上墙
    
    # 加窗
    gen.add_window((2000, 4000 + wall_thickness/2), 2000, 1500)
    
    # 加门
    gen.add_door((0 + wall_thickness/2, 1500), 900)
    
    # 标注
    gen.add_dimension_linear((0, 0), (6000, 0), 500)
    gen.add_dimension_linear((0, 0), (0, 4000), 500)
    
    # 标注文字
    gen.add_text("示例平面 6000x4000", (2500, -1000), 200)
    
    gen.save(output)


if __name__ == "__main__":
    main()
