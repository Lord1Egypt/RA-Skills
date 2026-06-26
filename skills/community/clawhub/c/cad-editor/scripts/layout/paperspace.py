"""图纸空间/布局管理"""
import ezdxf
from typing import Optional


# 标准图纸尺寸（mm）- GB/T 14689
PAPER_SIZES = {
    'A0':   (841,   1189),
    'A1':   (594,   841),
    'A2':   (420,   594),
    'A3':   (297,   420),
    'A4':   (210,   297),
    'A0L':  (1189,  841),  # 横版
    'A1L':  (841,   594),
    'A2L':  (594,   420),
    'A3L':  (420,   297),
    'A4L':  (297,   210),
}


class PaperSpace:
    """图纸布局管理"""

    @staticmethod
    def create_layout(doc: ezdxf.document.Drawing,
                      name: str = 'Layout1',
                      paper_size: str = 'A3') -> ezdxf.layouts.Layout:
        """创建新图纸空间"""
        if paper_size not in PAPER_SIZES:
            raise ValueError(f"未知纸张大小 '{paper_size}'，可用: {list(PAPER_SIZES.keys())}")
        try:
            layout = doc.layouts.new(name)
        except Exception:
            layout = doc.layouts.get(name)
        w, h = PAPER_SIZES[paper_size]
        try:
            layout.dxf.paper_width = w
            layout.dxf.paper_height = h
        except Exception:
            pass
        return layout

    @staticmethod
    def add_viewport(layout,
                     center: tuple,
                     width: float,
                     height: float,
                     scale: float = 1.0,
                     model_center: tuple = None):
        """创建视口（模型空间到图纸空间的窗口）"""
        vp = layout.add_viewport(
            center=(center[0], center[1]),
            size=(width, height),
            dxfattribs={'status': 1}
        )
        try:
            vp.dxf.view_height = height * scale
            if model_center:
                vp.dxf.center_point = (model_center[0], model_center[1])
        except Exception:
            pass
        return vp

    @staticmethod
    def draw_title_block(msp_or_layout,
                         corner: tuple,
                         size: str = 'A3',
                         title: str = '',
                         drawing_no: str = '',
                         scale_text: str = '1:100',
                         layer: str = 'frame',
                         color: int = 7) -> dict:
        """绘制标准图框和标题栏（GB风格）"""
        from entities.basic import BasicEntities
        from entities.polyline import PolylineEntity
        from entities.text import TextEntity

        if size not in PAPER_SIZES:
            size = 'A3'
        pw, ph = PAPER_SIZES[size]
        x, y = corner

        margin_left = 25
        margin_other = 5
        fw = pw - margin_left - margin_other
        fh = ph - 2 * margin_other

        # 外框线（粗实线）
        PolylineEntity.rectangle(msp_or_layout,
                                  (x+margin_left, y+margin_other),
                                  (x+margin_left+fw, y+margin_other+fh),
                                  layer=layer, color=color, lineweight=53)

        # 内框
        PolylineEntity.rectangle(msp_or_layout,
                                  (x+margin_left, y+margin_other),
                                  (x+margin_left+fw, y+margin_other+fh),
                                  layer=layer, color=color)

        # 标题栏（右下角 180x40mm）
        tb_x = x + margin_left + fw - 180
        tb_y = y + margin_other
        tb_w, tb_h = 180, 40

        PolylineEntity.rectangle(msp_or_layout,
                                  (tb_x, tb_y), (tb_x + tb_w, tb_y + tb_h),
                                  layer=layer, color=color)

        # 分隔线
        BasicEntities.line(msp_or_layout, (tb_x, tb_y+20), (tb_x+tb_w, tb_y+20),
                           layer=layer, color=color)
        BasicEntities.line(msp_or_layout, (tb_x+80, tb_y), (tb_x+80, tb_y+20),
                           layer=layer, color=color)
        BasicEntities.line(msp_or_layout, (tb_x+120, tb_y), (tb_x+120, tb_y+20),
                           layer=layer, color=color)

        # 标题文字
        if title:
            TextEntity.text(msp_or_layout, title, (tb_x + tb_w/2, tb_y + 10),
                           height=5, halign='CENTER', valign='MIDDLE', layer=layer, color=color)

        TextEntity.text(msp_or_layout, '图号', (tb_x+100, tb_y+10),
                       height=3, halign='CENTER', valign='MIDDLE', layer=layer, color=color)
        if drawing_no:
            TextEntity.text(msp_or_layout, drawing_no, (tb_x+150, tb_y+10),
                           height=3, halign='CENTER', valign='MIDDLE', layer=layer, color=color)

        TextEntity.text(msp_or_layout, '比例', (tb_x+40, tb_y+28),
                       height=2.5, halign='CENTER', valign='MIDDLE', layer=layer, color=color)
        TextEntity.text(msp_or_layout, scale_text, (tb_x+60, tb_y+28),
                       height=2.5, halign='CENTER', valign='MIDDLE', layer=layer, color=color)

        return {
            'frame_rect': ((x+margin_left, y+margin_other), (x+margin_left+fw, y+margin_other+fh)),
            'title_block_rect': ((tb_x, tb_y), (tb_x+tb_w, tb_y+tb_h)),
            'inner_area': ((x+margin_left, y+margin_other), (x+margin_left+fw, y+margin_other+fh)),
        }
