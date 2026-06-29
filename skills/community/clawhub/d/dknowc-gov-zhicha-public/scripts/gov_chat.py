#!/usr/bin/env python3
"""深知政务智查可信搜索调用脚本。

本脚本只负责调用可信搜索接口并整理材料包；最终政务问答由 Agent 基于材料生成。
"""

import argparse
import configparser
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.ini"
DEFAULT_ENDPOINT = "https://open.dknowc.cn/dependable/search"


def _as_bool(value: Optional[str], default: bool = False) -> bool:
    if value is None or not str(value).strip():
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def _as_int(value: Optional[str], default: int) -> int:
    if value is None or not str(value).strip():
        return default
    try:
        return int(str(value).strip())
    except ValueError:
        return default


def _split_csv(value: Optional[str]) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _read_config(path: Path) -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    cfg.read(path, encoding="utf-8")
    return cfg


def _cfg(cfg: configparser.ConfigParser, section: str, key: str, default: str = "") -> str:
    if not cfg.has_section(section):
        return default
    return cfg.get(section, key, fallback=default).strip()


def _pick(*values: Optional[str]) -> str:
    for value in values:
        if value and str(value).strip():
            return str(value).strip()
    return ""


def _clean_text(value: Any) -> str:
    text = html.unescape(str(value or ""))
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def _shorten(value: Any, limit: int = 500) -> str:
    text = " ".join(_clean_text(value).split())
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


def _format_units(value: Any) -> str:
    if isinstance(value, list):
        return "、".join(str(item) for item in value if item)
    return str(value or "")


def _article_value(article: Dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = article.get(key)
        if value:
            return _format_units(value)
    return ""


def _build_payload(args: argparse.Namespace, cfg: configparser.ConfigParser) -> Dict[str, Any]:
    defaults = "defaults"
    area = args.area or _cfg(cfg, defaults, "area", "深圳市")
    eff_time = args.eff_time or _cfg(cfg, defaults, "eff_time")

    search_types = args.search_type or _split_csv(_cfg(cfg, defaults, "search_type", "policy,affair,govSite,qa"))
    search_channels = args.search_channel or _split_csv(_cfg(cfg, defaults, "search_channel"))

    payload: Dict[str, Any] = {
        "query": args.input,
        "service_area": [area],
        "policy": args.policy or _as_bool(_cfg(cfg, defaults, "policy"), True),
        "item": args.item or _as_bool(_cfg(cfg, defaults, "item"), True),
        "return_full_content": args.return_full_content or _as_bool(_cfg(cfg, defaults, "return_full_content"), False),
        "segmentCount": args.segment_count or _as_int(_cfg(cfg, defaults, "segment_count"), 3),
        "simplified": args.simplified if args.simplified is not None else _as_bool(_cfg(cfg, defaults, "simplified"), True),
        "queryTopArea": args.query_top_area if args.query_top_area is not None else _as_bool(_cfg(cfg, defaults, "query_top_area"), True),
    }

    if eff_time:
        payload["eff_time"] = [eff_time]
    if search_types:
        payload["searchType"] = search_types
    if search_channels:
        payload["searchChannel"] = search_channels
    if args.search_source_url or _cfg(cfg, defaults, "search_source_url"):
        payload["searchSourceUrl"] = args.search_source_url or _cfg(cfg, defaults, "search_source_url")
    if args.search_source_id or _cfg(cfg, defaults, "search_source_id"):
        payload["searchSourceId"] = args.search_source_id or _cfg(cfg, defaults, "search_source_id")
    material_length = args.material_length or _as_int(_cfg(cfg, defaults, "material_length"), 0)
    if material_length > 0:
        payload["MaterialLength"] = material_length
    if args.return_md5 or _as_bool(_cfg(cfg, defaults, "return_md5"), False):
        payload["returnMd5"] = True
    if args.know_base or _as_bool(_cfg(cfg, defaults, "know_base"), False):
        payload["knowBase"] = True

    return payload


def _post(endpoint: str, api_key: str, payload: Dict[str, Any], timeout: int) -> Dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False)
    try:
        import requests

        response = requests.post(
            endpoint,
            headers={"api-key": api_key, "Content-Type": "application/json"},
            data=data.encode("utf-8"),
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()
    except Exception as first_error:
        cmd = [
            "curl",
            "-sS",
            "-L",
            endpoint,
            "-H",
            f"api-key: {api_key}",
            "-H",
            "Content-Type: application/json",
            "-d",
            data,
        ]
        try:
            proc = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout, check=False)
        except Exception as curl_error:
            raise RuntimeError(f"requests failed: {first_error}; curl failed: {curl_error}") from curl_error
        if proc.returncode != 0:
            raise RuntimeError(f"requests failed: {first_error}; curl failed: {proc.stderr.strip()}")
        return json.loads(proc.stdout)


