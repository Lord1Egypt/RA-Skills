#!/usr/bin/env python3
"""Cross-day theme lifecycle ledger for daily market-sense reports.

Tracks how 上涨主线 evolve across trading days（低位启动 → 在场候选 →
主线确认 → 高位分歧 → 退潮 → 修复 → 再聚焦 → 沉寂）. The script is fully
deterministic: alias resolution（当日临时主题名 → canonical theme_id）and
lifecycle-state judgment are model responsibilities; this script only
provides context, validates state-machine legality, persists records and
renders the HTML block.

Subcommands:
  context        registry + recent states + watchlist, for the model to judge today
  record         validate and upsert model-judged lifecycle records (one date per run)
  window         export a trailing-window JSON payload for the HTML block
  inject         idempotently embed the lifecycle block into an existing report HTML
  backfill-draft parse historical reviews' 主线判定 tables into a raw draft

Storage: theme_registry / theme_daily_state / theme_market_day in alpha_data
(schema: scripts/_shared/init_alpha_data.sql §13).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
_BUNDLED_SHARED = SCRIPT_DIR / "_shared"
_DEV_SHARED_ROOT = SCRIPT_DIR.parents[2] / "shared"
if _BUNDLED_SHARED.exists():
    # 同步包内 db_core 平铺、html_report 包均在 scripts/_shared 下
    sys.path.insert(0, str(_BUNDLED_SHARED))
else:
    # 开发仓库里 db_core 在 shared/data/，html_report 在 shared/
    sys.path.insert(0, str(_DEV_SHARED_ROOT / "data"))
    sys.path.insert(0, str(_DEV_SHARED_ROOT))

from db_core import BACKEND, Backend, get_connection, placeholder  # noqa: E402
from html_report.safe_json import safe_json_for_script  # noqa: E402

STATES = ["低位启动", "在场候选", "主线确认", "高位分歧", "退潮", "修复", "再聚焦", "沉寂"]

# A theme's first-ever record must be one of these; 修复/再聚焦/退潮 all imply
# prior history.  Use per-record "force": true to bypass (warning logged).
ENTRY_STATES = {"低位启动", "在场候选", "主线确认", "高位分歧"}

TRANSITIONS = {
    "低位启动": {"低位启动", "在场候选", "主线确认", "高位分歧", "退潮", "沉寂"},
    "在场候选": {"在场候选", "主线确认", "高位分歧", "退潮", "沉寂"},
    "主线确认": {"主线确认", "在场候选", "高位分歧", "退潮"},
    "高位分歧": {"高位分歧", "主线确认", "在场候选", "再聚焦", "修复", "退潮"},
    "退潮": {"退潮", "修复", "沉寂", "低位启动"},
    "修复": {"修复", "再聚焦", "主线确认", "在场候选", "高位分歧", "退潮"},
    "再聚焦": {"再聚焦", "主线确认", "高位分歧", "在场候选", "修复", "退潮"},
    "沉寂": {"沉寂", "低位启动", "在场候选", "修复"},
}

THEME_ID_RE = re.compile(r"^TH-[\w一-鿿·-]+$")

MARKER_START = "<!-- alphavault:theme-lifecycle:start -->"
MARKER_END = "<!-- alphavault:theme-lifecycle:end -->"

HOOK_NAME = "theme-lifecycle"


# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #
def norm_date(value: str) -> str:
    raw = str(value or "").strip().replace("-", "")
    if not re.match(r"^\d{8}$", raw):
        raise SystemExit(f"无法解析日期: {value!r}（期望 YYYYMMDD 或 YYYY-MM-DD）")
    return f"{raw[0:4]}-{raw[4:6]}-{raw[6:8]}"


def _iso(value: Any) -> str:
    if hasattr(value, "isoformat"):
        return value.isoformat()[:10]
    return str(value)[:10]


def _fetch_all(conn: Any, sql: str, params: tuple = ()) -> list[dict]:
    cur = conn.cursor()
    cur.execute(sql, params)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def _json_load_maybe(value: Any) -> Any:
    if isinstance(value, (list, dict)) or value is None:
        return value
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return value


def _json_param(value: Any) -> Any:
    if value is None:
        return None
    if BACKEND == Backend.POSTGRESQL:
        from psycopg2.extras import Json

        return Json(value, dumps=lambda v: json.dumps(v, ensure_ascii=False))
    return json.dumps(value, ensure_ascii=False)


def _print_json(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


# --------------------------------------------------------------------------- #
# DB reads
# --------------------------------------------------------------------------- #
def fetch_trade_dates(conn: Any, asof: str, n: int) -> list[str]:
    ph = placeholder()
    rows = _fetch_all(
        conn,
        f"SELECT cal_date FROM stock_trade_cal WHERE is_open = 1 AND cal_date <= {ph} "
        f"ORDER BY cal_date DESC LIMIT {int(n)}",
        (asof,),
    )
    return sorted(_iso(r["cal_date"]) for r in rows)


def fetch_registry(conn: Any) -> dict[str, dict]:
    rows = _fetch_all(
        conn,
        "SELECT theme_id, name, aliases, overlay, status FROM theme_registry",
    )
    registry = {}
    for r in rows:
        registry[r["theme_id"]] = {
            "name": r["name"],
            "aliases": _json_load_maybe(r["aliases"]) or [],
            "overlay": r["overlay"],
            "status": r["status"],
        }
    return registry


def fetch_states_between(conn: Any, first: str, last: str) -> list[dict]:
    ph = placeholder()
    rows = _fetch_all(
        conn,
        "SELECT trade_date, theme_id, raw_theme_name, stars, \"position\", crowding, "
        "state, state_prev, evidence, members_sample, source_report "
        f"FROM theme_daily_state WHERE trade_date >= {ph} AND trade_date <= {ph} "
        "ORDER BY trade_date",
        (first, last),
    )
    for r in rows:
        r["trade_date"] = _iso(r["trade_date"])
        r["members_sample"] = _json_load_maybe(r["members_sample"])
    return rows


def fetch_prev_state(conn: Any, theme_id: str, asof: str) -> Optional[dict]:
    ph = placeholder()
    rows = _fetch_all(
        conn,
        f"SELECT trade_date, state FROM theme_daily_state "
        f"WHERE theme_id = {ph} AND trade_date < {ph} ORDER BY trade_date DESC LIMIT 1",
        (theme_id, asof),
    )
    if not rows:
        return None
    return {"trade_date": _iso(rows[0]["trade_date"]), "state": rows[0]["state"]}


def fetch_market_days(conn: Any, first: str, last: str) -> dict[str, str]:
    ph = placeholder()
    rows = _fetch_all(
        conn,
        f"SELECT trade_date, market_state FROM theme_market_day "
        f"WHERE trade_date >= {ph} AND trade_date <= {ph}",
        (first, last),
    )
    return {_iso(r["trade_date"]): r["market_state"] for r in rows}


# --------------------------------------------------------------------------- #
# context
# --------------------------------------------------------------------------- #
def cmd_context(args: argparse.Namespace) -> int:
    asof = norm_date(args.asof)
    with get_connection() as conn:
        dates = fetch_trade_dates(conn, asof, args.days)
        if not dates:
            raise SystemExit(f"stock_trade_cal 中找不到 {asof} 及之前的交易日")
        registry = fetch_registry(conn)
        rows = fetch_states_between(conn, dates[0], dates[-1])

        recent: dict[str, list[dict]] = {}
        for r in rows:
            recent.setdefault(r["theme_id"], []).append(
                {"date": r["trade_date"], "state": r["state"], "stars": r["stars"]}
            )

        themes = []
        for tid, meta in sorted(registry.items()):
            themes.append(
                {
                    "theme_id": tid,
                    "name": meta["name"],
                    "aliases": meta["aliases"],
                    "overlay": meta["overlay"],
                    "status": meta["status"],
                    "recent": recent.get(tid, []),
                }
            )

        # Watchlist: themes alive recently and not yet recorded for asof.  If a
        # watchlist theme is absent from today's 主线判定 table, the model must
        # decide between 退潮（成员命中当日爆量下跌池 / 正文明确退潮）and 沉寂.
        watchlist = []
        for tid, hist in recent.items():
            latest = hist[-1]
            if latest["date"] == asof:
                continue
            if latest["state"] in ("退潮", "沉寂"):
                continue
            watchlist.append(
                {
                    "theme_id": tid,
                    "name": registry.get(tid, {}).get("name", tid),
                    "last_date": latest["date"],
                    "last_state": latest["state"],
                }
            )

    _print_json(
        {
            "asof": asof,
            "trade_dates": dates,
            "rules": {
                "states": STATES,
                "entry_states": sorted(ENTRY_STATES),
                "transitions": {k: sorted(v) for k, v in TRANSITIONS.items()},
            },
            "themes": themes,
            "watchlist": watchlist,
        }
    )
    return 0


# --------------------------------------------------------------------------- #
# record
# --------------------------------------------------------------------------- #
def cmd_record(args: argparse.Namespace) -> int:
    if args.input == "-":
        payload = json.load(sys.stdin)
    else:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))

    asof = norm_date(args.asof or payload.get("asof") or "")
    records = payload.get("records", [])
    source_report = payload.get("source_report", "")
    market_state = payload.get("market_state")
    if not records and not market_state:
        raise SystemExit("输入中既无 records 也无 market_state，无事可写")

    ph = placeholder()
    errors: list[str] = []
    warnings: list[str] = []
    plans: list[dict] = []
    new_themes: list[dict] = []
    alias_updates: dict[str, list[str]] = {}

    with get_connection() as conn:
        registry = fetch_registry(conn)
        seen_ids: set[str] = set()

        for i, rec in enumerate(records):
            label = f"records[{i}]"
            new_theme = rec.get("new_theme")
            if new_theme:
                tid = str(new_theme.get("theme_id") or "")
                if not THEME_ID_RE.match(tid):
                    errors.append(f"{label}: new_theme.theme_id {tid!r} 不符合 TH- 前缀命名")
                    continue
                if tid in registry:
                    errors.append(f"{label}: new_theme {tid} 已在注册表，去掉 new_theme 直接用 theme_id")
                    continue
                name = new_theme.get("name") or rec.get("raw_theme_name") or tid
                registry[tid] = {
                    "name": name,
                    "aliases": [],
                    "overlay": new_theme.get("overlay"),
                    "status": "active",
                }
                new_themes.append(
                    {"theme_id": tid, "name": name, "overlay": new_theme.get("overlay")}
                )
            else:
                tid = str(rec.get("theme_id") or "")
                if tid not in registry:
                    errors.append(f"{label}: theme_id {tid!r} 不在注册表，新主题请用 new_theme 注册")
                    continue

            if tid in seen_ids:
                errors.append(f"{label}: {tid} 在本批中重复")
                continue
            seen_ids.add(tid)

            state = rec.get("state")
            if state not in STATES:
                errors.append(f"{label}: state {state!r} 不在枚举 {STATES}")
                continue

            stars = rec.get("stars")
            if stars is not None and stars not in (1, 2, 3):
                errors.append(f"{label}: stars {stars!r} 须为 1/2/3 或 null")
                continue

            prev = None if tid in {t["theme_id"] for t in new_themes} else fetch_prev_state(conn, tid, asof)
            prev_state = prev["state"] if prev else None
            if rec.get("force"):
                warnings.append(f"{label}: {tid} force 跳过状态机校验（{prev_state} → {state}）")
            elif prev_state is None:
                if state not in ENTRY_STATES:
                    errors.append(
                        f"{label}: {tid} 无历史记录，首次状态须为 {sorted(ENTRY_STATES)}，"
                        f"得到 {state!r}（确认无误可加 \"force\": true）"
                    )
                    continue
            elif state not in TRANSITIONS[prev_state]:
                errors.append(
                    f"{label}: {tid} 非法转移 {prev_state} → {state}"
                    f"（{prev_state} 合法去向: {sorted(TRANSITIONS[prev_state])}；确认无误可加 \"force\": true）"
                )
                continue

            if state != "沉寂" and not rec.get("evidence"):
                warnings.append(f"{label}: {tid} 缺 evidence，可追溯性受损")

            raw_name = rec.get("raw_theme_name")
            meta = registry[tid]
            if raw_name and raw_name != meta["name"] and raw_name not in meta["aliases"]:
                meta["aliases"] = list(meta["aliases"]) + [raw_name]
                alias_updates[tid] = meta["aliases"]

            plans.append(
                {
                    "trade_date": asof,
                    "theme_id": tid,
                    "raw_theme_name": raw_name,
                    "stars": stars,
                    "position": rec.get("position"),
                    "crowding": rec.get("crowding"),
                    "state": state,
                    "state_prev": prev_state,
                    "evidence": rec.get("evidence"),
                    "members_sample": rec.get("members_sample"),
                    "source_report": rec.get("source_report") or source_report,
                }
            )

        if errors:
            _print_json({"ok": False, "asof": asof, "errors": errors, "warnings": warnings})
            raise SystemExit(1)

        cur = conn.cursor()
        for t in new_themes:
            cur.execute(
                f"INSERT INTO theme_registry (theme_id, name, aliases, overlay, status, updated_at) "
                f"VALUES ({ph}, {ph}, {ph}, {ph}, 'active', CURRENT_TIMESTAMP)",
                (t["theme_id"], t["name"], _json_param([]), t["overlay"]),
            )
        for tid, aliases in alias_updates.items():
            cur.execute(
                f"UPDATE theme_registry SET aliases = {ph}, updated_at = CURRENT_TIMESTAMP "
                f"WHERE theme_id = {ph}",
                (_json_param(aliases), tid),
            )
        for p in plans:
            cur.execute(
                "INSERT INTO theme_daily_state (trade_date, theme_id, raw_theme_name, stars, "
                "\"position\", crowding, state, state_prev, evidence, members_sample, source_report) "
                f"VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}) "
                "ON CONFLICT (trade_date, theme_id) DO UPDATE SET "
                "raw_theme_name = EXCLUDED.raw_theme_name, stars = EXCLUDED.stars, "
                "\"position\" = EXCLUDED.\"position\", crowding = EXCLUDED.crowding, "
                "state = EXCLUDED.state, state_prev = EXCLUDED.state_prev, "
                "evidence = EXCLUDED.evidence, members_sample = EXCLUDED.members_sample, "
                "source_report = EXCLUDED.source_report",
                (
                    p["trade_date"],
                    p["theme_id"],
                    p["raw_theme_name"],
                    p["stars"],
                    p["position"],
                    p["crowding"],
                    p["state"],
                    p["state_prev"],
                    p["evidence"],
                    _json_param(p["members_sample"]),
                    p["source_report"],
                ),
            )
        if market_state:
            cur.execute(
                f"INSERT INTO theme_market_day (trade_date, market_state, note) "
                f"VALUES ({ph}, {ph}, {ph}) "
                "ON CONFLICT (trade_date) DO UPDATE SET "
                "market_state = EXCLUDED.market_state, note = EXCLUDED.note",
                (asof, market_state, payload.get("market_note")),
            )

    _print_json(
        {
            "ok": True,
            "asof": asof,
            "written": len(plans),
            "new_themes": [t["theme_id"] for t in new_themes],
            "aliases_added": sorted(alias_updates),
            "market_state": market_state,
            "warnings": warnings,
        }
    )
    return 0


# --------------------------------------------------------------------------- #
# window
# --------------------------------------------------------------------------- #
def build_window_payload(conn: Any, asof: str, days: int) -> dict:
    dates = fetch_trade_dates(conn, asof, days)
    if not dates:
        raise SystemExit(f"stock_trade_cal 中找不到 {asof} 及之前的交易日")
    registry = fetch_registry(conn)
    rows = fetch_states_between(conn, dates[0], dates[-1])
    market_days = fetch_market_days(conn, dates[0], dates[-1])

    by_theme: dict[str, dict[str, dict]] = {}
    for r in rows:
        cell = {
            "state": r["state"],
            "stars": r["stars"],
            "position": r["position"],
            "crowding": r["crowding"],
            "evidence": r["evidence"],
            "source": r["source_report"],
        }
        by_theme.setdefault(r["theme_id"], {})[r["trade_date"]] = cell

    themes = []
    for tid, cells in by_theme.items():
        themes.append(
            {
                "theme_id": tid,
                "name": registry.get(tid, {}).get("name", tid),
                "_last": max(cells),
                "_count": len(cells),
                "cells": cells,
            }
        )
    themes.sort(key=lambda t: (t["_last"], t["_count"], t["name"]), reverse=True)
    for t in themes:
        t.pop("_last")
        t.pop("_count")

    return {
        "asof": dates[-1],
        "days": len(dates),
        "dates": dates,
        "market_days": market_days,
        "themes": themes,
    }


def cmd_window(args: argparse.Namespace) -> int:
    asof = norm_date(args.asof)
    with get_connection() as conn:
        payload = build_window_payload(conn, asof, args.days)
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        _print_json({"ok": True, "out": args.out, "themes": len(payload["themes"])})
    else:
        print(text)
    return 0


# --------------------------------------------------------------------------- #
# Lifecycle block JS (shared by the ChartHook path and `inject`)
# --------------------------------------------------------------------------- #
# Runs inside an IIFE with `__payload` in scope (the builder provides it from
# the #chart-data envelope; `inject` inlines it).  Finds the 主线判定 heading
# at view time and appends the block at the end of that subsection.
LIFECYCLE_JS_BODY = r"""
  const data = __payload || {};
  if (!data.dates || !data.dates.length || !data.themes || !data.themes.length) return;
  if (document.getElementById("theme-lifecycle-block")) return;
  const root = document.getElementById("report-body") || document.body;
  function findAnchor(text) {
    const nodes = root.querySelectorAll("h2,h3,h4");
    for (const el of nodes) {
      if ((el.textContent || "").indexOf(text) !== -1) return el;
    }
    return null;
  }
  const anchor = findAnchor("主线判定") || findAnchor("赚钱效应");
  let insertAfter = null;
  if (anchor) {
    insertAfter = anchor;
    let el = anchor.nextElementSibling;
    while (el && ["H2", "H3", "H4"].indexOf(el.tagName) === -1) {
      insertAfter = el;
      el = el.nextElementSibling;
    }
  }
  const COLORS = {
    "主线确认": "#E24B4A",
    "在场候选": "#F7C1C1",
    "修复": "#F09595",
    "高位分歧": "#EF9F27",
    "退潮": "#97C459",
    "再聚焦": "#378ADD",
    "沉寂": "#ECEFF1"
  };
  const EMPTY = "#F1F3F4";
  const BOLT_BG = "#CECBF6", BOLT_FG = "#3C3489";
  const STAR = { 1: "★", 2: "★★", 3: "★★★" };
  const lastIdx = data.dates.length - 1;
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function boltSvg(size) {
    return '<svg width="' + size + '" height="' + size + '" viewBox="0 0 24 24" fill="' + BOLT_FG + '" aria-hidden="true"><path d="M13 2 4 14h6l-1 8 9-12h-6l1-8z"/></svg>';
  }
  function swatchHtml(state) {
    if (state === "低位启动") {
      return '<span style="display:inline-flex;width:13px;height:13px;border-radius:3px;background:' + BOLT_BG + ';align-items:center;justify-content:center;">' + boltSvg(9) + "</span>";
    }
    const bg = state ? (COLORS[state] || EMPTY) : EMPTY;
    return '<span style="display:inline-block;width:13px;height:13px;border-radius:3px;background:' + bg + ';border:1px solid rgba(60,64,67,.12);"></span>';
  }
  const wrap = document.createElement("section");
  wrap.id = "theme-lifecycle-block";
  wrap.style.cssText = "margin:22px 0;border:1px solid #DADCE0;border-radius:12px;padding:16px 18px;background:#fff;font-size:13px;";
  const head = document.createElement("div");
  head.style.cssText = "display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:6px;margin-bottom:10px;";
  head.innerHTML =
    '<span style="font-weight:600;font-size:15px;color:#202124;">主线生命周期</span>' +
    '<span style="font-size:12px;color:#5F6368;">近 ' + data.dates.length + " 个交易日 · 截至本期 " + esc(data.asof) + "</span>";
  wrap.appendChild(head);
  const legendItems = [
    ["低位启动", "低位启动"],
    ["在场候选 ★★", "在场候选"],
    ["主线确认 ★★★", "主线确认"],
    ["高位分歧 / 换锚", "高位分歧"],
    ["修复", "修复"],
    ["再聚焦", "再聚焦"],
    ["退潮", "退潮"],
    ["离场 / 未上榜", null]
  ];
  const legend = document.createElement("div");
  legend.style.cssText = "display:flex;flex-wrap:wrap;gap:6px 14px;margin-bottom:12px;align-items:center;";
  for (const it of legendItems) {
    const s = document.createElement("span");
    s.style.cssText = "display:inline-flex;align-items:center;gap:5px;font-size:12px;color:#5F6368;";
    s.innerHTML = swatchHtml(it[1]) + esc(it[0]);
    legend.appendChild(s);
  }
  wrap.appendChild(legend);
  const detail = document.createElement("div");
  function showDetail(theme, di) {
    const d = data.dates[di];
    const cell = theme.cells[d];
    const md = (data.market_days || {})[d];
    let html = '<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px;">';
    html += '<span style="font-weight:600;font-size:13.5px;color:#202124;">' + esc(theme.name) + "</span>";
    html += '<span style="font-size:12px;color:#5F6368;">' + esc(d) + (di === lastIdx ? " · 本期" : "") + "</span>";
    html += '<span style="display:inline-flex;align-items:center;gap:5px;font-size:12px;color:#3C4043;">' + swatchHtml(cell ? cell.state : null) + esc(cell ? cell.state : "离场 / 未上榜") + "</span>";
    if (cell) {
      const bits = [];
      bits.push("确认度 " + (STAR[cell.stars] || "—"));
      if (cell.position) bits.push(esc(cell.position));
      if (cell.crowding) bits.push("拥挤度" + esc(cell.crowding));
      html += '<span style="font-size:12px;color:#5F6368;">' + bits.join(" · ") + "</span>";
    }
    html += "</div>";
    let body;
    if (cell && cell.evidence) {
      body = esc(cell.evidence);
    } else if (md) {
      body = "市场状态：" + esc(md) + "，当日无该主线判定记录。";
    } else {
      body = "当日该主线未上榜，无记录。";
    }
    html += '<div style="font-size:12.5px;line-height:1.65;color:#3C4043;">' + body + "</div>";
    if (cell && cell.source) {
      html += '<div style="margin-top:6px;font-size:11.5px;color:#80868B;">来源：' + esc(cell.source) + "</div>";
    }
    detail.innerHTML = html;
  }
  const cellW = Math.max(14, Math.min(24, Math.floor(520 / data.dates.length)));
  const lanes = document.createElement("div");
  lanes.style.cssText = "overflow-x:auto;padding-bottom:4px;";
  const inner = document.createElement("div");
  inner.style.cssText = "min-width:" + (160 + data.dates.length * (cellW + 2)) + "px;";
  data.themes.forEach(function (theme) {
    const row = document.createElement("div");
    row.style.cssText = "display:flex;align-items:center;margin-bottom:3px;";
    const label = document.createElement("div");
    label.style.cssText = "flex:0 0 152px;font-size:12px;line-height:1.3;color:#202124;padding-right:8px;";
    label.textContent = theme.name;
    row.appendChild(label);
    data.dates.forEach(function (d, di) {
      const cell = theme.cells[d];
      const box = document.createElement("div");
      let css = "width:" + cellW + "px;height:24px;margin-right:2px;border-radius:3px;cursor:pointer;display:flex;align-items:center;justify-content:center;flex:0 0 auto;";
      if (cell && cell.state === "低位启动") {
        css += "background:" + BOLT_BG + ";";
      } else {
        css += "background:" + (cell ? (COLORS[cell.state] || EMPTY) : EMPTY) + ";";
      }
      if (di === lastIdx) {
        css += "outline:1.5px solid #5F6368;outline-offset:1px;";
      }
      box.style.cssText = css;
      if (cell && cell.state === "低位启动") box.innerHTML = boltSvg(13);
      box.title = d + " · " + (cell ? cell.state + (STAR[cell && cell.stars] ? " " + STAR[cell.stars] : "") : "未上榜");
      box.addEventListener("click", function () { showDetail(theme, di); });
      row.appendChild(box);
    });
    inner.appendChild(row);
  });
  const axis = document.createElement("div");
  axis.style.cssText = "display:flex;align-items:flex-start;margin-top:6px;";
  const spacer = document.createElement("div");
  spacer.style.cssText = "flex:0 0 152px;";
  axis.appendChild(spacer);
  data.dates.forEach(function (d, di) {
    const lab = document.createElement("div");
    const md = (data.market_days || {})[d];
    let color = di === lastIdx ? "#202124" : "#80868B";
    let weight = di === lastIdx ? "600" : "400";
    if (md) color = "#1E8E3E";
    lab.style.cssText = "width:" + cellW + "px;margin-right:2px;font-size:11px;writing-mode:vertical-rl;height:46px;flex:0 0 auto;color:" + color + ";font-weight:" + weight + ";";
    lab.textContent = di % 2 === 0 || di === lastIdx || md ? d.slice(5) : "";
    if (md) lab.title = d + " · " + md;
    axis.appendChild(lab);
  });
  inner.appendChild(axis);
  lanes.appendChild(inner);
  wrap.appendChild(lanes);
  detail.style.cssText = "margin-top:12px;background:#F8F9FA;border-radius:8px;padding:12px 14px;min-height:64px;";
  wrap.appendChild(detail);
  const foot = document.createElement("div");
  foot.style.cssText = "margin-top:8px;font-size:11.5px;color:#80868B;";
  foot.textContent = "红 = 强势在场 · 绿 = 退潮 · 闪电 = 低位启动；点击格子查看当日证据。数据来自 theme_daily_state，证据可回溯当日复盘原文。";
  wrap.appendChild(foot);
  if (insertAfter) {
    insertAfter.after(wrap);
  } else {
    root.appendChild(wrap);
  }
  let defTheme = null;
  let defIdx = lastIdx;
  for (const t of data.themes) {
    if (t.cells[data.dates[lastIdx]]) { defTheme = t; break; }
  }
  if (!defTheme) {
    defTheme = data.themes[0];
    const ds = Object.keys(defTheme.cells).sort();
    defIdx = Math.max(0, data.dates.indexOf(ds[ds.length - 1]));
  }
  showDetail(defTheme, defIdx);
