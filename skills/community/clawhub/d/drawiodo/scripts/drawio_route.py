"""
drawio_route - 互斥布局引擎
碰撞检测 + 障碍感知路由 + 边缘标签定位

核心能力：
1. 节点互斥（CollisionResolver）— 保证任意两节点不重叠
2. 障碍感知路由（ObstacleRouter）— 连接线绕开所有节点
3. 智能端口选择（SmartPort）— 自动选最短且避障的出/入口
"""
import math
from typing import List, Tuple, Optional, Set, Any


# ================================================================
# 矩形碰撞核心
# ================================================================

class Rect:
    """带padding的矩形碰撞体"""
    __slots__ = ('x', 'y', 'w', 'h')

    def __init__(self, x: float, y: float, w: float, h: float):
        self.x, self.y, self.w, self.h = x, y, w, h

    @staticmethod
    def from_node(node) -> 'Rect':
        """从 drawio_gen.Node 构造"""
        return Rect(node.x, node.y, node.width, node.height)

    def left(self): return self.x
    def right(self): return self.x + self.w
    def top(self): return self.y
    def bottom(self): return self.y + self.h
    def cx(self): return self.x + self.w / 2
    def cy(self): return self.y + self.h / 2

    def expanded(self, pad: float) -> 'Rect':
        return Rect(self.x - pad, self.y - pad, self.w + 2 * pad, self.h + 2 * pad)

    def overlaps(self, other: 'Rect') -> bool:
        return not (self.right() <= other.left() or self.left() >= other.right() or
                    self.bottom() <= other.top() or self.top() >= other.bottom())

    def contains(self, px: float, py: float) -> bool:
        return self.left() <= px <= self.right() and self.top() <= py <= self.bottom()

    def __repr__(self):
        return f"Rect({self.x:.0f},{self.y:.0f},{self.w:.0f},{self.h:.0f})"


# ================================================================
# 碰撞解析器 - 迭代分离重叠节点
# ================================================================

class CollisionResolver:
    """
    互斥布局：迭代解决所有节点间的重叠。
    原理：对每对重叠的节点，沿最短分开方向推开。
    """

    MIN_GAP = 20        # 节点间最小间距
    CANVAS_W = 1169     # 画布宽度
    CANVAS_H = 1850     # 画布高度（足够大）
    MARGIN = 20         # 画布安全边距
    MAX_ITER = 30       # 最大迭代次数

    def __init__(self, min_gap: float = None):
        self.min_gap = min_gap or self.MIN_GAP

    def resolve(self, nodes: List[Any],
                # 可选的节点最小x/y约束
                min_xs: dict = None,
                min_ys: dict = None) -> int:
        """
        解析所有节点碰撞。直接修改 node.x, node.y。

        Args:
            nodes: drawio_gen.Node 列表
            min_xs: {node_id: min_x} — x方向的不可移动边界
            min_ys: {node_id: min_y} — y方向的不可移动边界

        Returns: 碰撞对数（0=完全解决）
        """
        node_ids = {n.id: n for n in nodes}
        pairs = len(nodes) * (len(nodes) - 1) // 2
        if pairs == 0:
            return 0

        moved = True
        it = 0
        while moved and it < self.MAX_ITER:
            moved = False
            it += 1
            for i in range(len(nodes)):
                a = nodes[i]
                ra = Rect(a.x, a.y, a.width, a.height).expanded(self.min_gap)
                for j in range(i + 1, len(nodes)):
                    b = nodes[j]
                    rb = Rect(b.x, b.y, b.width, b.height)

                    if not ra.overlaps(rb):
                        continue

                    # 计算重叠量
                    ox = min(ra.right(), rb.right()) - max(ra.left(), rb.left())
                    oy = min(ra.bottom(), rb.bottom()) - max(ra.top(), rb.top())

                    # 沿最短方向推开（较短的重叠方向意味着该方向更接近）
                    if oy <= ox:
                        # 垂直推开
                        push = (oy + self.min_gap) / 2
                        if a.y < b.y:
                            a.y -= push
                            b.y += push
                        else:
                            a.y += push
                            b.y -= push
                        # y 软边界
                        if min_ys:
                            a.y = max(min_ys.get(a.id, -1e6), min(a.y, self.CANVAS_H - a.height))
                            b.y = max(min_ys.get(b.id, -1e6), min(b.y, self.CANVAS_H - b.height))
                    else:
                        # 水平推开
                        push = (ox + self.min_gap) / 2
                        if a.x < b.x:
                            a.x -= push
                            b.x += push
                        else:
                            a.x += push
                            b.x -= push
                        if min_xs:
                            a.x = max(min_xs.get(a.id, -1e6), min(a.x, self.CANVAS_W - a.width))
                            b.x = max(min_xs.get(b.id, -1e6), min(b.x, self.CANVAS_W - b.width))

                    moved = True
                    ra = Rect(a.x, a.y, a.width, a.height).expanded(self.min_gap)

        return pairs


