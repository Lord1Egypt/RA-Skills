#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""图纸关系串联：把散图组织成「一套图」。

解决的问题
----------
单张图只能回答「这张图里有什么」，回答不了「这套图齐不齐」「哪张是这一层的结构、哪张是建筑」。
真实施工与算量必须跨专业对照（建筑 vs 结构、土建 vs 安装），前提是先知道图与图的关系。

本模块只做**关系推断**，输出五类结论：
1. 单体/标段聚类（路径目录 + 图号/分区前缀 + 轴网重叠度）
2. 楼层序列与缺口（能回答「这套图缺哪层」）
3. 专业判定（结构 / 建筑 / 给排水 / 暖通 / 电气 / 景观 / 人防 / 未知）
4. 图种判定（目录/总说明/专篇/系统图/大样/配筋/布置/立面剖面）
5. 跨专业配对 + 轴网核对（先定对照范围：楼层或楼栋；再按图种分档，
   配完再比一次轴网/标高，回答「这两张图是不是同一片区域」）

边界（红线）
------------
- 只推断关系与给建议，不改图纸、不算量、不做跨专业碰撞判定（碰撞是 qto_p3_clash 的职责）。
- 全部结论 inferred_candidate；不确定标 review_required 并给理由；final_quantity=false。
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "packs" / "structural-geometry" / "rules.json"

from cad_common import compact, load_rules  # noqa: E402
from cad_contract import contractize_payload  # noqa: E402
from cad_axis_net import compare_nets  # noqa: E402
from project_aggregate import (  # noqa: E402
    AGGREGATE_CONFIDENCE, UNKNOWN_FLOOR, UNKNOWN_ZONE, infer_floor, infer_zone,
    load_source, sheet_name,
)

SCHEMA = "cad-drawing-relation/v1"
CLEARANCE = "本表为图纸关系推断，非工程量，不可直接用于结算"

# 专业关键词：按「命中次数最多者胜」判定，避免单个词误判
DISCIPLINE_KEYWORDS: dict[str, list[str]] = {
    "结构": ["结构", "结施", "梁", "柱", "墙柱", "配筋", "顶板", "底板", "基础", "承台",
             "连系梁", "楼梯", "详图", "大样", "桩", "筏板", "锚固", "搭接"],
    "建筑": ["建筑", "建施", "平面", "立面", "剖面", "门窗", "装修", "做法", "墙身",
             "卫生间", "屋面做法", "楼梯间", "大样"],
    "给排水": ["给水", "排水", "给排", "水施", "消火栓", "喷淋", "雨水", "污水", "中水"],
    "暖通": ["暖通", "通风", "空调", "防排烟", "风管", "采暖", "冷热"],
    "电气": ["电气", "电施", "照明", "配电", "弱电", "火灾报警", "桥架", "防雷", "接地"],
    "景观": ["园林", "景观", "种植", "铺装", "绿化", "苗木", "园建"],
    "人防": ["人防", "防护", "密闭", "临空墙", "防爆"],
    "钢结构": ["钢结构", "钢梁", "钢柱", "网架", "桁架", "焊缝", "高强螺栓"],
}

# 构件类别（英文，来自 packs/structural-geometry/rules.json）→ 专业倾向
CATEGORY_DISCIPLINE = {"beam": "结构", "column": "结构", "slab": "结构",
                       "foundation": "结构", "stair": "结构", "wall": "结构"}

# ---- 图种（sheet kind）----
# 为什么需要它：跨专业对照只在**同类图**之间才成立。只按「同层」配对会把
# 「J-5#防火节能专篇」和「J-1结构（梁平法）」硬配成一组——专篇是报审文件，
# 图上没有可对照的构件位置，配进去等于给下游一个假信号：以为有资料可用。
# 实测 J 地块屋面层结构图 3 张（顶板布置 + 上/下皮配筋），建筑侧 5 张里有
# 3 张是防火节能专篇，真正可比的是「J车库屋面」那张。
SHEET_KIND_RULES: list[tuple[str, re.Pattern[str]]] = [
    ("目录", re.compile(r"目录|图纸清单|图册|封面")),
    ("总说明", re.compile(r"总说明|设计说明|统一说明|图纸说明|说明$")),
    ("专篇", re.compile(r"专篇|节能|防火|绿建|绿色建筑|消防专篇|人防专篇|环评|报审")),
    ("系统图", re.compile(r"系统图|原理图|配电系统|干线|控制原理|弱电系统|消防系统|水系图")),
    # 大样排在配筋之前：「8配筋大样」这类图是节点详图，不是整层配筋平面，
    # 若判成配筋会去和建筑平面配对，但两者的可比内容完全不同。
    ("大样", re.compile(r"大样|详图|节点|墙身|门窗表|门表|楼梯|坡道|雨蓬|雨棚|卫生间|"
                        r"集水坑|电梯井|机房详图|节点图")),
    ("配筋", re.compile(r"配筋|平法|钢筋|板筋|梁筋|柱筋|锚固|连系梁|板厚表|配筋表")),
    ("布置", re.compile(r"布置|定位|平面|顶板|底板|基础|承台|桩|筏板|结构|模板|"
                        r"车道|坡向|屋面|地面|楼面|层顶")),
    ("立面剖面", re.compile(r"立面|剖面|墙身大样")),
]

