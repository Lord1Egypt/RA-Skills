"""图块定义与插入"""
from typing import Tuple, Optional
import ezdxf


class BlockLib:
    """图块库操作"""

    @staticmethod
    def define(doc: ezdxf.document.Drawing,
               name: str,
               base_point: Tuple[float, float] = (0, 0),
               description: str = '') -> ezdxf.layouts.BlockLayout:
        """
        定义新图块（返回块空间，可在其中绘制内容）
        
        Args:
            name: 块名
            base_point: 插入基点 (x, y)
        """
        return doc.blocks.new(name, base_point=(base_point[0], base_point[1], 0))

    @staticmethod
    def insert(msp,
               block_name: str,
               insert_point: Tuple[float, float],
               scale: float = 1.0,
               rotation: float = 0,
               layer: str = '0',
               color: int = 7):
        """
        插入已定义的图块
        
        Returns:
            INSERT 实体，或 None 如果块不存在
        """
        try:
            return msp.add_blockref(
                block_name,
                (insert_point[0], insert_point[1]),
                dxfattribs={
                    'xscale': scale,
                    'yscale': scale,
                    'rotation': rotation,
                    'layer': layer,
                    'color': color,
                }
            )
        except Exception as e:
            print(f"[WARN] 图块 '{block_name}' 不存在或无法插入: {e}")
            return None

    @staticmethod
    def insert_array(msp,
                     block_name: str,
                     start_point: tuple,
                     rows: int = 1,
                     cols: int = 1,
                     row_spacing: float = 0,
                     col_spacing: float = 0,
                     scale: float = 1.0) -> list:
        """矩形阵列插入图块"""
        results = []
        for r in range(rows):
            for c in range(cols):
                px = start_point[0] + c * col_spacing
                py = start_point[1] + r * row_spacing
                ref = BlockLib.insert(msp, block_name, (px, py), scale)
                if ref:
                    results.append(ref)
        return results

    @staticmethod
    def list_blocks(doc: ezdxf.document.Drawing) -> dict:
        """列出文档中所有已定义的图块"""
        result = {}
        for name in doc.blocks.names():
            blk = doc.blocks.get(name)
            entities_count = len(list(blk))
            result[name] = {
                'entity_count': entities_count,
                'base_point': getattr(blk.block.dxf, 'base_point', None),
            }
        return result

    # ━━━━━━━━━ 预定义标准图块 ━━━━━━━━━

    @staticmethod
    def create_standard_blocks(doc: ezdxf.document.Drawing):
        """创建一组常用标准图块"""
        from entities.basic import BasicEntities
        from entities.curves import CurveEntities

        # --- 指北针 ---
        nc_blk = BlockLib.define(doc, '_NORTH_ARROW', (0, 0), '指北针')
        nmsp = nc_blk
        CurveEntities.circle(nmsp, (0, 0), 5, layer='0', color=7, lineweight=35)
        BasicEntities.line(nmsp, (-2, -4), (0, 6), layer='0', color=1)
        BasicEntities.line(nmsp, (2, -4), (0, 6), layer='0', color=1)
        BasicEntities.line(nmsp, (0, 6), (0, 8), layer='0', color=1)
        from entities.text import TextEntity
        TextEntity.text(nmsp, 'N', (0, 9), height=2, halign='CENTER', color=1)

        # --- 标高符号 ---
        elev_blk = BlockLib.define(doc, '_ELEVATION_MARK', (0, 0), '标高符号')
        esp = elev_blk.layout()
        BasicEntities.line(esp, (0, 3), (-5, 8), layer='0', color=7)
        BasicEntities.line(esp, (0, 3), (5, 8), layer='0', color=7)
        BasicEntities.line(esp, (-5, 8), (-3, 8), layer='0', color=7)
        TextEntity.text(esp, '%%P0.000', (6, 6), height=2.5, halign='LEFT', color=7)

        # --- 剖切符号 ---
        section_blk = BlockLib.define(doc, '_SECTION_MARK', (0, 0), '剖切符号')
        ssp = section_blk.layout()
        BasicEntities.line(ssp, (0, -5), (0, 5), layer='0', color=1, lineweight=50)
        CurveEntities.circle(ssp, (0, -5), 1.5, layer='0', color=1)
        CurveEntities.circle(ssp, (0, 5), 1.5, layer='0', color=1)

        # --- 轴网编号圆 ---
        grid_blk = BlockLib.define(doc, '_GRID_BUBBLE', (0, 0), '轴号圆圈')
        gsp = grid_blk.layout()
        CurveEntities.circle(gsp, (0, 0), 4, layer='0', color=7, lineweight=25)
        TextEntity.text(gsp, 'A', (0, -1.3), height=3, halign='CENTER', valign='MIDDLE', color=7)

        return ['_NORTH_ARROW', '_ELEVATION_MARK', '_SECTION_MARK', '_GRID_BUBBLE']
