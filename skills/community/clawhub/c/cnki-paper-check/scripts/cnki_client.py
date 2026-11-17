#!/usr/bin/env python3
"""Thin standard-library client for the fixed CQCCJY CNKI public workflow.

The client deliberately stops at safe public operations: read the live product
catalog, upload a document, create an order, query an original order or public
keyword, inspect report availability and hand verification back to the browser.
Payment, card settlement, CAPTCHA, admin operations and fulfillment routing are
excluded.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.json"
DOMAIN_PATH = ROOT / "domains" / "cqccjy.json"
CATALOG_PATH = ROOT / "references" / "product-catalog.json"

TERMINAL_STATUSES = {
    "REPORT_READY",
    "COMPLETED",
    "COMPLETE",
    "SUCCESS",
    "SUCCEEDED",
    "DONE",
}
FAILED_STATUSES = {"FAIL", "FAILED", "ERROR", "CANCELLED", "CANCELED"}
PAID_STATUSES = {"PAID", "SUCCESS", "COMPLETED", "PAY_SUCCESS", "PAYED"}
PROCESSING_STATUSES = {
    "PAID",
    "SUBMITTING",
    "SUBMITTED",
    "DETECTING",
    "PROCESSING",
    "PENDING",
}

PRODUCT_ALIASES = {
    "知网本科专科检测": "CNKI_UNDERGRADUATE",
    "知网本科专科": "CNKI_UNDERGRADUATE",
    "知网本科": "CNKI_UNDERGRADUATE",
    "知网本科版": "CNKI_UNDERGRADUATE",
    "知网专科": "CNKI_UNDERGRADUATE",
    "知网专科版": "CNKI_UNDERGRADUATE",
    "本科版": "CNKI_UNDERGRADUATE",
    "专科版": "CNKI_UNDERGRADUATE",
    "大学生版": "CNKI_UNDERGRADUATE",
    "知网硕博检测": "CNKI_GRADUATE",
    "知网硕博": "CNKI_GRADUATE",
    "知网研究生": "CNKI_GRADUATE",
    "知网硕士": "CNKI_GRADUATE",
    "知网博士": "CNKI_GRADUATE",
    "硕博版": "CNKI_GRADUATE",
    "研究生版": "CNKI_GRADUATE",
    "知网期刊检测": "CNKI_JOURNAL",
    "知网期刊": "CNKI_JOURNAL",
    "期刊版": "CNKI_JOURNAL",
    "投稿版": "CNKI_JOURNAL",
    "知网aigc检测": "CNKI_AIGC",
    "知网aigc": "CNKI_AIGC",
    "知网ai检测": "CNKI_AIGC",
    "知网ai率": "CNKI_AIGC",
    "知网aigc检测8万字及以上": "CNKI_AIGC_OVER_80000",
    "知网aigc8万字及以上": "CNKI_AIGC_OVER_80000",
    "知网aigc检测8万字符及以上": "CNKI_AIGC_OVER_80000",
    "知网aigc8万字符及以上": "CNKI_AIGC_OVER_80000",
    "知网aigc长文": "CNKI_AIGC_OVER_80000",
}


class CnkiError(RuntimeError):
    """Actionable error that excludes credentials, file contents and traces."""


def compact_text(value: Any) -> str:
    return re.sub(r"[\s·•,，。:：/\\()（）\[\]【】_\-]+", "", str(value or "")).lower()


def normalize_product(value: Any) -> str:
    text = str(value or "").strip()
    if text.upper().startswith("CNKI_"):
        return text.upper()
    return PRODUCT_ALIASES.get(compact_text(text), text)


def read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CnkiError(f"无法读取{label}: {exc}") from exc
    if not isinstance(data, dict):
        raise CnkiError(f"{label}必须是 JSON 对象")
    return data


def load_settings() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    config = read_json(CONFIG_PATH, "Skill 配置")
    domain = read_json(DOMAIN_PATH, "域名配置")
    catalog = read_json(CATALOG_PATH, "产品快照")
    base_url = domain.get("base_url")
    if not isinstance(base_url, str) or not base_url.startswith("https://"):
        raise CnkiError("知网基域名必须是 HTTPS")
    if domain.get("owner_user_id") != 2:
        raise CnkiError("知网域名配置的业务归属不匹配")
    if domain.get("channel") != "pcnki":
        raise CnkiError("知网公共渠道必须固定为 pcnki")
    return config, domain, catalog


def endpoint(domain: dict[str, Any], name: str, **values: Any) -> str:
    path = (domain.get("api") or {}).get(name)
    if not isinstance(path, str) or not path.startswith("/"):
        raise CnkiError(f"未配置接口: {name}")
    try:
        path = path.format(**values)
    except KeyError as exc:
        raise CnkiError(f"接口缺少参数: {exc.args[0]}") from exc
    return domain["base_url"].rstrip("/") + path


def browser_urls(domain: dict[str, Any], order_no: Any | None = None) -> dict[str, str]:
    pages: dict[str, str] = {}
    for name, template in (domain.get("pages") or {}).items():
        if not isinstance(template, str) or not template.startswith("https://"):
            continue
        if "{order_no}" in template:
            if order_no in (None, ""):
                continue
            template = template.replace(
                "{order_no}", urllib.parse.quote(str(order_no), safe="")
            )
        pages[name] = template
    return pages


def unwrap(payload: Any) -> Any:
    if not isinstance(payload, dict):
        return payload
    code = payload.get("code")
    if code not in (None, 0, "0", 200, "200"):
        message = payload.get("msg") or payload.get("message") or "请求失败"
        raise CnkiError(f"服务端返回错误（{code}）: {message}")
    return payload.get("data", payload)


def find_value(data: Any, *keys: str) -> Any:
    if isinstance(data, dict):
        for key in keys:
            value = data.get(key)
            if value not in (None, ""):
                return value
        for value in data.values():
            found = find_value(value, *keys)
            if found not in (None, ""):
                return found
    elif isinstance(data, list):
        for value in data:
            found = find_value(value, *keys)
            if found not in (None, ""):
                return found
    return None


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() not in {
            "",
            "0",
            "false",
            "no",
            "off",
            "none",
            "null",
        }
    return bool(value)


def is_paid(order: Any) -> bool:
    flag = find_value(order, "paid", "isPaid", "is_paid")
    if isinstance(flag, bool):
        return flag
    status = find_value(order, "payStatus", "pay_status", "paymentStatus")
    return str(status or "").strip().upper() in PAID_STATUSES


class RestClient:
    def __init__(self, timeout: int = 30, dry_run: bool = False):
        self.timeout = max(int(timeout), 1)
        self.dry_run = dry_run

    def request(
        self,
        method: str,
        url: str,
        *,
        payload: Any = None,
        query: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        raw: bool = False,
    ) -> Any:
        if not url.startswith("https://"):
            raise CnkiError("只允许向 HTTPS 接口或上传地址发请求")
        if query:
            encoded = urllib.parse.urlencode(
                {key: value for key, value in query.items() if value is not None}
            )
            if encoded:
                url += ("&" if "?" in url else "?") + encoded
        request_headers = {
            "Accept": "application/json",
            "User-Agent": "cnki-paper-check-skill/1.0",
        }
        request_headers.update(headers or {})
        if payload is None:
            body = None
        elif isinstance(payload, bytes):
            body = payload
        else:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            request_headers.setdefault("Content-Type", "application/json")
        if self.dry_run:
            return {
                "dry_run": True,
                "method": method.upper(),
                "url": url,
                "body_bytes": len(body or b""),
            }
        request = urllib.request.Request(
            url, data=body, headers=request_headers, method=method.upper()
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                data = response.read(3 * 1024 * 1024 + 1)
                if len(data) > 3 * 1024 * 1024:
                    raise CnkiError("接口响应超过 3 MB，已停止读取")
                if raw:
                    return data
                if not data:
                    return None
                try:
                    return unwrap(json.loads(data.decode("utf-8")))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise CnkiError("接口返回的不是 UTF-8 JSON") from exc
        except urllib.error.HTTPError as exc:
            message = ""
            try:
                error_payload = json.loads(exc.read(1200).decode("utf-8"))
                message = str(
                    error_payload.get("msg") or error_payload.get("message") or ""
                ).strip()
            except (UnicodeDecodeError, json.JSONDecodeError, AttributeError):
                message = ""
            suffix = f": {message}" if message else ""
            raise CnkiError(f"HTTP {exc.code}{suffix}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise CnkiError(f"网络请求失败: {exc}") from exc


def snapshot_config(catalog: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    return {
        "enabled": bool((config.get("runtime_snapshot") or {}).get("enabled", True)),
        "products": catalog.get("products") or [],
        "paymentChannels": (config.get("runtime_snapshot") or {}).get(
            "payment_channels", []
        ),
        "snapshot": True,
        "capturedAt": catalog.get("captured_at"),
    }


def load_live_config(client: RestClient, domain: dict[str, Any]) -> dict[str, Any]:
    data = client.request(
        "GET",
        endpoint(domain, "config"),
        query={"channel": domain["channel"]},
    )
    if not isinstance(data, dict):
        raise CnkiError("实时产品接口没有返回有效配置")
    return data


def safe_products(config_data: dict[str, Any]) -> list[dict[str, Any]]:
    products = config_data.get("products")
    if not isinstance(products, list):
        return []
    safe_keys = {
        "productCode",
        "productName",
        "unit",
        "pricingMode",
        "unitWordCount",
        "fileType",
        "minCount",
        "maxCount",
        "hintMinCount",
        "hintMaxCount",
        "defaultCheckDbs",
        "acceptTimeRequired",
        "salePrice",
        "priceLabel",
    }
    return [
        {key: value for key, value in item.items() if key in safe_keys}
        for item in products
        if isinstance(item, dict) and item.get("productCode")
    ]


def find_product(config_data: dict[str, Any], product_code: str) -> dict[str, Any]:
    for product in safe_products(config_data):
        if str(product.get("productCode") or "").upper() == product_code.upper():
            return product
    raise CnkiError(f"实时产品目录未启用 {product_code}")


def product_extensions(product: dict[str, Any], config: dict[str, Any]) -> set[str]:
    raw = str(product.get("fileType") or "")
    items = {"." + item.strip().lower().lstrip(".") for item in raw.split(",") if item.strip()}
    if items:
        return items
    return {
        str(item).lower()
        for item in (config.get("limits") or {}).get("supported_extensions", [])
    }


def validate_metadata(args: argparse.Namespace, product: dict[str, Any], config: dict[str, Any]) -> None:
    limits = config.get("limits") or {}
    title = (args.title or "").strip()
    author = (args.author or "").strip()
    max_title = int(limits.get("max_title_chars", 255))
    min_author = int(limits.get("min_author_chars", 2))
    max_author = int(limits.get("max_author_chars", 64))
    if not title:
        raise CnkiError("请填写论文题目")
    if len(title) > max_title:
        raise CnkiError(f"论文题目不能超过 {max_title} 个字符")
    if not author:
        raise CnkiError("请填写作者")
    if len(author) < min_author or len(author) > max_author:
        raise CnkiError(f"作者名称需为 {min_author}-{max_author} 个字符")
    if not any(
        "一" <= char <= "鿿" or (char.isascii() and char.isalnum())
        for char in author
    ):
        raise CnkiError("作者名称不能是纯符号")
    accept_time = (args.accept_time or "").strip()
    if as_bool(product.get("acceptTimeRequired")) and not accept_time:
        raise CnkiError(f"{product.get('productName') or '该产品'}必须填写 --accept-time")
    if accept_time:
        try:
            date.fromisoformat(accept_time)
        except ValueError as exc:
            raise CnkiError("--accept-time 必须是 YYYY-MM-DD") from exc


def validate_file(
    path_value: str,
    config: dict[str, Any],
    product: dict[str, Any],
) -> tuple[Path, bytes, str]:
    path = Path(path_value).expanduser()
    if not path.is_file():
        raise CnkiError(f"文件不存在: {path}")
    limits = config.get("limits") or {}
    max_bytes = int(limits.get("max_file_bytes", 50 * 1024 * 1024))
    if path.stat().st_size > max_bytes:
        raise CnkiError(f"文件超过 {max_bytes} 字节上限")
    supported = product_extensions(product, config)
    if path.suffix.lower() not in supported:
        raise CnkiError(
            f"{product.get('productName') or '该产品'}不支持 {path.suffix}；支持: "
            + ", ".join(sorted(supported))
        )
    try:
        content = path.read_bytes()
    except OSError as exc:
        raise CnkiError(f"无法读取文件: {exc}") from exc
    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return path, content, content_type


def upload_with_ticket(
    client: RestClient,
    ticket: dict[str, Any],
    content: bytes,
    content_type: str,
) -> str:
    upload_url = ticket.get("uploadUrl") or ticket.get("upload_url")
    object_key = ticket.get("objectKey") or ticket.get("object_key")
    if not isinstance(upload_url, str) or not upload_url.startswith("https://"):
        raise CnkiError("上传票据没有返回有效 HTTPS uploadUrl")
    if not object_key:
        raise CnkiError("上传票据没有返回 objectKey")
    headers = {
        str(key): str(value) for key, value in (ticket.get("headers") or {}).items()
    }
    headers.setdefault("Content-Type", content_type)
    client.request("PUT", upload_url, payload=content, headers=headers, raw=True)
    return str(object_key)


def has_report(order: Any) -> bool:
    status = str(find_value(order, "status") or "").strip().upper()
    report_value = find_value(
        order,
        "reportUrl",
        "report_url",
        "reportPreviewUrl",
        "reportMobilePreviewUrl",
        "reportNum",
    )
    return status in TERMINAL_STATUSES or report_value not in (None, "")


def choose_browser_url(
    urls: dict[str, str],
    order: Any,
) -> tuple[str | None, str]:
    status = str(find_value(order, "status") or "").strip().upper()
    fail_reason = find_value(order, "failReason", "fail_reason")
    if status in FAILED_STATUSES or fail_reason:
        return urls.get("progress") or urls.get("report"), "订单处理失败，请保留原订单号和失败原因，通过原页面联系客服。"
    if has_report(order):
        return urls.get("report"), "报告已可查看，打开本站报告页下载或在线预览；需要确认来源时再去验真。"
    if is_paid(order) or status in PROCESSING_STATUSES:
        return urls.get("progress"), "打开进度页查询同一订单，等待检测完成；不要重复建单。"
    return urls.get("payment"), "打开支付页，由用户本人选择页面提供的支付方式；支付后继续查询同一订单。"


def result(
    action: str,
    domain: dict[str, Any],
    order: Any,
    *,
    order_no: Any | None = None,
    report_download_url: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = str(
        order_no or find_value(order, "orderNo", "order_no", "bizNo") or ""
    ) or None
    urls = browser_urls(domain, resolved)
    if action == "verify":
        selected = urls.get("verify_funnel")
        next_action = "打开统一入口并选择知网报告类型；报告单编号和验证码由用户本人提交。"
    elif resolved:
        selected, next_action = choose_browser_url(urls, order)
    else:
        selected = urls.get("entry")
        next_action = "打开知网入口查看实时产品；正式提交前先确认论文类型。"
    safe_report_url = (
        report_download_url
        if isinstance(report_download_url, str)
        and report_download_url.startswith("https://")
        else None
    )
    if safe_report_url:
        urls["report_download"] = safe_report_url
    payload: dict[str, Any] = {
        "action": action,
        "order_no": resolved,
        "product_code": find_value(order, "productCode", "product_code"),
        "product_name": find_value(order, "productName", "product_name"),
        "status": find_value(order, "status"),
        "status_label": find_value(order, "statusLabel", "status_label"),
        "pay_status": find_value(order, "payStatus", "pay_status"),
        "pay_status_label": find_value(order, "payStatusLabel", "pay_status_label"),
        "pay_amount": find_value(order, "payAmount", "pay_amount"),
        "word_count": find_value(order, "wordCount", "word_count"),
        "fail_reason": find_value(order, "failReason", "fail_reason"),
        "browser_url": selected,
        "browser_action": "OPEN_BROWSER",
        "browser_urls": urls,
        "report_download_url": safe_report_url,
        "next_action": next_action,
    }
    if extra:
        payload.update(extra)
    return payload


def products_result(
    config_data: dict[str, Any],
    domain: dict[str, Any],
    *,
    source: str,
) -> dict[str, Any]:
    return {
        "action": "products",
        "enabled": config_data.get("enabled") is not False,
        "channel": domain.get("channel"),
        "source": source,
        "captured_at": config_data.get("capturedAt"),
        "payment_channels": config_data.get("paymentChannels") or [],
        "products": safe_products(config_data),
        "browser_url": browser_urls(domain).get("entry"),
        "browser_action": "OPEN_BROWSER",
        "next_action": "按论文层级或 AIGC 字符范围选择一个产品；正式订单金额以页面为准。",
    }


def submit_order(
    client: RestClient,
    config: dict[str, Any],
    domain: dict[str, Any],
    catalog: dict[str, Any],
    args: argparse.Namespace,
) -> dict[str, Any]:
    catalog_data = (
        snapshot_config(catalog, config)
        if client.dry_run
        else load_live_config(client, domain)
    )
    if catalog_data.get("enabled") is False:
        raise CnkiError("知网公共检测当前未启用")
    product_code = normalize_product(args.product_code)
    if not product_code:
        raise CnkiError("请填写 --product-code；未确认论文类型时不要提交")
    product = find_product(catalog_data, product_code)
    validate_metadata(args, product, config)
    path, content, content_type = validate_file(args.file, config, product)

    if client.dry_run:
        return result(
            "submit",
            domain,
            {
                "productCode": product_code,
                "productName": product.get("productName"),
                "status": None,
            },
            extra={
                "dry_run": True,
                "file_name": path.name,
                "file_size": len(content),
                "product_snapshot": product,
            },
        )

    ticket = client.request(
        "POST",
        endpoint(domain, "presign"),
        payload={
            "fileName": path.name,
            "productCode": product_code,
            "channel": domain["channel"],
        },
    )
    if not isinstance(ticket, dict):
        raise CnkiError("上传接口没有返回有效票据")
    object_key = upload_with_ticket(client, ticket, content, content_type)

    create_payload: dict[str, Any] = {
        "title": args.title.strip(),
        "author": args.author.strip(),
        "productCode": product_code,
        "fileName": path.name,
        "objectKey": object_key,
        "contentType": content_type,
        "fileSize": len(content),
        "channel": domain["channel"],
    }
    if args.accept_time:
        create_payload["acceptTime"] = args.accept_time.strip()
    if args.check_dbs:
        create_payload["checkDbs"] = args.check_dbs.strip()

    order = client.request(
        "POST", endpoint(domain, "create"), payload=create_payload
    )
    return result(
        "submit",
        domain,
        order,
        extra={
            "file_name": path.name,
            "file_size": len(content),
            "uploaded": True,
        },
    )


def load_order(client: RestClient, domain: dict[str, Any], order_no: str) -> Any:
    normalized = order_no.strip()
    if not normalized:
        raise CnkiError("订单号不能为空")
    return client.request("GET", endpoint(domain, "order", order_no=normalized))


def query_order(client: RestClient, domain: dict[str, Any], keyword: str) -> dict[str, Any]:
    normalized = keyword.strip()
    if not normalized:
        raise CnkiError("查询关键字不能为空")
    order = client.request(
        "GET",
        endpoint(domain, "order_query"),
        query={"keyword": normalized},
    )
    return result("query", domain, order)


def report_result(
    client: RestClient,
    domain: dict[str, Any],
    order_no: str,
) -> dict[str, Any]:
    order = load_order(client, domain, order_no)
    report_url = None
    if has_report(order):
        try:
            report_data = client.request(
                "GET", endpoint(domain, "report_download_url", order_no=order_no.strip())
            )
            if isinstance(report_data, str):
                report_url = report_data
            else:
                report_url = find_value(
                    report_data,
                    "reportDownloadUrl",
                    "downloadUrl",
                    "reportUrl",
                    "url",
                )
        except CnkiError:
            report_url = None
    output = result(
        "report",
        domain,
        order,
        order_no=order_no,
        report_download_url=report_url,
    )
    status = str(find_value(order, "status") or "").strip().upper()
    failed = status in FAILED_STATUSES or bool(
        find_value(order, "failReason", "fail_reason")
    )
    if has_report(order):
        output["browser_url"] = (
            output["browser_urls"].get("report") or output["browser_url"]
        )
    elif failed:
        return output
    else:
        output["next_action"] = "报告尚未确认完成，请继续查询同一订单；不要重复提交。"
    if has_report(order) and not output["report_download_url"]:
        output["next_action"] = "报告已完成，请在本站报告页点击下载或在线预览；未输出供应商非 HTTPS 地址。"
    return output


def verify_result(domain: dict[str, Any]) -> dict[str, Any]:
    output = result("verify", domain, {})
    output["verification_fields"] = ["报告单类型", "报告单编号", "验证码"]
    output["verification_note"] = "从报告首页 №: 后复制编号；验证码由用户本人识读，验真后核对题目、作者、时间和编号。"
    return output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="知网公共 /pzw 最小订单客户端")
    parser.add_argument("--dry-run", action="store_true", help="只用本地快照校验，不发网络请求")
    parser.add_argument("--timeout", type=int, default=30)
    sub = parser.add_subparsers(dest="command", required=True)

    def runtime_flags(command: argparse.ArgumentParser) -> None:
        command.add_argument("--dry-run", action="store_true", default=argparse.SUPPRESS)
        command.add_argument("--timeout", type=int, default=argparse.SUPPRESS)

    products = sub.add_parser("products", help="读取实时产品、价格、格式和支付方式")
    runtime_flags(products)

    submit = sub.add_parser("submit", help="上传论文并创建公共订单")
    runtime_flags(submit)
    submit.add_argument("--product-code", required=True, help="产品编码或明确的产品名称")
    submit.add_argument("--title", required=True, help="论文题目")
    submit.add_argument("--author", required=True, help="作者姓名")
    submit.add_argument("--file", required=True, help="待检测论文文件")
    submit.add_argument("--accept-time", help="产品要求时填写 YYYY-MM-DD")
    submit.add_argument("--check-dbs", help="页面明确提供时填写比对库值")

    status = sub.add_parser("status", help="查询原订单状态")
    runtime_flags(status)
    status.add_argument("--order-no", required=True)

    query = sub.add_parser("query", help="按订单号、检测卡号或第三方支付单号查询订单")
    runtime_flags(query)
    query.add_argument("--keyword", required=True, help="订单号/检测卡号/淘宝主子订单号/支付单号")

    report = sub.add_parser("report", help="检查报告并返回本站报告页")
    runtime_flags(report)
    report.add_argument("--order-no", required=True)

    verify = sub.add_parser("verify", help="返回统一入口和知网官方验真页")
    runtime_flags(verify)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        config, domain, catalog = load_settings()
        client = RestClient(args.timeout, args.dry_run)
        if args.command == "products":
            config_data = (
                snapshot_config(catalog, config)
                if args.dry_run
                else load_live_config(client, domain)
            )
            output = products_result(
                config_data,
                domain,
                source="snapshot" if args.dry_run else "live",
            )
        elif args.command == "submit":
            output = submit_order(client, config, domain, catalog, args)
        elif args.command == "status":
            order = load_order(client, domain, args.order_no)
            output = result("status", domain, order, order_no=args.order_no)
        elif args.command == "query":
            output = query_order(client, domain, args.keyword)
        elif args.command == "report":
            output = report_result(client, domain, args.order_no)
        elif args.command == "verify":
            output = verify_result(domain)
        else:
            raise CnkiError("未知命令")
        print(json.dumps(output, ensure_ascii=False, indent=2, default=str))
        return 0
    except CnkiError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
