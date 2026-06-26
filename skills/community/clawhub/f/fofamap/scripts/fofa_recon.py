#!/usr/bin/env python3
"""
Deterministic FOFA helper for the fofamap skill.

Environment:
  Required:
    FOFA_EMAIL
    FOFA_API_KEY
  Optional:
    FOFA_BASE_URL   default: https://fofa.info
    FOFA_TIMEOUT    default: 60

Network access:
  - FOFA API endpoints under FOFA_BASE_URL
  - target hosts when using icon-hash or alive-check

Local files:
  - optional CSV/XLSX exports
  - optional project output directories
  - optional Markdown reports and targets lists
"""

from __future__ import annotations

import argparse
import base64
import csv
import datetime as dt
import json
import os
import re
import shlex
import shutil
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence
from xml.sax.saxutils import escape as xml_escape


SAFE_FIELDS = "host,ip,port,protocol,title,domain,country_name,server"
DEFAULT_STATS_FIELDS = "country,title,org"
DEFAULT_ALIVE_CONCURRENCY = 20
DEFAULT_RESULTS_DIR = "results"

LEVEL0_SEARCH_FIELDS = [
    "ip",
    "port",
    "protocol",
    "base_protocol",
    "host",
    "domain",
    "link",
    "title",
    "server",
    "os",
    "header",
    "banner",
    "icp",
    "jarm",
    "country",
    "country_name",
    "region",
    "city",
    "longitude",
    "latitude",
    "asn",
    "org",
    "cert",
    "cert.domain",
    "cert.sn",
    "cert.issuer.org",
    "cert.issuer.cn",
    "cert.subject.org",
    "cert.subject.cn",
    "tls.ja3s",
    "tls.version",
    "cert.not_before",
    "cert.not_after",
    "status_code",
]

LEVEL11_SEARCH_FIELDS = [
    "header_hash",
    "banner_hash",
    "banner_fid",
]

LEVEL12_SEARCH_FIELDS = [
    "product",
    "product_category",
    "cname",
    "lastupdatetime",
]

LEVEL13_SEARCH_FIELDS = [
    "body",
    "icon_hash",
    "product.version",
    "cert.is_valid",
    "cname_domain",
    "cert.is_match",
    "cert.is_equal",
]

LEVEL5_SEARCH_FIELDS = [
    "icon",
    "fid",
    "structinfo",
]

KNOWN_STATS_FIELDS = [
    "protocol",
    "domain",
    "port",
    "title",
    "os",
    "server",
    "country",
    "asn",
    "org",
    "asset_type",
    "fid",
    "icp",
]

SEARCH_FIELD_PRESETS = {
    "asset_baseline": {
        "description": "basic asset handoff",
        "fields": ["host", "ip", "port", "protocol", "title", "domain", "country_name", "server"],
    },
    "web_delivery": {
        "description": "web-oriented delivery with indexed HTTP metadata",
        "fields": ["host", "link", "ip", "port", "protocol", "status_code", "title", "server"],
    },
    "geo_org": {
        "description": "geography and ownership context",
        "fields": ["country_name", "region", "city", "asn", "org"],
    },
    "banner_hashes": {
        "description": "header or banner hash pivots",
        "fields": ["header_hash", "banner_hash", "banner_fid"],
    },
    "product_stack": {
        "description": "product and stack attribution",
        "fields": ["product", "product_category", "cname", "lastupdatetime"],
    },
    "certificate_review": {
        "description": "certificate identity and issuer review",
        "fields": [
            "cert",
            "cert.domain",
            "cert.sn",
            "cert.subject.cn",
            "cert.subject.org",
            "cert.issuer.cn",
            "cert.issuer.org",
        ],
    },
    "tls_review": {
        "description": "TLS fingerprint and validity window review",
        "fields": ["tls.ja3s", "tls.version", "cert.not_before", "cert.not_after"],
    },
    "body_and_favicon": {
        "description": "web body and favicon pivots",
        "fields": ["body", "icon_hash"],
    },
    "enterprise_binary_pivots": {
        "description": "enterprise binary fingerprint pivots",
        "fields": ["fid", "icon", "structinfo"],
    },
    "deep_validation": {
        "description": "version and certificate validation checks",
        "fields": ["product.version", "cert.is_valid", "cname_domain", "cert.is_match", "cert.is_equal"],
    },
}

FOFA_VIP_METADATA = {
    0: {
        "level_name": "注册用户",
        "query_syntax_scope": "45 query syntaxes",
        "search_export_field_scope": "34 export fields",
        "documented_query_syntax_count": 45,
        "documented_search_export_field_count": 34,
        "can_use_host_api": False,
        "can_use_stats_api": False,
        "api_rps_limit": 1,
    },
    1: {
        "level_name": "普通会员",
        "query_syntax_scope": "same scope as subscription personal",
        "search_export_field_scope": "same scope as subscription personal",
        "documented_query_syntax_count": 57,
        "documented_search_export_field_count": 37,
        "can_use_host_api": True,
        "can_use_stats_api": False,
        "api_rps_limit": 1,
    },
    2: {
        "level_name": "高级会员",
        "query_syntax_scope": "same scope as subscription professional",
        "search_export_field_scope": "same scope as subscription professional",
        "documented_query_syntax_count": 59,
        "documented_search_export_field_count": 41,
        "can_use_host_api": True,
        "can_use_stats_api": True,
        "api_rps_limit": 1,
    },
    5: {
        "level_name": "标准企业版",
        "query_syntax_scope": "all query syntaxes",
        "search_export_field_scope": "all export fields",
        "documented_search_export_field_count": 51,
        "can_use_host_api": True,
        "can_use_stats_api": True,
        "api_rps_limit": 5,
    },
    11: {
        "level_name": "订阅个人版",
        "query_syntax_scope": "57 query syntaxes",
        "search_export_field_scope": "37 export fields",
        "documented_query_syntax_count": 57,
        "documented_search_export_field_count": 37,
        "can_use_host_api": True,
        "can_use_stats_api": False,
        "api_rps_limit": 1,
    },
    12: {
        "level_name": "订阅专业版",
        "query_syntax_scope": "59 query syntaxes",
        "search_export_field_scope": "41 export fields",
        "documented_query_syntax_count": 59,
        "documented_search_export_field_count": 41,
        "can_use_host_api": True,
        "can_use_stats_api": True,
        "api_rps_limit": 1,
    },
    13: {
        "level_name": "订阅商业版",
        "query_syntax_scope": "all query syntaxes",
        "search_export_field_scope": "48 export fields",
        "documented_search_export_field_count": 48,
        "can_use_host_api": True,
        "can_use_stats_api": True,
        "api_rps_limit": 2,
    },
    22: {
        "level_name": "教育账户",
        "query_syntax_scope": "education account scope",
        "search_export_field_scope": "education account scope",
        "can_use_host_api": True,
        "can_use_stats_api": False,
        "api_rps_limit": 1,
        "notes": [
            "FOFA does not expose a full public field matrix for education accounts in the summary table, so this skill stays conservative until the API proves otherwise.",
        ],
    },
}

DATA_LIMIT_KEYS = [
    "web_query",
    "web_data",
    "api_query",
    "api_data",
    "query",
    "data",
]

FIELD_REQUIREMENT_LABELS = {field: "注册用户及以上" for field in LEVEL0_SEARCH_FIELDS}
FIELD_REQUIREMENT_LABELS.update({field: "个人版/普通会员及以上" for field in LEVEL11_SEARCH_FIELDS})
FIELD_REQUIREMENT_LABELS.update({field: "专业版/高级会员及以上" for field in LEVEL12_SEARCH_FIELDS})
FIELD_REQUIREMENT_LABELS.update({field: "商业版及以上" for field in LEVEL13_SEARCH_FIELDS})
FIELD_REQUIREMENT_LABELS.update({field: "标准企业版" for field in LEVEL5_SEARCH_FIELDS})

KNOWN_SEARCH_FIELDS = list(
    dict.fromkeys(
        LEVEL0_SEARCH_FIELDS + LEVEL11_SEARCH_FIELDS + LEVEL12_SEARCH_FIELDS + LEVEL13_SEARCH_FIELDS + LEVEL5_SEARCH_FIELDS
    )
)

HIGH_RISK_PORTS = {
    "22": "SSH exposure can invite password spraying or key abuse.",
    "445": "SMB exposure often deserves urgent validation.",
    "1433": "MSSQL exposure may allow brute force or weak-service review.",
    "1521": "Oracle listener exposure is worth immediate review.",
    "3306": "MySQL exposure should be reviewed for unintended internet reachability.",
    "3389": "RDP exposure is a classic high-risk entry point.",
    "5432": "PostgreSQL exposure often indicates database services on the edge.",
    "6379": "Redis exposure is frequently tied to weak or absent auth.",
    "7001": "WebLogic administrative exposure deserves high attention.",
    "8080": "Alternate web management ports often hide admin panels.",
    "8443": "Alternate HTTPS management ports often hide admin surfaces.",
    "9200": "Elasticsearch exposure can leak operational data.",
    "27017": "MongoDB exposure can indicate poor access control.",
}

NUCLEI_RULES = [
    (["spring", "springboot", "spring boot"], ["spring", "java"], "Spring-related signals detected."),
    (["shiro"], ["shiro", "java"], "Shiro-related signals detected."),
    (["weblogic"], ["weblogic", "java"], "WebLogic indicators detected."),
    (["jboss", "wildfly"], ["jboss", "java"], "JBoss or WildFly indicators detected."),
    (["thinkphp"], ["thinkphp"], "ThinkPHP indicators detected."),
    (["laravel"], ["laravel", "php"], "Laravel indicators detected."),
    (["exchange", "owa", "outlook web app"], ["exchange"], "Exchange or OWA indicators detected."),
    (["seeyon", "致远"], ["oa", "seeyon"], "Seeyon OA indicators detected."),
    (["tongda", "通达"], ["oa", "tongda"], "Tongda OA indicators detected."),
    (["yonyou", "用友"], ["oa", "yonyou"], "Yonyou indicators detected."),
    (["redis"], ["redis"], "Redis indicators detected."),
    (["grafana"], ["grafana"], "Grafana indicators detected."),
    (["jenkins"], ["jenkins"], "Jenkins indicators detected."),
]

REPORT_PROFILE_METADATA = {
    "standard": {
        "label": "standard",
        "focus": "general asset exposure delivery and operator handoff",
        "title_suffix": "Asset Exposure",
    },
    "attack-infrastructure": {
        "label": "attack-infrastructure",
        "focus": "hosting concentration, suspicious tooling, repeat surface, and campaign-style infrastructure patterns",
        "title_suffix": "Attack Infrastructure",
    },
    "abnormal-exposure": {
        "label": "abnormal-exposure",
        "focus": "unexpected management exposure, leak-like artifacts, and unusual internet-facing services",
        "title_suffix": "Abnormal Exposure",
    },
    "takeover-risk": {
        "label": "takeover-risk",
        "focus": "dangling domains, placeholder services, abandoned platforms, and brand-control gaps",
        "title_suffix": "Takeover Risk",
    },
}

REPORT_PROFILE_CHOICES = list(REPORT_PROFILE_METADATA.keys())

CLOUD_PROVIDER_MARKERS = [
    "amazon",
    "aws",
    "alibaba",
    "aliyun",
    "tencent",
    "google",
    "gcp",
    "azure",
    "microsoft",
    "cloudflare",
    "digitalocean",
    "oracle",
    "huawei",
]

ATTACK_INFRA_MARKERS = [
    "cobaltstrike",
    "cobalt strike",
    "beacon",
    "metasploit",
    "sliver",
    "mythic",
    "supershell",
    "v2ray",
    "frp",
    "gost",
    "xray",
    "nps",
    "shadowsocks",
    "teamserver",
    "proxy pool",
]

ABNORMAL_EXPOSURE_MARKERS = [
    "swagger",
    "actuator",
    "jenkins",
    "grafana",
    "dashboard",
    "kibana",
    "elasticsearch",
    "mongodb",
    "redis",
    "listbucketresult",
    "config.txt",
    "algolia_api_key",
    "/api/",
    "/admin",
    "hacked by",
    "miner",
]

TAKEOVER_MARKERS = [
    "github pages",
    "site not found",
    "there isn't a github pages site here",
    "no such app",
    "no such bucket",
    "bucket not found",
    "domain not claimed",
    "placeholder",
    "coming soon",
    "default page",
]

DEFAULT_MEMORY_DIR = "fofamap_memory"

LEARNING_PATTERN_CATALOG = {
    "login_first_for_tier_sensitive_work": {
        "message": "Inspect login and permission_profile before asking FOFA for premium fields or host/stats APIs.",
        "category": "permissions",
    },
    "broaden_query_after_zero_results": {
        "message": "When FOFA returns nothing useful, broaden by signal family instead of only increasing volume.",
        "category": "query_strategy",
    },
    "prefer_alive_check_for_handoff": {
        "message": "Use alive-check before handoff when FOFA inventory is larger than the currently reachable surface.",
        "category": "validation",
    },
    "respect_documented_size_caps": {
        "message": "Respect FOFA's documented body and cert/banner size caps during deep continuous paging.",
        "category": "api_limits",
    },
    "use_search_next_for_deep_harvests": {
        "message": "Prefer search-next for deep or recurring harvests so pagination stays stable and resumable.",
        "category": "collection",
    },
    "review_high_signal_ports_first": {
        "message": "Prioritize high-signal admin, middleware, and database ports before low-signal commodity assets.",
        "category": "triage",
    },
    "use_profile_driven_reports": {
        "message": "Choose a report profile that matches the mission so delivery stays persuasive and operator-ready.",
        "category": "reporting",
    },
    "confirm_takeover_with_dns_and_platform": {
        "message": "Treat takeover hints as leads and confirm DNS plus platform ownership before making the claim.",
        "category": "validation",
    },
    "treat_drift_as_exposure_change": {
        "message": "In monitoring mode, treat new, removed, or changed assets as exposure drift until validated.",
        "category": "monitoring",
    },
    "separate_indexed_evidence_from_live_validation": {
        "message": "Keep FOFA indexed evidence separate from anything that still requires live confirmation.",
        "category": "analysis",
    },
    "capture_failures_as_playbook_updates": {
        "message": "Turn repeated failures into concrete playbook updates instead of repeating the same broken approach.",
        "category": "self_repair",
    },
}


def get_env(name: str, required: bool = True, default: str | None = None) -> str:
    value = os.environ.get(name, default)
    if required and not value:
        raise SystemExit(
            json.dumps(
                {
                    "ok": False,
                    "error": f"missing environment variable: {name}",
                },
                ensure_ascii=False,
            )
        )
    return value or ""


def json_print(payload: Dict[str, Any], exit_code: int = 0) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.stdout.write("\n")
    raise SystemExit(exit_code)


def api_config() -> tuple[str, str, str, int]:
    base_url = get_env("FOFA_BASE_URL", required=False, default="https://fofa.info").rstrip("/")
    email = get_env("FOFA_EMAIL")
    api_key = get_env("FOFA_API_KEY")
    timeout_raw = get_env("FOFA_TIMEOUT", required=False, default="60")
    try:
        timeout = int(timeout_raw)
    except ValueError:
        timeout = 60
    return base_url, email, api_key, timeout


def request_json(path: str, params: Dict[str, Any], retries: int = 3) -> Dict[str, Any]:
    base_url, email, api_key, timeout = api_config()
    merged = {"email": email, "key": api_key}
    merged.update(params)
    url = f"{base_url}{path}?{urllib.parse.urlencode(merged)}"
    headers = {"User-Agent": "fofamap-skill/2.0"}

    for attempt in range(1, retries + 1):
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < retries:
                time.sleep(2)
                continue
            body = exc.read().decode("utf-8", errors="replace")
            return {"error": True, "errmsg": body or f"http error {exc.code}", "status_code": exc.code}
        except urllib.error.URLError as exc:
            if attempt < retries:
                time.sleep(1)
                continue
            return {"error": True, "errmsg": str(exc.reason)}
        except Exception as exc:  # pragma: no cover - defensive
            if attempt < retries:
                time.sleep(1)
                continue
            return {"error": True, "errmsg": str(exc)}

    return {"error": True, "errmsg": "request failed"}


def field_names(fields_str: str) -> List[str]:
    return [part.strip() for part in str(fields_str).split(",") if part.strip()]


def normalize_row(row: Any, expected_count: int) -> List[str]:
    if isinstance(row, (list, tuple)):
        values = list(row)
    else:
        values = [row]
    normalized = ["" if value is None else str(value) for value in values]
    if len(normalized) < expected_count:
        normalized.extend([""] * (expected_count - len(normalized)))
    return normalized[:expected_count]


def build_row_mapping(row: Any, fields_str: str) -> Dict[str, str]:
    names = field_names(fields_str)
    values = normalize_row(row, len(names))
    return {names[index]: values[index] for index in range(len(names))}


def default_scheme_for_port(port: str) -> str:
    return "https" if str(port) in {"443", "8443"} else "http"


def normalize_url(raw: str) -> str:
    if raw.startswith("http://") or raw.startswith("https://"):
        return raw
    return f"http://{raw}"


def slugify(value: str, fallback: str = "fofa_task", limit: int = 40) -> str:
    text = re.sub(r"[^\w\-]+", "_", str(value)).strip("_")
    text = re.sub(r"_+", "_", text)
    text = text[:limit].strip("_")
    return text or fallback


def parse_csv_values(raw: str | None, lower: bool = False) -> List[str]:
    if not raw:
        return []
    values = [part.strip() for part in str(raw).split(",") if part.strip()]
    if lower:
        return [value.lower() for value in values]
    return values


