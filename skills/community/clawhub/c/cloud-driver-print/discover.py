from __future__ import annotations

import argparse
import ipaddress
import json
from typing import Any

from printer_store import PrinterRecord, format_printers, save_printer

try:
    from zeroconf import ServiceBrowser, ServiceListener, Zeroconf
except ImportError:  # pragma: no cover - optional dependency
    ServiceBrowser = None
    ServiceListener = object
    Zeroconf = None


SERVICE_TYPES = [
    "_ipp._tcp.local.",
    "_printer._tcp.local.",
    "_pdl-datastream._tcp.local.",
]


class PrinterListener(ServiceListener):
    """接收 zeroconf 回调，并提取打印机候选结果。"""

    def __init__(self) -> None:
        self.results_by_ip: dict[str, dict[str, Any]] = {}

    def add_service(self, zc: Any, service_type: str, name: str) -> None:
        # 读取 mDNS 服务详情，并将其中可解析的 IP 地址提取出来。
        info = zc.get_service_info(service_type, name)
        if not info:
            return
        for raw in info.parsed_addresses():
            try:
                ip = str(ipaddress.ip_address(raw))
            except ValueError:
                continue
            properties = _decode_properties(getattr(info, "properties", {}) or {})
            display_name = _extract_name(name.rstrip("."), properties, ip)
            model = _extract_model(properties)
            candidate = {
                "name": display_name,
                "model": model,
                "ip": ip,
                "name_rank": _name_rank(display_name, ip),
                "model_rank": _model_rank(model),
            }
            current = self.results_by_ip.get(ip)
            if current is None:
                self.results_by_ip[ip] = candidate
                continue
            if candidate["name_rank"] > current["name_rank"]:
                current["name"] = candidate["name"]
                current["name_rank"] = candidate["name_rank"]
            if candidate["model_rank"] > current["model_rank"]:
                current["model"] = candidate["model"]
                current["model_rank"] = candidate["model_rank"]

    def remove_service(self, zc: Any, service_type: str, name: str) -> None:
        return

    def update_service(self, zc: Any, service_type: str, name: str) -> None:
        self.add_service(zc, service_type, name)


def validate_ip(value: str) -> str:
    """校验用户手工输入的 IP 地址是否合法。"""
    return str(ipaddress.ip_address(value))


def _decode_properties(properties: dict[Any, Any]) -> dict[str, str]:
    """将 zeroconf 属性表统一解码为字符串字典。"""
    decoded: dict[str, str] = {}
    for raw_key, raw_value in properties.items():
        key = raw_key.decode("utf-8", errors="ignore") if isinstance(raw_key, bytes) else str(raw_key)
        if isinstance(raw_value, bytes):
            value = raw_value.decode("utf-8", errors="ignore").strip()
        else:
            value = str(raw_value).strip()
        decoded[key.lower()] = value
    return decoded


def _clean_value(value: str) -> str:
    """过滤空值、None 和广播里常见的无效占位值。"""
    cleaned = value.strip().strip("\x00")
    if not cleaned:
        return ""
    if cleaned.lower() in {"none", "null", "unknown", "-"}:
        return ""
    return cleaned


def _normalize_spaces(value: str) -> str:
    """压缩多余空白，统一展示格式。"""
    return " ".join(value.split())


def _strip_version_suffix(value: str) -> str:
    """去掉设备广播里常见的版本尾巴，例如 v1、ver 1。"""
    import re

    return re.sub(r"\s+(?:v(?:er(?:sion)?)?\.?\s*\d+)$", "", value, flags=re.IGNORECASE).strip()


def _looks_generic_name(value: str) -> bool:
    """识别过于泛化的名称，避免拿来作为最终展示名。"""
    lowered = value.lower()
    return lowered in {"printer", "webprinter", "ipp", "airprint"}


def _clean_model_text(value: str) -> str:
    """清洗型号文本，尽量保留设备型号而弱化驱动描述。"""
    import re

    cleaned = _normalize_spaces(_strip_version_suffix(_clean_value(value))).strip("()")
    if not cleaned:
        return ""
    cleaned = re.sub(r"\s+\b(?:PCL6?|PS3?|UFR\s*II|KPDL|ESC/P)\b.*$", "", cleaned, flags=re.IGNORECASE)
    return _normalize_spaces(cleaned)


def _clean_name_text(value: str) -> str:
    """清洗打印机名称，移除泛名、版本尾巴和服务名残片。"""
    import re

    cleaned = _normalize_spaces(_strip_version_suffix(_clean_value(value)))
    cleaned = cleaned.split("._", 1)[0].strip()
    cleaned = re.sub(r"\s*\([0-9A-F:]{8,}\)\s*$", "", cleaned, flags=re.IGNORECASE)
    if _looks_generic_name(cleaned):
        return ""
    return cleaned


