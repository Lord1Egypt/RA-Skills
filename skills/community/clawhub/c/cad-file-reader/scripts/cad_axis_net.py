#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""几何轴网提取：从 LINE 实体还原轴网，供跨专业对照使用。

为什么不用文字轴号
------------------
轴号在天正导出的 DWG 里往往是「圆 + 线 + 文字」的组合对象，转 T3/导出后
文字常常丢失或不落在轴网图层上。实测这批 61 张图里，轴网图层上有 0 条文字，
靠 `grid_pattern` 正则抓到的「轴号」99.4% 来自电话、喷淋、图签图层。
所以轴号文字这条路做不出可用轴网。

轴线本身却一直在图上：它是一组等长、互相平行、等距重复的直线。
本模块只认几何，不认文字，把轴线找出来并按「间距序列」输出指纹。

比对口径
--------
轴网指纹 = 单方向的间距序列（相邻轴线的距离），比较时用
  ① 总跨相对差（同栋同层的轴网总跨应几乎相等）
  ② 间距多重集重叠率（容差 2% 或 60mm）
两项都不需要轴号，也不需要两图坐标系对齐。

边界
----
- 只输出候选轴网与证据，不判定「这两张图一定是同一栋楼」：
  同户型不同楼栋共用同一套轴网，间距会完全一致。本模块能证明「不一致」，
  不能证明「是同一片区域」，后者仍需人工看图层/范围。
- 图纸若把轴线画成多段短线（不连续），本模块会判为「无轴网」而不是硬凑。
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

# 轴网图层：实测这批图在 AXIS / AXIS_TEXT / AXIS_NUM / 结_轴线 / SOCK-DOTE 上。
# 注意 AXIS 在部分设计院被当成通用线层（喷管、桥架也画在上面），
# 所以图层只是入口条件，能不能成为轴线还要过长度/等距两道判定。
AXIS_LAYER = re.compile(r"轴|AXIS|SOCK-DOTE|GRID|定位", re.I)

MIN_AXIS_LEN = 2000.0   # 轴线最短长度(mm)。短于此的是尺寸线、符号、填充
MERGE_TOL = 100.0       # 同一位置的重复轴线合并容差(mm)
# 共线短段拼接：天正导出的轴线常被切成多段（J-2# 轴网层最长段仅 3000mm，
# 而该楼轴距 6~9m），不先接起来就会把「被切碎的轴」判成「没有轴」。
COLLINEAR_TOL = 1.0     # 同一直线的位置容差(mm)，同一段轴的坐标是精确值
STITCH_GAP = 300.0      # 同一直线上两段之间允许的空隙(mm)，超过就断成两段
MIN_AXIS_COUNT = 3      # 少于 3 轴不构成轴网（2 轴只能定一个方向）
MAX_AXIS_COUNT = 40     # 一般住宅/车库轴网 3~30 轴，超过 40 基本是把墙线当轴线了
VIEW_SPLIT_FACTOR = 4.0  # 视图断开阈值 = max(4×中位间距, 20000)，且不超过 30000
VIEW_SPLIT_FLOOR = 20000.0
# 上限：中位间距不能无限放大断开阈值，否则「同一根轴在多视图里的副本」
# 会被当成一条 255m 跨的假轴网（实测 J-1 结构图 6 个副本间距 51000，
# 4×51000=204000 让它们连成一条，比不判更糟）。30m 以上的柱距基本不存在。
VIEW_SPLIT_CEIL = 30000.0
TINY_GAP = 1000.0       # 小于 1m 的间距视为碎片（附加轴线/标注残留）

MATCH_SPAN_TOL = 0.02   # 总跨相对差在此以内算「跨距吻合」
MATCH_COVER = 0.60      # 间距多重集重叠率在此以上算「间距吻合」
PARTIAL_COVER = 0.40
MISMATCH_SPAN = 0.10


def _round_to(value: float, step: float) -> float:
    return round(value / step) * step