# ================================================================
# 障碍感知路由
# ================================================================

class ObstacleRouter:
    """
    障碍感知正交路由。
    对每条边计算 waypoints 避免穿过任何节点。
    """

    PAD = 5  # 障碍物padding（仅防擦边，避免过度阻挡）

    def __init__(self, pad: float = None):
        self.pad = pad if pad is not None else self.PAD
        self.obstacles: List[Tuple[Rect, str]] = []  # (rect, node_id)

    def clear(self):
        self.obstacles = []

    def add_obstacles(self, nodes: List[Any]):
        """批量添加节点作为障碍物"""
        for n in nodes:
            r = Rect.from_node(n).expanded(self.pad)
            self.obstacles.append((r, n.id))

    def _segment_clear(self, x1: float, y1: float, x2: float, y2: float,
                       exclude: Set[str]) -> bool:
        """检查线段是否与任何障碍物相交"""
        # 构建线段AABB
        sx_min, sx_max = (x1, x2) if x1 <= x2 else (x2, x1)
        sy_min, sy_max = (y1, y2) if y1 <= y2 else (y2, y1)
        seg_rect = Rect(sx_min, sy_min, sx_max - sx_min, sy_max - sy_min)

        for rect, nid in self.obstacles:
            if nid in exclude:
                continue
            if seg_rect.overlaps(rect):
                return False
        return True

    def _path_clear(self, points: List[Tuple[float, float]],
                    exclude: Set[str]) -> bool:
        """检查整条路径是否避开所有障碍"""
        for i in range(len(points) - 1):
            if not self._segment_clear(points[i][0], points[i][1],
                                       points[i + 1][0], points[i + 1][1],
                                       exclude):
                return False
        return True

    @staticmethod
    def _port_point(node, port: int) -> Tuple[float, float]:
        """节点上端口的绝对坐标"""
        ports = {
            0: (node.x + node.width / 2, node.y),                    # 顶部
            1: (node.x + node.width, node.y + node.height / 2),      # 右侧
            2: (node.x + node.width / 2, node.y + node.height),      # 底部
            3: (node.x, node.y + node.height / 2),                   # 左侧
        }
        return ports.get(port, (node.x + node.width / 2, node.y + node.height / 2))

    def route(self, src_node, tgt_node,
              src_port: int = None, tgt_port: int = None,
              default_src: int = 2, default_tgt: int = 0,
              side_lane: str = None) -> List[Tuple[float, float]]:
        """
        计算避开障碍物的正交路径 waypoints。

        核心原则：ALL edges must have at least 1 waypoint.
        因为空 waypoints 会导致 draw.io 使用内置正交路由，
        该路由不感知障碍物，连接线会穿过节点。

        side_lane: None=自动, "left"/"right"=强制走侧边通道

        Returns: waypoints 列表（至少1个点，确保edgeStyle=none生效）
        """
        sx, sy = self._port_point(src_node, src_port if src_port is not None else default_src)
        tx, ty = self._port_point(tgt_node, tgt_port if tgt_port is not None else default_tgt)

        exclude = {src_node.id, tgt_node.id, 'edge_' + src_node.id + '_' + tgt_node.id}

        # === Strategy 1: 标准 L-path (horizontal first) ===
        path_h = [(sx, sy), (tx, sy), (tx, ty)]
        if self._path_clear(path_h, exclude):
            return [(tx, sy)]  # 返回拐点，强制 edgeStyle=none

        # === Strategy 1b: L-path (vertical first) ===
        path_v = [(sx, sy), (sx, ty), (tx, ty)]
        if self._path_clear(path_v, exclude):
            return [(sx, ty)]  # 返回拐点

        # === Strategy 2: 指定侧边通道 (流程图分支) ===
        if side_lane in ('left', 'right'):
            offset = 80 if side_lane == 'right' else -80
            lane_x = src_node.x + (src_node.width + offset if side_lane == 'right' else offset)
            lane_x = max(0, min(self.obstacles[0][0].right() + 200 if self.obstacles else 1169, lane_x))
            if lane_x < 0:
                lane_x = 0

            mid_y = (sy + ty) / 2
            path_lane = [(sx, sy), (lane_x, sy), (lane_x, ty), (tx, ty)]
            if self._path_clear(path_lane, exclude):
                return [(lane_x, sy), (lane_x, ty)]

            # 尝试不同的中间y
            for my in [sy + 30, ty - 30, (sy + ty) / 3, (sy + ty) * 2 / 3]:
                path_lane2 = [(sx, sy), (lane_x, sy), (lane_x, my), (tx, my), (tx, ty)]
                if self._path_clear(path_lane2, exclude):
                    return [(lane_x, sy), (lane_x, my), (tx, my)]

        # === Strategy 3: Z-path (2 bends, shifted) ===
        offsets = [40, 80, 120, 180, -40, -80, -120, -180]
        for off in offsets:
            # 水平先走再垂直
            mx = (sx + tx) / 2 + off
            p3 = [(sx, sy), (mx, sy), (mx, ty), (tx, ty)]
            if self._path_clear(p3, exclude):
                return [(mx, sy), (mx, ty)]

            # 垂直先走再水平
            my = (sy + ty) / 2 + off
            p4 = [(sx, sy), (sx, my), (tx, my), (tx, ty)]
            if self._path_clear(p4, exclude):
                return [(sx, my), (tx, my)]

        # === Strategy 4: 沿障碍物边缘绕行 ===
        # 找到阻挡的障碍物，沿其边缘走
        for rect, nid in self.obstacles:
            if nid in exclude:
                continue
            # 检查此障碍是否落在源-目标之间
            between = Rect(min(sx, tx), min(sy, ty),
                           abs(tx - sx), abs(ty - sy))
            if between.overlaps(rect):
                # 尝试绕过此障碍的4个方向
                candidates = [
                    [(sx, sy), (rect.right(), sy), (rect.right(), ty), (tx, ty)],  # 绕右
                    [(sx, sy), (rect.left(), sy), (rect.left(), ty), (tx, ty)],    # 绕左
                    [(sx, sy), (sx, rect.bottom()), (tx, rect.bottom()), (tx, ty)],  # 绕下
                    [(sx, sy), (sx, rect.top()), (tx, rect.top()), (tx, ty)],        # 绕上
                ]
                for cand in candidates:
                    if self._path_clear(cand, exclude):
                        return cand[1:-1]

        # === Strategy 5: 彻底绕行（绕整个图形区）===
        # 从源先水平到画布边缘，再垂直，再水平到目标
        for edge_x in [0, 1169]:
            cand = [(sx, sy), (edge_x, sy), (edge_x, ty), (tx, ty)]
            if self._path_clear(cand, exclude):
                return [(edge_x, sy), (edge_x, ty)]

        # === Strategy 6: 最终保底 —— 绕所有障碍物的外包围盒 ===
        if not self.obstacles:
            return [(tx, sy)]

        # 计算所有障碍物的外包围盒
        min_ox = min(r.left() for r, _ in self.obstacles)
        max_ox = max(r.right() for r, _ in self.obstacles)
        min_oy = min(r.top() for r, _ in self.obstacles)
        max_oy = max(r.bottom() for r, _ in self.obstacles)
        outer_pad = 30
        outer_left = min_ox - outer_pad
        outer_right = max_ox + outer_pad
        outer_top = min_oy - outer_pad
        outer_bottom = max_oy + outer_pad

        # 4条外围路径: 先到外围角点，再到目标外围角点，再到目标
        # 确保所有垂直/水平段都在外围区域，不穿过任何节点
        candidates = [
            # 左→上/下
            [(sx, sy), (outer_left, sy), (outer_left, outer_top), (tx, outer_top), (tx, ty)],
            [(sx, sy), (outer_left, sy), (outer_left, outer_bottom), (tx, outer_bottom), (tx, ty)],
            # 右→上/下
            [(sx, sy), (outer_right, sy), (outer_right, outer_top), (tx, outer_top), (tx, ty)],
            [(sx, sy), (outer_right, sy), (outer_right, outer_bottom), (tx, outer_bottom), (tx, ty)],
            # 上/下→左/右
            [(sx, sy), (sx, outer_top), (outer_left, outer_top), (outer_left, ty), (tx, ty)],
            [(sx, sy), (sx, outer_bottom), (outer_right, outer_bottom), (outer_right, ty), (tx, ty)],
        ]

        # 选跨越最少的外围路径
        CANVAS_W = 1169
        CANVAS_H = 1500
        best = None
        best_len = float('inf')
        for cand in candidates:
            # 裁剪到画布范围内
            clipped = []
            for px, py in cand:
                clipped.append((max(0, min(CANVAS_W, px)), max(0, min(CANVAS_H, py))))
            # 检查是否穿过节点
            blocked = False
            for k in range(len(cand) - 1):
                x1, y1 = cand[k]
                x2, y2 = cand[k + 1]
                sxmn, smx = (x1, x2) if x1 <= x2 else (x2, x1)
                symn, symx = (y1, y2) if y1 <= y2 else (y2, y1)
                for rect, nid in self.obstacles:
                    if nid in exclude:
                        continue
                    # 用未扩展的原始rect
                    unexpanded = Rect(rect.x + self.pad, rect.y + self.pad,
                                      rect.w - 2 * self.pad, rect.h - 2 * self.pad)
                    # 使用AABB检查
                    if sxmn < unexpanded.right() and smx > unexpanded.left() and \
                       symn < unexpanded.bottom() and symx > unexpanded.top():
                        blocked = True
                        break
                if blocked:
                    break
            if blocked:
                continue
            # 使用裁剪后的坐标
            cand = clipped
            length = sum(abs(cand[k][0] - cand[k + 1][0]) + abs(cand[k][1] - cand[k + 1][1])
                        for k in range(len(cand) - 1))
            if length < best_len:
                best_len = length
                best = cand

        if best:
            return best[1:-1]  # 去掉source和target边缘点
        # 绝对保底
        return [(tx, sy)]

    def route_flowchart_branch(self, src_node, tgt_node, side: str,
                                label: str = "", side_x: float = None) -> Tuple[int, int, List]:
        """
        流程图分支连线的专用路由。
        side='right'=Yes, side='left'=No
        side_x: 自定义侧边通道x坐标（用于多个决策避免标签重叠）
        返回: (src_port, tgt_port, waypoints)
        """
        src_port = 2
        tgt_port = 0
        lane_x = side_x or (750 if side == 'right' else 350)
        # Build a direct lane path
        sx = src_node.x + src_node.width / 2
        sy = src_node.y + src_node.height
        tx = tgt_node.x + tgt_node.width / 2
        ty = tgt_node.y
        waypoints = [(lane_x, sy), (lane_x, ty)]
        return src_port, tgt_port, waypoints


# ================================================================
# 智能端口选择
# ================================================================

def smart_port(src_node, tgt_node) -> Tuple[int, int]:
    """
    智能选择源和目标的连接端口。
    优选最短直线路径。
    """
    scx, scy = src_node.x + src_node.width / 2, src_node.y + src_node.height / 2
    tcx, tcy = tgt_node.x + tgt_node.width / 2, tgt_node.y + tgt_node.height / 2

    dx, dy = tcx - scx, tcy - scy

    # 根据方向选择端口
    if abs(dx) > abs(dy):
        # 水平方向为主
        if dx > 0:
            return 1, 3  # 源右 → 目标左
        else:
            return 3, 1  # 源左 → 目标右
    else:
        # 垂直方向为主
        if dy > 0:
            return 2, 0  # 源底 → 目标顶
        else:
            return 0, 2  # 源顶 → 目标底
