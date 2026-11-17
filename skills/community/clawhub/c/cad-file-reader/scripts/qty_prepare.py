#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""算量前置准备：把一张图「该按哪个图框算、板厚多少」定下来，交给算量技能。

为什么单独一个脚本
------------------
算量技能（tujian 等）的 `--floor-label` 实际是**图框标题**，不是楼层号：
`beam_instances_for_label` 用 `sheet_label == floor_label` 精确比对，传 `-0.050`
匹配不上 `-0.050梁平法施工图`，一条梁都取不到，量直接为 0。
而图框标题只有读过这张图的人才知道——所以由识图侧先把候选标题算出来。

同时给出板厚与标号：算量技能不传板厚时，板体积恒为 0，混凝土量只有梁没有板。

用法
----
    python3 qty_prepare.py --inputs a_detail.json b_detail.json --out prep.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

SCHEMA = "cad-qty-prepare/v1"
CLEARANCE = "本表只给算量入口参数（图框标题/板厚/标号），不是工程量"

# 梁标注类图框优先：只有这类图框里才有梁标注，算梁量必须用它。
BEAM_SHEET_HINT = re.compile(r"梁平法|梁配筋|梁施工图|BEAM", re.I)
# 明显不是算量对象的图框
NON_QTY_HINT = re.compile(r"总说明|目录|大样|详图|楼梯|坡道|雨蓬|雨棚|节点|门窗表", re.I)


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sheet_labels(payload: dict[str, Any]) -> dict[str, str]:
    """图框 id -> 标题。走 cad_interpret，与算量侧同一套口径。"""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import cad_interpret  # noqa: WPS433（运行期按需导入，避免影响无 vendor 环境）
        return dict(cad_interpret.detect_sheet_labels(payload) or {})
    except Exception:
        return {}


def _sheet_bbox(payload: dict[str, Any], sheet_id: str) -> list[float] | None:
    for sheet in (payload.get("meta") or {}).get("sheets") or []:
        if str(sheet.get("id")) == str(sheet_id):
            bbox = sheet.get("bbox")
            if bbox and len(bbox) == 4:
                return [float(v) for v in bbox]
    return None


def pick_sheets(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """按优先级给出可算量的图框候选。

    排序：梁平法类最先（算梁量只能用它）→ 其他结构图 → 排除总说明/大样/楼梯。
    每个候选都带 bbox，算量侧可直接 `--bbox` 定位，不依赖它自己再猜。
    """
    labels = _sheet_labels(payload)
    out: list[dict[str, Any]] = []
    for sheet_id, title in labels.items():
        bbox = _sheet_bbox(payload, sheet_id)
        if not bbox:
            continue
        title = str(title or "").strip()
        if not title:
            continue
        out.append({
            "sheet": str(sheet_id),
            "title": title,
            "bbox": bbox,
            "is_beam_sheet": bool(BEAM_SHEET_HINT.search(title)),
            "excluded": bool(NON_QTY_HINT.search(title)),
        })
    out.sort(key=lambda r: (not r["is_beam_sheet"], r["excluded"], r["title"]))
    return out


def slab_thickness(payload: dict[str, Any]) -> dict[str, Any]:
    """板厚候选。取图上出现最多的标注值作默认，同时保留全部档位。

    只给众数是因为算量入口一次只吃一个值；真实图里板厚分档，众数只是一种
    近似，所以把完整分布一并给出，报告里要写清这是近似而非实测分档。
    """
    raw = payload.get("slab_thk") or {}
    pairs: list[tuple[float, int]] = []
    if isinstance(raw, dict):
        for k, v in raw.items():
            try:
                pairs.append((float(k), int(v)))
            except (TypeError, ValueError):
                continue
    elif isinstance(raw, list):
        for item in raw:
            try:
                pairs.append((float(item.get("mm")), int(item.get("count") or 1)))
            except (TypeError, ValueError, AttributeError):
                continue
    if not pairs:
        return {"default_mm": None, "distribution": {}, "distinct": 0,
                "note": "图上没有板厚标注"}
    counter = Counter()
    for mm, n in pairs:
        counter[mm] += n
    top_mm, top_n = counter.most_common(1)[0]
    total = sum(counter.values())
    return {
        "default_mm": int(top_mm),
        "distribution": {str(int(k)): v for k, v in counter.most_common()},
        "distinct": len(counter),
        "note": (f"取图上出现最多的 {int(top_mm)}mm（{top_n}/{total} 处）作默认；"
                 f"实际有 {len(counter)} 种板厚，分档未闭合"),
    }


def concrete_grades(payload: dict[str, Any]) -> dict[str, int]:
    raw = payload.get("concrete") or {}
    if isinstance(raw, dict):
        return {str(k): int(v) for k, v in raw.items()}
    return {}


def prepare(sources: list[tuple[Path, dict[str, Any]]]) -> dict[str, Any]:
    drawings: list[dict[str, Any]] = []
    for path, payload in sources:
        sheets = pick_sheets(payload)
        beam = [s for s in sheets if s["is_beam_sheet"] and not s["excluded"]]
        usable = [s for s in sheets if not s["excluded"]]
        drawings.append({
            "file": path.name,
            "sheets": sheets,
            # 只推荐梁图框：板配筋图、基础图里没有梁标注，拿去算梁量必然
            # 报「未解析到梁标注」。宁可标 not_ready，也不要推荐一个必然失败的图框。
            "recommended": (beam or [None])[0],
            "other_usable": [s["title"] for s in usable if not s["is_beam_sheet"]][:8],
            "sheet_count": len(sheets),
            "beam_sheet_count": len(beam),
            "slab": slab_thickness(payload),
            "concrete_grades": concrete_grades(payload),
            # 有可用图框但都不是梁图框：可出板量，不出梁量
            "ready": bool(beam),
            "ready_for": "beam+slab" if beam else ("slab-only" if usable else "none"),
        })
    ready = [d for d in drawings if d["ready"]]
    return {
        "schema": SCHEMA,
        "clearance": CLEARANCE,
        "contract": {"final_quantity": False},
        "drawings": drawings,
        "summary": {
            "drawings": len(drawings),
            "ready": len(ready),
            "not_ready": len(drawings) - len(ready),
            "with_beam_sheet": sum(1 for d in drawings if d["beam_sheet_count"]),
            "slab_only": sum(1 for d in drawings if d["ready_for"] == "slab-only"),
        },
        "note": ("--floor-label 的真实语义是图框标题（算量侧按标题精确比对），"
                 "不是楼层号；传楼层号会得到 0 条梁、量恒为 0。这里的 recommended.title "
                 "就是该传给算量技能的标签，bbox 可作兜底定位。只推荐梁图框，"
                 "因为梁量必须从有梁标注的图框取；板配筋图与基础图不算在内。"),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="算量前置：图框标题 / 板厚 / 标号")
    ap.add_argument("--inputs", nargs="+", required=True, help="detail JSON 路径")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    sources: list[tuple[Path, dict[str, Any]]] = []
    for raw in args.inputs:
        p = Path(raw)
        try:
            sources.append((p, _load(p)))
        except Exception as exc:
            print(f"跳过 {p.name}：{exc}", file=sys.stderr)
    payload = prepare(sources)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    s = payload["summary"]
    print(f"可用图框 {s['ready']}/{s['drawings']} 张（其中梁图框 "
          f"{s['with_beam_sheet']} 张）→ {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
