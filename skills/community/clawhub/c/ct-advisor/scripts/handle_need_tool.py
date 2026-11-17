# -*- coding: utf-8 -*-
"""need_tool 执行卡 → 本地技能执行器（2026-08-14）

方案：Coze 单次调用。Coze 返回 need_tool 执行卡（技能 + 参数 + Coze 答案草稿），
本脚本机械执行对应本地技能 CLI，产出结构化结果；本地大模型以 draft_answer 为基底
缝合技能结果组织最终答案，**不回发 Coze**。

用法（供本地 agent 调用）：
    python handle_need_tool.py --card '<执行卡 JSON>'

执行卡 JSON（与 Coze GraphOutput need_tool 分支一致）：
    {
      "need_tool": "ct-registry",
      "params": {"cond": "...", "max": 20},
      "draft_answer": "Coze 原始答案草稿",
      "run_id": "..."
    }

输出（stdout，JSON）：
    {
      "tool": "ct-registry",
      "status": "ok" | "error" | "need_params",
      "result": <结构化结果（技能主产物 JSON/文本）>,
      "draft_answer": "<Coze 草稿，供缝合>",
      "elapsed_sec": 12.3
    }

status 语义：
    ok             技能执行成功，result 为结构化结果
    install_required  A 档技能（已上架）未安装 → 结构化上报**安装建议**
                    （github / install_hint / install_command / missing）。默认
                    `install_mode="suggest"`：**只建议、不执行** —— 把用途与命令交给用户，
                    由用户自行执行，或用户**明确授权**后在卡片带 install_consent="approved"
                    重跑（→ `install_mode="authorized"`，方可将命令交给 agent 代为执行）。
                    用户拒绝 → 卡片带 install_consent="declined" 重跑，走 local_fallback。
                    🔴 安装动作（下载 + 写入技能目录）可能触发本机安全提示，故一律以
                    「建议安装」为默认姿态，绝不自动安装（ct-base §5 禁止静默安装 +
                    2026-09-10 用户要求：安装可能触发安全警告，改为建议 / 明确授权后再装）
    local_fallback  用户拒绝安装（或明确不取数）→ 以自身能力作答，缝合层标注「未取数」
    unpublished_a   A 档技能（输入非涉密）未在 SkillHub 上架**且本机未注册** →
                    提示后以自身能力作答并标注「未取数」，无需征询安装授权。
                    2026-11-09 起：本机已注册的技能一律走 handoff，不进此门
    unreleased_b    B 档技能（输入涉密）或技能未登记，且**本机未注册** →
                    说明「不经公共市场分发 / 本机未注册」后以自身能力作答，
                    不尝试安装、不硬错（2026-11-09 口径）
    referral        referral-only 技能（如 meta-analysis）→ 引导用户显式 @skill 调用
    handoff         2026-11-09 新增（默认主路径）：技能已在本机注册、客户端可直接调用，
                    不再由 ct-advisor 代跑 CLI；返回结构化 @skill:<slug> 卡片
                    （含已识别参数 / 缺失参数 / 交付物说明 / B 档保密提醒），
                    由代码缝合进答案，用户/客户端据此直接调用技能本体。
                    CT_ADVISOR_HANDOFF=0 可整条关回原执行卡（红线 2 兜底）。
    error           技能执行失败（rc/超时/脚本缺失），回退 Coze 草稿
    need_params     执行卡参数不完整（如缺效应量），result.missing 列出缺失项，
                    由本地大模型向用户追问（不编造），补齐后重发执行卡
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

# ── Windows 子进程无控制台窗口（2026-10-15）─────────────────────────────────
# 本地技能 CLI（python.exe 等）是控制台子系统程序：父进程自身没有控制台时
# （如 WorkBuddy 桌面端宿主直接拉起本脚本），子进程会让 Windows 新建控制台
# → 屏幕闪出前台弹窗。CREATE_NO_WINDOW（+ STARTF_USESHOWWINDOW / SW_HIDE
# 双保险）令子进程完全后台运行；capture_output 管道捕获不受影响。
_CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)


def _hidden_kwargs() -> dict:
    """返回抑制控制台弹窗的 subprocess 关键字参数（非 Windows 平台返回 {}）。"""
    if not sys.platform.startswith("win"):
        return {}
    kw = {"creationflags": _CREATE_NO_WINDOW}
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 0  # SW_HIDE
        kw["startupinfo"] = si
    except Exception:
        pass
    return kw

# 技能根目录（WorkBuddy skills 目录），可用环境变量覆盖
SKILLS_DIR = os.environ.get(
    "CT_SKILLS_DIR",
    str(Path.home() / ".workbuddy" / "skills"),
)
# 映射表路径（本文件同目录）
MAPPING_PATH = Path(__file__).resolve().parent / "tool_mapping.json"
# 执行卡产物根目录（2026-08-23）：各技能默认把 out/ 写到**进程 cwd**，
# 此前 cwd = scripts/ → 产物污染脚本目录（实测 scripts/out/report.xlsx 等）。
# 改为按技能隔离到 ct-advisor/out/cards/<tool>/。
CARDS_ROOT = Path(__file__).resolve().parent.parent / "out" / "cards"

# stdout 噪声行（内联图 / 组件标记）：ct-samplesize 单次可输出数万字符 SVG，
# 直接进 result 会挤爆缝合层上下文 → 剥离并以占位符替代。
NOISE_PREFIXES = ("__SVG_WIDGET__", "__FIGURE__", "__HTML_WIDGET__")
MAX_RESULT_CHARS = 4000


def _load_mapping() -> dict:
    with open(MAPPING_PATH, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# A/B 档门控（2026-09-10）
#
# 权威口径 = ct-base §11（唯一分类轴 input_sensitivity）+ §13.1（保密声明）：
#   A 档 = 输入非涉密 → 可检测安装、**建议安装**（用户自行执行或明确授权后代办），
#                          安装完成后执行（前提：已发布）
#   B 档 = 输入涉密   → 本机未注册时提示「不经公共市场分发 / 本机未注册」，本地作答
#                        （2026-11-09：本机已注册则走 handoff，不再进档位门）
#
# 发布状态（tiers.registry[*].published）的权威判据 = **SkillHub 上架**，不是 GitHub
# ——GitHub 空占位仓库同样返回 HTTP 200（ct-pipeline 事故），复核用
# `python adapters/probe_publication.py`。故 A 档需再分两支：
#   已发布   → install_required（**建议安装**：默认 install_mode=suggest 只建议不代办；
#              用户明确授权（install_consent=approved）后才转 authorized 由 agent 代办）
#   未发布   → unpublished_a（不可安装，不给地址，直接本地作答 + 未取数标注）
#
# 🔴 本模块只做「检测 + 上报」，**绝不执行安装**：ct-base §5「禁止静默安装」红线要求
# 安装动作必须由 agent 在拿到用户**明确授权**后执行，非交互模式直接报错退出、不得阻塞。
# 2026-09-10 追加口径（用户要求）：安装需下载并写入本地技能目录，**可能触发本机安全警告**，
# 故默认姿态是「**建议安装**」——把用途与命令交给用户自行执行；仅当用户在卡片给出
# 明确授权词（install_consent ∈ _APPROVE_WORDS）时，install_mode 才转为 "authorized"。
# 因此 install_required 只是一个结构化请求，安装由调用方（agent）在授权后完成。
# ---------------------------------------------------------------------------


def _resolve_tier(mapping: dict, tool: str) -> dict:
    """解析技能的 A/B 档与发布状态；未登记技能按 default_tier（B）保守处理。

    返回 {tier, published, github, purpose, registered}。
    未登记 → tier 取 tiers.default_tier（默认 B）：不尝试安装未知技能，也不硬错卡死应答。

    2026-11-09：published 只描述「是否在 SkillHub 上架」这一**分发状态**，
    不再是「能否调用」的判据——本机可得性由 _client_callable() 判定，本函数
    仍负责 tier（涉密边界）与用途文案。
    """
    tiers = mapping.get("tiers") or {}
    entry = (tiers.get("registry") or {}).get(tool)
    if isinstance(entry, dict):
        return {
            "tier": entry.get("tier", "B"),
            "published": bool(entry.get("published")),
            "github": entry.get("github") or f"https://github.com/medstatstar/{tool}",
            "purpose": entry.get("purpose", ""),
            "registered": True,
        }
    return {
        "tier": tiers.get("default_tier", "B"),
        "published": False,
        "github": f"https://github.com/medstatstar/{tool}",
        "purpose": "",
        "registered": False,
    }


def _skill_installed(tool_cfg: dict) -> bool:
    """探测技能主脚本是否已落盘（{SKILLS_DIR} 展开后判定，不执行、不联网）。

    这是 install_required 分支的唯一判据：脚本在 → 直接执行；脚本不在 → 上报待安装。
    比「跑一次再看 rc」更早、更便宜，也不会把「未安装」伪装成「执行失败」。
    """
    for arg in (tool_cfg.get("args") or []):
        cand = arg.replace("{SKILLS_DIR}", SKILLS_DIR)
        if cand.endswith(".py"):
            return Path(cand).is_file()
    # 无 .py 入口（异常配置）：回退到整条 args 的末项存在性
    args = tool_cfg.get("args") or []
    if not args:
        return False
    return Path(args[-1].replace("{SKILLS_DIR}", SKILLS_DIR)).is_file()


# ---------------------------------------------------------------------------
# 客户端直调 handoff（2026-11-09 · 用户裁定：客户端已可直接调用兄弟技能）
#
# 背景：2026-09-10 的档位门以「SkillHub 上架 / 本地 CLI 脚本存在」为可得性
# 判据，B 档与未上架 A 档一律回 unreleased_b / unpublished_a（"不对外发布、
# 无法通过安装获取"）。2026-11-09 客户端已能直接调用本机注册的全部 ct-* 技能
# （sibling_registry.json 实测 22/22 installed=true），上述文案变成事实性错误；
# 且「advisor 代跑 CLI → 纯文本摘要」会把用户挡在技能本体的完整交付物之外。
#
# 新姿态：**handoff 优先**。已在本机注册的技能不再由 ct-advisor 代跑，改由代码
# 产出结构化 @skill:<slug> 卡片（含已识别参数 / 缺失参数 / 交付物 / 保密提醒），
# 用户/客户端据此直接调用技能本体，走完整 SAFE PREVIEW 与文件交付流程。
#
# 🔴 HARD GATE 不变：卡片由代码生成并经 entry.py 单一出口输出，本地 LLM 仍不得
#    自主决定调用哪个技能、不得追加或改写答案（SKILL.md §HARD GATE）。
# 🔴 红线 2 不变：CT_ADVISOR_HANDOFF=0 可整条关回原执行卡（engine=local 兜底）。
# 🔴 B 档涉密边界不变：能调用 ≠ 可把方案 / 受试者数据送往公共检索端点。
# 🔴 published（SkillHub 上架）降级为「分发状态」，不再是「能否调用」的判据。
# ---------------------------------------------------------------------------

HANDOFF_ENV = "CT_ADVISOR_HANDOFF"
_HANDOFF_OFF_VALUES = {"0", "false", "no", "off"}
SIBLING_REGISTRY_PATH = Path(__file__).resolve().parent / "sibling_registry.json"

# 技能本体可产出的交付物（仅用于 handoff 卡片说明；ct-advisor 不声称能产出文件）
_HANDOFF_DELIVERABLES = {
    "ct-registry": "report.xlsx / report.md（试验格局 + 竞品分布）",
    "ct-safety": "faers_report.xlsx / faers_report.md（PRR / ROR / IC / EBGM + 95%CI）",
    "ct-literature": "lit_report.xlsx / references_apa.md（PICO 检索 + PRISMA）",
    "ct-samplesize": "样本量与效能报告（含内联图）",
    "ct-protocol": "结构化评阅报告（U1–U12 / D1–D9）+ 批注版方案",
    "ct-csr": "ICH E3 / NMPA 双模板 CSR",
    "ct-sdtm": "SDTM 数据集 + Define-XML",
    "ct-adam": "ADaM 数据集",
    "ct-analysis": "ARD 结构化分析结果",
    "ct-tlf": "Tables / Listings / Figures（含 KM / forest 图）",
    "ct-statrev": "独立统计审阅报告",
    "ct-datacheck": "数据质控规则报告（DC.001–DC.xxx）",
    "ct-eligibility": "入组匹配结果",
    "ct-ecrf": "eCRF 设计规格",
    "ct-submission": "CTD / eCTD 申报包",
    "ct-congress": "会议摘要结构化疗效 / 安全性表",
    "ct-pipeline": "公开情报监测编排结果",
    "ct-synthdata": "合成 SDTM / ADaM 测试数据集",
    "meta-analysis": "Meta 分析全套结果与图表",
}


def _handoff_enabled() -> bool:
    """handoff 为默认主路径；显式 off 值可整条关闭（回落原执行卡）。"""
    return os.environ.get(HANDOFF_ENV, "").strip().lower() not in _HANDOFF_OFF_VALUES


def _client_callable(tool: str) -> bool:
    """技能是否已在本机注册、客户端可直接调用（纯本地探测，不联网、不执行技能）。

    双判据任一成立即可：① <SKILLS_DIR>/<tool>/SKILL.md 落盘（客户端注册表形态）；
    ② scripts/sibling_registry.json 中 installed=true（discover_siblings 扫描结果）。
    两者都不成立才回落到 2026-09-10 的档位门 / 安装门控。
    """
    if not tool:
        return False
    try:
        if (Path(SKILLS_DIR) / str(tool) / "SKILL.md").is_file():
            return True
    except OSError:
        pass
    try:
        with open(SIBLING_REGISTRY_PATH, encoding="utf-8") as _f:
            _info = (json.load(_f).get("skills") or {}).get(tool) or {}
        return bool(_info.get("installed"))
    except Exception:  # noqa: BLE001 - 注册表缺失/损坏不得卡死主链路
        return False


def _handoff_result(tool: str, params: dict, missing: list, tier_info: dict,
                    tool_cfg: dict, deferred: list, deferred_note: str,
                    draft: str) -> dict:
    """构造结构化 handoff 结果（纯代码，无 LLM，无网络）。"""
    clean = {k: v for k, v in (params or {}).items()
             if v not in (None, "", [], {})}
    # 混合执行卡的 params 可能混着其它技能的参数（如 topic 属于 ct-literature）。
    # 主卡片必须按**主技能自己的** CLI 白名单过滤，否则客户端拿去调用会
    # argparse 报 unrecognized arguments（2026-11-09 三源竞品实测发现）。
    allowed = set(((tool_cfg or {}).get("params") or {}).keys())
    if allowed:
        clean = {k: v for k, v in clean.items() if k in allowed}
    tier = tier_info.get("tier", "B")
    purpose = tier_info.get("purpose") or (tool_cfg or {}).get("prep_hint") or ""
    return {
        "tool": tool,
        "status": "handoff",
        "result": {
            "mention": "@skill:%s" % tool,
            "params": clean,
            "missing": list(missing or []),
            "purpose": purpose,
            "deliverables": _HANDOFF_DELIVERABLES.get(tool, ""),
            "tier": tier,
            "confidential": tier != "A",
            "locally_available": True,
        },
        "draft_answer": draft,
        "deferred_tools": deferred,
        "deferred_note": deferred_note,
        "elapsed_sec": 0,
        "mode": "client_handoff",
    }


# 用户拒绝安装的确认词（卡片 install_consent 字段，大小写不敏感）
_DECLINE_WORDS = {"declined", "decline", "refused", "refuse", "rejected", "reject", "no", "false"}
# 用户**明确授权**安装的确认词（2026-09-10）：只有显式命中这里，install_mode 才转为
# "authorized"（可由 agent 代为执行安装）。缺省 / 含糊表态一律按 "suggest"（只建议）。
_APPROVE_WORDS = {"approved", "approve", "authorized", "authorised", "authorize", "authorise",
                  "consent", "granted", "yes", "ok", "agree", "agreed", "true"}


def _skillhub_cli(mapping: dict) -> Path | None:
    """定位可用的 SkillHub CLI 脚本。

    顺序：环境变量 SKILLHUB_CLI → tiers.install.cli_candidates 中**优先含
    `--skip-self-upgrade` 的完整版**，无则退回首个存在者。返回 None 表示本机
    无可用 CLI —— 此时不编造安装命令，只给人工说明。

    为何要挑版本（2026-09-10 实测）：本机并存两份不同构建。
      · 完整版 v2026.8.5（226KB）：`--skip-self-upgrade` 存在，走公网
        api.skillhub.cn，安装成功；
      · 精简版 v2026.3.6（44KB）：无该 flag，其索引/下载端点指向内网 LB
        （http://lb-*.clb.gz-tencentclb.com），实测下载得到非 zip →
        "Downloaded file is not a valid zip archive"，**装不了**。
    故按 flag 探测挑完整版，避免把命令生成到装不了的 CLI 上。
    """
    env = os.environ.get("SKILLHUB_CLI")
    if env:
        p = Path(env)
        return p if p.is_file() else None
    cands = ((mapping.get("tiers") or {}).get("install") or {}).get("cli_candidates") or []
    existing = [p for p in (Path(os.path.expanduser(c)) for c in cands) if p.is_file()]
    for p in existing:
        if _cli_has_flag(p, "--skip-self-upgrade"):
            return p
    return existing[0] if existing else None


def _cli_has_flag(cli: Path, flag: str) -> bool:
    """离线探测 CLI 是否支持某 flag（读源码字符串，不执行子进程）。"""
    try:
        return flag in cli.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False


def _helper_path() -> Path | None:
    r"""定位 install_sibling.py，**刻意避开 UNC 形态的路径**。

    坑（2026-09-10 实测两次踩到）：本机技能目录是软链到网络盘的，Windows 上
    `os.getcwd()` 返回的已是解析后的真实路径，因此 `os.path.abspath(__file__)`
    仍会得到 UNC 形态。而该形态写进命令串经 bash 传递会被二次拼接（盘符段重复），
    Python 报 "can't open file"。

    故按「用户态规范路径 → 解析路径」顺序探测，取首个存在者；绝不主动构造 UNC。
    """
    cands = [
        Path.home() / ".workbuddy" / "skills" / "ct-advisor" / "adapters" / "install_sibling.py",
        Path(os.path.abspath(__file__)).parent.parent / "adapters" / "install_sibling.py",
    ]
    for p in cands:
        try:
            if p.is_file():
                return p
        except OSError:
            continue
    return None


def _install_command(mapping: dict, tool: str) -> str:
    """生成**实测可用**的安装命令（2026-09-10）。

    首选本技能自带的 install_sibling.py：它先核验 SkillHub 上架状态、再下载解压，
    以纯参数方式落盘，从而规避三条已实测的坑（见 install_sibling.py 模块 docstring）：
      · PATH 中无 `skillhub` 命令（裸命令必失败）；
      · 本机 ~/.skillhub 的 CLI 是精简版 v2026.3.6，下载端点指内网 LB 返回非 zip；
      · 完整版 CLI 在网络盘，其 UNC 形态路径经 bash 传递会被二次拼接而打不开。

    路径一律输出**正斜杠**形式（`as_posix()`）：Windows 上 Python 接受正斜杠，
    而 bash/Git-Bash 不会对其做盘符或 UNC 改写。

    找不到 install_sibling.py 时退回 SkillHub CLI（仍显式带 --dir；--skip-self-upgrade
    仅在所挑 CLI 支持时添加）。两者都不可用则返回空串（不编造命令）。
    """
    helper = _helper_path()
    # --dir 同样输出正斜杠：默认 SKILLS_DIR 在 Windows 上是 `C:\Users\...` 形态，
    # 反斜杠嵌进 shell 命令串会被当成转义符吃掉（bash 下 `\U`/`\A` 等直接消失）。
    dir_arg = Path(SKILLS_DIR).as_posix()
    if helper is not None:
        hp = helper.as_posix()
        if not hp.startswith("//"):  # UNC 形态一律不出厂
            return f'"{sys.executable}" "{hp}" {tool} --dir "{dir_arg}"'
    cli = _skillhub_cli(mapping)
    if cli is None:
        return ""
    cp = cli.as_posix()
    if cp.startswith("//"):
        return ""
    skip = " --skip-self-upgrade" if _cli_has_flag(cli, "--skip-self-upgrade") else ""
    return (f'"{sys.executable}" "{cp}"{skip} --dir "{dir_arg}" '
            f'install {tool}')


def _skillhub_id(mapping: dict, tool: str) -> str:
    """SkillHub 的 canonicalName（@handle/<slug>），供用户按名搜索。核不到 handle 则返回 slug。"""
    handle = ((mapping.get("tiers") or {}).get("install") or {}).get("namespace")
    return f"@{handle}/{tool}" if handle else tool


# 调用方语言透传（F3, 2026-09-03）：ct-base language_policy.md §"user_language 备用入参"
# 规定 coze 计算端经环境变量 CTSS_LOCALE 接收调用方语言（zh/en）。ct-advisor 作为调用方，
# 按【用户输入文本】内容级检测语言（与系统 locale 解耦，避免中文系统 + 英文输入误判 zh），
# 经 CTSS_LOCALE 透传给兄弟技能（ct-samplesize v5 coze 引擎据此切 coze 端报告 / 图表语言）。
# 算法与 ct-base/scripts/i18n.py::detect_text_language 一致，本地自包含（避免跨技能 import）。
_CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3000-\u303f\uff00-\uffef]")


def detect_text_language(text):
    """内容级语言检测：含 CJK → zh，纯英文 → en，空 → None。"""
    if not text or not text.strip():
        return None
    letters = re.sub(r"\s+", "", text)
    if not letters:
        return None
    cjk = len(_CJK_RE.findall(text))
    if cjk == 0:
        return "en"
    ratio = cjk / len(letters)
    return "zh" if (ratio >= 0.05 or cjk >= 2) else "en"


def _resolve_call_locale(card: dict, question: str) -> str:
    """调用方语言：卡片显式 locale > 问题内容级检测 > 中文默认（ct-base 运行期默认 zh）。"""
    loc = (card.get("locale") or "").strip().lower()
    if loc:
        if loc.startswith("zh") or loc in ("chinese", "中文", "cn"):
            return "zh"
        if loc.startswith("en") or loc in ("english", "英语"):
            return "en"
    det = detect_text_language(question)
    return det or "zh"


def _sanitize_result(result):
    """剥离内联图/组件噪声块并限长（仅对文本兜底结果生效）。

    2026-08-23 修正：首版只按行前缀过滤，但 `__SVG_WIDGET__` 是**多行块**
    （标记只在首行，后续 <svg>/<g>/<path> 上万行不带前缀）→ SVG 仍整块进 result。
    改为状态机：命中标记后丢弃其余所有行（内联图恒在数值输出之后）。
    """
    if not isinstance(result, str):
        return result
    kept, figures = [], []
    for line in result.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(NOISE_PREFIXES):
            figures.append(stripped.split()[0].strip("_"))
            if stripped.startswith("__SVG_WIDGET__") or stripped.startswith("__HTML_WIDGET__"):
                break  # 多行组件块：其后全部丢弃
            continue
        kept.append(line)
    text = "\n".join(kept).strip()
    if figures:
        text += f"\n[已剥离 {len(figures)} 个内联图形块（{'/'.join(sorted(set(figures)))}）：图形不参与文字缝合]"
    if len(text) > MAX_RESULT_CHARS:
        text = text[:MAX_RESULT_CHARS] + f"\n…[截断，原长 {len(result)} 字符]"
    return text


def _read_artifacts(tool_cfg: dict, workdir: Path) -> dict:
    """回读技能产物文件（stdout 无结构化数值时的唯一数据来源）。

    2026-08-23 实测：WorkBuddy 沙箱会把技能写出的 .md/.json 重定向到
    `<out>/_unsaved/` 子目录（.xlsx/.html 不受影响）。因此每个候选文件都要
    在 out/、out/_unsaved/ 两处 + 递归兜底里找，否则回读恒为空。
    """
    names = tool_cfg.get("result_files") or []
    if not names:
        return {}
    arts = {}
    for name in names:
        hit = None
        for cand in (workdir / "out" / name,
                     workdir / "out" / "_unsaved" / name,
                     workdir / name):
            if cand.is_file():
                hit = cand
                break
        if hit is None:
            matches = sorted(workdir.rglob(name))
            hit = matches[0] if matches else None
        if hit is None:
            continue
        # 路径白名单：仅回读解析后仍在 workdir 之内（含 _unsaved）的产物，
        # 抵御 result_files 含 ../ 的路径逃逸。
        try:
            hit.resolve().relative_to(workdir.resolve())
        except ValueError:
            continue
        try:
            raw = hit.read_text(encoding="utf-8", errors="replace")
        except Exception as e:  # noqa: BLE001
            arts[name] = f"[读取失败: {e}]"
            continue
        if hit.suffix == ".json":
            try:
                arts[name] = json.loads(raw)
                continue
            except Exception:
                pass
        arts[name] = raw[:MAX_RESULT_CHARS]
    return arts


def _build_deferred(mapping: dict, primary: str, need_tools,
                    card_params: dict | None = None) -> list:
    """多技能命中 → 主判出 handoff 卡片，其余各自生成**可直接调用的 @skill 卡片数据**。

    需求（2026-08-23）：一次提问可能同时命中试验格局/信号/文献/样本量，全部串行执行会
    叠加数分钟联网耗时且参数多半不全，故只把最关键的一个作为主判。

    2026-11-09：客户端已可直接调用本机注册技能，deferred **不再只是「请先准备数据」
    的文字提示**——混合跨技能问题若只在答案里给出主技能卡片，其余技能就彻底丢失了
    （test_cross_skill_handoff.py 的 B 组 8 条曾全部 FAIL）。此处改为带 mention /
    已识别参数 / 缺失参数 / 交付物 / 保密等级的结构化数据，由
    refine_answer._render_deferred_cards 渲染进答案，让每个技能都能被客户端直接调用。
    """
    deferred = []
    card_params = card_params or {}
    for t in (need_tools or []):
        if t == primary or not t:
            continue
        cfg = mapping["skills"].get(t) or {}
        ref = (mapping.get("referrals") or {}).get(t)
        if ref:
            prep_hint = ref.get("mention", f"@skill:{t}") + "（" + ref.get("reason", "referral-only") + "）"
        else:
            prep_hint = cfg.get("prep_hint", "需补充该技能的必填参数后单独调用")
        # 执行卡里的 params 是多技能混在一起的；按各技能自己的白名单拆分，
        # 避免把 ct-registry 的 cond 塞给 ct-safety（客户端拿到会 argparse 报错）。
        allow = set((cfg.get("params") or {}).keys())
        params = {k: v for k, v in card_params.items() if k in allow} if allow else {}
        required = list(cfg.get("required_params") or [])
        missing = [k for k in required if card_params.get(k) in (None, "")]
        tier = _resolve_tier(mapping, t)
        tier_id = tier.get("tier", "B")
        deferred.append({
            "tool": t,
            "mention": "@skill:%s" % t,
            "required_params": required,
            "params": params,
            "missing": missing,
            "prep_hint": prep_hint,
            "deliverables": _HANDOFF_DELIVERABLES.get(t, ""),
            "tier": tier_id,
            "confidential": tier_id != "A",
            # 混合执行卡可能夹带本机根本没有的技能（Coze / 上游误报）。渲染层据此
            # 不输出 @skill 卡片，避免把「可调」宣传成事实（2026-11-09 扩展用例）。
            "client_callable": _client_callable(t),
            # ct-safety 的 drug 只认英文通用名（openFDA）。中文问句抽不出英文时
            # 不硬填中文（会零命中），改为给一条可执行的换算提示。
            "hint": ("openFDA 需英文通用名（如 semaglutide）；中文药名请换算后再填 drug"
                     if t == "ct-safety" and "drug" in missing else ""),
            "hint_en": ("openFDA needs an English generic name (e.g. semaglutide); "
                        "translate a Chinese drug name before filling drug"
                        if t == "ct-safety" and "drug" in missing else ""),
        })
    return deferred


def ensure_deferred(tool_out: dict, card: dict) -> dict:
    """主流程兜底：handoff 结果缺 deferred 时，用执行卡里的多技能列表现场补齐。

    2026-11-09 主流程审查：混合调用的 `need_tools` 可能在传递中丢失
    （旧版委托块 / 上游只回 need_tool / 预判 card 漏字段）。此时
    `execute_card` 产出的 handoff 只有一个主卡片，用户看不到其余技能。
    本函数由**代码**在缝合前补齐 deferred，覆盖 build_output 预取路径与
    refine_answer 的 card-inline / ship 路径；纯本地、无 LLM、无网络。

    已有 deferred 时原样返回（不覆盖上游更完整的信息）。
    """
    if not isinstance(tool_out, dict) or tool_out.get("status") != "handoff":
        return tool_out
    if tool_out.get("deferred_tools"):
        return tool_out
    tools = [t for t in (card.get("need_tools") or []) if t and t != card.get("need_tool")]
    if not tools:
        return tool_out
    try:
        deferred = _build_deferred(_load_mapping(), card.get("need_tool"),
                                   card.get("need_tools"), card.get("params") or {})
    except Exception:  # noqa: BLE001 - 兜底失败不得影响主答案
        return tool_out
    out = dict(tool_out)
    out["deferred_tools"] = deferred
    return out


def _build_cmd(tool_cfg: dict, params: dict) -> list:
    """按映射表构造 CLI 命令；params 键对齐 argparse 参数，布尔 true 才加 flag"""
    cmd = [tool_cfg["cmd"]]
    for arg in tool_cfg["args"]:
        cmd.append(arg.replace("{SKILLS_DIR}", SKILLS_DIR))
    for key, spec in tool_cfg["params"].items():
        if key not in params or params[key] is None:
            continue
        val = params[key]
        if spec["type"] == "bool":
            if val is True:
                cmd.append(spec["flag"])
            # False → 不加 flag
            continue
        cmd.append(spec["flag"])
        cmd.append(str(val))
    # 追加额外参数（如 samplesize 的 --yes：执行卡场景视为已确认，跳过 SAFE PREVIEW）
    for extra in tool_cfg.get("extra_args", []):
        cmd.append(extra)
    # 条件参数（2026-08-23）：仅当某参数缺失/存在时才追加，用于补齐技能的默认行为落差
    # （如 ct-safety 缺 --event 时不做 disproportionality → 自动补 --top-events-signal）
    for rule in tool_cfg.get("conditional_args", []):
        absent = rule.get("when_absent")
        present = rule.get("when_present")
        if absent and params.get(absent) not in (None, ""):
            continue
        if present and params.get(present) in (None, ""):
            continue
        cmd.extend(rule.get("args", []))
    return cmd


# ---------------------------------------------------------------------------
# 可执行体边界校验（2026-09-15，回应 ClawHub 审计项：「resolved executable path
# 未做白名单校验 / tool_mapping.json 无信任边界」）
#
# cmd[0] 与 args 全部源自 `tool_mapping.json`；该文件若被篡改，即可借执行卡指向
# 任意解释器或任意本地脚本。故在 subprocess 调用前强制两道断言：
#   ① 解释器 basename 必须命中白名单（python / py / Rscript 系）；
#   ② 所有 `.py` 脚本类参数解析后必须落在 SKILLS_DIR（兄弟技能根）之内。
# 本校验只做「放行 / 拦截」判定，不改变正常映射表的行为。
# ---------------------------------------------------------------------------
_ALLOWED_INTERPRETERS = {
    "python", "python3", "py", "python.exe", "py.exe",
    "rscript", "rscript.exe",
}


def _execution_boundary_violation(cmd: list) -> str:
    """返回越界原因（空串 = 通过）。规则见上方节注。"""
    if not cmd:
        return "空命令"
    if os.path.basename(str(cmd[0])).lower() not in _ALLOWED_INTERPRETERS:
        return "解释器不在白名单: %s" % cmd[0]
    root = Path(SKILLS_DIR).resolve()
    for arg in cmd[1:]:
        if not isinstance(arg, str) or not arg.endswith(".py"):
            continue
        p = Path(arg)
        try:
            resolved = (p if p.is_absolute() else root / p).resolve()
        except OSError:
            return "脚本路径无法解析: %s" % arg
        if not resolved.is_relative_to(root):
            return "脚本路径越出技能根目录: %s" % arg
    return ""


def _extract_json(stdout: str):
    """从 stdout 提取 JSON 主产物（优先最后一个完整 JSON 对象）；无则返回文本兜底。

    2026-08-20 修复：旧实现用 rfind('{')/rfind('}') 定位，遇嵌套 JSON（如
    ct-registry --print-summary 的 landscape 对象）会取到内层 { 导致切片不完整、
    json.loads 失败 → 退回全文。改为按行累积：从最后一行以 '{' 开头的行往前
    累积到闭合 '}'，逐段尝试解析。
    """
    stdout = (stdout or "").strip()
    if not stdout:
        return None
    # 整体解析
    try:
        return json.loads(stdout)
    except Exception:
        pass
    # 按行累积：从后往前找以 { 开头的行，累积到闭合 } 尝试解析
    lines = stdout.splitlines()
    for i in range(len(lines) - 1, -1, -1):
        if not lines[i].lstrip().startswith("{"):
            continue
        buf = lines[i]
        depth = buf.count("{") - buf.count("}")
        for j in range(i + 1, len(lines) + 1):  # j == len(lines) 表示不再追加
            # 每到一个闭合点（depth<=0）就尝试解析当前 buf
            if depth <= 0:
                try:
                    return json.loads(buf)
                except Exception:
                    pass  # 解析失败 → 可能跨行，继续追加
            if j >= len(lines):
                break
            buf += lines[j]
            depth += lines[j].count("{") - lines[j].count("}")
    return stdout  # 文本兜底


def _infer_missing_params(tool_cfg: dict, params: dict, question: str) -> tuple:
    """补全缺失参数：test 类参数用 test_hints（配置化关键词→值）推断。

    返回 (补全后的 params, 仍缺失的必需参数列表)。
    """
    params = dict(params)
    missing = []
    required = tool_cfg.get("required_params", [])
    for rp in required:
        if params.get(rp) is None:
            hints = tool_cfg.get("test_hints", {})
            if hints and question:
                q = question or ""
                for pattern, value in hints.items():
                    if any(kw in q for kw in pattern.split("|")):
                        params[rp] = value
                        break
            if params.get(rp) is None:
                missing.append(rp)
    # 效应量检查（samplesize 等）：effect_params 中至少提供一个
    for ep in tool_cfg.get("effect_params", []):
        if params.get(ep) is not None:
            return params, missing
    if tool_cfg.get("effect_params"):
        missing.append("效应量参数(任选其一): " + " / ".join(tool_cfg["effect_params"]))
    return params, missing


def execute_card(card: dict) -> dict:
    tool = card.get("need_tool")
    params = card.get("params") or {}
    draft = card.get("draft_answer") or ""
    question = card.get("original_question") or ""
    # F3 (2026-09-03)：调用方语言透传——内容级检测用户语言，经 CTSS_LOCALE 注入子进程
    # 环境，兄弟技能（coze 引擎 ct-samplesize v5）据此切 coze 端报告 / 图表语言。
    call_locale = _resolve_call_locale(card, question)
    call_env = dict(os.environ)
    call_env["CTSS_LOCALE"] = call_locale
    if card.get("query_origin"):
        call_env["CT_QUERY_ORIGIN"] = str(card["query_origin"])
    mapping = _load_mapping()
    tool_cfg = mapping["skills"].get(tool)
    tier_info = _resolve_tier(mapping, tool)
    # 多命中场景：其余技能各自生成可直调的 @skill 卡片数据（2026-11-09）
    deferred = _build_deferred(mapping, tool, card.get("need_tools"), params)
    deferred_note = ""
    if deferred:
        items = "；".join(f"{d['mention']}（{d['prep_hint']}）" for d in deferred)
        deferred_note = (
            f"本轮主判为 {tool}；另识别到 {len(deferred)} 个相关技能，"
            f"客户端可按答案中的 @skill 卡片分别直接调用：{items}。"
        )

    # ---- cloud brief 分流（2026-11-09，默认关闭；任何失败一律回落原执行卡）----
    # 上移的是「执行位置」而非能力面：只对 config/brief_contract.json 登记的三个
    # A 档速览接口生效。参数白名单（护栏 1）、免责标注（护栏 2）、导流页脚（护栏 3）
    # 与回落链全部由该契约单一真相源管理；本地 engine=local 执行卡原样保留
    # （ct-base §20.19.7 红线 2：合并不取消本地引擎）。
    # 🔴 本块必须排在档位门 ①② 与「技能是否安装」判定之前：brief 通道的目的正是
    #    让用户不必为了一句速览问答而先安装三个技能。开关关闭时本块零副作用。
    import sys  # noqa: F401 - 保证下方 stderr 信号在直接调用本函数时可用
    # 本模块既被 subprocess 直接运行、也被 refine_answer.py import；后者场景下
    # sys.path 未必含 scripts/，显式补齐，避免 import 失败被误当成「回落」静默降级。
    _scripts_dir = str(Path(__file__).resolve().parent)
    if _scripts_dir not in sys.path:
        sys.path.insert(0, _scripts_dir)
    try:
        from cloud_brief import try_cloud_brief
        _brief_text = try_cloud_brief(card)
    except Exception as _e:  # noqa: BLE001 - 任何异常都不得卡死主链路
        _brief_text = None
        sys.stderr.write(
            f"[ct-advisor] cloud-brief 分流异常，回落本地执行卡: "
            f"{type(_e).__name__}: {_e}\n"
        )
    if _brief_text:
        sys.stderr.write("[ct-advisor] cloud-brief hit（Coze ct-search 速览通道）\n")
        return {
            "tool": tool,
            "status": "ok",
            # 字符串形态：缝合层 _render_skill_result 原样透出，不改写、不 JSON 化
            "result": _brief_text,
            "draft_answer": draft,
            "deferred_tools": deferred,
            "deferred_note": deferred_note,
            "elapsed_sec": 0,
            "mode": "coze_brief",
        }

    # ---- 客户端直调 handoff 分流（2026-11-09，默认开启）----
    # 🔴 必须排在档位门 ①② 之前：B 档 / 未上架 A 档只要已在本机注册，客户端就能
    #    直接调用，不该再被「不对外发布 / 尚未上架 / 无法通过安装获取」拦下。
    #    brief 分流仍排在前面：用户显式开 CT_ADVISOR_CLOUD_BRIEF=1 时以速览优先。
    #    CT_ADVISOR_HANDOFF=0 → 整条跳过，回到原执行卡（含档位门），可无成本回滚。
    if _handoff_enabled() and _client_callable(tool):
        _hp, _hmissing = _infer_missing_params(tool_cfg or {}, params, question)
        sys.stderr.write("[ct-advisor] client-handoff hit（%s 已在本机注册）\n" % tool)
        return _handoff_result(tool, _hp, _hmissing, tier_info, tool_cfg,
                               deferred, deferred_note, draft)

    # ---- 档位门 ①（2026-09-10 / 2026-11-09 口径）：本机未注册的 B 档 / 未登记技能
    #      → 提示「本机未注册 / 不经公共市场分发」，不尝试安装、不硬错 ----
    # 需求：B 类技能「直接提示需要调用 B 类技能，但该技能不对外发布，然后用自己能力范围内的
    # 功能完成相应的分析任务」。故此处返回结构化 unreleased_b，由缝合层把 Coze 草稿原样透出
    # 并附说明；不进入 subprocess，也就不存在 FileNotFoundError / 未映射两种硬错。
    if tier_info["tier"] != "A":
        unregistered = not tier_info["registered"]
        reason = (
            f"{tool} 未在 ct-advisor 的技能登记表中（按 B 档保守处理）"
            if unregistered else
            f"{tool} 属 B 档技能（输入含涉密信息：受试者数据 / 方案 / CRF）"
        )
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
                "hint": "用自身能力（Coze 草稿 + 本地知识库）尽量完成分析，并明确标注「深度分析未实际执行」。",
            },
            "draft_answer": draft,
            "deferred_tools": deferred,
            "deferred_note": deferred_note,
            "elapsed_sec": 0,
        }

    # ---- 档位门 ②（2026-09-10）：A 档但尚未发布 → 不可安装，本地作答，无需征询授权 ----
    # ⚠️ 本门必须排在 `if not tool_cfg` 之前：未发布的 A 档技能（如 ct-pipeline）只登记在
    # tiers 里、**不在 skills 自动执行表**，若晚于该分支就会落进「未在 tool_mapping 中找到
    # 技能映射」硬错——那正是本改造要消灭的行为（2026-09-10 实测踩到）。
    # 「已安装 + 未发布」的组合经 need_tool 不可达（此类技能不在自动执行表），故无需为它让路。
    if not tier_info["published"]:
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
                        "将该技能承担的用途纳入「需本地具备该能力」的说明，"
                        "以自身能力（Coze 草稿 + 本地知识库 + 已装兄弟技能）尽量完成分析，"
                        "并明确标注「数据未取数 / 深度分析未实际执行」。",
                "next_step": (f"若该技能已在你的客户端中可用，可直接调用 @skill:{tool}；"
                              "否则可先分别调用 ct-registry / ct-safety / ct-literature 取数，"
                              "再由 ct-advisor 就地缝合。"),
            },
            "draft_answer": draft,
            "deferred_tools": deferred,
            "deferred_note": deferred_note,
            "elapsed_sec": 0,
        }

    if not tool_cfg:
        # 优雅降级（F1, 2026-09-03）：referral-only 技能（如 meta-analysis）不在
        # tool_mapping 自动执行——它需数据抽取 + 重型 R 管线，不经 need_tool 机械调用，
        # 改为引导用户显式 @skill 调用，而不是报硬错卡死整条应答。
        ref = (mapping.get("referrals") or {}).get(tool)
        if ref:
            return {
                "tool": tool,
                "status": "referral",
                "result": {
                    "message": ref.get("reason", f"{tool} 为 referral-only，不经 need_tool 自动调用"),
                    "mention": ref.get("mention", f"@skill:{tool}"),
                    "github": ref.get("github", f"https://github.com/medstatstar/{tool}"),
                },
                "draft_answer": draft,
                "deferred_tools": deferred,
                "deferred_note": deferred_note,
                "elapsed_sec": 0,
            }
        return {
            "tool": tool,
            "status": "error",
            "result": f"未在 tool_mapping.json 中找到技能映射: {tool}",
            "draft_answer": draft,
            "deferred_tools": deferred,
            "deferred_note": deferred_note,
            "elapsed_sec": 0,
        }

    # ---- 档位门 ③（2026-09-10）：A 档 → 先查是否安装；未安装则**建议安装**（默认不代办） ----
    # 需求：A 类技能「首先检查是否安装，没有安装则提示用户安装。当用户拒绝时，给出在自己能力
    # 范围内的分析结果，如果用户同意则进行安装，安装以后调用相应的技能完成相应的分析」。
    # 🔴 本处只检测 + 上报，**绝不执行安装**；且默认姿态为「建议安装」（2026-09-10 用户要求：
    # 安装可能触发本机安全警告），仅在用户**明确授权**后才由 agent 代办（ct-base §5 禁止静默安装）。
    if not _skill_installed(tool_cfg):
        consent = str(card.get("install_consent") or "").strip().lower()
        # 安装授权门（2026-09-10 用户要求）：默认姿态是**建议安装**——安装动作会下载并写入
        # 本地技能目录，可能触发本机安全提示，故不得自动安装；只有用户给出**明确授权**词
        # 才转为「可代办执行」。含糊 / 缺省 → suggest（只建议，agent 不得代为执行）。
        authorized = consent in _APPROVE_WORDS
        # 其中参数缺失一并算好，让 agent 可以在同一轮里同时问「装不装」和「补哪些参数」
        _p, _missing = _infer_missing_params(tool_cfg, params, question)
        if consent in _DECLINE_WORDS:
            # 用户拒绝安装 → 用自身能力作答（Coze 草稿兜底），明确标注未取数
            return {
                "tool": tool,
                "status": "local_fallback",
                "result": {
                    "message": f"用户未安装 {tool}，本轮以自身能力作答（未调用该技能取数）。",
                    "tier": "A",
                    "github": tier_info["github"],
                    "purpose": tier_info["purpose"],
                    "hint": "仅可说方法论 / 框架 / 需准备的数据项；凡试验登记号、安全信号数值、"
                            "文献条目等需取数的内容，一律不得编造，须明确标注「数据未取数」。",
                },
                "draft_answer": draft,
                "deferred_tools": deferred,
                "deferred_note": deferred_note,
                "elapsed_sec": 0,
            }
        return {
            "tool": tool,
            "status": "install_required",
            "result": {
                "message": (
                    f"{tool} 的本地 CLI 尚未落盘（A 档技能，已在 SkillHub 上架）。"
                    "若客户端已能直接调用该技能，可跳过安装，直接用 "
                    f"@skill:{tool}；否则**建议安装**：你可自行执行安装命令，"
                    "或明确授权后由 ct-advisor 代为安装。"
                    if not authorized else
                    f"{tool} 尚未安装；用户已明确授权安装，可执行安装命令。"
                ),
                "tier": "A",
                "published": tier_info["published"],
                "github": tier_info["github"],
                "skillhub": _skillhub_id(mapping, tool),
                "purpose": tier_info["purpose"],
                # ---- 安装授权门（2026-09-10）----
                # 默认 suggest：**只向用户建议安装，agent 不得代为执行**（安装会下载并写入
                # 本地技能目录，可能触发本机安全提示）。仅当用户在卡片里给出 install_consent
                # 的**明确授权词**（_APPROVE_WORDS）时才转 authorized。
                "install_mode": "authorized" if authorized else "suggest",
                "install_authorized": authorized,
                "install_note": ("安装会从 SkillHub 下载技能包并写入本地技能目录，可能触发本机"
                                 "安全提示；在用户明确授权前，ct-advisor 不执行任何安装动作。"),
                # 安装通道 = SkillHub（平台自带市场未收录 ct-*，实测 total=0）。
                # install_command 由 _install_command() 生成，含 --dir 与完整解释器路径，
                # 是**实测可执行**的命令；不得退回裸 `skillhub install`（PATH 无此命令）。
                "install_command": _install_command(mapping, tool),
                "install_hint": (f"安装通道：SkillHub（{_skillhub_id(mapping, tool)}）"
                                 if _skillhub_cli(mapping) else
                                 "本机未找到 SkillHub CLI（~/.skillhub/skills_store_cli.py）；"
                                 "请使用上方的 install_command（自带安装器），"
                                 "或按 GitHub 仓库手动放入技能目录。"),
                "missing": _missing,
                "hint": (
                    "用户已明确授权安装 → 执行 install_command，安装成功后带**原执行卡**重跑 "
                    "`--card-inline`（代码会自动调用该技能并缝合）；安装失败则告知用户并改用"
                    "自身能力作答、标注「数据未取数」。"
                    if authorized else
                    "🔴 **只建议、不执行**：向用户说明该技能的用途，把 install_command 原样"
                    "给出（用户可自行执行），并说明「安装会写入本地技能目录、可能触发本机安全"
                    "提示」。**除非用户明确授权**（回复授权安装 → 在卡片加 "
                    "\"install_consent\": \"approved\" 重跑），否则**不得代为执行安装**。"
                    "用户拒绝 → 在卡片加 \"install_consent\": \"declined\" 重跑，"
                    "由代码产出「未取数」兜底答案。"
                ),
            },
            "draft_answer": draft,
            "deferred_tools": deferred,
            "deferred_note": deferred_note,
            "elapsed_sec": 0,
        }

    # 缺参检查与补全（test 推断 / 效应量缺失 → need_params 追问）
    params, missing = _infer_missing_params(tool_cfg, params, question)
    if missing:
        return {
            "tool": tool,
            "status": "need_params",
            "result": {
                "message": "执行卡参数不完整，需补充以下参数后才能执行",
                "missing": missing,
                "hint": "由本地大模型向用户询问缺失参数（不编造）；样本量/检验效能类必须提供效应量假设",
            },
            "draft_answer": draft,
            "deferred_tools": deferred,
            "deferred_note": deferred_note,
            "elapsed_sec": 0,
        }

    # 引擎类型（F5, 2026-09-03）：local = 本地执行引擎（需 --run/--yes 跳过交互确认门）；
    # coze = 远程 R 服务（v5 无 --yes 闸门，请求信封由执行卡触发直接发送）。
    # 仅在执行期使用，故置于早期 return（referral / need_params / 路径越界）之后。
    engine = tool_cfg.get("engine", "local")
    cmd = _build_cmd(tool_cfg, params)
    timeout = tool_cfg.get("timeout", 120)
    # 🔴 可执行体边界校验（2026-09-15）：解释器须命中白名单，脚本路径不得越出技能根。
    #    与下方 workdir 校验共同构成 subprocess 前的双闸门。
    _violation = _execution_boundary_violation(cmd)
    if _violation:
        return {
            "tool": tool,
            "status": "error",
            "result": f"执行被安全边界拦截：{_violation}",
            "draft_answer": draft,
            "deferred_tools": deferred,
            "deferred_note": deferred_note,
            "elapsed_sec": 0,
        }
    # 路径白名单防御（审计 §16 要求）：tool 已确认为 tool_mapping 已知键；
    # 再确保解析后 workdir 落在 CARDS_ROOT 之内，杜绝 ../ 逃逸。
    workdir = (CARDS_ROOT / tool).resolve()
    if not workdir.is_relative_to(CARDS_ROOT.resolve()):
        return {
            "tool": tool,
            "status": "error",
            "result": f"非法工具路径（超出允许目录）: {tool}",
            "draft_answer": draft,
            "deferred_tools": deferred,
            "deferred_note": deferred_note,
            "elapsed_sec": 0,
        }
    workdir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
            cwd=str(workdir),
            env=call_env,
            **_hidden_kwargs()
        )
        elapsed = round(time.time() - t0, 1)
        combined = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
        if proc.returncode != 0:
            return {
                "tool": tool,
                "status": "error",
                "result": f"技能执行失败 rc={proc.returncode}: {combined[:2000]}",
                "draft_answer": draft,
                "deferred_tools": deferred,
                "deferred_note": deferred_note,
                "elapsed_sec": elapsed,
            }
        result = _sanitize_result(_extract_json(proc.stdout or ""))
        artifacts = _read_artifacts(tool_cfg, workdir)
        # 假成功守卫（2026-08-23 / F5 2026-09-03）：仅本地引擎技能会因缺 --run/--yes
        # 停在 PREVIEW 安全门（把 "would run …" 当数据交给缝合层，ct-literature 实测）；
        # coze 引擎（如 ct-samplesize v5）无此闸门、请求信封直接发送，不因 [PREVIEW] 误判假成功。
        if engine != "coze" and isinstance(result, str) and "[PREVIEW]" in result and not artifacts:
            return {
                "tool": tool,
                "status": "error",
                "result": f"技能停在 PREVIEW 安全门未联网执行（缺 --run）：{result[:500]}",
                "draft_answer": draft,
                "deferred_tools": deferred,
                "deferred_note": deferred_note,
                "elapsed_sec": elapsed,
            }
        # 假成功守卫（2026-08-25 / F5 2026-09-03）：仅本地引擎技能会因缺确认词停在
        # 关键字体系确认门（KW-GATE）；coze 引擎无此门（同上，不因 [KW-GATE] 误判）。
        if engine != "coze" and isinstance(result, str) and "[KW-GATE]" in result:
            return {
                "tool": tool,
                "status": "error",
                "result": f"技能停在关键字体系确认门（KW-GATE）未联网执行（需 --kw-adopt / --no-expand / 确认词）：{result[:500]}",
                "draft_answer": draft,
                "deferred_tools": deferred,
                "deferred_note": deferred_note,
                "elapsed_sec": elapsed,
            }
        return {
            "tool": tool,
            "status": "ok",
            "result": result,
            "artifacts": artifacts,
            "workdir": str(workdir),
            "draft_answer": draft,
            "deferred_tools": deferred,
            "deferred_note": deferred_note,
            "elapsed_sec": elapsed,
        }
    except subprocess.TimeoutExpired:
        return {
            "tool": tool,
            "status": "error",
            "result": f"技能执行超时（>{timeout}s）",
            "draft_answer": draft,
            "deferred_tools": deferred,
            "deferred_note": deferred_note,
            "elapsed_sec": timeout,
        }
    except FileNotFoundError as e:
        return {
            "tool": tool,
            "status": "error",
            "result": f"技能脚本不存在: {e}",
            "draft_answer": draft,
            "deferred_tools": deferred,
            "deferred_note": deferred_note,
            "elapsed_sec": 0,
        }


def main():
    ap = argparse.ArgumentParser(description="need_tool 执行卡 → 本地技能执行器")
    ap.add_argument("--card", required=True, help="执行卡 JSON 字符串")
    args = ap.parse_args()
    try:
        card = json.loads(args.card)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "result": f"执行卡 JSON 解析失败: {e}"}, ensure_ascii=False))
        sys.exit(1)
    out = execute_card(card)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
