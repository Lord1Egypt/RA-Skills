#!/usr/bin/env python3

import hashlib
import json
import os
import sys
import urllib.request
from datetime import datetime
from pathlib import Path


CLASSIFICATION_LABELS = {
    101: "操作系统",
    102: "中间件",
    103: "网络设备",
    104: "应用",
    105: "数据库",
    107: "探测",
    108: "虚拟化",
    109: "链路",
    110: "云平台",
    111: "服务器",
    112: "存储",
    113: "容器",
    114: "物联网",
}

PRIORITY_LABELS = {
    5: "紧急(P5)",
    4: "严重(P4)",
    3: "次要(P3)",
    2: "警告(P2)",
    1: "信息(P1)",
}

ACTIVE_STATUS_LABELS = {
    -1: "未监控",
    0: "正常",
    1: PRIORITY_LABELS[1],
    2: PRIORITY_LABELS[2],
    3: PRIORITY_LABELS[3],
    4: PRIORITY_LABELS[4],
    5: PRIORITY_LABELS[5],
}

POWER_STATUS_LABELS = {
    1: "正常",
    2: "异常",
}

ABNORMAL_ACTIVE_STATUS_VALUES = [1, 5, 4, 3, 2, -1]


def load_env(env_path: Path) -> None:
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'").strip('"'))


def make_sign(data: dict, secret: str) -> str:
    parts = []
    for key in sorted(data):
        if key == "sign":
            continue
        value = data[key]
        if value in ("", None) or isinstance(value, (list, dict)):
            continue
        parts.append(f"{key}{value}")
    return hashlib.sha1(f"{secret}{''.join(parts)}".encode("utf-8")).hexdigest().lower()


def post_json(api_url: str, api_secret: str, route: str, params: dict, timeout: int = 30) -> dict:
    payload = dict(params)
    payload["timestamp"] = int(datetime.now().timestamp())
    payload["sign"] = make_sign(payload, api_secret)
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        api_url.rstrip("/") + route,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def parse_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    return value.lower() in {"1", "true", "yes", "y"}


def first_value(obj: dict, *keys):
    for key in keys:
        if key in obj and obj[key] not in (None, ""):
            return obj[key]
    return None


def extract_rows(payload):
    candidates = [
        payload,
        payload.get("data") if isinstance(payload, dict) else None,
        payload.get("result") if isinstance(payload, dict) else None,
    ]
    for item in candidates:
        if isinstance(item, list):
            return item
        if isinstance(item, dict):
            for key in ("rows", "list", "items", "records", "data"):
                value = item.get(key)
                if isinstance(value, list):
                    return value
    return []


def extract_total(payload, fallback: int) -> int:
    candidates = []
    if isinstance(payload, dict):
        candidates.extend(
            [
                payload.get("total"),
                payload.get("count"),
                first_value(payload.get("data", {}) if isinstance(payload.get("data"), dict) else {}, "total", "count"),
                first_value(payload.get("result", {}) if isinstance(payload.get("result"), dict) else {}, "total", "count"),
            ]
        )
    for value in candidates:
        if isinstance(value, bool):
            continue
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            continue
        if parsed >= 0:
            return parsed
    return fallback


def fetch_all_pages(api_url: str, api_secret: str, route: str, params: dict, page_size: int, label: str):
    clean_params = dict(params)
    clean_params.pop("page", None)
    clean_params.pop("pageSize", None)

    page = 1
    rows = []
    while True:
        page_params = dict(clean_params)
        page_params["page"] = page
        page_params["pageSize"] = page_size
        payload = post_json(api_url, api_secret, route, page_params)
        batch = extract_rows(payload)
        rows.extend(batch)
        total = extract_total(payload, len(rows))
        print(f"[{label}] page {page} fetched {len(batch)} rows, total {len(rows)}/{total}", file=sys.stderr)
        if not batch or len(rows) >= total or (len(batch) < page_size and total <= page * page_size):
            break
        page += 1
        if page > 10000:
            raise RuntimeError(f"{label} 分页异常，超过最大页数限制")
    return rows