def _extract_data(body: Dict[str, Any]) -> Dict[str, Any]:
    content = body.get("content")
    if isinstance(content, str):
        try:
            content = json.loads(content)
        except json.JSONDecodeError:
            content = {}
    if isinstance(content, dict) and isinstance(content.get("data"), dict):
        return content["data"]
    if isinstance(content, dict):
        return content
    return {}


def _knowledge_base(body: Dict[str, Any], data: Dict[str, Any]) -> str:
    content = body.get("content")
    if isinstance(content, str):
        try:
            content = json.loads(content)
        except json.JSONDecodeError:
            content = {}
    if isinstance(content, dict) and content.get("knowledgeBase"):
        return str(content["knowledgeBase"])
    if data.get("knowledgeBase"):
        return str(data["knowledgeBase"])
    return ""


def _status(body: Dict[str, Any]) -> Dict[str, Any]:
    content = body.get("content") if isinstance(body.get("content"), dict) else {}
    return {
        "ret": body.get("ret"),
        "code": content.get("code"),
        "msg": content.get("msg") or body.get("errmsg") or body.get("msg") or "",
        "id": content.get("id", ""),
    }


def _print_articles(articles: Iterable[Dict[str, Any]], max_articles: int, max_paragraphs: int) -> None:
    rows = [item for item in articles if isinstance(item, dict)]
    print(f"\n召回材料：{len(rows)} 篇")
    for index, article in enumerate(rows[:max_articles], 1):
        title = _clean_text(_article_value(article, "文章标题", "title") or "无标题")
        unit = _article_value(article, "发布或实施机构", "数据源", "unit")
        area = _article_value(article, "办理地域")
        date = _article_value(article, "发布日期", "createDate")
        reliability = _article_value(article, "发布日期可信度", "createDateReliability")
        url = _article_value(article, "源网址", "sourceUrl")
        art_md5 = _article_value(article, "artMd5")
        paragraphs = article.get("段落", [])
        if not isinstance(paragraphs, list):
            paragraphs = []

        print(f"\n材料{index}")
        print(f"标题：《{title}》")
        print(f"发布单位：{unit or '接口未返回'}")
        print(f"适用地域：{area or '接口未返回'}")
        print(f"发布日期：{date or '接口未返回'}")
        if reliability:
            print(f"日期可信度：{reliability}")
        print(f"链接：{url or '接口未返回源链接'}")
        if art_md5:
            print(f"文章MD5：{art_md5}")

        for para_index, paragraph in enumerate(paragraphs[:max_paragraphs], 1):
            if not isinstance(paragraph, dict):
                continue
            para_title = _article_value(paragraph, "标题", "title")
            para_content = _article_value(paragraph, "内容", "text", "content")
            par_md5 = _article_value(paragraph, "parMd5")
            print(f"  段落{para_index}")
            if para_title:
                print(f"  小标题：{_clean_text(para_title)}")
            if par_md5:
                print(f"  段落MD5：{par_md5}")
            print(f"  原文：{_shorten(para_content, 650) if para_content else '接口未返回'}")

        if article.get("全文"):
            print(f"全文摘录：{_shorten(article.get('全文'), 900)}")

    remaining = len(rows) - min(len(rows), max_articles)
    if remaining > 0:
        print(f"\n其余还有 {remaining} 篇召回材料未展开。需要更多材料时可提高 --max-articles。")


