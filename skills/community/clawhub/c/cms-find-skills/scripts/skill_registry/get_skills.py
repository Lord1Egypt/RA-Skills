#!/usr/bin/env python3
"""
主要内容：
  浏览、搜索、查看详情、获取下载地址。
  支持按官方 (Official)、推荐 (Recommended)、内置 (Built-in) 等多维度筛选与排序。
  通过 API_BASE 环境变量配置接口基础地址。
"""

from __future__ import annotations

import argparse
import json
import sys
import requests
import warnings

import os

# 禁用 InsecureRequestWarning (因为 verify=False)
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

DEFAULT_API_BASE = "https://aishuo.co"
API_BASE = DEFAULT_API_BASE
API_URL = f"{API_BASE.rstrip('/')}/api/skill/list"


def parse_api_response(response: requests.Response, action: str) -> dict:
    data = response.json()
    if isinstance(data, dict) and data.get("resultCode") not in (None, 1):
        message = data.get("resultMsg") or data.get("detailMsg") or response.text
        raise RuntimeError(f"{action}失败: {message}")
    return data


def call_api(app_key: str = None, keyword: str = None) -> dict:
    """调用平台公开 Skill 列表接口。"""
    headers = {"Content-Type": "application/json"}
    if app_key:
        headers["appKey"] = app_key
        
    url = f"{API_BASE.rstrip('/')}/api/skill/search" if keyword else API_URL
    json_data = {"keyword": keyword} if keyword else None
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json=json_data,
            verify=False,
            timeout=60,
            allow_redirects=True,
        )
        response.raise_for_status()
        return parse_api_response(response, "搜索 Skill" if keyword else "获取 Skill 列表")
    except Exception as exc:
        raise Exception(f"请求失败: {exc}")


def extract_skills(result: dict) -> list[dict]:
    """从响应中提取 Skill 列表。"""
    if isinstance(result, list):
        return result
    return result.get("data") or result.get("resultData") or []


def is_official(skill: dict) -> bool:
    """判断是否为官方 Skill。"""
    if skill.get("isOfficial") is not None:
        return bool(skill.get("isOfficial"))
    metadata = skill.get("metadata") or {}
    xgjk = metadata.get("xgjk") or {}
    return bool(xgjk.get("isOfficial"))


def get_recommend_score(skill: dict) -> int:
    """获取推荐得分。"""
    score = skill.get("recommendScore")
    if score is not None:
        return int(score)
    metadata = skill.get("metadata") or {}
    xgjk = metadata.get("xgjk") or {}
    return int(xgjk.get("recommendScore") or 0)


def is_built_in(skill: dict) -> bool:
    """判断是否为内置 Skill。"""
    if skill.get("isBuiltIn") is not None:
        return bool(skill.get("isBuiltIn"))
    metadata = skill.get("metadata") or {}
    xgjk = metadata.get("xgjk") or {}
    return bool(xgjk.get("isBuiltIn"))


def is_internal(skill: dict) -> bool:
    """判断是否为内部可见 Skill。"""
    if skill.get("isInternal") is not None:
        return bool(skill.get("isInternal"))
    metadata = skill.get("metadata") or {}
    xgjk = metadata.get("xgjk") or {}
    return bool(xgjk.get("isInternal", True))


def search_skills(skills: list[dict], keyword: str) -> list[dict]:
    """按名称、描述、skillCode、标签模糊匹配。"""
    kw = keyword.lower()
    results = []
    for skill in skills:
        tags = ""
        metadata = skill.get("metadata") or {}
        openclaw = metadata.get("openclaw") or {}
        if openclaw.get("tags"):
            tags = ",".join(openclaw["tags"])
        if (
            kw in (skill.get("skillCode") or skill.get("name") or "").lower()
            or kw in (skill.get("displayName") or skill.get("name") or "").lower()
            or kw in (skill.get("description") or "").lower()
            or kw in tags.lower()
        ):
            results.append(skill)
    return results


def find_one(skills: list[dict], query: str) -> dict | None:
    """按 skillCode 或 displayName 查找单个 Skill。"""
    q = query.lower()

    for skill in skills:
        if (skill.get("skillCode") or skill.get("name") or "").lower() == q:
            return skill

    for skill in skills:
        if (skill.get("displayName") or "").lower() == q:
            return skill

    for skill in skills:
        code = (skill.get("skillCode") or skill.get("name") or "").lower()
        display = (skill.get("displayName") or "").lower()
        if q in code or q in display:
            return skill

    return None


def get_download_url(skills: list[dict], query: str) -> str | None:
    """按 skillCode 或 displayName 获取下载地址。"""
    skill = find_one(skills, query)
    if not skill:
        return None
    return skill.get("downloadUrl")


