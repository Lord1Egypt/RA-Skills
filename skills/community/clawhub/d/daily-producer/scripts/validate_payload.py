#!/usr/bin/env python3
"""
校验日报 JSON 是否符合渲染器契约。
大模型生成 JSON 后必须跑一遍，不通过就报错让它改。

用法：
    python3 scripts/validate_payload.py output/daily/2026-04-05.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def validate(data: dict) -> tuple[list[str], list[str]]:
    """校验日报 JSON，返回 (错误列表, 告警列表)。"""
    errors = []
    warnings = []

    # ━━ meta ━━
    meta = data.get("meta")
    if not meta:
        errors.append("[meta] 缺失")
    else:
        for field in ("date", "date_label", "role"):
            if not meta.get(field):
                errors.append(f"[meta.{field}] 缺失或为空")
        date = meta.get("date", "")
        if date and len(date) != 10:
            errors.append(f"[meta.date] 格式应为 YYYY-MM-DD，当前: {date}")

    # ━━ left_sidebar ━━
    sidebar = data.get("left_sidebar")
    if not sidebar:
        errors.append("[left_sidebar] 缺失")
    else:
        overview = sidebar.get("overview")
        if not overview or not isinstance(overview, list):
            errors.append("[left_sidebar.overview] 缺失或不是数组")
        elif len(overview) < 2:
            errors.append(f"[left_sidebar.overview] 至少 2 条，当前 {len(overview)} 条")
        else:
            for i, item in enumerate(overview):
                if not item.get("title"):
                    errors.append(f"[left_sidebar.overview[{i}].title] 缺失")
                if not item.get("text"):
                    errors.append(f"[left_sidebar.overview[{i}].text] 缺失")

        actions = sidebar.get("actions")
        if not actions or not isinstance(actions, list):
            errors.append("[left_sidebar.actions] 缺失或不是数组")
        elif len(actions) < 2:
            errors.append(f"[left_sidebar.actions] 至少 2 条，当前 {len(actions)} 条")
        else:
            valid_types = {"learn", "try", "watch", "alert"}
            for i, item in enumerate(actions):
                if not item.get("text"):
                    errors.append(f"[left_sidebar.actions[{i}].text] 缺失")
                if not item.get("prompt"):
                    errors.append(f"[left_sidebar.actions[{i}].prompt] 缺失")
                if item.get("type") and item["type"] not in valid_types:
                    errors.append(f"[left_sidebar.actions[{i}].type] 无效: {item['type']}，应为 {valid_types}")

        trends = sidebar.get("trends")
        if not trends:
            errors.append("[left_sidebar.trends] 缺失")
        else:
            for field in ("rising", "cooling", "steady"):
                if not trends.get(field) or not isinstance(trends[field], list):
                    errors.append(f"[left_sidebar.trends.{field}] 缺失或不是数组")
            if not trends.get("insight"):
                errors.append("[left_sidebar.trends.insight] 缺失")

    # ━━ articles ━━
    articles = data.get("articles")
    if not articles or not isinstance(articles, list):
        errors.append("[articles] 缺失或不是数组")
    elif len(articles) < 5:
        errors.append(f"[articles] 至少 5 条，当前 {len(articles)} 条")
    else:
        valid_priorities = {"major", "notable", "normal", "minor"}
        seen_ids = set()
        for i, article in enumerate(articles):
            prefix = f"[articles[{i}]]"

            for field in ("id", "title", "priority", "source", "url"):
                if not article.get(field):
                    errors.append(f"{prefix}.{field} 缺失或为空")

            aid = article.get("id", "")
            if aid in seen_ids:
                errors.append(f"{prefix}.id 重复: {aid}")
            seen_ids.add(aid)

            priority = article.get("priority", "")
            if priority and priority not in valid_priorities:
                errors.append(f"{prefix}.priority 无效: {priority}，应为 {valid_priorities}")

            summary = article.get("summary")
            if not summary or not isinstance(summary, dict):
                errors.append(f"{prefix}.summary 缺失或不是对象")
            else:
                if not summary.get("what_happened"):
                    errors.append(f"{prefix}.summary.what_happened 缺失")
                if not summary.get("why_it_matters"):
                    errors.append(f"{prefix}.summary.why_it_matters 缺失")

            if not article.get("relevance"):
                errors.append(f"{prefix}.relevance 缺失")

            tags = article.get("tags")
            if not tags or not isinstance(tags, list):
                errors.append(f"{prefix}.tags 缺失或不是数组")

            url = article.get("url", "")
            if url and not url.startswith("http"):
                errors.append(f"{prefix}.url 格式错误: {url[:50]}")
            if url and "/example" in url:
                errors.append(f"{prefix}.url 疑似假 URL（含 /example）: {url[:60]}")

            cred = article.get("credibility")
            if cred:
                if cred.get("confidence") and cred["confidence"] not in ("high", "medium", "low"):
                    errors.append(f"{prefix}.credibility.confidence 无效: {cred['confidence']}")

                cross_refs = cred.get("cross_refs", 0)
                sources_list = cred.get("sources", [])
                if cross_refs > 1 and isinstance(sources_list, list) and len(sources_list) == 0:
                    errors.append(f"{prefix}.credibility cross_refs={cross_refs} 但 sources 为空，缺少来源 URL")

                if isinstance(sources_list, list):
                    source_urls = []
                    for si, src in enumerate(sources_list):
                        src_url = src.get("url", "") if isinstance(src, dict) else ""
                        if src_url and "/example" in src_url:
                            errors.append(f"{prefix}.credibility.sources[{si}].url 疑似假 URL: {src_url[:60]}")
                        if src_url:
                            source_urls.append(src_url)

                    unique_source_urls = list(dict.fromkeys(source_urls))

                    if cross_refs and cross_refs != len(sources_list):
                        errors.append(f"{prefix}.credibility.cross_refs={cross_refs} 与 sources 数量 {len(sources_list)} 不一致")

                    main_url = article.get("url", "")
                    if main_url and source_urls and main_url not in source_urls:
                        warnings.append(f"{prefix} 主 url 未出现在 credibility.sources 中")

                    if len(unique_source_urls) < len(source_urls):
                        warnings.append(f"{prefix} credibility.sources 存在重复 URL，去重后为 {len(unique_source_urls)} 条")

                    effective_count = len(unique_source_urls)
                    if effective_count == 1:
                        if article.get("priority") == "major":
                            errors.append(f"{prefix} 是 major 但只有单源，major 必须 ≥2 个来源交叉印证")
                        elif article.get("priority") == "notable":
                            warnings.append(f"{prefix} 是 notable，但只有单源，建议优先补充第二来源")
                        else:
                            warnings.append(f"{prefix} 只有 1 个有效来源")

    if not data.get("data_sources") or not isinstance(data.get("data_sources"), list):
        errors.append("[data_sources] 缺失或不是数组")

    # tools 可选字段校验：存在时检查结构
    tools = data.get("tools")
    if tools is not None:
        if not isinstance(tools, list):
            errors.append("[tools] 存在但不是数组")
        else:
            for ti, tool in enumerate(tools):
                if not isinstance(tool, dict):
                    errors.append(f"[tools][{ti}] 不是对象")
                elif not tool.get("id") or not tool.get("name"):
                    warnings.append(f"[tools][{ti}] 缺少 id 或 name 字段")

    return errors, warnings


def validate_urls_against_candidates(data: dict, candidates_data: dict) -> list[str]:
    """校验日报 JSON 中的所有 URL 是否来自 candidates.json。"""
    errors = []

    candidate_urls = set()
    for c in candidates_data.get("candidates", []):
        url = c.get("url", "")
        if url:
            candidate_urls.add(url)

    if not candidate_urls:
        errors.append("[candidates] candidates.json 中没有找到任何 URL")
        return errors

    articles = data.get("articles", [])
    for i, article in enumerate(articles):
        prefix = f"[articles[{i}]]"

        url = article.get("url", "")
        if url and url not in candidate_urls:
            errors.append(f"{prefix}.url 不在 candidates.json 中: {url[:70]}")

        cred = article.get("credibility", {})
        sources_list = cred.get("sources", [])
        if isinstance(sources_list, list):
            for si, src in enumerate(sources_list):
                src_url = src.get("url", "") if isinstance(src, dict) else ""
                if src_url and src_url not in candidate_urls:
                    errors.append(f"{prefix}.credibility.sources[{si}].url 不在 candidates.json 中: {src_url[:70]}")

    main_urls = [a.get("url", "") for a in articles if a.get("url")]
    seen = {}
    for url in main_urls:
        if url in seen:
            errors.append(f"多条 article 使用了相同的主 URL: {url[:70]}")
        seen[url] = True

    return errors


def main():
    import argparse
    parser = argparse.ArgumentParser(description="校验日报 JSON")
    parser.add_argument("input", help="日报 JSON 文件路径")
    parser.add_argument("--candidates", default="", help="candidates.json 路径，用于 URL 交叉校验")
    args = parser.parse_args()

    path = Path(args.input)
    if not path.exists():
        print(f"ERROR: {path} 不存在", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON 解析失败: {e}", file=sys.stderr)
        sys.exit(1)

    errors, warnings = validate(data)

    candidates_path = Path(args.candidates) if args.candidates else None
    if not candidates_path:
        date = data.get("meta", {}).get("date", "")
        if date:
            auto_path = path.parent.parent / "raw" / f"{date}_candidates.json"
            if auto_path.exists():
                candidates_path = auto_path

    if candidates_path and candidates_path.exists():
        try:
            candidates_data = json.loads(candidates_path.read_text(encoding="utf-8"))
            url_errors = validate_urls_against_candidates(data, candidates_data)
            errors.extend(url_errors)
            print(f"URL 交叉校验: 使用 {candidates_path.name}", file=sys.stderr)
        except json.JSONDecodeError:
            print(f"WARNING: {candidates_path} 解析失败，跳过 URL 校验", file=sys.stderr)
    else:
        print(f"INFO: 未找到 candidates.json，跳过 URL 交叉校验", file=sys.stderr)

    if errors:
        print(f"❌ 校验失败，{len(errors)} 个错误：")
        for e in errors:
            print(f"   {e}")
        if warnings:
            print(f"\n⚠️ 另有 {len(warnings)} 个告警：")
            for w in warnings:
                print(f"   {w}")
        sys.exit(1)

    articles = data.get("articles", [])
    priorities = {}
    for a in articles:
        p = a.get("priority", "unknown")
        priorities[p] = priorities.get(p, 0) + 1

    if warnings:
        print(f"⚠️ 校验通过，但有多源告警")
        print(f"   日期: {data.get('meta', {}).get('date', '?')}")
        print(f"   文章: {len(articles)} 条")
        print(f"   优先级: {priorities}")
        print(f"   速览: {len(data.get('left_sidebar', {}).get('overview', []))} 条")
        print(f"   行动: {len(data.get('left_sidebar', {}).get('actions', []))} 条")
        print(f"   告警: {len(warnings)} 条")
        print("\n建议模型回到 candidates 重新补源的条目：")
        for w in warnings:
            print(f"   {w}")
    else:
        print(f"✅ 校验通过")
        print(f"   日期: {data.get('meta', {}).get('date', '?')}")
        print(f"   文章: {len(articles)} 条")
        print(f"   优先级: {priorities}")
        print(f"   速览: {len(data.get('left_sidebar', {}).get('overview', []))} 条")
        print(f"   行动: {len(data.get('left_sidebar', {}).get('actions', []))} 条")


if __name__ == "__main__":
    main()
