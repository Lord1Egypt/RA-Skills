"""PITAX 规则元数据注册表 — 与官方 taxonomy v1.6.1 编号严格对齐。

编号对齐说明（重要）：
早期草稿曾使用 PIT-E21/T52/E39 等非官方编号，经与官方 taxonomy（172 节点）
逐条核对后全部修正为官方编号：
  不可见字符走私   → PIT-E-23 Invisible Text
  Bidi 源码欺骗    → PIT-E-54 Trojan Source（CVE-2021-42574）
  AI 配置文件后门  → PIT-T-46 Agent Instruction-File Injection（CVE-2025-53773）
  注释指令覆盖     → PIT-T-51 Instruction Override
  文档投毒         → PIT-N-06 Document / File Upload
  单层 Base64      → PIT-E-07 / ROT13 → PIT-E-14 / 反转 → PIT-E-36
  多层组合编码     → PIT-E-57 Layered Encoding

CWE / MITRE ATLAS 映射原则（硬红线：编号以官方为准，不编造）：
- 本平台规则全部以“代码/文档作为载体、被 LLM 读取后间接生效”为特征，
  对应 MITRE ATLAS 的 **Indirect** LLM Prompt Injection 子技术。
- **已核实（2026-09-11，基于 atlas-data 官方仓库 dist/ATLAS.yaml）**：
    AML.T0051.000 = Direct（攻击者直接作为用户注入）
    AML.T0051.001 = **Indirect**（经 LLM 常规处理的数据通道注入，「本平台适用」）
    AML.T0051.002 = Triggered（由用户动作/系统事件触发）
  → 因此本平台全部规则统一映射 **AML.T0051.001**。
  ⚠️ 曾一度误改为 .002（基于命名猜测），已根据官方数据回退，勿再改。
- CWE 仅在 NVD 有明确官方分类时标注，无官方对应时宁可留空，不硬凑。

⚠️ CVE-2025-53773 核实记录（2026-09-11，已查 NVD + 原研究）：
此 CVE **真实存在且与本规则直接相关**，描述为“GitHub Copilot / Visual Studio
命令注入（CVSS 7.8）”，攻击链正是“源码/文档中的提示注入 → 向 .vscode/settings.json
写入 chat.tools.autoApprove:true → Copilot YOLO 模式 → 本地 RCE”。
→ 故 PIT-T-46 保留此 CVE 引用。
⚠️ 教训：曾因外部评审误称“此 CVE 实为 SharePoint ToolShell”而一度
将其删除，经查证为**误判**，已恢复。**CVE 编号必须逐个查 NVD 验证，不得凭记忆或
二手结论修改。**

Based on the Arcanum Prompt Injection Taxonomy by Jason Haddix,
Arcanum Information Security (arcanum-sec.com). CC BY 4.0.
Citation: Haddix, J. (2026). Arcanum Prompt Injection Taxonomy (v1.6.1).
"""

PITAX_VERSION = "1.6.1"
PITAX_SOURCE = "https://github.com/Arcanum-Sec/arc_pi_taxonomy"
PITAX_REPO = "https://github.com/Arcanum-Sec/arc_pi_taxonomy"