# 图种分档，直接决定「能不能配对」：
# - admin ：目录/总说明/专篇/系统图 —— 管理或说明性图纸，不含可对照的构件位置，一律不配对
# - detail：大样/详图 —— 只在同类之间配（节点对节点），不跨到平面
# - plan  ：平立剖 + 未识别 —— 构件位置/标高/洞口都落在这一档，可互相配对
SHEET_KIND_TIER = {"目录": "admin", "总说明": "admin", "专篇": "admin", "系统图": "admin",
                   "大样": "detail", "配筋": "plan", "布置": "plan",
                   "立面剖面": "plan", "未知": "plan"}

SHEET_KIND_UNKNOWN = "未知"
# 图种判不出来的平立面图仍允许配对，但降置信度：宁可给弱建议，也不要因为
# 一批图名不含关键词（实测「J车库地面」「样例二区J-2、3#楼（改消防）」就是）
# 就把整层配对全部丢掉。
WEAK_CONFIDENCE = 0.62

# ---- 楼栋 ----
# 楼层未知时按楼栋配对。「J-1结构」「J-2#」「J-5结构」「J-8#」这类成套楼栋图
# 本来就没有单一楼层（一套图覆盖全楼各层），它们全落在 unknown 楼层里；
# 若只按楼层分组，4 栋楼的结构图会和 4 栋楼的建筑图堆成一组——名义上「配上了」，
# 实际没法用。按楼栋号分才配得出「J-1结构 ↔ J-1#楼建筑」这种真能对照的组。
BUILDING_LIST_RE = re.compile(r"[Jj]\s*[-－]?\s*(\d{1,3}(?:\s*[，,、]\s*\d{1,3})*)\s*#?")
BUILDING_HASH_RE = re.compile(r"(\d{1,3})\s*#")
# 没有楼栋号时退到单体名（车库/换热站这类），否则这些图永远配不上
BUILDING_WORDS = ("车库", "换热站", "人防", "商业", "幼儿园", "配电房")

DRAWING_NO_RE = re.compile(r"(?<![A-Za-z0-9])([A-Z]{0,3}\d{1,3}[A-Za-z]?)(?:[-\s]?\d{1,3})?(?![A-Za-z0-9])")


def infer_discipline(name: str, payload: dict[str, Any] | None = None,
                     source: Path | None = None) -> dict[str, Any]:
    """专业判定：路径里的专业目录 > 图名关键词票 ×2 > 构件类别票 ×1。

    **路径优先**是有实测依据的：建筑图纸名常写成「J车库地面」「J车库屋面」，
    一个「建筑」字样都没有，而构件类别票（墙/柱/板）全指向结构，结果 15 张建筑图
    全被判成结构，跨专业对照永远配不上。图纸本来就是按专业分目录存盘的，
    目录名比图名可靠得多。图名与构件票只在路径认不出专业时兜底。
    """
    from_path = _discipline_from_path(source) if source is not None else ""
    if from_path:
        return {"discipline": from_path, "confidence": 0.95,
                "terms": [f"路径专业目录:{from_path}"], "ambiguous": False,
                "basis": "path"}

    scores: Counter[str] = Counter()
    hits: dict[str, list[str]] = defaultdict(list)
    text = compact(name)
    for discipline, words in DISCIPLINE_KEYWORDS.items():
        for word in words:
            if word in text:
                scores[discipline] += 2
                hits[discipline].append(word)

    for row in (payload or {}).get("members") or []:
        category = compact(row.get("category") or "")
        discipline = CATEGORY_DISCIPLINE.get(category)
        if discipline:
            scores[discipline] += 1

    if not scores:
        return {"discipline": "未知", "confidence": AGGREGATE_CONFIDENCE, "terms": [],
                "ambiguous": False, "basis": "none"}

    ranked = scores.most_common()
    top, top_score = ranked[0]
    ambiguous = len(ranked) > 1 and ranked[1][1] == top_score
    return {"discipline": top, "confidence": AGGREGATE_CONFIDENCE,
            "terms": hits.get(top, [])[:5], "ambiguous": ambiguous, "basis": "name+members"}


def infer_buildings(name: str) -> list[str]:
    """从图名取楼栋号（J-1/J-2…）或单体名（车库/换热站）。

    图名常把多个楼栋写在一起：「J-3#4#6#7#」「J4，6，7#」「J-2、3#楼」。
    两个正则各管一种写法，合起来去重：前者认 `J` 开头的逗号/顿号列表，
    后者认任何 `数字#` 片段。只用一个必然漏（实测 J-3#4#6#7# 只会取到 J-3）。
    """
    text = compact(name)
    found: list[str] = []
    for match in BUILDING_LIST_RE.finditer(text):
        for num in re.split(r"[，,、]", match.group(1)):
            num = num.strip()
            if num.isdigit():
                found.append(f"J-{int(num)}")
    for match in BUILDING_HASH_RE.finditer(text):
        found.append(f"J-{int(match.group(1))}")
    if not found:
        found = [word for word in BUILDING_WORDS if word in text]
    seen: dict[str, None] = {}
    for item in found:
        seen.setdefault(item, None)
    return list(seen)


