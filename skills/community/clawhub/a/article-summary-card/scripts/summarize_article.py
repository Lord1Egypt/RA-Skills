#!/usr/bin/env python3
import argparse
import html
from html.parser import HTMLParser
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


COMMON_STOPWORDS = {
    "的", "了", "和", "是", "在", "就", "都", "而", "及", "与", "着", "或", "一个",
    "我们", "你", "我", "也", "把", "让", "并", "中", "对", "到", "用", "它", "这",
    "那", "可以", "就是", "不是", "一个", "进行", "通过", "以及", "如果", "需要",
    "技能", "文章", "作者", "目前", "这个", "这些", "还有", "已经", "因为", "所以",
}

NOISY_PATTERNS = (
    "github",
    "skills.sh",
    "chrome 商店",
    "edge 商店",
    "在线版",
    "npx ",
    "github 地址",
    "安装",
    "商店",
    "LICENSE",
    "input.md",
    "output.md",
    "template",
    "resources/",
)


class BlockTextExtractor(HTMLParser):
    block_tags = {"h1", "h2", "h3", "h4", "p", "li", "blockquote", "pre"}

    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag in self.block_tags:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style"} and self.skip_depth:
            self.skip_depth -= 1
            return
        if self.skip_depth:
            return
        if tag in self.block_tags:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.skip_depth:
            return
        text = " ".join(data.split())
        if text:
            self.parts.append(text)


def run_curl(url: str) -> str:
    commands = [
        [
            "curl",
            "-L",
            "--silent",
            "--show-error",
            "-A",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            url,
        ],
        [
            "curl",
            "-L",
            "--silent",
            "--show-error",
            "--http1.1",
            "-A",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            url,
        ],
    ]
    last_error = None
    for command in commands:
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            return result.stdout
        except subprocess.CalledProcessError as exc:
            last_error = exc
    raise last_error


def extract_title(raw_html: str) -> str:
    match = re.search(r"<title>(.*?)</title>", raw_html, re.I | re.S)
    if not match:
        return "未命名文章"
    title = html.unescape(match.group(1))
    title = re.sub(r"\s*-\s*掘金\s*$", "", title)
    return " ".join(title.split())


def slice_article_fragment(raw_html: str) -> str:
    site_specific = [
        (r'<div id="article-root".*?<div class="article-viewer markdown-body cache result">', r'<div id="article-suspended-panel"'),
        (r'<article[^>]*>', r'</article>'),
        (r'<main[^>]*>', r'</main>'),
        (r'<body[^>]*>', r'</body>'),
    ]
    for start_pat, end_pat in site_specific:
        start = re.search(start_pat, raw_html, re.I | re.S)
        if not start:
            continue
        end = re.search(end_pat, raw_html[start.end():], re.I | re.S)
        if end:
            return raw_html[start.end(): start.end() + end.start()]
    return raw_html


def extract_text(raw_html: str) -> str:
    fragment = slice_article_fragment(raw_html)
    parser = BlockTextExtractor()
    parser.feed(fragment)
    text = " ".join(parser.parts)
    text = html.unescape(text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_sentences(text: str):
    raw = re.split(r"(?<=[。！？!?])\s+|\n+", text)
    sentences = []
    for sentence in raw:
        sentence = sentence.strip(" \n\t-")
        lowered = sentence.lower()
        if len(sentence) >= 12 and not any(pattern in lowered for pattern in NOISY_PATTERNS):
            sentences.append(sentence)
    return sentences


def extract_keywords(sentences, top_n=12):
    words = re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z][A-Za-z0-9.+-]{2,}", "".join(sentences))
    counts = Counter(word for word in words if word not in COMMON_STOPWORDS)
    return [word for word, _ in counts.most_common(top_n)]


def score_sentence(sentence, keywords, index):
    score = 0
    for keyword in keywords:
        score += sentence.count(keyword) * 2
    if "skills" in sentence.lower():
        score += 3
    if index < 18:
        score += 4
    if any(token in sentence for token in ("简单来说", "核心", "本质", "就是", "意味着", "未来")):
        score += 3
    if any(token in sentence for token in ("安装", "命令", "Github", "skills.sh", "作品推荐")):
        score -= 6
    if len(sentence) > 120:
        score -= 1
    return score


