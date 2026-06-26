"""预定义线型"""
import ezdxf


class Linetypes:
    """常用线型定义与加载"""

    @staticmethod
    def load_standard(doc: ezdxf.document.Drawing):
        """加载标准线型到文档"""
        lts = doc.linetypes
        
        # 检查并添加常用线型
        _definitions = {
            'DASHED':    [0.5, -0.25],
            'DASHDOT':   [0.75, -0.125, 0.05, -0.125],
            'DASHDOT2':  [1.0, -0.15, 0.08, -0.15],
            'DOT':       [0.05, -0.2],
            'DOTTED':    [0.08, -0.12, 0.02, -0.12],
            'CENTER':    [1.5, -0.2, 0.1, -0.2],
            'CENTER2':   [2.0, -0.25, 0.15, -0.25],
            'PHANTOM2':  [1.2, -0.15, 0.15, -0.15, 0.05, -0.15],
            'DIVIDE':   [0.8, -0.1, 0.15, -0.1, 0.03, -0.1],
            'BORDER':    [1.0, -0.1, 0.8, -0.1, 0.3, -0.1],
            'HIDDEN':    [0.4, -0.15, 0.1, -0.15],
            'LONG_DASH': [2.0, -0.3],
            'CHAIN':     [1.5, -0.1, 0.3, -0.1, 0.1, -0.1],
        }
        
        for name, pattern in _definitions.items():
            try:
                if name not in lts:
                    lts.add(name, pattern=[pattern])
            except Exception:
                pass
    
    @staticmethod
    def load_custom(doc, name: str, pattern: list):
        """加载自定义线型
        Args:
            pattern: 线型元素列表 [画长, 空(-), 画长, 空...]
                     正数=画线长度, 负数=空白长度
        """
        doc.linetypes.add(name, pattern=[pattern])
