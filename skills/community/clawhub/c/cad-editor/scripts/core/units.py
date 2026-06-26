"""单位系统 - 缩放转换、格式化"""


class Units:
    """绘图单位工具"""

    # 单位定义
    DEFINITIONS = {
        'mm':     {'name': '毫米', 'factor': 1.0,       'insunits': 4},
        'cm':     {'name': '厘米', 'factor': 10.0,      'insunits': 5},
        'm':      {'name': '米',   'factor': 1000.0,    'insunits': 6},
        'inch':   {'name': '英寸', 'factor': 25.4,      'insunits': 1},
        'ft':     {'name': '英尺', 'factor': 304.8,     'insunits': 2},
    }

    @staticmethod
    def convert(value: float, from_unit: str, to_unit: str) -> float:
        """单位间换算（基于mm为基准）"""
        f_from = Units.DEFINITIONS.get(from_unit, {}).get('factor', 1.0)
        f_to   = Units.DEFINITIONS.get(to_unit,   {}).get('factor', 1.0)
        return value * f_from / max(f_to, 0.001)

    @staticmethod
    def format_dimension(value: float, unit: str = 'mm',
                        decimals: int = 2,
                        show_unit: bool = True) -> str:
        """格式化尺寸标注字符串"""
        unit_labels = {
            'mm': 'mm', 'm': 'm', 'cm': 'cm',
            'inch': '"', 'ft': '\'',
            None: '',
        }
        label = unit_labels.get(unit, '')
        formatted = f"{value:.{decimals}f}"
        return f"{formatted}{label}" if show_unit else formatted

    @staticmethod
    def scale_for_paper(value: float, drawing_scale: tuple = (1, 100),
                       paper_size: str = 'A3') -> float:
        """
        将模型空间尺寸转换为图纸空间尺寸
        
        Args:
            value: 模型空间值
            drawing_scale: 比例元组，如 (1,100) 表示 1:100
        """
        s_num, s_denom = drawing_scale
        return value * s_num / s_denom

    # 常用比例
    SCALES = {
        '1:50':  (1, 50),   '1:100': (1, 100),
        '1:150': (1, 150),  '1:200': (1, 200),
        '1:500': (1, 500),  '1:1000': (1, 1000),
        '1:20':  (1, 20),   '1:25':  (1, 25),
        '1:30':  (1, 30),   '1:75':  (1, 75),
        '1:1':   (1, 1),    '1:2':   (1, 2),
        '1:5':   (1, 5),    '1:10':  (1, 10),
    }
