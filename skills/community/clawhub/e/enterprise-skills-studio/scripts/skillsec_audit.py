#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能安全审计器（SkillSec Audit）— 借鉴 NVIDIA SkillSpector 公开的 16 类漏洞模式

本实现为自有开源代码（纯 Python 标准库，零第三方依赖）。方法论借鉴自 NVIDIA
SkillSpector 公开的「16 类漏洞模式」分类法（详见 references/skill-spector-method.md）。
我们不复制其代码或品牌，仅吸收其分类思想，构建可对本技能及其他任意技能做
静态安全审计的能力——这也正是「融合」的落点。

覆盖 16 类（类别 ID 与 SkillSpector 公开分类对应）：
  C01 过度能动 (Over-actuation)
  C02 输出处理 (Output handling)
  C03 叛变特工 (Rogue agent / self-modification)
  C04 触发滥用 (Trigger abuse)
  C05 MCP 最低特权 (MCP least privilege)
  C06 MCP 工具中毒 (MCP tool poisoning)
  C07 提示注入 (Prompt injection)
  C08 数据外流 (Data exfiltration)
  C09 特权升级 (Privilege escalation)
  C10 供应链 (Supply chain)
  C11 系统提示漏出 (System prompt leakage)
  C12 记忆中毒 (Memory poisoning)
  C13 工具滥用 (Tool abuse / unsafe defaults)
  C14 危险 AST (Dangerous AST: exec/eval/dynamic import)
  C15 污染追踪 (Taint tracking: untrusted -> sink)
  C16 YARA 签名 (Malware / webshell / cryptominer heuristics)

输出「类 SkillSpector」结构化报告：类别 / 严重度(高·中·低·INFO) / 置信度 / 证据 / 发现。
支持 --json / --md，便于接入 CI 卡点（studio audit <skill>）。

