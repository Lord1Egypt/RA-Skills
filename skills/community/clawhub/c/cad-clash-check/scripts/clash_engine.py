#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cross/engine.py —— 跨专业校对公共引擎 P0（统一对象模型 + 两两比较骨架）。

方案定位（§4.2，采纳 Codex 的公共引擎架构）：不按专业对写 N 套，
一次建好统一对象模型与比较骨架，全部专业对复用。

诚实边界（必须随结果告知）：这是 2D 图纸的**一致性倾向提示 / 校对辅助**，
不是 BIM 碰撞检测（无 3D 模型）；输出「疑似冲突清单 + 待人工复核的坐标证据」，
不是盖章结论。final_quantity=false。

统一 key = 项目 + 楼层 + 轴网位置 + 构件名。
两两比较三视图：
  占位（place）   一方有该 key、另一方没有 → warn（可能未建/未识别）
  属性（attr）    同 key 的共享属性不一致（如 混凝土标号/洞口宽）→ conflict
  关联（relate）  一方声明引用另一方的构件（如 门窗洞→结构洞口），引用落空 → warn

每条结果带 severity(pass/warn/conflict) + evidence（双方来源与坐标）+
residualReason（无法判定时的原因）。坐标缺失时只做 key 级比较并如实标注
no_evidence（降级：place/attr 仍可用，坐标级核对跳过）。

用法
    engine = CrossEngine()
    result = engine.compare(members_a, members_b, relations=rels)
    result.to_json() / to_md()
