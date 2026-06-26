# coding=utf-8
import requests
import json
import urllib3
import sys
from datetime import datetime, timedelta
from collections import Counter, defaultdict

# 禁用 SSL 警告（内网 IP）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ──────────────────────────────────────────
#  API 配置
# ──────────────────────────────────────────
API_URL = "https://10.50.86.28/xdr/openapi/v1.0/risk/listDetail"
API_KEY = "7445a03b544484ff3ab552fd81d1f2b7"

HEADERS = {
    "apikey": API_KEY,
    "accept": "*/*"
}

# ──────────────────────────────────────────
#  Step 1：拉取数据（支持时间范围）
# ──────────────────────────────────────────
def fetch_events(days=1) -> dict:
    """请求指定天数的安全事件，返回原始 JSON dict。"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days-1)
    
    start_time = f"{start_date.strftime('%Y-%m-%d')} 00:00:00"
    end_time = f"{end_date.strftime('%Y-%m-%d')} 23:59:59"
    
    params = {
        "startTime": start_time,
        "endTime": end_time
    }

    # 调试信息输出到 stderr（不会影响 stdout 的 JSON 解析）
    print(f"[INFO] 请求 API：{API_URL}", file=sys.stderr)
    print(f"[INFO] 时间范围：{params['startTime']}  →  {params['endTime']}", file=sys.stderr)
    print(f"[INFO] 统计天数：{days} 天", file=sys.stderr)
    print("-" * 60, file=sys.stderr)

    response = requests.get(
        API_URL,
        headers=HEADERS,
        params=params,
        verify=False,
        timeout=120
    )
    response.raise_for_status()

    raw = response.json()
    print(f"[INFO] 响应状态码：{response.status_code}，事件条数：{len(raw.get('data', []))}", file=sys.stderr)
    return raw


# ──────────────────────────────────────────
#  工具函数
# ──────────────────────────────────────────
def ensure_json(data):
    if isinstance(data, str):
        data = json.loads(data)
    if not isinstance(data, dict):
        raise ValueError("顶层数据必须是 dict")
    return data

def ensure_list(events):
    if not isinstance(events, list):
        raise ValueError("data 字段必须是列表 list")
    return events

def parse_time(t: str) -> datetime:
    return datetime.strptime(t, "%Y-%m-%d %H:%M:%S")


# ──────────────────────────────────────────
#  Step 2：数据处理（六大模块）
# ──────────────────────────────────────────

# ---------- 1. 威胁态势总览 ----------
def extract_trend_data(raw_data):
    raw_data = ensure_json(raw_data)
    events   = ensure_list(raw_data.get("data"))

    trend_events = []
    for e in events:
        start_time = e.get("startTime")
        end_time   = e.get("endTime")
        if not start_time and not end_time:
            continue
        trend_events.append({
            "startTime":      start_time,
            "eventCount":     e.get("counts"),
            "focusObjectCN":  e.get("focusObjectCN"),
            "name":           e.get("name"),
            "threatSeverity": e.get("threatSeverity")
        })
    return trend_events


def build_trend_stats(trend_events):
    time_record_counter     = defaultdict(int)
    severity_counter        = Counter()
    object_counter          = Counter()
    name_occurrence_counter = Counter()

    for e in trend_events:
        t = e.get("startTime")
        if not t:
            continue
        hour = t[:13]
        time_record_counter[hour] += 1
        severity_counter[e.get("threatSeverity", "未知")] += 1
        object_counter[e.get("focusObjectCN", "未知")] += 1

        c = int(e.get("eventCount", 0) or 0)
        name_occurrence_counter[e.get("name", "未知")] += c

    if not time_record_counter:
        return {}

    sorted_times = sorted(time_record_counter.items())
    first_count  = sorted_times[0][1]
    last_count   = sorted_times[-1][1]

    if last_count > first_count * 1.2:
        trend = "上升"
    elif last_count < first_count * 0.8:
        trend = "下降"
    else:
        trend = "波动"

    peak_time, peak_event_count = max(time_record_counter.items(), key=lambda x: x[1])
    avg_event_count = int(sum(time_record_counter.values()) / len(time_record_counter))

    return {
        "trend":                   trend,
        "timeBuckets":             len(sorted_times),
        "peakTime":                peak_time,
        "peakEventCount":          peak_event_count,
        "avgEventCount":           avg_event_count,
        "severityDistribution":    severity_counter.most_common(3),
        "focusObjectDistribution": object_counter.most_common(),
        "topEventNames":           name_occurrence_counter.most_common(3)
    }


def extract_event_totals(raw_data):
    raw_data = ensure_json(raw_data)
    events   = ensure_list(raw_data.get("data"))
    return {"totalEventRecords": len(events)}


def extract_top_attack_ips(raw_data, top_n=5):
    raw_data     = ensure_json(raw_data)
    events       = ensure_list(raw_data.get("data"))
    attacker_ips = []

    for e in events:
        if e.get("focusObjectCN") != "攻击者":
            continue
        focus_ip = e.get("focusIp")
        if focus_ip:
            attacker_ips.extend([ip.strip() for ip in focus_ip.split(",") if ip.strip()])

    return Counter(attacker_ips).most_common(top_n)


# ---------- 2. 重点受影响资产 ----------
def extract_victim_top_ips(raw_data, top_n=3):
    raw_data   = ensure_json(raw_data)
    events     = ensure_list(raw_data.get("data"))
    victim_ips = []

    for e in events:
        if e.get("focusObjectCN") != "受害者":
            continue
        focus_ip = e.get("focusIp")
        if focus_ip:
            victim_ips.extend([ip.strip() for ip in focus_ip.split(",") if ip.strip()])

    return Counter(victim_ips).most_common(top_n)


def extract_asset_data(events):
    # TODO: 按 asset / focusIp / name 聚合逻辑
    return []


# ---------- 3. 长周期潜伏事件（总结） ----------
SEVERITY_ORDER = {"低": 1, "中": 2, "高": 3, "严重": 4}

def extract_long_cycle_summary(raw_data):
    raw_data = ensure_json(raw_data)
    events   = ensure_list(raw_data.get("data"))

    long_cycle_events = []
    for e in events:
        start_time = e.get("startTime")
        end_time   = e.get("endTime")
        if not start_time or not end_time:
            continue

        start_dt      = parse_time(start_time)
        end_dt        = parse_time(end_time)
        delta         = end_dt - start_dt
        duration_days = delta.days + (1 if delta.seconds > 0 else 0)
        time_range    = f"{start_dt.strftime('%Y.%m.%d')}-{end_dt.strftime('%Y.%m.%d')}"

        focus_ip = e.get("focusIp", "")
        ips = ",".join(focus_ip.split(",")[:3]) if focus_ip else "无"

        long_cycle_events.append({
            "timeRange":      time_range,
            "durationDays":   duration_days,
            "focusObjectCN":  e.get("focusObjectCN", ""),
            "ips":            ips,
            "name":           e.get("name", ""),
            "threatSeverity": e.get("threatSeverity", ""),
            "alarmResults":   e.get("alarmResults", ""),
            "eventCount":     e.get("counts")
        })

    if not long_cycle_events:
        return {"longest_event": None, "highest_risk_event": None, "top5_events": []}

    longest_event      = max(long_cycle_events, key=lambda x: x["durationDays"])
    highest_risk_event = max(long_cycle_events, key=lambda x: SEVERITY_ORDER.get(x["threatSeverity"], 0))
    top5_events        = sorted(long_cycle_events, key=lambda x: x["durationDays"], reverse=True)[:5]

    return {
        "longest_event":      longest_event,
        "highest_risk_event": highest_risk_event,
        "top5_events":        top5_events
    }


def extract_long_cycle_top_attackers(raw_data, top_n=3):
    raw_data = ensure_json(raw_data)
    events   = ensure_list(raw_data.get("data"))

    ip_days   = defaultdict(set)
    ip_events = defaultdict(list)

    for e in events:
        if e.get("focusObjectCN") != "攻击者":
            continue
        start_time = e.get("startTime")
        end_time   = e.get("endTime")
        focus_ip   = e.get("focusIp")
        if not (start_time and end_time and focus_ip):
            continue

        start_dt = parse_time(start_time)
        end_dt   = parse_time(end_time)
        cur      = start_dt.date()
        end_date = end_dt.date()
        ip_list  = [ip.strip() for ip in focus_ip.split(",") if ip.strip()]

        while cur <= end_date:
            for ip in ip_list:
                ip_days[ip].add(cur)
            cur += timedelta(days=1)

        for ip in ip_list:
            ip_events[ip].append(e)

    result = []
    for ip, days in ip_days.items():
        evts         = ip_events[ip]
        start_dates  = [parse_time(e["startTime"]).date() for e in evts]
        end_dates    = [parse_time(e["endTime"]).date()   for e in evts]
        max_severity = max((e.get("threatSeverity", "低") for e in evts),
                         key=lambda x: SEVERITY_ORDER.get(x, 0))
        main_event   = max(
            (e.get("subCategory") or e.get("name") for e in evts),
            key=lambda x: sum(1 for e in evts if (e.get("subCategory") or e.get("name")) == x)
        )
        result.append({
            "ip":                ip,
            "timeRange":         f"{min(start_dates)}-{max(end_dates)}",
            "durationDays":      len(days),
            "eventCount":        len(evts),
            "maxThreatSeverity": max_severity,
            "mainEventType":     main_event
        })

    return sorted(result, key=lambda x: x["durationDays"], reverse=True)[:top_n]


# ---------- 4. 长周期潜伏事件（明细） ----------
def extract_long_cycle_details(events):
    # TODO: 按子类分组 + 时间顺序展开
    return {}


# ---------- 5. 高危安全事件解读（Top5） ----------
def extract_top5_risk_events(raw_data):
    raw_data = ensure_json(raw_data)
    events   = ensure_list(raw_data.get("data"))

    # 原逻辑里用 eventCount 排序可能拿不到值，这里改为优先 counts（更稳）
    def _get_count(x):
        return int(x.get("eventCount") or x.get("counts") or 0)

    events = sorted(events, key=_get_count, reverse=True)[:5]

    result = []
    for rank, e in enumerate(events, start=1):
        start_time = e.get("startTime", "")
        end_time   = e.get("endTime", "")
        time_range = f"{start_time} - {end_time}" if (start_time and end_time) else ""

        focus_ip_raw = e.get("focusIp", "")
        top3_ips     = [i.strip() for i in focus_ip_raw.split(",") if i.strip()][:3]

        risk           = e.get("riskAnalyse", {}) or {}
        suggestion_raw = risk.get("attackDisposalSuggestionList", []) or []

        result.append({
            "rank":                        rank,
            "subCategory":                 e.get("subCategory", ""),
            "eventCount":                  _get_count(e),
            "timeRange":                   time_range,
            "focusObjectCN":               e.get("focusObjectCN", ""),
            "top3Ips":                     top3_ips,
            "coreRisks":                   risk.get("coreRisks", ""),
            "criticalDangerPoint":         risk.get("criticalDangerPoint", ""),
            "attackDisposalSuggestionList": [
                {"step": item.get("step"), "desc": item.get("desc")}
                for item in suggestion_raw
            ]
        })
    return result


# ---------- 6. 智能分析与加固建议 ----------
def extract_ai_analysis_data(events):
    # TODO: 根据业务需要汇总数据特征
    return {}


# ──────────────────────────────────────────
#  Step 3：整合主流程
# ──────────────────────────────────────────
def process(raw_data: dict) -> dict:
    trend_data = extract_trend_data(raw_data)

    return {
        "trend_stats":              build_trend_stats(trend_data),
        "event_totals":             extract_event_totals(raw_data),
        "trend_top5_ips":           extract_top_attack_ips(raw_data),
        "victim_top3_ips":          extract_victim_top_ips(raw_data),
        "asset_data":               extract_asset_data(raw_data),
        "long_cycle_summary":       extract_long_cycle_summary(raw_data),
        "long_cycle_top_attackers": extract_long_cycle_top_attackers(raw_data),
        "long_cycle_details":       extract_long_cycle_details(raw_data),
        "top5_risk_events":         extract_top5_risk_events(raw_data),
        "analysis_and_recommend":   extract_ai_analysis_data(raw_data)
    }


# ──────────────────────────────────────────
#  入口：stdout 只输出 JSON，然后退出
# ──────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='获取安全事件数据')
    parser.add_argument('--days', type=int, default=1, help='统计周期天数（默认1天）')
    args = parser.parse_args()
    
    try:
        raw_data = fetch_events(args.days)
        result = process(raw_data)

        # stdout：只输出一份 JSON（无多余文本）
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)

    except requests.exceptions.RequestException as e:
        # stdout：仍输出 JSON，便于上游解析；调试信息走 stderr
        print(f"[ERROR] 请求失败：{e}", file=sys.stderr)
        err = {"ok": False, "stage": "fetch", "error": str(e)}
        print(json.dumps(err, ensure_ascii=False))
        sys.exit(1)

    except Exception as e:
        print(f"[ERROR] 未知错误：{e}", file=sys.stderr)
        err = {"ok": False, "stage": "process", "error": str(e)}
        print(json.dumps(err, ensure_ascii=False))
        sys.exit(2)