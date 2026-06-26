"""视口管理"""
import math


class Viewport:
    """视口操作"""

    @staticmethod
    def fit_to_extent(layout, viewport, min_pt: tuple, max_pt: tuple):
        """调整视口以显示指定范围"""
        extent_width = max_pt[0] - min_pt[0]
        extent_height = max_pt[1] - min_pt[1]

        try:
            viewport.dxf.center_point = (
                (min_pt[0] + max_pt[0]) / 2,
                (min_pt[1] + max_pt[1]) / 2,
            )
            viewport.dxf.view_height = max(extent_width, extent_height) * 1.05
        except Exception:
            pass

        return viewport

    @staticmethod
    def freeze_layer_in_vp(viewport, layer_name: str):
        """在视口中冻结指定图层"""
        try:
            viewport.freeze([layer_name])
        except Exception:
            pass