退出码：0=无「高」级发现；1=存在「高」级发现（可作阻断卡点）。
"""
import argparse
import json
import os
import re
import sys
from collections import namedtuple

Finding = namedtuple("Finding", ["cid", "category", "severity", "confidence", "evidence", "detail"])
SEV_HIGH, SEV_MED, SEV_LOW, SEV_INFO = "高", "中", "低", "INFO"

# ---------------------------------------------------------------------------
# 文件加载（与 review_checklist.py 同构）
# ---------------------------------------------------------------------------

def load_skill(target):
    if os.path.isdir(target):
        d = target
        md_path = os.path.join(d, "SKILL.md")
    else:
        md_path = target
        d = os.path.dirname(os.path.abspath(target))
    if not os.path.isfile(md_path):
        raise FileNotFoundError(f"找不到 SKILL.md: {md_path}")
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()
    siblings = []
    for root, _, files in os.walk(d):
        for fn in files:
            if fn == "SKILL.md":
                continue
            siblings.append(os.path.relpath(os.path.join(root, fn), d))
    return text, d, siblings


# ---------------------------------------------------------------------------
# 复用 / 新增检测模式
# ---------------------------------------------------------------------------

# 防御性语境：文档仅在"描述如何检测/防护"时提及对抗/外泄，不应判发现
RE_DEFENSIVE_CTX = re.compile(
    r"(排查|检测|防护|防御|识别|审计|监控|分析|处置|如何应对|如何检测|"
    r"示例|example|detect|prevent|scan|defen[sc]e|mitigat|避免|防范|反制|回应|"
    r"扫描|扫|检测|扫描器|语义层)",
    re.I,
)

# 否定语境：权限声明/安全边界常以"不/绝不/禁止/未"描述"我们不做某事"，不应判发现
RE_NEG = re.compile(r"(不|无|没有|禁止|绝不|未|拒绝|避免|防止|不会|禁)", re.I)

def in_defensive_context(text, m):
    if not m:
        return False
    s = max(0, m.start() - 90)
    e = min(len(text), m.end() + 90)
    return bool(RE_DEFENSIVE_CTX.search(text[s:e]))

def negated(text, m, win=25):
    """匹配点前方短窗口内是否出现否定词（如'不做自主决策''绝不访问 .env'）。"""
    if not m:
        return False
    pre = text[max(0, m.start() - win):m.start()]
    return bool(RE_NEG.search(pre))


# C01 过度能动：无用户确认下的自主/自动执行
RE_AUTO = re.compile(
    r"(自主(决策|执行|运行|行动)|自动(执行|运行|修改|写入|删除)|"
    r"无需(用户)?(确认|同意)|不(需|经)(用户)?(确认|同意)|自行决定|自行(执行|修改)|"
    r"without\s+(confirmation|user\s+(consent|confirmation))|"
    r"autonomous(ly)?\s+(decide|run|execute|act)|no\s+human\s+in\s+the\s+loop)",
    re.I,
)

# C03 叛变特工：自我修改 / 自我更新
RE_SELFMOD = re.compile(
    r"(自更新|自我更新|self[\- ]?update|自我修改|self[\- ]?modif|"
    r"改写自身|更新自身|修改自身|write.*(SKILL\.md|自身|own skill))",
    re.I,
)

# C04 触发滥用
RE_DESC_TRIGGER = re.compile(
    r"(当.{0,8}(用户|user|请求|出现)|when\s+the\s+user|use\s+this\s+skill\s+when|"
    r"触发|时机|如果用户)", re.I,
)
RE_VAGUE = re.compile(r"(尽力|尽可能|best\s+effort|尽量|自由发挥|你可以自行决定)", re.I)
RE_BROAD_TRIGGER = re.compile(r"(升级一下|检查更新|更新本技能|更新一下|update\s+(me|the\s+skill))", re.I)

# C05 MCP 最低特权
RE_MCP = re.compile(r"\bMCP\b|model\s*context\s*protocol|tool\s*call", re.I)
RE_PERM_DEC = re.compile(
    r"(capabilities|权限|最小权限|least\s+privilege|scope|许可|consent|同意|用户确认|显式触发)",
    re.I,
)

# C06 MCP 工具中毒 / Unicode 走私
RE_ZEROWIDTH = re.compile(r"[\u200b\u200c\u200d\u2060\ufeff\u00ad\u034f]")
RE_HIDDEN_INSTR = re.compile(r"(隐藏|暗藏|shadow)\s*(指令|指示|instruction|描述)", re.I)

# C07 提示注入（指令覆盖 / 隐藏指令）
RE_ADVERSARIAL = re.compile(
    r"(ignore\s+(previous|above|all|prior).{0,20}instructions)"
    r"|(disregard\s+(the\s+)?(above|previous|system))"
    r"|(system\s+prompt)"
    r"|(without\s+tell(ing)?\s+the\s+user)"
    r"|(secretly|silently)"
    r"|(override\s+(safety|security))"
    r"|(隐藏|忽略.{0,10}(安全|指令|规则)|秘密地|静默)",
    re.I,
)

# C08 数据外流
RE_EXFIL = re.compile(
    r"(id_rsa|~/.ssh|\.env\b|post\s+.{0,30}http|send\s+.{0,30}(external|外部)|exfil)",
    re.I,
)
RE_ENV = re.compile(r"(os\.environ|getenv|environ\[|\.env\b)", re.I)
RE_FS_ENUM = re.compile(r"(os\.walk\(['\"]~|os\.listdir\(['\"]~|glob\(['\"]~|/home/)", re.I)

# C09 特权升级
RE_PRIV = re.compile(
    r"(\bsudo\b|runas\s|elevation|提权|以管理员|管理员权限|runas\s+/user)", re.I)
RE_CRED = re.compile(
    r"(sk-[A-Za-z0-9]{20,})"            # OpenAI
    r"|(AKIA[0-9A-Z]{16})"              # AWS
    r"|(ghp_[A-Za-z0-9]{36})"           # GitHub
    r"|(xox[baprs]-[A-Za-z0-9-]{10,})"  # Slack
    r"|(api[_-]?key\s*[:=]\s*[\"'][^\"']{8,}[\"'])"
    r"|(password\s*[:=]\s*[\"'][^\"']{4,}[\"'])"
    r"|(token\s*[:=]\s*[\"'][^\"']{8,}[\"'])"
    r"|(secret\s*[:=]\s*[\"'][^\"']{8,}[\"'])",
    re.I,
)

# C10 供应链
RE_SUPPLY = re.compile(
    r"((curl|wget)[^\n|;&\"'`]*\|\s*(sh|bash|powershell|cmd))", re.I)
RE_DEPS_INSTALL = re.compile(
    r"(\bpip\s+install|\bnpm\s+install|\bapt(-get)?\s+install|\byarn\s+add|\bpip3\s+install)", re.I)
RE_FETCH = re.compile(r"(urllib\.request|requests\.get|httpx\.get|urlopen|fetch\()", re.I)
RE_ENC_DECODE = re.compile(
    r"(b64decode|base64\s*-d|base64\.b64decode|atob\s*\(|frombase64|rot13)", re.I)

# C11 系统提示漏出
RE_SYSLEAK = re.compile(
    r"(输出(你的)?(系统|system)\s*(提示|prompt|词)|打印(你的)?(系统|system)\s*(提示|prompt)|"
    r"reveal\s+your\s+(system\s+)?(prompt|instructions)|echo\s+(your|the)\s+system|"
    r"输出(你|本)技能(的)?(提示|prompt)|把(你的)?(指令|提示词)(输出|打印|泄露))",
    re.I,
)

# C12 记忆中毒
RE_MEMORY = re.compile(
    r"(MEMORY\.md|USER\.md|SOUL\.md|IDENTITY\.md|记忆文件|写入记忆|"
    r"持久化(到)?记忆|记住以下|记忆(污染|注入))",
    re.I,
)

# C13 工具滥用：不安全默认
RE_UNSAFE_DEF = re.compile(
    r"(force\s*=\s*True|dry_run\s*=\s*False|apply\s*=\s*True|confirm\s*=\s*False|"
    r"auto\s*=\s*True|default.*(执行|应用|删除))",
    re.I,
)

# C14 危险 AST
RE_DANGER_AST = re.compile(
    r"(\bexec\s*\(|\beval\s*\(|__import__\s*\(|"
    r"importlib\s*\.\s*import_module|getattr\s*\([^)]*,\s*[\"'][^\"']*[\"']\s*\))",
    re.I,
)

# C15 污染追踪：未校验外部输入 -> 危险函数
RE_UNTRUSTED = re.compile(
    r"(外部|用户输入|用户上传|API\s*输入|webhook|邮件|附件|文档解析|第三方返回|"
    r"untrusted|user\s*input|request\.(args|json|form))",
    re.I,
)
RE_VALIDATE = re.compile(
    r"(校验|验证|清洗|转义|白名单|allowlist|sanitiz|脱敏|过滤)", re.I)
RE_SINK = re.compile(
    r"(os\.system|subprocess|exec\s*\(|eval\s*\(|requests\.post|urllib\.request|http\.post|send\s*\()",
    re.I,
)

# C16 YARA 启发式（恶意软件 / webshell / 挖矿）
RE_MAL = re.compile(
    r"(stratum\+tcp|c99\.php|b374k|r57\.php|/xmr|monero|挖矿|xmrig|"
    r"webshell|菜刀|一句话木马)", re.I)
RE_HTML_BUILD = re.compile(r"(<table|<div|<tr|<script|<!doctype|<html)", re.I)
RE_FSTR = re.compile(r"f[\"']|\.format\(")

# 扫描自身代码会自引用误报；排除自带扫描器脚本
SELF_FILES = {
    "review_checklist.py", "skillsec_audit.py", "studio.py", "upgrade_skill.py",
    "update_skill.py", "cross_platform_check.py", "dupe_check.py", "maturity_assess.py",
    "lifecycle_track.py", "roi_filter.py", "evolution_log.py", "training_pack.py",
    "compose.py", "eval_gen.py", "portal.py", "usage_tracker.py",
}

CODE_EXTS = (".py", ".js", ".ts", ".sh", ".bat", ".ps1")


def snip(text, m, pre=40, post=120):
    s = max(0, m.start() - pre)
    e = min(len(text), m.end() + post)
    return text[s:e].replace("\n", " ").strip()


# ---------------------------------------------------------------------------
# 16 类检测器（每个返回 list[Finding]）
# ---------------------------------------------------------------------------

def det_over_actuation(ctx):
    out = []
    m = RE_AUTO.search(ctx["text"])
    if m and not in_defensive_context(ctx["text"], m) and not negated(ctx["text"], m):
        out.append(Finding("C01", "过度能动 Over-actuation", SEV_HIGH, 90,
                           snip(ctx["text"], m),
                           "技能声明在无用户确认下进行自主/自动执行、修改或决策，"
                           "属于过度能动（unrestricted autonomy），易被提示注入或无关对话触发。"))
    return out


def det_output_handling(ctx):
    out = []
    code_texts = ctx["code_texts"]
    # (a) subprocess 输出直接流入危险函数
    for name, code in code_texts:
        # stdout -> sink 近距离
        for mm in re.finditer(r"\.stdout", code):
            after = code[mm.end(): mm.end() + 260]
            if RE_SINK.search(after):
                out.append(Finding("C02", "输出处理 Output handling", SEV_HIGH, 85,
                                   f"{name}: ...stdout...{snip(after, RE_SINK.search(after))}",
                                   "子进程输出未经校验/清洗即流入 os.system/eval/exec 等危险函数，"
                                   "存在未验证输出注入（unvalidated output injection）。"))
                break
        # (b) 由外部元数据生成 HTML/MD 但未转义（存储型 XSS，如门户生成器）
        if RE_HTML_BUILD.search(code) and RE_FSTR.search(code) and "html.escape" not in code:
            mh = RE_HTML_BUILD.search(code)
            out.append(Finding("C02", "输出处理 Output handling", SEV_HIGH, 92,
                               f"{name}: {snip(code, mh, post=80)}",
                               "代码将变量插值进 HTML/MD 但不调用 html.escape，"
                               "若数据来自不受信任的技能元数据，则产生存储型 XSS（cross-context output）。"))
    return out


def det_rogue_agent(ctx):
    out = []
    m = RE_SELFMOD.search(ctx["text"])
    if m:
        out.append(Finding("C03", "叛变特工 Rogue agent", SEV_MED, 88,
                           snip(ctx["text"], m),
                           "技能具备自我修改/自我更新能力（写入自身目录）。若受治理（钉置版本+"
                           "完整性校验+白名单+需确认）则属设计内能力；否则存在无监督自我演变风险。"
                           "（设计内能力应在 SECURITY.md 披露信任模型）"))
    return out


def det_trigger_abuse(ctx):
    out = []
    desc = ctx["desc"]
    if desc:
        if len(desc) > 700:
            out.append(Finding("C04", "触发滥用 Trigger abuse", SEV_MED, 80,
                               f"description 长度 {len(desc)} 字",
                               "description 过长且含大量触发条件，易在非意图语境下（仅讨论话题）被激活，"
                               "属于过于宽泛的触发（overly broad trigger）。"))
        if RE_VAGUE.search(desc):
            mv = RE_VAGUE.search(desc)
            out.append(Finding("C04", "触发滥用 Trigger abuse", SEV_MED, 78,
                               snip(desc, mv),
                               "描述含模糊/自由发挥措辞，触发边界不清，易被无关文本或嵌入内容诱发。"))
    mb = RE_BROAD_TRIGGER.search(ctx["text"])
    if mb:
        out.append(Finding("C04", "触发滥用 Trigger abuse", SEV_MED, 86,
                           snip(ctx["text"], mb),
                           "存在过于宽泛的自然语言触发短语（如「升级一下」），指代敏感动作（修改技能自身），"
                           "增加意外或提示注入触发的概率。"))
    return out


def det_mcp_least_priv(ctx):
    out = []
    if RE_MCP.search(ctx["text"]):
        has_dec = RE_PERM_DEC.search(ctx["text"]) or "capabilities" in ctx["frontmatter"].lower()
        if not has_dec:
            out.append(Finding("C05", "MCP 最低特权 MCP least privilege", SEV_MED, 80,
                               "技能提及 MCP / tool call 但未声明权限边界",
                               "技能宣传涉及工具/MCP 调用，却未显式声明能力、权限范围或用户同意边界，"
                               "属能力申报不足（insufficient capability declaration）。"))
    return out


def det_mcp_poisoning(ctx):
    out = []
    all_text = ctx["all_text"]
    zw = RE_ZEROWIDTH.search(all_text)
    if zw:
        out.append(Finding("C06", "MCP 工具中毒 MCP tool poisoning", SEV_HIGH, 92,
                           f"命中不可见字符 U+{ord(zw.group(0)):04X}",
                           "文本/代码含零宽或不可见 Unicode 字符，可能用于隐藏指令或 Unicode 欺骗"
                           "（hidden instructions / Unicode spoofing）。"))
    mh = RE_HIDDEN_INSTR.search(ctx["text"])
    if mh:
        out.append(Finding("C06", "MCP 工具中毒 MCP tool poisoning", SEV_MED, 75,
                           snip(ctx["text"], mh),
                           "提及隐藏/暗藏指令，疑似工具描述注入（param description injection）。"))
    return out


def det_prompt_injection(ctx):
    out = []
    m = RE_ADVERSARIAL.search(ctx["text"])
    if m and not in_defensive_context(ctx["text"], m):
        out.append(Finding("C07", "提示注入 Prompt injection", SEV_HIGH, 90,
                           snip(ctx["text"], m),
                           "含指令覆盖/隐藏指令类表述（如忽略先前指令、静默执行），"
                           "若技能本身引导此类行为或可被注入诱导，属高风险提示注入面。"))
    return out


def det_exfiltration(ctx):
    out = []
    for name, code in ctx["code_texts"]:
        if RE_ENV.search(code):
            out.append(Finding("C08", "数据外流 Data exfiltration", SEV_MED, 76,
                               f"{name}: {snip(code, RE_ENV.search(code))}",
                               "代码采集环境变量（os.environ/getenv/.env），可能收集凭据或敏感配置。"))
        if RE_FS_ENUM.search(code):
            out.append(Finding("C08", "数据外流 Data exfiltration", SEV_MED, 76,
                               f"{name}: {snip(code, RE_FS_ENUM.search(code))}",
                               "代码枚举用户主目录/文件系统，存在敏感文件枚举风险。"))
    me = RE_EXFIL.search(ctx["text"])
    if me and not in_defensive_context(ctx["text"], me) and not negated(ctx["text"], me):
        out.append(Finding("C08", "数据外流 Data exfiltration", SEV_HIGH, 84,
                           snip(ctx["text"], me),
                           "存在疑似数据外发/外泄模式（外部传输、凭据/敏感路径外传）。"))
    return out


def det_privilege(ctx):
    out = []
    for name, code in ctx["code_texts"]:
        m = RE_PRIV.search(code)
        if m:
            out.append(Finding("C09", "特权升级 Privilege escalation", SEV_HIGH, 85,
                               f"{name}: {snip(code, m)}",
                               "代码含提权/管理员权限执行（sudo/runas/提权），违反最小权限。"))
        mc = RE_CRED.search(code)
        if mc:
            out.append(Finding("C09", "特权升级 Privilege escalation", SEV_HIGH, 90,
                               f"{name}: {snip(code, mc)}",
                               "代码含疑似硬编码凭据/令牌，可直接访问凭证。"))
    return out


def det_supply_chain(ctx):
    out = []
    for name, code in ctx["code_texts"]:
        m = RE_SUPPLY.search(code)
        if m:
            out.append(Finding("C10", "供应链 Supply chain", SEV_HIGH, 92,
                               f"{name}: {snip(code, m)}",
                               "存在下载即执行（curl|sh / wget|sh 管道给 shell），典型供应链投毒向量。"))
        if RE_FETCH.search(code) and RE_DANGER_AST.search(code):
            out.append(Finding("C10", "供应链 Supply chain", SEV_HIGH, 86,
                               f"{name}: 远程获取 + exec/eval",
                               "代码从网络获取内容后又执行（exec/eval/__import__），"
                               "若来源被篡改即远程代码执行。"))
        if RE_ENC_DECODE.search(code):
            out.append(Finding("C10", "供应链 Supply chain", SEV_HIGH, 85,
                               f"{name}: {snip(code, RE_ENC_DECODE.search(code))}",
                               "含编码解码绕过（base64/ROT13 解码），常用于混淆载荷，属混淆代码信号。"))
        if RE_DEPS_INSTALL.search(code) and not ctx["has_manifest"]:
            out.append(Finding("C10", "供应链 Supply chain", SEV_MED, 72,
                               f"{name}: {snip(code, RE_DEPS_INSTALL.search(code))}",
                               "运行时装包但未声明依赖清单（未钉置依赖），供应链不可复现。"))
    return out


def det_sysprompt_leak(ctx):
    out = []
    m = RE_SYSLEAK.search(ctx["text"])
    if m and not in_defensive_context(ctx["text"], m):
        out.append(Finding("C11", "系统提示漏出 System prompt leakage", SEV_HIGH, 90,
                           snip(ctx["text"], m),
                           "技能引导输出/泄露系统提示词或内部指令（直接泄漏/工具式排泄），"
                           "存在系统提示被提取风险。"))
    return out


def det_memory_poison(ctx):
    out = []
    m = RE_MEMORY.search(ctx["all_text"])
    if m and not in_defensive_context(ctx["all_text"], m):
        out.append(Finding("C12", "记忆中毒 Memory poisoning", SEV_MED, 78,
                           snip(ctx["all_text"], m),
                           "涉及写入/持久化到记忆文件（MEMORY/USER/SOUL/IDENTITY）或记忆注入，"
                           "存在持久上下文注入与记忆操纵风险。"))
    return out


def det_tool_abuse(ctx):
    out = []
    for name, code in ctx["code_texts"]:
        m = RE_UNSAFE_DEF.search(code)
        if m:
            out.append(Finding("C13", "工具滥用 Tool abuse", SEV_MED, 72,
                               f"{name}: {snip(code, m)}",
                               "默认参数启用高危动作（force=True / confirm=False / apply=True 等），"
                               "属不安全默认（unsafe defaults），应在调用处显式要求确认。"))
    return out


def det_danger_ast(ctx):
    out = []
    for name, code in ctx["code_texts"]:
        m = RE_DANGER_AST.search(code)
        if m:
            out.append(Finding("C14", "危险 AST Dangerous AST", SEV_HIGH, 85,
                               f"{name}: {snip(code, m)}",
                               "代码调用 exec()/eval()/__import__()/动态 import/危险 getattr，"
                               "属动态执行，易被用于绕过静态审查与运行任意代码。"))
    return out


def det_taint(ctx):
    out = []
    for name, code in ctx["code_texts"]:
        if RE_UNTRUSTED.search(code) and RE_SINK.search(code) and not RE_VALIDATE.search(code):
            out.append(Finding("C15", "污染追踪 Taint tracking", SEV_HIGH, 82,
                               f"{name}: 外部输入 -> 危险函数（无校验）",
                               "代码处理外部/用户输入并流入危险函数（exec/eval/os.system/网络外发），"
                               "但全程未见校验/清洗/白名单，构成凭证泄露链与污染流。"))
    return out


def det_yara(ctx):
    out = []
    # 仅扫可执行代码（不扫文档），避免方法论文档里"举例说明检测目标"触发误报
    for name, code in ctx["code_texts"]:
        m = RE_MAL.search(code)
        if m:
            out.append(Finding("C16", "YARA 签名 Malware heuristics", SEV_HIGH, 80,
                               f"{name}: {snip(code, m)}",
                               "命中恶意软件/webshell/加密挖矿启发式特征（挖矿池、webshell 名、一句话木马等），"
                               "建议人工复核或跑真实 YARA/杀软。"))
    return out


DETECTORS = [
    det_over_actuation, det_output_handling, det_rogue_agent, det_trigger_abuse,
    det_mcp_least_priv, det_mcp_poisoning, det_prompt_injection, det_exfiltration,
    det_privilege, det_supply_chain, det_sysprompt_leak, det_memory_poison,
    det_tool_abuse, det_danger_ast, det_taint, det_yara,
]


# ---------------------------------------------------------------------------
# 上下文构建 + 执行
# ---------------------------------------------------------------------------

def build_context(text, d, siblings):
    file_texts = [("SKILL.md", text)]
    for s in siblings:
        if s.lower().endswith((".py", ".md", ".json", ".txt", ".sh", ".js", ".ts", ".yaml", ".yml", ".toml")):
            fp = os.path.join(d, s)
            try:
                file_texts.append((s, open(fp, encoding="utf-8", errors="ignore").read()))
            except Exception:
                pass
    all_text = "\n".join(t for _, t in file_texts)
    code_texts = [
        (n, t) for n, t in file_texts
        if n.lower().endswith(CODE_EXTS) and os.path.basename(n) not in SELF_FILES
    ]
    fm = re.search(r"description\s*:\s*(.+)", text)
    desc = fm.group(1).strip() if fm else ""
    has_manifest = any(
        s.lower().endswith(("requirements.txt", "package.json", "pyproject.toml",
                            "pipfile", "environment.yml", "poetry.lock"))
        for s in siblings)
    return {
        "text": text, "all_text": all_text, "code_texts": code_texts,
        "desc": desc, "frontmatter": text[:1200], "has_manifest": has_manifest,
    }


def audit(target):
    text, d, siblings = load_skill(target)
    ctx = build_context(text, d, siblings)
    findings = []
    for det in DETECTORS:
        try:
            findings.extend(det(ctx))
        except Exception as e:  # 单类异常不影响整体
            findings.append(Finding("ERR", f"检测器异常 {det.__name__}", SEV_INFO, 0,
                                    str(e), "该类别检测过程出错，请人工复核。"))
    return findings


# ---------------------------------------------------------------------------
# 报告
# ---------------------------------------------------------------------------

SEV_RANK = {SEV_HIGH: 3, SEV_MED: 2, SEV_LOW: 1, SEV_INFO: 0}

def rating(findings):
    highs = [f for f in findings if f.severity == SEV_HIGH]
    meds = [f for f in findings if f.severity == SEV_MED]
    if highs:
        return "高危（建议阻断 / BLOCK）"
    if meds:
        return "中危（需人工确认）"
    if any(f.severity == SEV_LOW for f in findings):
        return "低危"
    return "未检出高危/中危（通过）"


def render_text(findings, path):
    highs = sum(1 for f in findings if f.severity == SEV_HIGH)
    meds = sum(1 for f in findings if f.severity == SEV_MED)
    lows = sum(1 for f in findings if f.severity == SEV_LOW)
    infos = sum(1 for f in findings if f.severity == SEV_INFO)
    print(f"技能安全审计报告（SkillSec · 16 类，方法论借鉴 NVIDIA SkillSpector）: {path}")
    print("=" * 68)
    print(f"总体评级: {rating(findings)}")
    print(f"[高 {highs} / 中 {meds} / 低 {lows} / INFO {infos}]  共 {len(findings)} 条发现")
    print("=" * 68)
    order = sorted(findings, key=lambda f: (-SEV_RANK.get(f.severity, 0), f.cid))
    cur = None
    for f in order:
        if f.cid != cur:
            cur = f.cid
            print(f"\n## {f.cid} {f.category}")
        icon = {"高": "🔴", "中": "🟠", "低": "🟡", "INFO": "⚪"}.get(f.severity, "·")
        print(f"  {icon} [{f.severity}] 置信度 {f.confidence}% — {f.detail}")
        if f.evidence:
            print(f"       证据: {f.evidence[:160]}")
    print()
    if highs:
        print("存在「高」级发现，建议修复/人工确认后再发布或安装（CI 可据此卡点）。")
    else:
        print("无「高」级发现。中/低级建议人工确认后放行。")


def render_md(findings, path):
    highs = sum(1 for f in findings if f.severity == SEV_HIGH)
    meds = sum(1 for f in findings if f.severity == SEV_MED)
    out = [f"# 技能安全审计报告（SkillSec）: {path}", "",
           f"**总体评级**: {rating(findings)} · 高 {highs} / 中 {meds} / 共 {len(findings)} 条", "",
           "> 方法论借鉴 NVIDIA SkillSpector 公开 16 类漏洞模式；本实现为自有开源代码。", "",
           "## 发现明细", "",
           "| 类别 | 严重度 | 置信度 | 发现 | 证据 |",
           "|------|--------|--------|------|------|"]
    order = sorted(findings, key=lambda f: (-SEV_RANK.get(f.severity, 0), f.cid))
    for f in order:
        out.append(f"| {f.cid} {f.category} | {f.severity} | {f.confidence}% | {f.detail} | {f.evidence[:120]} |")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="技能安全审计器（SkillSec，16 类）")
    ap.add_argument("target", help="skill 目录或 SKILL.md 路径")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--md", action="store_true", help="输出 Markdown")
    args = ap.parse_args()

    try:
        findings = audit(args.target)
    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 2

    if args.json:
        payload = {
            "path": args.target,
            "rating": rating(findings),
            "counts": {
                "high": sum(1 for f in findings if f.severity == SEV_HIGH),
                "medium": sum(1 for f in findings if f.severity == SEV_MED),
                "low": sum(1 for f in findings if f.severity == SEV_LOW),
                "info": sum(1 for f in findings if f.severity == SEV_INFO),
            },
            "findings": [
                {"cid": f.cid, "category": f.category, "severity": f.severity,
                 "confidence": f.confidence, "detail": f.detail, "evidence": f.evidence}
                for f in sorted(findings, key=lambda x: (-SEV_RANK.get(x.severity, 0), x.cid))
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif args.md:
        print(render_md(findings, args.target))
    else:
        render_text(findings, args.target)

    return 1 if any(f.severity == SEV_HIGH for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