def infer_sheet_kind(name: str, texts: list[str] | None = None) -> dict[str, Any]:
    """判图种：看**图名**，不看图内文字。

    试过把图内文字也纳进来，反而更差：成套图纸里每张图都有「本图说明」「防火」
    这类通用文字，混进来后专篇/总说明的命中会污染到正常平面图。图名是人起的，
    规律性远强于图内文字。
    """
    text = compact(name)
    for kind, pattern in SHEET_KIND_RULES:
        hit = pattern.search(text)
        if hit:
            return {"kind": kind, "tier": SHEET_KIND_TIER[kind],
                    "terms": [hit.group(0)], "basis": "name"}
    return {"kind": SHEET_KIND_UNKNOWN, "tier": SHEET_KIND_TIER[SHEET_KIND_UNKNOWN],
            "terms": [], "basis": "none"}


def grid_set(payload: dict[str, Any], limit: int = 4000) -> set[str]:
    """取一张图的轴号集合，用于算轴网重叠度。

    只收落在轴网图层上的（cad_structural_geometry 标了 `axis_layer`）。
    实测不过滤时 8 万个候选里 99.4% 来自 TEL_TEXT/TEXT_喷淋/图框，
    轴网重叠度会变成噪声平均——宁可这张图没有轴网，也不拿噪声充数。
    """
    values: set[str] = set()
    for row in payload.get("grids") or []:
        value = compact(row.get("value") or "")
        if not value:
            continue
        flag = row.get("axis_layer")
        # 老产物没有 axis_layer 字段：按形态放行，至少挡掉 PVC/SBS/C20 这类
        if flag is False:
            continue
        if flag is None and not AXIS_SHAPE.match(value):
            continue
        values.add(value)
        if len(values) >= limit:
            break
    return values


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    union = a | b
    return round(len(a & b) / len(union), 4) if union else 0.0


GRID_SAMPLE = 20
# 较小一侧轴号少于这个数就不下结论。实测 J-2~J-7 的结构图只解出 4~5 个轴号，
# 对上 3 个就是 75%——分母太小会把「几乎没数据」算成「高度一致」，比不判更糟。
MIN_GRID_SAMPLE = 10
# 轴号可接受的形态：1~3 位数字、1~2 位大写字母、或两者组合（1/A、A-1）。
# 其余（PVC/SBS/XPS 材料代号、C20/C30 混凝土标号、Co/Ltd 公司名残片、一二三 楼层词）
# 都不是轴号——它们混进来会把「重叠度」算成纯噪声。
# 注意：这条校验不改变提取逻辑（提取在 cad_structural_geometry.grid_candidates），
# 只用于判断「这批轴网数据能不能拿来比对」。先承认数据脏，再谈一致率。
AXIS_SHAPE = re.compile(r"^(?:\d{1,3}|[A-Z]{1,2}|\d{1,3}[/-][A-Z0-9]{1,3}|[A-Z][/-]\d{1,3})$")
DIRTY_LIMIT = 0.4


def grid_dirty_ratio(values: set[str]) -> float:
    """非轴号形态占比。超过 DIRTY_LIMIT 就不该拿这批值算重叠度。"""
    if not values:
        return 0.0
    bad = sum(1 for v in values if not AXIS_SHAPE.match(v))
    return round(bad / len(values), 4)


