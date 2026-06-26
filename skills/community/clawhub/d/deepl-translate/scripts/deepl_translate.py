#!/usr/bin/env python3

import argparse
import json
import mimetypes
import os
import sys
import time
import uuid
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, List, Optional, Tuple


DEFAULT_BASE_URL = "https://api.deepl.com"
ALLOWED_BASE_URLS = {
    "https://api.deepl.com",
    "https://api-free.deepl.com",
}
DEFAULT_TIMEOUT = 300
FORMALITY_CHOICES = ["default", "more", "less", "prefer_more", "prefer_less"]
MODEL_TYPE_CHOICES = ["latency_optimized", "quality_optimized", "prefer_quality_optimized"]


class ChineseArgumentParser(argparse.ArgumentParser):
    def format_help(self) -> str:
        text = super().format_help()
        replacements = {
            "optional arguments:": "可选参数:",
            "options:": "可选参数:",
            "positional arguments:": "位置参数:",
            "show this help message and exit": "显示此帮助信息并退出",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text


def add_common_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="HTTP 超时时间，单位秒，默认 300。")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON 响应。")


def add_text_options(parser: argparse.ArgumentParser, require_target: bool) -> None:
    parser.add_argument("--text", action="append", dest="texts", help="要处理的文本项。可重复传入。")
    parser.add_argument("--file", help="从文件读取文本，并作为一个文本项发送。")
    parser.add_argument("--stdin", action="store_true", help="从标准输入读取文本，并作为一个文本项发送。")
    parser.add_argument("--target-lang", required=require_target, help="目标语言代码，例如 ZH、DE、EN-US。")
    parser.add_argument("--source-lang", help="源语言代码。")
    parser.add_argument("--context", help="补充上下文，这部分不会被翻译。")