def ordered_unique(values: Iterable[str]) -> List[str]:
    seen: set[str] = set()
    ordered: List[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


def parse_vip_level(user_info: Dict[str, Any]) -> int:
    raw = user_info.get("vip_level", 0)
    try:
        return int(raw)
    except (TypeError, ValueError):
        return 0


def normalize_optional_int(value: Any) -> Any:
    if value in {"", None}:
        return value
    try:
        return int(value)
    except (TypeError, ValueError):
        return value


def normalize_data_limit(data_limit: Any) -> Dict[str, Any]:
    if not isinstance(data_limit, dict):
        return {}
    normalized: Dict[str, Any] = {}
    for key in DATA_LIMIT_KEYS:
        if key in data_limit and data_limit.get(key) is not None:
            normalized[key] = normalize_optional_int(data_limit.get(key))
    return normalized


def allowed_search_fields_for_vip_level(vip_level: int) -> List[str]:
    groups: List[List[str]] = [LEVEL0_SEARCH_FIELDS]

    if vip_level in {1, 11}:
        groups.append(LEVEL11_SEARCH_FIELDS)
    elif vip_level in {2, 12}:
        groups.extend([LEVEL11_SEARCH_FIELDS, LEVEL12_SEARCH_FIELDS])
    elif vip_level == 13:
        groups.extend([LEVEL11_SEARCH_FIELDS, LEVEL12_SEARCH_FIELDS, LEVEL13_SEARCH_FIELDS])
    elif vip_level == 5:
        groups.extend([LEVEL11_SEARCH_FIELDS, LEVEL12_SEARCH_FIELDS, LEVEL13_SEARCH_FIELDS, LEVEL5_SEARCH_FIELDS])
    elif vip_level == 22:
        groups.append([])
    elif vip_level > 13:
        groups.extend([LEVEL11_SEARCH_FIELDS, LEVEL12_SEARCH_FIELDS, LEVEL13_SEARCH_FIELDS])

    return ordered_unique(field for group in groups for field in group)


def recommended_default_search_fields(vip_level: int) -> List[str]:
    defaults = field_names(SAFE_FIELDS)
    if vip_level in {2, 5, 12, 13}:
        defaults.extend(["product", "lastupdatetime"])
    return ordered_unique(defaults)


def resolve_field_presets(allowed_fields: List[str]) -> Dict[str, Dict[str, Any]]:
    allowed_set = set(allowed_fields)
    presets: Dict[str, Dict[str, Any]] = {}
    for name, config in SEARCH_FIELD_PRESETS.items():
        preset_fields = ordered_unique(config.get("fields", []))
        available = [field for field in preset_fields if field in allowed_set]
        missing = [field for field in preset_fields if field not in allowed_set]
        presets[name] = {
            "description": config.get("description", ""),
            "available_fields": available,
            "available_fields_csv": ",".join(available),
            "missing_fields": missing,
        }
    return presets


def build_permission_profile(user_info: Dict[str, Any] | None) -> Dict[str, Any]:
    info = dict(user_info or {})
    vip_level = parse_vip_level(info)
    meta = dict(FOFA_VIP_METADATA.get(vip_level, FOFA_VIP_METADATA[0]))
    allowed_fields = allowed_search_fields_for_vip_level(vip_level)
    default_fields = recommended_default_search_fields(vip_level)
    data_limit = normalize_data_limit(info.get("data_limit"))
    notes = list(meta.get("notes", []))
    documented_field_count = meta.get("documented_search_export_field_count")

    if not info:
        notes.append("The skill could not read /api/v1/info/my, so it is using a conservative registered-user profile.")
    if vip_level == 1:
        notes.append("Level 1 is treated as the same export-field family as subscription personal for field planning.")
    if vip_level == 2:
        notes.append("Level 2 is treated as the same export-field family as subscription professional for field planning.")
    if documented_field_count and documented_field_count != len(allowed_fields):
        notes.append(
            "The locally normalized field catalog does not match the current public FOFA field count, so review the official docs before relying on edge-case fields."
        )

    return {
        "vip_level": vip_level,
        "level_name": meta["level_name"],
        "query_syntax_scope": meta["query_syntax_scope"],
        "documented_query_syntax_count": meta.get("documented_query_syntax_count"),
        "search_export_field_scope": meta["search_export_field_scope"],
        "documented_search_export_field_count": documented_field_count,
        "can_use_host_api": meta["can_use_host_api"],
        "can_use_stats_api": meta["can_use_stats_api"],
        "api_rps_limit": meta["api_rps_limit"],
        "remain_api_query": normalize_optional_int(info.get("remain_api_query")),
        "remain_api_data": normalize_optional_int(info.get("remain_api_data")),
        "data_limit": data_limit,
        "data_limit_keys": list(data_limit.keys()),
        "allowed_search_fields": allowed_fields,
        "allowed_search_fields_csv": ",".join(allowed_fields),
        "allowed_search_field_count": len(allowed_fields),
        "default_search_fields": default_fields,
        "default_search_fields_csv": ",".join(default_fields),
        "safe_fallback_fields_csv": ",".join(default_fields),
        "stats_default_fields": field_names(DEFAULT_STATS_FIELDS),
        "stats_default_fields_csv": DEFAULT_STATS_FIELDS,
        "stats_supported_fields": KNOWN_STATS_FIELDS,
        "stats_supported_fields_csv": ",".join(KNOWN_STATS_FIELDS),
        "field_families": {
            "base": LEVEL0_SEARCH_FIELDS,
            "personal": LEVEL11_SEARCH_FIELDS,
            "professional": LEVEL12_SEARCH_FIELDS,
            "business": LEVEL13_SEARCH_FIELDS,
            "enterprise": LEVEL5_SEARCH_FIELDS,
        },
        "search_field_presets": resolve_field_presets(allowed_fields),
        "notes": notes,
    }


def fetch_account_profile() -> tuple[Dict[str, Any], Dict[str, Any]]:
    user_info = request_json("/api/v1/info/my", {})
    if user_info.get("error"):
        return user_info, build_permission_profile({})
    return user_info, build_permission_profile(user_info)


def resolve_requested_search_fields(
    requested_fields: str | None,
    permission_profile: Dict[str, Any],
) -> Dict[str, Any]:
    requested_list = ordered_unique(
        field_names(requested_fields) if requested_fields else permission_profile.get("default_search_fields", field_names(SAFE_FIELDS))
    )
    allowed_set = set(permission_profile.get("allowed_search_fields", []))
    known_set = set(KNOWN_SEARCH_FIELDS)

    accepted: List[str] = []
    dropped: List[Dict[str, str]] = []
    unclassified: List[str] = []

    for field in requested_list:
        if field in allowed_set:
            accepted.append(field)
            continue
        if field in known_set:
            dropped.append(
                {
                    "field": field,
                    "required_plan": FIELD_REQUIREMENT_LABELS.get(field, "higher FOFA tier"),
                }
            )
            continue
        accepted.append(field)
        unclassified.append(field)

    if not accepted:
        accepted = permission_profile.get("default_search_fields", field_names(SAFE_FIELDS))

    return {
        "requested_fields": requested_list,
        "requested_fields_csv": ",".join(requested_list),
        "resolved_fields": ordered_unique(accepted),
        "resolved_fields_csv": ",".join(ordered_unique(accepted)),
        "dropped_fields": dropped,
        "unclassified_fields": unclassified,
        "used_default_fields": not requested_fields,
    }


def resolve_requested_stats_fields(requested_fields: str | None) -> Dict[str, Any]:
    requested_list = ordered_unique(field_names(requested_fields or DEFAULT_STATS_FIELDS))
    known_set = set(KNOWN_STATS_FIELDS)
    normalized: List[str] = []
    unclassified: List[str] = []

    for field in requested_list:
        normalized.append(field)
        if field not in known_set:
            unclassified.append(field)

    return {
        "requested_fields": requested_list,
        "requested_fields_csv": ",".join(requested_list),
        "resolved_fields": normalized,
        "resolved_fields_csv": ",".join(normalized),
        "unclassified_fields": unclassified,
        "used_default_fields": not requested_fields,
    }


def build_target_from_row(row: Any, fields_str: str) -> str | None:
    mapped = build_row_mapping(row, fields_str)
    host = mapped.get("host") or mapped.get("link") or mapped.get("domain") or mapped.get("ip")
    if not host:
        return None

    if host.startswith("http://") or host.startswith("https://"):
        return host

    protocol = mapped.get("protocol") or mapped.get("base_protocol")
    port = mapped.get("port", "")
    scheme = protocol if protocol in {"http", "https"} else default_scheme_for_port(port)

    parsed = urllib.parse.urlsplit(f"//{host}")
    host_has_port = parsed.port is not None
    netloc = host
    if port and not host_has_port:
        netloc = f"{host}:{port}"
    return f"{scheme}://{netloc}"


def collect_targets(rows: Iterable[Any], fields_str: str) -> List[str]:
    return ordered_unique(
        target
        for target in (build_target_from_row(row, fields_str) for row in rows)
        if target
    )


def candidate_probe_urls(target: str) -> List[str]:
    target = target.strip()
    if not target:
        return []
    if target.startswith("http://") or target.startswith("https://"):
        return [target]
    return [f"https://{target}", f"http://{target}"]


def probe_once(url: str, timeout: int) -> str:
    context = ssl._create_unverified_context()
    headers = {"User-Agent": "fofamap-skill/2.0"}

    last_error = "error"
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(url, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
                return str(response.getcode())
        except urllib.error.HTTPError as exc:
            return str(exc.code)
        except urllib.error.URLError as exc:
            last_error = str(exc.reason)
        except Exception as exc:  # pragma: no cover - defensive
            last_error = str(exc)
    return last_error


def probe_target(target: str, timeout: int) -> Dict[str, str]:
    last_status = "error"
    for url in candidate_probe_urls(target):
        status = probe_once(url, timeout=timeout)
        if status.isdigit():
            return {"target": target, "url": url, "status": status}
        last_status = status
    probe_urls = candidate_probe_urls(target)
    return {"target": target, "url": probe_urls[0] if probe_urls else target, "status": last_status}


def check_targets_alive(targets: List[str], timeout: int, concurrency: int) -> List[Dict[str, str]]:
    if not targets:
        return []
    ordered_targets = ordered_unique(targets)
    results: Dict[str, Dict[str, str]] = {}
    with ThreadPoolExecutor(max_workers=max(1, concurrency)) as executor:
        future_map = {
            executor.submit(probe_target, target, timeout): target
            for target in ordered_targets
        }
        for future in as_completed(future_map):
            result = future.result()
            results[result["target"]] = result
    return [results[target] for target in ordered_targets if target in results]


def is_alive_status(status: str) -> bool:
    return str(status).isdigit()


def load_targets_from_file(path: str) -> List[str]:
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    return [line.strip() for line in lines if line.strip()]


def timestamp_slug() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def resolve_export_format(output: str | None, export_format: str | None) -> str:
    if export_format:
        fmt = export_format.lower().strip(".")
    elif output and Path(output).suffix.lower() in {".csv", ".xlsx"}:
        fmt = Path(output).suffix.lower().lstrip(".")
    else:
        fmt = "xlsx"

    if fmt not in {"csv", "xlsx"}:
        raise ValueError("export format must be csv or xlsx")
    return fmt


def resolve_export_path(output: str | None, export_format: str | None, prefix: str) -> Path:
    fmt = resolve_export_format(output, export_format)
    if output:
        path = Path(output).expanduser()
        if path.suffix.lower() != f".{fmt}":
            path = path.with_suffix(f".{fmt}")
    else:
        path = Path.cwd() / f"{prefix}_{timestamp_slug()}.{fmt}"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def sanitize_sheet_name(name: str) -> str:
    cleaned = re.sub(r"[\[\]:*?/\\]", "_", name).strip()
    cleaned = cleaned[:31] or "Sheet1"
    return cleaned


def make_unique_sheet_names(names: Sequence[str]) -> List[str]:
    used: set[str] = set()
    output: List[str] = []
    for raw in names:
        base = sanitize_sheet_name(raw)
        candidate = base
        counter = 2
        while candidate in used:
            suffix = f"_{counter}"
            candidate = sanitize_sheet_name(f"{base[: 31 - len(suffix)]}{suffix}")
            counter += 1
        used.add(candidate)
        output.append(candidate)
    return output


def write_csv_export(path: Path, headers: List[str], rows: List[List[str]]) -> None:
    with open(path, "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)


def excel_column_name(index: int) -> str:
    result = ""
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result
    return result


def build_sheet_xml(headers: List[str], rows: List[List[str]]) -> str:
    all_rows = [headers] + rows
    xml_rows: List[str] = []
    for row_index, row in enumerate(all_rows, start=1):
        cells: List[str] = []
        for column_index, cell in enumerate(row, start=1):
            ref = f"{excel_column_name(column_index)}{row_index}"
            value = "" if cell is None else str(cell)
            cells.append(
                f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{xml_escape(value)}</t></is></c>'
            )
        xml_rows.append(f'<row r="{row_index}">{"".join(cells)}</row>')

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        "<sheetData>"
        f'{"".join(xml_rows)}'
        "</sheetData>"
        "</worksheet>"
    )


def write_xlsx_workbook(path: Path, sheets: List[Dict[str, Any]]) -> None:
    created = dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    unique_names = make_unique_sheet_names([sheet["name"] for sheet in sheets])

    overrides = [
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
    ]
    workbook_sheet_entries: List[str] = []
    workbook_relationships: List[str] = []

    for index, name in enumerate(unique_names, start=1):
        overrides.append(
            f'<Override PartName="/xl/worksheets/sheet{index}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
        workbook_sheet_entries.append(
            f'<sheet name="{xml_escape(name)}" sheetId="{index}" r:id="rId{index}"/>'
        )
        workbook_relationships.append(
            f'<Relationship Id="rId{index}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{index}.xml"/>'
        )

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        f'{"".join(overrides)}'
        "</Types>"
    )
    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        "</Relationships>"
    )
    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        "<sheets>"
        f'{"".join(workbook_sheet_entries)}'
        "</sheets>"
        "</workbook>"
    )
    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        f'{"".join(workbook_relationships)}'
        "</Relationships>"
    )
    core = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:creator>fofamap</dc:creator>'
        '<cp:lastModifiedBy>fofamap</cp:lastModifiedBy>'
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{created}</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{created}</dcterms:modified>'
        "</cp:coreProperties>"
    )
    app = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        "<Application>fofamap</Application>"
        "</Properties>"
    )

    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", root_rels)
        archive.writestr("xl/workbook.xml", workbook)
        archive.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        archive.writestr("docProps/core.xml", core)
        archive.writestr("docProps/app.xml", app)

        for index, sheet in enumerate(sheets, start=1):
            archive.writestr(
                f"xl/worksheets/sheet{index}.xml",
                build_sheet_xml(sheet["headers"], sheet["rows"]),
            )


def write_export(
    output: str | None,
    export_format: str | None,
    prefix: str,
    headers: List[str],
    rows: List[List[str]],
    sheet_name: str,
) -> str:
    path = resolve_export_path(output, export_format, prefix)
    fmt = path.suffix.lower().lstrip(".")
    if fmt == "csv":
        write_csv_export(path, headers, rows)
    else:
        write_xlsx_workbook(path, [{"name": sheet_name, "headers": headers, "rows": rows}])
    return str(path)


def write_multi_export(
    output: str | None,
    export_format: str | None,
    prefix: str,
    sheets: List[Dict[str, Any]],
    csv_headers: List[str],
    csv_rows: List[List[str]],
) -> str:
    path = resolve_export_path(output, export_format, prefix)
    fmt = path.suffix.lower().lstrip(".")
    if fmt == "csv":
        write_csv_export(path, csv_headers, csv_rows)
    else:
        write_xlsx_workbook(path, sheets)
    return str(path)


