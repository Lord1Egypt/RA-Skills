#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小递查查批量快递查询客户端
Xiaodicha (xdccy.com) Batch Express Tracking Client

针对「批量单号查询」场景优化：
  - 并发查询（文档声明无频率限制，默认并发 5）
  - 支持文件 / 内联 / 手机号映射表三种输入
  - 顺丰、中通按单号匹配手机号后四位
  - 聚合统计：状态分布、超时单量、签收时效
  - 多格式导出：JSON（原始）/ CSV（扁平）/ TXT（可读报告）

签名规则（严格遵循官方文档 §2.2.2）：
  原始RequestData(JSON) + APIKey → MD5(hex) → Base64(hex字符串) → URL(UTF-8)编码

零三方依赖，仅使用 Python 标准库。
"""

import argparse
import base64
import csv
import hashlib
import io
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional, Tuple

API_URL = "https://api.xdccy.com/IsvApi/GetXdccTrackInfoV2"
DEFAULT_TIMEOUT = 8          # 秒（文档：请求超时 8000ms）
DEFAULT_CONCURRENCY = 5      # 并发数（文档声明无频率限制）
MAX_CONCURRENCY = 20

# 需要手机号后四位的快递公司（文档 §4：顺丰、中通必填 Tel）
TEL_REQUIRED = {"SF", "ZTO", "STO", "YTO", "HTKY", "YD", "ZJS", "EMS"}  # 常见；顺丰/中通为核心

# 单号字母前缀 → (公司编码, 中文名)
# 纯数字单号没有可靠的前缀规律可依，一律不推断，避免误判。
PREFIX_TO_CODE = {
    "SF": ("SF", "顺丰速运"),
    "ZTO": ("ZTO", "中通快递"),
    "ZTOEXPRESS": ("ZTO", "中通快递"),
    "STO": ("STO", "申通快递"),
    "YTO": ("YTO", "圆通速递"),
    "YT": ("YTO", "圆通速递"),       # 圆通常见单号前缀（字母排序更长者优先匹配）
    "YD": ("YD", "韵达速递"),
    "HTKY": ("HTKY", "百世快递"),
    "ZJS": ("ZJS", "极兔速递"),
    "JT": ("ZJS", "极兔速递"),       # J&T 极兔前缀
    "EMS": ("EMS", "邮政 EMS"),
}

CODE_NAMES = {code: name for code, (_, name) in PREFIX_TO_CODE.items()}

# 状态归类关键词（文档仅确认 State=3 已签收，其余按 StateDesc 文本归类）
STATE_MAP = [
    ("已签收", ("签收",)),
    ("派送中", ("派送", "派件", "投递", "派达")),
    ("运输中", ("运输", "转运", "在途", "发往", "到达", "出发", "干线", "已揽收", "揽收")),
    ("已揽收", ("已揽收", "揽收")),
    ("疑难/异常", ("疑难", "异常", "退", "拒", "滞留", "问题")),
]

EXIT_OK = 0
EXIT_BAD_ARGS = 2
EXIT_PARTIAL = 1            # 部分失败仍产出结果


# --------------------------------------------------------------------------- #
# 签名 & 请求
# --------------------------------------------------------------------------- #
def generate_data_sign(request_data: str, api_key: str) -> str:
    """生成 DataSign。

    步骤：原始RequestData + APIKey → MD5(hex) → Base64(hex字符串) → URL(UTF-8)编码。
    文档示例：
      raw  = "{'MemberID':'123','Tel':'8789','No':'118954907573','ReturnFormat':'JSON'}"
      key  = "66da2cf8-c8a2-14b2-b6fa-176cd7d1ba18"
      MD5  = "42e8b3d72bc5036697443df68362f8ba"
      B64  = "NDJlOGIzZDcyYmM1MDM2Njk3NDQzZGY2ODM2MmY4YmE="
      Sign = "NDJlOGIzZDcyYmM1MDM2Njk3NDQzZGY2ODM2MmY4YmE%3d"
    """
    raw = request_data + api_key
    md5_hex = hashlib.md5(raw.encode("utf-8")).hexdigest()
    b64 = base64.b64encode(md5_hex.encode("utf-8")).decode("utf-8")
    encoded = urllib.parse.quote(b64, safe="")
    # 仅把百分号编码转小写（与文档示例 %3d 一致），保留 Base64 原有大小写
    return re.sub(r"%[0-9A-F]{2}", lambda m: m.group(0).lower(), encoded)


def build_request_data(member_id: str, no: str, tel: str = "",
                       return_format: str = "JSON") -> str:
    """构造未 URL 编码的 RequestData JSON 字符串。"""
    payload = {
        "MemberID": member_id,
        "Tel": tel,
        "No": no,
        "ReturnFormat": return_format,
    }
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def query_track(platform_id: str, api_key: str, member_id: str,
                tracking_no: str, tel: str = "",
                timeout: int = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    """查询单个运单号的物流轨迹，返回完整响应 dict（含 Code/Message/Data）。"""
    request_data_raw = build_request_data(member_id, tracking_no, tel)
    data_sign = generate_data_sign(request_data_raw, api_key)
    encoded_data = urllib.parse.quote(request_data_raw, safe="")

    body = (
        f"PlatformID={urllib.parse.quote(platform_id, safe='')}"
        f"&RequestData={encoded_data}"
        f"&DataSign={data_sign}"
    ).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return {"Code": e.code, "Message": f"HTTP错误: {e.reason}", "Data": None}
    except urllib.error.URLError as e:
        return {"Code": -1, "Message": f"网络错误: {e.reason}", "Data": None}
    except Exception as e:  # noqa: BLE001
        return {"Code": -2, "Message": f"请求异常: {e}", "Data": None}

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"Code": -3, "Message": "响应非JSON", "Data": raw}


# --------------------------------------------------------------------------- #
# 响应解析
# --------------------------------------------------------------------------- #
TIMEOUT_FIELDS = {
    "Pickup_TimeOut": "揽收超时",
    "FirstIssue_TimeOut": "首次发出超时",
    "FirstArrival_TimeOut": "首次到达转运超时",
    "LeaveDistributionCenter_TimeOut": "离开转运超时",
    "HalfwayStagnation_TimeOut": "中途停滞超时",
    "Dispatch_TimeOut": "派件超时",
    "SignFor_TimeOut": "签收超时",
}
SPAN_FIELDS = {
    "FirstIssue_TimeSpan": "揽收→发出",
    "FirstArrival_TimeSpan": "揽收→到达转运",
    "LeaveDistributionCenter_TimeSpan": "揽收→离开转运",
    "HalfwayStagnation_TimeSpan": "中途停滞",
    "Dispatch_TimeSpan": "揽收→开始派件",
    "SignFor_TimeSpan": "揽收→签收",
}


def classify_state(state_desc: Optional[str]) -> str:
    """根据 StateDesc 文本归类到可读状态。"""
    if not state_desc:
        return "未知"
    s = str(state_desc)
    for label, kws in STATE_MAP:
        if any(kw in s for kw in kws):
            return label
    return "其他"


def summarize(data: Dict[str, Any]) -> Dict[str, Any]:
    """把 Data 节点提炼成对用户友好的摘要。"""
    if not data:
        return {}

    timeouts = [
        {"field": f, "label": label, "value": data.get(f, 0)}
        for f, label in TIMEOUT_FIELDS.items()
    ]
    timeouts = [t for t in timeouts if t["value"] == 1]

    spans = []
    for f, label in SPAN_FIELDS.items():
        v = data.get(f)
        if v is not None:
            minutes = float(v)
            spans.append({
                "field": f,
                "label": label,
                "minutes": minutes,
                "human": _humanize_minutes(minutes),
            })

    traces = data.get("TraceList") or []
    latest_traces = traces[:3]  # 倒序：最新在前

    return {
        "shipper": data.get("ExpressName"),
        "shipper_code": data.get("ShipperCode"),
        "logistic_code": data.get("LogisticCode"),
        "state_code": data.get("State"),
        "state_desc": data.get("StateDesc"),
        "state_label": classify_state(data.get("StateDesc")),
        "note": data.get("message") or data.get("result"),
        "pickup_city": data.get("Pickup_City"),
        "delivery_city": data.get("Delivery_City"),
        "pickup_courier": data.get("Pickup_Courier"),
        "delivery_courier": data.get("Delivery_Courier"),
        "delivery_courier_phone": data.get("Delivery_Courier_Phone"),
        "first_arrival": data.get("FirstArrival_Name"),
        "pickup_time": data.get("Pickup_Time"),
        "dispatch_time": data.get("Dispatch_Time"),
        "signfor_time": data.get("SignFor_Time"),
        "trace_count": data.get("Count"),
        "last_trace": data.get("LastTrace"),
        "latest_traces": latest_traces,
        "timeouts": timeouts,
        "spans": spans,
    }


def _humanize_minutes(minutes: float) -> str:
    """分钟数转可读字符串：65 → '1小时5分钟'；2880 → '2天0小时'。"""
    m = int(minutes)
    if m < 60:
        return f"{m}分钟"
    days, rem = divmod(m, 1440)
    hours, rem = divmod(rem, 60)
    if days > 0:
        return f"{days}天{hours}小时"
    return f"{hours}小时{rem}分钟"


def format_text(summary: Dict[str, Any]) -> str:
    """把摘要渲染成对用户友好的多行文本。"""
    if not summary:
        return "(空)"
    lines = []
    lines.append(f"【{summary.get('shipper', '?')}】 {summary.get('logistic_code', '?')}")
    if summary.get("state_desc"):
        lines.append(f"状态：{summary['state_desc']}（{summary.get('state_label', '?')}）")
    else:
        lines.append(f"状态：{summary.get('state_label', '未知')}")
        if summary.get("note"):
            lines.append(f"说明：{summary['note']}")
    if summary.get("pickup_city") and summary.get("delivery_city"):
        lines.append(f"路线：{summary['pickup_city']} → {summary['delivery_city']}")
    if summary.get("pickup_time"):
        lines.append(f"揽收：{summary['pickup_time']}")
    if summary.get("dispatch_time"):
        lines.append(f"派件：{summary['dispatch_time']}")
    if summary.get("signfor_time"):
        lines.append(f"签收：{summary['signfor_time']}")
    if summary.get("delivery_courier"):
        courier = summary["delivery_courier"]
        phone = summary.get("delivery_courier_phone") or ""
        lines.append(f"派送员：{courier} {phone}".rstrip())
    if summary.get("spans"):
        lines.append("\n时效：")
        for s in summary["spans"]:
            lines.append(f"  · {s.get('label','')}：{s.get('human','')}（{s.get('minutes',0):.0f}分钟）")
    if summary.get("timeouts"):
        lines.append("\n⚠️ 超时标记：")
        for t in summary["timeouts"]:
            lines.append(f"  · {t['label']}")
    if summary.get("latest_traces"):
        lines.append("\n最新轨迹：")
        for tr in summary["latest_traces"]:
            lines.append(f"  [{tr.get('time')}] {tr.get('desc')}")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# 输入解析
# --------------------------------------------------------------------------- #
def parse_input(args) -> List[Tuple[str, str]]:
    """把用户输入解析为 [(no, tel), ...] 列表。

    来源优先级：
      1. --file 每行 "NO" 或 "NO,TEL"
      2. --nos "no1,no2,no3"
      3. --telmap csv(no,tel)
    最终 --tel 作为全局默认补充。
    """
    items: List[Tuple[str, str]] = []
    seen = set()

    def add(no: str, tel: str = ""):
        no = (no or "").strip()
        if not no:
            return
        key = no
        if key in seen:
            return  # 去重
        seen.add(key)
        items.append((no, tel.strip()))

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = [p.strip() for p in line.split(",")]
                add(parts[0], parts[1] if len(parts) > 1 else "")

    if args.telmap:
        with open(args.telmap, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                no = (row.get("no") or row.get("No") or row.get("运单号") or "").strip()
                tel = (row.get("tel") or row.get("Tel") or row.get("手机后四位") or "").strip()
                add(no, tel)

    if args.nos:
        for no in re.split(r"[,\s]+", args.nos.strip()):
            add(no)

    # 全局默认 tel
    if args.tel:
        items = [(no, tel or args.tel) for no, tel in items]

    return items


# --------------------------------------------------------------------------- #
# 手机号后四位（Tel）缺失检查
# --------------------------------------------------------------------------- #
def guess_shipper_code(no: str) -> str:
    """按单号字母前缀推断快递公司编码；无法识别时返回空串。"""
    s = (no or "").strip().upper()
    if not s:
        return ""
    for prefix in sorted(PREFIX_TO_CODE, key=len, reverse=True):
        if s.startswith(prefix):
            return PREFIX_TO_CODE[prefix][0]
    return ""


def find_missing_tel(items: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """找出「API 强制要求 Tel」却未提供手机后四位的单号。

    返回 [(单号, 公司编码), ...]，按输入顺序；纯数字单号无法推断公司，不计入。
    """
    missing = []
    for no, tel in items:
        if tel:
            continue
        code = guess_shipper_code(no)
        if code in TEL_REQUIRED:
            missing.append((no, code))
    return missing


def warn_missing_tel(items: List[Tuple[str, str]], limit: int = 5) -> str:
    """生成缺 Tel 预警文案。批量场景下只列前 limit 条 + 计数，避免刷屏。"""
    missing = find_missing_tel(items)
    if not missing:
        return ""
    lines = [
        f"\n⚠️ 有 {len(missing)} 个单号未提供手机号后四位，"
        f"这类公司（顺丰、中通、申通、圆通、韵达、百世、极兔、EMS）查询必须传 Tel，"
        f"否则接口会返回 400 查不到：",
    ]
    for no, code in missing[:limit]:
        lines.append(f"  · {no}（{CODE_NAMES.get(code, code)}）")
    if len(missing) > limit:
        lines.append(f"  …另有 {len(missing) - limit} 个，建议用 --tel 统一补或提供 --telmap 映射表")
    lines.append("补充方式：单号后加逗号与后四位（如 SF123,9378），或 --tel 统一补。")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# 批量查询（并发）
# --------------------------------------------------------------------------- #
def _worker(no_tel: Tuple[str, str], ctx: Dict[str, Any]) -> Dict[str, Any]:
    no, tel = no_tel
    resp = query_track(
        ctx["platform_id"], ctx["api_key"], ctx["member_id"],
        no, tel, ctx["timeout"],
    )
    ok = resp.get("Code") == 200 and bool(resp.get("Data"))
    summary = summarize(resp["Data"]) if ok else {}
    return {
        "no": no,
        "tel": tel,
        "ok": ok,
        "code": resp.get("Code"),
        "message": resp.get("Message"),
        "response": resp,
        "summary": summary,
    }


def batch_query(platform_id: str, api_key: str, member_id: str,
                items: List[Tuple[str, str]],
                concurrency: int = DEFAULT_CONCURRENCY,
                timeout: int = DEFAULT_TIMEOUT,
                progress: bool = True) -> List[Dict[str, Any]]:
    """并发批量查询。返回结果列表（顺序与输入一致）。"""
    ctx = {
        "platform_id": platform_id,
        "api_key": api_key,
        "member_id": member_id,
        "timeout": timeout,
    }
    results: List[Optional[Dict[str, Any]]] = [None] * len(items)
    done = 0
    total = len(items)

    with ThreadPoolExecutor(max_workers=max(1, min(concurrency, MAX_CONCURRENCY))) as ex:
        future_to_idx = {ex.submit(_worker, it, ctx): i for i, it in enumerate(items)}
        for fut in as_completed(future_to_idx):
            idx = future_to_idx[fut]
            try:
                results[idx] = fut.result()
            except Exception as e:  # noqa: BLE001
                no, tel = items[idx]
                results[idx] = {
                    "no": no, "tel": tel, "ok": False,
                    "code": -2, "message": f"异常: {e}", "response": {}, "summary": {},
                }
            done += 1
            if progress:
                sys.stderr.write(f"\r进度: {done}/{total}")
                sys.stderr.flush()

    if progress and total:
        sys.stderr.write("\n")
        sys.stderr.flush()

    return [r for r in results if r is not None]


# --------------------------------------------------------------------------- #
# 聚合统计
# --------------------------------------------------------------------------- #
def build_aggregate(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(results)
    ok = [r for r in results if r["ok"]]
    failed = [r for r in results if not r["ok"]]

    state_dist: Dict[str, int] = {}
    shipper_dist: Dict[str, int] = {}
    timeout_count = 0
    signfor_spans: List[float] = []

    for r in ok:
        s = r["summary"]
        label = s.get("state_label", "未知")
        state_dist[label] = state_dist.get(label, 0) + 1
        shipper = s.get("shipper") or "未知"
        shipper_dist[shipper] = shipper_dist.get(shipper, 0) + 1
        if s.get("timeouts"):
            timeout_count += 1
        # 仅统计「已签收」单的签收时效，避免未签收单的 0/空值拉低均值
        if s.get("state_label") == "已签收":
            for sp in s.get("spans", []):
                if sp["field"] == "SignFor_TimeSpan":
                    signfor_spans.append(sp["minutes"])

    signed = state_dist.get("已签收", 0)
    avg_signfor = (sum(signfor_spans) / len(signfor_spans)) if signfor_spans else None
    max_signfor = max(signfor_spans) if signfor_spans else None

    return {
        "total": total,
        "success": len(ok),
        "failed": len(failed),
        "state_dist": state_dist,
        "shipper_dist": shipper_dist,
        "timeout_count": timeout_count,
        "signed": signed,
        "avg_signfor_minutes": avg_signfor,
        "max_signfor_minutes": max_signfor,
        "failed_list": [{"no": r["no"], "code": r["code"], "message": r["message"]} for r in failed],
    }


def format_aggregate(agg: Dict[str, Any]) -> str:
    lines = []
    lines.append("【批量查询汇总】")
    lines.append(f"总单量：{agg['total']}　成功：{agg['success']}　失败：{agg['failed']}")
    lines.append(f"已签收：{agg['signed']}　超时单量：{agg['timeout_count']}")
    if agg["avg_signfor_minutes"] is not None:
        lines.append(f"签收时效（已签收）：平均 {_humanize_minutes(agg['avg_signfor_minutes'])}，"
                     f"最长 {_humanize_minutes(agg['max_signfor_minutes'])}")
    if agg["state_dist"]:
        lines.append("\n状态分布：")
        for k, v in sorted(agg["state_dist"].items(), key=lambda x: -x[1]):
            lines.append(f"  · {k}：{v}")
    if agg["shipper_dist"]:
        lines.append("\n快递公司分布：")
        for k, v in sorted(agg["shipper_dist"].items(), key=lambda x: -x[1]):
            lines.append(f"  · {k}：{v}")
    if agg["failed_list"]:
        lines.append("\n失败单号：")
        for f in agg["failed_list"]:
            lines.append(f"  · {f['no']}（Code={f['code']}）{f['message']}")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# 导出
# --------------------------------------------------------------------------- #
CSV_COLUMNS = [
    "No", "ExpressName", "StateDesc", "StateLabel", "State",
    "Pickup_City", "Delivery_City", "Pickup_Time", "SignFor_Time",
    "SignFor_TimeSpan(min)", "Timeout", "LatestTrace",
    "Delivery_Courier", "Delivery_Courier_Phone", "Code", "Message",
]


def _row_for(r: Dict[str, Any]) -> Dict[str, Any]:
    s = r["summary"]
    if r["ok"]:
        span = ""
        for sp in s.get("spans", []):
            if sp["field"] == "SignFor_TimeSpan":
                span = f"{sp['minutes']:.0f}"
        return {
            "No": r["no"],
            "ExpressName": s.get("shipper", ""),
            "StateDesc": s.get("state_desc", ""),
            "StateLabel": s.get("state_label", ""),
            "State": s.get("state_code", ""),
            "Pickup_City": s.get("pickup_city", ""),
            "Delivery_City": s.get("delivery_city", ""),
            "Pickup_Time": s.get("pickup_time", ""),
            "SignFor_Time": s.get("signfor_time", ""),
            "SignFor_TimeSpan(min)": span,
            "Timeout": "1" if s.get("timeouts") else "0",
            "LatestTrace": (s.get("last_trace") or "").replace("\n", " "),
            "Delivery_Courier": s.get("delivery_courier", ""),
            "Delivery_Courier_Phone": s.get("delivery_courier_phone", ""),
            "Code": r["code"],
            "Message": "",
        }
    return {
        "No": r["no"], "ExpressName": "", "StateDesc": "", "StateLabel": "查询失败",
        "State": "", "Pickup_City": "", "Delivery_City": "", "Pickup_Time": "",
        "SignFor_Time": "", "SignFor_TimeSpan(min)": "", "Timeout": "",
        "LatestTrace": "", "Delivery_Courier": "", "Delivery_Courier_Phone": "",
        "Code": r["code"], "Message": r["message"] or "",
    }


def write_csv(path: str, results: List[Dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        w.writeheader()
        for r in results:
            w.writerow(_row_for(r))


def write_json(path: str, results: List[Dict[str, Any]], agg: Dict[str, Any]) -> None:
    payload = {
        "aggregate": agg,
        "results": [
            {
                "no": r["no"], "tel": r["tel"], "ok": r["ok"],
                "code": r["code"], "message": r["message"],
                "summary": r["summary"], "raw": r["response"],
            }
            for r in results
        ],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def write_report_txt(path: str, results: List[Dict[str, Any]], agg: Dict[str, Any]) -> None:
    buf = io.StringIO()
    buf.write(format_aggregate(agg))
    buf.write("\n\n" + "=" * 48 + "\n逐单明细\n" + "=" * 48 + "\n")
    for r in results:
        if r["ok"]:
            buf.write(f"\n--- {r['no']} ---\n")
            buf.write(format_text(r["summary"]))
        else:
            buf.write(f"\n--- {r['no']} ---\n查询失败：Code={r['code']} {r['message']}\n")
    with open(path, "w", encoding="utf-8") as f:
        f.write(buf.getvalue())


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _cli(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(
        description="小递查查批量快递查询（支持文件/内联/手机号映射，并发查询+聚合统计）",
    )
    p.add_argument("--platform-id", default=os.environ.get("XDCC_PLATFORM_ID"),
                   help="平台ID（环境变量 XDCC_PLATFORM_ID）")
    p.add_argument("--api-key", default=os.environ.get("XDCC_API_KEY"),
                   help="API密钥（环境变量 XDCC_API_KEY）")
    p.add_argument("--member-id", default=os.environ.get("XDCC_MEMBER_ID", "default"),
                   help="会员唯一ID（环境变量 XDCC_MEMBER_ID）")
    src = p.add_argument_group("输入来源（三选一或组合）")
    src.add_argument("--file", help="批量文件：每行一个运单号，可附手机号 'NO,TEL'")
    src.add_argument("--nos", help="内联单号：逗号/空格分隔，如 'no1,no2,no3'")
    src.add_argument("--telmap", help="手机号映射 CSV：表头 no,tel")
    src.add_argument("--tel", default="", help="全局默认手机号后四位（顺丰/中通必填）")
    p.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY,
                   help=f"并发数（默认 {DEFAULT_CONCURRENCY}，上限 {MAX_CONCURRENCY}）")
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="单请求超时秒数")
    p.add_argument("--output", help="输出基名（不含扩展名）；配合 --format 生成文件")
    p.add_argument("--format", default="all", choices=["json", "csv", "txt", "all"],
                   help="导出格式（默认 all：三种都生成）")
    p.add_argument("--pretty", action="store_true", help="向 stdout 打印可读汇总+逐单明细")
    p.add_argument("--quiet", action="store_true", help="不打印进度")
    args = p.parse_args(argv)

    if not args.platform_id or not args.api_key:
        print("错误: 缺少 PlatformID 或 APIKey。请通过参数或环境变量 "
              "XDCC_PLATFORM_ID / XDCC_API_KEY 传入。", file=sys.stderr)
        return EXIT_BAD_ARGS

    try:
        items = parse_input(args)
    except (OSError, UnicodeDecodeError) as e:
        # 路径打错/编码不对时给中文提示，而不是把调用方扔进 FileNotFoundError 栈回溯
        print(f"错误: 读取输入失败：{e}", file=sys.stderr)
        print("请检查 --file / --telmap 路径是否存在，且文件为 UTF-8 编码。", file=sys.stderr)
        return EXIT_BAD_ARGS

    if not items:
        print("错误: 未解析到任何运单号。请通过 --file / --nos / --telmap 提供。", file=sys.stderr)
        return EXIT_BAD_ARGS

    warn = warn_missing_tel(items)
    if warn:
        sys.stderr.write(warn + "\n")

    results = batch_query(
        args.platform_id, args.api_key, args.member_id, items,
        concurrency=args.concurrency, timeout=args.timeout,
        progress=not args.quiet,
    )
    agg = build_aggregate(results)

    # 导出文件
    if args.output:
        fmt = args.format
        if fmt in ("json", "all"):
            write_json(args.output + ".json", results, agg)
        if fmt in ("csv", "all"):
            write_csv(args.output + ".csv", results)
        if fmt in ("txt", "all"):
            write_report_txt(args.output + ".report.txt", results, agg)

    if args.pretty or not args.output:
        print(format_aggregate(agg))
        if args.pretty:
            print("\n" + "=" * 48 + "\n逐单明细\n" + "=" * 48)
            for r in results:
                print(f"\n--- {r['no']} ---")
                if r["ok"]:
                    print(format_text(r["summary"]))
                else:
                    print(f"查询失败：Code={r['code']} {r['message']}")

    return EXIT_OK if not agg["failed"] else EXIT_PARTIAL


def main(argv: Optional[List[str]] = None) -> int:
    """供 selftest / 外部调用的稳定入口。"""
    return _cli(argv)


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass
    sys.exit(main())
