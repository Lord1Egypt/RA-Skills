#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ct-advisor — 转发前本地守卫编排（改进 A/B/C，2026-09-23）

把三件本地改进在「req.validate() 之后、各外发分支之前」统一编排：
  1. scope_guard  —— 范围路由：识别超范围（医学写作/综述）请求，记 scope_hint（不阻断，后置转介）；
  2. doc_memory   —— 大文档压缩：超长 original_question 压成「指令头 + 相关片段」，省去 32k 重发；
  3. dedup_guard  —— 同 origin 近似去重：串行路径下命中近期重复则本地短路复用旧答案。

硬约束（来自 race 模式纪律）：fire_only / collect 路径**零本地检索**，本模块对这两类模式直接 no-op，
绝不「先本地检索再发 Coze」。去重短路也只在串行（complex/vague）路径启用。

所有守卫异常均被调用方（refine_answer.py）兜底为 skip，本模块内部也尽量防御，绝不阻断主流程。

依赖：stdlib-only（dataclasses）。
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GuardOutcome:
    short_circuit: bool = False          # True → 调用方应直接输出 answer 并退出（去重命中）
    answer: str = ""                     # 短路复用的旧答案
    req: object = None                   # 可能已被原地修改（压缩/标记）的 req
    notes: list = field(default_factory=list)


def apply_guards(req, mode: str) -> GuardOutcome:
    """对 req 施加本地守卫。

    mode ∈ {fire_only, collect, ship, forward, serial}。
    返回 GuardOutcome；req 可能被原地修改（original_question 压缩、scope_hint/doc_context 标记）。
    """
    notes = []
    # race 硬闸门：fire_only/collect 路径不做任何本地检索，直接放行
    if mode in ("fire_only", "collect"):
        return GuardOutcome(req=req, notes=notes)

    q = getattr(req, "original_question", "") or ""

    # 1) 范围路由
    try:
        import scope_guard as _sg
        in_scope, tag, _referral = _sg.assess(q)
        if not in_scope and tag:
            req.scope_hint = tag
            notes.append(f"scope:{tag}")
    except Exception:  # noqa: BLE001
        pass

    # 2) 大文档：① 压缩问题文本（保证老 Coze 兼容）；② 构造结构化文档载荷（新 Coze 自行检索）
    try:
        import doc_memory as _dm
        new_q, doc_id = _dm.compact_large_question(q)
        if doc_id:
            req.original_question = new_q
            notes.append("doc:compacted")
        # 结构化载荷：新 Coze（v1.21+）据此自行分块检索、引用「文档 §N」、跨轮复用 doc_id。
        # 未部署新代码的 Coze 会因 pydantic extra='ignore' 静默忽略该字段，行为退化为①的压缩文本。
        payload, payload_id = _dm.build_doc_payload(q)
        if payload:
            req.doc_context = payload
            notes.append("doc:payload(%s)" % payload_id)
    except Exception:  # noqa: BLE001
        pass

    # 3) 同 origin 去重短路（仅串行路径；fire_only/collect 已在上游 no-op）
    if mode == "serial":
        try:
            import dedup_guard as _dg
            origin = ((getattr(req, "query_meta", None) or {}) or {}).get("query_origin", "") or ""
            is_dup, prev, mins = _dg.check(origin, getattr(req, "original_question", "") or "")
            if is_dup and prev:
                notes.append(f"dedup:hit({mins}m)")
                return GuardOutcome(short_circuit=True, answer=prev, req=req, notes=notes)
        except Exception:  # noqa: BLE001
            pass

    return GuardOutcome(req=req, notes=notes)


def record_answer(query_origin: str, question: str, answer: str) -> None:
    """在云端返回答案后回写去重库，供下次同 origin 近似重复时短路复用。异常静默。"""
    try:
        import dedup_guard as _dg
        _dg.record(query_origin, question, answer)
    except Exception:  # noqa: BLE001
        pass


def apply_scope_referral(final_answer: str, scope_hint: str) -> str:
    """把超范围转介声明前置注入最终答案。异常回退原文。"""
    try:
        import scope_guard as _sg
        return _sg.apply_referral(final_answer, scope_hint)
    except Exception:  # noqa: BLE001
        return final_answer


if __name__ == "__main__":
    # 鸭子类型离线自测（不触碰真实 req / 不联网）
    class FakeReq:
        def __init__(self, q, origin=""):
            self.original_question = q
            self.query_meta = {"query_origin": origin}
            self.scope_hint = ""
            self.doc_context = ""
    r = FakeReq("请帮我起草一份 EEG 神经调控研究报告的大纲", "sha256:u1")
    out = apply_guards(r, "serial")
    print("scope_hint:", r.scope_hint, "| notes:", out.notes)
    big = "请梳理：\n" + ("临床试验背景资料。" * 800)   # >6000 字，触发大文档路径
    r2 = FakeReq(big, "sha256:u2")
    out2 = apply_guards(r2, "serial")
    print("原文 %d 字 → 压缩后 %d 字" % (len(big), len(r2.original_question)),
          "| notes:", out2.notes)
    print("doc_context 前 160 字:", (r2.doc_context or "")[:160])
    # race 模式必须零本地检索（硬闸门）
    r3 = FakeReq(big, "sha256:u3")
    out3 = apply_guards(r3, "fire_only")
    print("fire_only 零副作用:", r3.doc_context == "" and r3.original_question == big,
          "| notes:", out3.notes)
