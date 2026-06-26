#!/usr/bin/env python3
"""
sycophancy-transform.py
将确认式句式自动转换为开放性问题
遵循 "Ask Don't Tell" 原则 (ArXiv 2602.23971)

输入: JSON {"originalUserPromptText": "..."} (通过 stdin)
输出: 转换后的纯文本 prompt
"""

import sys
import json
import re


def transform(text: str) -> str:
    """将确认式句式转换为开放性问题。"""
    original = text

    # 命令式前缀列表（这些开头的句子不追加质疑后缀）
    cmd_prefixes = [
        "帮我", "请", "能不能", "可以帮我", "麻烦", "劳驾", "写", "修改",
        "创建", "删除", "修复", "优化", "改进", "重写", "实现", "检查",
        "查看", "分析", "告诉我", "生成", "编译", "运行", "解释", "翻译",
        "总结", "概括", "对比", "比较", "列出", "查找", "搜索"
    ]
    is_command = any(text.lstrip().startswith(p) for p in cmd_prefixes)

    # 质疑性词汇（已有这些词汇的陈述句不追加）
    critical_words = [
        "问题", "风险", "漏洞", "反例", "质疑", "挑战",
        "反驳", "批评", "局限", "缺陷", "薄弱"
    ]
    has_critical = any(w in text for w in critical_words)

    did_transform = False

    # =============================================
    # 规则9: "X 是对的，对吧？" → "X 真的正确吗？反对意见是什么？"
    # =============================================
    for pat in [
        r"(.+)是对的，对吧[？?]$",
        r"(.+)是正确的，对吧[？?]$",
        r"(.+)是对的[，,。]?对吧[？?]$",
        r"(.+)是正确的[，,。]?对吧[？?]$",
    ]:
        m = re.search(pat, text)
        if m:
            text = text[:m.start()] + f"{m.group(1)} 真的正确吗？反对意见是什么？"
            did_transform = True
            break

    # =============================================
    # 规则10: "帮我 X，应该没问题吧？" → "帮我 X，请同时指出潜在问题。"
    # =============================================
    if not did_transform:
        m = re.search(r"(帮我.+?)应该没问题吧[？?]$", text)
        if m:
            prefix = m.group(1).rstrip("，,。")
            text = text[:m.start()] + prefix + "，请同时指出潜在问题。"
            did_transform = True

    # =============================================
    # 规则8: "应该没问题吧？" → "有哪些可能的失败场景？"
    # =============================================
    if not did_transform:
        new_text = re.sub(r"应该没问题吧[？?]$", "有哪些可能的失败场景？", text)
        if new_text != text:
            text = new_text
            did_transform = True

    # =============================================
    # 规则7: "这不是 X 吗？" → "这真的是 X 吗？有什么不同的角度？"
    # =============================================
    if not did_transform:
        m = re.search(r"这不是(.+?)[吗嘛\?]+", text)
        if m:
            text = text[:m.start()] + f"这真的是{m.group(1)}吗？有什么不同的角度？"
            did_transform = True

    # =============================================
    # 规则6: "我觉得 X，对吗？" / "我认为 X，对吧？"
    # =============================================
    if not did_transform:
        m = re.search(r"(我觉得|我认为|我觉着)(.+?)，对[吗嘛吧\?]", text)
        if m:
            content = m.group(2)
            text = text[:m.start()] + content + " 真的成立吗？有没有反例或例外情况？"
            did_transform = True

    # =============================================
    # 规则4: 末尾 "这样对吧？" → "这样做有什么潜在问题？"
    # =============================================
    if not did_transform:
        text = re.sub(r"这样对吧[？?]$", "这样做有什么潜在问题？", text)

    # =============================================
    # 规则1: 末尾 "对吧？" → "有什么问题？"
    # =============================================
    text = re.sub(r"对吧[？?]$", "有什么问题？", text)

    # =============================================
    # 规则2: 末尾 "没问题吧？" → "有什么潜在问题？"
    # =============================================
    text = re.sub(r"没问题吧[？?]$", "有什么潜在问题？", text)

    # =============================================
    # 规则3: 末尾 "没错吧？" → "有什么漏洞？"
    # =============================================
    text = re.sub(r"没错吧[？?]$", "有什么漏洞？", text)

    # =============================================
    # 规则5: "这样做...对吧？" (中间有内容，非开头) → "X 有什么问题？"
    # =============================================
    if not original.startswith("这样做") and re.search(r"对吧[？?]$", text):
        text = re.sub(r"对吧[？?]$", "有什么问题？", text)

    # =============================================
    # 规则11: 末尾 "可以吧？" / "行吧？" → "有什么风险？"
    # =============================================
    text = re.sub(r"[可以行]吧[？?]$", "有什么风险？", text)

    # =============================================
    # 规则12: 末尾 "这样可以吗？" → "这样做有什么风险？有没有更好的方案？"
    # =============================================
    text = re.sub(r"这样做可以吗[？？]$", "这样做有什么风险？有没有更好的方案？", text)

    # =============================================
    # 规则13: 末尾以"吧"结尾的确认式陈述 → 追加批判邀请
    # =============================================
    starts_with_question_word = re.search(r"^[怎么为什么如何怎样谁哪里什么]", text)
    ends_with_ba = re.search(r"吧$", text)
    if (ends_with_ba and not is_command and not has_critical
            and not starts_with_question_word):
        text = text + "（请先指出这个方案最薄弱的 2 个环节。）"

    # =============================================
    # 规则14: 纯肯定式陈述句（末尾为句号/感叹号）→ 追加批判邀请
    # =============================================
    starts_with_question_word = re.search(r"^[怎么为什么如何怎样谁哪里什么]", text)
    if (re.search(r"[。！]$", text) and not is_command and not has_critical
            and not starts_with_question_word):
        text = text + "（请先指出这个方案最薄弱的 2 个环节。）"

    return text


def main():
    try:
        data = json.load(sys.stdin)
        text = data.get("originalUserPromptText", "")
    except (json.JSONDecodeError, UnicodeDecodeError, KeyError):
        try:
            sys.stdout.write(sys.stdin.read())
        except:
            pass
        return

    if not text:
        sys.stdout.write("")
        return

    sys.stdout.write(transform(text))


if __name__ == "__main__":
    main()