def _service_instance_name(service_name: str) -> str:
    """从 zeroconf 服务实例名中提取更适合展示的打印机名称。"""
    short_name = service_name.split("._", 1)[0].strip()
    return _clean_name_text(short_name)


def _extract_model(properties: dict[str, str]) -> str:
    """优先从常见的打印机广播字段中提取型号。"""
    for key in ("usb_mdl", "mdl", "model", "product", "ty"):
        value = _clean_model_text(properties.get(key, ""))
        if value:
            return value
    return ""


def _extract_name(fallback_name: str, properties: dict[str, str], ip: str) -> str:
    """优先使用广播中的友好名称，缺失时退回服务名。"""
    for key in ("note", "name", "printer-name"):
        value = _clean_name_text(properties.get(key, ""))
        if value:
            return value
    model_like_name = _clean_name_text(properties.get("ty", ""))
    if model_like_name and not _looks_generic_name(model_like_name):
        return model_like_name
    return _service_instance_name(fallback_name) or ip


def _name_rank(name: str, ip: str) -> int:
    """给名称来源打分，优先保留更像友好名的结果。"""
    if not name or name == ip:
        return 0
    return 2 if "." not in name and "_" not in name else 1


def _model_rank(model: str) -> int:
    """给型号打分，保留非空结果即可。"""
    return 1 if model else 0


def discover(timeout: int) -> list[dict[str, Any]]:
    """通过 mDNS 在本地网段搜索常见打印服务。"""
    if Zeroconf is None or ServiceBrowser is None:
        raise RuntimeError(
            "mDNS discovery requires the 'zeroconf' package. Install it with: pip install zeroconf"
        )

    import time

    # 订阅几类常见打印服务，等待一小段时间收集广播结果。
    zc = Zeroconf()
    listener = PrinterListener()
    browsers = [ServiceBrowser(zc, service, listener) for service in SERVICE_TYPES]
    try:
        time.sleep(timeout)
        results = [
            {
                "name": item["name"],
                "model": item["model"],
                "ip": item["ip"],
            }
            for item in listener.results_by_ip.values()
        ]
        return sorted(results, key=lambda item: (item["ip"], item["name"], item.get("model", "")))
    finally:
        for browser in browsers:
            browser.cancel()
        zc.close()


def discover_by_ip(ip: str, timeout: int) -> dict[str, Any]:
    """按指定 IP 从发现结果中挑出最匹配的一台打印机。"""
    matches = [item for item in discover(timeout) if item["ip"] == ip]
    if matches:
        return sorted(matches, key=lambda item: (not bool(item.get("name")), not bool(item.get("model"))))[0]
    return {"name": ip, "model": "", "ip": ip}


def save_results(results: list[dict[str, Any]], notes: str = "") -> list[str]:
    """将发现结果批量保存到本地文件，并按 IP 去重更新。"""
    saved_paths: list[str] = []
    for item in results:
        record = PrinterRecord(
            name=item.get("name") or item["ip"],
            ip=item["ip"],
            model=item.get("model", ""),
            # 发现阶段只保存设备基础信息，驱动名称后续由 search_driver.py 回写。
            driver="",
            notes=notes,
        )
        saved_paths.append(str(save_printer(record)))
    return saved_paths


def print_results(results: list[dict[str, Any]]) -> None:
    """将发现结果格式化输出到终端。"""
    if not results:
        print("未发现打印机。")
        return
    for idx, item in enumerate(results, start=1):
        model = item.get("model") or "-"
        print(f"{idx}. {item['name']} | {model} | {item['ip']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="发现打印机并自动保存到本地文件，支持按 IP 定位单台设备。")
    parser.add_argument("--timeout", type=int, default=5, help="mDNS 发现等待时间，单位为秒。")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出发现结果。")
    parser.add_argument("--ip", help="只处理指定 IP 的打印机；脚本会先尝试发现其名称和型号再保存。")
    parser.add_argument("--notes", default="", help="保存到 Markdown 中的补充说明。")
    parser.add_argument("--list", action="store_true", help="列出已经保存到 Markdown 的打印机。")
    args = parser.parse_args()

    if args.list:
        from printer_store import list_printers

        print(format_printers(list_printers()))
        return

    if args.ip:
        ip = validate_ip(args.ip)
        payload = [discover_by_ip(ip, args.timeout)]
    else:
        payload = discover(args.timeout)

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print_results(payload)

    if not payload:
        raise SystemExit("没有可保存的打印机信息。")
    saved_paths = save_results(payload, notes=args.notes)
    if len(saved_paths) == 1:
        print(f"已保存打印机记录: {saved_paths[0]}")
    else:
        print(f"已保存 {len(saved_paths)} 台打印机记录。")


if __name__ == "__main__":
    main()
