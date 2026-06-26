#!/usr/bin/env python3
"""
Web search powered by DashScope (Qwen).
API key is read from DASHSCOPE_API_KEY environment variable.

Usage:
  python3 web_search.py "query"                          # Quick search
  python3 web_search.py --deep "query"                   # Deep search (multi-source)
  python3 web_search.py --agent "query"                  # Multi-round search
  python3 web_search.py --think "query"                  # Deep thinking + search
  python3 web_search.py --images "query"                 # Text + image mixed output
  python3 web_search.py --fresh 7 "query"                # Only last N days (7/30/180/365)
  python3 web_search.py --sites "arxiv.org,github.com" "query"  # Restrict to sites
"""
import sys
import os
import argparse
import re

API_KEY = os.environ.get("DASHSCOPE_API_KEY")
if not API_KEY:
    print("Error: DASHSCOPE_API_KEY not set.", file=sys.stderr)
    sys.exit(1)

BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_DEFAULT = "qwen3.5-plus"
MODEL_IMAGES = "qwen-plus-latest"


def convert_html_images_to_markdown(text):
    """Convert HTML <img> tags to Markdown ![](url) format."""
    pattern = r'<img\s+src="([^"]+)"\s+alt="([^"]*)"[^>]*>'
    replacement = r'![\2](\1)'
    text = re.sub(pattern, replacement, text)
    text = re.sub(r'<p\s+align="center">\s*', '', text)
    text = re.sub(r'</p>', '', text)
    return text


def search(query, strategy="turbo", freshness=None, sites=None,
           think=False, images=False):
    from openai import OpenAI
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    model = MODEL_IMAGES if images else MODEL_DEFAULT
    extra_body = {}

    if images and not strategy == "turbo":
        extra_body["enable_text_image_mixed"] = True
        extra_body["enable_search"] = True
        extra_body["search_options"] = {
            "search_strategy": strategy,
            "forced_search": True,
            "enable_source": True,
            "enable_citation": True,
            "enable_search_extension": True,
        }
    elif images:
        extra_body["enable_text_image_mixed"] = True
        extra_body["enable_search"] = True
        extra_body["search_options"] = {
            "forced_search": True,
            "enable_source": True,
            "enable_citation": True,
            "enable_search_extension": True,
        }
        if freshness:
            extra_body["search_options"]["freshness"] = freshness
        if sites:
            extra_body["search_options"]["assigned_site_list"] = sites
    else:
        search_options = {
            "search_strategy": strategy,
            "forced_search": True,
            "enable_source": True,
            "enable_citation": True,
            "enable_search_extension": True,
        }
        if freshness and strategy == "turbo":
            search_options["freshness"] = freshness
        if sites and strategy == "turbo":
            search_options["assigned_site_list"] = sites
        extra_body["enable_search"] = True
        extra_body["search_options"] = search_options

    if think:
        extra_body["enable_thinking"] = True

    messages = [{"role": "user", "content": query}]

    if think:
        completion = client.chat.completions.create(
            model=model, messages=messages,
            extra_body=extra_body, stream=True,
            stream_options={"include_usage": True},
        )
        reasoning, answer = [], []
        for chunk in completion:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                reasoning.append(delta.reasoning_content)
            elif delta.content:
                answer.append(delta.content)
        result = "".join(answer)
        if reasoning:
            result = "<thinking>\n" + "".join(reasoning) + "\n</thinking>\n\n" + result
        return result
    else:
        completion = client.chat.completions.create(
            model=model, messages=messages, extra_body=extra_body,
        )
        return completion.choices[0].message.content


def main():
    p = argparse.ArgumentParser(description="Web search via DashScope Qwen")
    p.add_argument("query", nargs="+")
    p.add_argument("--deep", action="store_true", help="Max strategy (thorough)")
    p.add_argument("--agent", action="store_true", help="Agent strategy (multi-round)")
    p.add_argument("--think", action="store_true", help="Deep thinking before answer")
    p.add_argument("--images", action="store_true", help="Include images in response")
    p.add_argument("--fresh", type=int, choices=[7, 30, 180, 365], default=None)
    p.add_argument("--sites", type=str, default=None)

    args = p.parse_args()
    query = " ".join(args.query)
    strategy = "max" if args.deep else "agent" if args.agent else "turbo"
    sites = [s.strip() for s in args.sites.split(",") if s.strip()] if args.sites else None

    try:
        result = search(query, strategy=strategy, freshness=args.fresh,
                        sites=sites, think=args.think, images=args.images)
        if args.images:
            result = convert_html_images_to_markdown(result)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
