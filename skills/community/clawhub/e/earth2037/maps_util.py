#!/usr/bin/env python3
"""
Earth2037 地图坐标：tileID / VillageID / CityID ↔ (x, y)
与服务端 Maps 一致。含 ASCII 线框图；可选集成 HTTP QM，按服端返回地块绘制。
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from typing import List, Optional

# 主图 mapId=1：Count=802，坐标轴 ∈ [-400, 401]（与游戏主图一致）
MAIN_COUNT_X = 802
MAIN_MAX = 401
MAIN_MIN = -400

# 小图 mapId=2: 162×162, X/Y ∈ [-80, 81]
MINI_COUNT_X = 162
MINI_MAX = 81
MINI_MIN = -80


def _v_main(x):
    """主图边界环绕"""
    if x > MAIN_MAX:
        return x - MAIN_COUNT_X
    if x < MAIN_MIN:
        return x + MAIN_COUNT_X
    return x


def _v_mini(x):
    """小图边界环绕"""
    if x > MINI_MAX:
        return x - MINI_COUNT_X
    if x < MINI_MIN:
        return x + MINI_COUNT_X
    return x


def get_x(tile_id, mini=False):
    """tileID → X"""
    count = MINI_COUNT_X if mini else MAIN_COUNT_X
    max_val = MINI_MAX if mini else MAIN_MAX
    v_fn = _v_mini if mini else _v_main
    val = ((tile_id % count) + count) % count - max_val
    return v_fn(val)


def get_y(tile_id, mini=False):
    """tileID → Y"""
    x = get_x(tile_id, mini)
    count = MINI_COUNT_X if mini else MAIN_COUNT_X
    max_val = MINI_MAX if mini else MAIN_MAX
    v_fn = _v_mini if mini else _v_main
    val = (max_val + 1) - math.ceil((tile_id - x) / count)
    return v_fn(int(val))


def get_id(x, y, mini=False):
    """(x, y) → tileID"""
    count = MINI_COUNT_X if mini else MAIN_COUNT_X
    max_val = MINI_MAX if mini else MAIN_MAX
    v_fn = _v_mini if mini else _v_main
    return (max_val + 1 - v_fn(y)) * count + v_fn(x) - max_val


def get_xy(tile_id, mini=False):
    """tileID → (x, y)"""
    return get_x(tile_id, mini), get_y(tile_id, mini)


def format_xy(tile_id, mini=False):
    """tileID → 字符串 '(x,y)'"""
    x, y = get_xy(tile_id, mini)
    return f"({x},{y})"


def ascii_map_window(cx, cy, radius=3, mini=False):
    """
    文字线框图：行 = y（上行 y 更大），列 = x 增大方向。
    @ = 中心格，. = 邻格（用 ASCII 点号，避免与数字列宽不一致）。与服务器 (x,y)/tileID 一致。
    """
    xs = list(range(cx - radius, cx + radius + 1))
    ys = list(range(cy + radius, cy - radius - 1, -1))
    cw = 6
    pad = "      "
    header_pad = " " * len(f"y={0:>4}|")
    lines = []
    tag = "小图 162×162" if mini else "主图 802×802 (mapId=1)"
    lines.append(f"# Earth2037 — {tag}")
    lines.append(f"# 窗口: 中心=({cx},{cy})  半径={radius}  |  x 轴向右为正")
    lines.append("")
    lines.append(header_pad + "".join(f"{x:^{cw}}|" for x in xs))
    row_sep = pad + "+" + "+".join("-" * cw for _ in xs) + "+"
    lines.append(row_sep)
    for y in ys:
        row = f"y={y:>4}|"
        for x in xs:
            ch = "@" if (x == cx and y == cy) else "."
            row += f"{ch:^{cw}}|"
        lines.append(row)
        lines.append(row_sep)
    lines.append("")
    lines.append(f"# 中心坐标 (x,y) = ({cx},{cy})   # 向玩家只描述坐标，不强调 tileID")
    lines.append("# 图例: @ = 中心; . = 邻格")
    return "\n".join(lines)


def ascii_map_from_tile_id(tile_id, radius=3, mini=False):
    """以 tileID 对应 (x,y) 为中心的 ASCII 窗口。"""
    x, y = get_xy(tile_id, mini)
    return ascii_map_window(x, y, radius=radius, mini=mini)


# --- QM HTTP + 按地块绘制 -------------------------------------------------

_qm_json_pat = re.compile(r"/svr\s+qm\s+(\[[\s\S]*\])", re.IGNORECASE)


def _field_type_char(ft: int) -> str:
    """
    单宽 ASCII，避免终端里中文双宽与数字列宽不一致导致竖线错位。
    人读对照：. 野地；1-7 田型；T 贸易站；F 要塞；^ 塔；B 基地；# 锁定
    """
    if ft == -1:
        return "#"
    if ft == 0:
        return "."
    if 1 <= ft <= 7:
        return str(ft)[0]
    if ft in (9, 10, 14, 15):
        return "T"
    if ft == 11:
        return "F"
    if ft == 12:
        return "^"
    if ft == 13:
        return "B"
    return "?"


def parse_qm_tiles(raw: str):
    """从响应中解析 QM 的 JSON 数组；每元素 [tileID, FieldType, ...]。"""
    if not raw or not isinstance(raw, str):
        return None
    m = _qm_json_pat.search(raw)
    if not m:
        return None
    try:
        arr = json.loads(m.group(1))
    except json.JSONDecodeError:
        return None
    if not isinstance(arr, list):
        return None
    rows = []
    for item in arr:
        if not isinstance(item, list) or len(item) < 2:
            continue
        try:
            tid = int(item[0])
            ft = int(item[1])
        except (TypeError, ValueError):
            continue
        rows.append((tid, ft, item))
    return rows


def ascii_map_from_qm_rows(rows: list, mini: bool, title: str = "") -> str:
    """根据 QM 返回的地块列表绘制矩形网格（未返回的格用空格）。"""
    if not rows:
        return "# QM 无地块数据（或服端过滤后为空）\n"

    cells = {}
    xs, ys = [], []
    for tid, ft, _ in rows:
        x, y = get_xy(tid, mini=mini)
        xs.append(x)
        ys.append(y)
        cells[(x, y)] = _field_type_char(ft)

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    x_rng = list(range(min_x, max_x + 1))
    y_rng = list(range(max_y, min_y - 1, -1))
    col_w = max(3, max(len(str(x)) for x in x_rng))
    header_pad = " " * len(f"y={0:>4}|")
    lines = []
    tag = "小图" if mini else "主图"
    lines.append(f"# Earth2037 QM — {tag}" + (f"  {title}" if title else ""))
    lines.append("# 行=y 上大下小，列=x 右增（符号均为单宽 ASCII，便于对齐）")
    lines.append("")
    lines.append(header_pad + "".join(f"{str(x):^{col_w}}|" for x in x_rng))
    pad = " " * len(header_pad)
    row_sep = pad + "+" + "+".join("-" * col_w for _ in x_rng) + "+"
    lines.append(row_sep)
    for y in y_rng:
        row = f"y={y:>4}|"
        for x in x_rng:
            ch = cells.get((x, y), " ")
            row += f"{ch:^{col_w}}|"
        lines.append(row)
        lines.append(row_sep)
    lines.append("")
    lines.append(
        "# 图例: .=野地0  1-7=田型  T=贸易  F=要塞  ^=塔  B=基地  #=锁定  ?=未知  空格=QM未返回本格"
    )
    return "\n".join(lines)


def run_qm(args: argparse.Namespace) -> int:
    base = os.path.dirname(os.path.abspath(__file__))
    if base not in sys.path:
        sys.path.insert(0, base)
    from cache import _game_command, _get_token, _load_config

    api_base = (args.api_base or os.environ.get("EARTH2037_API_BASE", "").strip() or _load_config()).rstrip("/")
    token = _get_token()
    if not token:
        print("❌ 需要 token：EARTH2037_TOKEN 或 config.json 中 token/apiKey", file=sys.stderr)
        return 1

    qm_args = args.qm_args
    raw = _game_command(api_base, token, "QM", qm_args)
    if re.search(r"/svr\s+qm\s+err", raw, re.I):
        print(raw, file=sys.stderr)
        return 1

    parsed = parse_qm_tiles(raw)
    if parsed is None:
        print("❌ 无法从响应中解析 /svr qm JSON。片段：", file=sys.stderr)
        print(raw[:1200], file=sys.stderr)
        return 1

    mini = args.mini
    if not mini and qm_args.strip():
        m = re.match(r"^\s*(\d+)\s+", qm_args)
        if m and int(m.group(1)) == 2:
            mini = True

    title = f"args={qm_args!r}" if qm_args.strip() else "args=(空 → 当前城 7×7)"
    print(ascii_map_from_qm_rows(parsed, mini=mini, title=title))
    print("")
    print("# --- 原始 /svr qm（首行截断）---")
    for line in raw.splitlines():
        if "/svr qm" in line.lower() and "err" not in line.lower():
            s = line.strip()
            print(s[:2500] + ("…" if len(s) > 2500 else ""))
            break
    return 0


def _legacy_tile(argv_tail: list) -> int:
    """maps_util.py <tileID> [--mini]"""
    if not argv_tail:
        return 2
    mini = "--mini" in argv_tail
    args = [a for a in argv_tail if a != "--mini"]
    try:
        tid = int(args[0])
    except (IndexError, ValueError):
        return 2
    x, y = get_xy(tid, mini)
    print(f"(x,y)=({x},{y})   # 玩家可见坐标；tileID={tid} 仅供程序换算")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])

    # 旧式长选项 → 子命令（与历史文档一致）
    if len(argv) >= 2 and argv[0] == "--ascii":
        argv = ["ascii"] + argv[1:]
    elif len(argv) >= 2 and argv[0] == "--ascii-tile":
        argv = ["ascii-tile"] + argv[1:]
    elif len(argv) >= 3 and argv[0] == "--id":
        argv = ["to-id"] + argv[1:]

    _subs = {"qm", "tile", "to-id", "ascii", "ascii-tile"}

    # 旧用法：仅「首参为整数」走 legacy（避免 --help 等被 int()）
    if (
        argv
        and argv[0] not in _subs
        and not str(argv[0]).startswith("-")
    ):
        try:
            int(argv[0])
            return _legacy_tile(argv)
        except ValueError:
            pass

    p = argparse.ArgumentParser(
        description="Earth2037 地图：坐标换算、ASCII 窗口、可选 HTTP QM 绘图",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
兼容旧用法:
  %(prog)s 142078 [--mini]
  %(prog)s --ascii -99 224 2 [--mini]
常用:
  %(prog)s qm                  # 需 token；QM 空参 = 当前城 7×7
  %(prog)s qm -a "1 -99,224,9,9"
        """.strip(),
    )
    p.add_argument("--mini", action="store_true", help="小图 mapId=2（162×162）")

    sub = p.add_subparsers(dest="cmd", required=True)

    p_tile = sub.add_parser("tile", help="tileID → (x,y)")
    p_tile.add_argument("tile_id", type=int)
    p_to_id = sub.add_parser("to-id", help="(x,y) → tileID")
    p_to_id.add_argument("x", type=int)
    p_to_id.add_argument("y", type=int)
    p_asc = sub.add_parser("ascii", help="以 (x,y) 为中心 ASCII 窗口")
    p_asc.add_argument("cx", type=int)
    p_asc.add_argument("cy", type=int)
    p_asc.add_argument("radius", type=int, nargs="?", default=3)
    p_at = sub.add_parser("ascii-tile", help="以 tileID 为中心 ASCII 窗口")
    p_at.add_argument("tile_id", type=int)
    p_at.add_argument("radius", type=int, nargs="?", default=3)
    p_qm = sub.add_parser("qm", help="POST QM 并按返回地块绘制 ASCII（需 token）")
    p_qm.add_argument(
        "-a",
        "--args",
        dest="qm_args",
        default="",
        help='QM 的 args，如 "1 -99,224,7,7"；默认空串（服端补当前城 7×7）',
    )
    p_qm.add_argument("--api-base", dest="api_base", default=None)

    if not argv:
        p.print_help()
        return 1

    args = p.parse_args(argv)
    mini = args.mini

    if args.cmd == "tile":
        x, y = get_xy(args.tile_id, mini)
        print(f"(x,y)=({x},{y})   # 玩家可见坐标；tileID={args.tile_id} 仅供程序换算")
        return 0
    if args.cmd == "to-id":
        print(get_id(args.x, args.y, mini))
        return 0
    if args.cmd == "ascii":
        print(ascii_map_window(args.cx, args.cy, radius=args.radius, mini=mini))
        return 0
    if args.cmd == "ascii-tile":
        print(ascii_map_from_tile_id(args.tile_id, radius=args.radius, mini=mini))
        return 0
    if args.cmd == "qm":
        args.mini = mini
        return run_qm(args)

    return 1


if __name__ == "__main__":
    sys.exit(main())