def _stitch(segments: list[Any], layers: list[Any], min_len: float) -> list[list[Any]]:
    """把轴网图层上共线的短段接成一条线，返回 [x1,y1,x2,y2,layer]。

    天正转出的轴线常被切成多段：实测 J-2# 轴网层最长线段只有 3000mm，
    而该楼轴网跨 6~9m。不先接起来，「轴线最短 2000mm」这条判据会把整张图
    判成没有轴网——不是图上没有轴，是轴被切碎了。
    只处理水平/垂直段；斜轴线（弧形墙、异形柱网）不在此列，跳过。
    """
    buckets: dict[tuple[str, float, str], list[tuple[float, float]]] = defaultdict(list)
    for seg, layer in zip(segments or [], layers or []):
        if not isinstance(seg, (list, tuple)) or len(seg) < 4:
            continue
        name = str(layer or "")
        if not AXIS_LAYER.search(name):
            continue
        try:
            x1, y1, x2, y2 = (float(v) for v in seg[:4])
        except (TypeError, ValueError):
            continue
        if abs(y2 - y1) <= 1e-3:
            pos = round(y1 / COLLINEAR_TOL) * COLLINEAR_TOL
            buckets[("H", pos, name)].append((min(x1, x2), max(x1, x2)))
        elif abs(x2 - x1) <= 1e-3:
            pos = round(x1 / COLLINEAR_TOL) * COLLINEAR_TOL
            buckets[("V", pos, name)].append((min(y1, y2), max(y1, y2)))
    merged: list[list[Any]] = []
    for (direction, pos, name), spans in buckets.items():
        spans.sort()
        a0, b0 = spans[0]
        for a, b in spans[1:]:
            if a <= b0 + STITCH_GAP:
                b0 = max(b0, b)
                continue
            if b0 - a0 >= 1.0:
                merged.append(_as_seg(direction, pos, a0, b0, name, min_len))
            a0, b0 = a, b
        if b0 - a0 >= 1.0:
            merged.append(_as_seg(direction, pos, a0, b0, name, min_len))
    return [m for m in merged if m is not None]


def _as_seg(direction: str, pos: float, a: float, b: float, name: str, min_len: float):
    length = b - a
    if length < min_len:
        return None
    if direction == "H":
        return [a, pos, b, pos, name, length]
    return [pos, a, pos, b, name, length]
    """把同一位置的多条线合并成一条轴线。

    items 已按位置排序。合并后保留首个位置与层名，供证据追溯。
    """
    merged: list[dict[str, Any]] = []
    for pos, a, b, layer in items:
        if merged and abs(pos - merged[-1]["pos"]) < MERGE_TOL:
            merged[-1]["dups"] += 1
            merged[-1]["a"] = min(merged[-1]["a"], a)
            merged[-1]["b"] = max(merged[-1]["b"], b)
            continue
        merged.append({"pos": round(pos, 3), "a": a, "b": b, "layer": layer, "dups": 0})
    return merged


def _merge_positions(items: list[tuple[float, float, float, str]]) -> list[dict[str, Any]]:
    """把同一位置的多条线合并成一条轴线。

    items 已按位置排序。合并后保留首个位置与层名，供证据追溯。
    同一根轴常被两个图层各画一遍（结_轴线 + AXIS），不合并会把轴数算重。
    """
    merged: list[dict[str, Any]] = []
    for pos, a, b, layer in items:
        if merged and abs(pos - merged[-1]["pos"]) < MERGE_TOL:
            merged[-1]["dups"] += 1
            merged[-1]["a"] = min(merged[-1]["a"], a)
            merged[-1]["b"] = max(merged[-1]["b"], b)
            continue
        merged.append({"pos": round(pos, 3), "a": a, "b": b, "layer": layer, "dups": 0})
    return merged


