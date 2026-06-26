#!/usr/bin/env python3
"""OpenClaw content-extraction router.

This is an executable routing helper for the content-extraction skill.
It does not perform browser/Feishu/YouTube extraction itself; instead it
classifies input, builds an actionable plan, and emits a concrete extraction
spec that OpenClaw tools can execute.

Examples:
    python3 extract_router.py 'https://mp.weixin.qq.com/s/xxx'
    python3 extract_router.py --format json 'https://www.feishu.cn/docx/xxx'
    python3 extract_router.py --title 'My Article' 'https://example.com'
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from urllib.parse import urlparse


@dataclass
class RoutePlan:
    input_url: str
    source_type: str
    handler: str
    fallback_chain: list[str]
    notes: str
    save_name: str
    output_format: str
    extraction_steps: list[str]
    failure_modes: list[str]


WECHAT_RE = re.compile(r"mp\.weixin\.qq\.com", re.I)
FEISHU_RE = re.compile(r"(feishu\.cn|larksuite\.com)", re.I)
YOUTUBE_RE = re.compile(r"(youtube\.com|youtu\.be)", re.I)
FEISHU_WIKI_RE = re.compile(r"/wiki/|wiki=", re.I)
FEISHU_DOC_RE = re.compile(r"/docx?/|/(doc|docx)(\?|/)|table=", re.I)


def normalize_save_name(title: str | None, source_type: str) -> str:
    base = (title or "").strip() or source_type
    base = re.sub(r"[\\/:*?\"<>|]+", "_", base)
    base = re.sub(r"\s+", " ", base).strip()
    return base[:120] if base else source_type


def classify_url(url: str, title: str | None = None) -> RoutePlan:
    url = url.strip()
    parsed = urlparse(url)
    path = parsed.path or ""
    query = parsed.query or ""
    target = f"{path}?{query}"

    if WECHAT_RE.search(url):
        return RoutePlan(
            input_url=url,
            source_type="公众号",
            handler="browser",
            fallback_chain=["r.jina.ai", "defuddle.md", "web_fetch"],
            notes="公众号文章优先走浏览器抓取，处理反爬和动态内容。",
            save_name=normalize_save_name(title, "公众号"),
            output_format="markdown",
            extraction_steps=[
                "打开文章页面",
                "等待正文区域加载完成",
                "提取标题 / 作者 / 发布时间 / 正文 / 图片",
                "生成 Markdown + frontmatter",
            ],
            failure_modes=[
                "登录墙",
                "反爬白页",
                "正文容器缺失",
            ],
        )

    if FEISHU_RE.search(url):
        if FEISHU_WIKI_RE.search(target):
            source_type = "飞书知识库"
            extra = "wiki 先解析节点，再读取实际文档结构。"
        elif FEISHU_DOC_RE.search(target):
            source_type = "飞书文档"
            extra = "doc / docx 优先走原生 Feishu 工具。"
        else:
            source_type = "飞书内容"
            extra = "命中飞书域名但无法细分类型时，默认走 Feishu 工具。"
        return RoutePlan(
            input_url=url,
            source_type=source_type,
            handler="feishu",
            fallback_chain=["web_fetch"],
            notes=extra,
            save_name=normalize_save_name(title, source_type),
            output_format="markdown",
            extraction_steps=[
                "识别 doc / docx / wiki 类型",
                "wiki 先解析节点/文档 token",
                "读取结构化 blocks",
                "转换为 Markdown",
            ],
            failure_modes=[
                "权限不足",
                "doc token 无效",
                "wiki 节点解析失败",
                "API 鉴权/配额失败",
            ],
        )

    if YOUTUBE_RE.search(url):
        return RoutePlan(
            input_url=url,
            source_type="YouTube",
            handler="transcript",
            fallback_chain=["web_fetch"],
            notes="YouTube 交给 transcript 相关技能链。",
            save_name=normalize_save_name(title, "YouTube"),
            output_format="markdown",
            extraction_steps=[
                "检测是否存在 transcript",
                "读取字幕/转录文本",
                "按需整理成 Markdown",
            ],
            failure_modes=[
                "无 transcript",
                "视频无法访问",
            ],
        )

    return RoutePlan(
        input_url=url,
        source_type="网页",
        handler="proxy_cascade",
        fallback_chain=["r.jina.ai", "defuddle.md", "web_fetch"],
        notes="通用网页优先代理级联，失败后再走本地回退。",
        save_name=normalize_save_name(title, "网页"),
        output_format="markdown",
        extraction_steps=[
            "先用 r.jina.ai 去噪抽取",
            "失败则用 defuddle.md 结构化净化",
            "再失败则 web_fetch",
            "最后 browser fallback",
        ],
        failure_modes=[
            "JS 重渲染导致空白",
            "页面噪音过重",
            "抽取层只返回杂乱 HTML",
        ],
    )


def plan_to_markdown(plan: RoutePlan) -> str:
    lines = [
        f"**输入**: {plan.input_url}",
        f"**来源**: {plan.source_type}",
        f"**处理器**: {plan.handler}",
        f"**保存名**: {plan.save_name}",
        f"**输出格式**: {plan.output_format}",
        "",
        "### 执行步骤",
    ]
    lines.extend([f"- {step}" for step in plan.extraction_steps])
    lines.append("")
    lines.append("### 失败模式")
    lines.extend([f"- {mode}" for mode in plan.failure_modes])
    lines.append("")
    lines.append("### 降级链")
    lines.extend([f"- {step}" for step in plan.fallback_chain])
    lines.append("")
    lines.append(f"### 备注\n{plan.notes}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="OpenClaw content-extraction router")
    parser.add_argument("url", help="URL or document reference")
    parser.add_argument("--title", default=None, help="Optional title for save-name suggestion")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    plan = classify_url(args.url, args.title)
    if args.format == "json":
        print(json.dumps(asdict(plan), ensure_ascii=False, indent=2))
    else:
        print(plan_to_markdown(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
