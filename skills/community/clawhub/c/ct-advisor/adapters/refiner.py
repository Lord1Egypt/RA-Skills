"""答案精校适配层（第 4 个 seam）：本地草稿 → 外发 3 变量 → 回收最终答案。

设计要点（沿用 v0.8.2 审计后确立的「安全默认」范式）：
- CozeRefiner 是**唯一**的精校后端：将 3 变量 POST 到扣子服务器，≤timeout 秒回收 final_answer；
  任何超时 / 网络 / 解析 / 字段缺失异常都优雅回退到 draft_answer（绝不丢答案、绝不报错给用户）。
- 不再有「local 精校模式」：答案精校经唯一的 `fast` 模式控制，按难度自动分流——
  simple/middle 走 **race 竞速（早发 / 速度优先）**：agent 在 **step 2** 后台调用
  `--fire-only`（agent 仅发 original_question，difficulty/category/accuracy 未提供时由脚本补空串，draft 留空），
  Coze 用**完整 90s** HTTP 超时独立分析；成功后写入 race 缓存。
  agent 在 **step 3** 并行写本地草稿 + `--collect` 收集：缓存命中（Coze 先回）→ 采用
  Coze（中断本地）；否则直接采用本地草稿（速度优先——本地秒级先出、Coze 实测 9~25s 慢、
  常态本地胜出）。complex/vague 走 **串行**（前台等 Coze 完整返回、含 draft_answer 一并发送），
  两者都走 Coze、失败/超时回退本地草稿。
- 传输层（2026-10-15 C 方案）：stdlib `urllib`（`_call_coze` 内），**零第三方依赖**——
  `requests` 不再是必需依赖，「依赖缺失」作为一类用户可见失败被整体消灭；
  urllib 同样读取 HTTP(S)_PROXY 环境变量，HTTPS 经 http 代理时自动走 CONNECT 隧道
  （本机实测：经系统代理 POST 端点返回 200）。
- 失败双通道（2026-10-15 B 方案）：人读提示挂 `RefineResult.connection_error` /
  `internal_error` 供 `build_output` 渲染；机器错误码经 `emit_err_signal` 发 stderr
  `[ct-advisor][ERR]` 信号，供调用方 agent 按 SKILL.md「错误自愈协议」决策。
  成功路径两通道均静默——未报错时 agent 不得进入自愈流程。

外发 payload（3 变量）：
- query_meta:   dict，包含 difficulty / category / accuracy 三字段 + query_origin 机器标识
                - difficulty: 入口闸门结论 vague | forwarded（2026-09-26 二值化；
                  旧值 simple | middle | complex 仅为 payload 兼容接受，不携带语义——
                  服务端一律用 LLM 重新估计难度；转发超时档位改由 route.timeout_tier 判定）
                - category:   问题类别（如 methodology:B / methodology:C / design / compliance:D，或匹配的 A–J 工作流；样本量用 methodology:C）
                - accuracy:   自评准确度 good | normal（good = 精确，normal = 一般）
                - query_origin: 审计元数据——机器标识（sha256(hostname)，主机派生的稳定标识：不含明文主机名/IP，但同设备跨请求稳定；不可逆；《隐私段》已向用户披露），
                                由脚本在 normalize() 时自动盖章写入本 dict（不再另设顶层字段）
- original_question:  用户的原始问题（未加工原话）
- draft_answer:       本地生成的答案（草稿），供服务器参考/精校（允许空串）。
                      注意：accuracy 不再写入 draft_answer，而是放在 query_meta 中。

来源标记协议（v0.9.1+）：
- draft_answer 中来自其他 ct 技能的段落用 <source skill="ct-xxx">...</source> 标记。
- ct-advisor 自己整合的段落**不**带标签。
- 出站给 coze 时**不剥离**标签——原样发送，由 coze prompt 负责识别并跳过标记段落。
- 因此本模块不需要剥离/嵌入逻辑，标签会原样穿过 coze。
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import socket
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import copy

# i18n: user-facing prompts (EN/ZH) resolved by OS locale / config
import pathlib
_SKILL_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(_SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(_SKILL_ROOT))
from scripts.i18n import t, resolve_user_language  # noqa: E402

# 公共凭据统一从 adapters/coze_token_embedded.py 导入（XOR+base64 混淆内嵌，ct-base §5 合规；
# .py 后缀不被 SkillHub 文件过滤删除；禁明文 JWT 落盘）。
from adapters.coze_token_embedded import get_token
from adapters.errsignal import emit_err_signal  # noqa: E402  结构化错误信号（stderr 机器通道）

# ── §8.6 硬件绑定机器标识：统一从本技能 scripts/hardware_id.py 导入（ct-base 共享件 vendored 副本）──
import os as _os
import sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "scripts"))
try:
    from hardware_id import hardware_id as _hardware_id
except Exception:  # pragma: no cover
    _hardware_id = None


class MissingDependencyError(Exception):
    """精校所需的第三方依赖缺失（如 requests），且自动安装失败。

    该异常**不**应被 refine() 的兜底逻辑静默吞掉——调用方须显式告知用户安装，
    否则用户会误以为拿到的答案来自 Coze 精校，实则是未精校的本地草稿。
    """


# 2026-10-15（C 方案）：传输层切换为 stdlib urllib 后，requests 不再是必需依赖，
# _ensure_requests() 及其「缺失即提示安装并退出」逻辑整体移除——
# 「依赖缺失」失败类被消灭（entry.py 预检同步改为非致命留痕）。
# MissingDependencyError 类保留：adapters/__init__.py 仍导出它；orchestrate /
# refine_answer 中的 except 分支为防御性死代码（urllib 路径不会抛出它）。

def _env_proxy_present() -> bool:
    """检测运行环境是否配置了系统/环境变量代理（HTTP(S)_PROXY / ALL_PROXY，大小写皆可）。

    仅用于决定出站重试顺序：有代理则优先走代理、连接失败再回退直连；无代理则直接直连。
    读取标准代理环境变量，不依赖任何平台特定 API。
    """
    for _k in ("HTTPS_PROXY", "HTTP_PROXY", "https_proxy", "http_proxy",
               "ALL_PROXY", "all_proxy"):
        if os.environ.get(_k):
            return True
    return False

_TIMEOUT_HINT = (
    "⚠️ 请求超时：Coze 服务未在限定时间内响应。请求很可能已送达 Coze，仅是回包较慢。\n\n"
    "请按以下步骤处理：\n"
    "  ① 稍等 1–2 分钟，重新运行本技能（多数情况下再次请求即可成功）；\n"
    "  ② 若持续超时，可能是 Coze 端繁忙或本机到代理链路拥塞，可尝试切换网络/代理后重试；\n"
    "  ③ 仍不行请间隔 10 分钟后再试，避免短时间高频重试造成请求重复发送。\n"
    "注意：超时不等于请求失败，请勿为「确认是否送达」而多次重复提问。"
)


def _current_proxy() -> str:
    """读取当前生效的代理值（HTTPS 优先，其次 HTTP）；未配置返回空串。

    用于错误提示里展示**真实**代理配置——避免硬编码过期端口误导用户
    （本地代理端口会随代理软件重启变化，写死必然过期）。
    """
    for _k in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"):
        _v = os.environ.get(_k)
        if _v:
            return _v
    return ""


def _classify_outbound_error(e: Exception, proxy_attempted: bool = False):
    """把出站异常分类为 ``(机器错误码, 人读提示)``；非网络类异常返回 ``(None, None)``。

    机器错误码见 adapters/errsignal.py::ERR_CODES（调用方经 emit_err_signal 发
    stderr 信号）；人读提示挂 RefineResult.connection_error，由 build_output
    渲染为「编号步骤」式排查指引。两类都绝不静默。

    proxy_attempted: 本次是否尝试过系统代理路径（env 含 HTTP(S)_PROXY）。
    当本机已配代理却失败时，优先给出「检查/启动代理」的针对性步骤。

    异常 taxonomy（stdlib urllib，2026-10-15 起；requests 版已移除）：
      - urllib.error.HTTPError        服务端有响应（401/5xx）→ AUTH_401 / COZE_HTTP_ERROR
      - TimeoutError(socket.timeout)  超时（含 URLError.reason 包装）→ TIMEOUT
      - ssl.SSLError                  TLS 握手失败（代理 MITM / 证书 / 时间偏差）→ CONN_FAIL_*
      - urllib.error.URLError / OSError   连接阶段失败 → CONN_FAIL_PROXY / CONN_FAIL_DIRECT
    """
    import socket
    import ssl
    import urllib.error

    _proxy_hint = _current_proxy() or "未设置（当前环境没有代理变量）"

    # ── HTTP 层：服务端有响应，不是连接问题 ──
    if isinstance(e, urllib.error.HTTPError):
        if e.code == 401:
            return ("AUTH_401",
                "⚠️ Coze 鉴权失败（HTTP 401）：访问令牌已失效或被撤销。\n\n"
                "请按以下步骤处理：\n"
                "  ① 这不是网络问题，重试无效；\n"
                "  ② 请向技能维护者索取新的访问令牌（内嵌于 adapters/coze_token_embedded.py）；\n"
                "  ③ 更新后重新运行本技能。")
        return ("COZE_HTTP_ERROR",
            "⚠️ Coze 服务端返回 HTTP %s：服务暂时不可用或请求被拒绝。\n\n"
            "请按以下步骤处理：\n"
            "  ① 稍等 1–2 分钟后重新运行本技能；\n"
            "  ② 若持续出现，请附上本提示联系技能维护者（Coze 工作流可能异常）。" % e.code)

    # ── 超时：Coze 很可能已收到请求，严禁自动重试 ──
    if isinstance(e, (socket.timeout, TimeoutError)):
        return ("TIMEOUT", _TIMEOUT_HINT)
    if isinstance(e, urllib.error.URLError) and isinstance(
            getattr(e, "reason", None), (socket.timeout, TimeoutError)):
        return ("TIMEOUT", _TIMEOUT_HINT)

    # ── TLS 握手失败：本地代理拦截 / 证书链 / 系统时间偏差 ──
    if isinstance(e, ssl.SSLError):
        _code = "CONN_FAIL_PROXY" if proxy_attempted else "CONN_FAIL_DIRECT"
        return (_code,
            "⚠️ TLS/SSL 握手失败：无法与 Coze 建立加密连接。\n\n"
            "请按以下步骤排查：\n"
            "  ① 若本机使用本地代理（当前值：%s），代理软件可能拦截了 HTTPS 流量——\n"
            "     检查代理的证书配置，或临时清除代理直连验证：set HTTPS_PROXY=\n"
            "  ② 检查系统时间是否准确（时间偏差会导致证书校验失败）；\n"
            "  ③ 检查防火墙 / 杀毒是否对 Python 做 HTTPS 扫描，必要时临时放行；\n"
            "  ④ 排查完成后重新运行本技能。" % _proxy_hint)

    # ── 连接阶段失败（拒绝 / 无路由 / DNS / 代理不可达） ──
    if isinstance(e, (urllib.error.URLError, ConnectionError, OSError)):
        if proxy_attempted:
            return ("CONN_FAIL_PROXY",
                "⚠️ 出站连接失败：本机已配置系统代理（当前值：%s），"
                "但经代理与直连均无法建立到 Coze 的连接。\n\n"
                "请按以下步骤恢复：\n"
                "  ① 优先确认代理软件/服务是否正在运行（本机常用 127.0.0.1 端口的本地代理）；\n"
                "     查看当前代理：PowerShell  $env:HTTPS_PROXY   /   CMD  echo %%HTTPS_PROXY%%\n"
                "  ② 若代理未启动，先启动它；若地址/端口已变更，更新环境变量：\n"
                "       set HTTPS_PROXY=http://<代理地址>:<端口>\n"
                "  ③ 若确无需代理，临时清除后重试（技能会改走直连）：\n"
                "       set HTTPS_PROXY=\n"
                "  ④ 用 curl 验证出网是否通畅：\n"
                "       curl -I https://ct-advisor.coze.site/run\n"
                "     仍连不通，检查防火墙 / 杀毒软件是否拦截了 Python 出网。\n"
                "  ⑤ 排查完成后，重新运行本技能即可。" % _proxy_hint)
        return ("CONN_FAIL_DIRECT",
            "⚠️ 出站连接失败：无法建立到 Coze 的网络连接（本机无出网路由，或连接被目标拒绝）。\n\n"
            "请按以下步骤排查并恢复：\n"
            "  ① 确认本机代理环境变量是否已设置（本机通常需经代理出网）：\n"
            "       PowerShell：  $env:HTTPS_PROXY\n"
            "       CMD：         echo %%HTTPS_PROXY%%\n"
            "     当前值：%s\n"
            "     若为空，请向网络管理员索取代理地址后设置，或直接在本机终端执行：\n"
            "       set HTTPS_PROXY=http://<代理地址>:<端口>\n"
            "  ② 若已配置代理，确认代理软件/服务正在运行且地址端口正确。\n"
            "  ③ 用 curl 验证出网是否通畅：\n"
            "       curl -I https://ct-advisor.coze.site/run\n"
            "     若连不通，检查防火墙 / 杀毒软件是否拦截了 Python 出网。\n"
            "  ④ 排查完成后，重新运行本技能即可。" % _proxy_hint)

    return (None, None)


def _internal_error_msg(e: Exception) -> str:
    """非网络类失败（配置损坏 / token 解码失败 / 响应解析失败 / 代码缺陷）的人读提示。

    与 connection_error 同理：绝不静默为空答案、绝不伪装成「返回为空，请稍后重试」。
    """
    return (
        "⚠️ 技能内部错误（%s）：未成功连接到 Coze 或响应解析失败，通常与网络无关。\n\n"
        "请按以下步骤处理：\n"
        "  ① 重新运行本技能一次（偶发瞬时故障多可自行恢复）；\n"
        "  ② 若持续出现，请把本提示连同上面的错误信息反馈给技能维护者；\n"
        "  ③ 排查期间不会返回任何未经精校的占位内容。"
        % type(e).__name__
    )

# 展示前剥离 <source> 标签的正则（注意：用字符类 ["'] 避免 \" 在 raw string 中的解析问题）
_DISPLAY_TAG_RE = re.compile(r'''<source\s+skill=["'][^"]*["']>\s*''', re.IGNORECASE)
_DISPLAY_CLOSE_TAG_RE = re.compile(r'\s*</source>', re.IGNORECASE)


def strip_display_tags(text: str) -> str:
    """剥离 <source skill="xxx"> 标签，仅用于展示。
    保留标签内的内容，只移除标签本身。
    示例：'<source skill="ct-safety">内容</source>' → '内容'
    """
    s = _DISPLAY_TAG_RE.sub("", text)
    s = _DISPLAY_CLOSE_TAG_RE.sub("", s)
    return s


def _purify_tilde_range(text: str) -> str:
    """把范围语义的半角 ~ 替换为连字符 -，避免被 markdown 渲染器误判为删除线。

    根因：Coze 返回的答案常写数值/百分比范围如 `40%~60%`、`3~4级`、`8%~12%`，
    半角 ~ 被 WorkBuddy 渲染面板当成 strikethrough 配对边界 → 中间文本被划线，
    用户误以为答案是"被删除/划掉"的内容。

    纠正策略（优于转全角 ～）：仅当 ~ 两侧均为数字或 %（即数值/百分比范围）时才
    替换为 -；其余 ~ 原样保留，保护代码块、`~/.workbuddy` 路径、URL、近似符号
    ~0.05 等不被误伤。中英文答案均适用（40%-60% / 3-4级 两种语境都自然）。

    说明：前端 strikethrough 语法解释无法在技能侧关闭，唯一可控的是在文本层
    破坏会触发删除线的配对，故采用精准的范围 ~ → - 替换。
    """
    if not text:
        return text
    # 仅替换两侧是数字或百分号的 ~（两侧允许空白）；其余 ~ 不动
    return re.sub(r"(?<=[\d%])\s*~\s*(?=[\d%])", "-", text)


# §20.15 顶层可选 message 字段归一化（ct-base references/coze_io_contract.md §5 信封唯一真相源）
_MESSAGE_LEVELS = ("tip", "info", "notice", "warning")


def _normalize_coze_message(raw: Any) -> Optional[dict]:
    """归一化 Coze 响应信封顶层可选 ``message`` 字段为统一结构。

    契约（ct-base §5）：结构 ``{level, text, dismissible}``；coze 给裸字符串时按
    ``{level:"notice", text, dismissible:True}`` 归一化；多条则合并进一段 text。
    返回 ``{"level": "notice", "text": "...", "dismissible": True}`` 或 None
    （缺失 / 为空 / 解析失败）。向后兼容：老 coze 不返回 → 返回 None（本地不渲染，呼应 §20.11）。
    """
    if raw is None:
        return None
    if isinstance(raw, str):
        raw = raw.strip()
        if not raw:
            return None
        return {"level": "notice", "text": raw, "dismissible": True}
    if isinstance(raw, list):
        # 多条合并：逐元素归一化取 text，非空则拼为一段（禁止递归数组）
        parts = []
        for item in raw:
            sub = _normalize_coze_message(item)
            if sub and sub.get("text"):
                parts.append(sub["text"])
        if not parts:
            return None
        return {"level": "notice", "text": "\n".join(parts), "dismissible": True}
    if isinstance(raw, dict):
        text = (raw.get("text") or "").strip() if isinstance(raw.get("text"), str) else ""
        if not text:
            return None
        level = raw.get("level")
        if level not in _MESSAGE_LEVELS:
            level = "notice"  # 非法 level 回退默认，仅影响样式不影响位置
        dismissible = raw.get("dismissible", True)
        if not isinstance(dismissible, bool):
            dismissible = True
        return {"level": level, "text": text, "dismissible": dismissible}
    # 其它类型（数字/布尔等）视为无效，静默跳过
    return None


# ── 2026-11-11 v1.68：云端返回结构对接校验（「对接不匹配」检测）──
# 已知响应字段（coze /run 的 GraphOutput 契约）。用于判断返回结构是否与本地技能版本匹配。
_KNOWN_RESPONSE_KEYS = (
    "final_answer", "answer", "need_tool", "need_tools", "deferred_tools",
    "params", "run_id", "message", "coze_version", "cached_answer", "cache_hit",
)


def _check_struct_mismatch(data: Any) -> bool:
    """检测 coze 返回结构是否与本地技能版本不匹配。

    返回 True 表示结构异常（应触发升级/改用 Web 应用提醒）：
      ① data 非 dict；
      ② 不含任何已知响应字段（完全未知结构）；
      ③ 既无答案字段（final_answer/answer）又无委托字段（need_tool/need_tools/
         deferred_tools）——handoff 场景 need_tool 有值属合法，不误报。
    """
    if not isinstance(data, dict):
        return True
    if not any(k in data for k in _KNOWN_RESPONSE_KEYS):
        return True
    if (not (data.get("final_answer") or data.get("answer") or data.get("cached_answer"))
            and not (data.get("need_tool") or data.get("need_tools")
                     or data.get("deferred_tools"))):
        return True
    return False


# difficulty 枚举（2026-09-26 二值化：vague | forwarded；旧三档标签仅为历史 payload 兼容保留）
DIFFICULTY_ENUM = ("vague", "forwarded", "simple", "middle", "complex")

# accuracy 枚举（good/normal）—— good = 精确，normal = 一般
ACCURACY_ENUM = ("good", "normal")

def _skill_version() -> str:
    """读取本技能 SKILL.md frontmatter 的 ``version:`` 作为 coze 信封 ``skill_version``。

    单一事实来源（ct-base coze_io_contract §1.2）：升版本免改代码；读取失败回退内置常量。
    """
    try:
        p = _SKILL_ROOT / "SKILL.md"
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                if line.startswith("version:"):
                    return line.split(":", 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return "1.0.0"


def compute_machine_id() -> str:
    """稳定、不可逆、硬件绑定的机器标识，由脚本在调用时自动盖章（覆盖输入，agent 不应手写）。

    同一台物理机器每次返回相同值（便于 Coze 侧按机器做审计/归因/限流）——优先取
    硬件令牌（SMBIOS UUID / MachineGuid / machine-id，跨 Windows 账号 / 改主机名 /
    重装系统稳定）；取不到时回退主机名（保证永不崩）。旧实现 sha256(hostname) 在
    容器 / 云端环境会随会话或账号漂移，已弃用。
    """
    if _hardware_id is not None:
        return "sha256:" + _hardware_id().split(":", 1)[1]
    try:
        return "sha256:" + hashlib.sha256(socket.gethostname().encode("utf-8")).hexdigest()
    except Exception:  # pragma: no cover
        return "sha256:" + hashlib.sha256(b"unknown-host").hexdigest()


def _parse_query_meta(query_meta: Any) -> Dict[str, Any]:
    """解析 query_meta：支持 JSON 字符串或 dict；缺失字段给默认值空串。

    query_origin（机器标识）若已在输入中存在则原样保留，供 validate() 校验。
    """
    if isinstance(query_meta, str):
        try:
            meta = json.loads(query_meta)
        except Exception:
            meta = {}
    elif isinstance(query_meta, dict):
        meta = dict(query_meta)
    else:
        meta = {}
    result: Dict[str, Any] = {
        "difficulty": str(meta.get("difficulty", "")).strip(),
        "category": str(meta.get("category", "")).strip(),
        "accuracy": str(meta.get("accuracy", "")).strip(),
    }
    # query_origin 透传：若输入已含合法机器标识则保留，否则留空待 normalize() 盖章
    qo = meta.get("query_origin", "")
    result["query_origin"] = str(qo).strip() if qo else ""
    return result


@dataclass
class RefineResult:
    """Coze 单次调用的结构化结果（全量直发方案，2026-08-14）。

    兼容旧调用方：final_answer 始终有值（need_tool 分支下为 Coze 草稿），
    cache_hit 字段保留；新字段 need_tool / params 供本地执行器识别。
    """
    final_answer: str = ""            # Coze 最终答案；need_tool 分支下=Coze 草稿（缝合基底）
    cached_answer: str = ""           # 缓存命中答案（兼容旧字段）
    cache_hit: bool = False           # 是否命中缓存
    need_tool: Optional[str] = None   # 需要本地执行的技能标识（None=无需技能）
    params: dict = field(default_factory=dict)  # 技能入参
    run_id: str = ""                  # 追踪用
    message: Optional[dict] = None     # §20.15：Coze 业务侧表面提示（顶层可选 message 字段归一化后）
    # 2026-11-09：Coze 侧 tool_router 若返回多技能命中，必须带进本地，
    # 否则预判未命中的混合问题在委托路径里只剩单一技能。缺省空列表，向后兼容。
    need_tools: list = field(default_factory=list)
    # 2026-11-11 v1.68：云端端点版本（出参侧，与飞书 coze_version 同源）。
    # 空串 = 云端未声明（老版本 / 响应契约不匹配）→ 本地兜底提醒升级。
    coze_version: str = ""

    def __post_init__(self):
        # 净化 final_answer：范围 ~ → -，避免渲染器误判删除线（见 _purify_tilde_range）
        self.final_answer = _purify_tilde_range(self.final_answer)


@dataclass
class RefineRequest:
    query_meta: dict = field(default_factory=dict)  # 包含 difficulty / category / accuracy / query_origin 的字典
    original_question: str = ""
    draft_answer: str = ""
    # 增量兼容字段（P0-A 本地澄清循环）：澄清子流程产出的问题画像与确认摘要。
    # 默认空 dict，下游（Coze 精校 / 本地草稿）忽略；原三字段契约完全不变。
    question_profile: dict = field(default_factory=dict)
    confirmation: dict = field(default_factory=dict)
    # 增量兼容字段（P0-B 语气写作）：tone_matcher.py 产出的风格 profile（仅风格、无事实）。
    # 默认空 dict；非空时随契约外发，Coze 按风格硬闸书写答案，绝不搬用样本事实。
    tone_profile: dict = field(default_factory=dict)
    # 增量兼容字段（P1-D 本地用户记忆）：memory_manager.py 产出的跨会话记忆上下文。
    # 默认空 dict；非空时随契约外发，仅作背景上下文，不得当作当前问题的事实。
    memory_context: dict = field(default_factory=dict)
    # 增量兼容字段（2026-08-25 混合上下文路线）：本地按时间窗+轮数裁剪后的有界对话历史，
    # 作为可选字段外发给 Coze，由 Coze LLM 自行判断相关性并引用前情（替代代码层窄启发式拼接）。
    # 默认空 list；非空时随契约外发。历史版本 Coze 忽略此字段亦兼容（pydantic 默认忽略额外字段）。
    conversation_history: list = field(default_factory=list)
    # 增量兼容字段（2026-08-25 模式 B 硬弃用本地 is_followup 正则）：is_followup 标记当前问题
    # 为「类型 B 追问」，现由 refine_answer.py 基于 history 存在性确定性派生（非正则猜），
    # 供远端 refiner 走 long_timeout（默认 300s）避免多轮上下文追问被截断。
    # 远端相关性判权已完全交 Coze LLM（经 conversation_history），本地不再做追问分类。
    is_followup: bool = False
    # 增量兼容字段（2026-09-23 大文档处理管线）：大文档的结构化载荷（JSON 信封，见
    # adapters/coze/src/doc/payload.py 契约真源：{v,doc_id,instruction,mode,text|chunks,...}）。
    # 非空时随契约外发，供 Coze（v1.21+）自行分块检索并按「文档 §N」引用；
    # 老 Coze 忽略该字段（pydantic extra='ignore'）→ 退化为 original_question 内联片段（仍可用）。
    doc_context: str = ""
    # 增量兼容字段（2026-09-23）：范围路由标签（""=在范围；"medical_writing" 等=超范围，
    # 由 scope_guard 产出）。本地已前置转介声明；非空时随契约外发，Coze 在提示词层一并强化声明。
    scope_hint: str = ""
    max_items: Optional[int] = None  # 已废弃且无操作：条目数量不再校验上限，统一直接发送 coze。

    def normalize(self) -> List[str]:
        """契约自愈（contract self-healing）。

        在 ``validate()`` 之前调用，将缺失/非法的可选字段补全为合法默认值，
        使 payload 在到达契约校验时一定合法——从根源上杜绝「契约校验失败 →
        静默兜底、远程根本没被调用」这一整类问题。

        自愈策略：
          - ``query_meta``：解析并修正枚举非法值；difficulty / category / accuracy
            缺失或非枚举合法值时统一补空串（``""``）；``query_origin`` 缺失则由脚本自动盖章
            （sha256 机器标识，写入 query_meta 字典）。
          - ``original_question``：若空，用 ``draft_answer`` 首行兜底。

        仅当 ``original_question`` 与 ``draft_answer`` 均为空（没有任何内容可兜底）
        时无法自愈；此时 ``validate()`` 会抛错，交由调用方（refine_answer.py）
        显式告警 + 兜底（而非静默）。

        返回本次被自动补全的字段/动作说明列表，供调用方在 stderr 做可见提示。
        """
        notes: List[str] = []

        # 1) query_meta：解析并补齐 / 修正枚举非法值（始终维持 dict 类型）
        if isinstance(self.query_meta, str):
            meta = _parse_query_meta(self.query_meta)
        elif isinstance(self.query_meta, dict):
            meta = dict(self.query_meta)
        else:
            meta = {}
        changed = False
        # difficulty 兜底（2026-09-26 二值化）：本地 route.py 只回答「是否 vague」——
        # vague 本地拦截澄清、不转发；转发链路统一携带 "forwarded"（与 entry.py 一致）。
        # 服务端 generate_organized_problems_node 会【一律用 LLM 重新估计】difficulty 并写回，
        # 因此此处兜底默认值不决定最终难度，仅保证出站 query_meta 非空（避免飞书收集空白）。
        # 缺失/非法一律默认 "forwarded"（转发即转发，不再冒充难度标签）。
        if not meta.get("difficulty") or meta["difficulty"] not in DIFFICULTY_ENUM:
            meta["difficulty"] = "forwarded"
            changed = True
        # category：允许 string 或 string[]（多标签）；缺失/空补空串；多标签去重保序、不裁剪
        cat_raw = meta.get("category", "")
        if isinstance(cat_raw, list):
            cat_filtered = []
            cat_seen = set()
            for s in cat_raw:
                if isinstance(s, str) and s.strip():
                    s2 = s.strip()
                    if s2 not in cat_seen:
                        cat_seen.add(s2)
                        cat_filtered.append(s2)
            meta["category"] = cat_filtered if cat_filtered else ""
            changed = True
        elif isinstance(cat_raw, str) and cat_raw.strip():
            pass  # 合法 string，保留
        else:
            meta["category"] = ""
            changed = True
        if not meta.get("accuracy") or meta["accuracy"] not in ACCURACY_ENUM:
            meta["accuracy"] = ""
            changed = True
        if changed or not isinstance(self.query_meta, dict):
            self.query_meta = meta
            notes.append("query_meta(auto-filled/coerced, kept as dict)")

        # 2) original_question：若空，用 draft_answer 首行兜底
        if not self.original_question or not self.original_question.strip():
            if self.draft_answer and self.draft_answer.strip():
                self.original_question = self.draft_answer.strip().splitlines()[0][:200]
                notes.append("original_question(filled from draft_answer)")
            # 两者皆空时不兜底，留给 validate 显式报错

        # 4) question_profile / confirmation（P0-A 增量字段）：非 dict 一律归一为空 dict，
        #    保证 to_payload() 外发的 JSON 始终合法、下游兼容。
        if not isinstance(self.question_profile, dict):
            self.question_profile = {}
        if not isinstance(self.confirmation, dict):
            self.confirmation = {}
        # 5) tone_profile / memory_context（P0-B / P1-D 增量字段）：非 dict 一律归一为空 dict。
        if not isinstance(self.tone_profile, dict):
            self.tone_profile = {}
        if not isinstance(self.memory_context, dict):
            self.memory_context = {}
        # 6.5) conversation_history（2026-08-25 混合上下文）：非 list 一律归一为空 list
        if not isinstance(self.conversation_history, list):
            self.conversation_history = []
        # 2026-10-30 修复（上下文交互缺陷 8）：除类型检查外，**按契约归一形态/顺序/摘要/轮数**。
        # 此前仅校验 isinstance(list) → 任何非契约形态（messages 形态 {role,content} 等）
        # 都会原样直达 Coze，后端 _history_fp 取空、"最近5轮"截断按条击穿 → 上下文事实为空。
        # 归一器 import 失败时保留原值（不阻断主流程）。
        if self.conversation_history:
            try:
                import history_norm as _hn
                self.conversation_history = _hn.normalize_history(self.conversation_history)
            except Exception:  # noqa: BLE001
                pass
        # 6.6) doc_context / scope_hint（2026-09-23 本地守卫）：非 str 一律归一为空串
        if not isinstance(self.doc_context, str):
            self.doc_context = ""
        if not isinstance(self.scope_hint, str):
            self.scope_hint = ""

        # 3) query_origin：脚本会盖章，写入 query_meta 字典（不再另设顶层字段）
        qm = self.query_meta if isinstance(self.query_meta, dict) else {}
        if not qm.get("query_origin") or not str(qm.get("query_origin", "")).strip():
            qm["query_origin"] = compute_machine_id()
            notes.append("query_meta.query_origin(stamped)")
            self.query_meta = qm

        return notes
    def validate(self) -> None:
        """契约校验（contract-first）。

        经 ``normalize()`` 自愈后，除「original_question 与 draft_answer 均为空」
        这一极端情形外，应当总能通过。校验失败抛 ValueError；调用方负责捕获后
        显式告警 + 兜底，不再静默。

        字段约束（经 normalize() 自愈后）：
          - query_meta       : 非空 dict，包含 difficulty / category / accuracy / query_origin
                               difficulty ∈ {simple, middle, complex, vague}（允许为空串）
                               accuracy ∈ {good, normal}（允许为空串）
                               category   : 任意非空串，或为空串（允许未提供）
                               query_origin : 非空，格式 sha256:<64 hex>（机器标识，脚本盖章）
          - original_question  : 非空
          - draft_answer       : 允许为空
          - difficulty / category / accuracy 缺失时由 normalize() 补空串，不再强制非空；
            仅当「非空但枚举非法」时（difficulty / accuracy）才报错。
        校验失败抛 ValueError；调用方（refine_answer.py）捕获后兜底输出 draft_answer。
        """
        # 校验 query_meta
        if not self.query_meta or not str(self.query_meta).strip():
            raise ValueError("required field 'query_meta' is empty")
        meta = _parse_query_meta(self.query_meta)
        # difficulty / category / accuracy 允许为空串（agent 未提供时由 normalize() 补空串）；
        # 仅在「非空但枚举非法」时才报错。category 无枚举约束，非空即合法。
        if meta["difficulty"] and meta["difficulty"] not in DIFFICULTY_ENUM:
            raise ValueError(
                f"query_meta.difficulty must be one of {DIFFICULTY_ENUM}, got {meta['difficulty']!r}"
            )
        if meta["accuracy"] and meta["accuracy"] not in ACCURACY_ENUM:
            raise ValueError(
                f"query_meta.accuracy must be one of {ACCURACY_ENUM}, got {meta['accuracy']!r}"
            )
        qo = str(meta.get("query_origin", "")).strip()
        if not qo:
            raise ValueError("query_meta.query_origin is empty (set via compute_machine_id)")
        if not qo.startswith("sha256:"):
            raise ValueError("query_meta.query_origin must start with 'sha256:'")
        hexpart = qo[len("sha256:"):]
        if len(hexpart) != 64 or any(ch not in "0123456789abcdef" for ch in hexpart):
            raise ValueError("query_meta.query_origin must be 'sha256:' + 64 hex chars")
        if not self.original_question or not self.original_question.strip():
            raise ValueError("required field 'original_question' is empty")
        # draft_answer 允许为空，不做校验
    def to_payload(self) -> Dict[str, Any]:
        self.normalize()  # 出站前自愈：任何外发路径都先补全缺失/非法字段
        self.validate()  # 契约校验前置：经自愈后此处应当通过
        # 发送变量（query_meta / original_question / draft_answer / conversation_history）：
        # 前三者为原始契约三字段；conversation_history 为 2026-08-25 新增的可选字段，
        # 由本地按时间窗+轮数裁剪后传出，供 Coze LLM 自行判相关性引用前情。
        # 默认空 list（无历史时不携带），历史版本 Coze 忽略此字段亦兼容。
        # ── 2026-09-23 大文档处理管线：doc_context / scope_hint 按「非空才带」外发 ──
        # doc_context：大文档结构化载荷（含 doc_id/instruction/正文或分块），Coze v1.21+ 据此
        #   自行分块检索并以「文档 §N」引用；空串时不带（普通问题零负担）。
        # scope_hint ：范围路由标签（如 medical_writing），Coze 在提示词层强化范围外声明。
        # 兼容性：老 Coze 的 GraphInput 为 pydantic 模型（extra='ignore'）→ 静默忽略这两个字段；
        #   老本地不发 → 新 Coze 用字段缺省值（""）→ 走无文档路径。双向兼容。
        # question_profile / confirmation / tone_profile / memory_context 保留在 RefineRequest
        # 内但不再外发（服务端未实现；待服务端补齐后再恢复发送）。
        # ── ct-base coze_io_contract §1.2：skill_version 注入 query_meta（与 query_origin 同级，非顶层）──
        qm = self.query_meta if isinstance(self.query_meta, dict) else {}
        qm["skill_version"] = _skill_version()
        self.query_meta = qm
        # ── ct-base coze_io_contract §1.1：user_language（备用语言提示）注入顶层 params 子对象 ──
        user_language = resolve_user_language(self.original_question, None)
        payload = {
            "query_meta": self.query_meta,
            "original_question": self.original_question,
            "draft_answer": self.draft_answer,
            "conversation_history": self.conversation_history,
            "params": {"user_language": user_language},
        }
        if getattr(self, "doc_context", ""):
            payload["doc_context"] = self.doc_context
        if getattr(self, "scope_hint", ""):
            payload["scope_hint"] = self.scope_hint
        return payload
class Refiner(ABC):
    @abstractmethod
    def refine(self, req: RefineRequest, timeout: float = 90.0) -> str:
        """返回最终答案（服务器精校结果，或兜底回退的 draft_answer）。"""
        ...


class CozeRefiner(Refiner):
    """扣子服务器精校（唯一精校后端）：外发 3 变量，≤timeout 秒回收 final_answer；异常兜底草稿。

    超时策略（2026-08-16）：默认 timeout=90s；complex / 模板类 / 追问类问题放宽到 long_timeout
    （默认 300s）——服务端 full_analysis 完整输出模式（模板归纳 / 长文档生成）或结合多轮
    上下文的追问类问题耗时长，
    90s 会被提前截断。服务端 main.py TIMEOUT_SECONDS=900，不会先于客户端砍断，放宽安全。
    由 build_refiner() 始终实例化。
    """

    def __init__(self, endpoint: str, token_env: str = "CT_ADVISOR_COZE_TOKEN",
                 timeout: float = 90.0, long_timeout: float = 300.0,
                 answer_mode: str = "fast", race_window: float = 2.0):
        self.endpoint = endpoint
        self.token_env = token_env
        self.timeout = timeout
        # long_timeout：complex / 模板类 / 追问类问题的等待上限（默认 300s）；其余问题用 timeout（90s）。
        # 详见 _resolve_timeout() / _is_long_running()。
        self.long_timeout = long_timeout
        # answer_mode 已固定为 fast（2026-08-05 删除 precise）；按难度分流：
        #   simple/middle = race 竞速（早发 / 速度优先，详见 refine_fire_only + collect_race）：
        #     agent 在 step 2 后台调用 --fire-only（draft_answer 留空、difficulty/category/accuracy 未提供→补空串），
        #     Coze 用**完整** HTTP 超时独立分析 original_question（默认 90s；complex/模板类走 long_timeout=300s），
        #     成功后写入 race 缓存文件；agent 在 step 3 并行写本地草稿 + 调用 --collect
        #     [--wait race_window] 收集：缓存命中（Coze 在 step 3→step 4 间已返回）→ 采用 Coze
        #     （中断本地、Coze 胜出）；否则直接采用本地草稿（速度优先——本地秒级先出、Coze 实测
        #     9~25s 慢，常态本地胜出）。
        #   complex/vague = 串行：前台等待 Coze 完整返回（单次调用 refine()；复杂/模板类 timeout=long_timeout 默认300s，其余 90s），
        #     且必须把本地已生成的 draft_answer 一并发送（作为 Coze 参考）。
        self.answer_mode = "fast"  # 2026-08-05 删除 precise，仅保留 fast 单一模式
        self.race_window = race_window  # race 竞速：step 4 收集 Coze 后台结果的等待上限（秒）；超时即放弃、用本地

    # ------------------------------------------------------------------ #
    # 条件化超时（2026-08-16）：complex / 模板类 / 追问类问题等待上限放宽到 long_timeout
    # （默认 300s）；其余问题维持默认 timeout（90s）。复杂/模板类问题服务端
    # full_analysis 走完整输出模式、追问类需结合多轮上下文，生成/检索耗时长，
    # 90s 会被提前截断 → 放宽。服务端 main.py TIMEOUT_SECONDS=900，不会先于客户端砍断，放宽安全。
    # ------------------------------------------------------------------ #
    _TEMPLATE_TOKENS = ("template", "模板", "doc", "document", "规范", "spec")

    def _is_long_running(self, req: "RefineRequest") -> bool:
        """长任务判定：本地超时档位 long，或 category 命中模板类标记，或当前为类型 B 追问。

        长任务走服务端 full_analysis 完整输出模式（模板归纳 / 长文档生成），或需结合多轮
        上下文，生成/检索耗时长，需用 long_timeout（默认 300s）而非默认 90s。
        - is_followup == True：类型 B 追问（refine_answer.py 已基于本地 context_stitch 标记），
          多轮上下文导致 Coze 处理更久，直接等同长任务。
        - conversation_history 非空：当前问题处于多轮对话中（refine_answer.py 在有效期内
          有对话历史时打包进 req）。这是比纯文本 is_followup 更稳的追问信号——无文本盲区，
          覆盖「第一针/后续/补充」等承接句式漏判的情况，统一走 long_timeout。
        - difficulty 档位（2026-09-26 二值化）：
            * "forwarded" / "vague"（新契约，不含难度信息）→ 改由 route.timeout_tier()
              按问句原文判超时档位（CPLX 长耗时信号或长度 >= 80 字 → long）；
            * "complex"（旧 payload 兼容）→ 仍等同长任务。
        - category（str 或 list）小写后含模板类 token：模板/文档/规范类问题。
        """
        if getattr(req, "is_followup", False):
            return True
        # 多轮上下文（类型 B 追问的更稳信号）：只要有效对话历史被打包进 req，
        # 即代表当前问题处于多轮对话中（Coze 需结合前情处理，耗时更久）→ 等同长任务。
        if getattr(req, "conversation_history", None):
            return True
        meta = req.query_meta if isinstance(req.query_meta, dict) else {}
        diff = str(meta.get("difficulty", "")).strip().lower()
        if diff == "complex":       # 旧 payload 兼容：显式 complex 仍为长任务
            return True
        if diff != "complex":
            # 二值化新契约（forwarded/vague/空/旧 simple/middle）：difficulty 不携带
            # 有效难度信息 → 用 route.timeout_tier 按原文判超时档位
            try:
                from route import timeout_tier as _timeout_tier
                if _timeout_tier(getattr(req, "original_question", "") or "") == "long":
                    return True
            except Exception:  # noqa: BLE001  route 不可用时不阻断主流程，落到 category 判定
                pass
        cat = meta.get("category", "")
        if isinstance(cat, list):
            cat = " ".join(str(c) for c in cat)
        cat = str(cat).lower()
        return any(tok in cat for tok in self._TEMPLATE_TOKENS)

    def _resolve_timeout(self, req: "RefineRequest", timeout: Optional[float]) -> float:
        """解析本次 Coze 调用的有效超时：

        - 调用方显式传入 timeout → 优先采用（保留可覆盖旧行为）；
        - 否则长任务（complex / 模板类 / 追问类）→ long_timeout（默认 300s）；
        - 其余 → 默认 timeout（90s）。
        """
        if timeout is not None:
            return float(timeout)
        if self._is_long_running(req):
            return self.long_timeout
        return self.timeout

    def resolve_timeout(self, req: "RefineRequest", timeout: Optional[float] = None) -> float:
        """公开入口：出站前预知本次 Coze 调用的有效超时（秒）。

        供调用方（如 refine_answer.py 的回退消息 / 诊断日志）复用同一套条件化判定，
        避免在别处重复实现或硬编码超时值，导致与真实等待时长不符。
        """
        return self._resolve_timeout(req, timeout)

    def refine(self, req: RefineRequest, timeout: float = None) -> RefineResult:
        # 2026-10-15（C 方案）：requests 依赖已移除（urllib 传输），无需预检。
        timeout = self._resolve_timeout(req, timeout)
        # 全量直发（2026-08-14）：不再按难度分流，一律单次转发 Coze，返回结构化结果。
        # 兼容旧调用方：仍可通过 .final_answer 取文本；旧 fire-only/collect（race）保留不删。
        return self.refine_forward(req, timeout)

    def refine_fire_only(self, req: RefineRequest) -> str:
        """Race 早发模式（agent 在 step 3 调用，对应 SKILL.md step 3 Fire Gate）。

        与 ``refine()``（单发、draft 作兜底）不同，此方法：
          - 仅基于 ``original_question`` 独立分析 Coze
            （``draft_answer`` 留空不发送——调用方此时草稿尚未写出）；
          - HTTP 超时用 **完整** 时长（默认 90s；complex/模板类走 long_timeout=300s，不给 Coze 强加短帽，
            恢复 ops.md 文档意图）；
          - 成功后把 Coze 结果写入 race 缓存文件（供 step 4 ``--collect`` 读取）；
            超时 / 网络 / 解析异常返回**空串**且不写缓存——
            真正的兜底由 agent 在 step 4 用自己的本地草稿完成（此处不回退 draft，
            因为 step 3 时草稿为空，回退会得到空白答案）。

        agent 在 step 2 后台调用此法（run_in_background），step 3 并行写本地草稿 + 
        用 ``--collect`` 读取缓存：命中则 Coze 胜出、中断本地；否则用本地草稿（速度优先）。
        """
        # 2026-10-15（C 方案）：requests 依赖已移除（urllib 传输），无需预检。
        coze_req = copy.copy(req)
        coze_req.draft_answer = ""
        cache = self._race_cache_path(req)
        try:
            text = self._call_coze(coze_req, self._resolve_timeout(coze_req, None))
        except MissingDependencyError:
            raise  # 致命依赖错误，向上传播（urllib 传输下不会产生，防御性保留）
        except Exception as e:  # noqa: BLE001
            # race 语义：失败即返回空串、本地草稿胜出（设计内降级，不阻塞用户）；
            # 但仍发 ERR 信号留痕，避免「静默」到无法观测。
            code, _msg = _classify_outbound_error(e, proxy_attempted=_env_proxy_present())
            emit_err_signal(code or "ORCH_FAIL",
                            detail="fire-only %s: %s" % (type(e).__name__, e))
            return ""
        if text:
            try:
                cache.write_text(text, encoding="utf-8")
            except Exception:
                pass
        return text

    # ------------------------------------------------------------------ #
    # race 缓存（step 3 写、step 4 读）——仅缓存 Coze 的「结果」，非 payload
    # （payload 仍走 stdin heredoc 内存管道，遵循 ops.md 禁止落盘规则；此缓存是
    # fire/collect 双调用跨进程传递 Coze 结果的必要机制，属显式例外）。
    # ------------------------------------------------------------------ #
    @staticmethod
    def _race_cache_dir() -> "Path":
        from pathlib import Path as _P
        import time as _t
        d = _P(__file__).resolve().parent.parent / ".coze_race_cache"
        d.mkdir(parents=True, exist_ok=True)
        # 轻量清理：删除超过 60 分钟的陈旧缓存（race collect 在数秒内完成，旧文件无用）
        try:
            now = _t.time()
            for f in d.iterdir():
                if f.is_file() and now - f.stat().st_mtime > 3600:
                    try:
                        f.unlink()
                    except Exception:
                        pass
        except Exception:
            pass
        return d

    def _race_cache_path(self, req: RefineRequest) -> "Path":
        """按 original_question + query_meta 生成确定性缓存路径（同 payload 同路径）。"""
        key = hashlib.sha256(
            (req.original_question + "|"
             + json.dumps(req.query_meta, ensure_ascii=False, sort_keys=True)).encode("utf-8")
        ).hexdigest()[:24]
        return self._race_cache_dir() / f"{key}.txt"

    def collect_race(self, req: RefineRequest, wait: float = None) -> str:
        """Race 收集（agent 在 step 4 调用，对应 ``--collect``）。

        读取 step 3 ``refine_fire_only`` 写入的 race 缓存：
          - 缓存命中（Coze 已在 step 3→step 4 间返回）→ 返回 Coze 结果（Coze 胜出、中断本地）；
          - 未命中 → 至多轮询 ``wait`` 秒（默认 ``self.race_window``）；仍无结果 → 返回空串
            （本地草稿胜出，agent 直接 ship 本地、不空等 Coze）。
        """
        import time
        wait = self.race_window if wait is None else wait
        cache = self._race_cache_path(req)
        deadline = time.time() + max(0.0, wait)
        while True:
            if cache.exists():
                try:
                    return cache.read_text(encoding="utf-8")
                except Exception:
                    return ""
            if time.time() >= deadline:
                return ""
            time.sleep(0.1)

    def _call_coze(self, req: RefineRequest, timeout: float) -> RefineResult:
        """真正发起一次 Coze 调用；任何失败都向上抛（由调用方决定回退/退出）。

        返回结构化 RefineResult（2026-08-14 全量直发改造）：
          - 普通路径：final_answer = Coze 答案；need_tool = None
          - need_tool 路径：final_answer = Coze 草稿（缝合基底）；need_tool/params 填充
          - 缓存命中：cache_hit=True，final_answer=cached_answer

        传输层为 stdlib urllib（零第三方依赖，2026-10-15 起），无需 requests。
        """
        # 2026-10-15（C 方案）：传输层改 stdlib urllib，此处不再需要 requests
        # （漏删这行会在 requests 缺失时直接 ImportError，废掉整个 C 方案）。
        from .sanitize import sanitize

        # 保留 draft_answer 中的 <source skill="xxx"> 标签，原样发给 coze。
        # coze prompt 已配置为：识别 <source> 标签 → 跳过标记段落（不修改、不验证）。
        # sanitize() 只处理 PII（身份证/手机号/邮箱），不伤害 XML 标签。
        payload = sanitize(req.to_payload())  # 出站前脱敏（ct-base §11）
        # token 解析：统一从 adapters/coze_token_embedded.py 内嵌 obfuscated blob 取（XOR+base64 公开凭据，无参 get_token()）
        token = get_token()
        _headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        # ── 出站传输层（2026-10-15 C 方案：stdlib urllib，零第三方依赖） ──
        # urllib 默认 opener 经 ProxyHandler(getproxies()) 读取环境变量代理
        # （HTTP(S)_PROXY，大小写不敏感归一）；HTTPS 经 http 代理时自动走 CONNECT
        # 隧道——本机实测：经系统代理 POST 本端点返回 200。
        # 重试顺序（与 requests 版语义一致）：
        #   1) 检测到系统代理 env → 先走系统代理（默认 opener，等价 proxies=None）；
        #   2) 仅「连接阶段」失败（URLError / OSError：代理不可达、DNS、连接被拒）
        #      才回退强制直连重试一次（ProxyHandler({}) 空代理表）；
        #   3) 超时（TimeoutError）不重试：无论哪条路径，Coze 多半已收到请求，
        #      重试只会造成重复发送；
        #   4) HTTPError（4xx/5xx）是服务端响应而非连接问题：跳出循环单独处理。
        import urllib.error as _urlerr
        import urllib.request as _urlreq

        _env_proxy = _env_proxy_present()
        _try_orders = (
            [("system-proxy", None), ("direct", "direct")]
            if _env_proxy else
            [("direct", "direct")]
        )
        _body = json.dumps(payload).encode("utf-8")
        _resp_raw = None        # 成功响应体（bytes）
        _http_error = None      # 非 2xx：urllib.error.HTTPError（本身也是响应对象）
        _last_exc = None
        for _label, _proxies in _try_orders:
            # None → 默认 opener（读 env 代理）；"direct" → 空 ProxyHandler 强制直连
            _opener = (_urlreq.build_opener() if _proxies is None
                       else _urlreq.build_opener(_urlreq.ProxyHandler({})))
            _request = _urlreq.Request(
                self.endpoint, data=_body, method="POST", headers=dict(_headers)
            )
            try:
                with _opener.open(_request, timeout=timeout) as _r:
                    _resp_raw = _r.read()
                break
            except _urlerr.HTTPError as _e:
                # 服务端有响应（401/5xx 等）：不是连接问题，跳出重试循环
                _http_error = _e
                break
            except (socket.timeout, TimeoutError):
                # 超时：Coze 很可能已收到请求，重试只会造成重复发送，直接上抛
                raise
            except (_urlerr.URLError, OSError) as _e:
                # 连接阶段失败（代理不可达 / DNS / 连接被拒）→ 尝试下一路径
                _last_exc = _e
                try:
                    sys.stderr.write(
                        f"[ct-advisor] {_label} 连接失败({type(_e).__name__})，尝试下一路径...\n"
                    )
                except Exception:  # noqa: BLE001
                    pass
                continue
        if _resp_raw is None and _http_error is None:
            # 所有可用路径均连接失败 → 上抛最后一次异常，交由上层兜底
            raise _last_exc if _last_exc is not None else RuntimeError("all outbound paths failed")
        # 显式暴露鉴权/服务错误：4xx/5xx 不应被上层 except 静默成「超时/没发」
        # （2026-08-08 加固：此前 TypeError 被静默吞掉，误判为未发送）
        if _http_error is not None:
            if _http_error.code == 401:
                try:
                    sys.stderr.write(t("error.coze_401") + "\n")
                except Exception:
                    pass
            # 上抛由 _classify_outbound_error 分类为 AUTH_401 / COZE_HTTP_ERROR
            raise _http_error
        data = json.loads(_resp_raw.decode("utf-8"))
        # 全量直发（2026-08-14）：解析结构化返回，透出 need_tool 分支
        # 兼容（2026-09-09）：新版 Coze 工作流返回顶层 `final_answer`；老版本仍返回 `answer`。
        # 两 key 都认（final_answer 优先），任一命中即采用，都不命中才回退本地草稿。
        final = data.get("final_answer") or data.get("answer") or req.draft_answer
        # 2026-11-10（v1.63）：响应顶层 `complexity_hint` 是云端「复杂混合调用」的
        # **布尔标记**（结构化元数据；v1.62 曾为提示文案，已撤销），此处刻意不解析、
        # 不渲染、不塞进 final_answer。用户可见的安全提示
        # 由本地 entry.py 唯一出口基于 route_tool 零联网预判生成（调用前 stderr 预警
        # + 答案最前前置），并在出口做去重剥离；双端各自渲染会导致用户看到两次。
        # 云端多技能命中：need_tools / deferred_tools 两种键都认；可能是 JSON 字符串，
        # 也可能是列表。任何异常形态一律安全降级为空列表（不影响主判 need_tool）。
        _nt = data.get("need_tools") or data.get("deferred_tools") or []
        if isinstance(_nt, str):
            try:
                _nt = json.loads(_nt)
            except Exception:  # noqa: BLE001
                _nt = []
        if not isinstance(_nt, list):
            _nt = []
        result = RefineResult(
            final_answer=strip_display_tags(final),
            cached_answer=data.get("cached_answer") or "",
            cache_hit=bool(data.get("cache_hit", False)),
            need_tool=data.get("need_tool") or None,
            params=data.get("params") or {},
            run_id=str(data.get("run_id") or ""),
            need_tools=[str(x) for x in _nt if x],
        )
        # §20.15：顶层可选 message 字段（Coze 业务侧表面提示），本地置顶渲染 banner
        result.message = _normalize_coze_message(data.get("message"))
        # 2026-11-11 v1.68：解析云端端点版本（出参侧）。缺失时本地兜底提醒——
        # 云端过旧 / 响应契约不匹配时，本地技能可能与云端对接异常，提示升级或改用 Web 应用。
        result.coze_version = str(data.get("coze_version") or "")
        # 2026-11-11 v1.68 增强：返回结构对接校验（「对接不匹配」检测）。
        _struct_mismatch = _check_struct_mismatch(data)
        if (not result.coze_version and result.message is None
                and (result.final_answer or result.need_tool)):
            result.message = {
                "level": "warning",
                "text": (
                    "⚠️ 未获取到云端版本信息，当前技能与云端可能存在对接差异。\n"
                    "建议升级 ct-advisor 技能到最新版；或直接使用 Web 应用 "
                    "ct.medstatstar.com 获得完整体验。"
                ),
                "dismissible": True,
            }
        elif _struct_mismatch and result.message is None:
            result.message = {
                "level": "warning",
                "text": (
                    "⚠️ 检测到云端返回结构与当前技能版本可能不匹配（关键字段缺失）。\n"
                    "建议升级 ct-advisor 技能到最新版；或直接使用 Web 应用 "
                    "ct.medstatstar.com 获得完整体验。"
                ),
                "dismissible": True,
            }
        return result

    def refine_forward(self, req: RefineRequest, timeout: float = None) -> RefineResult:
        """全量直发主链路（2026-08-14）：单次调用 Coze，返回结构化结果。

        与旧 serial 的差异：
          - 不做难度分流（所有问题一律直发，difficulty 由本地 normalize 兜底 complex）；
          - 返回 RefineResult（可透出 need_tool 执行卡）而非纯文本；
          - 失败/超时仍回退（final_answer=req.draft_answer），由调用方判定走本地兜底。

        本地大模型原则上不回答——本方法只负责「转发 + 结果结构化」，不生成草稿。
        """
        # 2026-10-15（C 方案）：requests 依赖已移除（urllib 传输），无需预检。
        timeout = self._resolve_timeout(req, timeout)
        try:
            return self._call_coze(req, timeout)
        except MissingDependencyError:
            raise  # 致命依赖错误，向上传播（urllib 传输下不会产生，防御性保留）
        except Exception as e:  # noqa: BLE001
            self._log_fallback(e, timeout)
            res = RefineResult(final_answer=req.draft_answer, need_tool=None)
            # 出站失败双通道透出（2026-10-15 B 方案）：机器错误码经 emit_err_signal
            # 发 stderr [ct-advisor][ERR] 信号；人读提示挂 res.connection_error
            # （网络/超时类）或 res.internal_error（其余），交由 build_output 渲染。
            # 两类都绝不静默，均不再伪装成「返回为空，请稍后重试」。
            code, msg = _classify_outbound_error(e, proxy_attempted=_env_proxy_present())
            if msg:
                res.connection_error = msg
            if code:
                emit_err_signal(code, detail="%s: %s" % (type(e).__name__, e))
            else:
                emit_err_signal("ORCH_FAIL", detail="%s: %s" % (type(e).__name__, e))
                res.internal_error = _internal_error_msg(e)
            return res

    def _refine_serial(self, req: RefineRequest, timeout: float) -> RefineResult:
        """⚠️ 已废弃（2026-08-14 全量直发改造）：保留仅为旧调用方兼容，返回 RefineResult。

        串行路径（serial）：前台串行等待 Coze 完整返回（直到 timeout）；超时/失败才回退草稿。
        """
        try:
            return self._call_coze(req, timeout)
        except MissingDependencyError:
            raise  # 致命依赖错误，向上传播（urllib 传输下不会产生，防御性保留）
        except Exception as e:  # noqa: BLE001
            self._log_fallback(e, timeout)
            res = RefineResult(final_answer=req.draft_answer, need_tool=None)
            # 出站失败双通道透出（2026-10-15 B 方案）：机器错误码经 emit_err_signal
            # 发 stderr [ct-advisor][ERR] 信号；人读提示挂 res.connection_error
            # （网络/超时类）或 res.internal_error（其余），交由 build_output 渲染。
            # 两类都绝不静默，均不再伪装成「返回为空，请稍后重试」。
            code, msg = _classify_outbound_error(e, proxy_attempted=_env_proxy_present())
            if msg:
                res.connection_error = msg
            if code:
                emit_err_signal(code, detail="%s: %s" % (type(e).__name__, e))
            else:
                emit_err_signal("ORCH_FAIL", detail="%s: %s" % (type(e).__name__, e))
                res.internal_error = _internal_error_msg(e)
            return res

    @staticmethod
    def _log_fallback(exc: Exception, timeout: float) -> None:
        """回退日志：仅打印异常类型与超时窗口，绝不输出 token / payload / draft 内容。"""
        try:
            sys.stderr.write(
                t("error.fallback_local", reason=type(exc).__name__, timeout=timeout) + "\n"
            )
        except Exception:
            pass
