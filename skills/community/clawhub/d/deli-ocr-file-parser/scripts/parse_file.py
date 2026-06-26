#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import uuid
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


OPENAPI_BASE_URL = "https://platform.delilegal.com/api/v1"
CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.json"
SKILL_PATH = Path(__file__).resolve().parents[1] / "SKILL.md"
SUPPORTED_EXTENSIONS = {
    ".img",
    ".html",
    ".docx",
    ".doc",
    ".docm",
    ".dotm",
    ".txt",
    ".pdf",
    ".png",
    ".jpeg",
    ".gif",
    ".bmp",
    ".rtf",
    ".xlsx",
    ".xls",
    ".ofd",
}


class OcrToolError(Exception):
    pass


class SkillRequestContext:
    def __init__(self, root_dir: Optional[Path] = None, filename: str = ".session") -> None:
        self.session_id = self._load_session(Path(root_dir or os.getcwd()) / filename)
        self.skill_id, self.skill_version = self._load_skill_meta(SKILL_PATH)
        self.headers = {
            "Session-Id": self.session_id,
            "Skill-Id": self.skill_id,
            "Skill-Version": self.skill_version,
        }

    @staticmethod
    def _load_session(path: Path) -> str:
        session_id = path.read_text(encoding="utf-8").strip() if path.exists() else ""
        if session_id:
            return session_id
        session_id = str(uuid.uuid4())
        path.write_text(session_id, encoding="utf-8")
        return session_id

    @staticmethod
    def _load_skill_meta(path: Path) -> tuple[str, str]:
        text = path.read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1] if text.startswith("---") else text
        name = re.search(r"^name:\s*[\"']?([^\"'\n]+)", frontmatter, re.MULTILINE)
        version = re.search(r"^\s*version:\s*[\"']?([^\"'\n]+)", frontmatter, re.MULTILINE)
        return (
            name.group(1).strip() if name else "deli-ocr-file-parser",
            version.group(1).strip() if version else "1.0.0",
        )


REQUEST_CONTEXT = SkillRequestContext()


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_text(path: Path, content: str) -> None:
    ensure_directory(path.parent)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    ensure_directory(path.parent)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_config() -> Dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {}
    try:
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        raise OcrToolError(f"读取或解析 config.json 失败：{exc}") from exc
    if not isinstance(config, dict):
        raise OcrToolError("config.json 格式错误，应为 JSON 对象。")
    return config


def get_config_value(config: Dict[str, Any], *keys: str, default: str = "") -> str:
    for key in keys:
        value = config.get(key)
        if value is not None:
            text = str(value).strip()
            if text and text != "YOUR_API_KEY":
                return text
    return default


def get_api_key(config: Dict[str, Any]) -> str:
    return (
        get_config_value(config, "apikey", "apiKey", "api_key", "APIKey")
        or get_config_value(config, "ocrApiKey", "ocr_api_key", "ocr_apikey")
        or os.getenv("EVIDENCE_OCR_API_TOKEN", "").strip()
        or os.getenv("EVIDENCE_FILE_API_TOKEN", "").strip()
        or os.getenv("AILAWYERS_API_KEY", "").strip()
    )


def validate_supported_file(path: Path) -> None:
    if path.suffix.lower() in SUPPORTED_EXTENSIONS:
        return
    ext = path.suffix.lower() or "(无扩展名)"
    raise OcrToolError(
        "\n".join(
            [
                "文件格式不支持",
                "",
                f"文件「{path.name}」格式为「{ext}」，请转换为支持格式后重新处理。",
                "支持格式：.pdf、.docx、.doc、.docm、.dotm、.rtf、.txt、.ofd、.xlsx、.xls、.png、.jpeg、.gif、.bmp、.img、.html",
            ]
        )
    )


def md5_file(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def request_json_api(
    *,
    url: str,
    payload: Dict[str, Any],
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 60,
) -> Dict[str, Any]:
    request_headers = {"Content-Type": "application/json"}
    if headers:
        request_headers.update(headers)
    if "platform.delilegal.com" in url:
        request_headers.update(REQUEST_CONTEXT.headers)

    request = Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=request_headers,
        method="POST",
    )
    return read_json_response(request, timeout=timeout)