def _split_views(axes: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    """同一长度组里可能塞了多个视图（同一栋楼的标准层被复制到不同位置）。

    视图之间的空档远大于轴网内部间距，用「4 倍中位间距」断开；
    大柱距厂房（24m）的中位间距本身就是 24m，阈值会自动放大，不会误切。
    """
    if len(axes) < 2:
        return [axes]
    gaps = [axes[i + 1]["pos"] - axes[i]["pos"] for i in range(len(axes) - 1)]
    # 算断簇阈值时排除碎片间隙：双线轴（同一根轴画两条相距 800mm 的线）
    # 会把中位数拉到 800，阈值跟着变小，视图间距就切不开了。
    solid = [g for g in gaps if g >= TINY_GAP] or gaps
    med = sorted(solid)[len(solid) // 2]
    limit = min(max(VIEW_SPLIT_FACTOR * med, VIEW_SPLIT_FLOOR), VIEW_SPLIT_CEIL)
    views: list[list[dict[str, Any]]] = [[axes[0]]]
    for i, gap in enumerate(gaps):
        if gap > limit:
            views.append([axes[i + 1]])
        else:
            views[-1].append(axes[i + 1])
    return views


def _score(gaps: list[float]) -> tuple[float, float, int]:
    """给一个候选轴网打分：间距重复率 ×(1−碎片率)。

    真实轴网的间距是模数的重复（3000/3300/3600 反复出现）；
    噪声（墙线、标注）的间距几乎两两不同，重复率接近 0。
    """
    if len(gaps) < 2:
        return 0.0, 0.0, 0
    vals = Counter(_round_to(g, 10) for g in gaps)
    repeated = [v for v, c in vals.items() if c >= 2]
    cover = 0.0
    if repeated:
        cover = sum(c for v, c in vals.items()
                    if any(abs(v - r) <= max(20.0, 0.02 * r) for r in repeated)) / len(gaps)
    tiny = sum(1 for g in gaps if g < TINY_GAP) / len(gaps)
    return round(cover, 4), round(tiny, 4), len(set(_round_to(g, 10) for g in gaps))


def axis_nets(segments: list[Any], layers: list[Any], *,
              min_len: float = MIN_AXIS_LEN) -> list[dict[str, Any]]:
    """从一张图的几何段里提取轴网候选。

    输入与 cad_scan 的 `geometry_segments[i]` / `geometry_layers[i]` 一一对应。
    输出按可信度降序，每项是一条独立的轴网（一个视图的一个方向）。

    先用原始线段算；某个方向提不出来时才启用共线拼接补算。
    不无条件拼接：完整轴线拼接后端点不齐，长度分组会漂，实测会把建筑图
    从 25 轴并成 20 轴、轴距从 3000 变成 3600，反而把对的判成错的。
    """
    nets = _nets_from(segments, layers, min_len, stitched=False, relax_len=False)
    missing = {"H", "V"} - {n["direction"] for n in nets if n["score"] >= 0.40}
    if missing:
        extra = _nets_from(segments, layers, min_len, stitched=True, relax_len=True)
        nets += [n for n in extra if n["direction"] in missing]
    nets.sort(key=lambda n: (-n["score"], -n["axis_count"]))
    # 同一轴网在同一张图里常有多个副本（标准层被复制到不同位置），
    # 指纹相同的只留一个，否则下游比对会拿同一套轴网自己跟自己对。
    unique: list[dict[str, Any]] = []
    seen: set[tuple[str, float, tuple[float, ...]]] = set()
    for net in nets:
        key = (net["direction"], net["span"], tuple(net["gaps"]))
        if key in seen:
            continue
        seen.add(key)
        unique.append(net)
    return unique


def _nets_from(segments: list[Any], layers: list[Any], min_len: float, *,
               stitched: bool, relax_len: bool) -> list[dict[str, Any]]:
    """单次提取。stitched=True 时先把共线短段接成长线。"""
    if stitched:
        lines = [(s[0], s[1], s[2], s[3], s[4], s[5]) for s in _stitch(segments, layers, min_len)]
    else:
        lines = []
        for seg, layer in zip(segments or [], layers or []):
            if not isinstance(seg, (list, tuple)) or len(seg) < 4:
                continue
            name = str(layer or "")
            if not AXIS_LAYER.search(name):
                continue
            try:
                x1, y1, x2, y2 = (float(v) for v in seg[:4])
            except (TypeError, ValueError):
                continue
            if abs(y2 - y1) <= 1e-3:
                length = abs(x2 - x1)
                if length >= min_len:
                    lines.append((x1, y1, x2, y2, name, length))
            elif abs(x2 - x1) <= 1e-3:
                length = abs(y2 - y1)
                if length >= min_len:
                    lines.append((x1, y1, x2, y2, name, length))

    raw: dict[tuple[str, float], list[tuple[float, float, float, str]]] = defaultdict(list)
    for x1, y1, x2, y2, name, length in lines:
        if abs(y2 - y1) <= 1e-3:
            raw[("H", length)].append((y1, min(x1, x2), max(x1, x2), name))
        else:
            raw[("V", length)].append((x1, min(y1, y2), max(y1, y2), name))

    # 同一视图的轴线长度几乎一致。拼接后端点不齐会有几十毫米差
    # （实测 87071 与 86271 相差 0.9%），精确按 10mm 分桶会把同一组轴拆散，
    # 所以拼接路径按 1% 相对容差归并；原始路径仍走精确桶，避免跨视图混组。
    buckets: dict[tuple[str, float], list[tuple[float, float, float, str]]] = {}
    for direction in ("H", "V"):
        groups = sorted((ln, items) for (d, ln), items in raw.items() if d == direction)
        merged: list[list[Any]] = []
        for length, items in groups:
            tol = max(50.0, merged[-1][0] * 0.01) if merged else 0.0
            if merged and relax_len and abs(length - merged[-1][0]) <= tol:
                merged[-1][1].extend(items)
            else:
                merged.append([length, list(items)])
        for length, items in merged:
            buckets[(direction, _round_to(length, 10))] = items

    nets: list[dict[str, Any]] = []
    for (direction, length), items in buckets.items():
        items.sort()
        axes = _merge_positions(items)
        if len(axes) < MIN_AXIS_COUNT:
            continue
        for view in _split_views(axes):
            if not (MIN_AXIS_COUNT <= len(view) <= MAX_AXIS_COUNT):
                continue
            pos = [a["pos"] for a in view]
            gaps = [round(pos[i + 1] - pos[i], 1) for i in range(len(pos) - 1)]
            cover, tiny, kinds = _score(gaps)
            # 轴数因子：3 轴只能定一个方向的两端，可信度打折
            factor = min(1.0, (len(pos) - 2) / 3.0)
            score = round(cover * (1 - tiny) * factor, 4)
            # 层名取该视图里出现最多的轴网层，便于回溯
            layer = Counter(a["layer"] for a in view).most_common(1)[0][0]
            span = round(sum(gaps), 1)
            nets.append({
                "direction": direction,
                "axis_count": len(pos),
                "length": round(length, 1),
                "positions": pos,
                "gaps": gaps,
                "span": span,
                "gap_cover": cover,
                "tiny_ratio": tiny,
                "gap_kinds": kinds,
                "layer": layer,
                "score": score,
                "extent": [round(view[0]["a"], 1), round(view[-1]["b"], 1)],
                "evidence": {"dir": direction, "length": round(length, 1),
                             "axis_layer": layer, "dups_merged": sum(a["dups"] for a in view)},
            })
    return nets


def _gap_overlap(ga: list[float], gb: list[float], max_window: int = 4) -> tuple[float, float]:
    """间距多重集重叠率（一对一匹配，容差 2% 或 60mm）。

    除了直接匹配，还接受「结构一个开间 = 建筑连续几个开间之和」：
    结构图只画柱网，建筑图会在柱网之间插入隔墙定位轴，同一个 3300 开间
    在建筑图上可能被画成 1500+1800 两段。只比等值会把这种正常情况
    算成「对不上」，进而把同一栋楼判成不是同一区域。
    """
    if not ga or not gb:
        return 0.0, 0.0
    used = [False] * len(gb)
    hit_a = 0
    for g in ga:
        tol = max(60.0, 0.02 * g)
        found = False
        for i, h in enumerate(gb):
            if not used[i] and abs(g - h) <= tol:
                used[i] = True
                found = True
                break
        if found:
            hit_a += 1
            continue
        # 段和匹配：窗口 2~max_window 段之和等于这个开间
        for w in range(2, max_window + 1):
            if found:
                break
            for i in range(len(gb) - w + 1):
                if any(used[i:i + w]):
                    continue
                if abs(sum(gb[i:i + w]) - g) <= tol:
                    for k in range(i, i + w):
                        used[k] = True
                    found = True
                    break
        if found:
            hit_a += 1
    hit_b = sum(1 for u in used if u)
    return round(hit_a / len(ga), 4), round(hit_b / len(gb), 4)


def _pair(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any] | None:
    if a["direction"] != b["direction"]:
        return None
    if a["axis_count"] < MIN_AXIS_COUNT or b["axis_count"] < MIN_AXIS_COUNT:
        return None
    big = max(a["span"], b["span"])
    if big <= 0:
        return None
    span_delta = abs(a["span"] - b["span"]) / big
    cover_a, cover_b = _gap_overlap(a["gaps"], b["gaps"])
    # 主判据用结构侧覆盖：结构柱网是建筑轴网的子集属正常，
    # 用两侧最大值会让「结构只对上 3 个开间、建筑有 30 个」也算一致。
    cover = cover_a
    # 三项加权：总跨接近 0.35 + 开间重合 0.30 + **绝对匹配开间数** 0.35。
    # 第三项不能省：只按比例打分时，轴少的小轴网更容易做到「全部对上」，
    # 会压过轴多、证据更足的大轴网（实测 J-1 结构 8 轴子网得分 0.73
    # 压过 14 轴主轴网 0.80→0.73，把本来一致的判成部分重叠）。
    matched = cover_a * max(1, a["axis_count"] - 1)
    score = round((1 - span_delta) * 0.35 + cover * 0.30
                  + min(1.0, matched / 8.0) * 0.35, 4)
    return {"span_delta": round(span_delta, 4), "cover": cover,
            "cover_a": cover_a, "cover_b": cover_b, "score": score,
            "matched": round(matched, 1),
            "extra_axes": b["axis_count"] - a["axis_count"]}


def verdict_of(best: dict[str, Any], s_count: int = 99) -> tuple[str, str]:
    """判读一对轴网。

    主判据是**结构侧覆盖率**（结构图的开间有多少能在建筑图里找到），
    不是两侧的最大值：结构柱网通常只是建筑轴网的子集（建筑多出外墙轴、
    门窗定位轴），用最大值会让「结构只对上 3 个开间、建筑有 30 个」也算一致。
    反向覆盖（建筑被结构完全包含）极少见，不作为一致依据。
    """
    span_delta, cover = best["span_delta"], best["cover_a"]
    cover_max = best["cover"]
    # 轴太少时，即使完全吻合也要谨慎：3 个开间全中也可能只是模数巧合
    # 3 轴（2 个开间）一律不下「一致」结论：两个开间同时命中的概率不低。
    # 4~5 轴只有在跨差≈0 且开间几乎全中时才放行（J-5 就是 4 轴全中）。
    tiny = s_count < 4 or (s_count < 6 and not (span_delta <= 0.01 and cover_max >= 0.99))
    if cover >= 0.65 and span_delta <= 0.15 and not tiny:
        extra = best.get("extra_axes", 0)
        note = "结构柱网能在建筑轴网里逐跨对上"
        if extra > 0:
            note += f"（建筑侧多 {extra} 轴，多为外墙/门窗定位轴，属正常详略差异）"
        return "轴网一致", note + "，可逐项对照构件位置与洞口"
    if cover >= 0.40 or cover_max >= 0.60:
        return ("部分重叠",
                "只对上一部分开间：两专业轴网详略不同（结构常合并跨过楼梯间的轴），"
                "或分属相邻分区，对照前先确认可比范围")
    if tiny and cover_max >= 0.60:
        return ("部分重叠",
                "结构侧轴数太少（少于 6 轴），即便开间吻合也不足以证明是同一片区域，需人工确认")
    return "轴网不对应", "开间几乎对不上，多半不是同一片区域，勿直接对照"


def compare_nets(s_nets: list[dict[str, Any]], a_nets: list[dict[str, Any]],
                 max_nets: int = 40) -> dict[str, Any]:
    """比两张图的轴网，取最匹配的一对作为结论依据。

    任一侧没有可用轴网就返回「样本不足」，不猜测。
    """
    base = {"shared": 0, "shared_ratio": 0.0,
            "structure_grids": len(s_nets), "architecture_grids": len(a_nets),
            "source": "geometry"}
    if not s_nets or not a_nets:
        return {**base, "verdict": "样本不足",
                "note": "一侧没有提取到可用几何轴网（轴线不连续或不在轴网图层），只能人工看图对照"}
    best = None
    for a in s_nets[:max_nets]:
        for b in a_nets[:max_nets]:
            cand = _pair(a, b)
            if not cand:
                continue
            if best is None or cand["score"] > best[1]["score"]:
                best = (a, cand, b)
    if best is None:
        return {**base, "verdict": "样本不足",
                "note": "两侧轴网方向不齐（缺水平或垂直轴网），无法构成可比网格"}
    a, cand, b = best
    verdict, note = verdict_of(cand, a["axis_count"])
    return {
        "verdict": verdict,
        "direction": a["direction"],
        "span_delta": cand["span_delta"],
        "shared_ratio": cand["cover_a"],
        "shared": max(1, round(cand["cover_a"] * max(1, a["axis_count"] - 1))),
        "structure_grids": a["axis_count"],
        "architecture_grids": b["axis_count"],
        "structure_span": a["span"],
        "architecture_span": b["span"],
        "sample": a["gaps"][:8],
        "source": "geometry",
        "score": cand["score"],
        "note": (f"{note}（结构 {a['axis_count']} 轴 总跨 {a['span']:.0f}mm，"
                 f"建筑 {b['axis_count']} 轴 总跨 {b['span']:.0f}mm，"
                 f"跨度差 {cand['span_delta'] * 100:.1f}%，"
                 f"结构开间重合 {cand['cover_a'] * 100:.0f}%）"),
    }


def nets_from_payload(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """从结构识图产物取轴网；老产物没有该字段时用内嵌几何现算一次。"""
    cached = payload.get("axis_nets")
    if isinstance(cached, list):
        return cached
    meta = payload.get("meta") or {}
    segments = meta.get("geometry_segments")
    layers = meta.get("geometry_layers")
    if not segments or not layers:
        return []
    # 兼容「按文件分组」的两层结构：取第一个文件的几何
    if segments and isinstance(segments[0], (list, tuple)) and segments[0] \
            and isinstance(segments[0][0], (list, tuple)):
        segments = segments[0]
        layers = layers[0] if layers and isinstance(layers[0], list) else layers
    return axis_nets(segments, layers)


def _main() -> None:
    parser = argparse.ArgumentParser(description="从 cad_scan 详情 JSON 提取几何轴网")
    parser.add_argument("--inputs", nargs="+", required=True, help="cad_scan --with-geom 的详情 JSON")
    parser.add_argument("--out", default="", help="输出 JSON 路径，默认打印到 stdout")
    parser.add_argument("--min-len", type=float, default=MIN_AXIS_LEN)
    args = parser.parse_args()

    rows = []
    for value in args.inputs:
        path = Path(value)
        data = json.loads(path.read_text(encoding="utf-8"))
        segs = (data.get("geometry_segments") or [[]])[0] or []
        lays = (data.get("geometry_layers") or [[]])[0] or []
        nets = axis_nets(segs, lays, min_len=args.min_len)
        good = [n for n in nets if n["score"] >= 0.5 and n["gap_kinds"] >= 2]
        rows.append({
            "file": path.name, "nets": len(nets), "usable": len(good),
            "best_h": next((n for n in good if n["direction"] == "H"), None),
            "best_v": next((n for n in good if n["direction"] == "V"), None),
        })
    payload = {"schema": "cad-axis-net/v1", "files": rows,
               "summary": {"files": len(rows),
                           "with_both": sum(1 for r in rows if r["best_h"] and r["best_v"])}}
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(json.dumps(payload["summary"], ensure_ascii=False))
    else:
        print(text)


if __name__ == "__main__":
    _main()