def build_parser() -> argparse.ArgumentParser:
    parser = ChineseArgumentParser(
        description="使用 DeepL API 的通用 CLI，支持翻译、语言查询、用量查询、文档翻译、Write/Rephrase、glossary v2/v3。"
    )
    subparsers = parser.add_subparsers(dest="command")

    translate = subparsers.add_parser("translate", help="文本翻译", description="调用 /v2/translate 进行文本翻译。")
    add_common_options(translate)
    add_text_options(translate, require_target=True)
    translate.add_argument("--formality", choices=FORMALITY_CHOICES, help="正式程度。")
    translate.add_argument("--model-type", choices=MODEL_TYPE_CHOICES, help="翻译模型类型。")
    translate.add_argument("--glossary-id", help="词汇表 ID。需要同时提供 --source-lang。")
    translate.add_argument("--tag-handling", choices=["html", "xml"], help="标签处理方式。")
    translate.add_argument("--tag-handling-version", choices=["v1", "v2"], help="标签处理版本。")
    translate.add_argument("--split-sentences", choices=["0", "1", "nonewlines"], help="句子拆分策略。")
    translate.add_argument("--preserve-formatting", action="store_true", help="尽量保留原始格式。")
    translate.add_argument("--outline-detection", choices=["true", "false"], help="仅 XML 标签处理场景常用。")
    translate.add_argument("--show-billed-characters", action="store_true", help="在响应中返回计费字符数。")
    translate.add_argument("--enable-beta-languages", action="store_true", help="启用 beta 语言支持。")
    translate.add_argument("--non-splitting-tags", action="append", help="不参与句子拆分的标签名。可重复。")
    translate.add_argument("--splitting-tags", action="append", help="显式参与句子拆分的标签名。可重复。")
    translate.add_argument("--ignore-tags", action="append", help="忽略翻译的标签名。可重复。")
    translate.add_argument("--style-id", help="风格规则 ID。")
    translate.add_argument("--custom-instructions", help="自定义翻译说明。")

    languages = subparsers.add_parser("languages", help="查询语言", description="调用 /v2/languages 查询支持的语言。")
    add_common_options(languages)
    languages.add_argument("--type", choices=["source", "target"], default="source", help="查询源语言还是目标语言。默认 source。")

    usage = subparsers.add_parser("usage", help="查询用量", description="调用 /v2/usage 查询当前账期用量和额度。")
    add_common_options(usage)

    rephrase = subparsers.add_parser("rephrase", help="文本润色", description="调用 /write/rephrase 进行改写或润色，不做跨语种翻译。")
    add_common_options(rephrase)
    add_text_options(rephrase, require_target=False)
    rephrase.add_argument(
        "--writing-style",
        choices=["default", "simple", "business", "academic", "casual", "prefer_simple", "prefer_business", "prefer_academic", "prefer_casual"],
        help="写作风格。",
    )
    rephrase.add_argument(
        "--tone",
        choices=["default", "confident", "diplomatic", "enthusiastic", "friendly", "prefer_confident", "prefer_diplomatic", "prefer_enthusiastic", "prefer_friendly"],
        help="语气。",
    )

    document_upload = subparsers.add_parser("document-upload", help="上传文档翻译", description="调用 /v2/document 上传文档并启动翻译。")
    add_common_options(document_upload)
    document_upload.add_argument("--file", required=True, help="待翻译文件路径。")
    document_upload.add_argument("--target-lang", required=True, help="目标语言代码。")
    document_upload.add_argument("--source-lang", help="源语言代码。")
    document_upload.add_argument("--filename", help="上传到服务端时使用的文件名。")
    document_upload.add_argument("--formality", choices=FORMALITY_CHOICES, help="正式程度。")
    document_upload.add_argument("--glossary-id", help="词汇表 ID。")
    document_upload.add_argument("--output-format", help="输出格式，例如 docx。")

    document_status = subparsers.add_parser("document-status", help="查询文档状态", description="调用 /v2/document/{document_id} 查询文档翻译状态。")
    add_common_options(document_status)
    document_status.add_argument("--document-id", required=True, help="文档 ID。")
    document_status.add_argument("--document-key", required=True, help="文档 key。")

    document_download = subparsers.add_parser("document-download", help="下载文档结果", description="调用 /v2/document/{document_id}/result 下载翻译后的文档。")
    add_common_options(document_download)
    document_download.add_argument("--document-id", required=True, help="文档 ID。")
    document_download.add_argument("--document-key", required=True, help="文档 key。")
    document_download.add_argument("--output-file", required=True, help="输出文件路径。")

    document_translate = subparsers.add_parser("document-translate", help="一键文档翻译", description="封装上传、轮询、下载，完成文档翻译闭环。")
    add_common_options(document_translate)
    document_translate.add_argument("--file", required=True, help="待翻译文件路径。")
    document_translate.add_argument("--target-lang", required=True, help="目标语言代码。")
    document_translate.add_argument("--source-lang", help="源语言代码。")
    document_translate.add_argument("--filename", help="上传到服务端时使用的文件名。")
    document_translate.add_argument("--formality", choices=FORMALITY_CHOICES, help="正式程度。")
    document_translate.add_argument("--glossary-id", help="词汇表 ID。")
    document_translate.add_argument("--output-format", help="输出格式，例如 docx。")
    document_translate.add_argument("--output-file", help="输出文件路径。不传则在原文件旁生成。")
    document_translate.add_argument("--poll-interval", type=int, default=5, help="轮询间隔秒数，默认 5。")

    glossary_pairs = subparsers.add_parser("glossary-language-pairs", help="查询 glossary 语言对", description="调用 /v2/glossary-language-pairs。")
    add_common_options(glossary_pairs)

    glossary_v2_list = subparsers.add_parser("glossary-v2-list", help="列出 v2 glossaries", description="调用 /v2/glossaries 列出单语种词汇表。")
    add_common_options(glossary_v2_list)

    glossary_v2_get = subparsers.add_parser("glossary-v2-get", help="查看 v2 glossary", description="调用 /v2/glossaries/{id} 获取详情。")
    add_common_options(glossary_v2_get)
    glossary_v2_get.add_argument("--glossary-id", required=True, help="glossary ID。")

    glossary_v2_entries = subparsers.add_parser("glossary-v2-entries", help="获取 v2 glossary 条目", description="调用 /v2/glossaries/{id}/entries 获取 TSV 条目。")
    add_common_options(glossary_v2_entries)
    glossary_v2_entries.add_argument("--glossary-id", required=True, help="glossary ID。")

    glossary_v2_create = subparsers.add_parser("glossary-v2-create", help="创建 v2 glossary", description="调用 /v2/glossaries 创建单语言对词汇表。")
    add_common_options(glossary_v2_create)
    glossary_v2_create.add_argument("--name", required=True, help="词汇表名称。")
    glossary_v2_create.add_argument("--source-lang", required=True, help="源语言代码。")
    glossary_v2_create.add_argument("--target-lang", required=True, help="目标语言代码。")
    glossary_v2_create.add_argument("--entries", help="直接传入 CSV/TSV 文本内容。")
    glossary_v2_create.add_argument("--entries-file", help="从文件读取条目。")
    glossary_v2_create.add_argument("--entries-format", choices=["csv", "tsv"], default="tsv", help="条目格式。默认 tsv。")

    glossary_v2_delete = subparsers.add_parser("glossary-v2-delete", help="删除 v2 glossary", description="调用 /v2/glossaries/{id} 删除词汇表。")
    add_common_options(glossary_v2_delete)
    glossary_v2_delete.add_argument("--glossary-id", required=True, help="glossary ID。")

    glossary_v3_list = subparsers.add_parser("glossary-v3-list", help="列出 v3 glossaries", description="调用 /v3/glossaries 列出多语言词汇表。")
    add_common_options(glossary_v3_list)

    glossary_v3_get = subparsers.add_parser("glossary-v3-get", help="查看 v3 glossary", description="调用 /v3/glossaries/{id} 获取详情。")
    add_common_options(glossary_v3_get)
    glossary_v3_get.add_argument("--glossary-id", required=True, help="glossary ID。")

    glossary_v3_entries = subparsers.add_parser("glossary-v3-entries", help="获取 v3 glossary 条目", description="调用 /v3/glossaries/{id}/entries 获取指定语言对条目。")
    add_common_options(glossary_v3_entries)
    glossary_v3_entries.add_argument("--glossary-id", required=True, help="glossary ID。")
    glossary_v3_entries.add_argument("--source-lang", required=True, help="源语言代码。")
    glossary_v3_entries.add_argument("--target-lang", required=True, help="目标语言代码。")

    glossary_v3_create = subparsers.add_parser("glossary-v3-create", help="创建 v3 glossary", description="调用 /v3/glossaries 创建多语言词汇表。")
    add_common_options(glossary_v3_create)
    glossary_v3_create.add_argument("--name", required=True, help="词汇表名称。")
    glossary_v3_create.add_argument("--dict", action="append", dest="dict_specs", required=True, help="字典定义，格式 source_lang:target_lang:entries_file[:entries_format]。可重复。")

    glossary_v3_patch = subparsers.add_parser("glossary-v3-patch", help="更新 v3 glossary", description="调用 PATCH /v3/glossaries/{id} 修改名称或合并字典条目。")
    add_common_options(glossary_v3_patch)
    glossary_v3_patch.add_argument("--glossary-id", required=True, help="glossary ID。")
    glossary_v3_patch.add_argument("--name", help="新的词汇表名称。")
    glossary_v3_patch.add_argument("--source-lang", help="要合并的字典源语言。")
    glossary_v3_patch.add_argument("--target-lang", help="要合并的字典目标语言。")
    glossary_v3_patch.add_argument("--entries", help="直接传入 CSV/TSV 文本内容。")
    glossary_v3_patch.add_argument("--entries-file", help="从文件读取条目。")
    glossary_v3_patch.add_argument("--entries-format", choices=["csv", "tsv"], default="tsv", help="条目格式。默认 tsv。")

    glossary_v3_put = subparsers.add_parser("glossary-v3-put", help="替换 v3 字典", description="调用 PUT /v3/glossaries/{id}/dictionaries 替换指定语言对字典。")
    add_common_options(glossary_v3_put)
    glossary_v3_put.add_argument("--glossary-id", required=True, help="glossary ID。")
    glossary_v3_put.add_argument("--source-lang", required=True, help="源语言代码。")
    glossary_v3_put.add_argument("--target-lang", required=True, help="目标语言代码。")
    glossary_v3_put.add_argument("--entries", help="直接传入 CSV/TSV 文本内容。")
    glossary_v3_put.add_argument("--entries-file", help="从文件读取条目。")
    glossary_v3_put.add_argument("--entries-format", choices=["csv", "tsv"], default="tsv", help="条目格式。默认 tsv。")

    glossary_v3_delete_dict = subparsers.add_parser("glossary-v3-delete-dict", help="删除 v3 字典", description="调用 DELETE /v3/glossaries/{id}/dictionaries 删除指定语言对字典。")
    add_common_options(glossary_v3_delete_dict)
    glossary_v3_delete_dict.add_argument("--glossary-id", required=True, help="glossary ID。")
    glossary_v3_delete_dict.add_argument("--source-lang", required=True, help="源语言代码。")
    glossary_v3_delete_dict.add_argument("--target-lang", required=True, help="目标语言代码。")

    glossary_v3_delete = subparsers.add_parser("glossary-v3-delete", help="删除 v3 glossary", description="调用 DELETE /v3/glossaries/{id} 删除词汇表。")
    add_common_options(glossary_v3_delete)
    glossary_v3_delete.add_argument("--glossary-id", required=True, help="glossary ID。")

    return parser