def read_json_rows(path_str: str):
    payload = json.loads(Path(path_str).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    return extract_rows(payload)


def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def format_clock(value) -> str:
    if value in (None, ""):
        return ""
    try:
        timestamp = float(value)
    except (TypeError, ValueError):
        return str(value)
    if timestamp > 10_000_000_000:
        timestamp = timestamp / 1000
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def normalize_host(host: dict) -> dict:
    classification = first_value(host, "classification_label", "classificationLabel", "classification_name", "classificationName")
    if classification in (None, ""):
        classification = CLASSIFICATION_LABELS.get(safe_int(first_value(host, "classification")), "")
    active_status = safe_int(first_value(host, "active_status", "activeStatus", "status"), -1)
    power_status = safe_int(first_value(host, "power_status", "powerStatus", "available"), 0)
    monitor_status = first_value(
        host,
        "active_status_label",
        "activeStatusLabel",
        "status_text",
        "statusText",
        "monitor_status_text",
        "monitorStatusText",
    )
    if monitor_status in (None, ""):
        monitor_status = ACTIVE_STATUS_LABELS.get(active_status, str(active_status))
    collect_status = first_value(
        host,
        "power_label",
        "powerLabel",
        "available_text",
        "availableText",
        "collect_status_text",
        "collectStatusText",
    )
    if collect_status in (None, ""):
        collect_status = POWER_STATUS_LABELS.get(power_status, str(power_status) if power_status else "")
    return {
        "hostid": str(first_value(host, "hostid", "id", "hostId") or ""),
        "name": str(first_value(host, "name", "host_name", "hostName", "hostname") or ""),
        "ip": str(first_value(host, "ip", "hostip", "host_ip", "true_ip", "agent_ip") or ""),
        "classification": classification or "",
        "active_status": active_status,
        "active_status_label": str(monitor_status or ""),
        "monitor_status": str(monitor_status or ""),
        "power_status": power_status,
        "power_label": str(collect_status or ""),
        "collect_status": str(collect_status or ""),
        "raw": host,
    }


def normalize_problem(problem: dict) -> dict:
    return {
        "hostid": str(first_value(problem, "hostid", "id", "hostId") or ""),
        "name": str(first_value(problem, "name", "host_name", "hostName", "hostname") or ""),
        "ip": str(first_value(problem, "ip", "hostip", "host_ip", "true_ip") or ""),
        "description": str(first_value(problem, "description", "problem", "event_name", "eventName") or ""),
        "priority": safe_int(first_value(problem, "priority", "level"), 0),
        "clock": format_clock(first_value(problem, "clock", "event_clock", "eventClock", "time")),
        "duration": str(first_value(problem, "clock_time", "duration", "duration_text", "durationText") or ""),
        "think_tank_nums": safe_int(first_value(problem, "think_tank_nums", "thinkTankNums"), 0),
        "suggestion": str(first_value(problem, "suggestion", "ai_suggestion", "advice", "recommendation") or ""),
        "raw": problem,
    }


def dedupe_hosts(hosts: list[dict]) -> list[dict]:
    seen = set()
    result = []
    for host in hosts:
        key = (host["hostid"], host["ip"], host["name"])
        if key in seen:
            continue
        seen.add(key)
        result.append(host)
    return result


def analyze_inventory(host_rows: list[dict], problem_rows: list[dict]) -> dict:
    hosts = dedupe_hosts([normalize_host(item) for item in host_rows])
    problems = [normalize_problem(item) for item in problem_rows]
    problems.sort(key=lambda item: (-item["priority"], item["clock"], item["name"], item["ip"]))
    normal_hosts = [host for host in hosts if host["active_status"] == 0]
    abnormal_hosts = [host for host in hosts if host["active_status"] != 0]

    priority_counts = {level: 0 for level in PRIORITY_LABELS}
    for item in problems:
        if item["priority"] in priority_counts:
            priority_counts[item["priority"]] += 1

    return {
        "hosts": hosts,
        "problems": problems,
        "normal_hosts": normal_hosts,
        "abnormal_hosts": abnormal_hosts,
        "priority_counts": priority_counts,
    }


def build_problem_params(args) -> dict:
    params = {"searchtype": args.searchtype or "history", "status": args.status}
    for attr in ("clock_begin", "clock_end", "ip", "keyword", "priority", "sort_order", "sort_name"):
        value = getattr(args, attr)
        if value not in (None, ""):
            key = attr.replace("_", "")
            if attr in {"sort_order", "sort_name"}:
                key = "sortOrder" if attr == "sort_order" else "sortName"
            params[key] = value
    for attr in ("classification", "subtype", "groupid", "hostid"):
        value = getattr(args, attr)
        if value is not None:
            params[attr] = value
    if args.hostids:
        params["hostids"] = [int(item) for item in args.hostids.split(",") if item.strip()]
    is_ip = parse_bool(args.is_ip)
    if is_ip is not None:
        params["is_ip"] = is_ip
    is_maintenanced = parse_bool(args.is_maintenanced)
    if is_maintenanced is not None:
        params["isMaintenanced"] = is_maintenanced
    is_acked = parse_bool(args.is_acked)
    if is_acked is not None:
        params["isAcked"] = is_acked
    return params


def build_host_params(args) -> dict:
    params = {}
    for attr in ("keyword", "ip", "classification", "subtype"):
        value = getattr(args, attr)
        if value not in (None, ""):
            params[attr] = value
    if args.true_ip is not None:
        params["true_ip"] = args.true_ip
    return params


def build_normal_host_params(args) -> dict:
    params = build_host_params(args)
    params["active_status"] = 0
    return params


def build_abnormal_host_params(args) -> dict:
    params = build_host_params(args)
    for index, value in enumerate(ABNORMAL_ACTIVE_STATUS_VALUES):
        params[f"active_status[{index}]"] = value
    return params