"""


def render_block_script(payload: dict) -> str:
    return (
        MARKER_START
        + "\n<script>\n(function () {\n  const __payload = "
        + safe_json_for_script(payload)
        + ";\n"
        + LIFECYCLE_JS_BODY
        + "\n})();\n</script>\n"
        + MARKER_END
    )


# --------------------------------------------------------------------------- #
# inject
# --------------------------------------------------------------------------- #
def cmd_inject(args: argparse.Namespace) -> int:
    html_path = Path(args.html)
    if not html_path.exists():
        raise SystemExit(f"HTML 不存在: {html_path}")
    if args.asof:
        asof = norm_date(args.asof)
    else:
        m = re.search(r"(\d{4}-\d{2}-\d{2})", html_path.name)
        if not m:
            raise SystemExit(f"文件名 {html_path.name} 中找不到日期，请用 --asof 指定")
        asof = m.group(1)

    with get_connection() as conn:
        payload = build_window_payload(conn, asof, args.days)
    if not payload["themes"]:
        _print_json({"ok": False, "file": str(html_path), "error": f"{asof} 窗口内无生命周期数据，先 record/回填"})
        raise SystemExit(1)

    block = render_block_script(payload)
    html = html_path.read_text(encoding="utf-8")
    marker_re = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.S)

    # 新版渲染器经 ChartHook 原生携带区块；此类页面不再叠加 marker 注入，
    # 已存在的重复 marker 块（如曾被旧版 inject 处理过）一并清除。
    chart_data = re.search(r'<script id="chart-data"[^>]*>(.*?)</script>', html, re.S)
    if chart_data and f'"{HOOK_NAME}"' in chart_data.group(1):
        if marker_re.search(html):
            new_html = marker_re.sub("", html)
            if not args.dry_run:
                html_path.write_text(new_html, encoding="utf-8")
            _print_json({"ok": True, "file": str(html_path), "asof": payload["asof"],
                         "action": "removed_duplicate_marker", "dry_run": bool(args.dry_run)})
        else:
            _print_json({"ok": True, "file": str(html_path), "asof": payload["asof"],
                         "action": "skipped_native_hook", "dry_run": bool(args.dry_run)})
        return 0

    if marker_re.search(html):
        new_html = marker_re.sub(lambda _m: block, html)
        action = "replaced"
    else:
        idx = html.rfind("</body>")
        if idx == -1:
            raise SystemExit(f"{html_path} 中找不到 </body>，无法注入")
        new_html = html[:idx] + block + "\n" + html[idx:]
        action = "inserted"

    if new_html == html:
        action = "unchanged"
    elif not args.dry_run:
        html_path.write_text(new_html, encoding="utf-8")

    _print_json(
        {
            "ok": True,
            "file": str(html_path),
            "asof": payload["asof"],
            "themes": len(payload["themes"]),
            "action": action,
            "dry_run": bool(args.dry_run),
        }
    )
    return 0


# --------------------------------------------------------------------------- #
# backfill-draft
# --------------------------------------------------------------------------- #
def _split_md_row(line: str) -> Optional[list[str]]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    return [c.strip() for c in stripped[1:-1].split("|")]


def _find_col(header: list[str], *needles: str) -> Optional[int]:
    for i, cell in enumerate(header):
        for needle in needles:
            if needle in cell:
                return i
    return None


def _parse_stars(cell: str) -> Optional[int]:
    count = cell.count("★")
    if count:
        return count
    for word, value in (("三星", 3), ("二星", 2), ("一星", 1)):
        if word in cell:
            return value
    return None


def _parse_review(text: str) -> Optional[list[dict]]:
    lines = text.splitlines()
    head_idx = None
    for i, line in enumerate(lines):
        if line.lstrip().startswith("#") and "主线判定" in line:
            head_idx = i
            break
    if head_idx is None:
        return None

    table: list[list[str]] = []
    for line in lines[head_idx + 1:]:
        stripped = line.strip()
        if stripped.startswith("#"):
            break
        if not stripped:
            continue
        cells = _split_md_row(line)
        if cells:
            table.append(cells)
        elif table:
            break
    if len(table) < 3:
        return None

    header = table[0]
    name_col = _find_col(header, "主题")
    stars_col = _find_col(header, "主线确认度", "确认度")
    pos_col = _find_col(header, "位置判断")
    crowd_col = _find_col(header, "拥挤度")
    ev_col = _find_col(header, "催化逻辑", "证据")
    if name_col is None or stars_col is None:
        return None
    if ev_col is None:
        ev_col = len(header) - 1

    rows = []
    for cells in table[2:]:
        if len(cells) <= max(name_col, stars_col):
            continue
        if all(re.match(r"^:?-{3,}:?$", c) for c in cells if c):
            continue
        rows.append(
            {
                "raw_theme_name": cells[name_col],
                "stars": _parse_stars(cells[stars_col]),
                "position": cells[pos_col] if pos_col is not None and pos_col < len(cells) else None,
                "crowding": cells[crowd_col] if crowd_col is not None and crowd_col < len(cells) else None,
                "evidence": cells[ev_col] if ev_col < len(cells) else None,
            }
        )
    return rows or None


def _review_hint(text: str) -> str:
    m = re.search(r"^#+\s*一句话盘面判断\s*$(.*?)(?=^#)", text, re.S | re.M)
    if m:
        body = " ".join(line.strip() for line in m.group(1).splitlines() if line.strip())
        if body:
            return body[:400]
    m = re.search(r"==([^=]{20,})==", text)
    if m:
        return m.group(1).strip()[:400]
    return ""


def cmd_backfill_draft(args: argparse.Namespace) -> int:
    reviews_dir = Path(args.reviews)
    if not reviews_dir.is_dir():
        raise SystemExit(f"目录不存在: {reviews_dir}")

    reviews = []
    for path in sorted(reviews_dir.iterdir()):
        if not path.name.endswith(".md") or "趋势复盘" not in path.name:
            continue
        m = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
        if not m:
            continue
        text = path.read_text(encoding="utf-8")
        rows = _parse_review(text)
        entry: dict[str, Any] = {"date": m.group(1), "file": path.name}
        if rows:
            entry["rows"] = rows
        else:
            entry["no_table"] = True
            entry["hint"] = _review_hint(text)
        reviews.append(entry)

    reviews.sort(key=lambda r: r["date"])
    out_payload = {
        "reviews_dir": str(reviews_dir),
        "count": len(reviews),
        "with_table": sum(1 for r in reviews if "rows" in r),
        "no_table": sum(1 for r in reviews if r.get("no_table")),
        "reviews": reviews,
    }
    text = json.dumps(out_payload, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        _print_json({"ok": True, "out": args.out, "count": len(reviews)})
    else:
        print(text)
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("context", help="输出注册表、近期状态与 watchlist，供模型判定当日生命周期")
    p.add_argument("--asof", required=True)
    p.add_argument("--days", type=int, default=10)
    p.set_defaults(func=cmd_context)

    p = sub.add_parser("record", help="校验并写入模型判定的生命周期记录（一次一个交易日）")
    p.add_argument("--input", required=True, help="lifecycle JSON 文件路径，- 表示 stdin")
    p.add_argument("--asof", help="覆盖输入中的 asof")
    p.set_defaults(func=cmd_record)

    p = sub.add_parser("window", help="导出截至某日的窗口 JSON（HTML 区块 payload）")
    p.add_argument("--asof", required=True)
    p.add_argument("--days", type=int, default=22)
    p.add_argument("--out")
    p.set_defaults(func=cmd_window)

    p = sub.add_parser("inject", help="向既有报告 HTML 幂等注入主线生命周期区块")
    p.add_argument("--html", required=True)
    p.add_argument("--asof", help="默认从文件名中的 YYYY-MM-DD 推断")
    p.add_argument("--days", type=int, default=22)
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_inject)

    p = sub.add_parser("backfill-draft", help="解析历史复盘的主线判定表，输出回填草稿")
    p.add_argument("--reviews", required=True, help="趋势复盘 Markdown 目录")
    p.add_argument("--out")
    p.set_defaults(func=cmd_backfill_draft)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