"""
from __future__ import annotations

import re

GRID_NORM = str.maketrans({" ": "", "（": "(", "）": ")", "×": "x", "Ｘ": "x",
                           "／": "/"})
AX_NUM_RE = re.compile(r"^\d+$")


class Member:
    """统一构件对象：跨专业比较的最小单元。"""

    __slots__ = ("project", "floor", "grid", "name", "category",
                 "attrs", "source", "bbox")

    def __init__(self, project: str, floor: str, grid: str, name: str,
                 category: str, attrs: dict | None = None,
                 source: str = "", bbox: list | None = None):
        self.project = str(project or "")
        self.floor = str(floor or "")
        self.grid = norm_grid(grid)
        self.name = str(name or "")
        self.category = str(category or "")
        self.attrs = dict(attrs or {})
        self.source = str(source or "")
        self.bbox = list(bbox) if bbox else None

    @property
    def key(self) -> tuple:
        return (self.project, self.floor, self.grid, self.name)

    def has_position(self) -> bool:
        return self.bbox is not None and len(self.bbox) == 4


def norm_grid(grid: str) -> str:
    """轴网位置归一：轴号大小写/分隔符统一，如 "A-C/1-3" 与 "a~c/1~3" 同键。"""
    s = str(grid or "").strip().translate(GRID_NORM).upper()
    s = s.replace("~", "-").replace("～", "-").replace("/", "-")
    return s or "?"


class CompareResult:
    """一次两两比较的结果集。"""

    def __init__(self, side_a: str, side_b: str):
        self.side_a = side_a
        self.side_b = side_b
        self.items: list[dict] = []

    def add(self, view: str, severity: str, key, message: str,
            evidence: dict | None = None, residual: str = "") -> None:
        self.items.append({"view": view, "severity": severity, "key": " / ".join(key),
                           "message": message, "evidence": evidence or {},
                           "residualReason": residual})

    def counts(self) -> dict:
        c = {"pass": 0, "warn": 0, "conflict": 0}
        for it in self.items:
            c[it["severity"]] += 1
        return c

    def to_json(self) -> dict:
        return {"schema": "cad-cross-compare/v1", "final_quantity": False,
                "side_a": self.side_a, "side_b": self.side_b,
                "counts": self.counts(), "items": self.items,
                "boundary": "2D 图纸一致性倾向提示，非 BIM 碰撞检测；"
                            "输出疑似冲突清单供人工复核，不是盖章结论"}

    def to_md(self) -> str:
        c = self.counts()
        lines = [f"# 跨专业校对：{self.side_a} × {self.side_b}",
                 "",
                 "> 2D 一致性倾向提示（非 BIM 碰撞检测）；conflict=属性冲突，"
                 "warn=占位/关联待人工复核。final_quantity=false。",
                 "",
                 f"- pass **{c['pass']}** / warn **{c['warn']}** / conflict **{c['conflict']}**",
                 ""]
        for it in sorted(self.items, key=lambda x: {"conflict": 0, "warn": 1,
                                                    "pass": 2}[x["severity"]]):
            if it["severity"] == "pass":
                continue
            ev = it["evidence"]
            ev_txt = f"（a:{ev.get('a', '-')} / b:{ev.get('b', '-')}）" if ev else ""
            lines.append(f"- **{it['severity']}** [{it['view']}] {it['key']}：{it['message']}{ev_txt}"
                         + (f" 残余：{it['residualReason']}" if it["residualReason"] else ""))
        return "\n".join(lines) + "\n"


def _shared_attr_conflicts(a: Member, b: Member) -> list[tuple[str, object, object]]:
    """两侧都有且值不同的属性。"""
    out = []
    for k, v in a.attrs.items():
        if k in b.attrs and b.attrs[k] != v:
            out.append((k, v, b.attrs[k]))
    return out


def _nearby(a: Member, b: Member, tol: float) -> bool | None:
    """bbox 中心距离是否 <= tol（单位与图一致）。无坐标返回 None。"""
    if not (a.has_position() and b.has_position()):
        return None
    ax = (a.bbox[0] + a.bbox[2]) / 2
    ay = (a.bbox[1] + a.bbox[3]) / 2
    bx = (b.bbox[0] + b.bbox[2]) / 2
    by = (b.bbox[1] + b.bbox[3]) / 2
    return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5 <= tol


class CrossEngine:
    """公共引擎：build index → 三视图比较。专业对复用同一实现。"""

    PLACE_TOL = 5000.0  # 图形单位（约 5m，可按项目比例覆盖）

    def __init__(self, place_tol: float | None = None):
        self.place_tol = place_tol if place_tol is not None else self.PLACE_TOL

    def compare(self, members_a: list[Member], members_b: list[Member],
                side_a: str = "A", side_b: str = "B",
                relations: list[dict] | None = None) -> CompareResult:
        res = CompareResult(side_a, side_b)
        idx_a = {m.key: m for m in members_a}
        idx_b = {m.key: m for m in members_b}

        # ---- 占位视图：key 集合差
        for k in sorted(set(idx_a) - set(idx_b)):
            res.add("place", "warn", k,
                    f"{side_a} 有、{side_b} 无（未建或未识别）",
                    evidence={"a": idx_a[k].source})
        for k in sorted(set(idx_b) - set(idx_a)):
            res.add("place", "warn", k,
                    f"{side_b} 有、{side_a} 无（未建或未识别）",
                    evidence={"b": idx_b[k].source})

        # ---- 属性视图：同 key 共享属性冲突 + 同名不同位的近似对
        for k in sorted(set(idx_a) & set(idx_b)):
            a, b = idx_a[k], idx_b[k]
            for attr, va, vb in _shared_attr_conflicts(a, b):
                res.add("attr", "conflict", k,
                        f"属性 {attr} 不一致：{va!r} vs {vb!r}",
                        evidence={"a": a.source, "b": b.source})
            near = _nearby(a, b, self.place_tol)
            if near is False:
                res.add("place", "warn", k,
                        f"同名构件位置偏差超过容差 {self.place_tol:.0f}",
                        evidence={"a": a.bbox, "b": b.bbox},
                        residual="同名但位置远——可能是重名构件或定位错误，需人工复核")
            elif near is None:
                res.add("place", "pass", k, "key 匹配（无坐标，跳过位置核对）",
                        residual="no_evidence: 双方无 bbox，坐标级核对降级为 key 级")
            else:
                res.add("place", "pass", k, "key 与位置均匹配")

        # ---- 关联视图：一方引用另一方的构件，引用落空 → warn
        for rel in relations or []:
            src_k = rel.get("from")
            dst_k = rel.get("to")
            if not src_k or not dst_k:
                continue
            src_ok = tuple(src_k) in idx_a or tuple(src_k) in idx_b
            dst_ok = tuple(dst_k) in idx_a or tuple(dst_k) in idx_b
            if src_ok and not dst_ok:
                side = side_a if tuple(dst_k) in {m.key for m in members_a} else side_b
                res.add("relate", "warn", tuple(src_k),
                        f"引用落空：声明的 {dst_k} 在 {side} 侧不存在",
                        evidence={"from": rel.get("from_source", ""),
                                  "to": rel.get("to_source", "")},
                        residual="可能为洞口/预埋漏建，或引用书写不一致")
            elif src_ok and dst_ok:
                res.add("relate", "pass", tuple(src_k), "引用闭合")
        return res