def build_summary(title: str, source: str, text: str):
    sentences = split_sentences(text)
    if not sentences:
        raise ValueError("No article text extracted.")

    keywords = extract_keywords(sentences)
    ranked = sorted(
        enumerate(sentences),
        key=lambda item: score_sentence(item[1], keywords, item[0]),
        reverse=True,
    )

    one_sentence = ranked[0][1]
    if len(one_sentence) > 88:
        one_sentence = one_sentence[:88].rstrip("，、；： ") + "。"

    seen = set()
    key_points = []
    for _, sentence in ranked:
        normalized = sentence.strip()
        if normalized in seen:
            continue
        seen.add(normalized)
        if len(normalized) > 120:
            normalized = normalized[:118].rstrip("，、；： ") + "。"
        key_points.append(normalized)
        if len(key_points) == 5:
            break

    return {
        "title": title,
        "source": source,
        "one_sentence": one_sentence,
        "sections": [
            {
                "heading": "核心事实",
                "summary": one_sentence,
                "points": key_points[:2],
            },
            {
                "heading": "关键信息",
                "summary": "文章的主要信息点和判断被压缩为便于手机端阅读的短条目。",
                "points": key_points[2:5],
            },
        ],
        "closing_takeaway": "这篇文章最值得记住的是核心事实、争议焦点和作者判断，而不是过程细节。",
    }


def normalize_summary(summary, title: str, source: str):
    normalized = {
        "title": str(summary.get("title") or title).strip(),
        "source": source,
        "one_sentence": str(summary.get("one_sentence") or "").strip(),
        "sections": [],
        "closing_takeaway": str(summary.get("closing_takeaway") or "").strip(),
    }

    if normalized["title"] == "":
        normalized["title"] = title

    if normalized["one_sentence"] == "":
        normalized["one_sentence"] = "文章的核心观点需要结合正文重新提炼。"

    sections = summary.get("sections")
    if isinstance(sections, list):
        for item in sections[:4]:
            if not isinstance(item, dict):
                continue
            heading = str(item.get("heading", "")).strip()
            section_summary = str(item.get("summary", "")).strip()
            points = []
            for point in item.get("points", [])[:3]:
                point_text = str(point).strip()
                if point_text:
                    points.append(point_text)
            if heading and (section_summary or points):
                normalized["sections"].append(
                    {
                        "heading": heading,
                        "summary": section_summary,
                        "points": points,
                    }
                )

    if not normalized["sections"]:
        key_points = [str(item).strip() for item in summary.get("key_points", []) if str(item).strip()]
        why_items = [str(item).strip() for item in summary.get("why_it_matters", []) if str(item).strip()]
        if key_points:
            normalized["sections"].append(
                {
                    "heading": "核心要点",
                    "summary": normalized["one_sentence"],
                    "points": key_points[:4],
                }
            )
        if why_items:
            normalized["sections"].append(
                {
                    "heading": "为什么值得关注",
                    "summary": "",
                    "points": why_items[:3],
                }
            )

    if not normalized["closing_takeaway"]:
        if isinstance(summary.get("why_it_matters"), list) and summary["why_it_matters"]:
            normalized["closing_takeaway"] = str(summary["why_it_matters"][0]).strip()
        else:
            normalized["closing_takeaway"] = normalized["one_sentence"]

    return normalized


def read_input(url: str | None, file_path: str | None):
    if url:
        raw_html = run_curl(url)
        title = extract_title(raw_html)
        text = extract_text(raw_html)
        return title, url, text
    if file_path:
        path = Path(file_path)
        text = path.read_text(encoding="utf-8")
        return path.stem, str(path), text
    raise ValueError("Either --url or --file is required.")


def main():
    parser = argparse.ArgumentParser(description="Summarize an article into structured JSON.")
    parser.add_argument("--url", help="Article URL")
    parser.add_argument("--file", help="Local text/markdown file")
    parser.add_argument("--out", required=True, help="Path to output summary JSON")
    parser.add_argument(
        "--mode",
        choices=["heuristic"],
        default="heuristic",
        help="Draft generation mode. Preferred final workflow is session summarization plus render_card.py.",
    )
    args = parser.parse_args()

    print(
        "Note: summarize_article.py is a draft helper. "
        "Preferred workflow is extract_article.py -> in-session two-round summary -> render_card.py.",
        file=sys.stderr,
    )

    title, source, text = read_input(args.url, args.file)
    summary = build_summary(title, source, text)

    summary = normalize_summary(summary, title=title, source=source)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
