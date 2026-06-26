"""预定义填充图案库"""
import ezdxf


class HatchPatterns:
    """标准图案填充定义"""

    # ━━━━━━━━━ 建筑常用填充 ━━━━━━━━━
    # 使用 ezdxf 内置图案名称（ANSI/ISO 标准）

    # ANSI 图案 (角度线)
    ANSI = {
        'ansi31':    'ANSI 31',     # 45度斜线（金属/砖）
        'ansi32':    'ANSI 32',     # 60度斜线
        'ansi33':    'ANSI 33',     # 45度交叉线
        'ansi34':    'ANSI 34',     # 60度交叉线
        'ansi35':    'ANSI 35',     # 45度反向斜线
        'ansi36':    'ANSI 36',     # 网格
        'ansi37':    'ANSI 37',     # 点划网格
        'ansi38':    'ANSI 38',     # 反向45度交叉线
    }

    # ISO 图案
    ISO = {
        'iso02w100': 'ISO02W100',   # 细虚线
        'iso03w100': 'ISO03W100',   # 虚线
        'iso04w100': 'ISO04W100',   # 长虚线
        'iso05w100': 'ISO05W100',   # 双点划线
    }

    # 其他标准
    OTHERS = {
        'solid':      'SOLID',       # 实体填充
        'dots':       'DOTS',        # 点阵
        'cross':      'CROSS',       # 十字
        'brick':      'BRICK',       # 砖墙
        'ar-conc':    'AR-CONC',     # 混凝土
        'ar-sand':    'AR-SAND',     # 沙子
        'gravel':     'GRAVEL',      # 砂石
        'honey':      'HONEY',       # 蜂窝
        'stars':      'STARS',       # 星形
        'triang':     'TRIANG',      # 三角
        'zigzag':     'ZIGZAG',      # 锯齿
        'angle':      'ANGLE',       # 角度
        'net':        'NET3',        # 网
        'earth':      'EARTH',       # 泥土
        'grass':      'GRASS',       # 草地
    }

    # 行业快捷映射
    BY_INDUSTRY = {
        'concrete':  ('AR-CONC', 1.0, 0),      # 混凝土
        'brick':     ('BRICK',    1.0, 0),      # 砖墙
        'sand':      ('AR-SAND',  1.0, 0),      # 砂
        'metal':     ('ANSI 31',  2.0, 0),      # 金属材料
        'steel':     ('ANSI 31',  3.0, 45),      # 钢材
        'wood':      ('ANSI 33',  2.0, 0),      # 木纹（交叉线近似）
        'glass':     ('ANSI 34',  2.0, 0),      # 玻璃
        'insulation':('ANSI 37',  1.5, 0),      # 保温层
        'soil':      ('EARTH',    1.0, 0),      # 土壤
        'water':     ('ANSI 32',  1.5, 30),      # 水
        'foam':      ('HONEY',    2.0, 0),      # 泡沫
    }


class HatchFill:
    """填充操作"""

    @staticmethod
    def fill_polygon(msp,
                     boundary_points: list,
                     pattern_name: str = 'ANSI 31',
                     scale: float = 1.0,
                     angle: float = 0,
                     color: int = 7,
                     layer: str = 'hatch'):
        """
        多边形边界内填充图案
        
        Args:
            boundary_points: 边界顶点 [(x,y), ...] 必须闭合
            pattern_name: 填充图案名（使用 ezdxf 内置名或自定义）
            scale: 图案缩放比例
            angle: 旋转角度（度）
        """
        pts_2d = [(p[0], p[1]) for p in boundary_points]
        
        hatch = msp.add_hatch(
            color=color,
            dxfattribs={
                'layer': layer,
                'pattern_name': pattern_name,
                'solid_fill': pattern_name.upper() == 'SOLID',
            }
        )
        
        hatch.paths.add_polyline_path(pts_2d, is_closed=True)
        
        if hasattr(hatch, 'set_pattern_fill'):
            try:
                hatch.set_pattern_fill(pattern_name, color=7)
            except Exception:
                pass
        
        # 设置比例和角度
        try:
            hatch.dxf.pattern_scale = scale
            hatch.dxf.pattern_angle = angle
        except Exception:
            pass
            
        return hatch

    @staticmethod
    def fill_circle(msp,
                    center: tuple,
                    radius: float,
                    pattern_name: str = 'ANSI 31',
                    scale: float = 1.0,
                    angle: float = 0,
                    color: int = 7,
                    layer: str = 'hatch'):
        """圆形区域内填充"""
        hatch = msp.add_hatch(color=7, dxfattribs={'layer': layer})
        
        # 用多边形近似圆（64段）
        import math
        points = []
        for i in range(65):
            a = math.radians(i * 360 / 64)
            px = center[0] + radius * math.cos(a)
            py = center[1] + radius * math.sin(a)
            points.append((px, py))
            
        hatch.paths.add_polyline_path(points, is_closed=True)
        
        try:
            hatch.dxf.pattern_scale = scale
            hatch.dxf.pattern_angle = angle
        except Exception:
            pass
            
        return hatch

    @staticmethod
    def solid_fill(msp,
                   boundary_points: list,
                   color: int = 7,
                   layer: str = 'hatch'):
        """实体纯色填充"""
        return HatchFill.fill_polygon(msp, boundary_points, 
                                       pattern_name='SOLID',
                                       color=color, layer=layer)

    @staticmethod
    def industry_fill(msp,
                      boundary_points: list,
                      material: str,
                      scale: float = 1.0,
                      angle: float = 0,
                      layer: str = 'hatch'):
        """按行业材料名自动选择填充图案"""
        mat_key = material.lower()
        if mat_key not in HatchPatterns.BY_INDUSTRY:
            print(f"[WARN] 未知材料 '{material}'，默认用 ANSI 31")
            pattern = ('ANSI 31', scale, angle)
        else:
            pattern = HatchPatterns.BY_INDUSTRY[mat_key]
            if scale != 1.0 or angle != 0:
                pattern = (pattern[0], scale, angle)
                
        return HatchFill.fill_polygon(msp, boundary_points,
                                       pattern_name=pattern[0],
                                       scale=pattern[1],
                                       angle=pattern[2],
                                       layer=layer)

    @staticmethod
    def gradient_fill_rect(msp,
                           corner1: tuple,
                           corner2: tuple,
                           color1: int = 5,
                           color2: int = 1,
                           layer: str = 'hatch'):
        """
        渐变填充矩形（简化实现：用密集线条模拟）
        
        注意：DXF 标准渐变支持有限，这里用实心+半透明近似，
        或建议导出后用其他工具处理
        """
        # 实际 DXF 中可用 SOLID + alpha，但兼容性有限
        # 这里先用 solid 作为 fallback
        x1, y1 = corner1
        x2, y2 = corner2
        return HatchFill.solid_fill(msp, 
                                     [(x1,y1),(x2,y1),(x2,y2),(x1,y2)],
                                     color=color1, layer=layer)