def ensure_command(parser: argparse.ArgumentParser) -> List[str]:
    argv = sys.argv[1:]
    known = {
        "translate", "languages", "usage", "rephrase", "document-upload", "document-status",
        "document-download", "document-translate", "glossary-language-pairs", "glossary-v2-list",
        "glossary-v2-get", "glossary-v2-entries", "glossary-v2-create", "glossary-v2-delete",
        "glossary-v3-list", "glossary-v3-get", "glossary-v3-entries", "glossary-v3-create",
        "glossary-v3-patch", "glossary-v3-put", "glossary-v3-delete-dict", "glossary-v3-delete",
    }
    if not argv:
        parser.print_help()
        raise SystemExit(0)
    if len(argv) == 1 and argv[0] in ("-h", "--help"):
        return argv
    if argv[0].startswith("-") or argv[0] not in known:
        return ["translate"] + argv
    return argv


def get_api_key() -> str:
    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise SystemExit("未设置 DEEPL_API_KEY。")
    return api_key


def get_base_url(args: argparse.Namespace) -> str:
    base_url = os.environ.get("DEEPL_API_BASE_URL") or DEFAULT_BASE_URL
    base_url = base_url.rstrip("/")
    if base_url not in ALLOWED_BASE_URLS:
        allowed = " 或 ".join(sorted(ALLOWED_BASE_URLS))
        raise SystemExit("DEEPL_API_BASE_URL 仅允许配置为 {}。".format(allowed))
    return base_url


