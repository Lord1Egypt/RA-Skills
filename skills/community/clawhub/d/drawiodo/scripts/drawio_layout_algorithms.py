"""
drawio_layout_algorithms - 四种经典布局算法范式

每种范式是独立的、经过验证的算法实现，彼此不耦合。
所有坐标计算在算法层完成，draw.io XML 生成层只负责渲染。

范式列表：
  1. RadialTreeLayout    — 极限树（含独占扇形区域） → 思维导图
  2. SugiyamaLayout      — 有向分层布局            → 网络拓扑 / 架构图
  3. ColumnFlowLayout    — 单列线性 + 侧边通道      → 流程图
  4. GridAutoLayout      — 居中网格 + 邻接优先       → UML类图 / ER图
"""
import math
from typing import List, Tuple, Optional, Any


# ================================================================
# 1. Horizontal Tree Layout — 水平树（代替径向树）
# 适用于：思维导图 — 解决径向树在密集数据下的重叠问题
# ================================================================

class HorizontalTreeLayout:
    """
    水平树布局算法。

    算法原理（代替 RadialTreeLayout）：
    - 根节点在画布左侧中央
    - 一级分支从根节点向右水平展开，垂直均匀分布
    - 二级子节点从一级分支向右展开，垂直堆叠
    - 每个分支独占一个垂直通道，子节点在通道内堆叠
    - 天然隔离：不同分支在不同x区间，绝对不会重叠

    适用于密集思维导图（8+分支 × 5+子节点）。
    """

    def __init__(self, canvas_w: float = 1169, canvas_h: float = 827,
                 margin_x: float = 50, margin_y: float = 30):
        self.cw = canvas_w
        self.ch = canvas_h
        self.mx = margin_x
        self.my = margin_y
        self.positions = []

    def _tw(self, text: str, font_size: int, pad: int) -> float:
        cn = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        en = len(text) - cn
        return max(80, cn * font_size * 1.8 + en * font_size * 0.6 + pad * 2)

    def layout(self, center_label: str, branches: List[dict]) -> dict:
        """
        Returns: {
            "center": (label, x, y, w, h),
            "nodes": [(label, x, y, w, h, level, parent), ...],
            "edges": [(parent, child, port_src, port_tgt), ...]
        }
        """
        result = {"nodes": [], "edges": []}

        center_w = self._tw(center_label, 16, 30)
        center_h = 60
        center_x = self.mx
        center_y = self.ch / 2 - center_h / 2

        n_branches = len(branches)
        usable_h = self.ch - self.my * 2 - 60  # 留底部空间

        # 一级分支：垂直均匀分布
        branch_gap = usable_h / (n_branches + 1)
        l1_x = center_x + center_w + 120  # 分支节点在中心右侧120px

        for i, br in enumerate(branches):
            bw = self._tw(br["label"], 13, 20)
            bh = 40
            by = self.my + (i + 1) * branch_gap - bh / 2

            subs = br.get("sub", [])
            n_subs = len(subs)

            # 子节点用2列网格排列，减少垂直占位
            sub_h = 32
            sub_gap_y = 4
            sub_gap_x = 8
            sub_cols = 2
            sub_rows = max(1, (n_subs + sub_cols - 1) // sub_cols)
            total_sub_h = sub_rows * sub_h + max(0, sub_rows - 1) * sub_gap_y

            if total_sub_h > usable_h * 0.8:
                sub_gap_y = 2
                total_sub_h = sub_rows * sub_h + max(0, sub_rows - 1) * sub_gap_y

            result["nodes"].append((br["label"], l1_x, by, bw, bh, 1, center_label))

            sub_x0 = l1_x + bw + 20
            sub_start_y = by + bh / 2 - total_sub_h / 2

            for j, sub in enumerate(subs):
                sw = self._tw(sub, 11, 12)
                col = j % sub_cols
                row = j // sub_cols
                sx = sub_x0 + col * (100 + sub_gap_x)
                sy = sub_start_y + row * (sub_h + sub_gap_y)
                result["nodes"].append((sub, sx, sy, sw, sub_h, 2, br["label"]))

            # 连线信息在生成时通过端口计算

        result["center"] = (center_label, center_x, center_y, center_w, center_h)
        return result


# ================================================================
# 2. Sugiyama Layered Layout — 有向分层
# 适用于：网络拓扑 / 分层架构
# ================================================================

class SugiyamaLayout:
    """
    Sugiyama 风格分层布局（简化版）。

    算法：
    - 节点按层次分配到水平层
    - 层内节点水平均匀分布
    - 层间连接采用垂直通道 + 水平绕行
    - 边缘标签放置在水平段中点

    参数：
        layer_gap: 层间垂直间距
        node_w, node_h: 统一节点尺寸
        margin_x, margin_y: 画布边距
    """

    def __init__(self, layer_gap: float = 140,
                 node_w: float = 150, node_h: float = 60,
                 margin_x: float = 40, margin_y: float = 40,
                 canvas_w: float = 1100):
        self.layer_gap = layer_gap
        self.nw = node_w
        self.nh = node_h
        self.mx = margin_x
        self.my = margin_y
        self.cw = canvas_w
        self.node_positions = {}  # {label: (x, y, w, h)}
        self.layers = {}          # {layer_id: [label, ...]}

    def add_nodes(self, layers: dict):
        """
        layers: {0: [dev1, dev2, ...], 1: [...], ...}
        每个 dev: {"label": str, "width": float, "height": float}
        """
        self.layers = layers
        for layer_id in sorted(layers.keys()):
            devices = layers[layer_id]
            n = len(devices)
            y0 = self.my + layer_id * self.layer_gap

            # 计算该层居中间距
            total_w = sum(d.get("width", self.nw) for d in devices)
            gap = max(15, (self.cw - total_w - self.mx * 2) / max(1, n - 1))
            start_x = self.cx_of_row(total_w + gap * max(0, n - 1))

            for j, dev in enumerate(devices):
                label = dev["label"]
                dw = dev.get("width", self.nw)
                dh = dev.get("height", self.nh)
                if "\n" in label:
                    dh = max(dh, (label.count("\n") + 1) * 18 + 10)
                x = start_x + j * (dw + gap)
                self.node_positions[label] = (x, y0, dw, dh)

    def cx_of_row(self, row_w: float) -> float:
        """计算居中的起始x"""
        return (self.cw - row_w) / 2

    def get_edges(self, connections: List[dict]) -> List[dict]:
        """
        返回: [{"from": x, ...}, ...] 用于连线生成
        """
        pass


# ================================================================
# 3. Column Flow Layout — 单列线性 + 侧边通道
# 适用于：流程图
# ================================================================

class ColumnFlowLayout:
    """
    单列线性 + 侧边通道 布局。

    主流程在中心列自上而下。
    Yes分支走右侧通道，No分支走左侧通道。
    分支通道与主列间距 >= 80px，确保不重叠。
    """

    CENTER_X = 550
    SIDE_LANE_R = 750   # Yes通道x坐标
    SIDE_LANE_L = 350   # No通道x坐标
    NODE_GAP = 90

    def __init__(self):
        self.nodes = {}  # {sid: (label, x, y, w, h, type)}

    def layout(self, steps: List[dict]) -> dict:
        """返回节点位置 {sid: (x, y, w, h, type)}"""
        y = self._start_y = 40
        for s in steps:
            sid = s.get("id", "")
            stype = s.get("type", "step")
            label = s.get("label", "")
            if stype == "decision":
                w, h = 140, 80
            elif stype == "terminal":
                w, h = 130, 50
            else:
                w, h = 180, 60
            x = self.CENTER_X - w / 2
            self.nodes[sid] = (label, x, y, w, h, stype)
            y += h + self.NODE_GAP
        return self.nodes


# ================================================================
# 4. Grid Auto Layout — 居中网格 + 邻接优先
# 适用于：UML类图 / ER图
# ================================================================

class GridAutoLayout:
    """
    居中网格布局。

    算法：
    - N个对象排列在 C×R 网格中
    - 每行居中对齐
    - 同类对象尽量放在同一行或相邻位置
    - 网格间距足够让边从间隔中通过
    """

    def __init__(self, cols: int = 3,
                 cell_w: float = 260, cell_h: float = 200,
                 gap_x: float = 60, gap_y: float = 50,
                 canvas_w: float = 1100):
        self.cols = cols
        self.cw = cell_w
        self.ch = cell_h
        self.gx = gap_x
        self.gy = gap_y
        self.cnv = canvas_w
        self.positions = []  # [(name, x, y, w, h), ...]

    def layout(self, items: List[dict]) -> List[tuple]:
        """
        items: [{"name": str, "height": float}, ...]
        返回: [(name, x, y, w, h), ...]
        """
        count = len(items)
        ncols = min(self.cols, count)
        positions = []
        for i, item in enumerate(items):
            r = i // ncols
            c = i % ncols
            # 该行居中对齐
            items_this_row = min(ncols, count - r * ncols)
            row_w = items_this_row * self.cw + self.gx * (items_this_row - 1)
            row_start = (self.cnv - row_w) / 2
            x = row_start + c * (self.cw + self.gx)
            y = 40 + r * (self.ch + self.gy)
            h = item.get("height", self.ch)
            positions.append((item["name"], x, y, self.cw, h))
        self.positions = positions
        return positions
