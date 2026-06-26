#!/usr/bin/env python3
"""
我的五子棋大脑 V4

版本小史（类名保留 `GomokuBrainV2` 是历史命名，当前行为是 V4）：
- V2：跳型棋型识别、双三/双四、浅 minimax、迫手检测。
- V3：`think()` 改为硬优先级决策树（P1 我五连 → P2 堵对手五连 →
      P3 对手活三威胁 → P4 常规评分）；新增 `find_win_points` /
      `find_three_threat_points`。
- V4：修复 V3 里 `find_three_threat_points` 的**二阶外端误判**——
      之前会把 `__OOO__` 中离三子 2 格的外端（如 (4,6)/(10,6)）也列成
      "活三关键点"，导致 P3 3a 分支选出看似"堵三"实际完全没挡住的点。
      根因与证据见 `postmortems.md` 对局 7；修法见 `find_three_threat_points`
      文档串。
- V5：修复 V4 `find_three_threat_points` 仍依赖 `analyze_line_patterns`
      模板（`__OOO__/_O_OO_/_OO_O_`）枚举活三的局限性。该模板要求两端
      各 2 格空白，**漏识别"半活三"——一端被对方子封了 1 格但另一端
      仍能扩展成活四的三子**（典型：`____OOO_X` 在 (4,8) 一手成
      `_OOOO_` 活四）。对局 8 (92bf2fc1) 黑方第 15 手就死在这个盲点：
      白方 (5,8)(6,8)(7,8) 横向三连右端被 (9,8) 黑封 1 格，brain
      完全识别不出活三威胁，自顾自下了 (8,6) 扩自己活三 → 白方下一
      手 (4,8) 形成 _OOOO_ 活四 → 三步五连。
      修法：放弃"模板枚举 open3 → 检查能否成活四"两段式，改为
      **直接试落每个候选空位，看落后能否形成 open4/jump_open4**。
      这覆盖所有半活三、跳活三、单边封堵活三等边角情形。
- V5.1：修复 P3 "攻守兼备" (3a) 在**多 open4-creator** 局面下的策略
      错误。对局 11 (694dc8d2) 第 40 手白下 (11,6) 后，brain 已识别
      6 个 open4-creator (3 条独立活三线)，但 3a 从 top_n 候选里挑
      "碰巧能堵威胁"的点 → 选了 (8,9)（只覆盖 (8,3)(8,9) 这条线），
      x=11 列 (11,5)(11,6)(11,7) 活三和 (12,5)(12,7) 完全没动。第 42
      手白下 (11,8) 直接活四 → 必败。
      修法：当 `|opp_three| >= 2` 时，禁用"我的扩展位凑数"逻辑，
      改为对每个候选点（top_n ∪ opp_three）计算 **"我下后对方剩余
      open4-creator 数量"**，选削减效果最大的；若最优削减后仍 >= 2
      则承认必败局面，转入"挣扎反扑"模式（优先找自己的 rush4/open4
      反将一军，逼对方先应）。
- V5.2：新增 **`find_open3_seed_points(opp)`** — 跳活二预警。对局 11
      第 38 手白(11,7) 后 x=11 列是 `_____W_W_______` 跳活二，brain
      完全识别不到任何 pattern；第 39 手 V5.1 推荐扩展自己活三 (6,8)，
      错过救命窗口（下 (11,6) 即可让白方威胁归零）。修法：识别"对方
      下一步即可形成 open3"的空位（用试落子检查 → 是否生成 open3/
      jump_open3/half_open3）。在 P3 之后加 P3.5 分支：当对方有 ≥ 2
      个 open3-seed 点（多线活二种子）且我方没有迫手时，优先压制最
      高价值种子，防止局面恶化为多 open4-creator 必败。
"""

from typing import List, Tuple, Dict, Set, Optional
from dataclasses import dataclass
from enum import Enum
import copy

class Color(Enum):
    BLACK = "black"
    WHITE = "white"

@dataclass
class Pattern:
    """棋型识别结果"""
    type: str  # five, open4, rush4, open3, sleep3, jump_open3, jump_open4
    positions: List[Tuple[int, int]]  # 棋子位置
    empty_spots: List[Tuple[int, int]]  # 空位（可落子完成棋型）
    direction: Tuple[int, int]  # 方向
    score: int

