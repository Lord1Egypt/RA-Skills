"""文字实体 - 单行文本、多行文本(MText)"""
from typing import Tuple, Optional


# 常用中文字体映射（优先级从高到低）
FONT_FALLBACKS = {
    'default': ['Arial', 'DejaVu Sans', 'sans-serif'],
    'cn': ['SimHei', 'Microsoft YaHei', 'SimSun', 'STSong', 'sans-serif'],
    'tech': ['ISOCP', 'isocp.ttf', 'romans.shx', 'txt.shx'],
}


class TextEntity:
    """文字绘制操作"""

    @staticmethod
    def text(msp,
             content: str,
             insert_point: Tuple[float, float],
             height: float = 2.5,
             rotation: float = 0,
             layer: str = '0',
             color: int = 7,
             style: str = 'STANDARD',
             halign: str = 'LEFT',
             valign: str = 'BASELINE',
             oblique: float = 0):
        """
        单行文本 (TEXT)
        
        Args:
            content: 文本内容
            insert_point: 插入点坐标 (x, y)
            height: 字高（绘图单位）
            rotation: 旋转角度（度）
            halign: 水平对齐 LEFT/CENTER/RIGHT
            valign: 垂直对齐 BASELINE/TOP/MIDDLE/BOTTOM
            oblique: 倾斜角度（度）
        """
        attribs = {
            'layer': layer,
            'color': color,
            'height': height,
            'rotation': rotation,
            'style': style,
        }
        
        txt = msp.add_text(content, dxfattribs=attribs)
        try:
            # align needs to be an ezdxf TextEntityAlignment or None
            if halign.upper() != 'BASELINE':
                from ezdxf.enums import TextEntityAlignment
                align_map = {
                    'LEFT': TextEntityAlignment.LEFT,
                    'CENTER': TextEntityAlignment.CENTER,
                    'RIGHT': TextEntityAlignment.RIGHT,
                    'MIDDLE': TextEntityAlignment.MIDDLE,
                    'MID': TextEntityAlignment.MIDDLE,
                    'TOP': TextEntityAlignment.TOP,
                    'BOTTOM': TextEntityAlignment.BOTTOM,
                }
                ea = align_map.get(halign.upper())
                if ea is not None:
                    txt.set_placement((insert_point[0], insert_point[1]), align=ea)
            else:
                txt.set_placement((insert_point[0], insert_point[1]))
        except Exception:
            txt.set_placement((insert_point[0], insert_point[1]))
        
        try:
            if oblique != 0:
                txt.set_oblique(oblique)
        except Exception:
            pass
            
        return txt

    @staticmethod
    def mtext(msp,
              content: str,
              insert_point: Tuple[float, float],
              char_height: float = 2.5,
              width: Optional[float] = None,
              rotation: float = 0,
              line_spacing: float = 1.5,
              attachment_point: int = 1,  # 1=左上, 2=中上, 3=右上...
              layer: str = '0',
              color: int = 7,
              font_name: str = 'txt'):
        """
        多行文本 (MTEXT) — 支持换行和富文本
        
        Args:
            content: 支持 \\n 换行符
            width: 文本框宽度（None=不限宽）
            attachment_point: 对齐位置 (1=TL, 2=TC, 3=TR, 4=ML, 5=MC, 6=MR, 7=BL, 8=BC, 9=BR)
            
        DXF MText 特殊字符：
            \\P = 换行, %%d = °, %%c = ⌀, %%p = ±, %%o = 上划线, %%u = 下划线
        """
        attribs = {
            'char_height': char_height,
            'width': width or 10.0,
            'rotation': rotation,
            'attachment_point': attachment_point,
            'layer': layer,
            'color': color,
            'style': font_name,
        }
        
        mtxt = msp.add_mtext(content, dxfattribs=attribs)
        mtxt.insert = (insert_point[0], insert_point[1])
        return mtxt

    @staticmethod
    def label(msp,
              text: str,
              position: Tuple[float, float],
              offset: Tuple[float, float] = (2, 2),
              leader_length: float = 5,
              height: float = 2.0,
              layer: str = 'text',
              color: int = 7):
        """
        带引线的标注文字
        在指定位置附近放置标签文字，用短线指向目标点
        """
        from .basic import BasicEntities
        
        # 引线起点
        text_pos = (position[0] + offset[0], position[1] + offset[1])
        
        # 画引线
        BasicEntities.line(msp, position, text_pos, layer=layer, color=color)
        
        # 写文字
        TextEntity.text(msp, text, text_pos, height=height,
                       layer=layer, color=color)
        
        return text_pos

    # ━━━━━━━━━ 快捷标注文字 ━━━━━━━━━

    @staticmethod
    def dimension_text(msp,
                       value: float,
                       mid_point: Tuple[float, float],
                       prefix: str = '',
                       suffix: str = '',
                       unit_label: str = '',
                       decimals: int = 2,
                       height: float = 2.0,
                       layer: str = 'dimension'):
        """尺寸标注专用文字"""
        fmt_val = f"{value:.{decimals}f}"
        display_text = f"{prefix}{fmt_val}{suffix}{unit_label}"
        return TextEntity.text(msp, display_text, mid_point, height=height,
                               layer=layer, halign='CENTER')
