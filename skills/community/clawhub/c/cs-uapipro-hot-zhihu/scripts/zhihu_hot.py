#!/usr/bin/env python3
"""
知乎热榜抓取脚本 - 使用 UAPIPRO API
依赖: requests (标准库urllib即可，无需额外安装)

用法:
    python zhihu_hot.py [top_n]

示例:
    python zhihu_hot.py 10   # 获取前10条
    python zhihu_hot.py      # 获取全部
"""

import json
import os
import sys
import urllib.request
import urllib.error


def fetch_zhihu_hot(top_n: int = 0) -> dict:
    """
    从 UAPIPRO API 获取知乎热榜

    Args:
        top_n: 返回前N条，0表示全部

    Returns:
        包含 list, update_time, type 的字典
    """
    api_key = os.environ.get("UAPIPRO_API_KEY")
    if not api_key:
        raise RuntimeError("环境变量 UAPIPRO_API_KEY 未设置")

    url = "https://uapis.cn/api/v1/misc/hotboard?type=zhihu"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "cs-uapipro-hot-zhihu/1.0"
    })

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"API请求失败 (HTTP {e.code}): {e.read().decode()}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"网络请求失败: {e.reason}")

    # API成功时直接返回数据（无code字段），失败时有code字段
    if "code" in data and data.get("code") != 0:
        raise RuntimeError(f"API返回错误: {data.get('msg', data)}")

    raw_list = data.get("list", [])
    if top_n > 0:
        raw_list = raw_list[:top_n]

    return {
        "list": raw_list,
        "update_time": data.get("update_time", ""),
        "type": data.get("type", "zhihu"),
    }


def format_text(data: dict, include_url: bool = False, include_cover: bool = False) -> str:
    """格式化输出为纯文本
    
    Args:
        data: 原始数据
        include_url: 是否显示链接
        include_cover: 是否显示封面图URL
    """
    lines = []
    update_time = data.get("update_time", "")
    lines.append(f"知乎热榜（更新时间: {update_time}）\n")

    for item in data.get("list", []):
        index = item.get("index", "?")
        title = item.get("title", "")
        hot_value = item.get("hot_value", "")
        url = item.get("url", "")
        desc = item.get("extra", {}).get("desc", "")
        label = item.get("extra", {}).get("label", "")
        image = item.get("extra", {}).get("image", "")

        lines.append(f"{index}. {title}")
        if desc:
            lines.append(f"   {desc[:80]}..." if len(desc) > 80 else f"   {desc}")
        lines.append(f"   {hot_value}  {'[' + label + ']' if label else ''}")
        if include_url:
            lines.append(f"   {url}")
        if include_cover and image:
            cover_url = f"https://uapis.cn/{image}"
            lines.append(f"   封面: {cover_url}")
        lines.append("")

    return "\n".join(lines).strip()


def format_feishu(data: dict) -> str:
    """格式化输出为飞书富文本JSON（post类型），支持链接和图片"""
    update_time = data.get("update_time", "")
    
    content_blocks = []
    
    # 标题
    content_blocks.append([{"tag": "text", "text": f"🔥 知乎热榜（更新: {update_time}）\n\n"}])
    
    for item in data.get("list", []):
        index = item.get("index", "?")
        title = item.get("title", "")
        hot_value = item.get("hot_value", "")
        url = item.get("url", "")
        desc = item.get("extra", {}).get("desc", "")
        label = item.get("extra", {}).get("label", "")
        image = item.get("extra", {}).get("image", "")
        
        # 序号 + 标题（可点击链接）
        title_text = f"{index}. {title}  {hot_value}"
        if label:
            title_text += f"  【{label}】"
        
        content_blocks.append([
            {"tag": "a", "text": title_text, "href": url}
        ])
        
        # 描述
        if desc:
            display_desc = desc[:100] + "..." if len(desc) > 100 else desc
            content_blocks.append([
                {"tag": "text", "text": f"   {display_desc}\n"}
            ])
        
        # 封面图
        if image:
            cover_url = f"https://uapis.cn/{image}"
            content_blocks.append([
                {"tag": "img", "src": cover_url, "alt": title[:20]}
            ])
        
        content_blocks.append([{"tag": "text", "text": "\n"}])
    
    post_content = {"zh_cn": {"title": "", "content": content_blocks}}
    return json.dumps(post_content, ensure_ascii=False)


def format_json(data: dict) -> str:
    """格式化输出为 JSON"""
    return json.dumps(data, indent=2, ensure_ascii=False)


def main():
    top_n = 0
    output_format = "text"
    include_url = False
    include_cover = False

    # 简单命令行参数解析
    args = sys.argv[1:]
    for arg in args:
        if arg.isdigit():
            top_n = int(arg)
        elif arg in ("--json", "-j"):
            output_format = "json"
        elif arg in ("--url", "-u"):
            include_url = True
        elif arg in ("--cover", "-c"):
            include_cover = True
        elif arg in ("--feishu", "-f"):
            output_format = "feishu"

    try:
        data = fetch_zhihu_hot(top_n)

        if output_format == "json":
            print(format_json(data))
        elif output_format == "feishu":
            print(format_feishu(data))
        else:
            print(format_text(data, include_url=include_url, include_cover=include_cover))
    except RuntimeError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
