"""PITAX 规则的英文描述层（IC27 合规：提交材料全英文，产品须以英语为表征语言之一）。

规则原文（rules.py）保持中文不动；本模块只提供 code → 英文描述 的映射，
`Finding.to_report_dict` 在 `ARCA_REPORT_LANG=en` 时取用。默认（未设）一切不变。
语言闸单一数据源 = codeark.report_lang.is_en()（2026-11-07 收口，原两处重复 env 判断退役）。
"""
from __future__ import annotations

from .report_lang import is_en

RULE_DESCRIPTIONS_EN: dict[str, str] = {
    "PIT-E-23": (
        "Uses zero-width characters, soft hyphens, U+E0000 tag characters and other Unicode that is "
        "invisible to humans but parsed by LLMs, smuggling malicious instructions into code or documents."
    ),
    "PIT-E-54": (
        "Uses bidirectional text control characters (U+202A-U+202E, U+2066-U+2069) to change the visual "
        "order of source code, so that what the code looks like differs from what the compiler or an "
        "LLM actually reads (CVE-2021-42574, trojansource.codes)."
    ),
    "PIT-T-46": (
        "Plants instruction-override or role-hijack directives in AI assistant configuration files "
        "(.cursor/rules, CLAUDE.md, copilot-instructions.md, .vscode/settings.json, ...), backdooring "
        "the repository's AI assistant (same attack pattern as CVE-2025-53773)."
    ),
    "PIT-T-51": (
        "Embeds prompt-injection instructions in code comments (e.g. 'ignore previous instructions'); "
        "an LLM reading the code or comments can be hijacked into unintended actions."
    ),
    "PIT-N-06": (
        "Plants instructions aimed at AI agents in project documents (README, design docs). Documents "
        "are routine agent input; poisoning them is invisible to human review and traditional tools."
    ),
    "PIT-E-07": "A Base64-encoded prompt-injection payload was found in a string constant.",
    "PIT-E-14": "A ROT13 (Caesar-shift) encoded prompt-injection payload was found in a string constant.",
    "PIT-E-36": (
        "A reversed string that decodes to a prompt-injection payload, used to evade keyword filters."
    ),
    "PIT-E-57": (
        "A multi-layer encoded payload (base64/ROT13/reverse, 2+ layers) that decodes to a "
        "prompt-injection instruction; built to bypass keyword-based filters."
    ),
}

SUGGESTION_EN = (
    "Remove the hidden content / malicious instruction. If this is a false positive, mark an "
    "exemption in CI and document the reason."
)


def description_for(code: str, fallback: str) -> str:
    """ARCA_REPORT_LANG=en → 英文；默认中文原文。"""
    return RULE_DESCRIPTIONS_EN.get(code, fallback) if is_en() else fallback


def suggestion_for(fallback: str) -> str:
    return SUGGESTION_EN if is_en() else fallback