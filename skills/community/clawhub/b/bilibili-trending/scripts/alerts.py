"""
异常检测与热点预警

检测维度：
- 互动率飙升：视频互动率远超历史均值
- 新 UP 主上榜：首次出现在该榜单的 UP 主
- 分区突变：分区占比显著偏离历史
- 关键词爆发：新关键词进入 Top 10
"""

import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict

from config import RANK_CONFIG
from common import load_trend, ANALYSIS_DIR

ALERTS_FILE = os.path.join(ANALYSIS_DIR, "alerts.json")

INTERACTION_SPIKE_RATIO = 2.5
ZONE_SURGE_RATIO = 2.0
MIN_HISTORICAL_RECORDS = 3


@dataclass
class Alert:
    rank_type: str
    rank_name: str
    level: str       # hot / warning / info
    category: str    # interaction / new_up / zone / keyword
    title: str
    detail: str
    timestamp: str


def load_alerts():
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_alerts(alerts):
    existing = load_alerts()
    for a in alerts:
        existing.append(asdict(a))
    existing = existing[-200:]
    with open(ALERTS_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)


def _get_historical_for_rank(rank_type):
    trend = load_trend()
    records = [r for r in trend["records"] if r.get("rank_type") == rank_type]
    if len(records) < MIN_HISTORICAL_RECORDS:
        return None

    interactions = [r.get("avg_interaction", 0) for r in records]
    zones = {}
    keywords = {}

    for r in records:
        zone = r.get("top_zone", "")
        if zone:
            zones[zone] = zones.get(zone, 0) + 1
        for kw in r.get("keywords", []):
            keywords[kw] = keywords.get(kw, 0) + 1

    return {
        "record_count": len(records),
        "avg_interaction": sum(interactions) / len(interactions) if interactions else 0,
        "historical_zones": zones,
        "historical_keywords": keywords,
    }


def detect_interaction_spikes(videos, rank_type):
    hist = _get_historical_for_rank(rank_type)
    if not hist:
        return []

    threshold = hist["avg_interaction"] * INTERACTION_SPIKE_RATIO
    rank_name = RANK_CONFIG[rank_type]["name"]
    alerts = []

    for v in videos:
        ir = v.get("interaction_rate", 0)
        if ir > threshold and threshold > 0:
            ratio = ir / hist["avg_interaction"]
            alerts.append(Alert(
                rank_type=rank_type,
                rank_name=rank_name,
                level="hot",
                category="interaction",
                title=f"高互动视频: {v['title'][:30]}",
                detail=f"互动率 {ir:.2f}%（历史均值 {hist['avg_interaction']:.2f}% 的 {ratio:.1f} 倍）| "
                        f"播放 {v['view']:,} | UP主 {v.get('owner', '未知')}",
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ))

    return alerts


def _load_historical_ups(rank_type):
    up_file = os.path.join(ANALYSIS_DIR, f"up_history_{rank_type}.json")
    if os.path.exists(up_file):
        with open(up_file, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def _save_historical_ups(rank_type, ups):
    up_file = os.path.join(ANALYSIS_DIR, f"up_history_{rank_type}.json")
    with open(up_file, "w", encoding="utf-8") as f:
        json.dump(list(ups), f, ensure_ascii=False)


def detect_new_ups(videos, rank_type):
    trend = load_trend()
    records = [r for r in trend["records"] if r.get("rank_type") == rank_type]
    if len(records) < MIN_HISTORICAL_RECORDS:
        return []

    seen_ups = _load_historical_ups(rank_type)
    rank_name = RANK_CONFIG[rank_type]["name"]
    alerts = []

    for v in videos:
        owner = v.get("owner", "")
        if not owner or len(owner) < 2:
            continue
        if owner not in seen_ups:
            seen_ups.add(owner)
            alerts.append(Alert(
                rank_type=rank_type,
                rank_name=rank_name,
                level="info",
                category="new_up",
                title=f"新 UP 主上榜: {owner}",
                detail=f"《{v['title'][:40]}》| 排名 #{v['rank']} | 播放 {v['view']:,} | "
                        f"分区 {v.get('tname', v.get('area', ''))}",
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ))

    _save_historical_ups(rank_type, seen_ups)
    return alerts


def detect_zone_anomaly(summary, rank_type):
    hist = _get_historical_for_rank(rank_type)
    if not hist:
        return []

    rank_name = RANK_CONFIG[rank_type]["name"]
    zone_dist = summary.get("zone_distribution", {})
    record_count = hist["record_count"]
    alerts = []

    for zone, count in zone_dist.items():
        hist_count = hist["historical_zones"].get(zone, 0)
        hist_ratio = hist_count / record_count if record_count else 0
        current_ratio = count / summary.get("total_videos", 1)

        if hist_ratio > 0 and current_ratio > hist_ratio * ZONE_SURGE_RATIO:
            alerts.append(Alert(
                rank_type=rank_type,
                rank_name=rank_name,
                level="warning",
                category="zone",
                title=f"分区热度突变: {zone}",
                detail=f"当前占比 {current_ratio * 100:.1f}%（历史均值 {hist_ratio * 100:.1f}%）| "
                        f"共 {count}/{summary.get('total_videos', 0)} 条视频",
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ))

    return alerts


def detect_keyword_burst(top_keywords, rank_type):
    hist = _get_historical_for_rank(rank_type)
    if not hist:
        return []

    rank_name = RANK_CONFIG[rank_type]["name"]
    alerts = []

    for kw in top_keywords[:5]:
        if kw not in hist["historical_keywords"]:
            alerts.append(Alert(
                rank_type=rank_type,
                rank_name=rank_name,
                level="info",
                category="keyword",
                title=f"新热词出现: {kw}",
                detail=f"「{kw}」首次进入 {rank_name} 榜 Top 10 关键词",
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ))

    return alerts


def detect_all(rank_type, videos, summary, top_keywords):
    alerts = []
    alerts.extend(detect_interaction_spikes(videos, rank_type))
    alerts.extend(detect_new_ups(videos, rank_type))
    alerts.extend(detect_zone_anomaly(summary, rank_type))
    alerts.extend(detect_keyword_burst(top_keywords, rank_type))
    return alerts


def format_alerts(alerts):
    if not alerts:
        return ""

    level_icons = {"hot": "HOT", "warning": "WARN", "info": "INFO"}
    lines = ["", "=" * 60, "预警报告", "=" * 60]

    for a in alerts:
        icon = level_icons.get(a.level, "?")
        lines.append(f"  [{icon}] [{a.category}] {a.title}")
        lines.append(f"        {a.detail}")

    lines.append("=" * 60)
    return "\n".join(lines)