PITAX_RULES: dict[str, dict] = {
    # ── 高价值主规则 1: 不可见字符走私 ──
    "PIT-E-23": {
        "name": "Invisible Text",
        "pillar": "evasion",
        "aliases": [
            "ASCII Smuggling", "Invisible Unicode", "Zero-Width Characters",
            "Unicode Tag Injection", "Hidden Instruction Characters",
        ],
        "severity": "high",
        "delivery": "either",
        "mitre_atlas": "AML.T0051.001",
        "description": (
            "使用零宽字符、软连字符、U+E0000 标签字符等人类阅读不可见、"
            "但 LLM 会解析的 Unicode 字符，在代码/文档中走私恶意指令。"
        ),
        "references": [f"{PITAX_SOURCE}#PIT-E-23", PITAX_REPO],
    },
    # ── 高价值主规则 2: Trojan Source（Bidi 源码欺骗）──
    "PIT-E-54": {
        "name": "Trojan Source",
        "pillar": "evasion",
        "aliases": ["Bidi Override", "Source Code Visual Spoofing"],
        "severity": "high",
        "delivery": "either",
        "cve": "CVE-2021-42574",
        "description": (
            "使用双向文本控制符（U+202A–U+202E、U+2066–U+2069）改变源码的"
            "视觉呈现顺序，使代码'看起来'的逻辑与编译器/LLM 实际解析的逻辑不一致。"
            "同时影响人类评审与 AI 编码助手。"
        ),
        "references": [
            f"{PITAX_SOURCE}#PIT-E-54",
            "https://trojansource.codes/",
            "https://nvd.nist.gov/vuln/detail/CVE-2021-42574",
            PITAX_REPO,
        ],
    },
    # ── 高价值主规则 3: AI 配置文件后门 ──
    "PIT-T-46": {
        "name": "Agent Instruction-File Injection",
        "pillar": "technique",
        "aliases": [
            "Cursor Rules Backdoor", "Copilot Instructions Hijack",
            "AI Config Injection", "CLAUDE.md Backdoor",
        ],
        "severity": "critical",
        "delivery": "input",
        "cve": "CVE-2025-53773",
        "cwe": "CWE-77",
        "mitre_atlas": "AML.T0051.001",
        "description": (
            "在 .cursor/rules、CLAUDE.md、copilot-instructions.md、.vscode/settings.json 等"
            "AI 助手指令/配置文件（或源码/文档中）植入指令覆盖/角色劫持后门，"
            "劫持所有使用该仓库的 AI 编码助手。真实案例：CVE-2025-53773，"
            "提示注入诱使 GitHub Copilot 向 .vscode/settings.json 写入 "
            "chat.tools.autoApprove:true 开启 YOLO 模式，进而实现本地 RCE。"
        ),
        "references": [
            f"{PITAX_SOURCE}#PIT-T-46",
            "https://nvd.nist.gov/vuln/detail/CVE-2025-53773",
            "https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/",
            PITAX_REPO,
        ],
    },
    # ── 高价值主规则 4: 注释指令覆盖 ──
    "PIT-T-51": {
        "name": "Instruction Override",
        "pillar": "technique",
        "aliases": ["Comment Prompt Injection", "Indirect Prompt Injection"],
        "severity": "high",
        "delivery": "input",
        "mitre_atlas": "AML.T0051.001",
        "description": (
            "在代码注释中嵌入提示注入指令（如 ignore previous instructions），"
            "当 LLM 阅读代码/注释时被劫持执行非预期指令。"
        ),
        "references": [f"{PITAX_SOURCE}#PIT-T-51", PITAX_REPO],
    },
    # ── 文档投毒（README / 设计文档面向 AI Agent 场景）──
    "PIT-N-06": {
        "name": "Document / File Upload",
        "pillar": "input",
        "aliases": ["README Poisoning", "Docs Prompt Injection"],
        "severity": "high",
        "delivery": "input",
        "mitre_atlas": "AML.T0051.001",
        "description": (
            "在 README、设计文档等项目文档中植入面向 AI Agent 的恶意指令。"
            "文档是 Agent 的常规输入（PIT-N-06），而文档投毒不会被传统工具检出。"
        ),
        "references": [f"{PITAX_SOURCE}#PIT-N-06", PITAX_REPO],
    },
    # ── 编码类：单层子类 + 多层组合 ──
    "PIT-E-07": {
        "name": "Base64 Encoding",
        "pillar": "evasion",
        "aliases": ["Base64 Smuggling"],
        "severity": "medium",
        "delivery": "either",
        "mitre_atlas": "AML.T0051.001",
        "description": "字符串常量中检测到 Base64 编码的提示注入载荷。",
        "references": [f"{PITAX_SOURCE}#PIT-E-07", PITAX_REPO],
    },
    "PIT-E-14": {
        "name": "Cipher (ROT13)",
        "pillar": "evasion",
        "aliases": ["ROT13 Smuggling"],
        "severity": "medium",
        "delivery": "either",
        "mitre_atlas": "AML.T0051.001",
        "description": "字符串常量中检测到 ROT13 凯撒移位编码的提示注入载荷。",
        "references": [f"{PITAX_SOURCE}#PIT-E-14", PITAX_REPO],
    },
    "PIT-E-36": {
        "name": "Reverse",
        "pillar": "evasion",
        "aliases": ["Reversed Text", "String Reversal Evasion"],
        "severity": "medium",
        "delivery": "either",
        "mitre_atlas": "AML.T0051.001",
        "description": "字符串常量反转后检测到提示注入载荷，用于规避关键词过滤。",
        "references": [f"{PITAX_SOURCE}#PIT-E-36", PITAX_REPO],
    },
    "PIT-E-57": {
        "name": "Layered Encoding",
        "pillar": "evasion",
        "aliases": ["Multi-layer Encoding", "Base64+ROT13 Chaining"],
        "severity": "critical",
        "delivery": "either",
        "mitre_atlas": "AML.T0051.001",
        "description": (
            "字符串常量中检测到多层组合编码（Base64→ROT13→反转等，≥2 层）的"
            "提示注入载荷，专门用于绕过基于关键词的过滤器。"
        ),
        "references": [f"{PITAX_SOURCE}#PIT-E-57", PITAX_REPO],
    },
}

# 4 条高价值规则（演示/文档排序用）
PRIMARY_RULES = ["PIT-E-23", "PIT-T-46", "PIT-T-51", "PIT-E-57"]
# 全部已实现规则（stats/CI 展示用）
ALL_RULES = [
    "PIT-E-23", "PIT-E-54", "PIT-T-46", "PIT-T-51", "PIT-N-06",
    "PIT-E-07", "PIT-E-14", "PIT-E-36", "PIT-E-57",
]

_FALLBACK_RULE = {
    "name": "Unknown PITAX Rule", "pillar": "unknown", "aliases": [],
    "severity": "medium", "description": "",
    "references": [PITAX_SOURCE],
}


def get_rule(code: str) -> dict:
    return PITAX_RULES.get(code, {**_FALLBACK_RULE, "name": code})
