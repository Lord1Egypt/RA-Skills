#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业技能审查器（Enterprise Skills Reviewer）

对一份 SKILL.md（及其目录）做静态体检，覆盖七大维度：
  1. 安全审查 8 项（发布前必过）
  2. CISO 五大风险（映射 OWASP AST10）
  3. 质量评估 5 维度
  4. 厚技能体检（厚技能 + 薄 harness 准则）
  5. 事务安全四件套（幂等/回滚/审计/最小权限，流程技能专用）
  6. 工作流可恢复性（状态机/HITL/降级/可观测，流程技能专用）
  7. 安全语义层（借鉴 skill-scanner/朱雀 + skill-vetter：编码绕过/敏感路径/
     裸IP外联/提权/未声明装包/声明-能力一致性，仅扫可执行文件）

纯标准库实现，无外部依赖，可在 WorkBuddy / Codex / Claude Code /
Cursor / 龙虾 / Hermes 等任意装了 Python 的环境运行。

用法：
  python review_checklist.py <skill目录或SKILL.md> [--json] [--md]

退出码：0=无 FAIL，1=存在 FAIL（便于 CI 卡点）。
"""
import argparse
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# 文件加载
# ---------------------------------------------------------------------------

def load_skill(target):
    """返回 (skill_md_text, dir_path, sibling_files)。"""
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
# 检测模式
# ---------------------------------------------------------------------------

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

RE_NETWORK = re.compile(
    r"(\bfetch\s*\()|(\bcurl\s)|(urllib)|(requests\.)|(axios\.)"
    r"|(http[s]?://[^\s)\"'`]+)",
    re.I,
)

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

RE_TOOL = re.compile(
    r"(\bos\.system\b|\bsubprocess\b|\bexec\s*\(|shell:|bash:|"
    r"write_file|read_file|\brm\s+-rf\b)",
    re.I,
)

RE_EXFIL = re.compile(
    r"(id_rsa|~/.ssh|\.env\b|post\s+.{0,30}http|send\s+.{0,30}(external|外部)|exfil)",
    re.I,
)

# 防御性语境：文档仅在"描述如何检测/防护"时提及对抗指令/外泄，不应判 FAIL
RE_DEFENSIVE_CTX = re.compile(
    r"(排查|检测|防护|防御|识别|审计|监控|分析|处置|如何应对|如何检测|"
    r"示例|example|detect|prevent|scan|defen[sc]e|mitigat|避免|防范|反制)",
    re.I,
)


def in_defensive_context(text, m):
    """匹配点周围窗口若处于防御/检测语境，则该提及属正常描述，不算攻击。"""
    if not m:
        return False
    s = max(0, m.start() - 90)
    e = min(len(text), m.end() + 90)
    return bool(RE_DEFENSIVE_CTX.search(text[s:e]))

RE_DESC_TRIGGER = re.compile(
    r"(当.{0,8}(用户|user|请求|出现)|when\s+the\s+user|use\s+this\s+skill\s+when|"
    r"触发|时机|如果用户)",
    re.I,
)

RE_VAGUE = re.compile(r"(尽力|尽可能|best\s+effort|尽量|自由发挥|你可以自行决定)", re.I)

# PII：手机号 / 身份证 / 邮箱（银行卡 16-19 位误报率高，不纳入）
RE_PII = re.compile(
    r"(?<!\d)(1[3-9]\d{9})(?!\d)"                         # 中国大陆手机号
    r"|(\d{17}[\dXx])"                                     # 身份证号
    r"|([A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,})"  # 邮箱
    , re.I,
)

# 外部/不可信输入源（用于"未校验外部输入"提示）
RE_UNTRUSTED = re.compile(
    r"(外部|用户输入|用户上传|API\s*输入|webhook|邮件|附件|文档解析|第三方返回|untrusted|user\s*input)",
    re.I,
)
RE_VALIDATE = re.compile(
    r"(校验|验证|清洗|转义|白名单|allowlist|sanitiz|脱敏|过滤|校验输入)",
    re.I,
)

# ----- 安全语义层（借鉴 skill-scanner/朱雀 + skill-vetter）-----
# 编码绕过：base64/ROT13 解码才是高危（FAIL 级）；字面 \xNN/\uNNNN 是弱信号（WARN 级）
RE_ENC_DECODE = re.compile(
    r"(b64decode|base64\s*-d|base64\.b64decode|atob\s*\(|frombase64|rot13)", re.I)
RE_ENC_LITERAL = re.compile(r"(\\x[0-9a-fA-F]{2}|\\u[0-9a-fA-F]{4})")
# 零宽 / 不可见字符（Unicode 走私载体）
RE_ZEROWIDTH = re.compile(r"[\u200b\u200c\u200d\u2060\ufeff\u00ad\u034f]")
# 敏感路径：ssh/aws/config 凭据、id_rsa、.env、agent 记忆文件
RE_SENSITIVE_PATH = re.compile(
    r"(~/\.ssh|~/\.aws|~/\.config|\.ssh/|id_rsa|\.env\b|credentials?|"
    r"(MEMORY|USER|SOUL|IDENTITY)\.md)", re.I)
# 裸 IP 外联（skill-vetter：应走域名而非 IP）
RE_IP_URL = re.compile(r"https?://\d{1,3}(\.\d{1,3}){3}(:\d+)?")
# 提权
RE_PRIV = re.compile(r"(\bsudo\b|runas\s|elevation|提权|以管理员|管理员权限|runas\s+/user)", re.I)
# 供应链投毒：下载即执行（curl|sh / wget|sh / 管道给 shell）
RE_SUPPLY = re.compile(
    r"((curl|wget)[^\n|;&\"'`]*\|\s*(sh|bash|powershell|cmd))", re.I)
# 运行时装包（未声明依赖）
RE_DEPS_INSTALL = re.compile(
    r"(\bpip\s+install|\bnpm\s+install|\bapt(-get)?\s+install|\byarn\s+add|\bpip3\s+install)", re.I)
# 写/执行类能力（用于声明-能力一致性）
RE_WRITE_OP = re.compile(
    r"(write_file|\.write\(|open\s*\([^)]*,\s*['\"]w|shutil\.rmtree|os\.remove|"
    r"subprocess|os\.system|requests\.post|urllib\.request|http\.post|send\s*\()", re.I)
# 声明"只读/不写"（一致性检查前提）
RE_READONLY_CLAIM = re.compile(
    r"(只读|仅读|不写|只读取|不会写入|read.?only|no\s+write|无需写入|不修改)", re.I)

# 语义层扫描时排除本工具自身的扫描器脚本：其源码合法包含上述检测目标串，
# 自扫会误报；本工具信任自带代码，只对第三方技能做语义体检。
SCANNER_SELF_FILES = {
    "review_checklist.py", "cross_platform_check.py", "dupe_check.py",
    "studio.py", "upgrade_skill.py", "maturity_assess.py", "lifecycle_track.py",
    "roi_filter.py", "evolution_log.py", "training_pack.py", "compose.py",
    "eval_gen.py", "usage_tracker.py", "portal.py",
}


# ---------------------------------------------------------------------------
# 检查器
# ---------------------------------------------------------------------------

def check(text, d, siblings, md_path):
    results = []  # (category, cid, name, status, detail)

    def add(cat, cid, name, status, detail=""):
        results.append((cat, cid, name, status, detail))

    skill_files = [s for s in siblings if s.lower().endswith((".py", ".sh", ".js", ".ts"))]
    has_refs = any(s.lower().startswith("references") or s.lower().startswith("refs") for s in siblings)
    word_count = len(text.split())

    # 收集可扫描文本（SKILL.md + 脚本/配置等），用于 PII / 密钥跨文件扫描
    file_texts = [("SKILL.md", text)]
    for s in siblings:
        if s.lower().endswith((".py", ".md", ".json", ".txt", ".sh", ".js", ".ts", ".yaml", ".yml", ".toml")):
            fp = os.path.join(d, s)
            try:
                file_texts.append((s, open(fp, encoding="utf-8", errors="ignore").read()))
            except Exception:
                pass
    all_text = "\n".join(t for _, t in file_texts)
    # 仅可执行文件参与"安全语义层"扫描，避免 SKILL.md 文档文字误报；
    # 并排除本工具自身的扫描器脚本（见 SCANNER_SELF_FILES），避免自引用误报
    code_exts = (".py", ".js", ".ts", ".sh", ".bat", ".ps1")
    code_texts = [
        (n, t) for n, t in file_texts
        if n.lower().endswith(code_exts)
        and os.path.basename(n) not in SCANNER_SELF_FILES
    ]
    all_code_text = "\n".join(t for _, t in code_texts)
    code_names = [n for n, _ in code_texts]

    # ---- 安全 8 项 ----
    add("安全8项", "S1", "全量审阅 SKILL.md 与脚本", "PASS" if text.strip() else "FAIL",
        "文件可读" if text.strip() else "内容为空")
    add("安全8项", "S2", "沙箱验脚本（隔离执行）",
        "WARN" if skill_files else "INFO",
        f"检测到脚本: {', '.join(skill_files) if skill_files else '无'}；有脚本须沙箱验证行为" if skill_files
        else "无脚本，跳过")
    m = RE_ADVERSARIAL.search(text)
    adv_defensive = m and in_defensive_context(text, m)
    add("安全8项", "S3", "排查对抗指令",
        "FAIL" if (m and not adv_defensive) else "PASS",
        (f"发现可疑表述（处防御性描述，不判 FAIL）: {m.group(0)!r}" if adv_defensive
         else f"发现可疑表述: {m.group(0)!r}" if m
         else "未发现忽略安全规则/隐藏操作等表述"))
    m = RE_NETWORK.search(text)
    add("安全8项", "S4", "核查网络调用",
        "WARN" if m else "PASS",
        "检测到网络相关调用/URL，须确认均为已声明用途" if m else "未发现网络调用")
    m = RE_CRED.search(text)
    add("安全8项", "S5", "校验凭据（无硬编码）", "FAIL" if m else "PASS",
        f"疑似硬编码凭据: {m.group(0)!r}" if m else "未发现硬编码密钥/令牌")
    m = RE_TOOL.search(text)
    add("安全8项", "S6", "梳理工具范围",
        "WARN" if m else "INFO",
        "检测到工具/命令调用，确认仅访问必要资源" if m else "未发现文件/命令调用")
    urls = RE_NETWORK.findall(text)
    ext_urls = [u for grp in urls for u in grp if isinstance(u, str) and u.startswith("http")]
    add("安全8项", "S7", "确认外跳转（目标域名）",
        "WARN" if ext_urls else "PASS",
        f"外部 URL({len(ext_urls)}个)，须确认均跳预期域名" if ext_urls else "无外部 URL")
    m = RE_EXFIL.search(text)
    exfil_defensive = m and in_defensive_context(text, m)
    exfil_external = bool(m) and bool(re.search(
        r"(send\s+.{0,30}(external|外部)|post\s+.{0,30}http)", m.group(0), re.I))
    if m and not exfil_defensive and exfil_external:
        s8_status, s8_detail = "FAIL", f"疑似外泄/外发模式: {m.group(0)!r}"
    elif m and exfil_defensive:
        s8_status, s8_detail = "PASS", f"外泄相关表述（处防御性描述，不判 FAIL）: {m.group(0)!r}"
    elif m:
        s8_status, s8_detail = "WARN", f"提及敏感路径/凭据: {m.group(0)!r}（弱信号，确认是否真实外发）"
    else:
        s8_status, s8_detail = "PASS", "未发现凭据/敏感数据外传"
    add("安全8项", "S8", "排查数据外泄", s8_status, s8_detail)

    # ---- CISO 5 风险 (AST10) ----
    has_owner = bool(re.search(r"(owner|所有者|负责人|maintainer)", text, re.I))
    add("CISO5", "C1", "无治理的技能蔓延 (AST09)",
        "WARN" if not has_owner else "PASS",
        "缺少 owner/所有者信息，建议登记注册表" if not has_owner else "已含所有者信息")
    add("CISO5", "C2", "供应链投毒 (AST01/02)",
        "WARN" if ext_urls else "PASS",
        "引用外部 URL，须确认来源可信且已签名" if ext_urls else "无外部来源引用")
    add("CISO5", "C3", "过度授权执行 (AST03/06)",
        "WARN" if (skill_files and RE_TOOL.search(text)) else "PASS",
        "脚本含文件/命令执行，确认最小权限" if (skill_files and RE_TOOL.search(text))
        else "未发现过度授权迹象")
    add("CISO5", "C4", "隐形载荷 Markdown 注入 (AST04/08)",
        "FAIL" if (m_adv := RE_ADVERSARIAL.search(text)) and not in_defensive_context(text, m_adv) else "PASS",
        "同 S3" if (m_adv := RE_ADVERSARIAL.search(text)) and not in_defensive_context(text, m_adv) else "未发现")
    add("CISO5", "C5", "跨平台可移植性 (AST10)",
        "INFO",
        "建议按 agentskills.io 标准写一次、多平台免改运行；注意各 surface 差异")

    # ---- 质量 5 维度 ----
    fm = re.search(r"description\s*:\s*(.+)", text)
    desc = fm.group(1).strip() if fm else ""
    add("质量5", "Q1", "触发准确率（描述含触发时机）",
        "PASS" if (desc and RE_DESC_TRIGGER.search(desc)) else "FAIL",
        f"description 长度 {len(desc)} 字，含触发词" if (desc and RE_DESC_TRIGGER.search(desc))
        else "description 缺失或未写清'何时调用'")
    add("质量5", "Q2", "共存冲突（描述不过宽）",
        "WARN" if (desc and len(desc) < 20) else "PASS",
        "描述过短易误触发，建议写清功能+场景" if (desc and len(desc) < 20) else "描述较具体")
    has_example = bool(re.search(r"(示例层|示例|example|should\s*trigger|应触发|不应触发|边界)", text, re.I))
    add("质量5", "Q3", "输出质量（示例层）", "PASS" if has_example else "WARN",
        "含示例/边界示范" if has_example else "缺示例层，质量上限无保障")
    has_boundary = bool(re.search(r"(边界|boundary|不应触发|should\s*not)", text, re.I))
    add("质量5", "Q4", "边界处理", "PASS" if has_boundary else "WARN",
        "含边界/不应触发示例" if has_boundary else "缺边界示例")
    add("质量5", "Q5", "资源效率（重内容外置）",
        "WARN" if (word_count > 1500 and not has_refs) else "PASS",
        f"SKILL.md 约 {word_count} 词且无 references/，建议外置大段参考" if (word_count > 1500 and not has_refs)
        else f"约 {word_count} 词，体量合理")

    # ---- 厚技能体检 ----
    add("厚技能", "T1", "确定性步骤有脚本 (scripts/)",
        "PASS" if skill_files else "WARN",
        f"脚本: {', '.join(skill_files)}" if skill_files else "无 scripts/，确定性任务建议脚本化")
    has_schema = bool(re.search(r"(模板|template|schema|json|格式要求|输出格式)", text, re.I))
    add("厚技能", "T2", "关键输出有模板/schema 约束", "PASS" if has_schema else "WARN",
        "含输出模板/格式约束" if has_schema else "建议固化输出结构")
    add("厚技能", "T3", "示例层（同质量 Q3）", "PASS" if has_example else "WARN",
        "已含示例" if has_example else "缺示例")
    has_check = bool(re.search(r"(校验|检查|验证|validate|check|自检)", text, re.I))
    add("厚技能", "T4", "自检/校验逻辑", "PASS" if has_check else "WARN",
        "含校验/验证逻辑" if has_check else "建议加入输出自检")
    vague = RE_VAGUE.search(text)
    add("厚技能", "T5", "harness 薄（无过多自由发挥指令）",
        "WARN" if vague else "PASS",
        f"发现模糊指令 '{vague.group(0)}'，建议改为显式控制流" if vague else "指令较显式")

    # ---- 事务安全 + 工作流可恢复性（流程技能专用，见 references/process-systems.md）----
    # 启发式：仅当技能涉及外部系统/工作流/写动作时才进入评估；否则 INFO 跳过，
    # 避免误伤纯方法论/问答类技能（如本工程台自身）。
    RE_SYS = re.compile(
        r"(连接器|connector|网关|gateway|MCP|ERP|CRM|HRM|OA系统|数据库|"
        r"状态机|state\s*machine|workflow|agentic|审批流|提交|写入|出账|发信|删数据)", re.I)
    RE_MUT = re.compile(
        r"(提交|写入|创建|新建|删除|更新|修改|出账|发信|删数据|审批|"
        r"modify|create|update|delete|insert)", re.I)
    is_process = bool(RE_SYS.search(text))
    has_mut = bool(RE_MUT.search(text))

    def proc_add(cat, cid, name, has_kw, kw_desc):
        if not is_process:
            add(cat, cid, name, "INFO", "未涉及外部系统/工作流，本条不适用")
            return
        status = "PASS" if has_kw else "WARN"
        detail = (f"已声明: {kw_desc}" if has_kw
                  else f"涉及系统型/写动作但未检出 {kw_desc}，建议补全（见 process-systems.md）")
        add(cat, cid, name, status, detail)

    # 事务安全四件套
    proc_add("事务安全", "TX1", "幂等（Idempotency）",
             bool(re.search(r"(幂等|idempotency|去重|幂等键|业务单号)", text, re.I)),
             "幂等键/去重")
    proc_add("事务安全", "TX2", "回滚（Rollback/补偿）",
             bool(re.search(r"(回滚|rollback|补偿|不归点|point of no return)", text, re.I)),
             "回滚/补偿/不归点")
    proc_add("事务安全", "TX3", "审计（Audit Log）",
             bool(re.search(r"(审计|audit|审计日志|前后值|链路)", text, re.I)),
             "审计日志")
    proc_add("事务安全", "TX4", "最小权限 / RBAC",
             bool(re.search(r"(最小权限|least privilege|RBAC|角色集|权限集|scope)", text, re.I)),
             "最小权限/RBAC")

    # 工作流可恢复性
    proc_add("工作流可恢复", "WF1", "状态机（State Machine）",
             bool(re.search(r"(状态机|state machine|状态\s*/\s*事件|状态表)", text, re.I)),
             "状态机/状态表")
    proc_add("工作流可恢复", "WF2", "HITL 门（人工确认）",
             bool(re.search(r"(HITL|人工确认|人工审核|确认人|不归点|人工审批)", text, re.I)),
             "HITL 门/人工确认")
    proc_add("工作流可恢复", "WF3", "降级 / 超时 / 重试",
             bool(re.search(r"(降级|degrad|超时|重试|retry|兜底|fallback)", text, re.I)),
             "降级/超时/重试")
    proc_add("工作流可恢复", "WF4", "可观测（Trace/日志）",
             bool(re.search(r"(可观测|observ|trace|链路|调用链|结构化日志)", text, re.I)),
             "可观测/trace")

    # ---- AI 安全加固（PII / 密钥跨文件扫描 / 外部输入校验）----
    m = RE_PII.search(all_text)
    add("AI安全", "P1", "PII 检测（个人敏感信息）",
        "WARN" if m else "PASS",
        f"疑似 PII: {m.group(0)!r}，请确认是否真实个人数据并脱敏" if m
        else "未检出手机号/身份证/邮箱等 PII")
    m = RE_CRED.search(all_text)
    add("AI安全", "S9", "凭据扫描（覆盖脚本文件）", "FAIL" if m else "PASS",
        f"疑似硬编码凭据: {m.group(0)!r}" if m else "脚本/配置中未发现硬编码密钥/令牌")
    has_untrusted = bool(RE_UNTRUSTED.search(text))
    has_validate = bool(RE_VALIDATE.search(text))
    add("AI安全", "INJ", "外部输入校验（防注入/越权）",
        "WARN" if (has_untrusted and not has_validate) else "PASS",
        "技能处理外部/用户输入但未声明校验/清洗/白名单，存在注入与越权风险"
        if (has_untrusted and not has_validate)
        else ("已声明处理外部输入且含校验逻辑" if has_untrusted else "未检出外部输入依赖"))

    # ---- 安全语义层（仅扫可执行文件，借鉴 skill-scanner/朱雀 + skill-vetter）----
    if not code_texts:
        add("语义层", "SEM", "可执行文件安全语义扫描", "INFO", "无 .py/.js/.sh 等可执行文件，跳过")
    else:
        m_dec = RE_ENC_DECODE.search(all_code_text)
        m_lit = RE_ENC_LITERAL.search(all_code_text)
        if m_dec:
            enc_status, enc_detail = "FAIL", f"疑似编码解码绕过: {m_dec.group(0)!r}"
        elif m_lit:
            enc_status, enc_detail = "WARN", (
                f"含字面转义 \\xNN/\\uNNNN: {m_lit.group(0)!r}（弱信号，确认非混淆指令）")
        else:
            enc_status, enc_detail = "PASS", "未检出 base64/ROT13 解码绕过"
        add("语义层", "ENC1", "编码绕过检测（base64/ROT13 解码）", enc_status, enc_detail)
        zw = RE_ZEROWIDTH.search(all_code_text)
        add("语义层", "ENC2", "零宽/不可见字符（Unicode 走私）",
            "FAIL" if zw else "PASS",
            f"命中不可见字符 U+{ord(zw.group(0)):04X}" if zw else "未检出零宽/不可见字符")
        m = RE_SENSITIVE_PATH.search(all_code_text)
        add("语义层", "SEN1", "敏感路径访问（ssh/aws/.env/记忆文件）",
            "WARN" if m else "PASS",
            f"疑似提及敏感路径: {m.group(0)!r}（弱信号，确认是否真实访问）" if m
            else "未检出 ~/.ssh/.aws/.env/记忆文件等访问")
        m = RE_IP_URL.search(all_code_text)
        add("语义层", "NET1", "裸 IP 外联（应走可信域名）",
            "WARN" if m else "PASS",
            f"裸 IP 外联: {m.group(0)!r}" if m else "未检出裸 IP 形式的网络调用")
        m = RE_PRIV.search(all_code_text)
        add("语义层", "PRIV1", "提权/管理员权限",
            "WARN" if m else "PASS",
            f"疑似提权: {m.group(0)!r}" if m else "未检出 sudo/runas/提权")
        # 未声明装包：脚本含 install 但目录无依赖清单
        m = RE_DEPS_INSTALL.search(all_code_text)
        has_manifest = any(
            s.lower().endswith(("requirements.txt", "package.json", "pyproject.toml",
                                 "pipfile", "environment.yml", "poetry.lock"))
            for s in siblings)
        add("语义层", "DEPS1", "依赖声明完整性（装包须声明）",
            "WARN" if (m and not has_manifest) else "PASS",
            f"含安装指令但无依赖清单: {m.group(0)!r}" if (m and not has_manifest)
            else ("含安装指令且已声明依赖清单" if m else "未检出运行时装包"))
        # 声明-能力一致性：声明只读却含写/执行能力
        claim_ro = bool(RE_READONLY_CLAIM.search(text))
        has_write = bool(RE_WRITE_OP.search(all_code_text))
        add("语义层", "CONS1", "声明-能力一致性（只读 vs 写/执行）",
            "WARN" if (claim_ro and has_write) else "PASS",
            "SKILL.md 声明只读/不写，但代码含写文件/执行/外发能力，存在声明与行为不符风险"
            if (claim_ro and has_write)
            else ("声明只读且未检出写/执行能力" if claim_ro else "未声明只读，本条不适用"))

        # 供应链投毒：下载即执行（curl|sh / wget|sh 等管道给 shell）
        m = RE_SUPPLY.search(all_code_text)
        add("语义层", "SUPPLY1", "供应链投毒（下载即执行 curl|sh 等）",
            "FAIL" if m else "PASS",
            f"疑似下载即执行: {m.group(0)!r}" if m else "未检出 curl|sh / wget|sh 等管道执行远程脚本")

    return results


# ---------------------------------------------------------------------------
# 报告
# ---------------------------------------------------------------------------

def score(results):
    counts = {"PASS": 0, "WARN": 0, "FAIL": 0, "INFO": 0}
    for r in results:
        counts[r[3]] = counts.get(r[3], 0) + 1
    decided = counts["PASS"] + counts["WARN"] + counts["FAIL"]
    pct = round(100 * (counts["PASS"] + 0.5 * counts["WARN"]) / decided) if decided else 0
    grade = "A" if pct >= 90 else "B" if pct >= 75 else "C" if pct >= 60 else "D"
    return counts, pct, grade


def render_text(results, counts, pct, grade, path):
    print(f"企业技能审查报告: {path}")
    print(f"{'='*60}")
    print(f"综合评分: {pct}/100  等级: {grade}  "
          f"[PASS {counts['PASS']} / WARN {counts['WARN']} / FAIL {counts['FAIL']} / INFO {counts['INFO']}]")
    print(f"{'='*60}")
    cur = None
    for cat, cid, name, status, detail in results:
        if cat != cur:
            cur = cat
            print(f"\n## {cat}")
        icon = {"PASS": "✅", "WARN": "⚠️ ", "FAIL": "❌", "INFO": "ℹ️ "}.get(status, "·")
        line = f"  [{cid}] {icon} {name} — {status}"
        if detail:
            line += f"\n        {detail}"
        print(line)
    print()
    if counts["FAIL"]:
        print("存在 FAIL，建议修复后再发布（CI 可据此卡点）。")
    else:
        print("无 FAIL。WARN 项建议人工确认后发布。")


def render_md(results, counts, pct, grade, path):
    out = [f"# 企业技能审查报告: {path}", ""]
    out.append(f"**综合评分**: {pct}/100 · **等级**: {grade} · "
               f"PASS {counts['PASS']} / WARN {counts['WARN']} / FAIL {counts['FAIL']} / INFO {counts['INFO']}")
    out.append("")
    cur = None
    for cat, cid, name, status, detail in results:
        if cat != cur:
            cur = cat
            out.append(f"## {cat}")
            out.append("")
            out.append("| ID | 检查项 | 状态 | 说明 |")
            out.append("|----|--------|------|------|")
        out.append(f"| {cid} | {name} | {status} | {detail or '-'} |")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="企业技能审查器")
    ap.add_argument("target", help="skill 目录或 SKILL.md 路径")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--md", action="store_true", help="输出 Markdown")
    args = ap.parse_args()

    try:
        text, d, siblings = load_skill(args.target)
    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 2

    results = check(text, d, siblings, args.target)
    counts, pct, grade = score(results)

    if args.json:
        payload = {
            "path": args.target,
            "score": pct, "grade": grade, "counts": counts,
            "checks": [
                {"category": c, "id": i, "name": n, "status": s, "detail": d2}
                for (c, i, n, s, d2) in results
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif args.md:
        print(render_md(results, counts, pct, grade, args.target))
    else:
        render_text(results, counts, pct, grade, args.target)

    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