def _print_policy_files(items: Iterable[Dict[str, Any]]) -> None:
    rows = [item for item in items if isinstance(item, dict)]
    if not rows:
        return
    print(f"\n政策文件清单：{len(rows)} 篇")
    for index, item in enumerate(rows, 1):
        title = _clean_text(item.get("title") or "无标题")
        doc_no = item.get("writtenText") or item.get("documentNo") or ""
        print(f"{index}. 《{title}》")
        print(f"   - 发文字号：{doc_no or '接口未返回'}")
        print(f"   - 发布日期：{item.get('createDate') or '接口未返回'}")
        if item.get("createDateReliability"):
            print(f"   - 日期可信度：{item['createDateReliability']}")
        print(f"   - 链接：{item.get('sourceUrl') or '接口未返回源链接'}")


def _print_items(items: Iterable[Dict[str, Any]]) -> None:
    rows = [item for item in items if isinstance(item, dict)]
    if not rows:
        return
    print(f"\n办理事项清单：{len(rows)} 项")
    for index, item in enumerate(rows, 1):
        print(f"{index}. {item.get('title') or '无标题'}")
        print(f"   - 实施单位：{item.get('unit') or '接口未返回'}")
        print(f"   - 服务对象：{item.get('itemCategory') or '接口未返回'}")
        print(f"   - 事项链接：{item.get('sourceUrl') or '接口未返回源链接'}")
        urls = item.get("onlineProcessUrls")
        if isinstance(urls, list) and urls:
            for url in urls:
                print(f"   - 网上办理：{html.unescape(str(url))}")


def _print_summary(body: Dict[str, Any], payload: Dict[str, Any], max_articles: int, max_paragraphs: int) -> None:
    status = _status(body)
    data = _extract_data(body)
    if status["ret"] not in (0, "0", None) or status["code"] not in (200, "200", None):
        print("错误：可信搜索接口返回异常")
        print(json.dumps(status, ensure_ascii=False, indent=2))
        return

    print("=== 深知政务智查可信搜索材料包 ===")
    if status["id"]:
        print(f"响应ID：{status['id']}")
    print(f"用户问题：{data.get('用户问题') or payload.get('query')}")
    print(f"办理地域：{data.get('办理地域') or '、'.join(payload.get('service_area', [])) or '接口未返回'}")
    print(f"搜索类型：{','.join(payload.get('searchType', [])) if payload.get('searchType') else '接口默认'}")
    print(f"参数：policy={payload.get('policy')} item={payload.get('item')} segmentCount={payload.get('segmentCount')} simplified={payload.get('simplified')}")

    knowledge_base = _knowledge_base(body, data)
    if knowledge_base:
        print(f"\n知识专库链接：{knowledge_base}")

    _print_articles(data.get("检索文章", []), max_articles, max_paragraphs)
    _print_items(data.get("recommendationItems", []))
    _print_policy_files(data.get("policyFiles", []))

    print("\n生成回答提醒")
    print("- 只使用以上材料生成政务回答，不要编造政策、链接、文号、发布日期。")
    print("- 默认按深圳市处理；用户明确给出其他地域时，以用户地域为准。")
    print("- 面向用户的最终回复应为自然回答 + 末尾字段化参考依据。")