def format_list(skills: list[dict]) -> str:
    """以紧凑表格格式展示列表。"""
    if not skills:
        return "（暂无已发布的 Skill）"

    lines = [
        f"{'#':<4} {'显示名':<22} {'SkillCode':<22} {'版本':<8} {'官方':<6} {'推荐':<6} {'内置':<6} {'描述'}",
        "-" * 120,
    ]
    for index, skill in enumerate(skills, 1):
        display_name = (skill.get("displayName") or skill.get("name") or "")[:20]
        skill_code = (skill.get("skillCode") or skill.get("name") or "")[:20]
        version = (skill.get("version") or "")[:7]
        official = "是" if is_official(skill) else "否"
        score = get_recommend_score(skill)
        score_str = str(score) if score > 0 else "-"
        builtin = "是" if is_built_in(skill) else "否"
        desc = (skill.get("description") or "")[:35]
        lines.append(f"{index:<4} {display_name:<22} {skill_code:<22} {version:<8} {official:<6} {score_str:<6} {builtin:<6} {desc}")
    lines.append(f"\n共 {len(skills)} 个 Skill")
    return "\n".join(lines)


def format_detail(skill: dict) -> str:
    """格式化单个 Skill 的详情。"""
    owner = skill.get("owner") or {}
    metadata = skill.get("metadata") or {}
    openclaw = metadata.get("openclaw") or {}
    tags = ",".join(openclaw.get("tags") or [])
    lines = [
        "=" * 72,
        f"显示名: {skill.get('displayName') or skill.get('name', '-')}",
        f"SkillCode: {skill.get('skillCode') or skill.get('name', '-')}",
        f"ID: {skill.get('id', '-')}",
        f"版本: {skill.get('version', '-')}",
        f"标签: {tags or '-'}",
        f"描述: {skill.get('description') or '-'}",
        f"下载地址: {skill.get('downloadUrl') or '-'}",
        f"作者: {owner.get('name', '-')}",
        f"创建时间: {skill.get('createTime', '-')}",
        f"下载数: {skill.get('downloadCount', '-')}",
        f"点赞数: {skill.get('likeCount', '-')}",
        f"收藏数: {skill.get('favoriteCount', '-')}",
        f"官方 Skill: {'是' if is_official(skill) else '否'}",
        f"推荐得分: {get_recommend_score(skill) or '-'}",
        f"内置 Skill: {'是' if is_built_in(skill) else '否'}",
        f"内部可见: {'是' if is_internal(skill) else '否'}",
        "=" * 72,
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Skill 发现：浏览、搜索、详情、下载地址")
    parser.add_argument("--search", "-s", help="按关键词搜索 Skill")
    parser.add_argument("--detail", "-d", help="查看某个 Skill 详情")
    parser.add_argument(
        "--url",
        "--download-url",
        "-u",
        dest="url",
        help="仅输出某个 Skill 的 downloadUrl",
    )
    parser.add_argument("--official", "-o", action="store_true", help="只列出官方 Skill")
    parser.add_argument("--recommended", "-r", action="store_true", help="只列出推荐 Skill（按推荐分数排序）")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    parser.add_argument("--appKey", help="从上下文中获取的 appKey，将其放到请求 header 中")
    args = parser.parse_args()

    try:
        result = call_api(args.appKey, args.search)
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    skills = extract_skills(result)

    if args.official:
        skills = [s for s in skills if is_official(s)]

    if args.recommended:
        skills = [s for s in skills if get_recommend_score(s) > 0]
        skills.sort(key=get_recommend_score, reverse=True)

    if args.search:
        skills = search_skills(skills, args.search)

    if args.json:
        if isinstance(result, dict):
            if "data" in result:
                result["data"] = skills
            elif "resultData" in result:
                result["resultData"] = skills
        else:
            result = skills
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.url:
        url = get_download_url(skills, args.url)
        if not url:
            print(f"未找到 \"{args.url}\" 的下载地址", file=sys.stderr)
            sys.exit(1)
        print(url)
        return

    if args.detail:
        skill = find_one(skills, args.detail)
        if not skill:
            print(f"未找到匹配 \"{args.detail}\" 的 Skill", file=sys.stderr)
            sys.exit(1)
        print(format_detail(skill))
        return

    if args.search:
        if not skills:
            print(f"搜索 \"{args.search}\" 无结果", file=sys.stderr)
            sys.exit(1)
        print(f"搜索 \"{args.search}\" 匹配到 {len(skills)} 个结果：\n")
        print(format_list(skills))
        return

    title = "平台 Skill 列表"
    if args.official and args.recommended:
        title = "平台官方推荐 Skill 列表"
    elif args.official:
        title = "平台官方 Skill 列表"
    elif args.recommended:
        title = "平台推荐 Skill 列表"

    print(f"{title}\n")
    print(format_list(skills))


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