class GomokuBrainV2:
    """增强版五子棋决策大脑"""

    BOARD_SIZE = 15
    DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]  # 横、竖、主对角、副对角

    # 棋型分值
    SCORES = {
        "five": 100000,
        "open4": 50000,      # 活四
        "double4": 45000,    # 双冲四
        "rush4": 10000,      # 冲四
        "jump_open4": 40000, # 跳活四
        "open3": 1000,       # 活三
        "double3": 8000,     # 双活三
        "jump_open3": 800,   # 跳活三
        "sleep3": 100,       # 眠三
        "open2": 50,         # 活二
    }

    def __init__(self, stones_data: List[Dict]):
        self.board = [[None] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        self.stones = []
        for s in stones_data:
            color = Color.BLACK if s["color"] == "black" else Color.WHITE
            self.stones.append({"x": s["x"], "y": s["y"], "color": color})
            self.board[s["x"]][s["y"]] = color

    def is_valid(self, x: int, y: int) -> bool:
        return 0 <= x < self.BOARD_SIZE and 0 <= y < self.BOARD_SIZE

    def get_line(self, x: int, y: int, dx: int, dy: int, length: int = 9) -> List:
        """获取一条线上长度为 length 的序列（中心在 x,y）"""
        result = []
        # 从 (x - (length//2)*dx, y - (length//2)*dy) 开始
        start_offset = length // 2
        for i in range(length):
            nx = x - start_offset * dx + i * dx
            ny = y - start_offset * dy + i * dy
            if self.is_valid(nx, ny):
                result.append((nx, ny, self.board[nx][ny]))
            else:
                result.append((nx, ny, "out"))  # 越界
        return result

    def analyze_line_patterns(self, x: int, y: int, dx: int, dy: int, color: Color) -> List[Pattern]:
        """
        分析一条线上的所有棋型，包括跳棋型
        返回该位置所有可能的棋型列表
        """
        patterns = []

        # 获取包含 (x,y) 的线段，长度9可以覆盖五子连珠的所有情况
        line = self.get_line(x, y, dx, dy, 9)

        # 转换为字符串表示：'O'=我的子, 'X'=对手, '_'=空, '#'=越界
        symbols = []
        my_pos = []  # 记录我的棋子位置
        for i, (px, py, c) in enumerate(line):
            if c == "out":
                symbols.append("#")
            elif c is None:
                symbols.append("_")
            elif c == color:
                symbols.append("O")
                if px == x and py == y:  # 标记中心点
                    center_idx = i
            else:
                symbols.append("X")

        line_str = "".join(symbols)

        # 棋型匹配（中心在O或_）
        # 活四: _OOOO_ 或 O_OOO 或 OO_OO 等
        # 冲四: XOOOO_ 或 _OOOOX 或 OOO_O 等
        # 活三: __OOO__ 或 _O_OO_ 等

        # 直接匹配
        if "OOOOO" in line_str:
            idx = line_str.find("OOOOO")
            positions = [(line[i][0], line[i][1]) for i in range(idx, idx+5) if line[i][2] == color]
            patterns.append(Pattern("five", positions, [], (dx, dy), self.SCORES["five"]))

        # 活四检测: _OOOO_
        if "_OOOO_" in line_str:
            idx = line_str.find("_OOOO_")
            # 两个空位是活四的延伸点
            empty_spots = [(line[idx][0], line[idx][1]), (line[idx+5][0], line[idx+5][1])]
            positions = [(line[i][0], line[i][1]) for i in range(idx+1, idx+5)]
            patterns.append(Pattern("open4", positions, empty_spots, (dx, dy), self.SCORES["open4"]))

        # 跳冲四（一个成五点，不是活四！）: O_OOO, OO_OO, OOO_O
        # 这些只有一个成五点(空位)，对手封掉就没了，本质是 rush4 不是 open4
        jump_rush4_patterns = ["O_OOO", "OO_OO", "OOO_O"]
        for jp in jump_rush4_patterns:
            if jp in line_str:
                idx = line_str.find(jp)
                empty_idx = idx + jp.find("_")
                positions = [(line[i][0], line[i][1]) for i in range(idx, idx+5) if line[i][2] == color]
                empty_spots = [(line[empty_idx][0], line[empty_idx][1])]
                patterns.append(Pattern("rush4", positions, empty_spots, (dx, dy), self.SCORES["rush4"]))

        # 活三检测: __OOO__, _O_OO_, _OO_O_
        open3_patterns = ["__OOO__", "_O_OO_", "_OO_O_"]
        for p in open3_patterns:
            if p in line_str:
                idx = line_str.find(p)
                positions = [(line[i][0], line[i][1]) for i in range(idx, idx+len(p)) if line[i][2] == color]
                empty_spots = [(line[i][0], line[i][1]) for i in range(idx, idx+len(p)) if line[i][2] is None]
                patterns.append(Pattern("open3", positions, empty_spots, (dx, dy), self.SCORES["open3"]))

        # 冲四检测
        rush4_patterns = [
            ("XOOOO_", [5]),  # 前封堵，后开放
            ("_OOOOX", [0]),  # 后封堵，前开放
            ("X_OOOO", [1]),  # 跳冲四
            ("OOOO_X", [4]),  # 跳冲四
        ]
        for rp, empty_indices in rush4_patterns:
            if rp in line_str:
                idx = line_str.find(rp)
                positions = [(line[i][0], line[i][1]) for i in range(idx, idx+6) if line[i][2] == color]
                empty_spots = [(line[idx+ei][0], line[idx+ei][1]) for ei in empty_indices]
                patterns.append(Pattern("rush4", positions, empty_spots, (dx, dy), self.SCORES["rush4"]))

        return patterns

    def find_all_patterns(self, color: Color) -> List[Pattern]:
        """找出棋盘上某颜色的所有棋型"""
        all_patterns = []

        for stone in self.stones:
            if stone["color"] != color:
                continue
            x, y = stone["x"], stone["y"]
            for dx, dy in self.DIRECTIONS:
                patterns = self.analyze_line_patterns(x, y, dx, dy, color)
                all_patterns.extend(patterns)

        # 去重（相同类型、相同位置的棋型）
        unique_patterns = []
        seen = set()
        for p in all_patterns:
            key = (p.type, tuple(sorted(p.positions)))
            if key not in seen:
                seen.add(key)
                unique_patterns.append(p)

        return unique_patterns

    def find_forced_moves(self, color: Color) -> List[Tuple[int, int, str]]:
        """
        找出所有"迫手"（对手必须回应的点）
        返回: [(x, y, description), ...]
        """
        forced = []
        patterns = self.find_all_patterns(color)

        for p in patterns:
            if p.type in ["five", "open4", "jump_open4", "rush4"]:
                # 这些棋型下在空位就能获胜或形成必胜
                for ex, ey in p.empty_spots:
                    forced.append((ex, ey, f"{p.type}_threat"))

        return forced

    def find_double_threats(self, color: Color) -> List[Tuple[int, int, str]]:
        """
        找出能形成双三/双四的点
        返回: [(x, y, description), ...]
        """
        threats = []
        empty_candidates = set()

        # 收集候选空位
        for stone in self.stones:
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    nx, ny = stone["x"] + dx, stone["y"] + dy
                    if self.is_valid(nx, ny) and self.board[nx][ny] is None:
                        empty_candidates.add((nx, ny))

        for x, y in empty_candidates:
            # 模拟落子
            self.board[x][y] = color
            patterns = self.find_all_patterns(color)
            self.board[x][y] = None

            # 统计活三/冲四数量
            open3_count = len([p for p in patterns if p.type == "open3"])
            rush4_count = len([p for p in patterns if p.type in ["rush4", "jump_open4"]])
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

    def evaluate_move(self, x: int, y: int, my_color: Color, depth: int = 1) -> int:
        """
        评估某个空位的价值（带一层 minimax）
        depth=1: 考虑我落子后，对手的最佳回应
        """
        if not self.is_valid(x, y) or self.board[x][y] is not None:
            return -1

        opponent = Color.BLACK if my_color == Color.WHITE else Color.WHITE

        # 模拟我落子
        self.board[x][y] = my_color
        my_patterns = self.find_all_patterns(my_color)

        # 检查我是否立即获胜
        for p in my_patterns:
            if p.type == "five":
                self.board[x][y] = None
                return 100000

        # 检查我是否形成活四
        for p in my_patterns:
            if p.type in ["open4", "jump_open4"]:
                self.board[x][y] = None
                return 50000

        # 检查我是否形成双三/双四
        double_threats = self.find_double_threats(my_color)
        for tx, ty, desc in double_threats:
            if tx == x and ty == y:
                if "double4" in desc:
                    score = 45000
                elif "double3" in desc:
                    score = 8000
                elif "rush4+open3" in desc:
                    score = 6000
                else:
                    score = 5000
                self.board[x][y] = None
                return score

        # 基础进攻分
        attack_score = 0
        for p in my_patterns:
            if (x, y) in p.empty_spots or (x, y) in p.positions:
                attack_score += self.SCORES.get(p.type, 0)

        # 模拟对手回应（ minimax ）
        if depth > 0:
            self.board[x][y] = my_color  # 保持我的落子

            # 找出对手的最佳回应
            opp_best_response = 0
            opp_forced = self.find_forced_moves(opponent)

            if opp_forced:
                # 对手有必须防守的点
                for ox, oy, desc in opp_forced[:1]:  # 取最紧急的一个
                    self.board[ox][oy] = opponent
                    opp_patterns = self.find_all_patterns(opponent)

                    # 如果对手能获胜或形成活四，这步很危险
                    for p in opp_patterns:
                        if p.type == "five":
                            opp_best_response = max(opp_best_response, 80000)
                        elif p.type in ["open4", "jump_open4"]:
                            opp_best_response = max(opp_best_response, 40000)

                    self.board[ox][oy] = None

            # 我的得分减去对手的最佳回应（ minimax 思想）
            attack_score -= opp_best_response * 0.5

            self.board[x][y] = None

        # 防守价值：阻止对手的威胁
        defense_score = 0
        self.board[x][y] = opponent
        opp_patterns = self.find_all_patterns(opponent)
        for p in opp_patterns:
            if (x, y) in p.empty_spots:
                if p.type == "five":
                    defense_score += 100000  # 必须封堵
                elif p.type in ["open4", "jump_open4"]:
                    defense_score += 50000   # 必须封堵活四
                elif p.type == "rush4":
                    defense_score += 10000   # 封堵冲四
                elif p.type == "open3":
                    defense_score += 1000    # 封堵活三
        self.board[x][y] = None

        # 位置价值
        center = self.BOARD_SIZE // 2
        dist = abs(x - center) + abs(y - center)
        position_score = max(0, (10 - dist) * 3)

        total_score = int(attack_score + defense_score + position_score)

        # 如果这步能让对手形成必胜，要严重惩罚
        if total_score < -10000:
            total_score = -50000

        return total_score

    def get_best_moves(self, my_color_str: str, top_n: int = 5) -> List[Tuple[int, int, int, str]]:
        """获取最佳落子点"""
        my_color = Color.BLACK if my_color_str == "black" else Color.WHITE
        opponent = Color.BLACK if my_color == Color.WHITE else Color.WHITE

        candidates = []

        # 评估范围：已有棋子附近
        check_positions = set()
        if not self.stones:
            check_positions.add((7, 7))
        else:
            for s in self.stones:
                for dx in range(-3, 4):
                    for dy in range(-3, 4):
                        nx, ny = s["x"] + dx, s["y"] + dy
                        if self.is_valid(nx, ny) and self.board[nx][ny] is None:
                            check_positions.add((nx, ny))

        # 评估每个候选位置
        for x, y in check_positions:
            score = self.evaluate_move(x, y, my_color, depth=1)
            if score > 0:
                reason = self._get_reason(x, y, my_color)
                candidates.append((x, y, score, reason))

        candidates.sort(key=lambda x: -x[2])
        return candidates[:top_n]

    def _get_reason(self, x: int, y: int, my_color: Color) -> str:
        """生成落子理由"""
        reasons = []
        opponent = Color.BLACK if my_color == Color.WHITE else Color.WHITE

        # 我的进攻
        self.board[x][y] = my_color
        patterns = self.find_all_patterns(my_color)
        for p in patterns:
            if (x, y) in p.positions or (x, y) in p.empty_spots:
                if p.type == "five":
                    reasons.append("✅五连获胜")
                elif p.type in ["open4", "jump_open4"]:
                    reasons.append("🔥活四必胜")
                elif p.type == "rush4":
                    reasons.append("⚡冲四")
                elif p.type == "open3":
                    reasons.append("📈活三")
        self.board[x][y] = None

        # 防守
        self.board[x][y] = opponent
        patterns = self.find_all_patterns(opponent)
        for p in patterns:
            if (x, y) in p.empty_spots:
                if p.type == "five":
                    reasons.append("🛡️封五连")
                elif p.type in ["open4", "jump_open4"]:
                    reasons.append("🛡️封活四")
                elif p.type == "rush4":
                    reasons.append("🛡️封冲四")
        self.board[x][y] = None

        return "+".join(reasons) if reasons else "扩展"

    # ============== V3 新增：必胜/必堵点提取 ==============

    def find_win_points(self, color: Color) -> set:
        """找出该颜色下一步就能五连的点（open4/jump_open4/rush4 的 empty_spots）"""
        points = set()
        for p in self.find_all_patterns(color):
            if p.type in ("open4", "jump_open4", "rush4", "five"):
                for ep in p.empty_spots:
                    if self.is_valid(*ep) and self.board[ep[0]][ep[1]] is None:
                        points.add(ep)
        return points

    def find_three_threat_points(self, color: Color) -> set:
        """找出该颜色的"活三关键点"：对方下在这里能形成 open4/jump_open4。

        V5 重写：彻底放弃"先匹配 open3 模板，再在 empty_spots 上试落"的
        两段式检测。原方案严重依赖 `analyze_line_patterns` 的模板覆盖度
        （`__OOO__/_O_OO_/_OO_O_`），凡是被对方棋子封了一端的"半活三"
        全部漏掉（对局 8 的 y=8 行 `____OOO_X` 即此案）。

        新实现：直接扫描已有棋子半径 3 内的所有空位，**试落 → 检查是否
        生成 open4/jump_open4**。这覆盖：

          * 紧邻活三 (`__OOO__`)
          * 内部 gap 跳活三 (`_O_OO_` / `_OO_O_`)
          * 单边封堵但仍能成活四的"半活三" (`X__OOO__` 等)
          * 任何模板没枚举到的边角棋型

        附带优势：V4 那个"二阶外端误判"的特判逻辑也不再需要——只要
        试落后没真生成 open4，就不会被加进来。
        """
        points = set()
        if not self.stones:
            return points
        candidates = set()
        for s in self.stones:
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    nx, ny = s["x"] + dx, s["y"] + dy
                    if self.is_valid(nx, ny) and self.board[nx][ny] is None:
                        candidates.add((nx, ny))
        for x, y in candidates:
            self.board[x][y] = color
            after = self.find_all_patterns(color)
            self.board[x][y] = None
            for ap in after:
                if ap.type in ("open4", "jump_open4"):
                    points.add((x, y))
                    break
        return points

    def find_open3_seed_points(self, color: Color) -> set:
        """V5.2 新增：跳活二/活二预警。返回"对方下一步能形成 open3 类
        棋型"的空位集合（活三种子点）。

        与 `find_three_threat_points` 的区别：那个找 "下一步能成活四" 的
        点（已是活三威胁），本方法找 "下一步能成活三" 的点（活二种子，
        提早 1 拍预警）。用于 P3.5：当对方有 ≥ 2 个种子点（多线活二
        累积）且我方无迫手时，提早压制，防止两手后变成多 open4-creator
        必败局面。
        """
        points = set()
        if not self.stones:
            return points
        candidates = set()
        for s in self.stones:
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    nx, ny = s["x"] + dx, s["y"] + dy
                    if self.is_valid(nx, ny) and self.board[nx][ny] is None:
                        candidates.add((nx, ny))
        for x, y in candidates:
            self.board[x][y] = color
            after = self.find_all_patterns(color)
            self.board[x][y] = None
            for ap in after:
                if ap.type in ("open3", "jump_open3"):
                    points.add((x, y))
                    break
        return points

    def think(self, my_color_str: str) -> Tuple[int, int, str]:
        """
        V3 决策：硬优先级决策树
        P1 我一步五连 → 下
        P2 对手一步五连 → 堵（除非能反杀）
        P3 对手有活三威胁 → 攻守兼备或强堵
        P4 常规评分
        """
        my = Color.BLACK if my_color_str == "black" else Color.WHITE
        opp = Color.BLACK if my == Color.WHITE else Color.WHITE

        # P1: 我下一步就能五连
        my_win = self.find_win_points(my)
        if my_win:
            x, y = sorted(my_win)[0]
            return (x, y, f"🏆 五连制胜 ({x},{y})")

        # P2: 对手下一步就能五连
        opp_win = self.find_win_points(opp)
        if len(opp_win) >= 2:
            # 对手活四两端都赢 — 必败局面，尝试反扑（下一步自己活四或冲四迫对手应）
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

        # P3: 对手有活三威胁（下一步会形成活四）
        opp_three = self.find_three_threat_points(opp)

        # 收集候选
        moves = self.get_best_moves(my_color_str, top_n=15)
        if not moves:
            return (7, 7, "开局天元")

        if opp_three:
            # ===== V5.1: 多 open4-creator 局面专用策略 =====
            # 当对方有 ≥ 2 个 open4-creator 时，"攻守兼备" 是自杀
            # （只堵其中一个，剩余的下一手任意一个被完成就活四必胜）。
            # 改为：对每个候选点计算"我下后对方剩余威胁数"，选削减最大。
            if len(opp_three) >= 2:
                # 第一步：在 opp_three 中找"削减后剩余最少"的堵点
                # （只考虑直接堵在威胁线上的点，避免被自己的高分扩展位干扰）
                best_block = None  # (rem_count, -sc, x, y)
                for cx, cy in opp_three:
                    if not self.is_valid(cx, cy) or self.board[cx][cy] is not None:
                        continue
                    self.board[cx][cy] = my
                    remaining = self.find_three_threat_points(opp)
                    self.board[cx][cy] = None
                    sc = self.evaluate_move(cx, cy, my, depth=1)
                    key = (len(remaining), -sc, cx, cy)
                    if best_block is None or key < best_block[:2] + (cx, cy):
                        best_block = (len(remaining), -sc, cx, cy)
                if best_block is None:
                    # opp_three 全被占？理论不会到这；走原 fallback
                    pass
                else:
                    rem_count, _, bx, by = best_block
                    if rem_count == 0:
                        return (bx, by, f"🛡️ 多威胁全清 ({bx},{by})")
                    if rem_count == 1:
                        return (bx, by, f"⚖️ 多威胁优堵 ({bx},{by}) 剩{rem_count}")
                    # rem_count >= 2：必败前夕，优先反扑
                    # 反扑：在 top moves 里找能形成 rush4/open4/五连 的点
                    for tx, ty, tsc, tr in moves:
                        if "活四" in tr or "冲四" in tr or "五连" in tr:
                            return (tx, ty, f"⚔️ 多威胁必败反扑 ({tx},{ty}) {tr}")
                    # 无反扑可用：堵最优威胁点（至少瓦解最强一条线）
                    return (bx, by, f"💀 多威胁({len(opp_three)})无反扑 → 堵 ({bx},{by}) 剩{rem_count}")
            # ===== V3/V4 单威胁逻辑 =====
            # 3a: 攻守兼备 — 我的 top 推荐里有堵活三的点
            for x, y, sc, r in moves:
                if (x, y) in opp_three:
                    return (x, y, f"⚖️ 攻守兼备 ({x},{y}) 堵三+{r}")
            # 3b: 无交集 — 评估堵活三的候选分，选最高
            best_block = None
            best_sc = -1
            for ex, ey in opp_three:
                sc = self.evaluate_move(ex, ey, my, depth=1)
                if sc > best_sc:
                    best_sc = sc
                    best_block = (ex, ey)
            # 3c: 若我方最佳进攻是活四/冲四（下一步我就能赢），且对手只有活三（需两步才成五），可以继续进攻
            top_x, top_y, top_sc, top_r = moves[0]
            if "活四" in top_r or "冲四" in top_r:
                return (top_x, top_y, f"⚡ 抢先 ({top_x},{top_y}) {top_r}")
            if best_block:
                return (best_block[0], best_block[1], f"🛡️ 堵活三关键点 ({best_block[0]},{best_block[1]})")

        # ===== V5.2 P3.5: 跳活二预警 =====
        # 对方有 ≥ 2 个 open3-seed (多线活二累积) 且我方无迫手时，
        # 提早压制，防止两手后变成多 open4-creator 必败局面。
        # 触发条件严格：仅当对方"种子线"明显多于我方进攻威胁时才介入。
        my_top = moves[0]
        top_x, top_y, top_sc, top_r = my_top
        has_my_pressure = ("活四" in top_r or "冲四" in top_r or
                           "五连" in top_r or "双" in top_r)
        if not has_my_pressure:
            opp_seeds = self.find_open3_seed_points(opp)
            # 按"我下后对方剩余种子数"评估每个种子点的削减效果
            if len(opp_seeds) >= 2:
                # 在我方 top moves 和 opp_seeds 中找"削减种子最多 + 自身分高"的点
                cand = set(opp_seeds)
                for x, y, _, _ in moves[:5]:
                    cand.add((x, y))
                best = None  # (-reduction, -sc, x, y)
                base = len(opp_seeds)
                for cx, cy in cand:
                    if not self.is_valid(cx, cy) or self.board[cx][cy] is not None:
                        continue
                    self.board[cx][cy] = my
                    rem = self.find_open3_seed_points(opp)
                    self.board[cx][cy] = None
                    sc = self.evaluate_move(cx, cy, my, depth=1)
                    reduction = base - len(rem)
                    # 只在能削减 ≥ 2 时考虑（否则普通 P4 评分更稳）
                    if reduction < 2:
                        continue
                    key = (-reduction, -sc, cx, cy)
                    if best is None or key < best:
                        best = key
                if best is not None:
                    _, _, bx, by = best
                    return (bx, by, f"⚠️ 跳活二预警 ({bx},{by}) 削减种子 {base}→{base+best[0]}")

        # P4: 常规评分
        x, y, score, reason = moves[0]
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


# ============== 测试 ==============

def _b(x, y):
    return {"x": x, "y": y, "color": "black"}


def _w(x, y):
    return {"x": x, "y": y, "color": "white"}


REGRESSION_CASES = [
    # ---- V2 原始回归：活四识别 ----
    {
        "name": "M2.pre16-open4-identify",
        "stones": [
            _b(7, 7), _w(7, 6),
            _b(6, 7), _w(6, 6),
            _b(5, 7), _w(8, 7),
            _b(5, 6), _w(7, 8),
            _b(4, 7), _w(3, 7),
            _b(4, 6), _w(6, 8),
            _b(8, 6), _w(8, 8),
            _b(9, 6),
        ],
        "to_move": "white",
        # 黑已有横向四 (5,6)(6,6)(8,6)(9,6) 带 (7,6)W 实际白方必须防
        "forbid": set(),
        "description": "V2 原始用例：活四识别与防守",
    },
    # ---- V3 对角活三防守 ----
    {
        "name": "diag2-open3-defense",
        "stones": [_b(6, 8), _b(7, 7), _b(8, 6), _w(0, 0)],
        "to_move": "white",
        "expect_in": {(5, 9), (9, 5)},
        "forbid": {(4, 10), (10, 4)},
        "description": "V3：反对角活三的紧邻封堵（非二阶外端）",
    },
    # ---- V4 真正触发迭代的对局 ----
    {
        # 对局 7 (cd91b5d4) 第 11 手后局面：黑横向活三 y=6 (6,6)(7,6)(8,6)
        # V3 曾错选 (4,6)/(10,6)（二阶外端），V4 必须紧邻堵 (5,6) 或 (9,6)
        "name": "M7.pre12-open3-horizontal-defense",
        "stones": [
            _b(7, 7), _w(6, 7),
            _b(7, 6), _w(8, 7),
            _b(7, 8), _w(7, 9),
            _b(7, 5), _w(7, 4),
            _b(6, 6), _w(5, 7),
            _b(8, 6),
        ],
        "to_move": "white",
        "expect_in": {(5, 6), (9, 6)},
        "forbid": {(4, 6), (10, 6)},
        "description": "V4 修复入口：横向活三紧邻堵，严禁二阶外端",
    },
    # ---- V5 触发迭代：半活三（一端被封 1 格仍能成活四） ----
    {
        # 对局 8 (92bf2fc1) 第 14 手后局面：白横向 (5,8)(6,8)(7,8)，
        # 右端被 (9,8) 黑封 1 格，但白下 (4,8) 仍能成 _OOOO_ 活四。
        # V4 (用 __OOO__ 模板) 漏判此活三，brain 推荐 (8,6) 自扩活三 →
        # 三步五连惨败。V5 必须识别并堵 (4,8) 或 (8,8)。
        "name": "M8.pre15-half-open3-blocked-end",
        "stones": [
            _b(7, 7),  _w(7, 8),
            _b(6, 7),  _w(5, 7),
            _b(7, 6),  _w(5, 8),
            _b(8, 7),  _w(9, 7),
            _b(9, 8),  _w(6, 5),
            _b(10, 9), _w(11, 10),
            _b(6, 6),  _w(6, 8),
        ],
        "to_move": "black",
        "expect_in": {(4, 8), (8, 8)},
        "forbid": {(8, 6)},
        "description": "V5 修复入口：半活三（被封一端但仍能成活四）必须识别",
    },
    # ---- 历史败局回归：对局 5 (531f31de) 黑方主对角四连必堵成五点 ----
    {
        # P2 (find_win_points) 验证：黑 (6,6)(7,7)(8,8)(9,9) 主对角四连，
        # 白方下一手必堵 (5,5) 或 (10,10)，否则黑下任一端即五连。
        # 史实白方人类层未服从 think() 给的 (5,5) 而下了 (9,4) → 惨败。
        "name": "M5.21-block-open4-main-diagonal",
        "stones": [
            _b(6, 6), _w(6, 7),
            _b(7, 7), _w(7, 6),
            _b(8, 8), _w(8, 9),
            _b(9, 9), _w(2, 2),
        ],
        "to_move": "white",
        "expect_in": {(5, 5), (10, 10)},
        "forbid": set(),
        "description": "对局 5：主对角四连 P2 必堵（防 think→执行层不一致）",
    },
    # ---- 历史败局回归：对局 8 (60ffaa0d) 主对角活三早期识别 ----
    {
        # 对局 8 中盘黑在主对角 (5,5)…(9,9) 上慢性堆子。本用例用最小局面
        # 验证：黑方 (6,6)(7,7)(8,8) 主对角活三时，V5 必须紧邻堵 (5,5)
        # 或 (9,9)。（实战死于多威胁同时施压，本用例只断单点识别能力。）
        "name": "M8x.diag1-open3-early-defense",
        "stones": [
            _b(6, 6), _b(7, 7), _b(8, 8),
            _w(0, 0), _w(1, 1),
        ],
        "to_move": "white",
        "expect_in": {(5, 5), (9, 9)},
        "forbid": set(),
        "description": "对局 8：主对角活三早期紧邻堵（多威胁实战仍需 VCF）",
    },
    # ---- V5.1 触发迭代：对局 11 (694dc8d2) 多 open4-creator 局面 ----
    {
        # 对局 11 第 40 手白下 (11,6) 后局面：白方有 6 个 open4-creator
        # （x=11 列活三 (11,5)(11,6)(11,7) 两端 (11,4)(11,8)；主对角
        # (8,3)(9,4)(10,5)(11,6) 系列 → (8,3)/(8,9)；反对角 → (12,5)/(12,7)）
        # V5 之前选 (8,9) "攻守兼备" → 只堵 1 条线 → 第 42 手白活四必胜
        # V5.1 必须挑能削减最多威胁的点（理想是覆盖 x=11 列：(11,4)/(11,8)）
        # 或承认必败转入反扑。
        "name": "M11.pre41-multi-open4-creators",
        "stones": [
            _b(7, 7),   _w(8, 7),
            _b(6, 7),   _w(5, 7),
            _b(7, 6),   _w(7, 8),
            _b(8, 5),   _w(9, 4),
            _b(5, 8),   _w(4, 9),
            _b(6, 6),   _w(6, 9),
            _b(9, 6),   _w(8, 6),
            _b(8, 8),   _w(5, 5),
            _b(9, 9),   _w(10, 10),
            _b(9, 7),   _w(9, 8),
            _b(7, 9),   _w(6, 10),
            _b(10, 6),  _w(11, 5),
            _b(7, 4),   _w(10, 7),
            _b(7, 5),   _w(7, 3),
            _b(6, 3),   _w(5, 2),
            _b(6, 5),   _w(6, 4),
            _b(9, 5),   _w(10, 5),
            _b(4, 6),   _w(5, 6),
            _b(12, 8),  _w(11, 7),
            _b(6, 8),   _w(11, 6),  # 第 40 手
        ],
        "to_move": "black",
        # V5.1 期望：comment 必须含"多威胁"或"必败"标记，证明算法识别到此为
        # 多 open4-creator 局面（而非旧 V5 那样毫无察觉地走"攻守兼备"）。
        # 实际此局在第 40 手已是 3 条独立活三必败，任何堵点都剩 4 威胁——
        # 真正的失误在白方第 38 手前（跳活二预警，属 V6 跳活二/VCT 范畴）。
        "expect_comment_substr": ["多威胁"],
        "description": "V5.1 修复入口：多 open4-creator 必识别（必败局面归因）",
    },
    # ---- V5.2 触发迭代：对局 11 (694dc8d2) 第 38 手前 救命窗口 ----
    {
        # 第 38 手白下 (11,7) 完成 x=11 列跳活二 (11,5)+(11,7)。
        # 旧 V5.1 推荐 (6,8) 自扩活三，错过救命窗口。
        # V5.2 P3.5 应该识别"白方多线活二种子"，优先压制 x=11 列。
        # 期望：comment 含"跳活二预警"，或选 (11,6)/(11,8)/(11,4) 等
        # 能让白方威胁完全归零的点。
        "name": "M11.pre39-jump-open2-early-warning",
        "stones": [
            _b(7, 7),   _w(8, 7),
            _b(6, 7),   _w(5, 7),
            _b(7, 6),   _w(7, 8),
            _b(8, 5),   _w(9, 4),
            _b(5, 8),   _w(4, 9),
            _b(6, 6),   _w(6, 9),
            _b(9, 6),   _w(8, 6),
            _b(8, 8),   _w(5, 5),
            _b(9, 9),   _w(10, 10),
            _b(9, 7),   _w(9, 8),
            _b(7, 9),   _w(6, 10),
            _b(10, 6),  _w(11, 5),
            _b(7, 4),   _w(10, 7),
            _b(7, 5),   _w(7, 3),
            _b(6, 3),   _w(5, 2),
            _b(6, 5),   _w(6, 4),
            _b(9, 5),   _w(10, 5),
            _b(4, 6),   _w(5, 6),
            _b(12, 8),  _w(11, 7),  # 第 38 手
        ],
        "to_move": "black",
        "expect_comment_substr": ["跳活二预警"],
        "description": "V5.2 修复入口：跳活二预警，提早压制多线活二种子",
    },
    # ---- V5 同时验证：被一端远封但另一端能成活四的"半活三" ----
    {
        # 白方 (5,5)(6,5)(7,5) 横三连，右端紧邻 (8,5) 空、(9,5)=B 封；
        # 左端 (4,5)(3,5) 都空。白下 (4,5) → (4,5)(5,5)(6,5)(7,5) 四子，
        # 左紧邻 (3,5) 空、右紧邻 (8,5) 空 → `_OOOO_` 活四（再外的
        # (9,5)=B 不影响活四判定）。这种"远端被封但近端能成活四"
        # 的形态正是 V4 模板漏判的核心场景。
        "name": "synthetic-half-open3-far-end-blocked",
        "stones": [
            _b(7, 7), _w(5, 5),
            _b(9, 5), _w(6, 5),
            _b(0, 0), _w(7, 5),
        ],
        "to_move": "black",
        "expect_in": {(4, 5)},
        "forbid": set(),
        "description": "V5：远端被封 1 格、近端 2 空的半活三必须识别",
    },
]


def run_regressions() -> int:
    failed = 0
    print("=" * 60)
    print("Brain 回归测试")
    print("=" * 60)
    for case in REGRESSION_CASES:
        brain = GomokuBrainV2(case["stones"])
        x, y, comment = brain.think(case["to_move"])
        picked = (x, y)
        expect_in = case.get("expect_in")
        forbid = case.get("forbid", set())
        expect_substr = case.get("expect_comment_substr", [])
        status_parts = [case["name"], f"picked={picked}", f"comment={comment}"]
        ok = True
        if expect_in and picked not in expect_in:
            ok = False
            status_parts.append(f"❌ not in {sorted(expect_in)}")
        if picked in forbid:
            ok = False
            status_parts.append(f"❌ in forbid {sorted(forbid)}")
        for sub in expect_substr:
            if sub not in comment:
                ok = False
                status_parts.append(f"❌ comment missing '{sub}'")
        if ok:
            status_parts.insert(0, "✅")
        else:
            status_parts.insert(0, "❌")
            failed += 1
        print(" ".join(status_parts))
        print(f"   - {case['description']}")
    print("=" * 60)
    if failed:
        print(f"{failed} case(s) failed")
    else:
        print("all green")
    return failed


if __name__ == "__main__":
    import sys as _sys
    _sys.exit(run_regressions())