def main() -> None:
    parser = argparse.ArgumentParser(description="深知政务智查可信搜索材料召回脚本")
    parser.add_argument("input", help="用户政务问题")
    parser.add_argument("--config", default=str(CONFIG_PATH), help="配置文件路径")
    parser.add_argument("--endpoint", help="覆盖接口地址")
    parser.add_argument("--api-key", help="覆盖 API Key")
    parser.add_argument("--area", help="地域；默认深圳市")
    parser.add_argument("--eff-time", help="生效时间，如 2026年、2026年06月、2026年06月17日")
    parser.add_argument("--policy", action="store_true", help="返回规范性文件清单")
    parser.add_argument("--item", action="store_true", help="返回公共事项在线办理清单")
    parser.add_argument("--return-full-content", action="store_true", help="返回资料全文")
    parser.add_argument("--segment-count", type=int, help="每篇材料最多返回段落数")
    parser.add_argument("--simplified", dest="simplified", action="store_true", default=None, help="启用精炼输出")
    parser.add_argument("--no-simplified", dest="simplified", action="store_false", help="关闭精炼输出")
    parser.add_argument("--query-top-area", dest="query_top_area", action="store_true", default=None, help="搜索当前地域及上级地域")
    parser.add_argument("--no-query-top-area", dest="query_top_area", action="store_false", help="仅搜索当前地域")
    parser.add_argument("--search-type", action="append", choices=["policy", "affair", "govSite", "qa", "private"], help="搜索材料类型，可重复传入")
    parser.add_argument("--search-channel", action="append", choices=["govSearch"], help="搜索渠道，仅 govSite 生效")
    parser.add_argument("--search-source-url", help="限定搜索网址，多个用英文逗号隔开")
    parser.add_argument("--search-source-id", help="限定搜索数据源 ID，多个用英文逗号隔开")
    parser.add_argument("--material-length", type=int, help="返回资料最大字符上限")
    parser.add_argument("--return-md5", action="store_true", help="返回文章和段落 MD5")
    parser.add_argument("--know-base", action="store_true", help="返回知识专库链接")
    parser.add_argument("--show-payload", action="store_true", help="打印请求参数")
    parser.add_argument("--dry-run", action="store_true", help="只打印请求参数，不发起请求")
    parser.add_argument("--raw", action="store_true", help="打印原始响应")
    parser.add_argument("--json-only", action="store_true", help="仅输出 JSON")
    parser.add_argument("--max-articles", type=int, help="最多展开多少篇材料")
    parser.add_argument("--max-paragraphs-per-article", type=int, help="每篇最多展开多少段原文")
    parser.add_argument("--timeout", type=int, default=90, help="请求超时秒数")
    args = parser.parse_args()

    cfg = _read_config(Path(args.config))
    endpoint = _pick(args.endpoint, os.environ.get("DKNOWC_GOV_ZHICHA_ENDPOINT"), _cfg(cfg, "api", "endpoint"), DEFAULT_ENDPOINT)
    api_key = _pick(args.api_key, os.environ.get("DKNOWC_GOV_ZHICHA_API_KEY"), _cfg(cfg, "api", "api_key"))

    if not api_key:
        print("错误：缺少 api_key，请在 config.ini 的 [api] 中配置，或使用 --api-key 临时传入。", file=sys.stderr)
        sys.exit(2)

    payload = _build_payload(args, cfg)
    if args.show_payload or args.dry_run:
        print("=== 请求参数 ===")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        print()
    if args.dry_run:
        return

    try:
        body = _post(endpoint, api_key, payload, args.timeout)
    except Exception as error:
        print(f"错误：可信搜索请求失败 - {type(error).__name__}: {error}", file=sys.stderr)
        sys.exit(1)

    if args.json_only:
        print(json.dumps({"success": True, "payload": payload, "data": body}, ensure_ascii=False, indent=2))
        return

    if args.raw:
        print(json.dumps(body, ensure_ascii=False, indent=2))
        return

    max_articles = args.max_articles or _as_int(_cfg(cfg, "defaults", "max_articles"), 10)
    max_paragraphs = args.max_paragraphs_per_article or _as_int(_cfg(cfg, "defaults", "max_paragraphs_per_article"), 3)
    _print_summary(body, payload, max_articles, max_paragraphs)


if __name__ == "__main__":
    main()