def write_text_file(path: Path, content: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return str(path)


def write_json_file(path: Path, payload: Dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def read_json_file(path: Path) -> Dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def append_jsonl_file(path: Path, payload: Dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return str(path)


def read_jsonl_tail(path: Path, limit: int = 10) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    output: List[Dict[str, Any]] = []
    for line in lines[-limit:]:
        try:
            data = json.loads(line)
        except Exception:
            continue
        if isinstance(data, dict):
            output.append(data)
    return output


def env_flag_true(name: str) -> bool:
    return str(os.environ.get(name, "")).strip().lower() in {"1", "true", "yes", "on"}


def learning_enabled() -> bool:
    return not env_flag_true("FOFAMAP_DISABLE_LEARNING")


def resolve_learning_dir(explicit: str | None = None) -> Path:
    if explicit:
        return Path(explicit).expanduser()
    env_value = os.environ.get("FOFAMAP_MEMORY_DIR", "").strip()
    if env_value:
        return Path(env_value).expanduser()
    return Path.cwd() / DEFAULT_RESULTS_DIR / DEFAULT_MEMORY_DIR


def default_semantic_memory() -> Dict[str, Any]:
    return {
        "updated_at": "",
        "totals": {"runs": 0, "success": 0, "failure": 0},
        "mode_counts": {},
        "report_profile_counts": {},
        "pattern_counts": {},
        "mode_pattern_counts": {},
        "issue_counts": {},
        "dropped_field_counts": {},
        "marker_counts": {"attack_infra": 0, "abnormal": 0, "takeover": 0},
        "recent_runs": [],
    }


def load_semantic_memory(path: Path) -> Dict[str, Any]:
    data = read_json_file(path)
    if not isinstance(data, dict):
        return default_semantic_memory()
    base = default_semantic_memory()
    for key, value in data.items():
        base[key] = value
    return base


def increment_counter(counter: Dict[str, Any], key: str, amount: int = 1) -> None:
    if not key:
        return
    counter[key] = int(counter.get(key, 0) or 0) + amount


def top_counter_items(counter: Dict[str, Any], limit: int = 5) -> List[tuple[str, int]]:
    items = [(str(key), int(value or 0)) for key, value in counter.items() if key]
    return sorted(items, key=lambda item: (-item[1], item[0]))[:limit]


def normalize_report_profile_name(profile: Any) -> str:
    if isinstance(profile, dict):
        return normalize_report_profile(profile.get("name"))
    return normalize_report_profile(str(profile or "standard"))


def count_marker_hits(result_objects: List[Dict[str, Any]]) -> Dict[str, int]:
    return {
        "attack_infra": sum(1 for item in result_objects if item_matches_markers(item, ATTACK_INFRA_MARKERS)),
        "abnormal": sum(1 for item in result_objects if item_matches_markers(item, ABNORMAL_EXPOSURE_MARKERS)),
        "takeover": sum(1 for item in result_objects if item_matches_markers(item, TAKEOVER_MARKERS)),
    }


def derive_learning_reflection(
    mode: str,
    payload: Dict[str, Any],
    result_objects: List[Dict[str, Any]] | None = None,
) -> Dict[str, Any]:
    status = "success" if payload.get("ok", True) else "failure"
    objects = list(result_objects or payload.get("result_objects") or [])
    profile_name = normalize_report_profile_name(payload.get("report_profile"))
    issues: List[str] = []
    strengths: List[str] = []
    next_actions: List[str] = []
    pattern_codes: List[str] = ["separate_indexed_evidence_from_live_validation"]

    if profile_name != "standard":
        pattern_codes.append("use_profile_driven_reports")
        strengths.append(f"Report delivery used the `{profile_name}` lens instead of a generic summary.")

    field_resolution = payload.get("field_resolution") or {}
    dropped_fields = [str(item.get("field", "")) for item in (field_resolution.get("dropped_fields") or []) if item.get("field")]
    if dropped_fields:
        pattern_codes.append("login_first_for_tier_sensitive_work")
        issues.append(f"FOFA tier dropped requested fields: {', '.join(dropped_fields[:8])}.")
        next_actions.append("Check permission_profile first and switch to tier-safe fields before repeating the same request.")

    if payload.get("size_limit_reasons"):
        pattern_codes.append("respect_documented_size_caps")
        issues.append("FOFA applied documented size limits because the query touched body or cert/banner-heavy fields.")

    result_count = int(
        payload.get("result_count")
        or payload.get("total_result_count")
        or payload.get("unique_target_count")
        or payload.get("current_count")
        or 0
    )
    if result_count == 0:
        pattern_codes.extend(["broaden_query_after_zero_results", "capture_failures_as_playbook_updates"])
        issues.append("This run produced no useful inventory and should feed back into query broadening.")
        next_actions.append("Broaden by signal family, not just by page count or result volume.")
    elif result_count > 0:
        strengths.append(f"The run produced `{result_count}` usable records for operator analysis.")

    alive_summary = payload.get("alive_summary") or {}
    alive_count = int(alive_summary.get("alive_count", 0) or 0)
    checked_count = int(alive_summary.get("checked_count", 0) or 0)
    if checked_count and alive_count < checked_count:
        pattern_codes.append("prefer_alive_check_for_handoff")
        issues.append(f"Only `{alive_count}` of `{checked_count}` checked web targets responded during live verification.")
        next_actions.append("Prefer alive-check before final handoff when the indexed surface looks noisy or stale.")
    elif alive_count and checked_count:
        strengths.append("Live verification confirmed the checked web targets were still reachable.")

    if mode in {"search-next", "monitor-run"} or payload.get("query_mode") == "search-next":
        pattern_codes.append("use_search_next_for_deep_harvests")
        strengths.append("Cursor-based harvesting preserved stable deep collection semantics.")

    marker_hits = count_marker_hits(objects)
    if any(port in HIGH_RISK_PORTS for port in (item.get("port", "") for item in objects)):
        pattern_codes.append("review_high_signal_ports_first")
        next_actions.append("Review management, middleware, and database ports before lower-signal web noise.")
    if profile_name == "takeover-risk" or marker_hits["takeover"]:
        pattern_codes.append("confirm_takeover_with_dns_and_platform")
        next_actions.append("Confirm DNS, CNAME, and platform ownership before escalating takeover claims.")

    if mode == "monitor-run":
        diff_summary = payload.get("diff_summary") or {}
        if diff_summary.get("baseline_established"):
            strengths.append("The run successfully established a baseline for later comparisons.")
        if any(int(diff_summary.get(key, 0) or 0) > 0 for key in ["added_count", "removed_count", "changed_count"]):
            pattern_codes.append("treat_drift_as_exposure_change")
            next_actions.append("Treat observed drift as exposure change until it is reconciled with change windows and live checks.")

    if mode == "host":
        host_profile = payload.get("host_profile") or {}
        if int(host_profile.get("port_count", 0) or 0) > 0:
            strengths.append("Host profiling recovered concrete per-port exposure details.")
        if int(host_profile.get("port_count", 0) or 0) >= 5:
            pattern_codes.append("review_high_signal_ports_first")

    if mode == "stats":
        stats_summary = payload.get("stats_summary") or {}
        if stats_summary.get("top_summary"):
            strengths.append("Aggregation produced concentration signals that can drive prioritization.")

    error_text = str(
        payload.get("error")
        or payload.get("errmsg")
        or (payload.get("data") or {}).get("errmsg", "")
        or ""
    ).strip()
    if status == "failure":
        pattern_codes.append("capture_failures_as_playbook_updates")
        if error_text:
            issues.append(error_text[:240])
        next_actions.append("Capture this failure as a reusable lesson so the next run avoids the same dead path.")

    pattern_codes = ordered_unique(pattern_codes)
    lessons = [
        LEARNING_PATTERN_CATALOG[code]["message"]
        for code in pattern_codes
        if code in LEARNING_PATTERN_CATALOG
    ]
    summary = (
        f"{mode} completed with {result_count} records and profile `{profile_name}`."
        if status == "success"
        else f"{mode} failed and produced a repairable lesson for the playbook."
    )
    if mode == "monitor-run" and payload.get("diff_summary"):
        diff_summary = payload.get("diff_summary") or {}
        summary = (
            f"{mode} compared snapshots and saw added={diff_summary.get('added_count', 0)}, "
            f"removed={diff_summary.get('removed_count', 0)}, changed={diff_summary.get('changed_count', 0)}."
        )

    return {
        "status": status,
        "summary": summary,
        "pattern_codes": pattern_codes,
        "lessons": lessons,
        "issues": ordered_unique(issues),
        "strengths": ordered_unique(strengths),
        "next_actions": ordered_unique(next_actions),
        "marker_hits": marker_hits,
        "dropped_fields": dropped_fields,
        "result_count": result_count,
        "report_profile": profile_name,
    }


def build_learning_reflection_markdown(event: Dict[str, Any], evolution_hints: List[str]) -> str:
    lines = [
        "# FOFAMAP Learning Reflection",
        "",
        f"- Episode ID: `{event.get('id', '')}`",
        f"- Mode: `{event.get('mode', '')}`",
        f"- Status: `{event.get('status', '')}`",
        f"- Timestamp: `{event.get('timestamp', '')}`",
        f"- Report Profile: `{event.get('report_profile', 'standard')}`",
        f"- Summary: {event.get('summary', '')}",
    ]
    if event.get("strengths"):
        lines.extend(["", "## Strengths", ""])
        for item in event["strengths"]:
            lines.append(f"- {item}")
    if event.get("issues"):
        lines.extend(["", "## Issues", ""])
        for item in event["issues"]:
            lines.append(f"- {item}")
    if event.get("lessons"):
        lines.extend(["", "## Lessons", ""])
        for item in event["lessons"]:
            lines.append(f"- {item}")
    if event.get("next_actions"):
        lines.extend(["", "## Next Actions", ""])
        for item in event["next_actions"]:
            lines.append(f"- {item}")
    if evolution_hints:
        lines.extend(["", "## Evolving Memory Hints", ""])
        for item in evolution_hints:
            lines.append(f"- {item}")
    return "\n".join(lines).strip() + "\n"


def build_learning_review_markdown(
    semantic_memory: Dict[str, Any],
    recent_events: List[Dict[str, Any]],
    learning_dir: Path,
) -> str:
    totals = semantic_memory.get("totals", {}) or {}
    lines = [
        "# FOFAMAP Evolution Review",
        "",
        f"- Learning Directory: `{learning_dir}`",
        f"- Updated: `{semantic_memory.get('updated_at', '')}`",
        f"- Total Runs Learned: `{totals.get('runs', 0)}`",
        f"- Success Runs: `{totals.get('success', 0)}`",
        f"- Failure Runs: `{totals.get('failure', 0)}`",
    ]

    top_patterns = top_counter_items(semantic_memory.get("pattern_counts", {}) or {}, limit=8)
    if top_patterns:
        lines.extend(["", "## Strongest Learned Patterns", ""])
        for code, count in top_patterns:
            message = LEARNING_PATTERN_CATALOG.get(code, {}).get("message", code)
            lines.append(f"- `{count}`x `{code}`: {message}")

    top_issues = top_counter_items(semantic_memory.get("issue_counts", {}) or {}, limit=6)
    if top_issues:
        lines.extend(["", "## Recurrent Friction", ""])
        for issue, count in top_issues:
            lines.append(f"- `{count}`x {issue}")

    dropped_fields = top_counter_items(semantic_memory.get("dropped_field_counts", {}) or {}, limit=8)
    if dropped_fields:
        lines.extend(["", "## Frequently Rejected Fields", ""])
        for field, count in dropped_fields:
            lines.append(f"- `{field}` dropped `{count}` times")

    profile_counts = top_counter_items(semantic_memory.get("report_profile_counts", {}) or {}, limit=6)
    if profile_counts:
        lines.extend(["", "## Report Lens Usage", ""])
        for profile, count in profile_counts:
            lines.append(f"- `{profile}` used `{count}` times")

    marker_counts = semantic_memory.get("marker_counts", {}) or {}
    lines.extend(
        [
            "",
            "## Marker Exposure",
            "",
            f"- Attack Infrastructure Signals Seen: `{marker_counts.get('attack_infra', 0)}`",
            f"- Abnormal Exposure Signals Seen: `{marker_counts.get('abnormal', 0)}`",
            f"- Takeover Signals Seen: `{marker_counts.get('takeover', 0)}`",
        ]
    )

    if recent_events:
        lines.extend(["", "## Recent Episodes", ""])
        for event in recent_events[-5:]:
            lines.append(f"- `{event.get('mode', '')}` `{event.get('status', '')}`: {event.get('summary', '')}")

    lines.extend(["", "## Operator Guidance", ""])
    lines.append("- Let the skill learn operational patterns and report structure, but keep actual code changes under explicit operator review.")
    lines.append("- Reuse the top learned patterns as default guidance for the next FOFA task in the same environment.")
    return "\n".join(lines).strip() + "\n"


def record_learning_event(
    mode: str,
    payload: Dict[str, Any],
    result_objects: List[Dict[str, Any]] | None = None,
    memory_dir: str | None = None,
) -> Dict[str, Any] | None:
    if not learning_enabled():
        return None

    learning_dir = resolve_learning_dir(memory_dir)
    runs_path = learning_dir / "runs.jsonl"
    semantic_path = learning_dir / "semantic-patterns.json"
    latest_reflection_json = learning_dir / "latest_reflection.json"
    latest_reflection_md = learning_dir / "latest_reflection.md"

    timestamp = dt.datetime.now().isoformat()
    reflection = derive_learning_reflection(mode, payload, result_objects=result_objects)
    event = {
        "id": f"ep-{timestamp_slug()}",
        "timestamp": timestamp,
        "mode": mode,
        "status": reflection["status"],
        "summary": reflection["summary"],
        "report_profile": reflection["report_profile"],
        "pattern_codes": reflection["pattern_codes"],
        "lessons": reflection["lessons"],
        "issues": reflection["issues"],
        "strengths": reflection["strengths"],
        "next_actions": reflection["next_actions"],
        "marker_hits": reflection["marker_hits"],
        "dropped_fields": reflection["dropped_fields"],
        "result_count": reflection["result_count"],
        "query": payload.get("query"),
        "target": payload.get("target"),
        "project_dir": payload.get("project_dir"),
        "state_dir": payload.get("state_dir"),
    }

    append_jsonl_file(runs_path, event)
    semantic_memory = load_semantic_memory(semantic_path)
    semantic_memory["updated_at"] = timestamp
    semantic_memory["totals"]["runs"] = int(semantic_memory["totals"].get("runs", 0) or 0) + 1
    semantic_memory["totals"][event["status"]] = int(semantic_memory["totals"].get(event["status"], 0) or 0) + 1
    increment_counter(semantic_memory.setdefault("mode_counts", {}), mode)
    increment_counter(semantic_memory.setdefault("report_profile_counts", {}), event["report_profile"])
    for code in event["pattern_codes"]:
        increment_counter(semantic_memory.setdefault("pattern_counts", {}), code)
        mode_pattern_counts = semantic_memory.setdefault("mode_pattern_counts", {}).setdefault(mode, {})
        increment_counter(mode_pattern_counts, code)
    for issue in event["issues"]:
        increment_counter(semantic_memory.setdefault("issue_counts", {}), issue)
    for field in event["dropped_fields"]:
        increment_counter(semantic_memory.setdefault("dropped_field_counts", {}), field)
    for key, value in event["marker_hits"].items():
        semantic_memory.setdefault("marker_counts", {})
        semantic_memory["marker_counts"][key] = int(semantic_memory["marker_counts"].get(key, 0) or 0) + int(value or 0)

    recent_runs = semantic_memory.setdefault("recent_runs", [])
    recent_runs.append(
        {
            "timestamp": timestamp,
            "mode": mode,
            "status": event["status"],
            "summary": event["summary"],
        }
    )
    semantic_memory["recent_runs"] = recent_runs[-20:]
    write_json_file(semantic_path, semantic_memory)

    top_mode_patterns = top_counter_items((semantic_memory.get("mode_pattern_counts", {}) or {}).get(mode, {}), limit=3)
    evolution_hints = [
        LEARNING_PATTERN_CATALOG.get(code, {}).get("message", code)
        for code, _ in top_mode_patterns
    ]
    write_json_file(latest_reflection_json, event)
    write_text_file(latest_reflection_md, build_learning_reflection_markdown(event, evolution_hints))

    return {
        "learning_dir": str(learning_dir),
        "runs_file": str(runs_path),
        "semantic_memory_file": str(semantic_path),
        "latest_reflection_json": str(latest_reflection_json),
        "latest_reflection_markdown": str(latest_reflection_md),
        "evolution_hints": evolution_hints,
    }


def results_to_objects(
    rows: List[Any],
    fields_str: str,
    alive_by_target: Dict[str, str] | None = None,
) -> List[Dict[str, str]]:
    names = field_names(fields_str)
    objects: List[Dict[str, str]] = []
    for row in rows:
        mapped = build_row_mapping(row, fields_str)
        target = build_target_from_row(row, fields_str)
        if target:
            mapped["target"] = target
        if alive_by_target is not None and target:
            mapped["http_status"] = alive_by_target.get(target, "")
        objects.append(mapped)
    return objects


def object_text_blob(item: Dict[str, Any]) -> str:
    return " ".join(str(value) for value in item.values() if value).lower()


def matches_keywords(item: Dict[str, Any], keywords: List[str]) -> bool:
    if not keywords:
        return True
    blob = object_text_blob(item)
    return any(keyword in blob for keyword in keywords)


def apply_result_filters(
    rows: List[Any],
    fields_str: str,
    alive_by_target: Dict[str, str] | None = None,
    keyword: str | None = None,
    include_status: str | None = None,
    only_alive: bool = False,
) -> tuple[List[List[str]], List[Dict[str, str]]]:
    keywords = parse_csv_values(keyword, lower=True)
    allowed_status = set(parse_csv_values(include_status))
    filtered_rows: List[List[str]] = []
    filtered_objects: List[Dict[str, str]] = []
    expected_count = len(field_names(fields_str))

    for row in rows:
        normalized = normalize_row(row, expected_count)
        item = build_row_mapping(normalized, fields_str)
        target = build_target_from_row(normalized, fields_str)
        if target:
            item["target"] = target
        status = alive_by_target.get(target, "") if alive_by_target and target else ""
        if alive_by_target is not None and target:
            item["http_status"] = status
        if not matches_keywords(item, keywords):
            continue
        if only_alive and not is_alive_status(status):
            continue
        if allowed_status and status not in allowed_status:
            continue
        filtered_rows.append(normalized)
        filtered_objects.append(item)

    return filtered_rows, filtered_objects


def search_page(
    query: str,
    requested_fields: str,
    fallback_fields: str,
    page: int,
    size: int,
    full: bool,
) -> Dict[str, Any]:
    query_b64 = base64.b64encode(query.encode("utf-8")).decode("ascii")
    params = {
        "qbase64": query_b64,
        "fields": requested_fields,
        "page": page,
        "size": size,
        "full": str(full).lower(),
    }
    data = request_json("/api/v1/search/all", params)
    used_fields = requested_fields
    error_text = str(data.get("errmsg", ""))
    permission_error = data.get("error") and ("820001" in error_text or "权限" in error_text)
    fallback_triggered = False
    if permission_error and requested_fields != fallback_fields:
        params["fields"] = fallback_fields
        used_fields = fallback_fields
        fallback_triggered = True
        data = request_json("/api/v1/search/all", params)

    ok = not data.get("error")
    return {
        "ok": ok,
        "query": query,
        "page": page,
        "requested_fields": requested_fields,
        "used_fields": used_fields,
        "fallback_triggered": fallback_triggered,
        "data": data,
    }


def search_next_page(
    query: str,
    requested_fields: str,
    fallback_fields: str,
    size: int,
    full: bool,
    next_cursor: str,
) -> Dict[str, Any]:
    query_b64 = base64.b64encode(query.encode("utf-8")).decode("ascii")
    effective_next_cursor = "" if str(next_cursor).strip().lower() in {"", "auto", "id", "first"} else str(next_cursor).strip()
    params = {
        "qbase64": query_b64,
        "fields": requested_fields,
        "size": size,
        "full": str(full).lower(),
    }
    if effective_next_cursor:
        params["next"] = effective_next_cursor
    data = request_json("/api/v1/search/next", params)
    used_fields = requested_fields
    error_text = str(data.get("errmsg", ""))
    permission_error = data.get("error") and ("820001" in error_text or "权限" in error_text)
    fallback_triggered = False
    if permission_error and requested_fields != fallback_fields:
        params["fields"] = fallback_fields
        used_fields = fallback_fields
        fallback_triggered = True
        data = request_json("/api/v1/search/next", params)

    ok = not data.get("error")
    return {
        "ok": ok,
        "query": query,
        "requested_fields": requested_fields,
        "used_fields": used_fields,
        "fallback_triggered": fallback_triggered,
        "requested_next_cursor": next_cursor,
        "effective_next_cursor": effective_next_cursor or None,
        "data": data,
    }


def search_query_workflow(
    query: str,
    requested_fields: str,
    permission_profile: Dict[str, Any] | None,
    pages: int,
    size: int,
    full: bool,
    alive_check: bool = False,
    alive_timeout: int = 5,
    alive_concurrency: int = DEFAULT_ALIVE_CONCURRENCY,
    keyword: str | None = None,
    include_status: str | None = None,
    only_alive: bool = False,
) -> Dict[str, Any]:
    raw_results: List[List[str]] = []
    last_data: Dict[str, Any] | None = None
    profile = permission_profile or build_permission_profile({})
    field_resolution = resolve_requested_search_fields(requested_fields, profile)
    used_fields = field_resolution["resolved_fields_csv"]
    fallback_fields = profile.get("safe_fallback_fields_csv", SAFE_FIELDS)
    api_permission_fallback = False

    for page in range(1, max(1, pages) + 1):
        page_payload = search_page(query, used_fields, fallback_fields, page, size, full)
        if not page_payload["ok"]:
            return {
                "ok": False,
                "mode": "search",
                "query": query,
                "requested_fields": requested_fields,
                "field_resolution": field_resolution,
                "permission_profile": profile,
                "used_fields": page_payload["used_fields"],
                "page": page,
                "size": size,
                "full": full,
                "data": page_payload["data"],
            }
        used_fields = page_payload["used_fields"]
        if page_payload["fallback_triggered"]:
            api_permission_fallback = True
        data = page_payload["data"]
        last_data = data
        page_results = data.get("results", []) or []
        if not page_results:
            break
        for item in page_results:
            raw_results.append(normalize_row(item, len(field_names(used_fields))))

    targets = collect_targets(raw_results, used_fields)
    alive_entries: List[Dict[str, str]] = []
    alive_by_target: Dict[str, str] | None = None
    if alive_check and targets:
        alive_entries = check_targets_alive(targets, timeout=alive_timeout, concurrency=alive_concurrency)
        alive_by_target = {entry["target"]: entry["status"] for entry in alive_entries}

    filtered_rows, filtered_objects = apply_result_filters(
        rows=raw_results,
        fields_str=used_fields,
        alive_by_target=alive_by_target,
        keyword=keyword,
        include_status=include_status,
        only_alive=only_alive,
    )

    alive_summary = None
    if alive_check:
        alive_count = sum(1 for entry in alive_entries if is_alive_status(entry["status"]))
        alive_summary = {
            "alive_count": alive_count,
            "checked_count": len(alive_entries),
            "requested_count": len(targets),
        }

    filtered_data = dict(last_data or {})
    filtered_data["results"] = filtered_rows

    return {
        "ok": True,
        "mode": "search",
        "query": query,
        "requested_fields": requested_fields,
        "field_resolution": field_resolution,
        "permission_profile": profile,
        "used_fields": used_fields,
        "api_permission_fallback": api_permission_fallback,
        "pages": pages,
        "size": size,
        "full": full,
        "raw_result_count": len(raw_results),
        "result_count": len(filtered_rows),
        "target_count": len(ordered_unique(item.get("target", "") for item in filtered_objects if item.get("target"))),
        "alive_summary": alive_summary,
        "alive_results": alive_entries,
        "data": filtered_data,
        "result_objects": filtered_objects,
    }


def normalize_search_next_size(query: str, size: int) -> Dict[str, Any]:
    requested_size = max(1, int(size))
    effective_size = requested_size
    reasons: List[str] = []
    query_blob = query.lower()

    if "body" in query_blob and effective_size > 500:
        effective_size = 500
        reasons.append("FOFA limits /api/v1/search/next to 500 rows when the query contains body clauses.")
    if ("cert" in query_blob or "banner" in query_blob) and effective_size > 2000:
        effective_size = min(effective_size, 2000)
        reasons.append("FOFA limits /api/v1/search/next to 2000 rows when the query contains cert or banner clauses.")

    return {
        "requested_size": requested_size,
        "effective_size": effective_size,
        "size_limited": effective_size != requested_size,
        "size_limit_reasons": reasons,
    }


def search_next_workflow(
    query: str,
    requested_fields: str,
    permission_profile: Dict[str, Any] | None,
    size: int,
    full: bool,
    next_cursor: str,
    max_pages: int,
    max_results: int | None,
    alive_check: bool = False,
    alive_timeout: int = 5,
    alive_concurrency: int = DEFAULT_ALIVE_CONCURRENCY,
    keyword: str | None = None,
    include_status: str | None = None,
    only_alive: bool = False,
) -> Dict[str, Any]:
    raw_results: List[List[str]] = []
    last_data: Dict[str, Any] | None = None
    profile = permission_profile or build_permission_profile({})
    field_resolution = resolve_requested_search_fields(requested_fields, profile)
    used_fields = field_resolution["resolved_fields_csv"]
    fallback_fields = profile.get("safe_fallback_fields_csv", SAFE_FIELDS)
    api_permission_fallback = False
    requested_next_cursor = (next_cursor or "").strip() or "auto"
    cursor = requested_next_cursor
    pages_fetched = 0
    reached_result_cap = False
    cursor_trace: List[Dict[str, Any]] = []
    size_meta = normalize_search_next_size(query, size)
    effective_size = size_meta["effective_size"]

    for cursor_page in range(1, max(1, max_pages) + 1):
        page_payload = search_next_page(
            query=query,
            requested_fields=used_fields,
            fallback_fields=fallback_fields,
            size=effective_size,
            full=full,
            next_cursor=cursor,
        )
        if not page_payload["ok"]:
            return {
                "ok": False,
                "mode": "search-next",
                "query": query,
                "requested_fields": requested_fields,
                "field_resolution": field_resolution,
                "permission_profile": profile,
                "used_fields": page_payload["used_fields"],
                "requested_next_cursor": requested_next_cursor,
                "effective_initial_next_cursor": None
                if requested_next_cursor.lower() in {"auto", "id", "first"}
                else requested_next_cursor,
                "failed_next_cursor": cursor,
                "cursor_page": cursor_page,
                "max_pages": max_pages,
                "max_results": max_results,
                "requested_size": size_meta["requested_size"],
                "effective_size": effective_size,
                "size_limited": size_meta["size_limited"],
                "size_limit_reasons": size_meta["size_limit_reasons"],
                "full": full,
                "cursor_trace": cursor_trace,
                "data": page_payload["data"],
            }

        pages_fetched += 1
        used_fields = page_payload["used_fields"]
        if page_payload["fallback_triggered"]:
            api_permission_fallback = True
        data = page_payload["data"]
        last_data = data
        page_results = data.get("results", []) or []
        returned_next_cursor = data.get("next")
        cursor_trace.append(
            {
                "cursor_page": cursor_page,
                "requested_next_cursor": cursor,
                "effective_next_cursor": page_payload.get("effective_next_cursor"),
                "returned_next_cursor": returned_next_cursor,
                "response_page": data.get("page"),
                "result_count": len(page_results),
            }
        )

        for item in page_results:
            raw_results.append(normalize_row(item, len(field_names(used_fields))))
            if max_results and max_results > 0 and len(raw_results) >= max_results:
                reached_result_cap = True
                break

        if reached_result_cap:
            raw_results = raw_results[:max_results]
            break
        if not page_results or not returned_next_cursor:
            break
        cursor = str(returned_next_cursor)

    targets = collect_targets(raw_results, used_fields)
    alive_entries: List[Dict[str, str]] = []
    alive_by_target: Dict[str, str] | None = None
    if alive_check and targets:
        alive_entries = check_targets_alive(targets, timeout=alive_timeout, concurrency=alive_concurrency)
        alive_by_target = {entry["target"]: entry["status"] for entry in alive_entries}

    filtered_rows, filtered_objects = apply_result_filters(
        rows=raw_results,
        fields_str=used_fields,
        alive_by_target=alive_by_target,
        keyword=keyword,
        include_status=include_status,
        only_alive=only_alive,
    )

    alive_summary = None
    if alive_check:
        alive_count = sum(1 for entry in alive_entries if is_alive_status(entry["status"]))
        alive_summary = {
            "alive_count": alive_count,
            "checked_count": len(alive_entries),
            "requested_count": len(targets),
        }

    filtered_data = dict(last_data or {})
    filtered_data["results"] = filtered_rows
    next_cursor_to_resume = filtered_data.get("next")

    return {
        "ok": True,
        "mode": "search-next",
        "query": query,
        "requested_fields": requested_fields,
        "field_resolution": field_resolution,
        "permission_profile": profile,
        "used_fields": used_fields,
        "api_permission_fallback": api_permission_fallback,
        "requested_next_cursor": requested_next_cursor,
        "effective_initial_next_cursor": None
        if requested_next_cursor.lower() in {"auto", "id", "first"}
        else requested_next_cursor,
        "next_cursor_to_resume": next_cursor_to_resume,
        "has_more": bool(next_cursor_to_resume),
        "pages_fetched": pages_fetched,
        "max_pages": max_pages,
        "max_results": max_results,
        "requested_size": size_meta["requested_size"],
        "effective_size": effective_size,
        "size_limited": size_meta["size_limited"],
        "size_limit_reasons": size_meta["size_limit_reasons"],
        "full": full,
        "raw_result_count": len(raw_results),
        "result_count": len(filtered_rows),
        "target_count": len(ordered_unique(item.get("target", "") for item in filtered_objects if item.get("target"))),
        "alive_summary": alive_summary,
        "alive_results": alive_entries,
        "cursor_trace": cursor_trace,
        "reached_result_cap": reached_result_cap,
        "data": filtered_data,
        "result_objects": filtered_objects,
    }


def port_int(port: str) -> int:
    try:
        return int(str(port))
    except Exception:
        return -1


def top_counts(values: Iterable[str], limit: int = 5) -> List[tuple[str, int]]:
    counter = Counter(value for value in values if value)
    return counter.most_common(limit)


def unique_nonempty(values: Iterable[str]) -> List[str]:
    return ordered_unique(value for value in values if value)


def detect_nuclei_suggestion(result_objects: List[Dict[str, str]], user_intent: str = "") -> Dict[str, Any]:
    text_blob = " ".join(object_text_blob(item) for item in result_objects).lower()
    intent_blob = user_intent.lower()

    tags: List[str] = []
    reasons: List[str] = []
    for keywords, rule_tags, reason in NUCLEI_RULES:
        if any(keyword in text_blob or keyword in intent_blob for keyword in keywords):
            for tag in rule_tags:
                if tag not in tags:
                    tags.append(tag)
            if reason not in reasons:
                reasons.append(reason)

    cve_ids: List[str] = []
    if "log4j" in intent_blob or "cve-2021-44228" in intent_blob:
        if "log4j" not in tags:
            tags.append("log4j")
        cve_ids.append("CVE-2021-44228")
        reasons.append("User intent explicitly mentions Log4Shell or CVE-2021-44228.")

    target_count = len(unique_nonempty(item.get("target", "") for item in result_objects))
    if target_count <= 25:
        severity = "critical,high"
        perf_args = ["-bs", "25", "-rl", "150"]
    elif target_count <= 100:
        severity = "critical,high,medium"
        perf_args = ["-bs", "50", "-rl", "100"]
    else:
        severity = "critical,high,medium"
        perf_args = ["-rl", "50"]

    broad_mode = not tags or target_count > 100
    if not tags:
        tags = ["cves", "misconfig"]
        reasons.append("No strong framework signature detected, so broad CVE and misconfiguration coverage is suggested.")

    parts = ["nuclei", "-l", "targets.txt", "-stats", "-severity", severity]
    if broad_mode:
        parts.append("-as")
    if cve_ids:
        parts.extend(["-id", ",".join(cve_ids)])
    if tags:
        parts.extend(["-tags", ",".join(ordered_unique(tags))])
    parts.extend(perf_args)

    return {
        "target_count": target_count,
        "severity": severity,
        "tags": ordered_unique(tags),
        "cve_ids": cve_ids,
        "broad_mode": broad_mode,
        "reasons": ordered_unique(reasons),
        "args": " ".join(parts[3:]),
        "command": " ".join(parts),
    }


def markdown_table(headers: List[str], rows: List[List[str]]) -> str:
    if not rows:
        return ""
    clean_headers = [str(header).replace("|", "\\|") for header in headers]
    out = ["| " + " | ".join(clean_headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        clean_row = [str(value).replace("|", "\\|").replace("\n", " ") for value in row]
        out.append("| " + " | ".join(clean_row) + " |")
    return "\n".join(out)


def normalize_report_profile(profile: str | None) -> str:
    normalized = str(profile or "").strip().lower().replace("_", "-")
    if normalized in REPORT_PROFILE_METADATA:
        return normalized
    return "standard"


def resolve_report_profile(
    requested_profile: str | None = None,
    user_intent: str = "",
    context_hint: str = "",
) -> Dict[str, str]:
    if requested_profile:
        profile = normalize_report_profile(requested_profile)
        reason = "explicit report profile requested"
    else:
        blob = f"{user_intent} {context_hint}".lower()
        if any(
            term in blob
            for term in [
                "takeover",
                "dangling",
                "github pages",
                "bucket",
                "subdomain takeover",
                "接管",
                "废弃",
                "失效",
            ]
        ):
            profile = "takeover-risk"
            reason = "intent hints at dangling assets, abandoned platforms, or brand-control review"
        elif any(
            term in blob
            for term in [
                "attack infrastructure",
                "adversary",
                "campaign",
                "cobalt",
                "metasploit",
                "honeypot",
                "蜜罐",
                "红队",
                "teamserver",
            ]
        ):
            profile = "attack-infrastructure"
            reason = "intent hints at campaign or offensive infrastructure tracking"
        elif any(
            term in blob
            for term in [
                "abnormal",
                "exposure",
                "leak",
                "misconfig",
                "unauthorized",
                "异常",
                "暴露",
                "泄露",
                "未授权",
                "存储桶",
                "bucket",
                "api",
            ]
        ):
            profile = "abnormal-exposure"
            reason = "intent hints at odd exposure, leakage, or misconfiguration review"
        else:
            profile = "standard"
            reason = "default general-purpose exposure reporting"

    meta = REPORT_PROFILE_METADATA[profile]
    return {
        "name": profile,
        "label": meta["label"],
        "focus": meta["focus"],
        "title_suffix": meta["title_suffix"],
        "reason": reason,
    }


def item_matches_markers(item: Dict[str, Any], markers: Sequence[str]) -> bool:
    blob = object_text_blob(item)
    return any(marker in blob for marker in markers)


def collect_profile_samples(
    report_profile: str,
    result_objects: List[Dict[str, str]],
    limit: int = 8,
) -> List[Dict[str, str]]:
    samples: List[Dict[str, str]] = []
    for item in result_objects:
        org_blob = f"{item.get('org', '')} {item.get('asn', '')}".lower()
        port = item.get("port", "")
        matched = False
        if report_profile == "attack-infrastructure":
            matched = item_matches_markers(item, ATTACK_INFRA_MARKERS) or (
                port in HIGH_RISK_PORTS and any(marker in org_blob for marker in CLOUD_PROVIDER_MARKERS)
            )
        elif report_profile == "abnormal-exposure":
            matched = item_matches_markers(item, ABNORMAL_EXPOSURE_MARKERS) or port in HIGH_RISK_PORTS
        elif report_profile == "takeover-risk":
            matched = item_matches_markers(item, TAKEOVER_MARKERS)
        if matched:
            samples.append(item)

    if len(samples) >= limit or report_profile == "standard":
        return samples[:limit]

    fallback_samples: List[Dict[str, str]] = []
    for item in result_objects:
        port = item.get("port", "")
        if report_profile == "attack-infrastructure" and port in HIGH_RISK_PORTS:
            fallback_samples.append(item)
        elif report_profile == "abnormal-exposure" and item.get("http_status") in {"200", "401", "403"}:
            fallback_samples.append(item)
        elif report_profile == "takeover-risk" and item.get("server"):
            fallback_samples.append(item)

    seen: set[str] = set()
    ordered: List[Dict[str, str]] = []
    for item in samples + fallback_samples:
        key = item.get("target") or item.get("host") or f"{item.get('ip', '')}:{item.get('port', '')}"
        if key and key not in seen:
            seen.add(key)
            ordered.append(item)
    return ordered[:limit]


def report_profile_action_lines(report_profile: str) -> List[str]:
    if report_profile == "attack-infrastructure":
        return [
            "Cluster repeated assets by ASN, org, title, and certificate to separate one-off noise from managed infrastructure.",
            "Prioritize cloud-hosted assets that combine suspicious tooling strings with management or database ports.",
            "Treat indexed evidence as a hunt lead and confirm reachability, ownership, and role before escalation.",
        ]
    if report_profile == "abnormal-exposure":
        return [
            "Start with admin, middleware, database, and alternate HTTPS ports before low-signal commodity web hosts.",
            "Validate whether leak-like artifacts are intentional, stale index residue, or true public exposure.",
            "Separate broad internet noise from assets that clearly tie back to the target's brand, domain, or organization.",
        ]
    if report_profile == "takeover-risk":
        return [
            "Confirm DNS, CNAME, and platform ownership before calling an asset truly takeable.",
            "Give extra weight to placeholder pages, default error responses, and cloud edge providers with missing origins.",
            "Preserve both the suspected hostname and the observed platform signal in the handoff so validation is reproducible.",
        ]
    return [
        "Keep the strongest signals first, then preserve concrete next steps for validation and delivery.",
        "Use the export, targets list, and any nuclei suggestion as the operational handoff bundle.",
    ]


def build_profile_focus_section(
    report_profile: str,
    result_objects: List[Dict[str, str]],
    user_intent: str = "",
) -> List[str]:
    meta = resolve_report_profile(report_profile, user_intent=user_intent)
    top_orgs = top_counts((item.get("org", "") for item in result_objects), limit=5)
    top_asns = top_counts((item.get("asn", "") for item in result_objects), limit=5)
    top_ports = top_counts((item.get("port", "") for item in result_objects), limit=5)
    sample_objects = collect_profile_samples(meta["name"], result_objects, limit=6)

    lines = [
        "",
        "## Report Lens",
        "",
        f"- Profile: `{meta['label']}`",
        f"- Focus: {meta['focus']}.",
        f"- Why This Lens: {meta['reason']}.",
    ]

    if meta["name"] == "attack-infrastructure":
        cloud_orgs = [name for name, _ in top_orgs if any(marker in name.lower() for marker in CLOUD_PROVIDER_MARKERS)]
        infra_hits = sum(1 for item in result_objects if item_matches_markers(item, ATTACK_INFRA_MARKERS))
        lines.extend(["", "## Infrastructure Hypotheses", ""])
        if cloud_orgs:
            lines.append(f"- Hosting concentration touches cloud or edge providers such as `{', '.join(cloud_orgs[:4])}`.")
        if infra_hits:
            lines.append(f"- `{infra_hits}` rows contain tooling or infrastructure markers worth campaign-style review.")
        if top_ports:
            lines.append(f"- Repeated exposed ports are `{', '.join(name for name, _ in top_ports[:5])}`, which can help cluster operator patterns.")
        if top_asns:
            lines.append(f"- Top ASNs include `{', '.join(name for name, _ in top_asns[:3] if name)}`.")
    elif meta["name"] == "abnormal-exposure":
        abnormal_hits = sum(1 for item in result_objects if item_matches_markers(item, ABNORMAL_EXPOSURE_MARKERS))
        high_signal_count = sum(1 for item in result_objects if item.get("port", "") in HIGH_RISK_PORTS)
        lines.extend(["", "## Exposure Hypotheses", ""])
        if high_signal_count:
            lines.append(f"- `{high_signal_count}` rows sit on management, database, or otherwise high-signal ports.")
        if abnormal_hits:
            lines.append(f"- `{abnormal_hits}` rows expose artifact strings that look more like operational leakage than commodity web content.")
        if top_orgs:
            lines.append(f"- Organization clustering is led by `{', '.join(name for name, _ in top_orgs[:3] if name)}`.")
    elif meta["name"] == "takeover-risk":
        placeholder_hits = sum(1 for item in result_objects if item_matches_markers(item, TAKEOVER_MARKERS))
        lines.extend(["", "## Takeover Hypotheses", ""])
        if placeholder_hits:
            lines.append(f"- `{placeholder_hits}` rows include placeholder, not-found, or platform-default signals worth brand-control review.")
        if top_orgs:
            lines.append(f"- Platform ownership appears concentrated around `{', '.join(name for name, _ in top_orgs[:3] if name)}`.")
        if top_ports:
            lines.append(f"- The dominant exposed ports are `{', '.join(name for name, _ in top_ports[:5])}`; web-heavy patterns deserve origin validation.")
    else:
        lines.extend(["", "## Analyst Focus", ""])
        lines.append("- Use this standard view when the job is delivery-first asset handoff rather than a single hunt family.")
        if top_orgs:
            lines.append(f"- The strongest ownership signals are `{', '.join(name for name, _ in top_orgs[:3] if name)}`.")

    if sample_objects:
        evidence_rows = [
            [
                item.get("target") or item.get("host") or item.get("ip", ""),
                item.get("ip", ""),
                item.get("port", ""),
                item.get("title", ""),
                item.get("server", "") or item.get("product", ""),
                item.get("org", ""),
            ]
            for item in sample_objects
        ]
        lines.extend(
            [
                "",
                "## Focus Evidence",
                "",
                markdown_table(["Target", "IP", "Port", "Title", "Server/Product", "Org"], evidence_rows),
            ]
        )

    lines.extend(["", "## Profile Actions", ""])
    for action in report_profile_action_lines(meta["name"]):
        lines.append(f"- {action}")
    return lines


def build_asset_report(
    project_name: str,
    query_summaries: List[Dict[str, Any]],
    result_objects: List[Dict[str, str]],
    user_intent: str,
    nuclei_suggestion: Dict[str, Any] | None,
    output_files: Dict[str, str],
    nuclei_log_summary: Dict[str, int] | None = None,
    report_profile: str | None = None,
) -> str:
    profile_meta = resolve_report_profile(report_profile, user_intent=user_intent, context_hint=project_name)
    date_str = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_assets = len(result_objects)
    unique_targets_count = len(unique_nonempty(item.get("target", "") for item in result_objects))
    unique_ips_count = len(unique_nonempty(item.get("ip", "") for item in result_objects))
    alive_count = sum(1 for item in result_objects if is_alive_status(item.get("http_status", "")))

    top_ports = top_counts((item.get("port", "") for item in result_objects), limit=5)
    top_servers = top_counts((item.get("server", "") for item in result_objects), limit=5)
    top_countries = top_counts((item.get("country_name", "") for item in result_objects), limit=5)
    top_orgs = top_counts((item.get("org", "") for item in result_objects), limit=5)
    top_titles = top_counts((item.get("title", "") for item in result_objects if item.get("title")), limit=5)

    risky_ports = ordered_unique(
        port for port in (item.get("port", "") for item in result_objects) if port in HIGH_RISK_PORTS
    )

    lines = [
        f"# FOFAMAP {profile_meta['title_suffix']} Report",
        "",
        f"- Project: `{project_name}`",
        f"- Generated: `{date_str}`",
        f"- User Intent: {user_intent or 'FOFA asset reconnaissance'}",
        f"- Report Profile: `{profile_meta['label']}`",
        f"- Queries Executed: `{len(query_summaries)}`",
        f"- Asset Rows: `{total_assets}`",
        f"- Unique Targets: `{unique_targets_count}`",
        f"- Unique IPs: `{unique_ips_count}`",
    ]
    if alive_count:
        lines.append(f"- Live HTTP Targets: `{alive_count}`")

    lines.extend(
        [
            "",
            "## Exposure Snapshot",
            "",
            "- This report preserves the original project's operator-first style: collect assets, keep what is actionable, and prepare the next step.",
        ]
    )

    if risky_ports:
        lines.append(f"- Notable exposed ports: `{', '.join(risky_ports)}`")
        for port in risky_ports[:5]:
            lines.append(f"  - Port `{port}`: {HIGH_RISK_PORTS.get(port, 'Review exposure.')}")
    else:
        lines.append("- No obviously high-signal management or database port stood out in the filtered result set.")

    lines.extend(build_profile_focus_section(profile_meta["name"], result_objects, user_intent=user_intent))

    if top_servers:
        lines.append("")
        lines.append("## Stack Signals")
        lines.append("")
        for name, count in top_servers:
            lines.append(f"- `{name}`: `{count}` rows")

    if top_countries:
        lines.append("")
        lines.append("## Geographic Distribution")
        lines.append("")
        for name, count in top_countries:
            lines.append(f"- `{name}`: `{count}` rows")

    if top_orgs:
        lines.append("")
        lines.append("## Ownership Signals")
        lines.append("")
        for name, count in top_orgs:
            lines.append(f"- `{name}`: `{count}` rows")

    if top_ports:
        lines.append("")
        lines.append("## Port Distribution")
        lines.append("")
        for name, count in top_ports:
            lines.append(f"- Port `{name}`: `{count}` rows")

    if nuclei_suggestion:
        lines.extend(
            [
                "",
                "## Suggested Nuclei Follow-up",
                "",
                "```bash",
                nuclei_suggestion["command"],
                "```",
            ]
        )
        if nuclei_suggestion.get("reasons"):
            for reason in nuclei_suggestion["reasons"]:
                lines.append(f"- {reason}")

    if nuclei_log_summary:
        lines.extend(
            [
                "",
                "## Nuclei Log Summary",
                "",
                f"- Critical: `{nuclei_log_summary.get('critical', 0)}`",
                f"- High: `{nuclei_log_summary.get('high', 0)}`",
                f"- Medium: `{nuclei_log_summary.get('medium', 0)}`",
                f"- Low: `{nuclei_log_summary.get('low', 0)}`",
                f"- Info: `{nuclei_log_summary.get('info', 0)}`",
            ]
        )

    if top_titles:
        lines.extend(["", "## Sample Titles", ""])
        for name, count in top_titles[:5]:
            lines.append(f"- `{name}`: `{count}` rows")

    lines.extend(["", "## Query Appendix", ""])
    appendix_rows: List[List[str]] = []
    for item in query_summaries:
        appendix_rows.append(
            [
                item.get("query", ""),
                item.get("used_fields", ""),
                str(item.get("result_count", 0)),
            ]
        )
    if appendix_rows:
        lines.append(markdown_table(["Query", "Used Fields", "Rows"], appendix_rows))

    lines.extend(["", "## Output Files", ""])
    for label, path in output_files.items():
        lines.append(f"- `{label}`: `{path}`")

    sample_rows: List[List[str]] = []
    for item in result_objects[:10]:
        sample_rows.append(
            [
                item.get("host") or item.get("target") or item.get("ip", ""),
                item.get("ip", ""),
                item.get("port", ""),
                item.get("title", ""),
                item.get("http_status", ""),
            ]
        )
    if sample_rows:
        lines.extend(["", "## Asset Sample", "", markdown_table(["Host", "IP", "Port", "Title", "HTTP Status"], sample_rows)])

    return "\n".join(lines).strip() + "\n"


def compact_monitor_object(item: Dict[str, Any], include_source_query: bool = False) -> Dict[str, str]:
    compact: Dict[str, str] = {}
    for key, value in item.items():
        if key == "source_query" and not include_source_query:
            continue
        if value in {"", None}:
            continue
        compact[str(key)] = str(value)
    return compact


def asset_identity_key(item: Dict[str, Any], include_source_query: bool = False) -> str:
    compact = compact_monitor_object(item, include_source_query=include_source_query)
    base = ""
    for key in ("target", "link", "host"):
        value = compact.get(key, "").strip().lower()
        if value:
            base = value
            break
    if not base:
        ip = compact.get("ip", "").strip().lower()
        port = compact.get("port", "").strip().lower()
        protocol = compact.get("protocol", "").strip().lower()
        domain = compact.get("domain", "").strip().lower()
        if ip and port:
            base = f"{ip}:{port}"
            if protocol:
                base = f"{base}/{protocol}"
        elif ip:
            base = ip
        elif domain:
            base = domain
    if not base:
        base = json.dumps(compact, ensure_ascii=False, sort_keys=True)
    if include_source_query and compact.get("source_query"):
        return f'{compact["source_query"]}::{base}'
    return base


def compare_asset_inventory(
    previous_objects: List[Dict[str, Any]],
    current_objects: List[Dict[str, Any]],
    include_source_query: bool = False,
) -> Dict[str, Any]:
    previous_map: Dict[str, Dict[str, str]] = {}
    current_map: Dict[str, Dict[str, str]] = {}

    for item in previous_objects:
        key = asset_identity_key(item, include_source_query=include_source_query)
        if key and key not in previous_map:
            previous_map[key] = compact_monitor_object(item, include_source_query=include_source_query)
    for item in current_objects:
        key = asset_identity_key(item, include_source_query=include_source_query)
        if key and key not in current_map:
            current_map[key] = compact_monitor_object(item, include_source_query=include_source_query)

    previous_keys = set(previous_map)
    current_keys = set(current_map)
    added_keys = sorted(current_keys - previous_keys)
    removed_keys = sorted(previous_keys - current_keys)
    shared_keys = sorted(previous_keys & current_keys)

    changed_objects: List[Dict[str, Any]] = []
    for key in shared_keys:
        previous_item = previous_map[key]
        current_item = current_map[key]
        changed_fields = [
            field
            for field in sorted(set(previous_item) | set(current_item))
            if previous_item.get(field, "") != current_item.get(field, "")
        ]
        if changed_fields:
            changed_objects.append(
                {
                    "asset_key": key,
                    "changed_fields": changed_fields,
                    "previous": previous_item,
                    "current": current_item,
                }
            )

    return {
        "previous_count": len(previous_map),
        "current_count": len(current_map),
        "added_count": len(added_keys),
        "removed_count": len(removed_keys),
        "changed_count": len(changed_objects),
        "unchanged_count": len(shared_keys) - len(changed_objects),
        "added_objects": [current_map[key] for key in added_keys],
        "removed_objects": [previous_map[key] for key in removed_keys],
        "changed_objects": changed_objects,
        "added_samples": [current_map[key] for key in added_keys[:10]],
        "removed_samples": [previous_map[key] for key in removed_keys[:10]],
        "changed_samples": changed_objects[:10],
    }


def compare_query_snapshots(previous_queries: List[Dict[str, Any]], current_queries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    previous_map = {
        str(item.get("query", "")): item
        for item in previous_queries
        if isinstance(item, dict) and item.get("query")
    }
    current_map = {
        str(item.get("query", "")): item
        for item in current_queries
        if isinstance(item, dict) and item.get("query")
    }

    summaries: List[Dict[str, Any]] = []
    for query in ordered_unique(list(previous_map.keys()) + list(current_map.keys())):
        previous_objects = previous_map.get(query, {}).get("result_objects", []) or []
        current_objects = current_map.get(query, {}).get("result_objects", []) or []
        diff = compare_asset_inventory(previous_objects, current_objects)
        summaries.append(
            {
                "query": query,
                "previous_count": diff["previous_count"],
                "current_count": diff["current_count"],
                "added_count": diff["added_count"],
                "removed_count": diff["removed_count"],
                "changed_count": diff["changed_count"],
                "has_changes": bool(diff["added_count"] or diff["removed_count"] or diff["changed_count"]),
            }
        )
    return summaries


def build_object_export_rows(objects: List[Dict[str, Any]]) -> tuple[List[str], List[List[str]]]:
    preferred = [
        "source_query",
        "target",
        "host",
        "link",
        "ip",
        "port",
        "protocol",
        "http_status",
        "title",
        "server",
        "product",
        "product.version",
        "domain",
        "country_name",
        "org",
        "asn",
        "lastupdatetime",
    ]
    ordered_fields: List[str] = [field for field in preferred if any(obj.get(field) for obj in objects)]
    for item in objects:
        for key in item.keys():
            if key not in ordered_fields:
                ordered_fields.append(key)
    headers = ["ID"] + [field.upper() for field in ordered_fields]
    rows: List[List[str]] = []
    for index, item in enumerate(objects, start=1):
        rows.append([str(index)] + [str(item.get(field, "")) for field in ordered_fields])
    return headers, rows


def build_changed_export_rows(changed_objects: List[Dict[str, Any]]) -> tuple[List[str], List[List[str]]]:
    headers = [
        "ID",
        "ASSET_KEY",
        "CHANGED_FIELDS",
        "SOURCE_QUERY",
        "TARGET",
        "IP",
        "PORT",
        "PROTOCOL",
        "PREVIOUS_HTTP_STATUS",
        "CURRENT_HTTP_STATUS",
        "PREVIOUS_TITLE",
        "CURRENT_TITLE",
        "PREVIOUS_SERVER",
        "CURRENT_SERVER",
    ]
    rows: List[List[str]] = []
    for index, item in enumerate(changed_objects, start=1):
        previous = item.get("previous", {})
        current = item.get("current", {})
        rows.append(
            [
                str(index),
                str(item.get("asset_key", "")),
                ", ".join(item.get("changed_fields", [])),
                current.get("source_query", "") or previous.get("source_query", ""),
                current.get("target", "") or previous.get("target", ""),
                current.get("ip", "") or previous.get("ip", ""),
                current.get("port", "") or previous.get("port", ""),
                current.get("protocol", "") or previous.get("protocol", ""),
                previous.get("http_status", ""),
                current.get("http_status", ""),
                previous.get("title", ""),
                current.get("title", ""),
                previous.get("server", ""),
                current.get("server", ""),
            ]
        )
    return headers, rows


def build_monitor_state_dir(project_name: str | None, outdir: str | None, seed_query: str) -> Path:
    if outdir:
        path = Path(outdir).expanduser()
    else:
        base_name = slugify(project_name or seed_query, fallback="fofa_monitor", limit=40)
        path = Path.cwd() / DEFAULT_RESULTS_DIR / f"monitor_{base_name}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def derive_monitor_alert(diff_summary: Dict[str, Any]) -> Dict[str, Any]:
    if diff_summary.get("baseline_established"):
        return {
            "alert": False,
            "alert_level": "none",
            "reasons": ["initial baseline snapshot established for future scheduled comparisons"],
            "risky_added_ports": [],
        }

    alert_level = "none"
    reasons: List[str] = []
    added_objects = diff_summary.get("added_objects", []) or []
    risky_added_ports = ordered_unique(
        item.get("port", "") for item in added_objects if item.get("port", "") in HIGH_RISK_PORTS
    )

    if risky_added_ports:
        alert_level = "high"
        reasons.append(f"new assets appeared on high-signal ports: {', '.join(risky_added_ports)}")
    elif diff_summary.get("added_count") or diff_summary.get("removed_count"):
        alert_level = "medium"
        reasons.append("asset inventory changed since the previous snapshot")
    elif diff_summary.get("changed_count"):
        alert_level = "low"
        reasons.append("existing assets changed metadata or live status")
    else:
        reasons.append("no inventory drift was observed")

    return {
        "alert": alert_level != "none",
        "alert_level": alert_level,
        "reasons": reasons,
        "risky_added_ports": risky_added_ports,
    }


def build_monitor_report(
    project_name: str,
    query_mode: str,
    query_summaries: List[Dict[str, Any]],
    current_objects: List[Dict[str, str]],
    diff_summary: Dict[str, Any],
    query_diffs: List[Dict[str, Any]],
    output_files: Dict[str, str],
    previous_generated_at: str = "",
    user_intent: str = "",
    nuclei_suggestion: Dict[str, Any] | None = None,
    report_profile: str | None = None,
) -> str:
    profile_meta = resolve_report_profile(report_profile, user_intent=user_intent, context_hint=project_name)
    date_str = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    unique_targets_count = len(unique_nonempty(item.get("target", "") for item in current_objects))
    unique_ips_count = len(unique_nonempty(item.get("ip", "") for item in current_objects))
    alive_count = sum(1 for item in current_objects if is_alive_status(item.get("http_status", "")))
    top_ports = top_counts((item.get("port", "") for item in current_objects), limit=5)
    top_servers = top_counts((item.get("server", "") for item in current_objects), limit=5)
    top_countries = top_counts((item.get("country_name", "") for item in current_objects), limit=5)
    top_titles = top_counts((item.get("title", "") for item in current_objects if item.get("title")), limit=5)
    alert = derive_monitor_alert(diff_summary)

    lines = [
        f"# FOFAMAP {profile_meta['title_suffix']} Monitoring Report",
        "",
        f"- Monitoring Profile: `{project_name}`",
        f"- Generated: `{date_str}`",
        f"- User Intent: {user_intent or 'FOFA asset monitoring'}",
        f"- Report Profile: `{profile_meta['label']}`",
        f"- Query Mode: `{query_mode}`",
        f"- Queries Executed: `{len(query_summaries)}`",
        f"- Previous Snapshot: `{previous_generated_at or 'none, this is the first baseline run'}`",
        f"- Alert Status: `{alert['alert_level']}`",
        f"- Current Unique Targets: `{unique_targets_count}`",
        f"- Current Unique IPs: `{unique_ips_count}`",
        f"- Added Assets: `{diff_summary.get('added_count', 0)}`",
        f"- Removed Assets: `{diff_summary.get('removed_count', 0)}`",
        f"- Changed Assets: `{diff_summary.get('changed_count', 0)}`",
    ]
    if alive_count:
        lines.append(f"- Live HTTP Targets: `{alive_count}`")

    lines.extend(["", "## Executive Judgment", ""])
    for reason in alert["reasons"]:
        lines.append(f"- {reason}.")
    if not previous_generated_at:
        lines.append("- This run established the baseline snapshot that later scheduled runs can compare against.")
    else:
        lines.append("- Treat newly observed assets as exposure growth until an operator confirms they are expected.")
        lines.append("- Treat removed assets as either decommissioning, temporary FOFA drift, or visibility loss that should be confirmed.")

    lines.extend(build_profile_focus_section(profile_meta["name"], current_objects, user_intent=user_intent))

    if query_diffs:
        lines.extend(["", "## Query Drift Summary", ""])
        drift_rows = [
            [
                item.get("query", ""),
                str(item.get("previous_count", 0)),
                str(item.get("current_count", 0)),
                str(item.get("added_count", 0)),
                str(item.get("removed_count", 0)),
                str(item.get("changed_count", 0)),
            ]
            for item in query_diffs
        ]
        lines.append(markdown_table(["Query", "Previous", "Current", "Added", "Removed", "Changed"], drift_rows))

    if diff_summary.get("added_samples"):
        lines.extend(["", "## Newly Observed Assets", ""])
        new_rows: List[List[str]] = []
        for item in diff_summary["added_samples"]:
            new_rows.append(
                [
                    item.get("source_query", ""),
                    item.get("target") or item.get("host") or item.get("ip", ""),
                    item.get("ip", ""),
                    item.get("port", ""),
                    item.get("title", ""),
                    item.get("http_status", ""),
                ]
            )
        lines.append(markdown_table(["Query", "Target", "IP", "Port", "Title", "HTTP Status"], new_rows))

    if diff_summary.get("removed_samples"):
        lines.extend(["", "## Removed Or Missing Assets", ""])
        removed_rows: List[List[str]] = []
        for item in diff_summary["removed_samples"]:
            removed_rows.append(
                [
                    item.get("source_query", ""),
                    item.get("target") or item.get("host") or item.get("ip", ""),
                    item.get("ip", ""),
                    item.get("port", ""),
                    item.get("title", ""),
                    item.get("http_status", ""),
                ]
            )
        lines.append(markdown_table(["Query", "Target", "IP", "Port", "Title", "HTTP Status"], removed_rows))

    if diff_summary.get("changed_samples"):
        lines.extend(["", "## Changed Existing Assets", ""])
        changed_rows: List[List[str]] = []
        for item in diff_summary["changed_samples"]:
            current = item.get("current", {})
            previous = item.get("previous", {})
            changed_rows.append(
                [
                    current.get("source_query", "") or previous.get("source_query", ""),
                    current.get("target", "") or previous.get("target", ""),
                    ", ".join(item.get("changed_fields", [])),
                    previous.get("http_status", ""),
                    current.get("http_status", ""),
                ]
            )
        lines.append(markdown_table(["Query", "Target", "Changed Fields", "Prev HTTP", "Curr HTTP"], changed_rows))

    lines.extend(["", "## Current Exposure Snapshot", ""])
    if alert["risky_added_ports"]:
        for port in alert["risky_added_ports"][:5]:
            lines.append(f"- New high-signal port `{port}`: {HIGH_RISK_PORTS.get(port, 'Review exposure.')}")
    if top_ports:
        lines.append("")
        lines.append("### Port Distribution")
        lines.append("")
        for name, count in top_ports:
            lines.append(f"- Port `{name}`: `{count}` rows")
    if top_servers:
        lines.append("")
        lines.append("### Stack Signals")
        lines.append("")
        for name, count in top_servers:
            lines.append(f"- `{name}`: `{count}` rows")
    if top_countries:
        lines.append("")
        lines.append("### Geographic Distribution")
        lines.append("")
        for name, count in top_countries:
            lines.append(f"- `{name}`: `{count}` rows")
    if top_titles:
        lines.append("")
        lines.append("### Common Titles")
        lines.append("")
        for name, count in top_titles:
            lines.append(f"- `{name}`: `{count}` rows")

    if nuclei_suggestion:
        lines.extend(
            [
                "",
                "## Suggested Validation Path",
                "",
                "```bash",
                nuclei_suggestion["command"],
                "```",
            ]
        )
        for reason in nuclei_suggestion.get("reasons", []):
            lines.append(f"- {reason}")

    lines.extend(["", "## Recommended Actions", ""])
    if diff_summary.get("added_count"):
        lines.append("- Review newly observed assets first, especially entries on admin, middleware, database, or alternate HTTPS ports.")
    if diff_summary.get("removed_count"):
        lines.append("- Confirm removed assets against change windows so FOFA index delay is not mistaken for true decommissioning.")
    if diff_summary.get("changed_count"):
        lines.append("- Check changed assets for title, server, or HTTP status shifts that may indicate upgrades, outages, or access-control changes.")
    if not (diff_summary.get("added_count") or diff_summary.get("removed_count") or diff_summary.get("changed_count")):
        lines.append("- No obvious drift was detected, so keep the current cadence and preserve this snapshot as a clean baseline.")

    lines.extend(["", "## Output Files", ""])
    for label, path in output_files.items():
        lines.append(f"- `{label}`: `{path}`")

    return "\n".join(lines).strip() + "\n"


def extract_host_payload(host_data: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(host_data.get("data"), dict):
        return dict(host_data.get("data") or {})
    return dict(host_data or {})


def normalize_host_ports(raw_ports: Any) -> List[Dict[str, Any]]:
    if isinstance(raw_ports, dict):
        ports: List[Dict[str, Any]] = []
        for port_key, item in raw_ports.items():
            mapped = dict(item or {})
            if "port" not in mapped:
                mapped["port"] = port_key
            ports.append(mapped)
        return sorted(ports, key=lambda item: port_int(str(item.get("port", ""))))
    if isinstance(raw_ports, list):
        return sorted(
            [dict(item) for item in raw_ports if isinstance(item, dict)],
            key=lambda item: port_int(str(item.get("port", ""))),
        )
    return []


def normalize_named_items(raw_items: Any, fallback_key: str = "name") -> List[str]:
    values: List[str] = []
    if isinstance(raw_items, list):
        for item in raw_items:
            if isinstance(item, dict):
                value = str(item.get(fallback_key, "")).strip()
            else:
                value = str(item).strip()
            if value:
                values.append(value)
    return ordered_unique(values)


def extract_port_products(port_item: Dict[str, Any]) -> List[str]:
    names: List[str] = []
    for product in port_item.get("products", []) or []:
        if isinstance(product, dict):
            value = str(product.get("product", "")).strip()
            if value:
                names.append(value)
    for key in ("product", "service", "server"):
        value = str(port_item.get(key, "")).strip()
        if value:
            names.append(value)
    return ordered_unique(names)


def summarize_host_profile(target: str, host_data: Dict[str, Any]) -> Dict[str, Any]:
    payload = extract_host_payload(host_data)
    ports = normalize_host_ports(payload.get("ports"))
    domains = normalize_named_items(payload.get("domains"))
    rules = normalize_named_items(payload.get("rules"))
    port_rules = payload.get("port_rules", {}) if isinstance(payload.get("port_rules"), dict) else {}

    protocols: List[str] = []
    raw_protocols = payload.get("protocols")
    if isinstance(raw_protocols, list):
        for item in raw_protocols:
            if isinstance(item, dict):
                base_protocol = str(item.get("base_protocol", "")).strip().lower()
                protocol = str(item.get("protocol", "")).strip().lower()
                label = "/".join(part for part in [base_protocol.upper(), protocol.upper()] if part)
            else:
                label = str(item).strip()
            if label:
                protocols.append(label)
    if not protocols:
        for item in ports:
            base_protocol = str(item.get("base_protocol", "")).strip().lower()
            protocol = str(item.get("protocol", "")).strip().lower()
            label = "/".join(part for part in [base_protocol.upper(), protocol.upper()] if part)
            if label:
                protocols.append(label)

    product_hints: List[str] = []
    for item in ports:
        product_hints.extend(extract_port_products(item))

    return {
        "target": target,
        "ip": str(payload.get("ip", "")),
        "asn": str(payload.get("asn", "")),
        "org": str(payload.get("org", "")),
        "isp": str(payload.get("isp", "")),
        "country": str(payload.get("country_name") or payload.get("country") or ""),
        "country_code2": str(payload.get("country_code2") or payload.get("country_code") or ""),
        "city": str(payload.get("city", "")),
        "update_time": str(
            payload.get("update_time")
            or payload.get("lastupdatetime")
            or payload.get("mtime")
            or payload.get("last_atime")
            or ""
        ),
        "domains": domains,
        "domain_count": len(domains),
        "protocols": ordered_unique(protocols),
        "protocol_count": len(ordered_unique(protocols)),
        "ports": ports,
        "port_count": len(ports),
        "rules": rules,
        "rule_count": len(rules),
        "port_rules": port_rules,
        "product_hints": ordered_unique(product_hints),
    }


def build_host_profile_section(report_profile: str, host_profile: Dict[str, Any], risk_level: str) -> List[str]:
    meta = resolve_report_profile(report_profile)
    lines = [
        "",
        "## Analyst Lens",
        "",
        f"- Profile: `{meta['label']}`",
        f"- Focus: {meta['focus']}.",
        f"- Current Risk Baseline: `{risk_level}`.",
    ]
    ports = [str(item.get("port", "")) for item in host_profile.get("ports", [])]
    products = ", ".join(host_profile.get("product_hints", [])[:8])
    if meta["name"] == "attack-infrastructure":
        lines.append("- Use this lens to ask whether the host belongs to a broader managed cluster, tooling stack, or campaign pattern.")
        if products:
            lines.append(f"- Product fingerprints that can support clustering: `{products}`.")
        if ports:
            lines.append(f"- Port spread for clustering: `{', '.join(ports[:10])}`.")
    elif meta["name"] == "abnormal-exposure":
        lines.append("- Use this lens to separate normal business exposure from odd admin, middleware, or data-service reachability.")
        if ports:
            lines.append(f"- High-signal host ports to validate first: `{', '.join(port for port in ports if port in HIGH_RISK_PORTS) or ', '.join(ports[:8])}`.")
    elif meta["name"] == "takeover-risk":
        lines.append("- Use this lens when the host may be part of a dangling service, misbound domain, or abandoned edge deployment.")
        if host_profile.get("domains"):
            lines.append(f"- Domains that deserve DNS and platform-ownership review: `{', '.join(host_profile['domains'][:8])}`.")
    else:
        lines.append("- Use this standard lens for host-level delivery, triage, and validation handoff.")
    return lines


def build_host_report(
    target: str,
    host_data: Dict[str, Any],
    user_intent: str = "",
    report_profile: str | None = None,
) -> str:
    profile_meta = resolve_report_profile(report_profile, user_intent=user_intent, context_hint=target)
    host_profile = summarize_host_profile(target, host_data)
    ports = host_profile["ports"]
    products = host_profile["product_hints"]
    port_numbers = [str(item.get("port", "")) for item in ports]

    score = 0
    for port in port_numbers:
        if port in {"3389", "445", "6379", "7001", "1433"}:
            score += 3
        elif port in {"22", "3306", "5432", "8080", "8443"}:
            score += 1
    product_blob = " ".join(products).lower()
    for keywords, _, _ in NUCLEI_RULES:
        if any(keyword in product_blob for keyword in keywords):
            score += 2
            break
    if len(ports) >= 5:
        score += 1

    if score >= 6:
        risk_level = "High"
    elif score >= 3:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    attack_paths: List[str] = []
    for port in port_numbers:
        if port in HIGH_RISK_PORTS:
            attack_paths.append(f"Port `{port}`: {HIGH_RISK_PORTS[port]}")
    if "weblogic" in product_blob:
        attack_paths.append("Validate WebLogic-specific exposures and admin interfaces.")
    if "redis" in product_blob or "6379" in port_numbers:
        attack_paths.append("Check for weak or absent Redis authentication and unsafe exposure.")
    if "exchange" in product_blob:
        attack_paths.append("Review Exchange-specific surface such as OWA or legacy endpoints.")
    if not attack_paths:
        attack_paths.append("Prioritize reachable web services and identify whether any exposed service is administrative.")

    appendix_rows: List[List[str]] = []
    for item in ports:
        appendix_rows.append(
            [
                str(item.get("port", "")),
                str(item.get("protocol", "")),
                ", ".join(extract_port_products(item))[:120],
                str(
                    item.get("update_time")
                    or item.get("lastupdatetime")
                    or item.get("mtime")
                    or host_profile.get("update_time", "")
                ).split(" ")[0],
            ]
        )

    lines = [
        f"# FOFAMAP {profile_meta['title_suffix']} Host Report",
        "",
        f"- Target: `{target}`",
        f"- User Intent: {user_intent or 'Host profiling'}",
        f"- Report Profile: `{profile_meta['label']}`",
        f"- IP: `{host_profile.get('ip', '')}`",
        f"- ASN: `{host_profile.get('asn', '')}`",
        f"- Org: `{host_profile.get('org', '')}`",
        f"- ISP: `{host_profile.get('isp', '')}`",
        f"- Country: `{host_profile.get('country', '')}`",
        f"- City: `{host_profile.get('city', '')}`",
        f"- Country Code: `{host_profile.get('country_code2', '')}`",
        f"- Update Time: `{host_profile.get('update_time', '')}`",
        f"- Ports Observed: `{host_profile.get('port_count', 0)}`",
        f"- Domains Observed: `{host_profile.get('domain_count', 0)}`",
        f"- Rules Observed: `{host_profile.get('rule_count', 0)}`",
        "",
        "## Exposure Analysis",
        "",
    ]
    if ports:
        for item in ports:
            port = str(item.get("port", ""))
            protocol = str(item.get("protocol", ""))
            note = HIGH_RISK_PORTS.get(port, "Observed service exposure.")
            lines.append(f"- `{port}/{protocol}`: {note}")
    else:
        lines.append("- FOFA did not return detailed open-port information for this host.")

    if host_profile.get("protocols"):
        lines.extend(["", "## Protocol View", ""])
        for item in host_profile["protocols"][:10]:
            lines.append(f"- `{item}`")

    if host_profile.get("domains"):
        lines.extend(["", "## Domain View", ""])
        for item in host_profile["domains"][:10]:
            lines.append(f"- `{item}`")

    if host_profile.get("rules"):
        lines.extend(["", "## Component Rules", ""])
        for item in host_profile["rules"][:10]:
            lines.append(f"- `{item}`")

    lines.extend(build_host_profile_section(profile_meta["name"], host_profile, risk_level))

    lines.extend(["", "## Risk Judgement", "", f"- Overall Risk: `{risk_level}`"])
    if products:
        lines.append(f"- Product Hints: `{', '.join(products[:8])}`")
    else:
        lines.append("- Product fingerprints are limited; confirm service identity with live validation if permitted.")

    lines.extend(["", "## Likely Attack Paths", ""])
    for item in attack_paths[:6]:
        lines.append(f"- {item}")

    if appendix_rows:
        lines.extend(["", "## Raw Port Snapshot", "", markdown_table(["Port", "Protocol", "Products", "Update"], appendix_rows)])

    return "\n".join(lines).strip() + "\n"


def summarize_stats_data(stat_data: Dict[str, Any]) -> Dict[str, Any]:
    total = int(stat_data.get("size", 0) or 0)
    aggs = stat_data.get("aggs", {}) or {}
    distinct = stat_data.get("distinct", {}) or {}
    top_summary: Dict[str, Dict[str, Any]] = {}

    for field_name, items in aggs.items():
        if not items:
            continue
        top = items[0]
        top_count = int(top.get("count", 0) or 0)
        top_summary[field_name] = {
            "name": str(top.get("name", "")),
            "count": top_count,
            "ratio": (top_count / total * 100) if total else 0,
        }

    return {
        "size": total,
        "consumed_fpoint": normalize_optional_int(stat_data.get("consumed_fpoint")),
        "required_fpoints": normalize_optional_int(stat_data.get("required_fpoints")),
        "lastupdatetime": str(stat_data.get("lastupdatetime", "")),
        "distinct": distinct,
        "top_summary": top_summary,
    }


def build_stats_profile_section(
    report_profile: str,
    stats_summary: Dict[str, Any],
    aggs: Dict[str, Any],
) -> List[str]:
    meta = resolve_report_profile(report_profile)
    lines = [
        "",
        "## Analyst Lens",
        "",
        f"- Profile: `{meta['label']}`",
        f"- Focus: {meta['focus']}.",
    ]
    if meta["name"] == "attack-infrastructure":
        lines.append("- Use the aggregation to spot hosting concentration, repeated providers, and campaign-style spread rather than one isolated host.")
        if "asn" in aggs:
            lines.append("- ASN concentration is especially useful for clustering infrastructure footprints.")
    elif meta["name"] == "abnormal-exposure":
        lines.append("- Use the aggregation to identify outlier ports, locations, and stacks that deserve validation before broad handoff.")
        if "port" in aggs:
            lines.append("- Port buckets help surface non-default operational exposure quickly.")
    elif meta["name"] == "takeover-risk":
        lines.append("- Use the aggregation to look for platform-heavy concentration, web-edge distribution, and unusual ownership patterns around the target.")
        if "domain" in aggs:
            lines.append("- Domain buckets can reveal whether risk is concentrated on a specific brand or namespace.")
    else:
        lines.append("- Use the aggregation as a baseline exposure map to support later host-level or project-level decisions.")
    if stats_summary.get("distinct"):
        lines.append(f"- Distinct dimensions returned: `{', '.join(str(key) for key in stats_summary['distinct'].keys())}`.")
    return lines


def build_stats_report(
    query: str,
    stat_data: Dict[str, Any],
    user_intent: str = "",
    report_profile: str | None = None,
) -> str:
    profile_meta = resolve_report_profile(report_profile, user_intent=user_intent, context_hint=query)
    stats_summary = summarize_stats_data(stat_data)
    total = int(stats_summary.get("size", 0) or 0)
    aggs = stat_data.get("aggs", {}) or {}
    distinct = stats_summary.get("distinct", {}) or {}

    lines = [
        f"# FOFAMAP {profile_meta['title_suffix']} Statistical Report",
        "",
        f"- Query: `{query}`",
        f"- User Intent: {user_intent or 'Statistical distribution analysis'}",
        f"- Report Profile: `{profile_meta['label']}`",
        f"- Total Matches: `{total}`",
        f"- Consumed F-Point: `{stats_summary.get('consumed_fpoint', '')}`",
        f"- Required F-Points: `{stats_summary.get('required_fpoints', '')}`",
        f"- Last Update Time: `{stats_summary.get('lastupdatetime', '')}`",
        "",
        "## Distribution Traits",
        "",
    ]

    for field_name, summary in stats_summary.get("top_summary", {}).items():
        lines.append(
            f"- `{field_name}` is led by `{summary.get('name', '')}` with `{summary.get('count', 0)}` records ({summary.get('ratio', 0):.2f}%)."
        )

    if not aggs:
        lines.append("- FOFA returned no aggregation buckets for the requested dimensions.")

    lines.extend(build_stats_profile_section(profile_meta["name"], stats_summary, aggs))

    lines.extend(["", "## Anomaly Notes", ""])
    if "port" in aggs and aggs["port"]:
        unusual_ports = [item.get("name", "") for item in aggs["port"][:5] if item.get("name", "") not in {"80", "443"}]
        if unusual_ports:
            lines.append(f"- Non-default ports appear prominently: `{', '.join(unusual_ports)}`.")
        else:
            lines.append("- Distribution is dominated by standard web ports.")
    else:
        lines.append("- Port distribution data is not present in this query.")

    if distinct:
        lines.extend(["", "## Distinct Counts", ""])
        for key, value in distinct.items():
            lines.append(f"- `{key}`: `{value}`")

    for field_name, items in aggs.items():
        if not items:
            continue
        appendix_rows: List[List[str]] = []
        for item in items[:10]:
            appendix_rows.append(
                [
                    str(item.get("name", "")),
                    str(item.get("count", "")),
                    ", ".join(f"{region.get('name')}({region.get('count')})" for region in (item.get("regions", []) or [])[:3]),
                ]
            )
        lines.extend(["", f"## Top {field_name.upper()}", "", markdown_table(["Name", "Count", "Top Regions"], appendix_rows)])

    return "\n".join(lines).strip() + "\n"


def parse_nuclei_log(path: str | None) -> Dict[str, int] | None:
    if not path:
        return None
    file_path = Path(path).expanduser()
    if not file_path.exists():
        return None
    content = file_path.read_text(encoding="utf-8", errors="ignore").lower()
    return {
        "critical": content.count("[critical]"),
        "high": content.count("[high]"),
        "medium": content.count("[medium]"),
        "low": content.count("[low]"),
        "info": content.count("[info]"),
    }


def build_export_rows(result_objects: List[Dict[str, str]], fields_str: str, include_http_status: bool) -> tuple[List[str], List[List[str]]]:
    names = field_names(fields_str)
    headers = ["ID"] + [name.upper() for name in names]
    if include_http_status:
        headers.append("HTTP_STATUS")
    rows: List[List[str]] = []
    for index, item in enumerate(result_objects, start=1):
        row = [str(index)] + [item.get(name, "") for name in names]
        if include_http_status:
            row.append(item.get("http_status", ""))
        rows.append(row)
    return headers, rows


def build_query_sheet_name(index: int, query: str) -> str:
    return f"{index}_{slugify(query, fallback='query', limit=24)}"


def build_project_dir(project_name: str | None, outdir: str | None, seed_query: str) -> Path:
    if outdir:
        path = Path(outdir).expanduser()
        path.mkdir(parents=True, exist_ok=True)
        return path
    base_name = slugify(project_name or seed_query, fallback="fofa_task", limit=40)
    path = Path.cwd() / DEFAULT_RESULTS_DIR / f"{base_name}_{timestamp_slug()}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_targets_file(project_dir: Path, result_objects: List[Dict[str, str]], suffix: str) -> str:
    targets = ordered_unique(item.get("target", "") for item in result_objects if item.get("target"))
    path = project_dir / f"targets_{suffix}.txt"
    path.write_text("\n".join(targets), encoding="utf-8")
    return str(path)


def build_nuclei_command_file(project_dir: Path, suggestion: Dict[str, Any], suffix: str) -> str:
    path = project_dir / f"nuclei_command_{suffix}.txt"
    body = suggestion["command"] + "\n"
    if suggestion.get("reasons"):
        body += "\n# Rationale\n"
        for reason in suggestion["reasons"]:
            body += f"# - {reason}\n"
    return write_text_file(path, body)


def locate_nuclei_binary() -> str | None:
    found = shutil.which("nuclei")
    if found:
        return found
    cwd_candidate = Path.cwd() / "nuclei"
    if cwd_candidate.exists() and cwd_candidate.is_file():
        return str(cwd_candidate)
    exe_candidate = Path.cwd() / "nuclei.exe"
    if exe_candidate.exists() and exe_candidate.is_file():
        return str(exe_candidate)
    return None


def run_nuclei_scan(nuclei_path: str, targets_file: str, extra_args: str, output_file: str) -> Dict[str, Any]:
    cmd = [nuclei_path, "-l", targets_file, "-o", output_file, "-stats"] + shlex.split(extra_args or "")
    completed = subprocess.run(cmd, capture_output=True, text=True)
    summary = parse_nuclei_log(output_file)
    return {
        "ok": completed.returncode == 0 or Path(output_file).exists(),
        "command": " ".join(cmd),
        "returncode": completed.returncode,
        "stdout": completed.stdout[-2000:],
        "stderr": completed.stderr[-2000:],
        "output_file": output_file,
        "summary": summary,
    }


def run_nuclei_update(nuclei_path: str) -> Dict[str, Any]:
    commands = [
        [nuclei_path, "-update"],
        [nuclei_path, "-ut"],
    ]
    results: List[Dict[str, Any]] = []
    ok = True
    for cmd in commands:
        completed = subprocess.run(cmd, capture_output=True, text=True)
        results.append(
            {
                "command": " ".join(cmd),
                "returncode": completed.returncode,
                "stdout": completed.stdout[-2000:],
                "stderr": completed.stderr[-2000:],
            }
        )
        if completed.returncode != 0:
            ok = False
    return {"ok": ok, "steps": results}


def project_csv_union_headers(query_payloads: List[Dict[str, Any]], include_http_status: bool) -> List[str]:
    ordered_fields: List[str] = []
    for payload in query_payloads:
        for field in field_names(payload.get("used_fields", "")):
            if field not in ordered_fields:
                ordered_fields.append(field)
    headers = ["QUERY", "ID"] + [field.upper() for field in ordered_fields]
    if include_http_status:
        headers.append("HTTP_STATUS")
    return headers


def project_csv_rows(query_payloads: List[Dict[str, Any]], include_http_status: bool) -> List[List[str]]:
    ordered_fields: List[str] = []
    for payload in query_payloads:
        for field in field_names(payload.get("used_fields", "")):
            if field not in ordered_fields:
                ordered_fields.append(field)

    rows: List[List[str]] = []
    for payload in query_payloads:
        for index, item in enumerate(payload.get("result_objects", []), start=1):
            row = [payload.get("query", ""), str(index)]
            for field in ordered_fields:
                row.append(item.get(field, ""))
            if include_http_status:
                row.append(item.get("http_status", ""))
            rows.append(row)
    return rows


def handle_login(_: argparse.Namespace) -> None:
    data, permission_profile = fetch_account_profile()
    ok = not data.get("error")
    json_print(
        {
            "ok": ok,
            "mode": "login",
            "data": data,
            "permission_profile": permission_profile,
        },
        0 if ok else 1,
    )


def finalize_search_payload_outputs(
    args: argparse.Namespace,
    payload: Dict[str, Any],
    export_prefix: str,
    fallback_sheet_name: str,
) -> Dict[str, Any]:
    exported_to = None
    targets_written_to = None
    report_written_to = None
    nuclei_suggestion = None
    nuclei_command_file = None

    if args.output or args.export_format:
        export_headers, export_rows = build_export_rows(
            result_objects=payload["result_objects"],
            fields_str=payload["used_fields"],
            include_http_status=args.alive_check,
        )
        exported_to = write_export(
            output=args.output,
            export_format=args.export_format,
            prefix=export_prefix,
            headers=export_headers,
            rows=export_rows,
            sheet_name=args.sheet_name or fallback_sheet_name,
        )

    if args.targets_output:
        targets = ordered_unique(item.get("target", "") for item in payload["result_objects"] if item.get("target"))
        target_path = Path(args.targets_output).expanduser()
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text("\n".join(targets), encoding="utf-8")
        targets_written_to = str(target_path)

    if args.suggest_nuclei:
        nuclei_suggestion = detect_nuclei_suggestion(payload["result_objects"], user_intent=args.user_intent or args.query)
        if args.nuclei_command_output:
            nuclei_path = Path(args.nuclei_command_output).expanduser()
            nuclei_path.parent.mkdir(parents=True, exist_ok=True)
            nuclei_command_file = write_text_file(nuclei_path, nuclei_suggestion["command"] + "\n")

    if args.report_output:
        output_files: Dict[str, str] = {}
        if exported_to:
            output_files["export"] = exported_to
        if targets_written_to:
            output_files["targets"] = targets_written_to
        if nuclei_command_file:
            output_files["nuclei_command"] = nuclei_command_file
        report_text = build_asset_report(
            project_name=slugify(args.query, fallback=export_prefix),
            query_summaries=[payload],
            result_objects=payload["result_objects"],
            user_intent=args.user_intent or args.query,
            nuclei_suggestion=nuclei_suggestion,
            output_files=output_files,
            report_profile=args.report_profile,
        )
        report_written_to = write_text_file(Path(args.report_output).expanduser(), report_text)

    payload["exported_to"] = exported_to
    payload["targets_written_to"] = targets_written_to
    payload["report_written_to"] = report_written_to
    payload["report_profile"] = resolve_report_profile(
        args.report_profile,
        user_intent=args.user_intent or args.query,
        context_hint=args.query,
    )
    payload["nuclei_suggestion"] = nuclei_suggestion
    payload["nuclei_command_file"] = nuclei_command_file
    payload["learning_artifacts"] = record_learning_event("search-next" if payload.get("mode") == "search-next" else "search", payload)
    return payload


def handle_search(args: argparse.Namespace) -> None:
    login_data, permission_profile = fetch_account_profile()
    payload = search_query_workflow(
        query=args.query,
        requested_fields=args.fields,
        permission_profile=permission_profile,
        pages=args.pages,
        size=args.size,
        full=args.full,
        alive_check=args.alive_check,
        alive_timeout=args.alive_timeout,
        alive_concurrency=args.alive_concurrency,
        keyword=args.keyword,
        include_status=args.include_status,
        only_alive=args.only_alive,
    )
    payload["account_info"] = login_data
    payload["permission_profile"] = permission_profile
    if not payload["ok"]:
        payload["report_profile"] = resolve_report_profile(args.report_profile, user_intent=args.user_intent or args.query, context_hint=args.query)
        payload["learning_artifacts"] = record_learning_event("search", payload)
        json_print(payload, 1)

    payload = finalize_search_payload_outputs(
        args=args,
        payload=payload,
        export_prefix="fofa_search",
        fallback_sheet_name="FOFA Assets",
    )
    json_print(payload)


def handle_search_next(args: argparse.Namespace) -> None:
    login_data, permission_profile = fetch_account_profile()
    payload = search_next_workflow(
        query=args.query,
        requested_fields=args.fields,
        permission_profile=permission_profile,
        size=args.size,
        full=args.full,
        next_cursor=args.next_cursor,
        max_pages=args.max_pages,
        max_results=args.max_results,
        alive_check=args.alive_check,
        alive_timeout=args.alive_timeout,
        alive_concurrency=args.alive_concurrency,
        keyword=args.keyword,
        include_status=args.include_status,
        only_alive=args.only_alive,
    )
    payload["account_info"] = login_data
    payload["permission_profile"] = permission_profile
    if not payload["ok"]:
        payload["report_profile"] = resolve_report_profile(args.report_profile, user_intent=args.user_intent or args.query, context_hint=args.query)
        payload["learning_artifacts"] = record_learning_event("search-next", payload)
        json_print(payload, 1)

    payload = finalize_search_payload_outputs(
        args=args,
        payload=payload,
        export_prefix="fofa_search_next",
        fallback_sheet_name="FOFA Cursor Search",
    )
    json_print(payload)


def handle_host(args: argparse.Namespace) -> None:
    login_data, permission_profile = fetch_account_profile()
    if not permission_profile.get("can_use_host_api"):
        error_payload = {
            "ok": False,
            "mode": "host",
            "target": args.target,
            "error": "host aggregation API is not available for the current FOFA membership tier",
            "account_info": login_data,
            "permission_profile": permission_profile,
            "report_profile": resolve_report_profile(args.report_profile, user_intent=args.user_intent or "", context_hint=args.target),
        }
        error_payload["learning_artifacts"] = record_learning_event("host", error_payload)
        json_print(
            error_payload,
            1,
        )

    data = request_json(f"/api/v1/host/{urllib.parse.quote(args.target)}", {"detail": "true"})
    ok = not data.get("error")
    if not ok:
        error_payload = {
            "ok": False,
            "mode": "host",
            "target": args.target,
            "data": data,
            "account_info": login_data,
            "permission_profile": permission_profile,
            "report_profile": resolve_report_profile(args.report_profile, user_intent=args.user_intent or "", context_hint=args.target),
        }
        error_payload["learning_artifacts"] = record_learning_event("host", error_payload)
        json_print(
            error_payload,
            1,
        )

    host_profile = summarize_host_profile(args.target, data)
    report_written_to = None
    report_markdown = None
    if args.report_output:
        report_markdown = build_host_report(
            args.target,
            data,
            user_intent=args.user_intent or "",
            report_profile=args.report_profile,
        )
        report_written_to = write_text_file(Path(args.report_output).expanduser(), report_markdown)

    payload = {
        "ok": True,
        "mode": "host",
        "target": args.target,
        "data": data,
        "host_profile": host_profile,
        "account_info": login_data,
        "permission_profile": permission_profile,
        "report_profile": resolve_report_profile(args.report_profile, user_intent=args.user_intent or "", context_hint=args.target),
        "report_written_to": report_written_to,
        "report_markdown": report_markdown,
    }
    payload["learning_artifacts"] = record_learning_event("host", payload)
    json_print(payload)


def handle_stats(args: argparse.Namespace) -> None:
    login_data, permission_profile = fetch_account_profile()
    if not permission_profile.get("can_use_stats_api"):
        error_payload = {
            "ok": False,
            "mode": "stats",
            "query": args.query,
            "error": "stats aggregation API is not available for the current FOFA membership tier",
            "account_info": login_data,
            "permission_profile": permission_profile,
            "report_profile": resolve_report_profile(args.report_profile, user_intent=args.user_intent or "", context_hint=args.query),
        }
        error_payload["learning_artifacts"] = record_learning_event("stats", error_payload)
        json_print(
            error_payload,
            1,
        )

    field_resolution = resolve_requested_stats_fields(args.fields)
    query_b64 = base64.b64encode(args.query.encode("utf-8")).decode("ascii")
    data = request_json("/api/v1/search/stats", {"qbase64": query_b64, "fields": field_resolution["resolved_fields_csv"]})
    ok = not data.get("error")
    if not ok:
        error_payload = {
            "ok": False,
            "mode": "stats",
            "query": args.query,
            "fields": field_resolution["resolved_fields_csv"],
            "field_resolution": field_resolution,
            "data": data,
            "account_info": login_data,
            "permission_profile": permission_profile,
            "report_profile": resolve_report_profile(args.report_profile, user_intent=args.user_intent or "", context_hint=args.query),
        }
        error_payload["learning_artifacts"] = record_learning_event("stats", error_payload)
        json_print(
            error_payload,
            1,
        )

    report_written_to = None
    report_markdown = None
    stats_summary = summarize_stats_data(data)
    if args.report_output:
        report_markdown = build_stats_report(
            args.query,
            data,
            user_intent=args.user_intent or "",
            report_profile=args.report_profile,
        )
        report_written_to = write_text_file(Path(args.report_output).expanduser(), report_markdown)

    payload = {
        "ok": True,
        "mode": "stats",
        "query": args.query,
        "fields": field_resolution["resolved_fields_csv"],
        "field_resolution": field_resolution,
        "data": data,
        "stats_summary": stats_summary,
        "account_info": login_data,
        "permission_profile": permission_profile,
        "report_profile": resolve_report_profile(args.report_profile, user_intent=args.user_intent or "", context_hint=args.query),
        "report_written_to": report_written_to,
        "report_markdown": report_markdown,
    }
    payload["learning_artifacts"] = record_learning_event("stats", payload)
    json_print(payload)


def handle_alive_check(args: argparse.Namespace) -> None:
    targets: List[str] = []
    for item in args.target or []:
        targets.append(item.strip())
    if args.file:
        targets.extend(load_targets_from_file(args.file))
    targets = [target for target in targets if target]

    if not targets:
        json_print({"ok": False, "mode": "alive-check", "error": "no targets provided"}, 1)

    results = check_targets_alive(targets=targets, timeout=args.timeout, concurrency=args.concurrency)
    alive_count = sum(1 for result in results if is_alive_status(result["status"]))

    exported_to = None
    if args.output or args.export_format:
        rows = [
            [str(index), result["target"], result["url"], result["status"]]
            for index, result in enumerate(results, start=1)
        ]
        exported_to = write_export(
            output=args.output,
            export_format=args.export_format,
            prefix="fofa_alive",
            headers=["ID", "TARGET", "URL", "HTTP_STATUS"],
            rows=rows,
            sheet_name=args.sheet_name or "Alive Check",
        )

    json_print(
        {
            "ok": True,
            "mode": "alive-check",
            "target_count": len(targets),
            "alive_count": alive_count,
            "results": results,
            "exported_to": exported_to,
        }
    )


def handle_project_run(args: argparse.Namespace) -> None:
    login_data, permission_profile = fetch_account_profile()
    queries: List[str] = []
    for query in args.query or []:
        if query.strip():
            queries.append(query.strip())
    if args.query_file:
        queries.extend(load_targets_from_file(args.query_file))
    queries = [query for query in queries if query]

    if not queries:
        json_print({"ok": False, "mode": "project-run", "error": "no queries provided"}, 1)

    suffix = timestamp_slug()
    project_dir = build_project_dir(args.project_name, args.outdir, queries[0])
    query_payloads: List[Dict[str, Any]] = []
    per_query_exports: List[str] = []

    for index, query in enumerate(queries, start=1):
        payload = search_query_workflow(
            query=query,
            requested_fields=args.fields,
            permission_profile=permission_profile,
            pages=args.pages,
            size=args.size,
            full=args.full,
            alive_check=args.alive_check,
            alive_timeout=args.alive_timeout,
            alive_concurrency=args.alive_concurrency,
            keyword=args.keyword,
            include_status=args.include_status,
            only_alive=args.only_alive,
        )
        if not payload["ok"]:
            error_payload = {
                "ok": False,
                "mode": "project-run",
                "project_dir": str(project_dir),
                "failed_query": query,
                "error_payload": payload,
                "account_info": login_data,
                "permission_profile": permission_profile,
                "report_profile": resolve_report_profile(
                    args.report_profile,
                    user_intent=args.user_intent or " ; ".join(queries),
                    context_hint=project_dir.name,
                ),
                "error": str(payload.get("error") or payload.get("errmsg") or "project query failed"),
            }
            error_payload["learning_artifacts"] = record_learning_event("project-run", error_payload)
            json_print(
                error_payload,
                1,
            )

        if args.split_exports:
            headers, rows = build_export_rows(
                result_objects=payload["result_objects"],
                fields_str=payload["used_fields"],
                include_http_status=args.alive_check,
            )
            export_path = project_dir / f"query_{index}_{slugify(query, fallback='query', limit=30)}.{args.export_format}"
            per_query_exports.append(
                write_export(
                    output=str(export_path),
                    export_format=args.export_format,
                    prefix="query",
                    headers=headers,
                    rows=rows,
                    sheet_name=build_query_sheet_name(index, query),
                )
            )
        query_payloads.append(payload)

    merged_result_objects: List[Dict[str, str]] = []
    sheets: List[Dict[str, Any]] = []
    for index, payload in enumerate(query_payloads, start=1):
        headers, rows = build_export_rows(
            result_objects=payload["result_objects"],
            fields_str=payload["used_fields"],
            include_http_status=args.alive_check,
        )
        sheets.append(
            {
                "name": build_query_sheet_name(index, payload["query"]),
                "headers": headers,
                "rows": rows,
            }
        )
        for item in payload["result_objects"]:
            enriched = dict(item)
            enriched["source_query"] = payload["query"]
            merged_result_objects.append(enriched)

    merged_headers = project_csv_union_headers(query_payloads, include_http_status=args.alive_check)
    merged_rows = project_csv_rows(query_payloads, include_http_status=args.alive_check)
    merged_export_path = project_dir / f"batch_merge_{suffix}.{args.export_format}"
    merged_export = write_multi_export(
        output=str(merged_export_path),
        export_format=args.export_format,
        prefix="batch_merge",
        sheets=sheets,
        csv_headers=merged_headers,
        csv_rows=merged_rows,
    )

    targets_file = build_targets_file(project_dir, merged_result_objects, suffix)
    nuclei_suggestion = detect_nuclei_suggestion(
        merged_result_objects,
        user_intent=args.user_intent or " ; ".join(queries),
    )
    nuclei_command_file = build_nuclei_command_file(project_dir, nuclei_suggestion, suffix)
    nuclei_log_summary = parse_nuclei_log(args.nuclei_log)
    nuclei_run = None

    if args.run_nuclei:
        nuclei_path = locate_nuclei_binary()
        if not nuclei_path:
            json_print(
                {
                    "ok": False,
                    "mode": "project-run",
                    "project_dir": str(project_dir),
                    "error": "nuclei binary not found",
                },
                1,
            )
        nuclei_args = args.nuclei_args or nuclei_suggestion["args"]
        nuclei_output = str(project_dir / f"nuclei_result_{suffix}.txt")
        nuclei_run = run_nuclei_scan(
            nuclei_path=nuclei_path,
            targets_file=targets_file,
            extra_args=nuclei_args,
            output_file=nuclei_output,
        )
        if nuclei_run.get("summary"):
            nuclei_log_summary = nuclei_run["summary"]

    output_files = {
        "merged_export": merged_export,
        "targets": targets_file,
        "nuclei_command": nuclei_command_file,
    }
    if per_query_exports:
        output_files["per_query_exports"] = "\n".join(per_query_exports)
    if nuclei_run and nuclei_run.get("output_file"):
        output_files["nuclei_result"] = nuclei_run["output_file"]

    report_markdown = build_asset_report(
        project_name=project_dir.name,
        query_summaries=query_payloads,
        result_objects=merged_result_objects,
        user_intent=args.user_intent or " ; ".join(queries),
        nuclei_suggestion=nuclei_suggestion,
        output_files=output_files,
        nuclei_log_summary=nuclei_log_summary,
        report_profile=args.report_profile,
    )
    report_path = write_text_file(project_dir / f"report_{suffix}.md", report_markdown)

    payload = {
        "ok": True,
        "mode": "project-run",
        "project_dir": str(project_dir),
        "account_info": login_data,
        "permission_profile": permission_profile,
        "query_count": len(query_payloads),
        "total_result_count": len(merged_result_objects),
        "unique_target_count": len(unique_nonempty(item.get("target", "") for item in merged_result_objects)),
        "merged_export": merged_export,
        "per_query_exports": per_query_exports,
        "targets_file": targets_file,
        "report_file": report_path,
        "nuclei_command_file": nuclei_command_file,
        "nuclei_suggestion": nuclei_suggestion,
        "report_profile": resolve_report_profile(
            args.report_profile,
            user_intent=args.user_intent or " ; ".join(queries),
            context_hint=project_dir.name,
        ),
        "nuclei_run": nuclei_run,
        "queries": query_payloads,
    }
    payload["learning_artifacts"] = record_learning_event("project-run", payload, result_objects=merged_result_objects)
    json_print(payload)


def handle_monitor_run(args: argparse.Namespace) -> None:
    login_data, permission_profile = fetch_account_profile()
    queries: List[str] = []
    for query in args.query or []:
        if query.strip():
            queries.append(query.strip())
    if args.query_file:
        queries.extend(load_targets_from_file(args.query_file))
    queries = [query for query in queries if query]

    if not queries:
        json_print({"ok": False, "mode": "monitor-run", "error": "no queries provided"}, 1)

    suffix = timestamp_slug()
    state_dir = build_monitor_state_dir(args.project_name, args.state_dir, queries[0])
    snapshots_dir = state_dir / "snapshots"
    exports_dir = state_dir / "exports"
    diffs_dir = state_dir / "diffs"
    for path in (snapshots_dir, exports_dir, diffs_dir):
        path.mkdir(parents=True, exist_ok=True)

    previous_snapshot_path = state_dir / "latest_snapshot.json"
    previous_snapshot = read_json_file(previous_snapshot_path)
    previous_generated_at = str((previous_snapshot or {}).get("generated_at", ""))

    query_payloads: List[Dict[str, Any]] = []
    per_query_exports: List[str] = []

    for index, query in enumerate(queries, start=1):
        if args.use_search_next:
            payload = search_next_workflow(
                query=query,
                requested_fields=args.fields,
                permission_profile=permission_profile,
                size=args.size,
                full=args.full,
                next_cursor=args.next_cursor,
                max_pages=args.max_pages,
                max_results=args.max_results,
                alive_check=args.alive_check,
                alive_timeout=args.alive_timeout,
                alive_concurrency=args.alive_concurrency,
                keyword=args.keyword,
                include_status=args.include_status,
                only_alive=args.only_alive,
            )
        else:
            payload = search_query_workflow(
                query=query,
                requested_fields=args.fields,
                permission_profile=permission_profile,
                pages=args.pages,
                size=args.size,
                full=args.full,
                alive_check=args.alive_check,
                alive_timeout=args.alive_timeout,
                alive_concurrency=args.alive_concurrency,
                keyword=args.keyword,
                include_status=args.include_status,
                only_alive=args.only_alive,
            )

        if not payload["ok"]:
            error_payload = {
                "ok": False,
                "mode": "monitor-run",
                "state_dir": str(state_dir),
                "failed_query": query,
                "error_payload": payload,
                "account_info": login_data,
                "permission_profile": permission_profile,
                "report_profile": resolve_report_profile(
                    args.report_profile,
                    user_intent=args.user_intent or " ; ".join(queries),
                    context_hint=state_dir.name,
                ),
                "error": str(payload.get("error") or payload.get("errmsg") or "monitor query failed"),
            }
            error_payload["learning_artifacts"] = record_learning_event("monitor-run", error_payload)
            json_print(
                error_payload,
                1,
            )

        if args.split_exports:
            headers, rows = build_export_rows(
                result_objects=payload["result_objects"],
                fields_str=payload["used_fields"],
                include_http_status=args.alive_check,
            )
            export_path = exports_dir / f"current_query_{index}_{slugify(query, fallback='query', limit=30)}.{args.export_format}"
            per_query_exports.append(
                write_export(
                    output=str(export_path),
                    export_format=args.export_format,
                    prefix="current_query",
                    headers=headers,
                    rows=rows,
                    sheet_name=build_query_sheet_name(index, query),
                )
            )
        query_payloads.append(payload)

    merged_result_objects: List[Dict[str, str]] = []
    sheets: List[Dict[str, Any]] = []
    snapshot_queries: List[Dict[str, Any]] = []
    for index, payload in enumerate(query_payloads, start=1):
        headers, rows = build_export_rows(
            result_objects=payload["result_objects"],
            fields_str=payload["used_fields"],
            include_http_status=args.alive_check,
        )
        sheets.append(
            {
                "name": build_query_sheet_name(index, payload["query"]),
                "headers": headers,
                "rows": rows,
            }
        )
        snapshot_queries.append(
            {
                "query": payload["query"],
                "used_fields": payload.get("used_fields", ""),
                "result_count": payload.get("result_count", 0),
                "raw_result_count": payload.get("raw_result_count", 0),
                "field_resolution": payload.get("field_resolution"),
                "api_permission_fallback": payload.get("api_permission_fallback", False),
                "requested_next_cursor": payload.get("requested_next_cursor"),
                "next_cursor_to_resume": payload.get("next_cursor_to_resume"),
                "has_more": payload.get("has_more"),
                "cursor_trace": payload.get("cursor_trace"),
                "result_objects": payload.get("result_objects", []),
            }
        )
        for item in payload["result_objects"]:
            enriched = dict(item)
            enriched["source_query"] = payload["query"]
            merged_result_objects.append(enriched)

    merged_headers = project_csv_union_headers(query_payloads, include_http_status=args.alive_check)
    merged_rows = project_csv_rows(query_payloads, include_http_status=args.alive_check)
    merged_export = write_multi_export(
        output=str(exports_dir / f"current_assets_{suffix}.{args.export_format}"),
        export_format=args.export_format,
        prefix="current_assets",
        sheets=sheets,
        csv_headers=merged_headers,
        csv_rows=merged_rows,
    )

    targets_file = build_targets_file(state_dir, merged_result_objects, suffix)
    latest_targets_path = write_text_file(
        state_dir / "latest_targets.txt",
        "\n".join(ordered_unique(item.get("target", "") for item in merged_result_objects if item.get("target"))) + "\n",
    )

    nuclei_suggestion = detect_nuclei_suggestion(
        merged_result_objects,
        user_intent=args.user_intent or " ; ".join(queries),
    ) if args.suggest_nuclei else None
    nuclei_command_file = build_nuclei_command_file(state_dir, nuclei_suggestion, suffix) if nuclei_suggestion else None

    if previous_snapshot:
        diff_summary = compare_asset_inventory(
            previous_snapshot.get("merged_result_objects", []) or [],
            merged_result_objects,
        )
        query_diffs = compare_query_snapshots(previous_snapshot.get("queries", []) or [], snapshot_queries)
    else:
        baseline_summary = compare_asset_inventory([], merged_result_objects)
        diff_summary = {
            **baseline_summary,
            "baseline_established": True,
            "added_count": 0,
            "removed_count": 0,
            "changed_count": 0,
            "added_objects": [],
            "removed_objects": [],
            "changed_objects": [],
            "added_samples": [],
            "removed_samples": [],
            "changed_samples": [],
        }
        query_diffs = [
            {
                "query": item.get("query", ""),
                "previous_count": 0,
                "current_count": item.get("result_count", 0),
                "added_count": 0,
                "removed_count": 0,
                "changed_count": 0,
                "has_changes": False,
            }
            for item in snapshot_queries
        ]

    alert_summary = derive_monitor_alert(diff_summary)

    added_export = None
    removed_export = None
    changed_export = None
    if diff_summary.get("added_objects"):
        headers, rows = build_object_export_rows(diff_summary["added_objects"])
        added_export = write_export(
            output=str(diffs_dir / f"added_assets_{suffix}.{args.export_format}"),
            export_format=args.export_format,
            prefix="added_assets",
            headers=headers,
            rows=rows,
            sheet_name="Added Assets",
        )
    if diff_summary.get("removed_objects"):
        headers, rows = build_object_export_rows(diff_summary["removed_objects"])
        removed_export = write_export(
            output=str(diffs_dir / f"removed_assets_{suffix}.{args.export_format}"),
            export_format=args.export_format,
            prefix="removed_assets",
            headers=headers,
            rows=rows,
            sheet_name="Removed Assets",
        )
    if diff_summary.get("changed_objects"):
        headers, rows = build_changed_export_rows(diff_summary["changed_objects"])
        changed_export = write_export(
            output=str(diffs_dir / f"changed_assets_{suffix}.{args.export_format}"),
            export_format=args.export_format,
            prefix="changed_assets",
            headers=headers,
            rows=rows,
            sheet_name="Changed Assets",
        )

    snapshot_payload = {
        "generated_at": dt.datetime.now().isoformat(),
        "mode": "monitor-run",
        "project_name": state_dir.name,
        "query_mode": "search-next" if args.use_search_next else "search",
        "user_intent": args.user_intent or " ; ".join(queries),
        "alive_check": args.alive_check,
        "account_info": login_data,
        "permission_profile": permission_profile,
        "queries": snapshot_queries,
        "merged_result_objects": merged_result_objects,
    }
    snapshot_file = write_json_file(snapshots_dir / f"snapshot_{suffix}.json", snapshot_payload)
    latest_snapshot_file = write_json_file(previous_snapshot_path, snapshot_payload)

    diff_payload = {
        "generated_at": dt.datetime.now().isoformat(),
        "project_name": state_dir.name,
        "previous_generated_at": previous_generated_at or None,
        "query_mode": snapshot_payload["query_mode"],
        "alert_summary": alert_summary,
        "diff_summary": diff_summary,
        "query_diffs": query_diffs,
    }
    diff_file = write_json_file(diffs_dir / f"diff_{suffix}.json", diff_payload)
    latest_diff_file = write_json_file(state_dir / "latest_diff.json", diff_payload)

    output_files = {
        "current_export": merged_export,
        "latest_targets": latest_targets_path,
        "snapshot": snapshot_file,
        "latest_snapshot": latest_snapshot_file,
        "diff": diff_file,
        "latest_diff": latest_diff_file,
    }
    if per_query_exports:
        output_files["per_query_exports"] = "\n".join(per_query_exports)
    if added_export:
        output_files["added_export"] = added_export
    if removed_export:
        output_files["removed_export"] = removed_export
    if changed_export:
        output_files["changed_export"] = changed_export
    if nuclei_command_file:
        output_files["nuclei_command"] = nuclei_command_file

    report_markdown = build_monitor_report(
        project_name=state_dir.name,
        query_mode=snapshot_payload["query_mode"],
        query_summaries=query_payloads,
        current_objects=merged_result_objects,
        diff_summary=diff_summary,
        query_diffs=query_diffs,
        output_files=output_files,
        previous_generated_at=previous_generated_at,
        user_intent=args.user_intent or " ; ".join(queries),
        nuclei_suggestion=nuclei_suggestion,
        report_profile=args.report_profile,
    )
    report_file = write_text_file(state_dir / f"monitor_report_{suffix}.md", report_markdown)
    latest_report_file = write_text_file(state_dir / "latest_report.md", report_markdown)
    extra_report_file = None
    if args.report_output:
        extra_report_file = write_text_file(Path(args.report_output).expanduser(), report_markdown)

    payload = {
        "ok": True,
        "mode": "monitor-run",
        "state_dir": str(state_dir),
        "account_info": login_data,
        "permission_profile": permission_profile,
        "query_mode": snapshot_payload["query_mode"],
        "query_count": len(query_payloads),
        "total_result_count": len(merged_result_objects),
        "unique_target_count": len(unique_nonempty(item.get("target", "") for item in merged_result_objects)),
        "alert_summary": alert_summary,
        "diff_summary": {
            "previous_count": diff_summary.get("previous_count", 0),
            "current_count": diff_summary.get("current_count", 0),
            "added_count": diff_summary.get("added_count", 0),
            "removed_count": diff_summary.get("removed_count", 0),
            "changed_count": diff_summary.get("changed_count", 0),
            "baseline_established": diff_summary.get("baseline_established", False),
        },
        "query_diffs": query_diffs,
        "current_export": merged_export,
        "targets_file": targets_file,
        "latest_targets_file": latest_targets_path,
        "snapshot_file": snapshot_file,
        "latest_snapshot_file": latest_snapshot_file,
        "diff_file": diff_file,
        "latest_diff_file": latest_diff_file,
        "report_file": report_file,
        "latest_report_file": latest_report_file,
        "report_output_copy": extra_report_file,
        "per_query_exports": per_query_exports,
        "added_export": added_export,
        "removed_export": removed_export,
        "changed_export": changed_export,
        "nuclei_command_file": nuclei_command_file,
        "nuclei_suggestion": nuclei_suggestion,
        "report_profile": resolve_report_profile(
            args.report_profile,
            user_intent=args.user_intent or " ; ".join(queries),
            context_hint=state_dir.name,
        ),
        "queries": query_payloads,
    }
    payload["learning_artifacts"] = record_learning_event("monitor-run", payload, result_objects=merged_result_objects)
    exit_code = 2 if args.fail_on_change and alert_summary["alert"] else 0
    json_print(payload, exit_code)


def handle_nuclei_run(args: argparse.Namespace) -> None:
    nuclei_path = locate_nuclei_binary()
    if not nuclei_path:
        json_print({"ok": False, "mode": "nuclei-run", "error": "nuclei binary not found"}, 1)

    targets_file = args.targets_file
    temp_file = None
    if not targets_file:
        targets = [item.strip() for item in args.target or [] if item.strip()]
        if not targets:
            json_print({"ok": False, "mode": "nuclei-run", "error": "no targets provided"}, 1)
        temp_file = Path.cwd() / f"nuclei_targets_{timestamp_slug()}.txt"
        temp_file.write_text("\n".join(targets), encoding="utf-8")
        targets_file = str(temp_file)

    output = args.output or str(Path.cwd() / f"nuclei_result_{timestamp_slug()}.txt")
    payload = run_nuclei_scan(
        nuclei_path=nuclei_path,
        targets_file=targets_file,
        extra_args=args.args or "",
        output_file=output,
    )
    payload["mode"] = "nuclei-run"
    payload["targets_file"] = targets_file
    payload["temporary_targets_file"] = str(temp_file) if temp_file else None
    json_print(payload, 0 if payload["ok"] else 1)


def handle_nuclei_update(_: argparse.Namespace) -> None:
    nuclei_path = locate_nuclei_binary()
    if not nuclei_path:
        json_print({"ok": False, "mode": "nuclei-update", "error": "nuclei binary not found"}, 1)
    payload = run_nuclei_update(nuclei_path)
    payload["mode"] = "nuclei-update"
    payload["nuclei_path"] = nuclei_path
    json_print(payload, 0 if payload["ok"] else 1)


def handle_learn_review(args: argparse.Namespace) -> None:
    learning_dir = resolve_learning_dir(args.memory_dir)
    semantic_path = learning_dir / "semantic-patterns.json"
    runs_path = learning_dir / "runs.jsonl"
    semantic_memory = load_semantic_memory(semantic_path)
    recent_events = read_jsonl_tail(runs_path, limit=args.last)
    report_markdown = build_learning_review_markdown(semantic_memory, recent_events, learning_dir)
    latest_review = write_text_file(learning_dir / "latest_review.md", report_markdown)
    output_copy = None
    if args.output:
        output_copy = write_text_file(Path(args.output).expanduser(), report_markdown)

    top_patterns = [
        {
            "code": code,
            "count": count,
            "message": LEARNING_PATTERN_CATALOG.get(code, {}).get("message", code),
        }
        for code, count in top_counter_items(semantic_memory.get("pattern_counts", {}) or {}, limit=8)
    ]
    json_print(
        {
            "ok": True,
            "mode": "learn-review",
            "learning_dir": str(learning_dir),
            "semantic_memory_file": str(semantic_path),
            "runs_file": str(runs_path),
            "latest_review_file": latest_review,
            "output_copy": output_copy,
            "top_patterns": top_patterns,
            "recent_events": recent_events,
            "semantic_memory": semantic_memory,
            "report_markdown": report_markdown,
        }
    )


def rotl32(value: int, shift: int) -> int:
    value &= 0xFFFFFFFF
    return ((value << shift) & 0xFFFFFFFF) | (value >> (32 - shift))


def fmix32(value: int) -> int:
    value ^= value >> 16
    value = (value * 0x85EBCA6B) & 0xFFFFFFFF
    value ^= value >> 13
    value = (value * 0xC2B2AE35) & 0xFFFFFFFF
    value ^= value >> 16
    return value & 0xFFFFFFFF


def murmurhash3_x86_32(data: bytes, seed: int = 0) -> int:
    length = len(data)
    h1 = seed & 0xFFFFFFFF
    c1 = 0xCC9E2D51
    c2 = 0x1B873593
    rounded_end = length & 0xFFFFFFFC

    for index in range(0, rounded_end, 4):
        k1 = (
            data[index]
            | (data[index + 1] << 8)
            | (data[index + 2] << 16)
            | (data[index + 3] << 24)
        )
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = rotl32(k1, 15)
        k1 = (k1 * c2) & 0xFFFFFFFF
        h1 ^= k1
        h1 = rotl32(h1, 13)
        h1 = (h1 * 5 + 0xE6546B64) & 0xFFFFFFFF

    k1 = 0
    tail = length & 0x03
    if tail == 3:
        k1 ^= data[rounded_end + 2] << 16
    if tail >= 2:
        k1 ^= data[rounded_end + 1] << 8
    if tail >= 1:
        k1 ^= data[rounded_end]
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = rotl32(k1, 15)
        k1 = (k1 * c2) & 0xFFFFFFFF
        h1 ^= k1

    h1 ^= length
    h1 = fmix32(h1)
    if h1 & 0x80000000:
        return -((~h1 + 1) & 0xFFFFFFFF)
    return h1


def handle_icon_hash(args: argparse.Namespace) -> None:
    url = normalize_url(args.url)
    parsed = urllib.parse.urlparse(url)
    favicon_url = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, args.favicon_path, "", "", ""))
    context = ssl._create_unverified_context() if args.insecure else None

    request = urllib.request.Request(
        favicon_url,
        headers={"User-Agent": "fofamap-skill/2.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=15, context=context) as response:
            content = response.read()
    except Exception as exc:
        json_print(
            {
                "ok": False,
                "mode": "icon-hash",
                "url": url,
                "favicon_url": favicon_url,
                "error": str(exc),
            },
            1,
        )

    encoded = base64.encodebytes(content)
    icon_hash = murmurhash3_x86_32(encoded)
    json_print(
        {
            "ok": True,
            "mode": "icon-hash",
            "url": url,
            "favicon_url": favicon_url,
            "icon_hash": icon_hash,
            "fofa_query": f'icon_hash="{icon_hash}"',
        }
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FOFA helper for the fofamap skill")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    login = subparsers.add_parser("login", help="validate FOFA credentials and return the permission profile")
    login.set_defaults(func=handle_login)

    search = subparsers.add_parser("search", help="run a FOFA search query")
    search.add_argument("--query", required=True, help="FOFA query string")
    search.add_argument("--fields", help="comma-separated response fields; defaults to a tier-aware field set")
    search.add_argument("--pages", type=int, default=1, help="number of pages to fetch")
    search.add_argument("--size", type=int, default=100, help="page size, FOFA max is usually 10000")
    search.add_argument("--full", action="store_true", help="search historical data")
    search.add_argument("--keyword", help="comma-separated local keyword filter over returned rows")
    search.add_argument("--alive-check", action="store_true", help="probe returned web assets for live HTTP/HTTPS responses")
    search.add_argument("--alive-timeout", type=int, default=5, help="per-target timeout in seconds for alive checks")
    search.add_argument("--alive-concurrency", type=int, default=DEFAULT_ALIVE_CONCURRENCY, help="concurrency for alive checks")
    search.add_argument("--only-alive", action="store_true", help="keep only rows that return an HTTP status during alive checks")
    search.add_argument("--include-status", help="comma-separated HTTP statuses to keep after alive checks, e.g. 200,302,401")
    search.add_argument("--output", help="optional export path for csv/xlsx output")
    search.add_argument("--export-format", choices=["csv", "xlsx"], help="export format when writing a file")
    search.add_argument("--sheet-name", help="sheet name for xlsx export")
    search.add_argument("--targets-output", help="optional path to write a targets.txt handoff file")
    search.add_argument("--suggest-nuclei", action="store_true", help="include heuristic nuclei command suggestions")
    search.add_argument("--nuclei-command-output", help="optional path to write the suggested nuclei command")
    search.add_argument("--report-output", help="optional path to write a Markdown report")
    search.add_argument("--user-intent", help="optional original user intent to enrich suggestions and reports")
    search.add_argument("--report-profile", choices=REPORT_PROFILE_CHOICES, help="optional reporting lens such as attack-infrastructure, abnormal-exposure, or takeover-risk")
    search.set_defaults(func=handle_search)

    search_next = subparsers.add_parser("search-next", help="run FOFA continuous paging with the official next cursor API")
    search_next.add_argument("--query", required=True, help="FOFA query string")
    search_next.add_argument("--fields", help="comma-separated response fields; defaults to a tier-aware field set")
    search_next.add_argument(
        "--size",
        type=int,
        default=100,
        help="page size per cursor request; FOFA caps body queries at 500 and cert/banner queries at 2000",
    )
    search_next.add_argument("--full", action="store_true", help="search historical data")
    search_next.add_argument(
        "--next-cursor",
        default="auto",
        help="cursor token for /api/v1/search/next; leave as auto for the first request, and id is accepted as a compatibility sentinel",
    )
    search_next.add_argument("--max-pages", type=int, default=1, help="maximum number of cursor pages to fetch in this run")
    search_next.add_argument("--max-results", type=int, help="optional hard cap for collected rows across cursor pages")
    search_next.add_argument("--keyword", help="comma-separated local keyword filter over returned rows")
    search_next.add_argument("--alive-check", action="store_true", help="probe returned web assets for live HTTP/HTTPS responses")
    search_next.add_argument("--alive-timeout", type=int, default=5, help="per-target timeout in seconds for alive checks")
    search_next.add_argument("--alive-concurrency", type=int, default=DEFAULT_ALIVE_CONCURRENCY, help="concurrency for alive checks")
    search_next.add_argument("--only-alive", action="store_true", help="keep only rows that return an HTTP status during alive checks")
    search_next.add_argument("--include-status", help="comma-separated HTTP statuses to keep after alive checks, e.g. 200,302,401")
    search_next.add_argument("--output", help="optional export path for csv/xlsx output")
    search_next.add_argument("--export-format", choices=["csv", "xlsx"], help="export format when writing a file")
    search_next.add_argument("--sheet-name", help="sheet name for xlsx export")
    search_next.add_argument("--targets-output", help="optional path to write a targets.txt handoff file")
    search_next.add_argument("--suggest-nuclei", action="store_true", help="include heuristic nuclei command suggestions")
    search_next.add_argument("--nuclei-command-output", help="optional path to write the suggested nuclei command")
    search_next.add_argument("--report-output", help="optional path to write a Markdown report")
    search_next.add_argument("--user-intent", help="optional original user intent to enrich suggestions and reports")
    search_next.add_argument("--report-profile", choices=REPORT_PROFILE_CHOICES, help="optional reporting lens such as attack-infrastructure, abnormal-exposure, or takeover-risk")
    search_next.set_defaults(func=handle_search_next)

    host = subparsers.add_parser("host", help="query one host aggregation record")
    host.add_argument("--target", required=True, help="single IP or domain")
    host.add_argument("--report-output", help="optional path to write a Markdown host report")
    host.add_argument("--user-intent", help="optional original user intent")
    host.add_argument("--report-profile", choices=REPORT_PROFILE_CHOICES, help="optional reporting lens such as attack-infrastructure, abnormal-exposure, or takeover-risk")
    host.set_defaults(func=handle_host)

    stats = subparsers.add_parser("stats", help="run a FOFA stats aggregation")
    stats.add_argument("--query", required=True, help="FOFA query string")
    stats.add_argument("--fields", help="comma-separated stats fields; defaults to country,title,org")
    stats.add_argument("--report-output", help="optional path to write a Markdown stats report")
    stats.add_argument("--user-intent", help="optional original user intent")
    stats.add_argument("--report-profile", choices=REPORT_PROFILE_CHOICES, help="optional reporting lens such as attack-infrastructure, abnormal-exposure, or takeover-risk")
    stats.set_defaults(func=handle_stats)

    alive = subparsers.add_parser("alive-check", help="probe targets for HTTP/HTTPS liveness")
    alive.add_argument("--target", action="append", help="target URL, host, or host:port; repeat for multiple targets")
    alive.add_argument("--file", help="optional file containing one target per line")
    alive.add_argument("--timeout", type=int, default=5, help="per-target timeout in seconds")
    alive.add_argument("--concurrency", type=int, default=DEFAULT_ALIVE_CONCURRENCY, help="concurrency for live checks")
    alive.add_argument("--output", help="optional export path for csv/xlsx output")
    alive.add_argument("--export-format", choices=["csv", "xlsx"], help="export format when writing a file")
    alive.add_argument("--sheet-name", help="sheet name for xlsx export")
    alive.set_defaults(func=handle_alive_check)

    monitor = subparsers.add_parser("monitor-run", help="run a scheduler-friendly asset monitoring workflow with snapshot diffing")
    monitor.add_argument("--query", action="append", help="FOFA query string; repeat for multiple queries")
    monitor.add_argument("--query-file", help="optional file containing one FOFA query per line")
    monitor.add_argument("--fields", help="comma-separated response fields; defaults to a tier-aware field set")
    monitor.add_argument("--pages", type=int, default=1, help="number of pages to fetch when using ordinary search mode")
    monitor.add_argument(
        "--size",
        type=int,
        default=100,
        help="page size; FOFA caps search-next body queries at 500 and cert/banner queries at 2000",
    )
    monitor.add_argument("--full", action="store_true", help="search historical data")
    monitor.add_argument("--use-search-next", action="store_true", help="use the official continuous paging cursor API")
    monitor.add_argument(
        "--next-cursor",
        default="auto",
        help="starting cursor for search-next mode; auto is recommended for the first run",
    )
    monitor.add_argument("--max-pages", type=int, default=1, help="maximum cursor pages when --use-search-next is set")
    monitor.add_argument("--max-results", type=int, help="optional hard cap for collected rows in search-next mode")
    monitor.add_argument("--keyword", help="comma-separated local keyword filter over returned rows")
    monitor.add_argument("--alive-check", action="store_true", help="probe returned web assets for live HTTP/HTTPS responses")
    monitor.add_argument("--alive-timeout", type=int, default=5, help="per-target timeout in seconds for alive checks")
    monitor.add_argument("--alive-concurrency", type=int, default=DEFAULT_ALIVE_CONCURRENCY, help="concurrency for live checks")
    monitor.add_argument("--only-alive", action="store_true", help="keep only rows that return an HTTP status during alive checks")
    monitor.add_argument("--include-status", help="comma-separated HTTP statuses to keep after alive checks")
    monitor.add_argument("--project-name", help="optional monitoring profile name")
    monitor.add_argument("--state-dir", help="persistent state directory for snapshots, diffs, reports, and exports")
    monitor.add_argument("--export-format", choices=["csv", "xlsx"], default="xlsx", help="export format for monitoring outputs")
    monitor.add_argument("--split-exports", action="store_true", help="also export one current result file per query")
    monitor.add_argument("--suggest-nuclei", action="store_true", help="include heuristic nuclei command suggestions in the report")
    monitor.add_argument("--report-output", help="optional extra path to write a Markdown monitoring report copy")
    monitor.add_argument("--user-intent", help="optional original user intent to enrich reports and recommendations")
    monitor.add_argument("--report-profile", choices=REPORT_PROFILE_CHOICES, help="optional reporting lens such as attack-infrastructure, abnormal-exposure, or takeover-risk")
    monitor.add_argument("--fail-on-change", action="store_true", help="exit with code 2 when the comparison detects inventory drift")
    monitor.set_defaults(func=handle_monitor_run)

    project = subparsers.add_parser("project-run", help="run one or more FOFA queries as a project workflow")
    project.add_argument("--query", action="append", help="FOFA query string; repeat for multiple queries")
    project.add_argument("--query-file", help="optional file containing one FOFA query per line")
    project.add_argument("--fields", help="comma-separated response fields; defaults to a tier-aware field set")
    project.add_argument("--pages", type=int, default=1, help="number of pages to fetch for each query")
    project.add_argument("--size", type=int, default=100, help="page size for each FOFA request")
    project.add_argument("--full", action="store_true", help="search historical data")
    project.add_argument("--keyword", help="comma-separated local keyword filter over returned rows")
    project.add_argument("--alive-check", action="store_true", help="probe returned web assets for live HTTP/HTTPS responses")
    project.add_argument("--alive-timeout", type=int, default=5, help="per-target timeout in seconds for alive checks")
    project.add_argument("--alive-concurrency", type=int, default=DEFAULT_ALIVE_CONCURRENCY, help="concurrency for alive checks")
    project.add_argument("--only-alive", action="store_true", help="keep only rows that return an HTTP status during alive checks")
    project.add_argument("--include-status", help="comma-separated HTTP statuses to keep after alive checks")
    project.add_argument("--project-name", help="optional project name used in the output directory name")
    project.add_argument("--outdir", help="optional explicit project output directory")
    project.add_argument("--export-format", choices=["csv", "xlsx"], default="xlsx", help="export format for project outputs")
    project.add_argument("--split-exports", action="store_true", help="also export each query as its own file inside the project directory")
    project.add_argument("--user-intent", help="optional original user intent to enrich the report and nuclei suggestion")
    project.add_argument("--nuclei-log", help="optional existing nuclei log to fold into the project report")
    project.add_argument("--run-nuclei", action="store_true", help="run nuclei against the generated targets.txt using the suggested or provided args")
    project.add_argument("--nuclei-args", help="explicit nuclei arguments to use when --run-nuclei is set")
    project.add_argument("--report-profile", choices=REPORT_PROFILE_CHOICES, help="optional reporting lens such as attack-infrastructure, abnormal-exposure, or takeover-risk")
    project.set_defaults(func=handle_project_run)

    nuclei_run = subparsers.add_parser("nuclei-run", help="run nuclei against a targets file or explicit targets")
    nuclei_run.add_argument("--targets-file", help="path to an existing targets file")
    nuclei_run.add_argument("--target", action="append", help="single target; repeat for multiple entries when not using --targets-file")
    nuclei_run.add_argument("--args", help="extra nuclei arguments such as '-tags grafana -severity critical,high'")
    nuclei_run.add_argument("--output", help="result log path")
    nuclei_run.set_defaults(func=handle_nuclei_run)

    nuclei_update = subparsers.add_parser("nuclei-update", help="run nuclei template and binary update steps")
    nuclei_update.set_defaults(func=handle_nuclei_update)

    learn_review = subparsers.add_parser("learn-review", help="review fofamap's local memory, reflections, and evolving playbook hints")
    learn_review.add_argument("--memory-dir", help="optional explicit memory directory; defaults to results/fofamap_memory")
    learn_review.add_argument("--last", type=int, default=10, help="number of recent episodes to include in the review")
    learn_review.add_argument("--output", help="optional extra path to write the review Markdown")
    learn_review.set_defaults(func=handle_learn_review)

    icon_hash = subparsers.add_parser("icon-hash", help="calculate a FOFA icon hash query")
    icon_hash.add_argument("--url", required=True, help="target URL or host")
    icon_hash.add_argument("--favicon-path", default="/favicon.ico", help="favicon path")
    icon_hash.add_argument("--insecure", action="store_true", help="skip TLS verification for favicon fetch")
    icon_hash.set_defaults(func=handle_icon_hash)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
