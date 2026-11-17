#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ct-advisor — 代码全自动编排器（2026-08-15，模式 B + 委托本地大模型）

设计定位（与用户确认）：
  - 🔴 代码是**全自动编排器 / 决策者**：判定难度、前端高置信预判、并行触发
    Coze 与预判的 ct 技能、合并两边结果、**由代码决定「信息是否已足够」**。
  - 本地大模型**不是**编排器；但「任何代码过程中需要调用其他 ct 技能」这一步
    被**委托给本地大模型执行**（通过 <<<CT_TOOL_DELEGATE>>> 标记块）。
  - 本地大模型只做两件事（只决策 + 代码缝合）：
      1) 补全 / 追问执行卡参数（need_params 时向用户追问，不编造）；
      2) 把执行卡交给 `refine_answer.py` 由**代码**执行技能 + 确定性缝合 + 包裹答案。
  - 本地大模型**不**判断「信息是否足够」、**不**重写 Coze 文本。

与既有协议的关系：
  - 信息足够 → 返回**明文答案**（v1.3.20 起内部无编码包裹；标记与 checksum 只在
    `entry._emit_plain` 出口产生一次），本地大模型只做原样透传（pipe）。
  - 仍需 ct 技能 → 输出 <<<CT_TOOL_DELEGATE>>>…<<<CT_TOOL_DELEGATE_END>>> 结构化块，
    本地大模型读取后执行（见下方「委托协议」），最终仍由 --card-inline 走代码缝合。

委托协议（本地大模型收到 <<<CT_TOOL_DELEGATE>>> 后的动作）：
  1. 读取块内 need_tool / params / draft_answer / original_question；
  2. 若 params 完整 → 直接 `python scripts/refine_answer.py --card-inline '<执行卡 JSON>'`；
  3. 若缺失 → 向用户追问补齐（不编造），再执行上述 --card-inline；
  --card-inline 会由代码执行技能 + 缝合 Coze 草稿（大模型不重写）。

