"""DataPulse command line entry."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import datapulse
from datapulse.core.config import SearchGatewayConfig
from datapulse.reader import DataPulseReader
from datapulse.tools.session import login_platform, supported_platforms

_GITHUB_RELEASES_API = "https://api.github.com/repos/sunyifei83/DataPulse/releases/latest"
_GITHUB_REPO = "https://github.com/sunyifei83/DataPulse"


def _print_list(items, limit: int = 20):
    if not items:
        print("📦 Inbox is empty")
        return

    print(f"📦 {len(items)} item(s)\n")
    for idx, item in enumerate(items[:limit], 1):
        score = f"{item.confidence:.3f}"
        print(f"{idx:2d}. [{item.source_type.value}] {item.title[:55]} - {score}")
        print(f"    {item.url}")


def _print_sources(sources, include_inactive: bool = False, public_only: bool = True):
    for source in sources:
        status = "active" if source.get("is_active", True) else "inactive"
        visibility = "public" if source.get("is_public", True) else "private"
        print(f"{source.get('id')}: {source.get('name')} | {source.get('source_type')} | {status}/{visibility}")


def _print_packs(packs):
    for pack in packs:
        count = len(pack.get("source_ids", []))
        print(f"{pack.get('slug')}: {pack.get('name')} | {count} source(s)")


def _print_watches(watches):
    for watch in watches:
        status = "enabled" if watch.get("enabled", True) else "disabled"
        platforms = ",".join(watch.get("platforms", [])) or "any"
        sites = ",".join(watch.get("sites", [])) or "-"
        query = str(watch.get("query", "")).strip()
        last_run = watch.get("last_run_at") or "-"
        last_status = watch.get("last_run_status") or "-"
        schedule = watch.get("schedule_label") or watch.get("schedule") or "manual"
        due = "yes" if watch.get("is_due") else "no"
        print(
            f"{watch.get('id')}: {watch.get('name')} | {status} | "
            f"platforms={platforms} | sites={sites} | top_n={watch.get('top_n', 5)} | "
            f"schedule={schedule} | due={due} | alerts={watch.get('alert_rule_count', 0)}"
        )
        print(f"    query: {query}")
        intent_summary = watch.get("intent_summary", {}) if isinstance(watch, dict) else {}
        if isinstance(intent_summary, dict) and intent_summary.get("has_intent"):
            demand_intent = str(intent_summary.get("demand_intent", "") or "").strip()
            if demand_intent:
                print(f"    intent: {demand_intent}")
            scope = str(intent_summary.get("scope", "") or "").strip()
            if scope:
                print(f"    scope: {scope}")
            freshness = str(intent_summary.get("freshness", "") or "").strip()
            if freshness:
                print(f"    freshness: {freshness}")
        print(f"    last_run: {last_run} | status: {last_status}")


def _print_alerts(alerts):
    for alert in alerts:
        delivered = ",".join(alert.get("delivered_channels", [])) or "json"
        print(f"{alert.get('id')}: {alert.get('mission_name')} | {alert.get('rule_name')} | channels={delivered}")
        print(f"    summary: {alert.get('summary', '')}")
        print(f"    created_at: {alert.get('created_at', '-')}")
        delivery_errors = alert.get("extra", {}).get("delivery_errors", {}) if isinstance(alert.get("extra"), dict) else {}
        if delivery_errors:
            print(f"    delivery_errors: {delivery_errors}")


def _print_alert_routes(routes):
    for route in routes:
        name = route.get("name", "-")
        channel = route.get("channel", "-")
        print(f"{name}: channel={channel}")


def _print_alert_route_health(routes):
    for route in routes:
        print(
            f"{route.get('name', '-')}: channel={route.get('channel', '-')}"
            f" | status={route.get('status', 'idle')}"
            f" | events={route.get('event_count', 0)}"
            f" | delivered={route.get('delivered_count', 0)}"
            f" | failed={route.get('failure_count', 0)}"
        )
        success_rate = route.get("success_rate")
        if success_rate is not None:
            print(f"    success_rate: {float(success_rate) * 100:.1f}%")
        print(f"    last_event_at: {route.get('last_event_at', '-') or '-'}")
        print(f"    last_error: {route.get('last_error', '-') or '-'}")


def _print_watch_status(payload):
    metrics = payload.get("metrics", {}) if isinstance(payload, dict) else {}
    print(f"state: {payload.get('state', 'idle')}")
    print(f"heartbeat_at: {payload.get('heartbeat_at', '-')}")
    print(f"last_error: {payload.get('last_error', '-') or '-'}")
    print(f"cycles_total: {metrics.get('cycles_total', 0)}")
    print(f"runs_total: {metrics.get('runs_total', 0)}")
    print(f"alerts_total: {metrics.get('alerts_total', 0)}")


def _print_ops_overview(payload):
    collector_summary = payload.get("collector_summary", {}) if isinstance(payload, dict) else {}
    collector_tiers = payload.get("collector_tiers", {}) if isinstance(payload, dict) else {}
    collector_drilldown = payload.get("collector_drilldown", []) if isinstance(payload, dict) else []
    watch_metrics = payload.get("watch_metrics", {}) if isinstance(payload, dict) else {}
    watch_summary = payload.get("watch_summary", {}) if isinstance(payload, dict) else {}
    watch_health = payload.get("watch_health", []) if isinstance(payload, dict) else []
    route_summary = payload.get("route_summary", {}) if isinstance(payload, dict) else {}
    route_drilldown = payload.get("route_drilldown", []) if isinstance(payload, dict) else []
    route_timeline = payload.get("route_timeline", []) if isinstance(payload, dict) else []
    degraded_collectors = payload.get("degraded_collectors", []) if isinstance(payload, dict) else []
    recent_failures = payload.get("recent_failures", []) if isinstance(payload, dict) else []

    print("collector_health:")
    print(f"  total: {collector_summary.get('total', 0)}")
    print(f"  ok: {collector_summary.get('ok', 0)}")
    print(f"  warn: {collector_summary.get('warn', 0)}")
    print(f"  error: {collector_summary.get('error', 0)}")
    print(f"  unavailable: {collector_summary.get('unavailable', 0)}")
    if degraded_collectors:
        print("  degraded_collectors:")
        for collector in degraded_collectors[:5]:
            print(
                f"    - {collector.get('name', '-')}"
                f" [{collector.get('tier', '-')}]"
                f" status={collector.get('status', '-')}"
                f" available={collector.get('available', True)}"
            )
            message = str(collector.get("message", "") or "").strip()
            if message:
                print(f"      message: {message}")
    if collector_tiers:
        print("  tiers:")
        for tier_name in sorted(collector_tiers):
            tier = collector_tiers.get(tier_name, {})
            print(
                f"    - {tier_name}"
                f" | total={tier.get('total', 0)}"
                f" | ok={tier.get('ok', 0)}"
                f" | warn={tier.get('warn', 0)}"
                f" | error={tier.get('error', 0)}"
            )
    if collector_drilldown:
        print("  drilldown:")
        for collector in collector_drilldown[:8]:
            print(
                f"    - {collector.get('name', '-')}"
                f" | tier={collector.get('tier', '-')}"
                f" | status={collector.get('status', '-')}"
                f" | available={collector.get('available', True)}"
            )
            detail = str(collector.get("setup_hint") or collector.get("message") or "").strip()
            if detail:
                print(f"      detail: {detail}")

    print("watch_metrics:")
    print(f"  state: {watch_metrics.get('state', 'idle')}")
    print(f"  heartbeat_at: {watch_metrics.get('heartbeat_at', '-') or '-'}")
    print(f"  cycles_total: {watch_metrics.get('cycles_total', 0)}")
    print(f"  runs_total: {watch_metrics.get('runs_total', 0)}")
    print(f"  success_total: {watch_metrics.get('success_total', 0)}")
    print(f"  error_total: {watch_metrics.get('error_total', 0)}")
    print(f"  alerts_total: {watch_metrics.get('alerts_total', 0)}")
    success_rate = watch_metrics.get("success_rate")
    if success_rate is not None:
        print(f"  success_rate: {float(success_rate) * 100:.1f}%")
    print(f"  last_error: {watch_metrics.get('last_error', '-') or '-'}")
    print("watch_health:")
    print(f"  total: {watch_summary.get('total', 0)}")
    print(f"  enabled: {watch_summary.get('enabled', 0)}")
    print(f"  disabled: {watch_summary.get('disabled', 0)}")
    print(f"  healthy: {watch_summary.get('healthy', 0)}")
    print(f"  degraded: {watch_summary.get('degraded', 0)}")
    print(f"  idle: {watch_summary.get('idle', 0)}")
    print(f"  due: {watch_summary.get('due', 0)}")
    if watch_health:
        print("  missions:")
        for mission in watch_health[:5]:
            rate = mission.get("success_rate")
            rate_label = f"{float(rate) * 100:.1f}%" if rate is not None else "-"
            print(
                f"    - {mission.get('id', '-')}"
                f" | status={mission.get('status', 'idle')}"
                f" | enabled={mission.get('enabled', True)}"
                f" | due={mission.get('is_due', False)}"
                f" | rate={rate_label}"
            )
            print(
                f"      {mission.get('name', '')}"
                f" | next={mission.get('next_run_at', '-') or '-'}"
                f" | last={mission.get('last_run_at', '-') or '-'}"
            )
            last_error = str(mission.get("last_run_error", "") or "").strip()
            if last_error:
                print(f"      last_error: {last_error}")

    print("route_health:")
    print(f"  total: {route_summary.get('total', 0)}")
    print(f"  healthy: {route_summary.get('healthy', 0)}")
    print(f"  degraded: {route_summary.get('degraded', 0)}")
    print(f"  missing: {route_summary.get('missing', 0)}")
    print(f"  idle: {route_summary.get('idle', 0)}")
    if route_drilldown:
        print("  drilldown:")
        for route in route_drilldown[:8]:
            rate = route.get("success_rate")
            rate_label = f"{float(rate) * 100:.1f}%" if rate is not None else "-"
            print(
                f"    - {route.get('name', '-')}"
                f" | channel={route.get('channel', '-')}"
                f" | status={route.get('status', '-')}"
                f" | rate={rate_label}"
            )
            print(
                f"      missions={route.get('mission_count', 0)}"
                f" | rules={route.get('rule_count', 0)}"
                f" | events={route.get('event_count', 0)}"
                f" | failed={route.get('failure_count', 0)}"
            )
            detail = str(route.get("last_error") or route.get("last_summary") or "").strip()
            if detail:
                print(f"      detail: {detail}")
    if route_timeline:
        print("  timeline:")
        for event in route_timeline[:8]:
            print(
                f"    - {event.get('created_at', '-')}"
                f" | {event.get('route', '-')}"
                f" | {event.get('status', '-')}"
                f" | mission={event.get('mission_name', event.get('mission_id', '-'))}"
            )
            detail = str(event.get("error") or event.get("summary") or "").strip()
            if detail:
                print(f"      detail: {detail}")

    if recent_failures:
        print("recent_failures:")
        for failure in recent_failures[:5]:
            if failure.get("kind") == "watch_run":
                print(
                    f"  - watch_run {failure.get('mission_name', failure.get('mission_id', '-'))}"
                    f" | status={failure.get('status', 'error')}"
                    f" | attempts={failure.get('attempts', 0)}"
                )
            else:
                print(
                    f"  - route_delivery {failure.get('name', '-')}"
                    f" | channel={failure.get('channel', '-')}"
                    f" | status={failure.get('status', 'degraded')}"
                )
            print(f"    error: {failure.get('error', '-') or '-'}")


def _print_watch_detail(payload):
    run_stats = payload.get("run_stats", {}) if isinstance(payload, dict) else {}
    delivery_stats = payload.get("delivery_stats", {}) if isinstance(payload, dict) else {}
    last_failure = payload.get("last_failure") if isinstance(payload, dict) else None
    retry_advice = payload.get("retry_advice") if isinstance(payload, dict) else None
    mission_intent = payload.get("mission_intent", {}) if isinstance(payload, dict) else {}
    print(f"id: {payload.get('id', '-')}")
    print(f"name: {payload.get('name', '')}")
    print(f"query: {payload.get('query', '')}")
    print(f"enabled: {payload.get('enabled', True)}")
    print(f"schedule: {payload.get('schedule_label') or payload.get('schedule') or 'manual'}")
    print(f"is_due: {payload.get('is_due', False)}")
    print(f"next_run_at: {payload.get('next_run_at', '-') or '-'}")
    print(f"last_run_at: {payload.get('last_run_at', '-') or '-'}")
    print(f"last_run_status: {payload.get('last_run_status', '-') or '-'}")
    print(f"last_run_error: {payload.get('last_run_error', '-') or '-'}")
    print(f"run_total: {run_stats.get('total', 0)}")
    print(f"run_success: {run_stats.get('success', 0)}")
    print(f"run_error: {run_stats.get('error', 0)}")
    print(f"avg_items: {run_stats.get('average_items', 0)}")
    print(f"recent_alert_count: {delivery_stats.get('recent_alert_count', 0)}")
    print(f"recent_delivery_error_count: {delivery_stats.get('recent_error_count', 0)}")

    if isinstance(mission_intent, dict) and mission_intent:
        print("mission_intent:")
        if mission_intent.get("demand_intent"):
            print(f"  demand_intent: {mission_intent.get('demand_intent')}")
        key_questions = mission_intent.get("key_questions", [])
        if key_questions:
            print(f"  key_questions: {', '.join(str(question) for question in key_questions)}")
        for field_name in ("scope_entities", "scope_topics", "scope_regions", "coverage_targets"):
            values = mission_intent.get(field_name, [])
            if values:
                print(f"  {field_name}: {', '.join(str(value) for value in values)}")
        if mission_intent.get("scope_window"):
            print(f"  scope_window: {mission_intent.get('scope_window')}")
        freshness_parts: list[str] = []
        if mission_intent.get("freshness_expectation"):
            freshness_parts.append(str(mission_intent.get("freshness_expectation")))
        if mission_intent.get("freshness_max_age_hours"):
            freshness_parts.append(f"max_age<={int(mission_intent.get('freshness_max_age_hours', 0))}h")
        if freshness_parts:
            print(f"  freshness: {' | '.join(freshness_parts)}")

    if isinstance(last_failure, dict) and last_failure:
        print("last_failure:")
        print(
            f"  - {last_failure.get('id', '-')}"
            f" | status={last_failure.get('status', 'error')}"
            f" | trigger={last_failure.get('trigger', 'manual')}"
            f" | finished_at={last_failure.get('finished_at', '-')}"
        )
        print(f"    error: {last_failure.get('error', '-') or '-'}")

    if isinstance(retry_advice, dict) and retry_advice:
        print("retry_advice:")
        print(f"  failure_class: {retry_advice.get('failure_class', '-') or '-'}")
        print(f"  summary: {retry_advice.get('summary', '')}")
        print(f"  retry_command: {retry_advice.get('retry_command', '-') or '-'}")
        daemon_retry = str(retry_advice.get("daemon_retry_command", "") or "").strip()
        if daemon_retry:
            print(f"  daemon_retry_command: {daemon_retry}")
        suspected_collectors = retry_advice.get("suspected_collectors", [])
        if suspected_collectors:
            print("  suspected_collectors:")
            for collector in suspected_collectors:
                print(
                    f"    - {collector.get('name', '-')}"
                    f" | tier={collector.get('tier', '-')}"
                    f" | status={collector.get('status', '-')}"
                    f" | available={collector.get('available', True)}"
                )
                if collector.get("message"):
                    print(f"      message: {collector.get('message')}")
                if collector.get("setup_hint"):
                    print(f"      setup_hint: {collector.get('setup_hint')}")
        notes = retry_advice.get("notes", [])
        if notes:
            print("  notes:")
            for note in notes:
                print(f"    - {note}")

    runs = payload.get("runs", []) if isinstance(payload, dict) else []
    if runs:
        print("recent_runs:")
        for run in runs[:5]:
            print(
                f"  - {run.get('id', '-')}"
                f" | status={run.get('status', '-')}"
                f" | trigger={run.get('trigger', 'manual')}"
                f" | items={run.get('item_count', 0)}"
                f" | finished_at={run.get('finished_at', '-')}"
            )
            error = str(run.get("error", "") or "").strip()
            if error:
                print(f"    error: {error}")

    alerts = payload.get("recent_alerts", []) if isinstance(payload, dict) else []
    if alerts:
        print("recent_alerts:")
        for alert in alerts[:5]:
            delivered = ",".join(alert.get("delivered_channels", [])) or "json"
            print(
                f"  - {alert.get('id', '-')}"
                f" | rule={alert.get('rule_name', '-')}"
                f" | channels={delivered}"
                f" | created_at={alert.get('created_at', '-')}"
            )
            print(f"    summary: {alert.get('summary', '')}")

    results = payload.get("recent_results", []) if isinstance(payload, dict) else []
    if results:
        print("recent_results:")
        for item in results[:8]:
            print(
                f"  - {item.get('id', '-')}"
                f" | score={item.get('score', 0)}"
                f" | confidence={float(item.get('confidence', 0.0)):.3f}"
                f" | state={item.get('review_state', 'new')}"
            )
            print(f"    {item.get('title', '')}")
            print(f"    {item.get('url', '-')}")

    result_filters = payload.get("result_filters", {}) if isinstance(payload, dict) else {}
    if result_filters:
        print("result_filters:")
        for bucket_name in ("states", "sources", "domains"):
            rows = result_filters.get(bucket_name, [])
            if not rows:
                continue
            chips = ", ".join(
                f"{row.get('label', row.get('key', '-'))}({row.get('count', 0)})"
                for row in rows[:6]
            )
            print(f"  {bucket_name}: {chips}")

    timeline_strip = payload.get("timeline_strip", []) if isinstance(payload, dict) else []
    if timeline_strip:
        print("timeline_strip:")
        for event in timeline_strip[:6]:
            print(
                f"  - {event.get('time', '-')}"
                f" | {event.get('kind', '-')}"
                f" | {event.get('label', '-')}"
            )
            detail = str(event.get("detail", "") or "").strip()
            if detail:
                print(f"    detail: {detail}")


def _print_watch_results(items):
    for item in items:
        print(
            f"{item.get('id', '-')}: score={item.get('score', 0)}"
            f" | confidence={float(item.get('confidence', 0.0)):.3f}"
            f" | state={item.get('review_state', 'new')}"
            f" | source={item.get('source_name') or item.get('source_type') or '-'}"
        )
        print(f"    {item.get('title', '')}")
        print(f"    {item.get('url', '-')}")


def _print_triage_items(items):
    for item in items:
        state = item.get("review_state", "new")
        duplicate_of = item.get("duplicate_of") or "-"
        notes = len(item.get("review_notes", []) or [])
        print(
            f"{item.get('id')}: {state} | score={item.get('score', 0)} | "
            f"confidence={float(item.get('confidence', 0.0)):.3f} | notes={notes}"
        )
        print(f"    {item.get('title', '')}")
        print(f"    duplicate_of: {duplicate_of}")


def _print_triage_stats(payload):
    print(f"total: {payload.get('total', 0)}")
    print(f"open_count: {payload.get('open_count', 0)}")
    print(f"closed_count: {payload.get('closed_count', 0)}")
    print(f"processed_count: {payload.get('processed_count', 0)}")
    print(f"note_count: {payload.get('note_count', 0)}")
    states = payload.get("states", {}) if isinstance(payload, dict) else {}
    for state in ("new", "triaged", "verified", "duplicate", "ignored", "escalated"):
        print(f"{state}: {states.get(state, 0)}")


def _print_triage_explain(payload):
    item = payload.get("item", {}) if isinstance(payload, dict) else {}
    print(f"item: {item.get('id', '-')}")
    print(f"title: {item.get('title', '')}")
    print(f"suggested_primary_id: {payload.get('suggested_primary_id', '-')}")
    print(f"candidate_count: {payload.get('candidate_count', 0)}")
    print(f"returned_count: {payload.get('returned_count', 0)}")
    candidates = payload.get("candidates", []) if isinstance(payload, dict) else []
    if not candidates:
        print("No duplicate candidate found.")
        return
    for candidate in candidates:
        signals = ",".join(candidate.get("signals", [])) or "-"
        print(
            f"{candidate.get('id')}: similarity={float(candidate.get('similarity', 0.0)):.3f} | "
            f"state={candidate.get('review_state', 'new')} | signals={signals}"
        )
        print(f"    {candidate.get('title', '')}")


def _print_story_list(stories):
    for story in stories:
        print(
            f"{story.get('id')}: items={story.get('item_count', 0)} | "
            f"sources={story.get('source_count', 0)} | score={float(story.get('score', 0.0)):.1f} | "
            f"status={story.get('status', 'active')}"
        )
        print(f"    {story.get('title', '')}")


def _print_story_graph(payload):
    story = payload.get("story", {}) if isinstance(payload, dict) else {}
    print(f"story: {story.get('id', '-')}")
    print(f"title: {story.get('title', '')}")
    print(f"status: {story.get('status', 'active')}")
    print(f"entity_count: {payload.get('entity_count', 0)}")
    print(f"relation_count: {payload.get('relation_count', 0)}")
    print(f"edge_count: {payload.get('edge_count', 0)}")
    nodes = payload.get("nodes", []) if isinstance(payload, dict) else []
    edges = payload.get("edges", []) if isinstance(payload, dict) else []
    entity_nodes = [node for node in nodes if node.get("kind") == "entity"]
    if entity_nodes:
        print("entities:")
        for node in entity_nodes:
            print(
                f"  - {node.get('label', '')} | type={node.get('entity_type', 'UNKNOWN')} | "
                f"in_story_sources={node.get('in_story_source_count', 0)}"
            )
    if edges:
        print("edges:")
        for edge in edges:
            print(
                f"  - {edge.get('source')} -> {edge.get('target')} | "
                f"{edge.get('relation_type', 'RELATED')} | kind={edge.get('kind', '-')}"
            )


def _build_watch_alert_rules_from_args(args) -> list[dict[str, Any]] | None:
    if not any(
        value is not None and value != []
        for value in (
            args.watch_alert_name,
            args.watch_alert_min_score,
            args.watch_alert_min_confidence,
            args.watch_alert_channel,
            args.watch_alert_route,
            args.watch_alert_keyword,
            args.watch_alert_keyword_all,
            args.watch_alert_exclude_keyword,
            args.watch_alert_required_tag,
            args.watch_alert_excluded_tag,
            args.watch_alert_domain,
            args.watch_alert_source_type,
            args.watch_alert_max_age_minutes,
        )
    ):
        return None

    alert_rule: dict[str, Any] = {
        "name": args.watch_alert_name or "threshold",
        "min_score": args.watch_alert_min_score or 0,
        "min_confidence": args.watch_alert_min_confidence or 0.0,
        "min_results": max(1, args.watch_alert_min_results),
        "cooldown_seconds": max(0, args.watch_alert_cooldown),
        "channels": args.watch_alert_channel or ["json"],
    }
    if args.watch_alert_route:
        alert_rule["routes"] = args.watch_alert_route
    if args.watch_alert_keyword:
        alert_rule["keyword_any"] = args.watch_alert_keyword
    if args.watch_alert_keyword_all:
        alert_rule["keyword_all"] = args.watch_alert_keyword_all
    if args.watch_alert_exclude_keyword:
        alert_rule["exclude_keywords"] = args.watch_alert_exclude_keyword
    if args.watch_alert_required_tag:
        alert_rule["required_tags"] = args.watch_alert_required_tag
    if args.watch_alert_excluded_tag:
        alert_rule["excluded_tags"] = args.watch_alert_excluded_tag
    if args.watch_alert_domain:
        alert_rule["domains"] = args.watch_alert_domain
    if args.watch_alert_source_type:
        alert_rule["source_types"] = args.watch_alert_source_type
    if args.watch_alert_max_age_minutes:
        alert_rule["max_age_minutes"] = max(1, args.watch_alert_max_age_minutes)
    return [alert_rule]


_FIX_COMMANDS_BY_COLLECTOR = {
    "xhs": ["datapulse --login xhs"],
    "wechat": ["datapulse --login wechat"],
    "telegram": [
        'pip install -e ".[telegram]"',
        "export TG_API_ID=<your_tg_api_id>",
        "export TG_API_HASH=<your_tg_api_hash>",
    ],
    "jina": ["export JINA_API_KEY=<your_jina_api_key>"],
    "generic": ["pip install trafilatura"],
    "youtube": [
        "pip install -e \".[youtube]\"",
        "export GROQ_API_KEY=<your_groq_api_key>",
    ],
    "twitter": ["curl -I https://api.fxtwitter.com"],
}


def _search_gateway_defaults() -> dict[str, tuple[object, object, str]]:
    """Collect effective and default SearchGateway values for quick diagnostics."""

    effective = SearchGatewayConfig.load()
    default = SearchGatewayConfig()
    return {
        "DATAPULSE_SEARCH_TIMEOUT": (
            effective.timeout_seconds,
            default.timeout_seconds,
            "search timeout (seconds)",
        ),
        "DATAPULSE_SEARCH_RETRY_ATTEMPTS": (
            effective.retry_attempts,
            default.retry_attempts,
            "retry attempts",
        ),
        "DATAPULSE_SEARCH_RETRY_BASE_DELAY": (
            effective.retry_base_delay,
            default.retry_base_delay,
            "retry base delay (s)",
        ),
        "DATAPULSE_SEARCH_RETRY_MAX_DELAY_SECONDS": (
            effective.retry_max_delay,
            default.retry_max_delay,
            "retry max delay (s)",
        ),
        "DATAPULSE_SEARCH_RETRY_BACKOFF": (
            effective.retry_backoff_factor,
            default.retry_backoff_factor,
            "retry backoff factor",
        ),
        "DATAPULSE_SEARCH_RETRY_RESPECT_RETRY_AFTER": (
            effective.retry_respect_retry_after,
            default.retry_respect_retry_after,
            "respect Retry-After",
        ),
        "DATAPULSE_SEARCH_CB_FAILURE_THRESHOLD": (
            effective.breaker_failure_threshold,
            default.breaker_failure_threshold,
            "circuit breaker failure threshold",
        ),
        "DATAPULSE_SEARCH_CB_RECOVERY_TIMEOUT": (
            effective.breaker_recovery_timeout,
            default.breaker_recovery_timeout,
            "circuit breaker recovery timeout (s)",
        ),
        "DATAPULSE_SEARCH_CB_RATE_LIMIT_WEIGHT": (
            effective.breaker_rate_limit_weight,
            default.breaker_rate_limit_weight,
            "circuit breaker rate-limit weight",
        ),
        "DATAPULSE_SEARCH_PROVIDER_PRECEDENCE": (
            ",".join(effective.provider_preference),
            ",".join(default.provider_preference),
            "provider preference",
        ),
    }


def _format_env_value(value: str | None) -> str:
    if value is None:
        return ""
    text = value.strip()
    if not text:
        return "<empty>"
    if len(text) <= 28:
        return text
    return f"{text[:22]}..."


def _collect_fix_commands(collector_name: str, setup_hint: str) -> list[str]:
    commands: list[str] = []
    commands.extend(_FIX_COMMANDS_BY_COLLECTOR.get(collector_name, []))

    run_hints = re.findall(r"Run:\s*([^;\n]+)", setup_hint, flags=re.IGNORECASE)
    if run_hints:
        commands.extend([h.strip() for h in run_hints])

    for match in re.findall(r"Set\s+([A-Z0-9_]+(?:\s+and\s+[A-Z0-9_]+)*)", setup_hint, flags=re.IGNORECASE):
        for env_name in re.findall(r"[A-Z0-9_]+", match):
            if env_name:
                commands.append(f"export {env_name}=<{env_name.lower()}>")

    pip_hints = re.findall(r"pip\s+install\s+[^;\n]+", setup_hint, flags=re.IGNORECASE)
    if pip_hints:
        commands.extend([h.strip() for h in pip_hints])

    out: list[str] = []
    seen: set[str] = set()
    for cmd in commands:
        if cmd and cmd not in seen:
            seen.add(cmd)
            out.append(cmd)

    return out


def _print_doctor_report(report: dict[str, list[dict[str, str | bool]]]) -> None:
    tier_labels = {
        "tier_0": "Zero-config",
        "tier_1": "Network / Free",
        "tier_2": "Needs Setup",
    }

    for tier_key in ("tier_0", "tier_1", "tier_2"):
        entries = report.get(tier_key, [])
        if not entries:
            continue
        print(f"\n  {tier_labels[tier_key]} (tier {tier_key[-1]})")
        print(f"  {'─' * 50}")
        for e in entries:
            status = e.get("status", "ok")
            icon = "[OK]" if status == "ok" else "[WARN]" if status == "warn" else "[ERR]"
            name = e.get("name", "?")
            msg = e.get("message", "")
            hint = e.get("setup_hint", "")
            print(f"  {icon:6s} {name:<14s} {msg}")
            if hint:
                print(f"         Hint: {hint}")

            if status != "ok":
                commands = _collect_fix_commands(str(name), str(hint))
                if commands:
                    print("         建议执行：")
                    for cmd in commands:
                        print(f"           - {cmd}")

    print("\nSearchGateway runtime defaults:")
    for env_name, (value, default, desc) in _search_gateway_defaults().items():
        marker = "default" if value == default else "override"
        print(f"  - {env_name} = {value} ({desc}, {marker})")


def _print_config_check() -> None:
    print("=== DataPulse Config Check ===")
    print("\n1) Must-have environment variables")
    print("   - None (bootstrap is runnable without mandatory env variables)")

    print("\n2) Optional environment variables")

    # Search provider keys (at least one is enough for robust search)
    has_jina = bool(os.getenv("JINA_API_KEY", "").strip())
    has_tavily = bool(os.getenv("TAVILY_API_KEY", "").strip())
    if has_jina and has_tavily:
        print("   [OK] Search keys: JINA_API_KEY + TAVILY_API_KEY")
    elif has_jina or has_tavily:
        print("   [WARN] Search keys: only one search key is set")
    else:
        print("   [WARN] Search keys: neither JINA_API_KEY nor TAVILY_API_KEY set")
        print("         Recommended fix:")
        print("           - export JINA_API_KEY=<your_jina_api_key>")
        print("           - export TAVILY_API_KEY=<your_tavily_api_key>")

    # Telegram credentials
    has_tg_id = bool(os.getenv("TG_API_ID", "").strip())
    has_tg_hash = bool(os.getenv("TG_API_HASH", "").strip())
    if has_tg_id and has_tg_hash:
        print("   [OK] Telegram credentials: TG_API_ID + TG_API_HASH")
    else:
        print("   [WARN] Telegram credentials: TG_API_ID / TG_API_HASH")
        print("         Recommended fix:")
        print("           - export TG_API_ID=<your_tg_api_id>")
        print("           - export TG_API_HASH=<your_tg_api_hash>")

    # General optional keys (display current/placeholder for fast onboarding)
    optional_envs = [
        "FIRECRAWL_API_KEY",
        "GROQ_API_KEY",
        "NITTER_INSTANCES",
        "FXTWITTER_API_URL",
        "DATAPULSE_SESSION_DIR",
        "DATAPULSE_BATCH_CONCURRENCY",
        "DATAPULSE_MIN_CONFIDENCE",
        "DATAPULSE_LOG_LEVEL",
    ]

    for env_name in optional_envs:
        present = _format_env_value(os.getenv(env_name, ""))
        status = "[OK]" if present not in ("", "<empty>") else "[WARN]"
        print(f"   {status} {env_name}: {present or 'not set'}")

    print("\nSearchGateway tuning (effective / default):")
    for env_name, (value, default, desc) in _search_gateway_defaults().items():
        marker = "default" if value == default else "override"
        print(f"   - {env_name}: {value} ({desc}, {marker})")



def _normalize_csv_ids(value: str | None) -> list[str] | None:
    if not value:
        return None
    return [item.strip() for item in value.split(",") if item.strip()]


def _version_tuple(version: str) -> tuple[int, ...]:
    cleaned = (version or "").lstrip("vV").strip()
    parts = [int(part) for part in re.findall(r"\d+", cleaned)]
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])


def _fetch_latest_release_tag() -> tuple[str | None, str | None]:
    try:
        request = Request(
            _GITHUB_RELEASES_API,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "datapulse-cli",
            },
        )
        with urlopen(request, timeout=8) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="ignore"))
            latest_tag = payload.get("tag_name")
            if isinstance(latest_tag, str):
                return latest_tag.strip(), None
            return None, "GitHub release API did not return tag_name"
    except (HTTPError, URLError, ValueError, TimeoutError, OSError) as exc:
        return None, str(exc)


def _print_version() -> None:
    print(f"DataPulse v{datapulse.__version__}")


def _print_update_status() -> None:
    current = datapulse.__version__
    latest_tag, error = _fetch_latest_release_tag()

    print(f"Current version: v{current}")
    if not latest_tag:
        print("Latest version: unavailable")
        if error:
            print(f"Update check failed: {error}")
        return

    latest = latest_tag.lstrip("vV")
    print(f"Latest version: v{latest}")
    if _version_tuple(latest) <= _version_tuple(current):
        print("✅ Already up to date")
        return

    print("🔔 Update available")
    print("   Recommended: datapulse --self-update")


def _run_self_update() -> None:
    current = datapulse.__version__
    latest_tag, error = _fetch_latest_release_tag()
    if not latest_tag:
        print("❌ Failed to check latest release before update")
        if error:
            print(f"   Detail: {error}")
        return

    latest = latest_tag.lstrip("vV")
    print(f"Current version: v{current}")
    print(f"Latest version: v{latest}")

    if _version_tuple(latest) <= _version_tuple(current):
        print("✅ Already up to date, no update needed")
        return

    command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--upgrade",
        f"git+{_GITHUB_REPO}@{latest_tag}",
    ]
    print("🚀 Running update command:")
    print(f"   {' '.join(shlex.quote(part) for part in command)}")
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError as exc:
        print(f"❌ Update failed: {exc}")
    except subprocess.CalledProcessError as exc:
        print(f"❌ Update failed with exit code {exc.returncode}")
        print("   You may manually run:")
        print(f"   {sys.executable} -m pip install --upgrade 'git+{_GITHUB_REPO}@{latest_tag}'")
    else:
        print("✅ Update command completed. Please restart your CLI session.")


def _load_skill_manifest() -> dict[str, Any]:
    manifest_path = Path(__file__).resolve().parent.parent / "datapulse_skill" / "manifest.json"
    if not manifest_path.exists():
        return {}

    try:
        content = manifest_path.read_text(encoding="utf-8")
        payload: Any = json.loads(content)
        if isinstance(payload, dict):
            return payload
    except Exception:
        return {}
    return {}


def _collect_mcp_tool_contract() -> list[dict[str, Any]]:
    try:
        from datapulse import mcp_server

        app = mcp_server._LocalMCP("datapulse")
        mcp_server._register_tools(app)
        contract: list[dict[str, Any]] = []
        for item in sorted(app._tool_metadata(), key=lambda x: x["name"]):
            input_schema = item.get("inputSchema", {})
            props = input_schema.get("properties", {})
            required = set(input_schema.get("required", []) or [])
            args = sorted(props) if isinstance(props, dict) else []
            contract.append(
                {
                    "name": item.get("name"),
                    "description": item.get("description", ""),
                    "required_args": sorted(required),
                    "optional_args": [arg for arg in args if arg not in required],
                }
            )
        return contract
    except Exception:
        return []


def _print_skill_contract() -> None:
    manifest = _load_skill_manifest()
    mcp_tools = _collect_mcp_tool_contract()

    contract: dict[str, Any] = {
        "name": manifest.get("name", "DataPulse"),
        "description": manifest.get("description", "Cross-platform data intake and confidence-aware workflow."),
        "version": datapulse.__version__,
        "entry_points": {
            "cli": "datapulse",
            "mcp": "python3 -m datapulse.mcp_server",
            "skill": "datapulse_skill",
        },
        "agent_triggers": manifest.get("triggers", []),
        "capabilities": manifest.get("capabilities", []),
        "memory_path": manifest.get("memory_path"),
        "arguments": {
            "flags": [
                "--search / -s",
                "--trending / -T",
                "--batch / -b",
                "--entities",
                "--watch-create",
                "--watch-list",
                "--watch-alert-set",
                "--watch-alert-clear",
                "--watch-show",
                "--watch-results",
                "--watch-run",
                "--watch-run-due",
                "--watch-daemon",
                "--alert-list",
                "--alert-route-list",
                "--alert-route-health",
                "--watch-status",
                "--ops-overview",
                "--triage-list",
                "--triage-explain",
                "--triage-update",
                "--triage-note",
                "--triage-stats",
                "--story-build",
                "--story-list",
                "--story-show",
                "--story-update",
                "--story-graph",
                "--story-export",
                "--doctor",
                "--config-check",
                "--troubleshoot",
                "--skill-contract",
                "--check-update",
                "--self-update",
                "--version",
            ],
            "env": {
                "DATAPULSE_MIN_CONFIDENCE": "Global minimum confidence",
                "DATAPULSE_BATCH_CONCURRENCY": "Read concurrency override",
                "DATAPULSE_LOG_LEVEL": "Log verbosity",
                "DATAPULSE_WATCHLIST_PATH": "Watch mission storage file",
                "DATAPULSE_ALERTS_PATH": "Alert event storage file",
                "DATAPULSE_ALERTS_MARKDOWN_PATH": "Alert markdown sink",
                "DATAPULSE_ALERT_ROUTING_PATH": "Named alert route config file",
                "DATAPULSE_ALERT_WEBHOOK_URL": "Default webhook alert sink",
                "DATAPULSE_FEISHU_WEBHOOK_URL": "Default Feishu webhook",
                "DATAPULSE_TELEGRAM_BOT_TOKEN": "Telegram bot token for alerts",
                "DATAPULSE_TELEGRAM_CHAT_ID": "Telegram chat id for alerts",
                "DATAPULSE_WATCH_DAEMON_LOCK": "Single-instance daemon lock file",
                "DATAPULSE_WATCH_STATUS_PATH": "Daemon JSON heartbeat file",
                "DATAPULSE_WATCH_STATUS_HTML": "Daemon HTML status page",
                "DATAPULSE_STORIES_PATH": "Story workspace storage file",
            },
        },
        "mcp_tools": mcp_tools,
        "recommended_workflows": [
            "for ingestion of URLs: datapulse --batch",
            "for discovery: datapulse --search",
            "for recurring themes: --watch-create/--watch-list/--watch-run",
            "for alert rule tuning: --watch-alert-set/--watch-alert-clear",
            "for scheduled recurring themes: --watch-run-due",
            "for daemon polling: --watch-daemon --watch-daemon-once",
            "for alert review: --alert-list",
            "for route audit: --alert-route-list",
            "for daemon status: --watch-status",
            "for analyst queue operations: --triage-list/--triage-explain/--triage-update/--triage-note/--triage-stats",
            "for story workspace: --story-build/--story-list/--story-show/--story-update/--story-graph/--story-export",
            "for source governance: --list-sources/--list-packs/--query-feed",
            "for health checks: --doctor / --troubleshoot",
        ],
    }

    print(json.dumps(contract, ensure_ascii=False, indent=2))


def _print_troubleshoot_report(
    report: dict[str, list[dict[str, str | bool]]],
    target: str | None = None,
) -> None:
    target_norm = (target or "").strip().lower()
    filtered: list[tuple[str, dict[str, str | bool]]] = []
    found_target = False

    for tier_key, entries in report.items():
        for entry in entries:
            name = str(entry.get("name", "")).strip()
            if target and name.lower() != target_norm:
                continue
            status = str(entry.get("status", "unknown"))
            if target and status:
                found_target = True
            if status != "ok":
                filtered.append((tier_key, entry))

    if target and not found_target:
        print(f"⚠️  No collector named '{target}' in doctor report")
        return

    print("🩺 DataPulse Troubleshoot")
    if not filtered:
        if target:
            print(f"✅ Collector '{target}' is healthy")
        else:
            print("✅ No failing collectors found in current environment")
        return

    for tier_key, entry in filtered:
        name = str(entry.get("name", "unknown"))
        status = str(entry.get("status", "warn"))
        msg = str(entry.get("message", "")).strip()
        hint = str(entry.get("setup_hint", "")).strip()

        print(f"- {name} [{tier_key}] ({status})")
        if msg:
            print(f"  message: {msg}")
        if hint:
            print(f"  hint: {hint}")
        commands = _collect_fix_commands(name, hint)
        if commands:
            print("  suggested commands:")
            for cmd in commands:
                print(f"    - {cmd}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="DataPulse Intelligence Hub",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "\nScenario snippets:\n"
            "A) Parse one URL:          datapulse <url>\n"
            "B) Parse URL batch:         datapulse --batch <url1> <url2>\n"
            "C) Web search:              datapulse --search <query> [--search-limit N]\n"
            "D) Trending topics:         datapulse --trending [us|uk|jp]\n"
            "E) Entity workflow:         datapulse <url> --entities --entity-mode fast\n"
            "F) Watch mission:           datapulse --watch-create --watch-name <name> --watch-query <query>\n"
            "G) Watch cockpit:           datapulse --watch-show <watch_id>\n"
            "H) Watch scheduler:         datapulse --watch-run-due\n"
            "I) Watch daemon:            datapulse --watch-daemon --watch-daemon-once\n"
            "J) Watch status:            datapulse --watch-status / --alert-route-health / --ops-overview\n"
            "K) Triage queue:            datapulse --triage-list / --triage-update <item_id> --triage-state verified\n"
            "L) Story workspace:         datapulse --story-build / --story-list / --story-show <story_id> / --story-update <story_id>\n"
            "Diagnostics: datapulse --config-check / --doctor / --troubleshoot / --skill-contract / --check-update / --self-update / --version"
        ),
    )
    parser.add_argument("inputs", nargs="*", help="URLs or commands")

    parsing_group = parser.add_argument_group("解析类")
    search_group = parser.add_argument_group("搜索类")
    management_group = parser.add_argument_group("管理类")
    diagnostic_group = parser.add_argument_group("诊断类")

    parsing_group.add_argument(
        "-b",
        "--batch",
        nargs="+",
        help="Process a batch of URLs",
    )
    parsing_group.add_argument(
        "--entities",
        action="store_true",
        help="Extract entities while reading URL inputs",
    )
    parsing_group.add_argument(
        "--entity-mode",
        default="fast",
        choices=["fast", "llm"],
        help="Entity extraction mode",
    )
    parsing_group.add_argument(
        "--entity-store",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Persist extracted entities to local entity store",
    )
    parsing_group.add_argument("--target-selector", metavar="CSS", help="CSS selector for targeted extraction")
    parsing_group.add_argument("--no-cache", action="store_true", help="Bypass Jina cache")
    parsing_group.add_argument("--with-alt", action="store_true", help="Enable AI image descriptions via Jina")
    parsing_group.add_argument(
        "--min-confidence",
        type=float,
        default=0.0,
        help="Filter by confidence",
    )
    parsing_group.add_argument("--list", "-l", action="store_true", help="List inbox")
    parsing_group.add_argument("--clear", action="store_true", help="Clear inbox")

    search_group.add_argument("-s", "--search", metavar="QUERY", help="Search the web")
    search_group.add_argument(
        "-S",
        "--site",
        action="append",
        metavar="DOMAIN",
        help="Restrict search to domain (repeatable)",
    )
    search_group.add_argument("--search-limit", type=int, default=5, help="Max search results (default 5)")
    search_group.add_argument("--no-fetch", action="store_true", help="Skip full content fetch for search results")
    search_group.add_argument(
        "--search-provider",
        default="auto",
        choices=["auto", "jina", "tavily", "multi"],
        help="Search provider: auto/jina/tavily/multi",
    )
    search_group.add_argument(
        "--search-mode",
        default="single",
        choices=["single", "multi"],
        help="Search mode: single (fallback) / multi (fused)",
    )
    search_group.add_argument("--search-deep", action="store_true", help="Enable deep search depth (Tavily)")
    search_group.add_argument("--search-news", action="store_true", help="Enable news-only retrieval (Tavily)")
    search_group.add_argument("--search-time-range", choices=["day", "week", "month", "year"], help="Time range filter (Tavily)")
    search_group.add_argument("--search-freshness", choices=["day", "week", "month", "year"], help="Alias for time range filter")
    search_group.add_argument(
        "--platform",
        choices=["xhs", "twitter", "reddit", "hackernews", "arxiv", "bilibili"],
        help="Restrict search to a specific platform",
    )
    search_group.add_argument(
        "-T",
        "--trending",
        nargs="?",
        const="",
        metavar="LOCATION",
        help="Show trending topics (default: worldwide). Locations: us, uk, jp, etc.",
    )
    search_group.add_argument("--trending-limit", type=int, default=20, help="Max trending topics (default 20)")
    search_group.add_argument("--trending-store", action="store_true", help="Save trending snapshot to inbox")
    search_group.add_argument("--trending-validate", action="store_true", help="Use cross-validated trending strategy")
    search_group.add_argument("--trending-validate-mode", default="strict", choices=["strict", "news", "lenient"], help="Trending validate mode")

    management_group.add_argument(
        "--source-profile",
        default="default",
        help="Source profile for feed/subscription ops",
    )
    management_group.add_argument("--source-ids", help="Comma separated source IDs for query_feed")
    management_group.add_argument("--list-sources", action="store_true", help="List source catalog entries")
    management_group.add_argument("--list-packs", action="store_true", help="List source packs")
    management_group.add_argument("--limit", type=int, default=20, help="List/feed/feed-like limit")
    management_group.add_argument("--include-inactive-sources", action="store_true", help="Include inactive sources")
    management_group.add_argument("--public-sources-only", action="store_true", help="Only list public sources")
    management_group.add_argument("--resolve-source", metavar="URL", help="Resolve source metadata for a URL")
    management_group.add_argument("--source-subscribe", metavar="SOURCE_ID", help="Subscribe profile source")
    management_group.add_argument("--source-unsubscribe", metavar="SOURCE_ID", help="Unsubscribe profile source")
    management_group.add_argument("--install-pack", metavar="PACK_SLUG", help="Install source pack to profile")
    management_group.add_argument("--query-feed", action="store_true", help="Print JSON feed output")
    management_group.add_argument("--query-rss", action="store_true", help="Print RSS feed output")
    management_group.add_argument("--query-atom", action="store_true", help="Print Atom 1.0 feed output")
    management_group.add_argument("--digest", action="store_true", help="Build curated digest")
    management_group.add_argument("--emit-digest-package", action="store_true", help="Export minimal office-ready digest package")
    management_group.add_argument("--emit-digest-format", default="json", choices=["json", "markdown", "md"], help="Digest package output format")
    management_group.add_argument("--top-n", type=int, default=3, help="Number of primary stories in digest")
    management_group.add_argument("--secondary-n", type=int, default=7, help="Number of secondary stories in digest")
    management_group.add_argument("--entity-query", help="Query entities from store by name")
    management_group.add_argument("--entity-type", help="Filter entity query by type")
    management_group.add_argument("--entity-limit", type=int, default=50, help="Limit for entity query")
    management_group.add_argument("--entity-min-sources", type=int, default=1, help="Minimum source count for entity query")
    management_group.add_argument("--entity-graph", help="Show related entities for one entity name")
    management_group.add_argument("--entity-stats", action="store_true", help="Show entity store stats")
    management_group.add_argument("--watch-create", action="store_true", help="Create a recurring watch mission")
    management_group.add_argument("--watch-list", action="store_true", help="List watch missions")
    management_group.add_argument("--watch-alert-set", metavar="WATCH", help="Replace alert rules for one watch mission")
    management_group.add_argument("--watch-alert-clear", metavar="WATCH", help="Clear alert rules for one watch mission")
    management_group.add_argument(
        "--watch-show",
        metavar="WATCH",
        help="Show one watch mission with run history, persisted results, alert history, and retry advice",
    )
    management_group.add_argument("--watch-results", metavar="WATCH", help="Show recent persisted results for one watch mission")
    management_group.add_argument("--watch-run", metavar="WATCH", help="Run one watch mission by id or name")
    management_group.add_argument("--watch-run-due", action="store_true", help="Run all due watch missions once")
    management_group.add_argument("--watch-daemon", action="store_true", help="Run the watch scheduler daemon loop")
    management_group.add_argument("--watch-daemon-once", action="store_true", help="Run one daemon cycle and exit")
    management_group.add_argument("--watch-status", action="store_true", help="Show watch daemon heartbeat and metrics")
    management_group.add_argument("--watch-disable", metavar="WATCH", help="Disable one watch mission by id or name")
    management_group.add_argument("--watch-name", help="Watch mission name (used with --watch-create)")
    management_group.add_argument("--watch-query", help="Watch mission query (used with --watch-create)")
    management_group.add_argument(
        "--watch-platform",
        action="append",
        choices=["xhs", "twitter", "reddit", "hackernews", "arxiv", "bilibili"],
        help="Restrict watch mission to platform (repeatable)",
    )
    management_group.add_argument("--watch-site", action="append", metavar="DOMAIN", help="Restrict watch mission to domain (repeatable)")
    management_group.add_argument("--watch-schedule", default="manual", help="Mission schedule label (default manual)")
    management_group.add_argument("--watch-top-n", type=int, default=5, help="Max watch results to keep (default 5)")
    management_group.add_argument("--watch-results-limit", type=int, default=10, help="Max persisted watch results to show")
    management_group.add_argument("--watch-min-confidence", type=float, default=0.0, help="Stored watch confidence threshold")
    management_group.add_argument("--watch-include-disabled", action="store_true", help="Include disabled watch missions in --watch-list")
    management_group.add_argument("--watch-due-limit", type=int, default=0, help="Max due watch missions to run (0 = all due)")
    management_group.add_argument("--watch-alert-name", help="Threshold alert rule name for one watch mission")
    management_group.add_argument("--watch-alert-min-score", type=int, help="Trigger alert when score >= N")
    management_group.add_argument("--watch-alert-min-confidence", type=float, help="Trigger alert when confidence >= N")
    management_group.add_argument("--watch-alert-min-results", type=int, default=1, help="Trigger alert when at least N items match")
    management_group.add_argument("--watch-alert-cooldown", type=int, default=0, help="Suppress duplicate alert for N seconds")
    management_group.add_argument("--watch-alert-route", action="append", help="Named delivery route from DATAPULSE_ALERT_ROUTING_PATH (repeatable)")
    management_group.add_argument("--watch-alert-keyword", action="append", help="Alert only when any keyword is present (repeatable)")
    management_group.add_argument("--watch-alert-keyword-all", action="append", help="Alert only when all keywords are present (repeatable)")
    management_group.add_argument("--watch-alert-exclude-keyword", action="append", help="Suppress alert when keyword is present (repeatable)")
    management_group.add_argument("--watch-alert-required-tag", action="append", help="Require item tags for alert match (repeatable)")
    management_group.add_argument("--watch-alert-excluded-tag", action="append", help="Block alert when item tags are present (repeatable)")
    management_group.add_argument("--watch-alert-domain", action="append", help="Restrict alert match to domains (repeatable)")
    management_group.add_argument("--watch-alert-source-type", action="append", help="Restrict alert match to source types (repeatable)")
    management_group.add_argument("--watch-alert-max-age-minutes", type=int, help="Only alert on items newer than N minutes")
    management_group.add_argument(
        "--watch-alert-channel",
        action="append",
        choices=["json", "markdown", "webhook", "feishu", "telegram"],
        help="Alert delivery channel for one watch mission rule",
    )
    management_group.add_argument("--alert-list", action="store_true", help="List stored watch alert events")
    management_group.add_argument("--alert-route-list", action="store_true", help="List configured named alert routes")
    management_group.add_argument("--alert-route-health", action="store_true", help="Show delivery health for named alert routes")
    management_group.add_argument("--alert-limit", type=int, default=20, help="Max alert events to print")
    management_group.add_argument("--alert-route-health-limit", type=int, default=100, help="Max alert events to aggregate for route health")
    management_group.add_argument("--alert-mission", help="Filter alert list by mission id")
    management_group.add_argument("--ops-overview", action="store_true", help="Show unified ops snapshot across collectors, watches, and route delivery")
    management_group.add_argument("--watch-daemon-poll-seconds", type=float, default=60.0, help="Daemon poll interval in seconds")
    management_group.add_argument("--watch-daemon-cycles", type=int, default=0, help="Stop daemon after N cycles (0 = run forever)")
    management_group.add_argument("--watch-daemon-retry-attempts", type=int, default=1, help="Retry attempts per scheduled mission")
    management_group.add_argument("--watch-daemon-retry-base-delay", type=float, default=1.0, help="Retry base delay in seconds")
    management_group.add_argument("--watch-daemon-retry-max-delay", type=float, default=30.0, help="Retry max delay in seconds")
    management_group.add_argument("--watch-daemon-retry-backoff", type=float, default=2.0, help="Retry backoff factor")
    management_group.add_argument("--triage-list", action="store_true", help="List triage queue items")
    management_group.add_argument("--triage-explain", metavar="ITEM_ID", help="Explain duplicate candidates for one inbox item")
    management_group.add_argument("--triage-update", metavar="ITEM_ID", help="Update triage state for one inbox item")
    management_group.add_argument("--triage-note", metavar="ITEM_ID", help="Append one triage note to an inbox item")
    management_group.add_argument("--triage-stats", action="store_true", help="Show triage queue stats")
    management_group.add_argument("--triage-explain-limit", type=int, default=5, help="Max duplicate candidates to print for --triage-explain")
    management_group.add_argument(
        "--triage-state",
        action="append",
        choices=["new", "triaged", "verified", "duplicate", "ignored", "escalated"],
        help="Target triage state for update or list filter (repeatable on --triage-list)",
    )
    management_group.add_argument("--triage-note-text", help="Triage note text for update/note commands")
    management_group.add_argument("--triage-author", default="cli", help="Actor label for triage updates")
    management_group.add_argument("--triage-duplicate-of", metavar="ITEM_ID", help="Canonical item id when state=duplicate")
    management_group.add_argument("--triage-include-closed", action="store_true", help="Include verified/duplicate/ignored in --triage-list")
    management_group.add_argument("--story-build", action="store_true", help="Build and persist clustered story workspace snapshot")
    management_group.add_argument("--story-list", action="store_true", help="List persisted stories")
    management_group.add_argument("--story-show", metavar="STORY", help="Show one persisted story by id or title")
    management_group.add_argument("--story-update", metavar="STORY", help="Update one persisted story by id or title")
    management_group.add_argument("--story-graph", metavar="STORY", help="Show entity graph for one persisted story")
    management_group.add_argument("--story-export", metavar="STORY", help="Export one story as json or markdown")
    management_group.add_argument("--story-limit", type=int, default=10, help="Max stories to build or list")
    management_group.add_argument("--story-evidence-limit", type=int, default=6, help="Evidence items to keep per story")
    management_group.add_argument("--story-min-items", type=int, default=1, help="Minimum clustered items when listing stories")
    management_group.add_argument("--story-title", help="Replacement title for --story-update")
    management_group.add_argument("--story-summary", help="Replacement summary for --story-update (empty string clears it)")
    management_group.add_argument("--story-status", help="Replacement status for --story-update")
    management_group.add_argument("--story-graph-entity-limit", type=int, default=12, help="Max entity nodes for --story-graph")
    management_group.add_argument("--story-graph-relation-limit", type=int, default=24, help="Max relation edges for --story-graph")
    management_group.add_argument("--story-format", default="json", choices=["json", "markdown", "md"], help="Output format for --story-export")
    management_group.add_argument(
        "-i",
        "--login",
        choices=supported_platforms(),
        help="Capture browser login state for platform (xhs, wechat)",
    )

    diagnostic_group.add_argument("-d", "--doctor", action="store_true", help="Run health checks on all collectors")
    diagnostic_group.add_argument("--troubleshoot", nargs="?", const="", metavar="COLLECTOR", help="Show actionable fix suggestions; optionally specify one collector")
    diagnostic_group.add_argument(
        "--skill-contract",
        action="store_true",
        help="Print skill contract and tool descriptors for agent/agentic integrations",
    )
    diagnostic_group.add_argument(
        "--self-update",
        action="store_true",
        help="Upgrade DataPulse from GitHub repo",
    )
    diagnostic_group.add_argument(
        "--check-update",
        action="store_true",
        help="Check latest release tag on GitHub",
    )
    diagnostic_group.add_argument(
        "--version",
        action="store_true",
        help="Show DataPulse version",
    )
    diagnostic_group.add_argument(
        "-k",
        "--config-check",
        action="store_true",
        help="Check optional config completeness and show fix suggestions",
    )
    args = parser.parse_args()

    reader = DataPulseReader()

    if args.list:
        _print_list(reader.list_memory(limit=args.limit, min_confidence=args.min_confidence), limit=args.limit)
        return

    if args.login:
        try:
            path = login_platform(args.login)
            print(f"✅ Saved {args.login} session: {path}")
        except KeyboardInterrupt:
            print("⚠️ Login cancelled.")
        except Exception as exc:
            print(f"❌ Login failed: {exc}")
        return

    if args.doctor:
        report = reader.doctor()
        _print_doctor_report(report)
        return

    if args.troubleshoot is not None:
        report = reader.doctor()
        target = args.troubleshoot.strip() if isinstance(args.troubleshoot, str) else None
        target = target or None
        _print_troubleshoot_report(report, target=target)
        return

    if args.self_update:
        _run_self_update()
        return

    if args.skill_contract:
        _print_skill_contract()
        return

    if args.check_update:
        _print_update_status()
        return

    if args.version:
        _print_version()
        return

    if args.config_check:
        _print_config_check()
        return

    if args.clear:
        inbox_path = reader.inbox.path
        if inbox_path.exists():
            inbox_path.write_text("[]", encoding="utf-8")
            print(f"✅ Cleared inbox: {inbox_path}")
        else:
            print("ℹ️ Inbox already empty")
        return

    if args.list_sources:
        public_only = True
        if args.include_inactive_sources:
            public_only = bool(args.public_sources_only)
        sources = reader.list_sources(
            include_inactive=args.include_inactive_sources,
            public_only=public_only,
        )
        if not sources:
            print("No source in catalog.")
        else:
            print(f"📚 Sources: {len(sources)}")
            _print_sources(sources)
        return

    if args.list_packs:
        packs = reader.list_packs(public_only=True)
        if not packs:
            print("No source pack in catalog.")
        else:
            print(f"📦 Source packs: {len(packs)}")
            _print_packs(packs)
        return

    if args.resolve_source:
        print(json.dumps(reader.resolve_source(args.resolve_source), ensure_ascii=False, indent=2))
        return

    if args.source_subscribe:
        ok = reader.subscribe_source(args.source_subscribe, profile=args.source_profile)
        print("✅ subscribed" if ok else "⚠️ already subscribed or invalid source")
        return

    if args.source_unsubscribe:
        ok = reader.unsubscribe_source(args.source_unsubscribe, profile=args.source_profile)
        print("✅ unsubscribed" if ok else "⚠️ source not found in subscription")
        return

    if args.install_pack:
        count = reader.install_pack(args.install_pack, profile=args.source_profile)
        print(f"✅ installed {count} source(s) from pack")
        return

    if args.watch_create:
        if not args.watch_name or not args.watch_query:
            parser.error("--watch-create requires --watch-name and --watch-query")
        alert_rules = _build_watch_alert_rules_from_args(args)
        mission = reader.create_watch(
            name=args.watch_name,
            query=args.watch_query,
            platforms=args.watch_platform or None,
            sites=args.watch_site or None,
            schedule=args.watch_schedule,
            min_confidence=args.watch_min_confidence,
            top_n=args.watch_top_n,
            alert_rules=alert_rules,
        )
        print(f"✅ created watch mission: {mission['id']}")
        print(f"   name: {mission['name']}")
        print(f"   query: {mission['query']}")
        print(f"   platforms: {', '.join(mission.get('platforms', [])) or 'any'}")
        print(f"   sites: {', '.join(mission.get('sites', [])) or '-'}")
        mission_intent = mission.get("mission_intent", {}) if isinstance(mission, dict) else {}
        if isinstance(mission_intent, dict) and mission_intent.get("demand_intent"):
            print(f"   demand_intent: {mission_intent['demand_intent']}")
        print(f"   alert_rules: {len(mission.get('alert_rules', []))}")
        return

    if args.watch_alert_set:
        alert_rules = _build_watch_alert_rules_from_args(args)
        if not alert_rules:
            parser.error("--watch-alert-set requires at least one watch alert field to define the replacement rule")
        alert_mission = reader.set_watch_alert_rules(args.watch_alert_set, alert_rules=alert_rules)
        if alert_mission is None:
            print(f"⚠️ watch mission not found: {args.watch_alert_set}")
        else:
            print(f"✅ updated alert rules for: {alert_mission['id']}")
            print(f"   alert_rules: {len(alert_mission.get('alert_rules', []))}")
            _print_watch_detail(alert_mission)
        return

    if args.watch_alert_clear:
        cleared_mission = reader.set_watch_alert_rules(args.watch_alert_clear, alert_rules=[])
        if cleared_mission is None:
            print(f"⚠️ watch mission not found: {args.watch_alert_clear}")
        else:
            print(f"✅ cleared alert rules for: {cleared_mission['id']}")
            print(f"   alert_rules: {len(cleared_mission.get('alert_rules', []))}")
            _print_watch_detail(cleared_mission)
        return

    if args.watch_list:
        watches = reader.list_watches(include_disabled=args.watch_include_disabled)
        if not watches:
            print("No watch mission configured.")
        else:
            print(f"🛰️ Watch missions: {len(watches)}")
            _print_watches(watches)
        return

    if args.watch_show:
        watch_payload = reader.show_watch(args.watch_show)
        if watch_payload is None:
            print(f"⚠️ watch mission not found: {args.watch_show}")
        else:
            _print_watch_detail(watch_payload)
        return

    if args.watch_results:
        items = reader.list_watch_results(
            args.watch_results,
            limit=args.watch_results_limit,
            min_confidence=args.min_confidence,
        )
        if items is None:
            print(f"⚠️ watch mission not found: {args.watch_results}")
        elif not items:
            print("No persisted watch result matched.")
        else:
            print(f"📡 Watch results: {len(items)}")
            _print_watch_results(items)
        return

    if args.watch_disable:
        disabled_mission = reader.disable_watch(args.watch_disable)
        if disabled_mission is None:
            print(f"⚠️ watch mission not found: {args.watch_disable}")
        else:
            print(f"✅ disabled watch mission: {disabled_mission['id']}")
        return

    if args.alert_list:
        alerts = reader.list_alerts(limit=args.alert_limit, mission_id=args.alert_mission)
        if not alerts:
            print("No alert event stored.")
        else:
            print(f"🚨 Alert events: {len(alerts)}")
            _print_alerts(alerts)
        return

    if args.alert_route_list:
        routes = reader.list_alert_routes()
        if not routes:
            print("No alert route configured.")
        else:
            print(f"🧭 Alert routes: {len(routes)}")
            _print_alert_routes(routes)
        return

    if args.alert_route_health:
        routes = reader.alert_route_health(limit=args.alert_route_health_limit)
        if not routes:
            print("No alert route health signal yet.")
        else:
            print(f"🩺 Alert route health: {len(routes)}")
            _print_alert_route_health(routes)
        return

    if args.watch_status:
        _print_watch_status(reader.watch_status_snapshot())
        return

    if args.ops_overview:
        _print_ops_overview(reader.ops_snapshot())
        return

    if args.triage_list:
        items = reader.triage_list(
            limit=args.limit,
            min_confidence=args.min_confidence,
            states=args.triage_state,
            include_closed=args.triage_include_closed,
        )
        if not items:
            print("No triage queue item matched.")
        else:
            print(f"🧭 Triage queue: {len(items)}")
            _print_triage_items(items)
        return

    if args.triage_explain:
        payload = reader.triage_explain(args.triage_explain, limit=max(0, args.triage_explain_limit))
        if payload is None:
            print(f"⚠️ triage item not found: {args.triage_explain}")
        else:
            _print_triage_explain(payload)
        return

    if args.triage_update:
        if not args.triage_state:
            parser.error("--triage-update requires --triage-state")
        state_values = list(args.triage_state)
        if len(state_values) != 1:
            parser.error("--triage-update accepts exactly one --triage-state")
        try:
            item = reader.triage_update(
                args.triage_update,
                state=state_values[0],
                note=args.triage_note_text or "",
                actor=args.triage_author,
                duplicate_of=args.triage_duplicate_of,
            )
        except ValueError as exc:
            print(f"❌ {exc}")
            return
        if item is None:
            print(f"⚠️ triage item not found: {args.triage_update}")
        else:
            print(f"✅ triage updated: {item['id']} -> {item['review_state']}")
        return

    if args.triage_note:
        if not args.triage_note_text:
            parser.error("--triage-note requires --triage-note-text")
        item = reader.triage_note(
            args.triage_note,
            note=args.triage_note_text,
            author=args.triage_author,
        )
        if item is None:
            print(f"⚠️ triage item not found: {args.triage_note}")
        else:
            print(f"✅ triage note added: {item['id']}")
        return

    if args.triage_stats:
        _print_triage_stats(reader.triage_stats(min_confidence=args.min_confidence))
        return

    if args.story_build:
        payload = reader.story_build(
            profile=args.source_profile,
            source_ids=_normalize_csv_ids(args.source_ids),
            max_stories=args.story_limit,
            evidence_limit=args.story_evidence_limit,
            min_confidence=args.min_confidence,
        )
        print(f"Stories built: {payload['stats']['stories_built']}")
        print(f"Stories saved: {payload['stats']['stories_saved']}")
        if payload["stories"]:
            print()
            _print_story_list(payload["stories"])
        return

    if args.story_list:
        stories = reader.list_stories(limit=args.story_limit, min_items=args.story_min_items)
        if not stories:
            print("No story available.")
        else:
            print(f"📚 Stories: {len(stories)}")
            _print_story_list(stories)
        return

    if args.story_show:
        story_payload = reader.show_story(args.story_show)
        if story_payload is None:
            print(f"⚠️ story not found: {args.story_show}")
        else:
            print(json.dumps(story_payload, ensure_ascii=False, indent=2))
        return

    if args.story_update:
        if args.story_title is None and args.story_summary is None and args.story_status is None:
            parser.error("--story-update requires --story-title, --story-summary, or --story-status")
        try:
            story_payload = reader.update_story(
                args.story_update,
                title=args.story_title,
                summary=args.story_summary,
                status=args.story_status,
            )
        except ValueError as exc:
            print(f"❌ {exc}")
            return
        if story_payload is None:
            print(f"⚠️ story not found: {args.story_update}")
        else:
            print(f"✅ story updated: {story_payload['id']}")
            print(json.dumps(story_payload, ensure_ascii=False, indent=2))
        return

    if args.story_graph:
        story_graph_payload = reader.story_graph(
            args.story_graph,
            entity_limit=args.story_graph_entity_limit,
            relation_limit=args.story_graph_relation_limit,
        )
        if story_graph_payload is None:
            print(f"⚠️ story not found: {args.story_graph}")
        else:
            _print_story_graph(story_graph_payload)
        return

    if args.story_export:
        story_export_payload = reader.export_story(args.story_export, output_format=args.story_format)
        if story_export_payload is None:
            print(f"⚠️ story not found: {args.story_export}")
        else:
            print(story_export_payload)
        return

    if args.watch_run_due:
        async def run_due() -> None:
            payload = await reader.run_due_watches(
                limit=args.watch_due_limit or None,
                retry_attempts=args.watch_daemon_retry_attempts,
                retry_base_delay=args.watch_daemon_retry_base_delay,
                retry_max_delay=args.watch_daemon_retry_max_delay,
                retry_backoff_factor=args.watch_daemon_retry_backoff,
            )
            print(f"Due watch missions: {payload['due_count']}")
            print(f"Executed: {payload['run_count']}")
            if not payload["results"]:
                return
            print()
            for result in payload["results"]:
                status = result.get("status", "unknown")
                mission_name = result.get("mission_name", result.get("mission_id", "watch"))
                item_count = result.get("item_count", 0)
                print(
                    f"- {mission_name} [{status}] items={item_count} "
                    f"attempts={result.get('attempts', 1)} alerts={result.get('alert_count', 0)}"
                )
                if result.get("error"):
                    print(f"  error: {result['error']}")

        asyncio.run(run_due())
        return

    if args.watch_daemon:
        async def run_daemon() -> None:
            payload = await reader.run_watch_daemon(
                poll_seconds=args.watch_daemon_poll_seconds,
                max_cycles=1 if args.watch_daemon_once else (args.watch_daemon_cycles or None),
                due_limit=args.watch_due_limit or None,
                retry_attempts=args.watch_daemon_retry_attempts,
                retry_base_delay=args.watch_daemon_retry_base_delay,
                retry_max_delay=args.watch_daemon_retry_max_delay,
                retry_backoff_factor=args.watch_daemon_retry_backoff,
            )
            print(f"Watch daemon cycles: {payload.get('cycles', 0)}")
            last_result = payload.get("last_result", {})
            if isinstance(last_result, dict):
                print(f"Last due count: {last_result.get('due_count', 0)}")
                print(f"Last run count: {last_result.get('run_count', 0)}")

        try:
            asyncio.run(run_daemon())
        except RuntimeError as exc:
            print(f"❌ {exc}")
        return

    if args.entity_stats:
        print(json.dumps(reader.entity_stats(), ensure_ascii=False, indent=2))
        return

    if args.entity_graph:
        print(json.dumps(reader.entity_graph(entity_name=args.entity_graph), ensure_ascii=False, indent=2))
        return

    if args.entity_query:
        query_payload = reader.query_entities(
            name=args.entity_query,
            entity_type=args.entity_type,
            limit=args.entity_limit,
            min_sources=args.entity_min_sources,
        )
        print(json.dumps(query_payload, ensure_ascii=False, indent=2))
        return

    if args.query_feed:
        feed_payload = reader.build_json_feed(
            profile=args.source_profile,
            source_ids=_normalize_csv_ids(args.source_ids),
            limit=args.limit,
            min_confidence=args.min_confidence,
        )
        print(json.dumps(feed_payload, ensure_ascii=False, indent=2))
        return

    if args.query_rss:
        print(
            reader.build_rss_feed(
                profile=args.source_profile,
                source_ids=_normalize_csv_ids(args.source_ids),
                limit=args.limit,
                min_confidence=args.min_confidence,
            )
        )
        return

    if args.query_atom:
        print(
            reader.build_atom_feed(
                profile=args.source_profile,
                source_ids=_normalize_csv_ids(args.source_ids),
                limit=args.limit,
                min_confidence=args.min_confidence,
            )
        )
        return

    if args.digest:
        digest_payload = reader.build_digest(
            profile=args.source_profile,
            source_ids=_normalize_csv_ids(args.source_ids),
            top_n=args.top_n,
            secondary_n=args.secondary_n,
            min_confidence=args.min_confidence,
        )
        print(json.dumps(digest_payload, ensure_ascii=False, indent=2))
        return

    if args.emit_digest_package:
        package_payload = reader.emit_digest_package(
            profile=args.source_profile,
            source_ids=_normalize_csv_ids(args.source_ids),
            top_n=args.top_n,
            secondary_n=args.secondary_n,
            min_confidence=args.min_confidence,
            output_format=args.emit_digest_format,
        )
        print(package_payload)
        return

    if args.trending is not None:
        async def run_trending() -> None:
            result = await reader.trending(
                location=args.trending,
                top_n=args.trending_limit,
                store=args.trending_store,
                validate=args.trending_validate,
                validate_mode=args.trending_validate_mode,
            )
            if not result["trends"]:
                print("No trending data found")
                requested_loc = result.get("requested_location")
                fallback_reason = result.get("fallback_reason")
                if requested_loc:
                    print(f"Requested location: {requested_loc}")
                if fallback_reason:
                    print(f"Fallback reason: {fallback_reason}")
                return
            loc = result["location"]
            print(f"Trending Topics on X ({loc}) — {result['snapshot_time']}\n")
            requested_loc = result.get("requested_location")
            fallback_reason = result.get("fallback_reason")
            if requested_loc and requested_loc != loc:
                print(f"Requested location: {requested_loc}")
                if fallback_reason:
                    print(f"Fallback reason: {fallback_reason}")
                print()
            for t in result["trends"]:
                vol = f" ({t['volume']})" if t.get("volume") else ""
                print(f"  {t['rank']:2d}. {t['name']}{vol}")
            print(f"\nTotal: {result['trend_count']} topic(s)")
            if result.get("stored_item_id"):
                print(f"Stored as: {result['stored_item_id']}")

        asyncio.run(run_trending())
        return

    if args.search:
        async def run_search() -> None:
            results = await reader.search(
                args.search,
                sites=args.site or None,
                platform=args.platform,
                limit=args.search_limit,
                fetch_content=not args.no_fetch,
                extract_entities=args.entities,
                entity_mode=args.entity_mode,
                store_entities=args.entity_store,
                min_confidence=args.min_confidence,
                provider=args.search_provider,
                mode=args.search_mode,
                deep=args.search_deep,
                news=args.search_news,
                time_range=args.search_time_range,
                freshness=args.search_freshness,
            )
            if not results:
                if args.min_confidence > 0:
                    print("No search results above confidence threshold")
                else:
                    print("No search results returned")
                return
            print(f"Found {len(results)} result(s) for: {args.search}\n")
            for idx, item in enumerate(results, 1):
                sample = (item.content or "")[:140].replace("\n", " ")
                print(f"{idx}. {item.title}")
                print(f"   confidence: {item.confidence:.3f}  score: {item.score}")
                print(f"   url: {item.url}")
                print(f"   sample: {sample}\n")

        asyncio.run(run_search())
        return

    if args.watch_run:
        async def run_watch() -> None:
            payload = await reader.run_watch(args.watch_run)
            mission = payload["mission"]
            items = payload["items"]
            alert_events = payload.get("alert_events", [])
            print(f"Watch mission: {mission['name']} ({mission['id']})")
            print(f"Query: {mission['query']}")
            print(f"Results: {len(items)}")
            print(f"Alerts: {len(alert_events) if isinstance(alert_events, list) else 0}")
            if not items:
                return
            print()
            for idx, item in enumerate(items, 1):
                sample = str(item.get("content", ""))[:140].replace("\n", " ")
                print(f"{idx}. {item.get('title', 'Untitled')}")
                print(f"   confidence: {float(item.get('confidence', 0.0)):.3f}  score: {int(item.get('score', 0) or 0)}")
                print(f"   url: {item.get('url', '')}")
                print(f"   sample: {sample}\n")

        try:
            asyncio.run(run_watch())
        except ValueError as exc:
            print(f"❌ {exc}")
        return

    # Apply Jina reader options if provided
    if args.target_selector or args.no_cache or args.with_alt:
        from datapulse.collectors.jina import JinaCollector

        jina_opts = {}
        if args.target_selector:
            jina_opts["target_selector"] = args.target_selector
        if args.no_cache:
            jina_opts["no_cache"] = True
        if args.with_alt:
            jina_opts["with_alt"] = True
        # Replace the Jina collector in the pipeline with the enhanced one
        enhanced_jina = JinaCollector(**jina_opts)
        for i, p in enumerate(reader.router.parsers):
            if getattr(p, "name", "") == "jina":
                reader.router.parsers[i] = enhanced_jina
                break

    targets = []
    if args.batch:
        targets.extend(args.batch)
    else:
        targets.extend([x for x in args.inputs if "://" in x or x.startswith("www.")])

    if not targets:
        print("Usage:\n  datapulse <url> [urls...]\n  datapulse --batch <url1> <url2>\n  datapulse --list\n  datapulse --search QUERY\n")
        return

    async def run() -> None:
        results = await reader.read_batch(
            targets,
            min_confidence=args.min_confidence,
            extract_entities=args.entities,
            entity_mode=args.entity_mode,
            store_entities=args.entity_store,
        )
        if not results:
            print("No result above confidence threshold")
            return
        for idx, item in enumerate(results, 1):
            sample = (item.content or "")[:140].replace("\n", " ")
            print(f"\n{idx}. [{item.source_type.value}] {item.title}")
            print(f"   confidence: {item.confidence:.3f}")
            print(f"   url: {item.url}")
            print(f"   sample: {sample}")

    asyncio.run(run())


if __name__ == "__main__":
    main()
