#!/usr/bin/env python3
"""
Chinese SEO Keyword Density Checker
Checks keyword density and placement for Chinese content across platforms.

Usage:
  python keyword_check.py --content "content text" --keywords "关键词1,关键词2" --platform baidu
  python keyword_check.py --file content.txt --keywords "关键词1,关键词2" --platform xiaohongshu
"""

import argparse
import re
import sys
from collections import Counter


def count_chinese_chars(text: str) -> int:
    """Count Chinese characters in text."""
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def count_keyword_occurrences(text: str, keyword: str) -> int:
    """Count keyword occurrences in text."""
    return text.count(keyword)


def check_title_keyword_placement(title: str, keyword: str, platform: str) -> dict:
    """Check if keyword is properly placed in title per platform rules."""
    result = {"keyword": keyword, "title": title, "platform": platform, "issues": []}

    if not keyword:
        result["issues"].append("未提供关键词")
        result["passed"] = False
        return result

    if keyword not in title:
        result["issues"].append(f"标题中未包含关键词「{keyword}」")
        result["passed"] = False
        return result

    # Find position of keyword in title
    pos = title.index(keyword)
    char_count_before = count_chinese_chars(title[:pos])

    if platform == "baidu":
        if char_count_before > 15:
            result["issues"].append(f"关键词出现在第{char_count_before+1}个中文字符后，建议在前15个字符内")
    elif platform == "xiaohongshu":
        if char_count_before > 10:
            result["issues"].append(f"小红书标题关键词应尽量靠前，当前在第{char_count_before+1}个字符后")

    title_len = count_chinese_chars(title)
    if platform == "baidu" and (title_len < 25 or title_len > 35):
        result["issues"].append(f"百度标题建议25-35字，当前{title_len}字")
    elif platform == "xiaohongshu" and title_len > 20:
        result["issues"].append(f"小红书标题建议20字以内，当前{title_len}字")

    result["passed"] = len(result["issues"]) == 0
    return result


def check_keyword_density(text: str, keywords: list[str], platform: str) -> dict:
    """Check keyword density for the content."""
    chinese_char_count = count_chinese_chars(text)
    if chinese_char_count == 0:
        return {"error": "内容中无中文字符"}

    results = {"total_chinese_chars": chinese_char_count, "keywords": [], "platform": platform}

    for kw in keywords:
        count = count_keyword_occurrences(text, kw)
        density = (count * len(kw)) / chinese_char_count * 100
        kw_result = {
            "keyword": kw,
            "count": count,
            "density": f"{density:.2f}%",
        }

        if platform == "baidu":
            if density < 2:
                kw_result["status"] = "偏低"
                kw_result["suggestion"] = "百度建议关键词密度2-4%"
            elif density > 4:
                kw_result["status"] = "过高"
                kw_result["suggestion"] = "关键词密度过高，可能被判定为堆砌"
            else:
                kw_result["status"] = "合适"
        else:
            kw_result["status"] = "info"
            kw_result["suggestion"] = "非百度平台无严格密度要求，自然融入即可"

        results["keywords"].append(kw_result)

    return results


def check_banned_words(text: str) -> list[dict]:
    """Check for common advertising law banned words."""
    banned_patterns = [
        (r"最好|最佳|最优|最强|最大|最高级|最便宜|最流行|最先进", "绝对化用语（广告法第九条）"),
        (r"全国第一|销量第一|排名第一|行业第一|NO\.1|No\.1", "第一/排名用语"),
        (r"极品|极致|顶级|顶尖|绝版", "极端化用语"),
        (r"独家|独创|独有|唯一", "排他性用语"),
        (r"绝对|绝无仅有|绝佳", "绝对化用语"),
        (r"首个|首选|首款|首次", "首字用语"),
        (r"万能|全能|包治|根治", "夸大效果用语"),
        (r"100%有效|百分之百|零风险", "绝对保证用语"),
        (r"治愈|根治|药到病除|疗效", "医疗效果承诺（非医疗产品禁用）"),
    ]

    violations = []
    for pattern, category in banned_patterns:
        matches = re.findall(pattern, text)
        if matches:
            violations.append({
                "category": category,
                "found_words": list(set(matches)),
                "suggestion": "请替换为更温和的表述，避免违反广告法"
            })

    return violations


def run_check(content: str, keywords: list[str], platform: str, title: str = "") -> dict:
    """Run all checks and return comprehensive report."""
    report = {"platform": platform}

    if title:
        report["title_check"] = check_title_keyword_placement(title, keywords[0] if keywords else "", platform)

    report["density_check"] = check_keyword_density(content, keywords, platform)
    report["banned_words_check"] = check_banned_words(content)

    # Content length check
    char_count = count_chinese_chars(content)
    length_advice = {}
    if platform == "baidu":
        if char_count < 1500:
            length_advice = {"status": "偏短", "suggestion": "百度竞争词建议1500-3000字", "current": char_count}
        else:
            length_advice = {"status": "合适", "current": char_count}
    elif platform == "xiaohongshu":
        if char_count > 500:
            length_advice = {"status": "偏长", "suggestion": "小红书笔记建议300-500字", "current": char_count}
        else:
            length_advice = {"status": "合适", "current": char_count}
    else:
        length_advice = {"current": char_count, "status": "info"}

    report["length_check"] = length_advice

    return report


def main():
    parser = argparse.ArgumentParser(description="Chinese SEO Keyword Density Checker")
    parser.add_argument("--content", help="Content text to check")
    parser.add_argument("--file", help="File containing content to check")
    parser.add_argument("--keywords", required=True, help="Comma-separated keywords")
    parser.add_argument("--platform", required=True, choices=["baidu", "xiaohongshu", "douyin", "taobao", "jd"], help="Target platform")
    parser.add_argument("--title", help="Title to check keyword placement", default="")

    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    elif args.content:
        content = args.content
    else:
        print("Error: Provide --content or --file")
        sys.exit(1)

    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    report = run_check(content, keywords, args.platform, args.title)

    import json
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
