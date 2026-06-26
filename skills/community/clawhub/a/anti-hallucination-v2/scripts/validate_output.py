#!/usr/bin/env python3
"""
Anti-Hallucination Output Validator
扫描AI输出，检测潜在幻觉信号。
用法: python validate_output.py <text>
或: echo "text" | python validate_output.py
"""
import sys
import re

# 禁止词 - 这些词通常表示AI在猜测
HEDGE_WORDS = [
    "通常", "一般来说", "应该是", "可能是", "大概是",
    "应该", "大概", "据我所知", "我记得", "我印象中",
    "理论上", "基本上", "差不多", "估计", "想必",
    "generally", "usually", "probably", "likely",
    "typically", "normally", "roughly", "about",
]

# 需要验证的信号
VERIFY_SIGNALS = {
    "date": r'\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日号]?',
    "percentage": r'\d+\.?\d*%',
    "money": r'[¥$€£]\d+\.?\d*|\d+\.?\d*[元万亿]',
    "url": r'https?://[^\s<>\"\']+',
    "function_call": r'\w+\.\w+\([^)]*\)',
    "file_path": r'[A-Za-z]:\\[^\s<>\"\']+|~/[^\s<>\"\']+|/[a-z][^\s<>\"\']+',
    "version": r'v?\d+\.\d+\.\d+',
    "api_endpoint": r'https?://[^\s<>\"\']+/api/[^\s<>\"\']*',
}


def scan_text(text: str) -> dict:
    """扫描文本，返回检测到的风险信号。"""
    results = {
        "hedge_words": [],
        "unverified_claims": [],
        "needs_verification": [],
    }

    # 检测禁止词
    for word in HEDGE_WORDS:
        if word.lower() in text.lower():
            results["hedge_words"].append(word)

    # 检测需要验证的信号
    for signal_type, pattern in VERIFY_SIGNALS.items():
        matches = re.findall(pattern, text)
        if matches:
            results["needs_verification"].append({
                "type": signal_type,
                "matches": matches[:5],  # 最多显示5个
            })

    return results


def format_report(results: dict) -> str:
    """格式化检测报告。"""
    lines = []

    if results["hedge_words"]:
        lines.append("⚠️ 禁止词检测:")
        for word in set(results["hedge_words"]):
            lines.append(f"  - {word}")
        lines.append("  → 建议: 这些词表示你在猜测，请用工具验证或标注'不确定'")
        lines.append("")

    if results["needs_verification"]:
        lines.append("🔍 需要验证的信号:")
        for item in results["needs_verification"]:
            lines.append(f"  [{item['type']}]")
            for match in item["matches"]:
                lines.append(f"    - {match}")
        lines.append("  → 建议: 这些内容需要通过工具/搜索验证后再输出")
        lines.append("")

    if not lines:
        lines.append("✅ 未检测到明显的幻觉风险信号")

    return "\n".join(lines)


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("用法: python validate_output.py <text>")
        print("  或: echo 'text' | python validate_output.py")
        sys.exit(1)

    results = scan_text(text)
    print(format_report(results))