def read_json_response(request: Request, *, timeout: int) -> Dict[str, Any]:
    try:
        with urlopen(request, timeout=timeout) as response:  # type: ignore[call-arg]
            data = response.read().decode("utf-8")
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise OcrToolError(f"接口调用失败，HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise OcrToolError(f"接口调用失败：{exc}") from exc
    except Exception as exc:
        raise OcrToolError(f"接口调用失败：{exc}") from exc

    try:
        parsed = json.loads(data)
    except json.JSONDecodeError as exc:
        parsed = parse_event_stream_response(data)
        if not parsed:
            raise OcrToolError(f"接口返回的不是合法 JSON：{exc}") from exc
    if not isinstance(parsed, dict):
        raise OcrToolError("接口返回 JSON 格式错误，应为对象。")
    return parsed


def parse_event_stream_response(data: str) -> Dict[str, Any]:
    events = []
    content_parts = []
    last_message: Dict[str, Any] = {}

    for line in data.splitlines():
        line = line.strip()
        if not line.startswith("data:"):
            continue
        value = line[5:].strip()
        if not value or value in {"[DONE]", "[HEARTBEAT]"}:
            continue
        try:
            payload = json.loads(value)
        except json.JSONDecodeError:
            content_parts.append(value)
            continue
        if isinstance(payload, dict):
            events.append(payload)
            last_message = payload
            content = payload.get("content")
            if content:
                content_parts.append(str(content))

    if not events and not content_parts:
        return {}

    success = last_message.get("success")
    return {
        "success": success if isinstance(success, bool) else True,
        "msg": last_message.get("msg") or "",
        "text": "\n".join(content_parts).strip(),
        "events": events,
    }


def find_first_string_by_key(payload: Any, keys: set[str]) -> str:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in keys and isinstance(value, str) and value.strip():
                return value.strip()
        for value in payload.values():
            found = find_first_string_by_key(value, keys)
            if found:
                return found
    elif isinstance(payload, list):
        for item in payload:
            found = find_first_string_by_key(item, keys)
            if found:
                return found
    return ""


def find_upload_url(payload: Dict[str, Any]) -> str:
    return find_first_string_by_key(
        payload,
        {
            "uploadUrl",
            "uploadURL",
            "upload_url",
            "putUrl",
            "putURL",
            "put_url",
            "ossUrl",
            "ossURL",
            "oss_url",
            "signedUrl",
            "signedURL",
            "signed_url",
            "url",
        },
    )


def find_upload_headers(payload: Dict[str, Any]) -> Dict[str, str]:
    body = payload.get("body") if isinstance(payload, dict) else None
    headers = body.get("headers") if isinstance(body, dict) else None
    if not isinstance(headers, dict):
        return {}
    return {str(key): str(value) for key, value in headers.items() if str(key).strip()}


def is_upload_already_present(payload: Dict[str, Any]) -> bool:
    body = payload.get("body") if isinstance(payload, dict) else None
    return isinstance(body, dict) and body.get("exist") is True


def put_binary_file(
    *,
    url: str,
    path: Path,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 180,
) -> None:
    request_headers = {"Content-Type": "application/octet-stream"}
    if headers:
        request_headers.update(headers)
    request = Request(url, data=path.read_bytes(), headers=request_headers, method="PUT")
    try:
        with urlopen(request, timeout=timeout) as response:  # type: ignore[call-arg]
            if response.status < 200 or response.status >= 300:
                detail = response.read().decode("utf-8", errors="ignore")
                raise OcrToolError(f"文件上传失败，HTTP {response.status}: {detail}")
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise OcrToolError(f"文件上传失败，HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise OcrToolError(f"文件上传失败：{exc}") from exc


def call_legacy_ocr_api(
    *,
    url: str,
    file_path: Path,
    task_type: str,
    lang: str,
    token: str,
    timeout: int,
) -> Dict[str, Any]:
    payload = {
        "task_type": task_type,
        "file_name": file_path.name,
        "lang": lang,
        "file_base64": base64.b64encode(file_path.read_bytes()).decode("ascii"),
    }
    headers = {"Authorization": f"Bearer {token}"} if token else None
    return request_json_api(url=url, payload=payload, headers=headers, timeout=timeout)


def parse_file_with_deli_ocr(
    file_path: Path,
    *,
    task_type: str,
    lang: str,
    timeout: int,
) -> Dict[str, Any]:
    config = load_config()
    validate_supported_file(file_path)

    legacy_api_url = os.getenv("EVIDENCE_OCR_API_URL", "").strip()
    if legacy_api_url:
        return call_legacy_ocr_api(
            url=legacy_api_url,
            file_path=file_path,
            task_type=task_type,
            lang=lang,
            token=os.getenv("EVIDENCE_OCR_API_TOKEN", "").strip(),
            timeout=timeout,
        )

    api_key = get_api_key(config)
    if not api_key:
        raise OcrToolError(
            "config.json 中的 apikey 尚未配置。请前往 https://open.delilegal.com/personal/keys "
            "创建 API Key，并填入技能目录下的 config.json 文件中。"
        )

    base_url = get_config_value(
        config,
        "openapiBaseUrl",
        "openapi_base_url",
        "baseUrl",
        "base_url",
        default=OPENAPI_BASE_URL,
    ).rstrip("/")
    prepare_url = get_config_value(
        config,
        "prepareUploadFileUrl",
        "prepare_upload_file_url",
        "prepareUploadUrl",
        "prepare_upload_url",
        default=f"{base_url}/file/prepareUploadFile",
    )
    parsing_url = get_config_value(
        config,
        "fileParsingUrl",
        "file_parsing_url",
        "parsingUrl",
        "parsing_url",
        default=f"{base_url}/file/fileParsing",
    )

    headers = {"Authorization": f"Bearer {api_key}"}
    file_hash = md5_file(file_path)
    payload = {"fileHash": file_hash, "fileName": file_path.name}

    prepare_response = request_json_api(url=prepare_url, payload=payload, headers=headers, timeout=timeout)
    if prepare_response.get("success") is False:
        raise OcrToolError(
            "prepareUploadFile 调用失败，"
            f"code={prepare_response.get('code')}, msg={prepare_response.get('msg') or '未知错误'}"
        )

    upload_url = find_upload_url(prepare_response)
    if not upload_url:
        raise OcrToolError("prepareUploadFile 未返回可用的 OSS 上传地址。")

    if not is_upload_already_present(prepare_response):
        put_binary_file(
            url=upload_url,
            path=file_path,
            headers=find_upload_headers(prepare_response),
            timeout=timeout,
        )

    response = request_json_api(url=parsing_url, payload=payload, headers=headers, timeout=timeout)
    response.setdefault("source", "得理 OCR 文件解析接口")
    response.setdefault("task_type", task_type)
    return response


def collect_text_from_json_payload(payload: Any) -> str:
    if isinstance(payload, dict):
        return "\n".join(f"{key}: {collect_text_from_json_payload(value)}" for key, value in payload.items())
    if isinstance(payload, list):
        return "\n".join(collect_text_from_json_payload(item) for item in payload)
    return str(payload)


def extract_markdown_or_text(payload: Dict[str, Any]) -> str:
    text = find_first_string_by_key(
        payload,
        {"markdown", "text", "content", "md", "resultText", "result_text"},
    )
    if text:
        return text
    return collect_text_from_json_payload(payload).strip()


def build_markdown_document(input_path: Path, response: Dict[str, Any]) -> str:
    text = extract_markdown_or_text(response)
    if not text:
        raise OcrToolError("OCR 接口返回成功，但未找到可用 markdown/text 字段。")

    confidence = response.get("confidence") or response.get("result", {}).get("confidence") or "unknown"
    source = response.get("source") or "得理 OCR 文件解析接口"
    metadata = "\n".join(
        [
            "<!--",
            f"原始文件: {input_path.name}",
            f"来源: {source}",
            f"置信度: {confidence}",
            "-->",
        ]
    )
    return "\n".join([metadata, f"# {input_path.stem}", "", text.strip()]).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="在 Agent/平台无法解析文件时，调用得理 OCR 接口输出 Markdown。")
    parser.add_argument("input_file", help="输入文件路径")
    parser.add_argument("--output_dir", default=None, help="输出目录，默认与输入文件同目录")
    parser.add_argument("--lang", default="zh-cn+en", help="OCR 语言参数，默认 zh-cn+en")
    parser.add_argument("--task-type", default="file_parsing", help="接口任务类型，默认 file_parsing")
    parser.add_argument("--timeout", type=int, default=180, help="接口超时时间，默认 180 秒")
    parser.add_argument("--save-response", action="store_true", help="保存接口原始 JSON 响应")
    args = parser.parse_args()

    input_path = Path(args.input_file).resolve()
    if not input_path.exists() or not input_path.is_file():
        raise SystemExit(f"文件不存在：{input_path}")

    output_dir = Path(args.output_dir).resolve() if args.output_dir else input_path.parent
    ensure_directory(output_dir)

    response = parse_file_with_deli_ocr(
        input_path,
        task_type=args.task_type,
        lang=args.lang,
        timeout=args.timeout,
    )
    markdown = build_markdown_document(input_path, response)

    output_path = output_dir / f"{input_path.stem}.md"
    write_text(output_path, markdown)
    print(f"已输出 Markdown：{output_path}")

    if args.save_response:
        response_dir = ensure_directory(output_dir / "raw_response")
        response_path = response_dir / f"{input_path.stem}.ocr.json"
        write_json(response_path, response)
        print(f"已保存接口响应：{response_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except OcrToolError as exc:
        raise SystemExit(str(exc))