def grid_check(s_rows: list[dict[str, Any]], a_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """配对后真正比一次轴网，回答「这两张图描述的是不是同一片区域」。

    配对成立 ≠ 能对照。实测同层同类图种也可能分属不同分区（J 区 vs 车库区），
    轴线一个都对不上——这种配对拿去对构件位置/洞口只会得到一堆假差异。

    两条口径按可靠性排序：
    1. 几何轴网（轴线实体）——轴号文字抓不到，但轴线一直在图上，能给出总跨与开间；
    2. 文字轴号——只在几何不可用时兜底，且要先过「是不是轴号形态」的校验。
    """
    s_nets: list[dict[str, Any]] = []
    a_nets: list[dict[str, Any]] = []
    for r in s_rows:
        s_nets += r.get("axis_nets") or []
    for r in a_rows:
        a_nets += r.get("axis_nets") or []
    geo = compare_nets(s_nets, a_nets)
    if geo["verdict"] != "样本不足":
        base = {"shared": geo["shared"], "shared_ratio": geo["shared_ratio"],
                "structure_grids": geo["structure_grids"],
                "architecture_grids": geo["architecture_grids"],
                "sample": geo["sample"], "source": "geometry",
                "direction": geo["direction"], "span_delta": geo["span_delta"],
                "structure_span": geo["structure_span"],
                "architecture_span": geo["architecture_span"]}
        if geo["verdict"] == "轴网不对应":
            return {**base, "verdict": "轴网不对应", "note": geo["note"]}
        return {**base, "verdict": geo["verdict"], "note": geo["note"]}
    # 几何不可用时退回文字口径；把几何那一侧的原因也带上，别让人以为没试过
    return grid_check_text(s_rows, a_rows, geo_note=geo.get("note") or "")


def grid_check_text(s_rows: list[dict[str, Any]], a_rows: list[dict[str, Any]],
                    geo_note: str = "") -> dict[str, Any]:
    """文字轴号口径（兜底）。分母取**较小一侧**而不是并集：结构图常只画本区轴网，
    建筑图覆盖范围更大，用并集会把这个正常情况算成「重叠度低」。
    """
    s_grids: set[str] = set()
    for r in s_rows:
        s_grids |= r["grids"]
    a_grids: set[str] = set()
    for r in a_rows:
        a_grids |= r["grids"]
    base = {"shared": 0, "shared_ratio": 0.0,
            "structure_grids": len(s_grids), "architecture_grids": len(a_grids),
            "sample": [], "source": "text"}
    tail = f"；几何口径：{geo_note}" if geo_note else ""
    if not s_grids or not a_grids:
        return {**base, "verdict": "无法比对",
                "note": "一侧没有轴网/标高文字，只能人工看图对照" + tail}
    # 先验数据本身可不可信：实测一张图的 grids 里 40% 是 PVC/SBS/C20/Co/Ltd 这类
    # 短文字，拿它算出的「重叠 56.8%」看着精确，其实是噪声平均值。
    dirty = max(grid_dirty_ratio(s_grids), grid_dirty_ratio(a_grids))
    if dirty > DIRTY_LIMIT:
        return {**base, "verdict": "数据不可信", "dirty_ratio": dirty,
                "note": (f"轴网提取里 {dirty * 100:.0f}% 不是轴号形态（材料代号/标号/公司名残片），"
                         f"层叠率不可用；需先把轴网提取收紧到轴网图层再比") + tail}
    small = min(len(s_grids), len(a_grids))
    if small < MIN_GRID_SAMPLE:
        return {**base, "verdict": "样本不足", "dirty_ratio": dirty,
                "note": (f"较小一侧只有 {small} 个轴号（少于 {MIN_GRID_SAMPLE}），"
                         f"覆盖度不足以判定，需人工确认") + tail}
    shared = s_grids & a_grids
    ratio = round(len(shared) / small, 4)
    if ratio >= 0.6:
        verdict, note = "轴网一致", "轴号/标高大部分对得上，可逐项对照构件位置与洞口"
    elif ratio >= 0.2:
        verdict, note = "部分重叠", "轴号只对上一部分，可能分属不同分区，对照前先确认范围"
    else:
        verdict, note = "轴网不对应", "轴号几乎对不上，配对成立但多半不是同一片区域，勿直接对照"
    return {"verdict": verdict, "shared": len(shared), "shared_ratio": ratio,
            "structure_grids": len(s_grids), "architecture_grids": len(a_grids),
            "dirty_ratio": dirty,
            "sample": sorted(shared)[:GRID_SAMPLE], "note": note}


def floor_series(labels: list[tuple[str, int]]) -> dict[str, Any]:
    """把楼层排成序列并标缺口（只对连续数字楼层判缺口，屋面/机房层/基础/unknown 不参与）。"""
    orders = sorted({order for label, order in labels if label not in (UNKNOWN_FLOOR,)})
    numeric_pos = [o for o in orders if 1 <= o < 900]
    numeric_neg = [o for o in orders if -900 < o <= -1]
    gaps: list[str] = []
    for series, fmt in ((numeric_pos, "{0}F"), (numeric_neg, "{0}F")):
        if len(series) < 2:
            continue
        for missing in range(min(series), max(series) + 1):
            if missing not in series:
                gaps.append(fmt.format(missing))
    return {"orders": orders, "gaps": gaps}


CLUSTER_DIR_SUFFIXES = ("_detail", "_structural", "_scan")

# 图纸常见的专业目录名。图纸本来就是按专业分目录存档的，这是最可靠的信号：
# 图名未必写「建筑」（实际叫「J车库地面」「J车库屋面」），但目录一定分专业。
DISCIPLINE_DIRS = {
    "建筑": "建筑", "建筑施工图": "建筑", "建施": "建筑",
    "结构": "结构", "结构施工图": "结构", "结施": "结构",
    "暖通": "暖通", "暖通空调": "暖通", "通风": "暖通",
    "电气": "电气", "强电": "电气", "弱电": "电气",
    "给排水": "给排水", "给水排水": "给排水", "水暖": "给排水",
    "人防": "人防", "景观": "景观", "园林": "景观",
    "市政": "市政", "钢结构": "钢结构", "总图": "总图",
}


def _discipline_from_path(path: Path) -> str:
    """从路径里的专业目录段取专业；没有则返回空串。"""
    for part in reversed(path.parts[:-1]):
        mapped = DISCIPLINE_DIRS.get(str(part).strip())
        if mapped:
            return mapped
    return ""


def _cluster_key(path: Path) -> str:
    """聚类键：图纸所在项目目录。

    工具链产物常把每张图输出到 `<图纸名>_structural/detail.json`，此时该层目录是
    「按图分目录」而不是「项目目录」，必须上跳一级，否则同一套图会被拆成一图一簇。

    **再从专业目录往上跳一级**：一套图纸通常存成 `<项目>/结构/<子目录>`、
    `<项目>/建筑/<子目录>`。只看目录名会把同一单体的结构图和建筑图判成两个单体，
    跨专业对照就永远配不上（实测 J 地块 59 张图纸全被塞进一个 "structural" 簇）。

    分区（1J区/5J区…）不作为聚类键——同一车库的不同区仍是一个单体，只作簇内属性，
    并用轴网重叠度校验「是不是同一单体」。
    """
    parts = list(path.parent.parts)
    # 先找专业目录，找到就用它的上一级（项目目录）作键
    for index in range(len(parts) - 1, -1, -1):
        if str(parts[index]).strip() in DISCIPLINE_DIRS:
            return parts[index - 1] if index > 0 else parts[index]
    directory = path.parent
    if directory.name.endswith(CLUSTER_DIR_SUFFIXES):
        directory = directory.parent
    return directory.name or "-"


def _source_path(payload: dict[str, Any], fallback: Path) -> Path:
    """产物记录的源图路径（cad_scan 写进 source_paths）；没有就退回产物路径。"""
    for item in (payload.get("source_paths") or []):
        try:
            return Path(str(item))
        except (TypeError, ValueError):
            continue
    return fallback


def nets_digest(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """只留比对要用的字段：方向、轴数、总跨、开间序列。

    `positions` 是原始坐标，比对用不到，留着会让 relation.json 膨胀几倍。
    """
    out = []
    for net in payload.get("axis_nets") or []:
        if not isinstance(net, dict) or not net.get("gaps"):
            continue
        out.append({"direction": net.get("direction"),
                    "axis_count": net.get("axis_count"),
                    "span": net.get("span"),
                    "gaps": net.get("gaps"),
                    "score": net.get("score")})
    return out


def build(sources: list[tuple[Path, dict[str, Any]]]) -> dict[str, Any]:
    drawings: list[dict[str, Any]] = []
    for path, payload in sources:
        name = sheet_name(payload, path)
        texts = [compact((r.get("evidence") or [{}])[0].get("text", "")) for r in (payload.get("members") or [])]
        texts += [compact((r.get("evidence") or [{}])[0].get("text", "")) for r in (payload.get("rebars") or [])]
        floor = infer_floor(name, texts)
        source = _source_path(payload, path)
        discipline = infer_discipline(name, payload, source)
        kind = infer_sheet_kind(name, texts)
        drawings.append({
            "drawing": name, "path": str(path), "source_path": str(source),
            "floor": floor["label"],
            "floor_order": floor["order"], "floor_source": floor["source"],
            "zone": infer_zone(name), "buildings": infer_buildings(name),
            "discipline": discipline["discipline"],
            "discipline_terms": discipline["terms"], "discipline_ambiguous": discipline["ambiguous"],
            "sheet_kind": kind["kind"], "sheet_kind_tier": kind["tier"],
            "sheet_kind_terms": kind["terms"],
            "grids": grid_set(payload), "cluster_key": _cluster_key(source),
            # 几何轴网：轴号文字常抓不到，但轴线实体能给出总跨与开间，
            # 跨专业核对优先用它。老产物没有该字段就是空列表，退回文字口径。
            "axis_nets": nets_digest(payload),
        })

    clusters: dict[str, dict[str, Any]] = {}
    reviews: list[dict[str, Any]] = []
    for row in drawings:
        key = row["cluster_key"]
        node = clusters.setdefault(key, {"id": key, "directory": key, "drawings": [],
                                        "disciplines": Counter(), "zones": Counter(),
                                        "zone_grids": defaultdict(set), "grid_union": set()})
        node["drawings"].append(row["drawing"])
        node["disciplines"][row["discipline"]] += 1
        node["zones"][row["zone"]] += 1
        node["zone_grids"][row["zone"]] |= row["grids"]
        node["grid_union"] |= row["grids"]

    out_clusters: list[dict[str, Any]] = []
    for node in clusters.values():
        members = [r for r in drawings if r["cluster_key"] == node["id"]]
        series = floor_series([(r["floor"], r["floor_order"]) for r in members])
        out_clusters.append({
            "id": node["id"], "directory": node["directory"],
            "zones": [{"zone": z, "drawing_count": c} for z, c in node["zones"].most_common()],
            "drawing_count": len(node["drawings"]), "drawings": sorted(node["drawings"]),
            "disciplines": dict(node["disciplines"]),
            "floors": sorted({r["floor"] for r in members}),
            "floor_orders": series["orders"],
            "floor_gaps": series["gaps"],
            "confidence": AGGREGATE_CONFIDENCE, "status": "candidate",
        })
        if series["gaps"]:
            reviews.append({"type": "floor_gap", "reason": f"{node['id']} 楼层缺口：{'、'.join(series['gaps'])}",
                            "evidence": [{"cluster": node["id"]}]})
        if len(node["disciplines"]) > 1:
            reviews.append({"type": "cluster_mixed_discipline",
                            "reason": f"{node['id']} 同一目录混装多专业：{'、'.join(sorted(node['disciplines']))}",
                            "evidence": [{"cluster": node["id"]}]})
        # 轴网一致性：同目录不同分区之间重叠度过低，提示可能不是同一单体
        # unknown 不是真实分区（目录/大样/楼梯这类图本就不带分区），不参与轴网交叉比对，否则全是噪声
        zones = [z for z in node["zone_grids"] if z != UNKNOWN_ZONE and node["zone_grids"][z]]
        low: list[tuple[float, str, str]] = []
        for i in range(len(zones)):
            for j in range(i + 1, len(zones)):
                overlap = jaccard(node["zone_grids"][zones[i]], node["zone_grids"][zones[j]])
                if overlap < 0.30:
                    low.append((overlap, zones[i], zones[j]))
        if low:
            # 只出一条汇总，不逐对刷屏：不同分区本来就是各自的局部轴网，逐对报警会淹没有效信息
            low.sort()
            worst, za, zb = low[0]
            reviews.append({
                "type": "grid_low_overlap",
                "reason": (f"{node['id']} 有 {len(low)} 对分区轴网重叠低于 30%（最低 {za} vs {zb} 仅 {worst:.0%}）。"
                           f"分区各有局部轴网属正常，不能据此判定单体；如需确认请人工核对图签与轴网图"),
                "evidence": [{"cluster": node["id"], "pairs": len(low), "worst": worst},
                             {"zone": za}, {"zone": zb}]})

    # 跨专业配对建议：先分「对照范围」，再在范围内按图种分档配对
    #
    # 对照范围怎么定：
    # - plan 档（平面/配筋）：楼层可识别 → 按楼层；楼层不可识别 → 按楼栋。
    #   成套楼栋图（J-1结构 / J-2# / J-8#）本就覆盖全楼各层，没有单一楼层；
    #   若仍按楼层分组，4 栋楼的结构图会和 4 栋楼的建筑图堆成一大组，等于没配。
    # - detail 档（大样/详图）：整簇汇总，不细分。
    #   大样是节点做法图，同一套图里跨楼栋通用；若也按楼栋切，
    #   「10坡道施工图 / 8配筋大样 / 9J楼梯」这类图名不带楼栋号的，
    #   就配不上「J车库楼梯00」——本来可比的两张图被硬拆开。
    pairs: list[dict[str, Any]] = []
    for node in clusters.values():
        members = [r for r in drawings if r["cluster_key"] == node["id"]]
        scopes: dict[str, dict[str, Any]] = {}
        for row in members:
            if row["sheet_kind_tier"] == "admin":
                continue
            if row["sheet_kind_tier"] == "detail":
                keys = [("整簇", "大样汇总")]
            elif row["floor"] == UNKNOWN_FLOOR and row["buildings"]:
                keys = [("楼栋", b) for b in row["buildings"]]
            else:
                keys = [("楼层", row["floor"])]
            for kind, name in keys:
                scope = scopes.setdefault(f"{kind} {name}",
                                          {"kind": kind, "name": name, "rows": []})
                scope["rows"].append(row)

        missing_scopes: list[dict[str, Any]] = []
        for scope_key, scope in scopes.items():
            rows = scope["rows"]
            tier = "detail" if scope["kind"] == "整簇" else "plan"
            s_rows = [r for r in rows
                      if r["discipline"] == "结构" and r["sheet_kind_tier"] == tier]
            a_rows = [r for r in rows
                      if r["discipline"] == "建筑" and r["sheet_kind_tier"] == tier]
            if not s_rows:
                continue
            if not a_rows:
                missing_scopes.append({"scope": scope, "rows": s_rows})
                continue
            # 含未识别图种的配对降置信度：图名没关键词不等于不可比，
            # 但也不能和「两边都认出图种」的配对同等看待
            weak = [r["drawing"] for r in s_rows + a_rows
                    if r["sheet_kind"] == SHEET_KIND_UNKNOWN]
            check = grid_check(s_rows, a_rows)
            pairs.append({
                "cluster": node["id"], "scope": scope["name"], "scope_kind": scope["kind"],
                "floor": scope["name"] if scope["kind"] == "楼层" else UNKNOWN_FLOOR,
                "tier": tier,
                "structure": [r["drawing"] for r in s_rows],
                "architecture": [r["drawing"] for r in a_rows],
                "structure_kinds": sorted({r["sheet_kind"] for r in s_rows}),
                "architecture_kinds": sorted({r["sheet_kind"] for r in a_rows}),
                "reason": ("大样类同类可对照（节点做法/尺寸）" if tier == "detail"
                           else f"同{scope['kind']}平面/配筋类图可对照（构件位置/标高/洞口）"),
                "grid_check": check,
                "match_quality": "weak" if weak else "strong",
                "weak_members": weak,
                "confidence": WEAK_CONFIDENCE if weak else AGGREGATE_CONFIDENCE,
                "status": "candidate",
            })
            # 轴网对不上的配对要单独报：它形式上配上了，实质上不能拿去对构件
            if check["verdict"] == "轴网不对应":
                reviews.append({
                    "type": "pair_grid_mismatch",
                    "reason": (f"{node['id']} {scope['name']} 配对成立但轴网几乎不重叠"
                               f"（{check['shared']} 个共享轴，覆盖 "
                               f"{check['shared_ratio'] * 100:.0f}%），"
                               f"多半不是同一片区域，对照前需人工确认"),
                    "evidence": [{"cluster": node["id"]}, {"scope": scope["name"]}]})

        # 没配上的，必须说清原因，否则下游只看到「0 组配对」而不知道是被主动排除的
        # 未知专业也要算：专篇/目录这类图名常不含专业词，路径也未必带专业目录，
        # 漏掉的话「专篇被排除」这件事就没人说了
        admin = [r["drawing"] for r in members
                 if r["sheet_kind_tier"] == "admin"
                 and r["discipline"] in ("结构", "建筑", "未知")]
        if admin:
            reviews.append({
                "type": "pair_excluded_admin_sheets",
                "reason": (f"{node['id']} 有 {len(admin)} 张目录/总说明/专篇/系统图未参与跨专业配对"
                           f"（{'、'.join(admin[:3])}{'…' if len(admin) > 3 else ''}）："
                           f"这类图不含可对照的构件位置"),
                "evidence": [{"cluster": node["id"], "count": len(admin)}]})
        # 逐对照范围报缺，不并成一条：并起来就只能写「12 张结构图没配上」，
        # 说不清缺的是哪栋楼/哪一层，补图的人无从下手。
        for item in missing_scopes[:20]:
            scope, rows = item["scope"], item["rows"]
            names = [r["drawing"] for r in rows]
            reviews.append({
                "type": "missing_architecture",
                "reason": (f"{node['id']} {scope['kind']}{scope['name']} 有 {len(names)} 张结构图"
                           f"但无对应建筑图，无法跨专业对照"
                           f"（{'、'.join(names[:3])}{'…' if len(names) > 3 else ''}）"),
                "evidence": [{"cluster": node["id"]}, {"scope": scope["name"]}]})

    floor_rows: list[dict[str, Any]] = []
    for label in sorted({r["floor"] for r in drawings},
                        key=lambda x: next(r["floor_order"] for r in drawings if r["floor"] == x)):
        rows = [r for r in drawings if r["floor"] == label]
        floor_rows.append({"floor": label, "order": rows[0]["floor_order"],
                           "drawings": [r["drawing"] for r in rows],
                           "disciplines": sorted({r["discipline"] for r in rows}),
                           "confidence": AGGREGATE_CONFIDENCE, "status": "candidate"})

    payload = {
        "schema": SCHEMA,
        "clearance": CLEARANCE,
        "boundary": "只推断图纸关系（聚类/楼层序列/专业/轴网一致性/配对建议）；不改图纸、不算量、不做碰撞判定。",
        "source_count": len(sources),
        # 轴网全量留在内存里做比对，产物只留计数 + 样本：61 张图全给会有上千个轴号，
        # 下游要的是「配对有没有对上」，不是自己重算一遍轴网。
        "drawings": [{**{k: v for k, v in r.items() if k != "grids"},
                      "grid_count": len(r["grids"]),
                      "grids": sorted(r["grids"])[:200]} for r in drawings],
        "clusters": sorted(out_clusters, key=lambda r: (-r["drawing_count"], r["id"])),
        "floor_series": floor_rows,
        "pairs": pairs,
        "review": reviews,
        "summary": {
            "drawings": len(drawings),
            "clusters": len(out_clusters),
            "floor_series": len(floor_rows),
            "disciplines": dict(Counter(r["discipline"] for r in drawings)),
            "sheet_kinds": dict(Counter(r["sheet_kind"] for r in drawings)),
            "pairs": len(pairs),
            "pairs_strong": sum(1 for p in pairs if p["match_quality"] == "strong"),
            "pairs_grid_ok": sum(1 for p in pairs
                                 if p.get("grid_check", {}).get("verdict") == "轴网一致"),
            "pairs_grid_mismatch": sum(1 for p in pairs
                                       if p.get("grid_check", {}).get("verdict") == "轴网不对应"),
            "pairs_grid_inconclusive": sum(1 for p in pairs
                                           if p.get("grid_check", {}).get("verdict")
                                           in ("样本不足", "无法比对", "数据不可信")),
            "review_items": len(reviews),
        },
    }
    return payload


def write_markdown(payload: dict[str, Any], path: Path) -> None:
    s = payload["summary"]
    lines = ["# 图纸关系推断", "",
             f"- 图纸 {s['drawings']} 张，单体/标段 {s['clusters']} 个，楼层 {s['floor_series']} 个，"
             f"可对照配对 {s['pairs']} 组（强配对 {s.get('pairs_strong', 0)} 组），"
             f"轴网核对：一致 {s.get('pairs_grid_ok', 0)} / 不对应 {s.get('pairs_grid_mismatch', 0)}"
             f" / 判不了 {s.get('pairs_grid_inconclusive', 0)} 组",
             f"- 专业分布：" + "、".join(f"{k} {v}" for k, v in s["disciplines"].items()),
             f"- 图种分布：" + "、".join(f"{k} {v}" for k, v in (s.get("sheet_kinds") or {}).items()),
             f"- 待复核 {s['review_items']} 项", "", f"> {payload['clearance']}", "",
             "## 图纸清单", "", "| 图纸 | 楼层 | 分区 | 楼栋 | 专业 | 图种 | 专业依据 |",
             "|---|---|---|---|---|---|---|"]
    for row in payload["drawings"]:
        lines.append(f"| {row['drawing']} | {row['floor']} | {row['zone']} "
                     f"| {('、'.join(row.get('buildings') or [])) or '-'} | {row['discipline']} "
                     f"| {row.get('sheet_kind', '-')} | {('、'.join(row['discipline_terms'])) or '-'} |")

    lines += ["", "## 单体/标段聚类", "", "| 聚类 | 图纸数 | 专业 | 楼层 | 楼层缺口 |", "|---|---|---|---|---|"]
    for row in payload["clusters"]:
        lines.append(f"| {row['id']} | {row['drawing_count']} | {('、'.join(row['disciplines']))} | {('、'.join(row['floors']))} | {('、'.join(row['floor_gaps'])) or '无'} |")

    lines += ["", "## 跨专业配对与轴网核对", "",
              "先定对照范围（平面/配筋档：楼层可识别按楼层，否则按楼栋；大样档整簇汇总），"
              "再在范围内按图种配对。目录、总说明、专篇、系统图不参与配对；"
              "含未识别图种的配对置信度下调。", "",
              "配对上之后还会比一次轴网：同一层同类图也可能分属不同分区，"
              "轴线对不上就说明不是同一片区域。核对优先用**几何轴线**（轴号文字在天正图里多半抓不到），"
              "先比总跨再比开间；几何提不出轴网时才退回文字轴号，覆盖度按**较小一侧**算。", ""]
    if payload["pairs"]:
        lines += ["| 聚类 | 对照范围 | 档 | 结构图 | 建筑图 | 配对强度 | 轴网核对 |",
                  "|---|---|---|---|---|---|---|"]
        for row in payload["pairs"]:
            gc = row.get("grid_check") or {}
            if gc.get("source") == "geometry":
                grid_txt = (f"{gc.get('verdict', '-')}（几何·{gc.get('direction', '-')}向 "
                            f"{gc.get('structure_grids', 0)}轴/{gc.get('architecture_grids', 0)}轴，"
                            f"跨度差 {gc.get('span_delta', 0) * 100:.1f}%，"
                            f"开间重合 {gc.get('shared_ratio', 0) * 100:.0f}%）")
            elif gc:
                grid_txt = (f"{gc.get('verdict', '-')}（文字·共享 {gc.get('shared', 0)}，"
                            f"覆盖 {gc.get('shared_ratio', 0) * 100:.0f}%）")
            else:
                grid_txt = "-"
            lines.append(f"| {row['cluster']} | {row.get('scope_kind', '楼层')} {row.get('scope', row['floor'])} "
                         f"| {row['tier']} | {('、'.join(row['structure']))} "
                         f"| {('、'.join(row['architecture']))} | {row['match_quality']} | {grid_txt} |")
    else:
        lines.append("无（缺少同层同类图种，或建筑侧只有专篇/目录类图纸）")

    lines += ["", "## 待复核", ""]
    if payload["review"]:
        lines += ["| 类型 | 原因 |", "|---|---|"]
        for row in payload["review"][:80]:
            lines.append(f"| {row['type']} | {row['reason']} |")
    else:
        lines.append("无")
    lines += ["", f"> {payload['boundary']}", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    import pyboot
    pyboot.ensure_utf8_io()
    parser = argparse.ArgumentParser(description="图纸关系推断：聚类/楼层序列/专业/轴网一致性/配对建议。")
    parser.add_argument("--inputs", nargs="+", required=True)
    parser.add_argument("--out", default="图纸关系.json")
    parser.add_argument("--md-out", default="")
    parser.add_argument("--rules", default=str(RULES_PATH))
    args = parser.parse_args()

    rules = load_rules(Path(args.rules))
    sources = []
    for value in args.inputs:
        src = Path(value)
        if not src.exists():
            raise FileNotFoundError(src)
        sources.append((src, load_source(src, rules)))

    payload = build(sources)
    payload = contractize_payload(payload, source=[p.name for p, _ in sources])
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    outputs = [str(out)]
    if args.md_out:
        mp = Path(args.md_out)
        mp.parent.mkdir(parents=True, exist_ok=True)
        write_markdown(payload, mp)
        outputs.append(str(mp))
    print(json.dumps({"source_count": len(sources), "summary": payload["summary"],
                      "contract": payload["contract"]["summary"], "outputs": outputs}, ensure_ascii=False))


if __name__ == "__main__":
    main()