用法：
  python scripts/orchestrate.py --payload-inline '<3变量 JSON>'
        → 输出明文答案（信息足够，pipe 透传；标记/checksum 由 entry.py 出口统一添加）
          或 <<<CT_TOOL_DELEGATE>>>…<<<CT_TOOL_DELEGATE_END>>>（委托大模型调 ct 技能）
  python scripts/orchestrate.py --payload-inline '<JSON>' --no-prefetch
        → 跳过前端预判预取，仅走 Coze；Coze 判定需工具时仍委托大模型
  python scripts/orchestrate.py --self-test
        → 跑内置编排决策自测（mock Coze / 预判，无网络 / 无本地技能调用）
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import threading
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
for _p in (str(SCRIPT_DIR), str(SKILL_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# ── 延迟导入策略（2026-09-25 性能修复）─────────────────────────────────────
# refine_answer(57KB) / handle_need_tool(43KB) / adapters.refiner(44KB) 在导入期合计约 12s，
# 且这些符号绝大多数只在 build_output（Coze 返回之后）或子线程里才用到。
# 改为「用前再 import」：把它们的加载塞进 Coze 网络等待窗口内并发完成，不再串行堆积在
# 发请求之前（此前每次冷启动白白烧 ~13s）。ANSWER_START/END 作为定界常量在此本地重定义
# （与 refine_answer 完全同值），避免仅为两个常量而整体导入 57KB 模块。
# 2026-10-22（v1.3.20）：答案在**进程间也是明文**。base64 当年的唯一价值是绕过
# 控制台代码页（cp936 会把 UTF-8 字节误解码）；那个问题现在由出口的
# `stdout.buffer.write(utf-8 字节)` + 答案文件承担，内部再加一层编码只会多出
# 「谁负责解码」的分支。现在标记与 checksum **只在 entry._emit_plain 产生一次**，
# 本模块只做行尾归一。
ANSWER_START = "<<<CT_ANSWER_START>>>"
ANSWER_END = "<<<CT_ANSWER_END>>>"

# 编码统一（2026-10-22 修订职责边界）：本条只服务「orchestrate.py 被**直接**当 CLI
# 跑」的场景（调试 / --self-test / --payload-inline 的 stdout 提示）。**答案通道**
# 不依赖它——`entry._emit_plain` 用 `stdout.buffer.write(utf-8 字节)` 直接落字节，
# 既不看 `sys.stdout.encoding`，也不受这里的 reconfigure 影响。
for _s in (sys.stdin, sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace", newline="\n")  # type: ignore[attr-defined]
    except Exception:
        pass

# 委托标记（本编排器新增；与 ANSWER_START/END 同家族，供本地大模型识别）
TOOL_DELEGATE_START = "<<<CT_TOOL_DELEGATE>>>"
TOOL_DELEGATE_END = "<<<CT_TOOL_DELEGATE_END>>>"


# ---------------------------------------------------------------------------
# 输出构造（确定性，无 LLM）
# ---------------------------------------------------------------------------

def _finalize(text: str) -> str:
    """编排结果的行尾归一——内部唯一形态是**明文**，无编码、无解包。

    v1.3.20 起：标记与 checksum 只在 `entry._emit_plain` 产生一次，本函数不再
    包裹任何东西（历史 `_wrap` 的 base64 信封已删除，见 CHANGELOG）。
    """
    return (text or "").replace("\r\n", "\n")


def _enrich_coze_params(orig_q: str, coze_tool: str | None, coze_params: dict) -> dict:
    """用本地 route_tool 预判补全 Coze 判定工具的真实入参（Coze 仅判类别、不抽真实参数）。

    与 refine_answer.py --ship 同策略：route_tool 抽到的真实参数（cond/drug/topic/test/p1/p2）
    覆盖 Coze 默认值（max/top/alpha/power），使「代码走本地全流程」在 need_tool 场景成立，
    避免「Coze 需不同工具」分支(2c)委托时只带 Coze 默认值、再弹一轮 need_params。
    """
    if not coze_tool:
        return dict(coze_params)
    from route_tool import predict as predict_tool  # 函数级 from-import 仅绑定本函数局部，兄弟函数需各自导入
    pred = predict_tool(orig_q)
    if pred.get("need_tool") != coze_tool:
        return dict(coze_params)
    out = dict(coze_params)
    for k, v in (pred.get("params") or {}).items():
        if v not in (None, ""):
            out.setdefault(k, v)
    return out


def _render_delegate(orig_q: str, tool: str, params: dict,
                     draft_answer: str, missing: list | None = None,
                     prefetch_satisfied: dict | None = None,
                     note: str | None = None,
                     need_tools: list | None = None,
                     extra: dict | None = None) -> str:
    """构造 <<<CT_TOOL_DELEGATE>>> 结构化块（供本地大模型执行 ct 技能）。

    大模型读取后：补全/追问参数 → 调 `refine_answer.py --card-inline '<执行卡>'`
    由代码执行技能 + 缝合 + 包裹。大模型不重写 Coze 文本。

    extra（2026-09-10）：附加字段并入块顶（如 install_required 的 github / install_hint），
    让大模型在征询安装时无需另查映射表。
    """
    if missing is None:
        missing = []
    if prefetch_satisfied is None:
        prefetch_satisfied = {}
    block = {
        "need_tool": tool,
        # 2026-08-23：透传全部命中，使 handle_need_tool 在委派路径也能生成
        # 「其余数据源待准备」提示（此前只有直执行路径有 need_tools）。
        "need_tools": need_tools or ([tool] if tool else []),
        "params": params or {},
        "draft_answer": draft_answer or "",
        "original_question": orig_q or "",
        "missing_params": missing,
        "prefetch_satisfied": prefetch_satisfied,
        "note": note or (
            "代码预判 / Coze 判定需调用 ct 系列技能补充信息，委托本地大模型执行。"
            "请：①确认或补全执行卡参数（缺失则向用户追问、不编造）；"
            "②将执行卡 JSON 传给 `python scripts/refine_answer.py --card-inline '<JSON>'`，"
            "由代码执行技能并确定性缝合 + 包裹最终答案（本地大模型只做透传，不重写 Coze 文本）。"
        ),
    }
    if extra:
        for k, v in extra.items():
            block.setdefault(k, v)
    return (f"{TOOL_DELEGATE_START}\n"
            f"{json.dumps(block, ensure_ascii=False, indent=2)}\n"
            f"{TOOL_DELEGATE_END}\n")


def _unreleased_payload(tool: str) -> dict:
    """构造 B 档 / 未登记技能的 unreleased_b 产物（与 handle_need_tool 同语义，本地无 subprocess）。"""
    from handle_need_tool import _load_mapping, _resolve_tier  # 函数级 from-import 仅绑定本函数局部
    tier_info = _resolve_tier(_load_mapping(), tool)
    if tier_info["registered"]:
        reason = f"{tool} 属 B 档技能（输入含涉密信息：受试者数据 / 方案 / CRF）"
    else:
        reason = f"{tool} 未在 ct-advisor 的技能登记表中（按 B 档保守处理）"
    return {
        "tool": tool,
        "status": "unreleased_b",
        "result": {
            "message": reason + (
                "。该技能不经公共市场分发；当前**本机未注册**，客户端尚无法直接调用。"
                "如需其能力，请在该技能自己的运行环境中准备；"
                "切勿把方案 / 受试者数据发往公共检索端点（F33 出域红线）。"),
            "tier": "B",
            "registered": tier_info["registered"],
            "purpose": tier_info["purpose"],
            "purpose_note": (
                "该技能的处理能力（如方案深度审阅 / 统计审阅 / 数据质控）需在其本地运行环境中"
                "用真实数据执行；ct-advisor 不冒充其能力。"
            ),
            "hint": "请稍后重试，或检查网络连接。深度分析未实际执行。",
        },
        "elapsed_sec": 0,
    }


def _unpublished_payload(tool: str) -> dict:
    """构造「未在 SkillHub 上架且本机未注册」的 unpublished_a 产物（与 handle_need_tool 同语义）。

    2026-11-09：本机已注册的技能由 build_output 改走 handoff，不会落到这里。
    """
    from handle_need_tool import _load_mapping, _resolve_tier  # 函数级 from-import 仅绑定本函数局部
    tier_info = _resolve_tier(_load_mapping(), tool)
    return {
        "tool": tool,
        "status": "unpublished_a",
        "result": {
            "message": (f"{tool} 属 A 档技能（输入非涉密），**未在 SkillHub 上架**，"
                        f"且当前**本机未注册**，客户端尚无法直接调用。"),
            "tier": "A",
            "published": False,
            "registered": tier_info["registered"],
            "purpose": tier_info["purpose"],
            "hint": "不向用户提供安装地址（避免给出装完仍不可用的空仓库 / 未上架技能）；"
                    "以自身能力 + 已装兄弟技能尽量完成分析，并标注「数据未取数」。",
            "next_step": (f"若该技能已在你的客户端中可用，可直接调用 @skill:{tool}；"
                          "否则可先分别调用 ct-registry / ct-safety / ct-literature 取数，"
                          "再由 ct-advisor 就地缝合。"),
        },
        "elapsed_sec": 0,
    }


# ---------------------------------------------------------------------------
# 并行触发：Coze + 前端预判 ct 技能
# ---------------------------------------------------------------------------

def _fire_coze(req: RefineRequest, config_path: str) -> RefineResult:
    """线程内调用 Coze 全量直发。

    依赖缺失（MissingDependencyError）**绝不静默回退**：把安装提示挂到
    RefineResult.dependency_error 上交给 build_output 渲染，否则用户会误以为
    拿到的是 Coze 精校答案，实则连请求都没发出去。
    （2026-10-15 注：传输层已改 stdlib urllib，requests 缺失不再触发本分支，
     此处作为防御性死代码保留。）

    其余异常分两类透出，均**不伪装成「返回为空，请稍后重试」**：
      - 网络/超时类：refine_forward 内部已分类为 connection_error + ERR 信号；
      - 调用前异常（配置损坏 / token 解码失败 / 代码缺陷）：逃逸到本层，
        归类 ORCH_FAIL 并挂 internal_error 人读提示。
    """
    # 延迟导入重模块（性能修复）：仅在线程内使用，避免主流程导入期加载
    from adapters import build_refiner, RefineResult, MissingDependencyError, emit_err_signal
    from adapters.refiner import _internal_error_msg
    from refine_answer import _check_outbound_authorization, _get_endpoint_from_config
    try:
        return build_refiner(config_path=config_path).refine_forward(req)
    except MissingDependencyError as e:
        # 依赖缺失：挂上安装提示，交由 build_output 透传给用户（不伪装成空答案）
        sys.stderr.write(f"[ct-advisor][DEP-MISS] {e}\n")
        res = RefineResult(final_answer=req.draft_answer, need_tool=None)
        res.dependency_error = str(e)  # 动态属性；build_output 用 getattr 读取
        return res
    except Exception as e:  # noqa: BLE001
        # 调用前/配置类异常：ORCH_FAIL 机器信号 + internal_error 人读提示。
        # （网络/超时类异常已在 refine_forward 内部分类，不会到达这里。）
        emit_err_signal("ORCH_FAIL", detail="%s: %s" % (type(e).__name__, e))
        sys.stderr.write(f"[ct-advisor][COZE-FALLBACK] {type(e).__name__}: {e}\n")
        res = RefineResult(final_answer=req.draft_answer, need_tool=None)
        res.internal_error = _internal_error_msg(e)  # 动态属性；build_output 用 getattr 读取
        return res


def _fire_prefetch(card: dict) -> dict:
    """高置信预取：默认产出客户端 handoff 卡片；显式开启 brief 时优先走速览直连。

    2026-11-09 架构重评：客户端已可直接调用兄弟技能，cloud brief 降为 opt-in
    （CT_ADVISOR_CLOUD_BRIEF=1，默认关闭），handoff 成为默认主路径——把执行权
    交回技能本体，用户拿到的是完整交付物而不是纯文本速览。
    共享凭据仍只在本地技能，Coze 云端不发起需凭据的外部调用；任何失败回落
    本地执行卡（ct-base §20.19.7 红线 2）。
    """
    try:
        from cloud_brief import try_cloud_brief
        text = try_cloud_brief(card)
        if text:
            return {
                "tool": card.get("need_tool"), "status": "ok", "result": text,
                "draft_answer": card.get("draft_answer") or "",
                "deferred_tools": [], "deferred_note": "",
                "elapsed_sec": 0, "mode": "coze_brief",
            }
    except Exception as e:  # noqa: BLE001 - 预取失败不得卡死主链路
        sys.stderr.write("[ct-advisor] brief 预取异常，回落本地执行卡: %s\n"
                         % type(e).__name__)
    from refine_answer import _run_handle_need_tool
    return _run_handle_need_tool(card)


# ---------------------------------------------------------------------------
# 核心决策：合并 + 判定信息是否足够（纯代码，无 LLM）
# ---------------------------------------------------------------------------

def build_output(orig_q: str, coze_result: RefineResult,
                 prefetch_out: dict | None, prefetch_tool: str | None,
                 prefetch_params: dict | None,
                 need_tools: list | None = None,
                 suggest_tools: list | None = None) -> str:
    """返回最终应输出字符串（包裹答案 或 委托块）。

    decision（代码决定，非 LLM）：
      - 预判已执行且 ok，且 Coze 未要求其他工具 → 信息足够 → 包裹答案
        （多源问题在答案尾部追加「⚠️ 多源提示」指明其余工具，2026-08-21）。
      - 预判已执行且 ok，但 Coze 要求**不同**工具 → 仍委托（Coze 工具），
        预判结果作为补充并入 draft_answer。
      - 预判 need_params / error，且存在待调工具 → 委托（补全参数或重试）。
      - 无预判但 Coze 要求工具 → 委托（entry.py STEP 4 由代码执行，产出 handoff 卡片）。
      - 预判 status=handoff（默认主路径）→ 代码缝合 @skill 卡片并包裹，绝不委托给 LLM。
      - Coze 未要求工具且预判无有效补充 → Coze 答案足够 → 包裹。
    """
    # ── 依赖缺失快速通道（2026-10-15 修复）：绝不静默失败 ──
    # _fire_coze 在 requests 缺失时把安装提示挂在 dependency_error 上；此处直接
    # 渲染为用户可见的「请先安装」提示，避免冒充 Coze 空答案。
    dep_err = getattr(coze_result, "dependency_error", None)
    if dep_err:
        return _finalize(
            "⚠️ 答案精校服务依赖缺失，无法连接 Coze。\n\n"
            f"{dep_err}\n\n"
            "安装完成前本技能无法提供精校答案（不会返回任何未经精校的占位内容）。"
        )
    # ── 出站连接/超时失败快速通道（2026-10-15 修复）：绝不静默为「返回为空」 ──
    # 与 dependency_error 同理：连接失败必须明确告知用户检查网络/代理，
    # 而非误导为「Coze 返回空、请稍后重试」。仅当 Coze 真正返回空答案时才走原提示。
    conn_err = getattr(coze_result, "connection_error", None)
    if conn_err:
        return _finalize(
            "精校服务连接失败，无法获取 Coze 答案。\n\n"
            f"{conn_err}\n\n"
            "完成上述排查并恢复网络/代理后，重新运行本技能即可（连接恢复前本技能不会返回任何未经精校的占位内容）。"
        )
    # ── 技能内部错误快速通道（2026-10-15）：配置/代码类失败，不伪装成「返回为空」 ──
    internal_err = getattr(coze_result, "internal_error", None)
    if internal_err:
        return _finalize(internal_err)
    # coze_result 为 None（线程异常崩溃兜底）：降级为空结果，避免 AttributeError 连环崩溃
    if coze_result is None:
        coze_result = _mk_coze("", None, {})

    # 延迟导入重模块（性能修复 + 自测路径兼容）：run_orchestrate 已在 Coze 等待窗口预热
    # sys.modules，此处为缓存命中；run_self_test 直调本函数时则在此首次加载。
    # 注意：函数级 from-import 仅绑定本函数局部，兄弟函数（_enrich_coze_params /
    # _render_skill_text 等）已在各自内部就近导入，避免可见性陷阱。
    from refine_answer import (_merge_answer, _render_skill_result, _detect_lang)
    from handle_need_tool import _load_mapping, _resolve_tier, _client_callable
    from route_tool import suggest_footer
    coze_answer = coze_result.final_answer or ""
    coze_tool = coze_result.need_tool
    # 2026-11-09 主流程修复：混合技能列表有两个来源 —— 本地预判 need_tools 与
    # Coze 侧 RefineResult.need_tools（云端 tool_router 的多技能命中）。
    # 任一来源单独缺失时另一路仍要能补齐，故在此合并去重后统一向下传递。
    _coze_tools = list(getattr(coze_result, "need_tools", None) or [])
    if _coze_tools:
        need_tools = list(dict.fromkeys(list(need_tools or []) + _coze_tools))
    # P2 修复（2026-08-15）：对 Coze 判定工具做本地 route_tool 参数富集，
    # 避免「Coze 需不同工具」分支(2c)委托时只带 Coze 默认值、再弹一轮 need_params。
    coze_params = _enrich_coze_params(orig_q, coze_tool, coze_result.params or {})

    # 2026-09-10（第十四轮，用户要求）：**先自身作答、末尾再建议**兄弟技能。
    # 未自动调用任何兄弟技能、但问题与某技能沾边（弱命中 / 咨询意图）时，
    # 在最终答案**末尾**追加一行软建议；不改写答案本身、不阻断取数决策。
    sugg = suggest_footer(suggest_tools or [], lang=_detect_lang(orig_q))

    def _final_out(text: str) -> str:
        return _finalize(text + sugg)

    # ---- 有预判执行结果 ----
    if prefetch_out is not None:
        status = prefetch_out.get("status")
        tool = prefetch_out.get("tool") or prefetch_tool
        if status == "ok":
            if coze_tool is None or coze_tool == tool:
                # 信息足够：Coze 答案 + 预判技能结果（多源问题附提示其余工具）
                lang = _detect_lang(orig_q)  # 2026-08-21：缝合文案/标签随提问语言
                merged = _merge_answer(coze_answer, prefetch_out, lang=lang)
                # 2026-11-09：_merge_answer 已把 deferred_tools 渲染成
                # 「其余可直接调用的技能」小节时，不再叠加 _multi_tool_hint，
                # 否则回滚路径（status=ok）会把同一批技能列两遍。
                hint = "" if (prefetch_out.get("deferred_tools") or []) else \
                    _multi_tool_hint(need_tools or [], tool, lang=lang)
                return _final_out(merged + hint)
            # Coze 要求不同工具：预判结果并入草稿，委托 Coze 工具
            base = _merge_answer(coze_answer, prefetch_out) if coze_answer.strip() else \
                f"## 补充信息（来源：{tool}）\n\n" + _render_skill_text(prefetch_out)
            return _render_delegate(
                orig_q, coze_tool, coze_params, base,
                prefetch_satisfied={tool: prefetch_out.get("result")},
                note="预判技能已执行；Coze 另需补充「%s」信息，委托本地大模型执行该技能。" % coze_tool,
                need_tools=need_tools,
            )
        if status == "need_params":
            # 预判参数不完整 → 委托大模型追问后执行
            missing = (prefetch_out.get("result") or {}).get("missing", [])
            return _render_delegate(
                orig_q, tool, prefetch_params or {}, coze_answer, missing=missing,
                note="预判技能参数不完整（%s），委托本地大模型向用户追问后执行。" % "; ".join(missing),
                need_tools=need_tools,
            )
        # ---- 2026-09-10 A/B 档门控（四新状态，均非「执行失败」，不得落到 error 兜底）----
        if status in ("unreleased_b", "local_fallback", "unpublished_a",
                      "handoff", "referral"):
            # 本机不可调用 / 用户拒绝安装 / 客户端直调 handoff / referral-only
            # → 一律由代码直接缝合包裹（无需 agent 介入、无需征询同意）。
            # 🔴 handoff 绝不能落到 _render_delegate：那会要求本地 LLM 去执行技能，
            #    违反 SKILL.md HARD GATE。卡片由代码产出、经 entry.py 单一出口输出。
            lang = _detect_lang(orig_q)
            # 2026-11-09 兜底：执行卡/上游丢了 need_tools 时，用合并后的列表
            # 现场补齐 deferred，保证混合提问不会只剩主技能一张卡片。
            if status == "handoff":
                from handle_need_tool import ensure_deferred
                prefetch_out = ensure_deferred(
                    prefetch_out,
                    {"need_tool": tool, "need_tools": need_tools,
                     "params": prefetch_params or {}})
            if coze_answer.strip():
                return _final_out(_merge_answer(coze_answer, prefetch_out, lang=lang))
            return _final_out(_render_skill_text(prefetch_out))
        if status == "install_required":
            # 2026-09-10（第十四轮，用户要求）：由「委托补参 / 安装」改为
            # 「**先自身作答，末尾再建议安装**」——不再用安装动作阻断答案。
            # 安全姿态不变（只建议、不执行：安装会写入本地技能目录、可能触发本机
            # 安全提示；用户明确授权后才代办）：复用 refine_answer._merge_answer 的
            # install 渲染（答案在前、安装建议在后），再叠加通用软建议。
            # 用户授权 → 在卡片加 "install_consent": "approved" 重跑；拒绝 → 加
            # "install_consent": "declined" 重跑，由代码产出「未取数」兜底答案。
            lang = _detect_lang(orig_q)
            return _final_out(_merge_answer(coze_answer, prefetch_out, lang=lang))
        # error：预判执行失败
        if coze_tool:
            return _render_delegate(
                orig_q, coze_tool, coze_params, coze_answer,
                note="预判技能执行出错，Coze 仍判定需补充「%s」，委托本地大模型重新执行。" % coze_tool,
                need_tools=need_tools,
            )
        # 预判失败且无 Coze 工具 → 仅 Coze 答案（若有）或兜底警告
        if coze_answer.strip():
            return _final_out(coze_answer)
        return _final_out("⚠️ Coze 服务暂时不可用且无法获取技能补充数据，请稍后重试。")

    # ---- 无预判 ----
    if coze_tool:
        # 本机确实未注册时：B 档 / 未登记 → 说明「本机未注册」+ 自身能力作答，
        # 免去一次无谓的委托往返。A 档未在 SkillHub 上架且本机也没有同理短路。
        # 2026-11-09：已在本机注册的技能不再短路，改走委托 → 代码产出 handoff。
        tier_info = _resolve_tier(_load_mapping(), coze_tool)
        # 2026-11-09：B 档 / 未上架 A 档只要已在本机注册，客户端就能直接调用，
        # 不再短路成「不对外发布」文案，改为委托 → entry.py STEP 4 代码产出 handoff 卡片。
        if (tier_info["tier"] != "A" or not tier_info["published"]) \
                and not _client_callable(coze_tool):
            lang = _detect_lang(orig_q)
            payload = (_unreleased_payload(coze_tool) if tier_info["tier"] != "A"
                       else _unpublished_payload(coze_tool))
            if coze_answer.strip():
                return _final_out(_merge_answer(coze_answer, payload, lang=lang))
            return _final_out(_render_skill_text(payload))
        return _render_delegate(orig_q, coze_tool, coze_params, coze_answer,
                                need_tools=need_tools)
    if coze_answer.strip():
        return _final_out(coze_answer)
    return _final_out("⚠️ Coze 返回为空，请稍后重试。")


def _render_skill_text(tool_out: dict) -> str:
    """把技能主产物渲染为可读文本（与 refine_answer._render_skill_result 同逻辑）。"""
    from refine_answer import _render_skill_result  # 函数级 from-import 仅绑定本函数局部，必须就近导入
    return _render_skill_result(tool_out.get("result"))


# 工具用途说明（多源提示用，2026-08-21）
_TOOL_DESC = {
    "ct-registry": "试验注册库检索（试验格局 / 分期 / 申办方 / 时间线）",
    "ct-safety": "FAERS 药物警戒信号（PRR / ROR / EBGM + 95%CI）",
    "ct-literature": "学术文献检索（含临床指南 / 病例报告 / 综述 / 证据摘要）",
    "ct-samplesize": "样本量 / 检验效能计算",
}


def _multi_tool_hint(need_tools: list, executed_tool: str, lang: str = "zh-CN") -> str:
    """多源问题提示：已缝合主源后，明确指出其余数据源并建议分别调用。

    2026-08-21（用户要求）：架构单工具时先缝合一个源即可，但需要多工具时
    **必须直接指出**，提示用户分别先调用这些工具获取信息，不掩盖"其余源
    尚未用真实数据缝合"这一事实（此前由 Coze 知识叙述冒充，无来源标签）。
    提示文案随提问语言（lang）切换；工具名保持 id 原文。

    2026-08-23（四技能联调）：文案升级为**可执行**——除工具名/用途外，明确列出
    该技能需要用户先准备的参数（取自 tool_mapping.json 的 prep_hint /
    required_params，与执行器 _build_deferred 共用同一数据源，避免两套文案漂移）。
    """
    others = [t for t in (need_tools or []) if t != executed_tool]
    if not others:
        return ""
    try:
        from handle_need_tool import _load_mapping  # 复用映射表，单一数据源
        skills_cfg = _load_mapping().get("skills", {})
    except Exception:  # noqa: BLE001
        skills_cfg = {}
    lines = []
    for t in others:
        desc = _TOOL_DESC.get(t, t)
        cfg = skills_cfg.get(t, {})
        prep = cfg.get("prep_hint", "")
        req = "/".join(cfg.get("required_params", []))
        if lang == "zh-CN":
            # prep_hint 自带「XX：需确认…」句式，不叠加「需先准备」前缀（避免双重冗余）
            extra = prep or (f"需确认必填参数 {req}" if req else "需补充必填参数")
            # 2026-11-09：客户端已可直接调用，不再说「确认后我再调用」。
            lines.append(f"- `@skill:{t}`（{desc}）：{extra}。客户端可直接调用。")
        else:
            # 英文语境不塞中文 prep_hint，改用参数名（跨语言稳定）
            extra = f"required params: {req}" if req else "required params pending"
            lines.append(f"- `@skill:{t}` ({desc}): {extra}. Invoke directly from the client.")
    if lang == "zh-CN":
        return ("\n\n---\n\n### ⚠️ 多源提示：本问题还涉及以下数据源\n"
                "主判技能见上方 `@skill` 卡片；其余源也可在客户端分别直接调用：\n%s"
                % "\n".join(lines))
    return ("\n\n---\n\n### ⚠️ Multi-source note: this question also involves the following data sources\n"
            "The primary skill is in the `@skill` card above; the remaining sources can also be "
            "invoked directly from the client:\n%s" % "\n".join(lines))


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def _build_request(raw: str) -> RefineRequest:
    from adapters import RefineRequest  # 函数级 from-import 仅绑定本函数局部，就近导入确保可见
    obj = json.loads(raw)
    # suggested_task → query_meta.task_category：把 entry.py 推断的任务类别（pairwise_meta / samplesize 等）
    # 透传到 Coze 端，辅助 Coze 标注任务类型（此前该字段被静默丢弃）。
    _qm = obj.get("query_meta", "") if isinstance(obj, dict) else ""
    if isinstance(_qm, dict):
        _st = (obj or {}).get("suggested_task")
        if _st and isinstance(_st, str) and _st.strip():
            _qm.setdefault("task_category", _st.strip())
    # 2026-10-30 修复（上下文交互缺陷 7）：此前 conversation_history **原样透传**，
    # 任何非契约形态（messages 形态 {role,content} 等）都会直达 Coze →
    # 后端 _history_fp 取空 + "最近5轮"截断按条击穿 → 上下文事实为空。
    # 现按契约（question/answer_summary、升序、每轮 1 条、摘要 ≤200 字、轮数有界）归一后再传。
    try:
        import history_norm as _hn
        _conversation_history = _hn.normalize_history(
            (obj or {}).get("conversation_history"))
    except Exception:  # noqa: BLE001  归一化失败不阻断主流程 → 退回空历史
        _conversation_history = []
    req = RefineRequest(
        query_meta=_qm,
        original_question=str((obj or {}).get("original_question", "")),
        draft_answer=str((obj or {}).get("draft_answer", "")),
        doc_context=str((obj or {}).get("doc_context", "") or ""),
        scope_hint=str((obj or {}).get("scope_hint", "") or ""),
        conversation_history=_conversation_history,
        is_followup=bool((obj or {}).get("is_followup", False)),
    )
    return req


def run_orchestrate(raw: str, config_path: str, no_prefetch: bool = False) -> str:
    # 性能修复（L2, 2026-09-25）：在启动 Coze 线程前于主线程预预热全部重模块，使
    # _fire_coze 线程内的延迟导入变为 sys.modules 缓存命中，Coze 网络调用可立即发起，
    # 不再把 ~8s 的重模块导入串行排在 Coze 等待窗口之外（常驻服务 L1 下此处为缓存命中）。
    from route_tool import predict as predict_tool, suggest_footer  # noqa: F401
    from adapters import build_refiner, RefineResult  # noqa: F401
    import refine_answer  # noqa: F401
    import handle_need_tool  # noqa: F401
    req = _build_request(raw)
    req.normalize()

    orig_q = req.original_question or ""

    # 0) 主链路本地答案缓存（2026-10-16 性能修复）
    # 背景：entry.py 主链路（orchestrate → refine_forward → Coze）不经过
    # forward_guards，dedup_guard 的 30 分钟短路在这条链路上从未生效；agent 一旦
    # 重跑 entry.py 就是一次真实 Coze 往返（log.docx 中可见 3 次）。此处按问题指纹
    # 做精确缓存，命中直接复用，0 次 Coze 调用。
    _ck = ""
    try:
        import answer_cache as _ac
        _ck = _ac.key_of(orig_q, req.doc_context or "",
                         str((req.query_meta or {}).get("difficulty", "")))
        _cached = _ac.get(_ck)
        if _cached:
            sys.stderr.write("[ct-advisor] answer-cache hit: replayed local cached "
                             "answer (no new Coze call)\n")
            return _finalize(_cached)
    except Exception:  # noqa: BLE001
        _ck = ""

    # 1) 前端高置信预判（模式 B 预取）—— 仅高置信才触发，漏判由 Coze 兜底
    pred = predict_tool(orig_q) if not no_prefetch else {"need_tool": None, "params": {}}
    prefetch_tool = pred.get("need_tool")
    prefetch_params = pred.get("params") or {}
    # 2026-08-21：多源问题保留全部命中（need_tools），缝合主源后提示其余工具
    need_tools = pred.get("need_tools") or []
    # 2026-11-10 P1-1：本地意图分级信号透传 query_meta，辅助云端 tool_router 兜底
    # （命名空间隔离字段 _local_intent，Coze 未知字段忽略；纯本地增量，不触碰云端包）。
    if isinstance(req.query_meta, dict):
        req.query_meta["_local_intent"] = {
            "confidence": pred.get("confidence"),
            "ambiguity": pred.get("ambiguity"),
            "candidates": pred.get("candidates"),
            "need_tool": prefetch_tool,
            "need_tools": need_tools,
        }
    # 2026-11-09 扩展：多技能时给每个技能分别抽参数。此前只抽主判，
    # 混合问题的副卡片全是「需补齐」；合并后仍由各技能白名单过滤，不会串参。
    if len(need_tools) > 1:
        try:
            from route_tool import extract_params_for_tools
            prefetch_params = dict(prefetch_params)
            for k, v in extract_params_for_tools(need_tools, orig_q).items():
                prefetch_params.setdefault(k, v)
        except Exception:  # noqa: BLE001 - 抽参失败不阻断主流程
            pass

    # 2) 并行触发：Coze（需授权）+ 预判 ct 技能（本地执行，免授权）
    coze_result = [None]
    prefetch_out = [None]
    threads = []

    def _coze_job():
        from adapters import RefineResult
        from refine_answer import _check_outbound_authorization, _get_endpoint_from_config
        _ep = _get_endpoint_from_config(config_path)
        if not _check_outbound_authorization(_ep, config_path):
            # 2026-10-16 修复（主流程偏差）：此前只返回一个空 RefineResult，
            # build_output 会把它渲染成「⚠️ Coze 返回为空，请稍后重试」——
            # 把「未授权出站 / 配置缺失」误报成「云端返回空」，用户按提示反复
            # 重试永远不会成功，也看不到真实原因。改挂 internal_error（配置类
            # 失败通道），让 build_output 渲染准确的人读提示。
            _res = RefineResult(final_answer=req.draft_answer, need_tool=None)
            if not (_ep or "").strip():
                _res.internal_error = (
                    "⚠️ 无法连接 Coze：未能从 config.json 读到 refiner.endpoint。\n\n"
                    "配置文件可能缺失或损坏。请检查技能目录下的 config.json 是否包含：\n"
                    '  "refiner": { "endpoint": "https://ct-advisor.coze.site/run" }\n\n'
                    "本技能的问答能力完全依赖云端 Coze 引擎，配置恢复前无法作答。"
                )
            else:
                _res.internal_error = (
                    "⚠️ 未授权出站到 Coze，无法获取答案。\n\n"
                    f"目标 endpoint：{_ep}\n"
                    "该地址不在 config.json 的 auto_approve_endpoints 白名单中，"
                    "出站请求已被拦截。\n\n"
                    "请由用户确认后将该 endpoint 加入白名单再重试"
                    "（授权项只能由用户自行修改 config.json，本地大模型不得代改配置）。"
                )
            coze_result[0] = _res
            return
        coze_result[0] = _fire_coze(req, config_path)

    t_coze = threading.Thread(target=_coze_job, name="coze")
    t_coze.start()
    threads.append(t_coze)

    t_pre = None
    if prefetch_tool:
        card = {
            "need_tool": prefetch_tool,
            # 2026-11-09 主流程修复：此前预判只把主判技能塞进执行卡，
            # need_tools 虽已算出却没传下去 → execute_card 的 deferred 为空，
            # 混合提问的答案里只剩一张 handoff 卡片，其余技能全部丢失。
            "need_tools": need_tools or [prefetch_tool],
            "params": prefetch_params,
            "draft_answer": "",
            "original_question": orig_q,
        }
        def _pre_job():
            prefetch_out[0] = _fire_prefetch(card)
        t_pre = threading.Thread(target=_pre_job, name="prefetch")
        t_pre.start()
        threads.append(t_pre)

    for t in threads:
        t.join()

    out = build_output(orig_q, coze_result[0], prefetch_out[0], prefetch_tool,
                       prefetch_params, need_tools=need_tools,
                       suggest_tools=(pred.get("suggest_tools") or []))

    # 回写本地答案缓存（2026-10-16）：**只缓存 Coze 正常返回的非空答案**。
    # 必须排除的四类输出，否则会把「错误提示」缓存 30 分钟，形成
    # 「Coze 已恢复、却一直返回旧错误」的新故障（代码复审 2026-10-16 发现）：
    #   - 委托块：需 agent 侧继续执行，缓存会跳过必要流程；
    #   - dependency_error / connection_error / internal_error 三类错误通道
    #     （build_output 第 320/330/338 行，均以 _wrap 包裹后返回）；
    #   - Coze final_answer 为空：build_output 会降级成「⚠️ Coze 返回为空」
    #     （第 437 行）或纯技能兜底文本（第 398/433 行）。
    _coze_res = coze_result[0]
    _cacheable = (
        _coze_res is not None
        and not getattr(_coze_res, "dependency_error", None)
        and not getattr(_coze_res, "connection_error", None)
        and not getattr(_coze_res, "internal_error", None)
        and bool((getattr(_coze_res, "final_answer", "") or "").strip())
    )
    if _ck and _cacheable and TOOL_DELEGATE_START not in out:
        try:
            import answer_cache as _ac
            if out.strip():                     # 内部已是明文，直接入缓存
                _ac.put(_ck, out)
        except Exception:  # noqa: BLE001
            pass

    return out


# ---------------------------------------------------------------------------
# 内置自测（mock Coze / 预判，无网络 / 无本地技能调用）
# ---------------------------------------------------------------------------

def _mk_coze(final_answer: str, need_tool: str | None = None, params: dict | None = None):
    """构造 mock 的 Coze 结构化结果（自测用）。

    用标准库 SimpleNamespace 仅承载 build_output 读取的三个字段，避免为自测而在模块导入期
    加载 adapters.refiner（44KB 重模块）——SELF_TEST 列表在 import 时即调用本函数，
    故必须保持零重依赖。
    """
    import types
    return types.SimpleNamespace(final_answer=final_answer, need_tool=need_tool, params=params or {})


def _mk_prefetch(tool: str, status: str, result=None) -> dict:
    return {"tool": tool, "status": status, "result": result or {}, "draft_answer": "", "elapsed_sec": 0.0}


SELF_TEST = [
    # (描述, orig_q, coze, prefetch_out, prefetch_tool, prefetch_params, 期望标记)
    ("预判ok且Coze无需工具 → 包裹答案",
     "算样本量 ORR 30% vs 45%", _mk_coze("Coze说算一下"), _mk_prefetch("ct-samplesize", "ok", {"n": 120}),
     "ct-samplesize", {"p1": 0.3, "p2": 0.45}, "__ANSWER__"),

    ("Coze需同工具且预判ok → 包裹答案（不重复调）",
     "算样本量", _mk_coze("Coze草稿", "ct-samplesize", {}), _mk_prefetch("ct-samplesize", "ok", {"n": 99}),
     "ct-samplesize", {}, "__ANSWER__"),

    ("预判need_params → 委托（列出缺失）",
     "算样本量", _mk_coze("Coze草稿", "ct-samplesize", {}),
     _mk_prefetch("ct-samplesize", "need_params", {"missing": ["效应量参数(任选其一): p1 / p2"]}),
     "ct-samplesize", {}, "CT_TOOL_DELEGATE"),

    ("预判ok但Coze需不同工具 → 委托（并入预判）",
     "查PD-1三期试验并算样本量", _mk_coze("Coze草稿", "ct-registry", {"cond": "PD-1"}),
     _mk_prefetch("ct-samplesize", "ok", {"n": 88}), "ct-samplesize", {},
     "CT_TOOL_DELEGATE"),

    ("无预判且Coze需工具 → 委托",
     "XX药文献", _mk_coze("Coze草稿", "ct-literature", {"topic": "XX药"}),
     None, None, {}, "CT_TOOL_DELEGATE"),

    ("Coze答案足够且无预判 → 包裹",
     "什么是SDTM", _mk_coze("SDTM是...", None, {}),
     None, None, {}, "__ANSWER__"),

    ("Coze空 + 无工具 → 兜底警告包裹",
     "边缘问题", _mk_coze("", None, {}),
     None, None, {}, "__ANSWER__"),

    ("预判error但Coze需同工具 → 委托重试",
     "查XX药安全性", _mk_coze("Coze草稿", "ct-safety", {"drug": "XX"}),
     _mk_prefetch("ct-safety", "error", "rc=1"), "ct-safety", {"drug": "XX"},
     "CT_TOOL_DELEGATE"),

    # 2026-09-25 补充回归用例：B 档 / 未发布 A 档分支（此前因自测只覆盖 Tier-A 工具，
    # 漏掉 _unreleased_payload / _unpublished_payload 的 NameError，真实触发即崩）。
    ("无预判 + Coze需B档工具(ct-protocol) → unreleased包裹",
     "审阅试验方案", _mk_coze("草稿", "ct-protocol", {}),
     None, None, {}, "__ANSWER__"),

    ("无预判 + Coze需未发布A档工具(ct-pipeline) → unpublished包裹",
     "公开情报编排", _mk_coze("草稿", "ct-pipeline", {}),
     None, None, {}, "__ANSWER__"),
]


def run_self_test() -> int:
    print("orchestrate.py 编排决策自测")
    print("=" * 60)
    ok = 0
    for desc, q, coze, pre, pt, pp, expect in SELF_TEST:
        out = build_output(q, coze, pre, pt, pp)
        if expect == "__ANSWER__":
            # 答案路径：有正文且不是委托卡（v1.3.20 起内部不再有包裹标记）
            valid = bool(out.strip()) and TOOL_DELEGATE_START not in out
        else:
            valid = TOOL_DELEGATE_START in out and TOOL_DELEGATE_END in out
        mark = "✓" if valid else "✗"
        if valid:
            ok += 1
        print(f"  {mark} [{('OK' if valid else 'BADFMT'):<6}] {desc}")
    # 2026-09-10（第十四轮，用户要求）：软建议页脚——不调用兄弟技能，
    # 先自身作答，再在答案**末尾**追加可直接调用的 @skill 建议（弱命中 / 咨询意图路径）。
    prog = build_output("样本量计算要注意什么", _mk_coze("样本量取决于效应量与把握度。")
                        , None, None, {}, suggest_tools=["ct-samplesize"])
    sug_ok = ("兄弟技能" in prog) and ("ct-samplesize" in prog) \
        and (TOOL_DELEGATE_START not in prog)
    print(f"  {'✓' if sug_ok else '✗'} [{'OK' if sug_ok else 'BADFMT'}] 软建议：先作答 + 末尾建议 ct-samplesize")
    ok += 1 if sug_ok else 0

    total = len(SELF_TEST) + 1
    print("-" * 60)
    print(f"  准确率: {ok}/{total} = {ok / total * 100:.1f}%")
    return 0 if ok == total else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="ct-advisor code-only orchestrator (Mode B + LLM delegate)")
    ap.add_argument("--payload-inline", help="inline JSON payload (3变量: query_meta/original_question/draft_answer)")
    ap.add_argument("--payload", help="path to JSON payload file (legacy)")
    ap.add_argument("--config", default=str(SKILL_ROOT / "config.json"), help="path to config.json")
    ap.add_argument("--no-prefetch", action="store_true", help="跳过前端预判预取，仅走 Coze")
    ap.add_argument("--tone", default=None, help="path to tone_profile.json (style-only)")
    ap.add_argument("--memory", default=None, help="path to ct-advisor-memory.json")
    ap.add_argument("--self-test", action="store_true", help="运行内置编排决策自测")
    args = ap.parse_args()

    if args.self_test:
        return run_self_test()

    # 读取 payload（优先 inline，其次文件，再次 stdin）
    if args.payload_inline:
        raw = args.payload_inline
    elif args.payload:
        p = Path(args.payload)
        if not p.exists():
            sys.stderr.write(f"[ct-advisor] payload 文件未找到: {args.payload}\n")
            sys.exit(2)
        raw = p.read_text(encoding="utf-8")
    else:
        raw = sys.stdin.read()

    try:
        out = run_orchestrate(raw, args.config, no_prefetch=args.no_prefetch)
    except Exception as e:  # noqa: BLE001
        # 编排器本身崩溃：绝不静默，输出明确兜底
        sys.stderr.write(f"[ct-advisor][ORCH-FAIL] {type(e).__name__}: {e}\n")
        sys.stdout.write(
            "⚠️ 编排器执行异常，未产出结构化答案。请稍后重试。"
        )
        sys.exit(0)

    sys.stdout.write(out)
    sys.exit(0)


if __name__ == "__main__":
    sys.exit(main())
