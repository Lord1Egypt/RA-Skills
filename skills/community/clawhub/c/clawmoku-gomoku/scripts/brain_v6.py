#!/usr/bin/env python3
"""
五子棋大脑 V6 = V5 + VCF 搜索 + 反 VCF

V5 → V6 改进：
  1. VCF 搜索（Victory by Continuous Four）：通过连续冲四找到必胜路径
  2. 反 VCF：检测对手是否有 VCF 路径，提前破坏
  3. 决策树新增 P1.5（我方 VCF）和 P2.5（对手 VCF）优先级

兼容接口：GomokuBrainV6.think(color_str) → (x, y, comment)
"""

from __future__ import annotations

import random
import time
from typing import List, Tuple, Dict, Set, Optional
from dataclasses import dataclass
from enum import Enum


class Color(Enum):
    BLACK = "black"
    WHITE = "white"


@dataclass
class Pattern:
    type: str
    positions: List[Tuple[int, int]]
    empty_spots: List[Tuple[int, int]]
    direction: Tuple[int, int]
    score: int


class GomokuBrainV6:

    BOARD_SIZE = 15
    DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]

    SCORES = {
        "five": 100000, "open4": 50000, "double4": 45000,
        "rush4": 10000, "jump_open4": 40000, "open3": 1000,
        "double3": 8000, "jump_open3": 800, "sleep3": 100, "open2": 50,
    }

    def __init__(self, stones_data: List[Dict]):
        self.board = [[None] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        self.stones = []
        for s in stones_data:
            color = Color.BLACK if s["color"] == "black" else Color.WHITE
            self.stones.append({"x": s["x"], "y": s["y"], "color": color})
            self.board[s["x"]][s["y"]] = color

    # ==================== 基础工具 ====================

    def is_valid(self, x: int, y: int) -> bool:
        return 0 <= x < self.BOARD_SIZE and 0 <= y < self.BOARD_SIZE

    def get_line(self, x, y, dx, dy, length=9):
        result = []
        start = length // 2
        for i in range(length):
            nx, ny = x - start * dx + i * dx, y - start * dy + i * dy
            if self.is_valid(nx, ny):
                result.append((nx, ny, self.board[nx][ny]))
            else:
                result.append((nx, ny, "out"))
        return result

    def _get_nearby_empties(self, radius=3) -> Set[Tuple[int, int]]:
        empties = set()
        for s in self.stones:
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    nx, ny = s["x"] + dx, s["y"] + dy
                    if self.is_valid(nx, ny) and self.board[nx][ny] is None:
                        empties.add((nx, ny))
        return empties

    # ==================== 棋型识别（同 V5） ====================

    def analyze_line_patterns(self, x, y, dx, dy, color) -> List[Pattern]:
        patterns = []
        line = self.get_line(x, y, dx, dy, 9)
        symbols = []
        for _, (px, py, c) in enumerate(line):
            if c == "out": symbols.append("#")
            elif c is None: symbols.append("_")
            elif c == color: symbols.append("O")
            else: symbols.append("X")
        line_str = "".join(symbols)

        if "OOOOO" in line_str:
            idx = line_str.find("OOOOO")
            pos = [(line[i][0], line[i][1]) for i in range(idx, idx + 5) if line[i][2] == color]
            patterns.append(Pattern("five", pos, [], (dx, dy), self.SCORES["five"]))

        if "_OOOO_" in line_str:
            idx = line_str.find("_OOOO_")
            emp = [(line[idx][0], line[idx][1]), (line[idx+5][0], line[idx+5][1])]
            pos = [(line[i][0], line[i][1]) for i in range(idx+1, idx+5)]
            patterns.append(Pattern("open4", pos, emp, (dx, dy), self.SCORES["open4"]))

        for jp in ["O_OOO", "OO_OO", "OOO_O"]:
            if jp in line_str:
                idx = line_str.find(jp)
                ei = idx + jp.find("_")
                pos = [(line[i][0], line[i][1]) for i in range(idx, idx+5) if line[i][2] == color]
                patterns.append(Pattern("rush4", pos, [(line[ei][0], line[ei][1])], (dx, dy), self.SCORES["rush4"]))

        for rp, eis in [("XOOOO_",[5]),("_OOOOX",[0]),("X_OOOO",[1]),("OOOO_X",[4]),("#OOOO_",[5]),("_OOOO#",[0])]:
            if rp in line_str:
                idx = line_str.find(rp)
                pos = [(line[i][0], line[i][1]) for i in range(idx, idx+len(rp)) if line[i][2] == color]
                emp = [(line[idx+e][0], line[idx+e][1]) for e in eis]
                patterns.append(Pattern("rush4", pos, emp, (dx, dy), self.SCORES["rush4"]))

        for p in ["__OOO__", "_O_OO_", "_OO_O_"]:
            if p in line_str:
                idx = line_str.find(p)
                pos = [(line[i][0], line[i][1]) for i in range(idx, idx+len(p)) if line[i][2] == color]
                emp = [(line[i][0], line[i][1]) for i in range(idx, idx+len(p)) if line[i][2] is None]
                patterns.append(Pattern("open3", pos, emp, (dx, dy), self.SCORES["open3"]))

        for p in ["__OOO_X", "__OOO_#", "X_OOO__", "#_OOO__"]:
            if p in line_str:
                idx = line_str.find(p)
                pos = [(line[i][0], line[i][1]) for i in range(idx, idx+len(p)) if line[i][2] == color]
                emp = [(line[i][0], line[i][1]) for i in range(idx, idx+len(p)) if line[i][2] is None]
                patterns.append(Pattern("open3", pos, emp, (dx, dy), self.SCORES["open3"]))

        for p in ["X_OOO_X", "#_OOO_X", "X_OOO_#", "#_OOO_#"]:
            if p in line_str:
                idx = line_str.find(p)
                pos = [(line[i][0], line[i][1]) for i in range(idx, idx+len(p)) if line[i][2] == color]
                emp = [(line[i][0], line[i][1]) for i in range(idx, idx+len(p)) if line[i][2] is None]
                patterns.append(Pattern("sleep3", pos, emp, (dx, dy), self.SCORES["sleep3"]))

        return patterns

    def find_all_patterns(self, color) -> List[Pattern]:
        all_p = []
        for s in self.stones:
            if s["color"] != color: continue
            for dx, dy in self.DIRECTIONS:
                all_p.extend(self.analyze_line_patterns(s["x"], s["y"], dx, dy, color))
        seen = set()
        unique = []
        for p in all_p:
            key = (p.type, tuple(sorted(p.positions)))
            if key not in seen:
                seen.add(key)
                unique.append(p)
        return unique

    # ==================== 威胁检测（同 V5） ====================

    def find_win_points(self, color) -> set:
        pts = set()
        for p in self.find_all_patterns(color):
            if p.type in ("open4", "jump_open4", "rush4", "five"):
                for ep in p.empty_spots:
                    if self.is_valid(*ep) and self.board[ep[0]][ep[1]] is None:
                        pts.add(ep)
        return pts

    def find_threat_creation_points(self, color) -> Tuple[set, set]:
        urgent, secondary = set(), set()
        for ex, ey in self._get_nearby_empties(radius=2):
            self.board[ex][ey] = color
            level = None
            for dx, dy in self.DIRECTIONS:
                for p in self.analyze_line_patterns(ex, ey, dx, dy, color):
                    if p.type in ("open4", "jump_open4"):
                        level = "open4"; break
                    elif p.type == "rush4" and level is None:
                        level = "rush4"
                if level == "open4": break
            self.board[ex][ey] = None
            if level == "open4": urgent.add((ex, ey))
            elif level == "rush4": secondary.add((ex, ey))
        return urgent, secondary

    def find_forced_moves(self, color):
        forced = []
        for p in self.find_all_patterns(color):
            if p.type in ("five", "open4", "jump_open4", "rush4"):
                for ex, ey in p.empty_spots:
                    forced.append((ex, ey, f"{p.type}_threat"))
        return forced

    def find_double_threats(self, color):
        threats = []
        for x, y in self._get_nearby_empties(radius=3):
            self.board[x][y] = color
            pats = self.find_all_patterns(color)
            self.board[x][y] = None
            o3 = len([p for p in pats if p.type == "open3"])
            r4 = len([p for p in pats if p.type in ("rush4", "jump_open4")])
            o4 = len([p for p in pats if p.type == "open4"])
            if o4 >= 1: threats.append((x, y, "open4_created"))
            elif r4 >= 2: threats.append((x, y, "double4"))
            elif o3 >= 2: threats.append((x, y, "double3"))
            elif r4 >= 1 and o3 >= 1: threats.append((x, y, "rush4+open3"))
        return threats

    # ==================== VCF 搜索（V6 核心） ====================

    def _find_four_creating_moves(self, color) -> List[Tuple[int, int, set]]:
        """找出所有能创建四（冲四/活四/五连）的落子点。
        返回 [(x, y, win_points), ...] win_points 为成五的空位集合。
        """
        moves = []
        for ex, ey in self._get_nearby_empties(radius=2):
            self.board[ex][ey] = color
            wins = set()
            is_five = False
            for dx, dy in self.DIRECTIONS:
                for p in self.analyze_line_patterns(ex, ey, dx, dy, color):
                    if p.type == "five":
                        is_five = True
                        break
                    if p.type in ("open4", "jump_open4", "rush4"):
                        for ep in p.empty_spots:
                            if self.is_valid(*ep) and self.board[ep[0]][ep[1]] is None:
                                wins.add(ep)
                if is_five:
                    break
            self.board[ex][ey] = None
            if is_five:
                moves.append((ex, ey, {(ex, ey)}))  # 标记为直接五连
            elif wins:
                moves.append((ex, ey, wins))
        # 排序：win_points 多的优先（open4 > rush4），然后按位置离中心近
        center = self.BOARD_SIZE // 2
        moves.sort(key=lambda m: (-len(m[2]), abs(m[0]-center) + abs(m[1]-center)))
        return moves

    def vcf_search(self, color: Color, max_depth: int = 15, time_limit: float = 2.0) -> Optional[List[Tuple[int, int]]]:
        """VCF 搜索：通过连续冲四找到必胜路径。

        原理：
          攻方每步下冲四 → 守方只有 1 个堵点（被迫）→ 攻方再下冲四 → ...
          直到攻方形成五连或活四（两端堵不住）→ 必胜。

        搜索空间极小（每步 3-10 个冲四选择，守方只有 1 种应对），
        可以轻松搜到 15 层深度。

        Returns: 必胜落子序列 [(x,y), ...] 或 None
        """
        opp = Color.BLACK if color == Color.WHITE else Color.WHITE
        deadline = time.time() + time_limit

        def _search(depth: int) -> Optional[List[Tuple[int, int]]]:
            if depth > max_depth or time.time() > deadline:
                return None

            four_moves = self._find_four_creating_moves(color)
            if not four_moves:
                return None

            for mx, my, wins in four_moves:
                self.board[mx][my] = color

                # 检查是否直接五连
                is_five = False
                for dx, dy in self.DIRECTIONS:
                    for p in self.analyze_line_patterns(mx, my, dx, dy, color):
                        if p.type == "five":
                            is_five = True
                            break
                    if is_five:
                        break
                if is_five:
                    self.board[mx][my] = None
                    return [(mx, my)]

                # 重新计算落子后的赢点
                actual_wins = set()
                for dx, dy in self.DIRECTIONS:
                    for p in self.analyze_line_patterns(mx, my, dx, dy, color):
                        if p.type in ("open4", "jump_open4", "rush4"):
                            for ep in p.empty_spots:
                                if self.is_valid(*ep) and self.board[ep[0]][ep[1]] is None:
                                    actual_wins.add(ep)

                if len(actual_wins) >= 2:
                    # 活四/双杀：守方堵不住
                    self.board[mx][my] = None
                    return [(mx, my)]

                if len(actual_wins) == 1:
                    bx, by = next(iter(actual_wins))
                    self.board[bx][by] = opp

                    # 检查守方的堵子是否意外形成五连（极端情况）
                    opp_five = False
                    for dx, dy in self.DIRECTIONS:
                        for p in self.analyze_line_patterns(bx, by, dx, dy, opp):
                            if p.type == "five":
                                opp_five = True
                                break
                        if opp_five:
                            break

                    if not opp_five:
                        result = _search(depth + 1)
                        if result is not None:
                            self.board[bx][by] = None
                            self.board[mx][my] = None
                            return [(mx, my)] + result

                    self.board[bx][by] = None

                self.board[mx][my] = None

            return None

        return _search(0)

    def find_vcf_disruption(self, opp: Color) -> Optional[List[Tuple[int, int]]]:
        """如果对手有 VCF，找出能破坏它的落子点。

        方法：拿到对手的 VCF 序列，尝试在序列中的每个攻方落子点
        放上我方棋子，检查 VCF 是否还成立。
        """
        my = Color.BLACK if opp == Color.WHITE else Color.WHITE

        vcf_seq = self.vcf_search(opp, max_depth=12, time_limit=1.5)
        if vcf_seq is None:
            return None

        # 只取 VCF 序列中攻方的落子点（奇数步）
        attacker_moves = vcf_seq[::2] if len(vcf_seq) > 0 else []
        # 加上序列中守方的堵点（偶数步），我方也可以抢先占据
        all_candidates = list(dict.fromkeys(vcf_seq))  # 去重保序

        disruption_points = []
        for px, py in all_candidates:
            if self.board[px][py] is not None:
                continue
            self.board[px][py] = my
            remaining = self.vcf_search(opp, max_depth=10, time_limit=0.5)
            self.board[px][py] = None
            if remaining is None:
                disruption_points.append((px, py))

        return disruption_points if disruption_points else None

    # ==================== 评估（同 V5） ====================

    def evaluate_move(self, x, y, my_color, depth=1) -> int:
        if not self.is_valid(x, y) or self.board[x][y] is not None:
            return -1
        opp = Color.BLACK if my_color == Color.WHITE else Color.WHITE

        self.board[x][y] = my_color
        my_p = self.find_all_patterns(my_color)
        for p in my_p:
            if p.type == "five":
                self.board[x][y] = None; return 100000
        for p in my_p:
            if p.type in ("open4", "jump_open4"):
                self.board[x][y] = None; return 50000

        dt = self.find_double_threats(my_color)
        for tx, ty, desc in dt:
            if tx == x and ty == y:
                m = {"double4":45000,"open4_created":50000,"double3":8000,"rush4+open3":6000}
                self.board[x][y] = None; return m.get(desc, 5000)

        attack = sum(self.SCORES.get(p.type, 0) for p in my_p if (x,y) in p.empty_spots or (x,y) in p.positions)

        if depth > 0:
            fm = self.find_forced_moves(opp)
            resp = 0
            if fm:
                ox, oy, _ = fm[0]
                self.board[ox][oy] = opp
                for p in self.find_all_patterns(opp):
                    if p.type == "five": resp = max(resp, 80000)
                    elif p.type in ("open4", "jump_open4"): resp = max(resp, 40000)
                self.board[ox][oy] = None
            attack -= resp * 0.5

        self.board[x][y] = None

        defense = 0
        self.board[x][y] = opp
        for p in self.find_all_patterns(opp):
            if (x, y) in p.empty_spots:
                d = {"five":100000,"open4":50000,"jump_open4":50000,"rush4":10000,"open3":1500,"sleep3":200}
                defense += d.get(p.type, 0)
        self.board[x][y] = None
        defense = int(defense * 1.3)

        center = self.BOARD_SIZE // 2
        pos_score = max(0, (10 - abs(x-center) - abs(y-center)) * 3)
        total = int(attack + defense + pos_score)
        return max(total, -50000)

    def get_best_moves(self, color_str, top_n=10):
        my = Color.BLACK if color_str == "black" else Color.WHITE
        cands = []
        positions = self._get_nearby_empties(radius=3) or {(7, 7)}
        for x, y in positions:
            sc = self.evaluate_move(x, y, my, depth=1)
            if sc > 0:
                cands.append((x, y, sc, self._get_reason(x, y, my)))
        cands.sort(key=lambda c: -c[2])
        return cands[:top_n]

    def _get_reason(self, x, y, my_color) -> str:
        reasons = []
        opp = Color.BLACK if my_color == Color.WHITE else Color.WHITE
        labels_atk = {"five":"✅五连获胜","open4":"🔥活四必胜","rush4":"⚡冲四","open3":"📈活三"}
        labels_def = {"five":"🛡️封五连","open4":"🛡️封活四","rush4":"🛡️封冲四","open3":"🛡️封活三"}

        self.board[x][y] = my_color
        for p in self.find_all_patterns(my_color):
            if (x,y) in p.positions or (x,y) in p.empty_spots:
                l = labels_atk.get(p.type)
                if l and l not in reasons: reasons.append(l)
        self.board[x][y] = None

        self.board[x][y] = opp
        for p in self.find_all_patterns(opp):
            if (x,y) in p.empty_spots:
                l = labels_def.get(p.type)
                if l and l not in reasons: reasons.append(l)
        self.board[x][y] = None
        return "+".join(reasons) if reasons else "扩展"

    # ==================== 决策（V6 重写） ====================

    def think(self, my_color_str: str) -> Tuple[int, int, str]:
        """
        V6 决策树：
        P1   我一步五连 → 赢
        P1.5 我有 VCF → 执行第一步（必胜）
        P2   对手一步五连 → 堵
        P2.5 对手有 VCF → 破坏
        P3   对手有威胁 → 防守
        P4   常规评分 + 随机
        """
        my = Color.BLACK if my_color_str == "black" else Color.WHITE
        opp = Color.BLACK if my == Color.WHITE else Color.WHITE

        # P1: 我一步五连
        my_win = self.find_win_points(my)
        if my_win:
            x, y = sorted(my_win)[0]
            return (x, y, f"🏆 五连制胜 ({x},{y})")

        # P1.5: 我有 VCF（连续冲四必胜）
        vcf = self.vcf_search(my, max_depth=15, time_limit=2.0)
        if vcf:
            x, y = vcf[0]
            steps = len(vcf)
            return (x, y, f"🔥 VCF 必胜路径（{steps}步） ({x},{y})")

        # P2: 对手一步五连
        opp_win = self.find_win_points(opp)
        if len(opp_win) >= 2:
            for px, py in sorted(opp_win):
                self.board[px][py] = my
                after = self.find_all_patterns(my)
                self.board[px][py] = None
                for p in after:
                    if p.type in ("open4", "jump_open4", "rush4"):
                        return (px, py, f"⚔️ 挣扎反扑 ({px},{py}) 堵+{p.type}")
            x, y = sorted(opp_win)[0]
            return (x, y, f"💀 对手双杀，挣扎 ({x},{y})")
        if len(opp_win) == 1:
            x, y = next(iter(opp_win))
            return (x, y, f"🛡️ 封对手五连点 ({x},{y})")

        # P2.5: 对手有 VCF → 找破坏点
        disruption = self.find_vcf_disruption(opp)
        if disruption:
            # 在破坏点中选评分最高的
            best, best_sc = None, -1
            for dx, dy in disruption:
                sc = self.evaluate_move(dx, dy, my, depth=1)
                if sc > best_sc:
                    best_sc = sc
                    best = (dx, dy)
            if best:
                return (best[0], best[1], f"🛡️ 破坏对手 VCF ({best[0]},{best[1]})")

        # P3: 对手威胁
        opp_urgent, opp_secondary = self.find_threat_creation_points(opp)
        moves = self.get_best_moves(my_color_str, top_n=15)
        if not moves:
            return (7, 7, "开局天元")

        opp_must_block = opp_urgent if opp_urgent else opp_secondary
        if opp_must_block:
            for x, y, sc, r in moves:
                if (x, y) in opp_must_block:
                    return (x, y, f"⚖️ 攻守兼备 ({x},{y}) 堵威胁+{r}")
            top_x, top_y, _, top_r = moves[0]
            if "活四" in top_r or "冲四" in top_r:
                return (top_x, top_y, f"⚡ 抢先 ({top_x},{top_y}) {top_r}")
            best_block, best_sc = None, -1
            for ex, ey in opp_must_block:
                sc = self.evaluate_move(ex, ey, my, depth=1)
                if sc > best_sc:
                    best_sc = sc
                    best_block = (ex, ey)
            if best_block:
                return (best_block[0], best_block[1], f"🛡️ 堵威胁 ({best_block[0]},{best_block[1]})")

        # P4: 常规评分 + 随机
        x, y, score, reason = moves[0]
        if len(moves) > 1 and score > 0:
            threshold = score * 0.95
            similar = [(mx, my, ms, mr) for mx, my, ms, mr in moves if ms >= threshold]
            if len(similar) > 1:
                x, y, score, reason = random.choice(similar)

        if "五连" in reason: c = f"🏆 五子连珠 ({x},{y})"
        elif "活四" in reason and "封" not in reason: c = f"🔥 形成活四 ({x},{y})"
        elif "双四" in reason or "双三" in reason: c = f"⚡ 双重威胁 ({x},{y})"
        elif "封" in reason: c = f"🛡️ {reason} ({x},{y})"
        else: c = f"选 ({x},{y}) {reason}"
        return (x, y, c)


# ==================== 兼容别名 ====================
GomokuBrainV2 = GomokuBrainV6


# ==================== 回归测试 ====================

def _b(x, y): return {"x": x, "y": y, "color": "black"}
def _w(x, y): return {"x": x, "y": y, "color": "white"}

REGRESSION_CASES = [
    {
        "name": "M2.open4-identify",
        "stones": [_b(7,7),_w(7,6),_b(6,7),_w(6,6),_b(5,7),_w(8,7),_b(5,6),_w(7,8),
                   _b(4,7),_w(3,7),_b(4,6),_w(6,8),_b(8,6),_w(8,8),_b(9,6)],
        "to_move": "white", "forbid": set(),
        "description": "活四识别与防守",
    },
    {
        "name": "diag2-open3-defense",
        "stones": [_b(6,8), _b(7,7), _b(8,6), _w(0,0)],
        "to_move": "white", "expect_in": {(5,9),(9,5)}, "forbid": {(4,10),(10,4)},
        "description": "反对角活三紧邻封堵",
    },
    {
        "name": "M7.open3-horizontal",
        "stones": [_b(7,7),_w(6,7),_b(7,6),_w(8,7),_b(7,8),_w(7,9),
                   _b(7,5),_w(7,4),_b(6,6),_w(5,7),_b(8,6)],
        "to_move": "white", "expect_in": {(5,6),(9,6)}, "forbid": {(4,6),(10,6)},
        "description": "横向活三紧邻堵",
    },
    {
        "name": "V5.asymmetric-open3",
        "stones": [_b(7,7),_w(7,8),_b(6,7),_w(5,7),_b(7,6),_w(5,8),
                   _b(8,7),_w(9,7),_b(9,8),_w(6,5),_b(10,9),_w(11,10),_b(6,6),_w(6,8)],
        "to_move": "black", "expect_in": {(4,8),(8,8)}, "forbid": set(),
        "description": "不对称活三防守",
    },
    # V6 新增：VCF 检测
    {
        "name": "V6.vcf-simple",
        "stones": [
            # 黑方在 y=7 有 (5,7)(6,7)(7,7) 三连 + 在 y=6 有 (5,6)(6,6)(7,6) 三连
            # 黑方先冲四 (8,7) → 白堵 (4,7) 或 (9,7)
            # 然后冲四 (8,6) → 活四
            _b(5,7), _b(6,7), _b(7,7),
            _b(5,6), _b(6,6), _b(7,6),
            _w(0,0), _w(1,1), _w(2,2), _w(3,3),  # 白棋远离
        ],
        "to_move": "black",
        "description": "VCF 检测：双线冲四必胜",
        "check_vcf": True,  # 特殊标记：验证 VCF 能找到必胜路径
    },
]


def run_regressions() -> int:
    failed = 0
    print("=" * 60)
    print("Brain V6 回归测试")
    print("=" * 60)
    for case in REGRESSION_CASES:
        brain = GomokuBrainV6(case["stones"])
        x, y, comment = brain.think(case["to_move"])
        picked = (x, y)
        expect_in = case.get("expect_in")
        forbid = case.get("forbid", set())
        parts = [case["name"], f"picked={picked}", f"comment={comment}"]
        ok = True

        if expect_in and picked not in expect_in:
            ok = False; parts.append(f"❌ not in {sorted(expect_in)}")
        if picked in forbid:
            ok = False; parts.append(f"❌ in forbid")

        # VCF 检测
        if case.get("check_vcf"):
            color = Color.BLACK if case["to_move"] == "black" else Color.WHITE
            vcf = brain.vcf_search(color)
            if vcf is None:
                ok = False; parts.append("❌ VCF 未找到必胜路径")
            else:
                parts.append(f"VCF={len(vcf)}步")

        parts.insert(0, "✅" if ok else "❌")
        if not ok: failed += 1
        print(" ".join(parts))
        print(f"   - {case['description']}")

    print("=" * 60)
    print(f"{'all green' if not failed else f'{failed} FAILED'}")
    return failed


if __name__ == "__main__":
    import sys as _sys
    _sys.exit(run_regressions())
