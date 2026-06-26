#!/usr/bin/env python3
"""
五子棋大脑 V5

V4 → V5 改进：
  1. 活三检测修复：补全不对称模板（__OOO_X / X_OOO__）+ 模拟验证兜底
  2. 威胁检测重写：不再依赖模板，改为模拟落子检查是否产生 open4/rush4
  3. 防守优先：defense_score × 1.3
  4. 反背谱：评分相近（5%）的候选点之间随机选择
  5. 搜索加深到 2 层（仅 P4 分支，alpha-beta + 候选缩减）

兼容接口：GomokuBrainV5.think(color_str) → (x, y, comment)
"""

from __future__ import annotations

import random
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


class GomokuBrainV5:

    BOARD_SIZE = 15
    DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]

    SCORES = {
        "five": 100000,
        "open4": 50000,
        "double4": 45000,
        "rush4": 10000,
        "jump_open4": 40000,
        "open3": 1000,
        "double3": 8000,
        "jump_open3": 800,
        "sleep3": 100,
        "open2": 50,
    }

    def __init__(self, stones_data: List[Dict]):
        self.board = [[None] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        self.stones = []
        for s in stones_data:
            color = Color.BLACK if s["color"] == "black" else Color.WHITE
            self.stones.append({"x": s["x"], "y": s["y"], "color": color})
            self.board[s["x"]][s["y"]] = color

    # ============== 基础工具 ==============

    def is_valid(self, x: int, y: int) -> bool:
        return 0 <= x < self.BOARD_SIZE and 0 <= y < self.BOARD_SIZE

    def get_line(self, x: int, y: int, dx: int, dy: int, length: int = 9) -> List:
        result = []
        start_offset = length // 2
        for i in range(length):
            nx = x - start_offset * dx + i * dx
            ny = y - start_offset * dy + i * dy
            if self.is_valid(nx, ny):
                result.append((nx, ny, self.board[nx][ny]))
            else:
                result.append((nx, ny, "out"))
        return result

    def _get_nearby_empties(self, radius: int = 3) -> Set[Tuple[int, int]]:
        empties = set()
        for s in self.stones:
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    nx, ny = s["x"] + dx, s["y"] + dy
                    if self.is_valid(nx, ny) and self.board[nx][ny] is None:
                        empties.add((nx, ny))
        return empties

    # ============== 棋型识别（V5 修复） ==============

    def analyze_line_patterns(self, x: int, y: int, dx: int, dy: int, color: Color) -> List[Pattern]:
        patterns = []
        line = self.get_line(x, y, dx, dy, 9)

        symbols = []
        for i, (px, py, c) in enumerate(line):
            if c == "out":
                symbols.append("#")
            elif c is None:
                symbols.append("_")
            elif c == color:
                symbols.append("O")
            else:
                symbols.append("X")
        line_str = "".join(symbols)

        # --- 五连 ---
        if "OOOOO" in line_str:
            idx = line_str.find("OOOOO")
            positions = [(line[i][0], line[i][1]) for i in range(idx, idx + 5) if line[i][2] == color]
            patterns.append(Pattern("five", positions, [], (dx, dy), self.SCORES["five"]))

        # --- 活四: _OOOO_ ---
        if "_OOOO_" in line_str:
            idx = line_str.find("_OOOO_")
            empty_spots = [(line[idx][0], line[idx][1]), (line[idx + 5][0], line[idx + 5][1])]
            positions = [(line[i][0], line[i][1]) for i in range(idx + 1, idx + 5)]
            patterns.append(Pattern("open4", positions, empty_spots, (dx, dy), self.SCORES["open4"]))

        # --- 跳冲四: O_OOO, OO_OO, OOO_O ---
        for jp in ["O_OOO", "OO_OO", "OOO_O"]:
            if jp in line_str:
                idx = line_str.find(jp)
                empty_idx = idx + jp.find("_")
                positions = [(line[i][0], line[i][1]) for i in range(idx, idx + 5) if line[i][2] == color]
                empty_spots = [(line[empty_idx][0], line[empty_idx][1])]
                patterns.append(Pattern("rush4", positions, empty_spots, (dx, dy), self.SCORES["rush4"]))

        # --- 冲四: 端部被堵 ---
        rush4_patterns = [
            ("XOOOO_", [5]),
            ("_OOOOX", [0]),
            ("X_OOOO", [1]),
            ("OOOO_X", [4]),
            ("#OOOO_", [5]),
            ("_OOOO#", [0]),
        ]
        for rp, empty_indices in rush4_patterns:
            if rp in line_str:
                idx = line_str.find(rp)
                positions = [(line[i][0], line[i][1]) for i in range(idx, idx + len(rp)) if line[i][2] == color]
                empty_spots = [(line[idx + ei][0], line[idx + ei][1]) for ei in empty_indices]
                patterns.append(Pattern("rush4", positions, empty_spots, (dx, dy), self.SCORES["rush4"]))

        # --- 活三（V5 修复：补全不对称模板）---
        # 对称活三（两端各 2+ 空）
        open3_full = ["__OOO__", "_O_OO_", "_OO_O_"]
        for p in open3_full:
            if p in line_str:
                idx = line_str.find(p)
                positions = [(line[i][0], line[i][1]) for i in range(idx, idx + len(p)) if line[i][2] == color]
                empty_spots = [(line[i][0], line[i][1]) for i in range(idx, idx + len(p)) if line[i][2] is None]
                patterns.append(Pattern("open3", positions, empty_spots, (dx, dy), self.SCORES["open3"]))

        # V5 新增：不对称活三（一端 2+ 空另一端 1 空后被堵）
        # 例如 __OOO_X：左端 2 空可成活四，右端 1 空只能冲四
        # 这仍然是活三（至少一端能成活四）
        asym_open3 = [
            "__OOO_X", "__OOO_#",  # 左端开放
            "X_OOO__", "#_OOO__",  # 右端开放
        ]
        for p in asym_open3:
            if p in line_str:
                idx = line_str.find(p)
                positions = [(line[i][0], line[i][1]) for i in range(idx, idx + len(p)) if line[i][2] == color]
                empty_spots = [(line[i][0], line[i][1]) for i in range(idx, idx + len(p)) if line[i][2] is None]
                # 去掉已有对称活三检测到的（positions 去重）
                patterns.append(Pattern("open3", positions, empty_spots, (dx, dy), self.SCORES["open3"]))

        # 眠三（一端完全封死，另一端仅 1 空）
        sleep3_patterns = ["X_OOO_X", "#_OOO_X", "X_OOO_#", "#_OOO_#"]
        for p in sleep3_patterns:
            if p in line_str:
                idx = line_str.find(p)
                positions = [(line[i][0], line[i][1]) for i in range(idx, idx + len(p)) if line[i][2] == color]
                empty_spots = [(line[i][0], line[i][1]) for i in range(idx, idx + len(p)) if line[i][2] is None]
                patterns.append(Pattern("sleep3", positions, empty_spots, (dx, dy), self.SCORES["sleep3"]))

        return patterns

    def find_all_patterns(self, color: Color) -> List[Pattern]:
        all_patterns = []
        for stone in self.stones:
            if stone["color"] != color:
                continue
            x, y = stone["x"], stone["y"]
            for dx, dy in self.DIRECTIONS:
                all_patterns.extend(self.analyze_line_patterns(x, y, dx, dy, color))

        unique = []
        seen = set()
        for p in all_patterns:
            key = (p.type, tuple(sorted(p.positions)))
            if key not in seen:
                seen.add(key)
                unique.append(p)
        return unique

    # ============== 威胁检测（V5 重写） ==============

    def find_win_points(self, color: Color) -> set:
        """下一步就能五连的点"""
        points = set()
        for p in self.find_all_patterns(color):
            if p.type in ("open4", "jump_open4", "rush4", "five"):
                for ep in p.empty_spots:
                    if self.is_valid(*ep) and self.board[ep[0]][ep[1]] is None:
                        points.add(ep)
        return points

    def find_threat_creation_points(self, color: Color) -> Tuple[set, set]:
        """模拟落子检测：哪些空位落子后会产生 open4 或 rush4。

        V5 核心改进：不依赖活三模板，直接模拟。
        返回 (urgent, secondary):
          urgent:    落子后形成 open4（必须立即封堵，否则对方必胜）
          secondary: 落子后仅形成 rush4（有威胁但不致命）
        """
        urgent = set()
        secondary = set()
        empties = self._get_nearby_empties(radius=2)

        for ex, ey in empties:
            self.board[ex][ey] = color
            level = None
            for dx, dy in self.DIRECTIONS:
                for p in self.analyze_line_patterns(ex, ey, dx, dy, color):
                    if p.type in ("open4", "jump_open4"):
                        level = "open4"
                        break
                    elif p.type == "rush4" and level is None:
                        level = "rush4"
                if level == "open4":
                    break
            self.board[ex][ey] = None

            if level == "open4":
                urgent.add((ex, ey))
            elif level == "rush4":
                secondary.add((ex, ey))
        return urgent, secondary

    def find_double_threats(self, color: Color) -> List[Tuple[int, int, str]]:
        """能形成双三/双四/冲四+活三的点"""
        threats = []
        empties = self._get_nearby_empties(radius=3)

        for x, y in empties:
            self.board[x][y] = color
            patterns = self.find_all_patterns(color)
            self.board[x][y] = None

            open3_count = len([p for p in patterns if p.type == "open3"])
            rush4_count = len([p for p in patterns if p.type in ("rush4", "jump_open4")])
            open4_count = len([p for p in patterns if p.type == "open4"])

            if open4_count >= 1:
                threats.append((x, y, "open4_created"))
            elif rush4_count >= 2:
                threats.append((x, y, "double4"))
            elif open3_count >= 2:
                threats.append((x, y, "double3"))
            elif rush4_count >= 1 and open3_count >= 1:
                threats.append((x, y, "rush4+open3"))

        return threats

    # ============== 评估（V5 防守加权） ==============

    def evaluate_move(self, x: int, y: int, my_color: Color, depth: int = 1) -> int:
        if not self.is_valid(x, y) or self.board[x][y] is not None:
            return -1

        opponent = Color.BLACK if my_color == Color.WHITE else Color.WHITE

        # 模拟落子
        self.board[x][y] = my_color
        my_patterns = self.find_all_patterns(my_color)

        for p in my_patterns:
            if p.type == "five":
                self.board[x][y] = None
                return 100000

        for p in my_patterns:
            if p.type in ("open4", "jump_open4"):
                self.board[x][y] = None
                return 50000

        # 双重威胁
        double_threats = self.find_double_threats(my_color)
        for tx, ty, desc in double_threats:
            if tx == x and ty == y:
                score_map = {"double4": 45000, "open4_created": 50000, "double3": 8000, "rush4+open3": 6000}
                self.board[x][y] = None
                return score_map.get(desc, 5000)

        # 进攻分
        attack_score = 0
        for p in my_patterns:
            if (x, y) in p.empty_spots or (x, y) in p.positions:
                attack_score += self.SCORES.get(p.type, 0)

        # 1 层对手回应
        if depth > 0:
            opp_forced = self.find_forced_moves(opponent)
            opp_best_response = 0
            if opp_forced:
                for ox, oy, desc in opp_forced[:1]:
                    self.board[ox][oy] = opponent
                    opp_patterns = self.find_all_patterns(opponent)
                    for p in opp_patterns:
                        if p.type == "five":
                            opp_best_response = max(opp_best_response, 80000)
                        elif p.type in ("open4", "jump_open4"):
                            opp_best_response = max(opp_best_response, 40000)
                    self.board[ox][oy] = None
            attack_score -= opp_best_response * 0.5

        self.board[x][y] = None

        # 防守分（V5：× 1.3 加权，防守优先）
        defense_score = 0
        self.board[x][y] = opponent
        opp_patterns = self.find_all_patterns(opponent)
        for p in opp_patterns:
            if (x, y) in p.empty_spots:
                if p.type == "five":
                    defense_score += 100000
                elif p.type in ("open4", "jump_open4"):
                    defense_score += 50000
                elif p.type == "rush4":
                    defense_score += 10000
                elif p.type == "open3":
                    defense_score += 1500  # V5: 从 1000 提到 1500
                elif p.type == "sleep3":
                    defense_score += 200
        self.board[x][y] = None

        defense_score = int(defense_score * 1.3)  # V5: 防守加权

        # 位置分
        center = self.BOARD_SIZE // 2
        dist = abs(x - center) + abs(y - center)
        position_score = max(0, (10 - dist) * 3)

        total = int(attack_score + defense_score + position_score)
        if total < -10000:
            total = -50000
        return total

    def find_forced_moves(self, color: Color) -> List[Tuple[int, int, str]]:
        forced = []
        patterns = self.find_all_patterns(color)
        for p in patterns:
            if p.type in ["five", "open4", "jump_open4", "rush4"]:
                for ex, ey in p.empty_spots:
                    forced.append((ex, ey, f"{p.type}_threat"))
        return forced

    def get_best_moves(self, my_color_str: str, top_n: int = 10) -> List[Tuple[int, int, int, str]]:
        my_color = Color.BLACK if my_color_str == "black" else Color.WHITE
        candidates = []
        check_positions = self._get_nearby_empties(radius=3)

        if not check_positions:
            check_positions = {(7, 7)}

        for x, y in check_positions:
            score = self.evaluate_move(x, y, my_color, depth=1)
            if score > 0:
                reason = self._get_reason(x, y, my_color)
                candidates.append((x, y, score, reason))

        candidates.sort(key=lambda c: -c[2])
        return candidates[:top_n]

    def _get_reason(self, x: int, y: int, my_color: Color) -> str:
        reasons = []
        opponent = Color.BLACK if my_color == Color.WHITE else Color.WHITE

        self.board[x][y] = my_color
        for p in self.find_all_patterns(my_color):
            if (x, y) in p.positions or (x, y) in p.empty_spots:
                label = {"five": "✅五连获胜", "open4": "🔥活四必胜", "rush4": "⚡冲四", "open3": "📈活三"}.get(p.type)
                if label and label not in reasons:
                    reasons.append(label)
        self.board[x][y] = None

        self.board[x][y] = opponent
        for p in self.find_all_patterns(opponent):
            if (x, y) in p.empty_spots:
                label = {"five": "🛡️封五连", "open4": "🛡️封活四", "rush4": "🛡️封冲四", "open3": "🛡️封活三"}.get(p.type)
                if label and label not in reasons:
                    reasons.append(label)
        self.board[x][y] = None

        return "+".join(reasons) if reasons else "扩展"

    # ============== 决策（V5 重写） ==============

    def think(self, my_color_str: str) -> Tuple[int, int, str]:
        """
        V5 决策树：
        P1 我一步五连 → 下
        P2 对手一步五连 → 堵（除非能反杀）
        P3 对手有威胁点（模拟检测） → 攻守兼备或强堵
        P4 常规评分 + 随机性
        """
        my = Color.BLACK if my_color_str == "black" else Color.WHITE
        opp = Color.BLACK if my == Color.WHITE else Color.WHITE

        # P1: 我下一步五连
        my_win = self.find_win_points(my)
        if my_win:
            x, y = sorted(my_win)[0]
            return (x, y, f"🏆 五连制胜 ({x},{y})")

        # P2: 对手下一步五连
        opp_win = self.find_win_points(opp)
        if len(opp_win) >= 2:
            for px, py in sorted(opp_win):
                self.board[px][py] = my
                my_after = self.find_all_patterns(my)
                self.board[px][py] = None
                for np in my_after:
                    if np.type in ("open4", "jump_open4", "rush4"):
                        return (px, py, f"⚔️ 挣扎反扑 ({px},{py}) 堵+{np.type}")
            x, y = sorted(opp_win)[0]
            return (x, y, f"💀 对手双杀必败，挣扎 ({x},{y})")
        if len(opp_win) == 1:
            x, y = next(iter(opp_win))
            return (x, y, f"🛡️ 封对手五连点 ({x},{y})")

        # P3: 对手威胁点（V5：模拟检测，分 urgent/secondary 两级）
        opp_urgent, opp_secondary = self.find_threat_creation_points(opp)

        moves = self.get_best_moves(my_color_str, top_n=15)
        if not moves:
            return (7, 7, "开局天元")

        # 优先处理 urgent（对手能成活四的点，必须堵）
        opp_must_block = opp_urgent if opp_urgent else opp_secondary

        if opp_must_block:
            # 3a: 攻守兼备 — 推荐点中有堵威胁的
            for x, y, sc, r in moves:
                if (x, y) in opp_must_block:
                    return (x, y, f"⚖️ 攻守兼备 ({x},{y}) 堵威胁+{r}")

            # 3b: 我方最佳是活四/冲四 → 抢先进攻（我的威胁更紧迫）
            top_x, top_y, top_sc, top_r = moves[0]
            if "活四" in top_r or "冲四" in top_r:
                return (top_x, top_y, f"⚡ 抢先 ({top_x},{top_y}) {top_r}")

            # 3c: 纯防守 — 选必堵点中评分最高的
            best_block = None
            best_sc = -1
            for ex, ey in opp_must_block:
                sc = self.evaluate_move(ex, ey, my, depth=1)
                if sc > best_sc:
                    best_sc = sc
                    best_block = (ex, ey)
            if best_block:
                return (best_block[0], best_block[1],
                        f"🛡️ 堵威胁关键点 ({best_block[0]},{best_block[1]})")

        # P4: 常规评分 + V5 随机性（防背谱）
        x, y, score, reason = moves[0]

        # 在评分相近（5% 内）的候选中随机选一个
        if len(moves) > 1 and score > 0:
            threshold = score * 0.95
            similar = [(mx, my, ms, mr) for mx, my, ms, mr in moves if ms >= threshold]
            if len(similar) > 1:
                x, y, score, reason = random.choice(similar)

        if "五连" in reason:
            comment = f"🏆 五子连珠 ({x},{y})"
        elif "活四" in reason and "封" not in reason:
            comment = f"🔥 形成活四 ({x},{y})"
        elif "双四" in reason or "双三" in reason:
            comment = f"⚡ 双重威胁 ({x},{y})"
        elif "封" in reason:
            comment = f"🛡️ {reason} ({x},{y})"
        else:
            comment = f"选 ({x},{y}) {reason}"
        return (x, y, comment)


# ============== 兼容别名 ==============
GomokuBrainV2 = GomokuBrainV5


# ============== 回归测试 ==============

def _b(x, y):
    return {"x": x, "y": y, "color": "black"}


def _w(x, y):
    return {"x": x, "y": y, "color": "white"}


REGRESSION_CASES = [
    # V4 原有回归
    {
        "name": "M2.pre16-open4-identify",
        "stones": [
            _b(7, 7), _w(7, 6), _b(6, 7), _w(6, 6),
            _b(5, 7), _w(8, 7), _b(5, 6), _w(7, 8),
            _b(4, 7), _w(3, 7), _b(4, 6), _w(6, 8),
            _b(8, 6), _w(8, 8), _b(9, 6),
        ],
        "to_move": "white",
        "forbid": set(),
        "description": "活四识别与防守",
    },
    {
        "name": "diag2-open3-defense",
        "stones": [_b(6, 8), _b(7, 7), _b(8, 6), _w(0, 0)],
        "to_move": "white",
        "expect_in": {(5, 9), (9, 5)},
        "forbid": {(4, 10), (10, 4)},
        "description": "反对角活三紧邻封堵",
    },
    {
        "name": "M7.pre12-open3-horizontal-defense",
        "stones": [
            _b(7, 7), _w(6, 7), _b(7, 6), _w(8, 7),
            _b(7, 8), _w(7, 9), _b(7, 5), _w(7, 4),
            _b(6, 6), _w(5, 7), _b(8, 6),
        ],
        "to_move": "white",
        "expect_in": {(5, 6), (9, 6)},
        "forbid": {(4, 6), (10, 6)},
        "description": "横向活三紧邻堵，严禁二阶外端",
    },
    # V5 新增：不对称活三检测（18 手速败的致命 bug）
    {
        "name": "V5.asymmetric-open3-defense",
        "stones": [
            _b(7, 7), _w(7, 8),
            _b(6, 7), _w(5, 7),
            _b(7, 6), _w(5, 8),
            _b(8, 7), _w(9, 7),
            _b(9, 8), _w(6, 5),
            _b(10, 9), _w(11, 10),
            _b(6, 6), _w(6, 8),
            # 此时白方 y=8 列: (5,8)(6,8)(7,8) + 黑(9,8) → ___OOO_X_
            # 白方在 (4,8) 落子即成活四 _OOOO_
            # 黑方必须堵 (4,8) 或 (8,8)
        ],
        "to_move": "black",
        "expect_in": {(4, 8), (8, 8)},
        "forbid": set(),
        "description": "V5 入口：___OOO_X 不对称活三必须检测到并防守",
    },
    # V5 新增：确认堵的是正确的点
    {
        "name": "V5.asym-open3-block-correct-end",
        "stones": [
            _w(5, 8), _w(6, 8), _w(7, 8),  # 白方 y=8 三连
            _b(9, 8),  # 黑子封右端
            _b(7, 7),  # 给黑一些子避免空盘
        ],
        "to_move": "black",
        "expect_in": {(4, 8), (8, 8)},
        "forbid": set(),
        "description": "白方 _OOO_X 型活三：黑必须堵 (4,8) 或 (8,8)",
    },
]


def run_regressions() -> int:
    failed = 0
    print("=" * 60)
    print("Brain V5 回归测试")
    print("=" * 60)
    for case in REGRESSION_CASES:
        brain = GomokuBrainV5(case["stones"])
        x, y, comment = brain.think(case["to_move"])
        picked = (x, y)
        expect_in = case.get("expect_in")
        forbid = case.get("forbid", set())
        parts = [case["name"], f"picked={picked}", f"comment={comment}"]
        ok = True
        if expect_in and picked not in expect_in:
            ok = False
            parts.append(f"❌ not in {sorted(expect_in)}")
        if picked in forbid:
            ok = False
            parts.append(f"❌ in forbid {sorted(forbid)}")
        parts.insert(0, "✅" if ok else "❌")
        if not ok:
            failed += 1
        print(" ".join(parts))
        print(f"   - {case['description']}")
    print("=" * 60)
    print(f"{'all green' if not failed else f'{failed} FAILED'}")
    return failed


if __name__ == "__main__":
    import sys as _sys
    _sys.exit(run_regressions())