def read_entries(entries: Optional[str], entries_file: Optional[str]) -> str:
    if entries is not None:
        return entries
    if entries_file:
        with open(entries_file, "r", encoding="utf-8") as handle:
            return handle.read()
    raise SystemExit("未提供条目内容。请使用 --entries 或 --entries-file。")


def collect_texts(args: argparse.Namespace) -> List[str]:
    texts = []
    if getattr(args, "texts", None):
        texts.extend(args.texts)
    if getattr(args, "file", None) and args.command in ("translate", "rephrase"):
        with open(args.file, "r", encoding="utf-8") as handle:
            texts.append(handle.read())
    if getattr(args, "stdin", False):
        texts.append(sys.stdin.read())
    texts = [text for text in texts if text]
    if not texts:
        raise SystemExit("未提供输入文本。请使用 --text、--file 或 --stdin。")
    if len(texts) > 50:
        raise SystemExit("DeepL 单次文本请求最多接受 50 个 text 项。")
    return texts


def build_headers(api_key: str, content_type: Optional[str] = None, extra_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    headers = {"Authorization": "DeepL-Auth-Key " + api_key}
    if content_type:
        headers["Content-Type"] = content_type
    if extra_headers:
        headers.update(extra_headers)
    return headers


def perform_request(
    base_url: str,
    api_key: str,
    path: str,
    method: str = "GET",
    json_body: Optional[dict] = None,
    form_body: Optional[dict] = None,
    multipart_body: Optional[List[Tuple[str, Optional[str], bytes, Optional[str]]]] = None,
    query: Optional[dict] = None,
    extra_headers: Optional[Dict[str, str]] = None,
    timeout: int = DEFAULT_TIMEOUT,
    binary_response: bool = False,
) -> Tuple[int, Dict[str, str], object]:
    url = base_url.rstrip("/") + path
    if query:
        query = {key: value for key, value in query.items() if value is not None}
        if query:
            url += "?" + urllib.parse.urlencode(query)

    data = None
    content_type = None
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        content_type = "application/json"
    elif form_body is not None:
        encoded = urllib.parse.urlencode({key: value for key, value in form_body.items() if value is not None})
        data = encoded.encode("utf-8")
        content_type = "application/x-www-form-urlencoded"
    elif multipart_body is not None:
        boundary = "----DeepLSkillBoundary" + uuid.uuid4().hex
        data = build_multipart_body(boundary, multipart_body)
        content_type = "multipart/form-data; boundary=" + boundary

    request = urllib.request.Request(
        url,
        data=data,
        headers=build_headers(api_key, content_type=content_type, extra_headers=extra_headers),
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
            headers = dict(response.headers.items())
            headers_lower = {key.lower(): value for key, value in headers.items()}
            if binary_response:
                return response.getcode(), headers, raw
            if not raw:
                return response.getcode(), headers, {}
            content_type_header = headers_lower.get("content-type", "")
            if "application/json" in content_type_header:
                return response.getcode(), headers, json.loads(raw.decode("utf-8"))
            return response.getcode(), headers, raw.decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit("DeepL API 请求失败：HTTP {}: {}".format(exc.code, body)) from exc
    except urllib.error.URLError as exc:
        raise SystemExit("DeepL API 请求失败：{}".format(exc.reason)) from exc


def build_multipart_body(boundary: str, parts: List[Tuple[str, Optional[str], bytes, Optional[str]]]) -> bytes:
    lines = []
    for field_name, filename, content, content_type in parts:
        lines.append(("--" + boundary).encode("utf-8"))
        disposition = 'Content-Disposition: form-data; name="{}"'.format(field_name)
        if filename is not None:
            disposition += '; filename="{}"'.format(filename)
        lines.append(disposition.encode("utf-8"))
        if content_type:
            lines.append(("Content-Type: " + content_type).encode("utf-8"))
        lines.append(b"")
        lines.append(content)
    lines.append(("--" + boundary + "--").encode("utf-8"))
    lines.append(b"")
    return b"\r\n".join(lines)


def build_translate_payload(args: argparse.Namespace, texts: List[str]) -> dict:
    if args.glossary_id and not args.source_lang:
        raise SystemExit("--glossary-id 需要同时提供 --source-lang。")
    payload = {
        "text": texts,
        "target_lang": args.target_lang,
    }
    optional_fields = {
        "source_lang": args.source_lang,
        "context": args.context,
        "formality": args.formality,
        "model_type": args.model_type,
        "glossary_id": args.glossary_id,
        "tag_handling": args.tag_handling,
        "tag_handling_version": args.tag_handling_version,
        "split_sentences": args.split_sentences,
        "style_id": args.style_id,
        "custom_instructions": args.custom_instructions,
    }
    for key, value in optional_fields.items():
        if value is not None:
            payload[key] = value
    if args.preserve_formatting:
        payload["preserve_formatting"] = True
    if args.show_billed_characters:
        payload["show_billed_characters"] = True
    if args.enable_beta_languages:
        payload["enable_beta_languages"] = True
    if args.outline_detection is not None:
        payload["outline_detection"] = args.outline_detection == "true"
    for list_name, api_name in [
        ("non_splitting_tags", "non_splitting_tags"),
        ("splitting_tags", "splitting_tags"),
        ("ignore_tags", "ignore_tags"),
    ]:
        value = getattr(args, list_name, None)
        if value:
            payload[api_name] = value
    return payload


def build_rephrase_payload(args: argparse.Namespace, texts: List[str]) -> dict:
    if args.writing_style and args.tone:
        raise SystemExit("--writing-style 和 --tone 不能同时使用。")
    payload = {"text": texts}
    if args.target_lang:
        payload["target_lang"] = args.target_lang
    if args.writing_style:
        payload["writing_style"] = args.writing_style
    if args.tone:
        payload["tone"] = args.tone
    return payload


def build_document_parts(args: argparse.Namespace) -> List[Tuple[str, Optional[str], bytes, Optional[str]]]:
    parts = []
    form_fields = {
        "target_lang": args.target_lang,
        "source_lang": args.source_lang,
        "filename": args.filename,
        "formality": args.formality,
        "glossary_id": args.glossary_id,
        "output_format": args.output_format,
    }
    for key, value in form_fields.items():
        if value is not None:
            parts.append((key, None, str(value).encode("utf-8"), None))
    file_name = args.filename or os.path.basename(args.file)
    mime_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"
    with open(args.file, "rb") as handle:
        parts.append(("file", file_name, handle.read(), mime_type))
    return parts


def parse_dict_spec(spec: str) -> dict:
    parts = spec.split(":")
    if len(parts) not in (3, 4):
        raise SystemExit("--dict 格式错误，应为 source_lang:target_lang:entries_file[:entries_format]")
    source_lang, target_lang, entries_file = parts[0], parts[1], parts[2]
    entries_format = parts[3] if len(parts) == 4 else "tsv"
    if entries_format not in ("csv", "tsv"):
        raise SystemExit("--dict 中 entries_format 仅支持 csv 或 tsv。")
    with open(entries_file, "r", encoding="utf-8") as handle:
        entries = handle.read()
    return {
        "source_lang": source_lang,
        "target_lang": target_lang,
        "entries": entries,
        "entries_format": entries_format,
    }


def print_response(data: object, as_json: bool) -> None:
    if as_json or not isinstance(data, (dict, list)):
        if isinstance(data, (dict, list)):
            json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
            sys.stdout.write("\n")
        else:
            print(data)
        return
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def get_output_file_path(input_path: str, explicit_output: Optional[str], output_format: Optional[str]) -> str:
    if explicit_output:
        return explicit_output
    root, ext = os.path.splitext(input_path)
    final_ext = ext
    if output_format:
        final_ext = "." + output_format.lstrip(".")
    return root + ".translated" + final_ext


def cmd_translate(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    texts = collect_texts(args)
    payload = build_translate_payload(args, texts)
    _, _, response = perform_request(base_url, api_key, "/v2/translate", method="POST", json_body=payload, timeout=args.timeout)
    if args.json:
        print_response(response, True)
        return
    for item in response.get("translations", []):
        print(item.get("text", ""))


def cmd_languages(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    _, _, response = perform_request(base_url, api_key, "/v2/languages", method="GET", query={"type": args.type}, timeout=args.timeout)
    print_response(response, args.json)


def cmd_usage(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    _, _, response = perform_request(base_url, api_key, "/v2/usage", method="GET", timeout=args.timeout)
    print_response(response, args.json)


def cmd_rephrase(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    texts = collect_texts(args)
    payload = build_rephrase_payload(args, texts)
    _, _, response = perform_request(base_url, api_key, "/v2/write/rephrase", method="POST", json_body=payload, timeout=args.timeout)
    if args.json:
        print_response(response, True)
        return
    results = response.get("improvements") or response.get("rephrased_texts") or response.get("texts") or []
    if results:
        for item in results:
            if isinstance(item, dict):
                print(item.get("text", ""))
            else:
                print(item)
        return
    print_response(response, True)


def cmd_document_upload(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    _, _, response = perform_request(
        base_url,
        api_key,
        "/v2/document",
        method="POST",
        multipart_body=build_document_parts(args),
        timeout=args.timeout,
    )
    print_response(response, args.json)


def cmd_document_status(args: argparse.Namespace, base_url: str, api_key: str) -> dict:
    _, _, response = perform_request(
        base_url,
        api_key,
        "/v2/document/{}".format(args.document_id),
        method="POST",
        form_body={"document_key": args.document_key},
        timeout=args.timeout,
    )
    print_response(response, args.json)
    return response


def cmd_document_download(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    _, headers, data = perform_request(
        base_url,
        api_key,
        "/v2/document/{}/result".format(args.document_id),
        method="POST",
        form_body={"document_key": args.document_key},
        timeout=args.timeout,
        binary_response=True,
    )
    with open(args.output_file, "wb") as handle:
        handle.write(data)
    if args.json:
        print_response({"output_file": args.output_file, "content_type": headers.get("Content-Type")}, True)
    else:
        print("已下载到: {}".format(args.output_file))


def cmd_document_translate(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    _, _, upload_response = perform_request(
        base_url,
        api_key,
        "/v2/document",
        method="POST",
        multipart_body=build_document_parts(args),
        timeout=args.timeout,
    )
    document_id = upload_response["document_id"]
    document_key = upload_response["document_key"]
    while True:
        _, _, status = perform_request(
            base_url,
            api_key,
            "/v2/document/{}".format(document_id),
            method="POST",
            form_body={"document_key": document_key},
            timeout=args.timeout,
        )
        state = status.get("status")
        if state == "done":
            break
        if state == "error":
            raise SystemExit("文档翻译失败：{}".format(status.get("error_message", "未知错误")))
        print("当前状态: {}，预计剩余 {} 秒".format(state, status.get("seconds_remaining", "?")), file=sys.stderr)
        time.sleep(args.poll_interval)
    output_file = get_output_file_path(args.file, args.output_file, args.output_format)
    _, headers, data = perform_request(
        base_url,
        api_key,
        "/v2/document/{}/result".format(document_id),
        method="POST",
        form_body={"document_key": document_key},
        timeout=args.timeout,
        binary_response=True,
    )
    with open(output_file, "wb") as handle:
        handle.write(data)
    if args.json:
        print_response(
            {
                "document_id": document_id,
                "document_key": document_key,
                "output_file": output_file,
                "content_type": headers.get("Content-Type"),
                "status": "done",
            },
            True,
        )
    else:
        print("文档翻译完成: {}".format(output_file))


def cmd_glossary_language_pairs(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    _, _, response = perform_request(base_url, api_key, "/v2/glossary-language-pairs", method="GET", timeout=args.timeout)
    print_response(response, args.json)


def cmd_glossary_v2_list(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    _, _, response = perform_request(base_url, api_key, "/v2/glossaries", method="GET", timeout=args.timeout)
    print_response(response, args.json)


def cmd_glossary_v2_get(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    _, _, response = perform_request(base_url, api_key, "/v2/glossaries/{}".format(args.glossary_id), method="GET", timeout=args.timeout)
    print_response(response, args.json)


def cmd_glossary_v2_entries(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    _, _, response = perform_request(
        base_url,
        api_key,
        "/v2/glossaries/{}/entries".format(args.glossary_id),
        method="GET",
        extra_headers={"Accept": "text/tab-separated-values"},
        timeout=args.timeout,
    )
    print_response(response, args.json)


def cmd_glossary_v2_create(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    payload = {
        "name": args.name,
        "source_lang": args.source_lang,
        "target_lang": args.target_lang,
        "entries": read_entries(args.entries, args.entries_file),
        "entries_format": args.entries_format,
    }
    _, _, response = perform_request(base_url, api_key, "/v2/glossaries", method="POST", json_body=payload, timeout=args.timeout)
    print_response(response, args.json)


def cmd_glossary_v2_delete(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    _, _, response = perform_request(base_url, api_key, "/v2/glossaries/{}".format(args.glossary_id), method="DELETE", timeout=args.timeout)
    print_response(response, True)


def cmd_glossary_v3_list(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    _, _, response = perform_request(base_url, api_key, "/v3/glossaries", method="GET", timeout=args.timeout)
    print_response(response, args.json)


def cmd_glossary_v3_get(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    _, _, response = perform_request(base_url, api_key, "/v3/glossaries/{}".format(args.glossary_id), method="GET", timeout=args.timeout)
    print_response(response, args.json)


def cmd_glossary_v3_entries(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    _, _, response = perform_request(
        base_url,
        api_key,
        "/v3/glossaries/{}/entries".format(args.glossary_id),
        method="GET",
        query={"source_lang": args.source_lang, "target_lang": args.target_lang},
        timeout=args.timeout,
    )
    print_response(response, args.json)


def cmd_glossary_v3_create(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    payload = {
        "name": args.name,
        "dictionaries": [parse_dict_spec(spec) for spec in args.dict_specs],
    }
    _, _, response = perform_request(base_url, api_key, "/v3/glossaries", method="POST", json_body=payload, timeout=args.timeout)
    print_response(response, args.json)


def cmd_glossary_v3_patch(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    payload = {}
    if args.name:
        payload["name"] = args.name
    if args.source_lang or args.target_lang or args.entries or args.entries_file:
        if not (args.source_lang and args.target_lang):
            raise SystemExit("更新字典内容时必须同时提供 --source-lang 和 --target-lang。")
        payload.update(
            {
                "source_lang": args.source_lang,
                "target_lang": args.target_lang,
                "entries": read_entries(args.entries, args.entries_file),
                "entries_format": args.entries_format,
            }
        )
    if not payload:
        raise SystemExit("至少提供 --name 或一组字典更新参数。")
    _, _, response = perform_request(
        base_url,
        api_key,
        "/v3/glossaries/{}".format(args.glossary_id),
        method="PATCH",
        json_body=payload,
        timeout=args.timeout,
    )
    print_response(response, args.json)


def cmd_glossary_v3_put(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    payload = {
        "source_lang": args.source_lang,
        "target_lang": args.target_lang,
        "entries": read_entries(args.entries, args.entries_file),
        "entries_format": args.entries_format,
    }
    _, _, response = perform_request(
        base_url,
        api_key,
        "/v3/glossaries/{}/dictionaries".format(args.glossary_id),
        method="PUT",
        json_body=payload,
        timeout=args.timeout,
    )
    print_response(response, args.json)


def cmd_glossary_v3_delete_dict(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    _, _, response = perform_request(
        base_url,
        api_key,
        "/v3/glossaries/{}/dictionaries".format(args.glossary_id),
        method="DELETE",
        query={"source_lang": args.source_lang, "target_lang": args.target_lang},
        timeout=args.timeout,
    )
    print_response(response, True)


def cmd_glossary_v3_delete(args: argparse.Namespace, base_url: str, api_key: str) -> None:
    _, _, response = perform_request(base_url, api_key, "/v3/glossaries/{}".format(args.glossary_id), method="DELETE", timeout=args.timeout)
    print_response(response, True)


COMMAND_HANDLERS = {
    "translate": cmd_translate,
    "languages": cmd_languages,
    "usage": cmd_usage,
    "rephrase": cmd_rephrase,
    "document-upload": cmd_document_upload,
    "document-status": cmd_document_status,
    "document-download": cmd_document_download,
    "document-translate": cmd_document_translate,
    "glossary-language-pairs": cmd_glossary_language_pairs,
    "glossary-v2-list": cmd_glossary_v2_list,
    "glossary-v2-get": cmd_glossary_v2_get,
    "glossary-v2-entries": cmd_glossary_v2_entries,
    "glossary-v2-create": cmd_glossary_v2_create,
    "glossary-v2-delete": cmd_glossary_v2_delete,
    "glossary-v3-list": cmd_glossary_v3_list,
    "glossary-v3-get": cmd_glossary_v3_get,
    "glossary-v3-entries": cmd_glossary_v3_entries,
    "glossary-v3-create": cmd_glossary_v3_create,
    "glossary-v3-patch": cmd_glossary_v3_patch,
    "glossary-v3-put": cmd_glossary_v3_put,
    "glossary-v3-delete-dict": cmd_glossary_v3_delete_dict,
    "glossary-v3-delete": cmd_glossary_v3_delete,
}


def main() -> None:
    parser = build_parser()
    argv = ensure_command(parser)
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        raise SystemExit(0)
    api_key = get_api_key()
    base_url = get_base_url(args)
    handler = COMMAND_HANDLERS[args.command]
    handler(args, base_url, api_key)


if __name__ == "__main__":
    main()
