#!/usr/bin/env python3
"""Render a daily-market-sense Markdown report as a self-contained HTML page.

All the generic machinery — CLI parsing, Markdown→HTML, theming, the chart kit
(``window.CK``), text-preservation validation and the pill/hero decorations —
comes from the shared ``html_report`` package (synced into ``scripts/_shared/``).
This file owns only the market-sense-specific bits: loading market_data.json /
evidence_*.json, extracting the index K-line + stock K-line + market-trend
payloads, the pill vocabulary and the JS that draws those charts.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


SCRIPT_ROOT = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_ROOT.parent
DEFAULT_MARKET_DATA = SKILL_ROOT / "references" / "market_data.json"
INDEX_KLINE_DISPLAY_DAYS = 120
MONTHLY_KLINE_DISPLAY_MONTHS = 72

_BUNDLED_SHARED = SCRIPT_ROOT / "_shared"
_DEV_SHARED = SCRIPT_ROOT.parents[2] / "shared"
sys.path.insert(0, str(_BUNDLED_SHARED if _BUNDLED_SHARED.exists() else _DEV_SHARED))

from html_report import (  # noqa: E402
    ChartHook,
    HeroDecoration,
    HtmlReportBuilder,
    PillDecoration,
    RenderJob,
    render_report,
)


# --------------------------------------------------------------------------- #
# Data loading (market-sense-specific)
# --------------------------------------------------------------------------- #
def load_market_data(path: Path) -> dict:
    if not path.exists():
        return {
            "metadata": {"missing": True, "source": str(path)},
            "columns": [],
            "records": [],
            "series": {},
            "quality": {"records_available": 0, "has_120_records": False},
        }
    return json.loads(path.read_text(encoding="utf-8"))


def default_evidence_path(input_path: Path) -> Optional[Path]:
    match = re.match(r"^report_(\d{8})$", input_path.stem)
    if not match:
        return None
    return input_path.with_name(f"evidence_{match.group(1)}_utf8.json")


def default_kline_path(input_path: Path) -> Optional[Path]:
    match = re.match(r"^report_(\d{8})$", input_path.stem)
    if not match:
        return None
    return input_path.with_name(f"kline_{match.group(1)}.json")


def load_evidence(path: Optional[Path]) -> dict:
    if path is None or not path.exists():
        return {
            "metadata": {"missing": True, "source": str(path) if path is not None else ""},
            "market_trend": {"indices": {}},
        }
    return json.loads(path.read_text(encoding="utf-8"))


def load_stock_klines(evidence: dict, kline_path: Optional[Path]) -> dict:
    """Stock klines live in a sibling kline_YYYYMMDD.json; older evidence
    files carried them inline under stock_kline_records."""
    if kline_path is not None and kline_path.exists():
        return json.loads(kline_path.read_text(encoding="utf-8"))
    inline = evidence.get("stock_kline_records")
    return inline if isinstance(inline, dict) else {}


def extract_index_kline_payload(evidence: dict, source_path: Optional[Path]) -> Dict[str, Any]:
    indices = ((evidence.get("market_trend") or {}).get("indices") or {})
    payload: Dict[str, Any] = {
        "metadata": {
            "source": str(source_path) if source_path is not None else "",
            "missing": bool((evidence.get("metadata") or {}).get("missing")),
        },
        "indices": {},
    }
    for key in ("shanghai", "chinext", "star50"):
        item = indices.get(key) or {}
        records = item.get("kline_records") if isinstance(item, dict) else []
        if isinstance(records, list):
            records = records[-INDEX_KLINE_DISPLAY_DAYS:]
        else:
            records = []
        payload["indices"][key] = {
            "available": bool(item.get("available")) and bool(records),
            "name": item.get("name"),
            "ts_code": item.get("ts_code"),
            "trade_date": item.get("trade_date"),
            "kline_days": item.get("kline_days"),
            "kline_days_requested": item.get("kline_days_requested"),
            "records": records,
        }
    return payload


def extract_stock_kline_payload(raw: dict, source_path: Optional[Path], missing: bool = False) -> Dict[str, Any]:
    raw = raw or {}
    by_ts_code = raw.get("by_ts_code") if isinstance(raw, dict) else {}
    name_to_ts_code = raw.get("name_to_ts_code") if isinstance(raw, dict) else {}
    payload: Dict[str, Any] = {
        "metadata": {
            "source": str(source_path) if source_path is not None else "",
            "missing": missing,
            "kline_days_requested": (raw.get("metadata") or {}).get("kline_days_requested") if isinstance(raw, dict) else None,
            "price_adjustment": (raw.get("metadata") or {}).get("price_adjustment") if isinstance(raw, dict) else None,
        },
        "by_ts_code": {},
        "name_to_ts_code": name_to_ts_code if isinstance(name_to_ts_code, dict) else {},
    }
    if not isinstance(by_ts_code, dict):
        return payload
    for ts_code, item in by_ts_code.items():
        if not isinstance(item, dict):
            continue
        records = item.get("records")
        if isinstance(records, list):
            records = records[-INDEX_KLINE_DISPLAY_DAYS:]
        else:
            records = []
        payload["by_ts_code"][str(ts_code)] = {
            "available": bool(item.get("available")) and bool(records),
            "name": item.get("name"),
            "ts_code": item.get("ts_code") or ts_code,
            "trade_date": item.get("trade_date"),
            "price_adjustment": item.get("price_adjustment") or payload["metadata"].get("price_adjustment"),
            "kline_days": item.get("kline_days"),
            "kline_days_requested": item.get("kline_days_requested"),
            "records": records,
        }

    # 月线平台突破组（5.2）的月线序列：多年底部箱体 + pivot + 突破月，供月线 K 线图。
    monthly_raw = raw.get("monthly") if isinstance(raw, dict) else None
    if isinstance(monthly_raw, dict):
        m_by = monthly_raw.get("by_ts_code")
        m_name = monthly_raw.get("name_to_ts_code")
        monthly_payload: Dict[str, Any] = {
            "by_ts_code": {},
            "name_to_ts_code": m_name if isinstance(m_name, dict) else {},
        }
        if isinstance(m_by, dict):
            for ts_code, item in m_by.items():
                if not isinstance(item, dict):
                    continue
                records = item.get("records")
                records = records[-MONTHLY_KLINE_DISPLAY_MONTHS:] if isinstance(records, list) else []
                monthly_payload["by_ts_code"][str(ts_code)] = {
                    "available": bool(records),
                    "name": item.get("name"),
                    "ts_code": item.get("ts_code") or ts_code,
                    "base_top_pivot": item.get("base_top_pivot"),
                    "base_start_month": item.get("base_start_month"),
                    "breakout_month": item.get("breakout_month"),
                    "records": records,
                }
        payload["monthly"] = monthly_payload
    return payload


def _clean_style_series_records(records: Any, display_days: int) -> List[Dict[str, Any]]:
    cleaned: List[Dict[str, Any]] = []
    if not isinstance(records, list):
        return cleaned
    for row in records:
        if not isinstance(row, dict):
            continue
        trade_date = str(row.get("trade_date") or "").strip()
        try:
            close = float(row.get("close"))
        except (TypeError, ValueError):
            continue
        if trade_date and close == close:
            cleaned.append({"trade_date": trade_date, "close": round(close, 2)})
    return sorted(cleaned, key=lambda item: item["trade_date"])[-display_days:]


def extract_style_series_payload(evidence: dict, display_days: int = 60) -> Optional[Dict[str, Any]]:
    style = ((evidence or {}).get("market_trend") or {}).get("market_style") or {}
    if not isinstance(style, dict) or not style.get("available"):
        return None
    indices = style.get("indices") or {}
    items: List[Dict[str, Any]] = []
    for key, item in indices.items():
        if not isinstance(item, dict) or not item.get("available"):
            continue
        series = item.get("series") or {}
        records = _clean_style_series_records(series.get("records"), display_days)
        if not records:
            continue
        items.append({
            "key": key,
            "name": item.get("name"),
            "style_role": item.get("style_role"),
            "proxy_note": item.get("proxy_note"),
            "records": records,
        })
    if not items:
        return None
    return {
        "display_days": int(display_days),
        "trade_date": style.get("trade_date"),
        "indices": items,
    }


# --------------------------------------------------------------------------- #
# Decorations: pill vocabulary + "一句话盘面判断" hero card (mechanism lives in
# the shared package; here we only declare the market-sense-specific data).
# --------------------------------------------------------------------------- #
MARKET_SENSE_PILL_RULES = [
    (r"^高位强势股退潮$", "pill neg"),
    (r"^流动性杀跌$", "pill warn"),
    (r"^主线内部分歧$", "pill warn"),
    (r"^高位趋势$", "pill"),
    (r"^高$", "pill neg"),
    (r"^中$", "pill warn"),
    (r"^低$", "pill pos"),
    (r"^领导股$", "pill"),
    (r"^弹性股$", "pill violet"),
    (r"^启动型$|^持续换手型$|^分歧型$", "pill"),
    (r"^[ABC]$", "pill"),
]

HERO_KEYWORDS = "上证|创业板|科创50|国证2000|中证红利|半导体设备与材料|电力能源"
MARKET_SENSE_EXTRA_CSS = """
.kline-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.style-compare-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; margin: 12px 0 22px; }
.style-compare-card { min-width: 0; margin: 0; }
.style-compare-legend { display: flex; flex-wrap: wrap; gap: 6px 12px; color: var(--ink-3); font-size: 12px; margin-top: 6px; padding-top: 6px; border-top: 1px solid var(--line-2); }
.style-compare-legend span { display: inline-flex; align-items: center; gap: 6px; font-family: var(--font-mono); }
.style-compare-legend svg { width: 24px; height: 8px; overflow: visible; }
.style-compare-note { margin-top: 6px; color: var(--ink-3); font-size: 12px; line-height: 1.55; }
@media (max-width: 900px) { .style-compare-grid { grid-template-columns: 1fr; } }
@media (max-width: 900px) { .kline-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 560px) { .kline-grid { grid-template-columns: 1fr; } }
"""


# --------------------------------------------------------------------------- #
# Chart drawing: index K-lines + stock-table K-lines.
# Reads its payload slice from __payload; draws with the shared chart kit (CK).
# --------------------------------------------------------------------------- #
KLINE_CHARTS_JS = r"""
const payload = __payload.index || {};
const stockPayload = __payload.stocks || {};
const klineDisplayDays = __payload.display_days || 120;
const indices = payload.indices || {};
const stockByCode = stockPayload.by_ts_code || {};
const stockNameIndex = stockPayload.name_to_ts_code || {};
const monthlyPayload = __payload.stocks_monthly || {};
const monthlyByCode = monthlyPayload.by_ts_code || {};
const monthlyNameIndex = monthlyPayload.name_to_ts_code || {};
const klineDisplayMonths = __payload.display_months || 72;
const reportBody = document.getElementById("report-body");
if (!reportBody) return;

const { svgEl, svgText } = CK;
const formatDate = CK.fmt.date;
const formatPercent = CK.fmt.signedPct;

const indexConfigs = [
  { key: "shanghai", anchorTexts: ["指数趋势", "上证指数趋势判断", "上证指数趋势"], fallbackTitle: "上证指数" },
  { key: "chinext", anchorTexts: ["指数趋势", "创业板趋势判断", "创业板指数趋势判断", "创业板指数趋势"], fallbackTitle: "创业板指数" },
  { key: "star50", anchorTexts: ["指数趋势", "科创50趋势判断", "科创50指数趋势", "科创50"], fallbackTitle: "科创50" }
];
const stockSectionConfigs = [
  { headingText: "3.3", gridLabel: "module3-leaders" },
  { headingText: "5.1", gridLabel: "module5-capacity-up" },
  { headingText: "5.3", gridLabel: "module5-early-limit" },
  { headingText: "5.4", gridLabel: "module5-discount-relaunch" }
];

insertIndexKlines();
insertStockTableKlines();
insertMonthlyBreakoutKlines();

function insertIndexKlines() {
  const prepared = indexConfigs.map(config => {
    const indexData = indices[config.key] || {};
    const rows = normalizeRows(indexData.records).slice(-klineDisplayDays);
    return rows.length ? { ...config, indexData, rows } : null;
  }).filter(Boolean);
  if (!prepared.length) return;

  const trendHeading = findHeading("指数趋势");
  const trendTable = trendHeading ? findNextTableWrap(trendHeading) : null;
  const anchor = trendTable ? { element: trendTable, insert: "after" } : findInsertionAnchor(indexConfigs[0].anchorTexts) || findInsertionAnchor(indexConfigs.flatMap(c => c.anchorTexts));
  if (!anchor) return;

  const grid = document.createElement("div");
  grid.className = "kline-grid";
  prepared.forEach(item => {
    grid.appendChild(buildKlineCard(item.rows, item.indexData, item.fallbackTitle));
  });
  if (anchor.insert === "after") {
    anchor.element.after(grid);
  } else {
    anchor.element.before(grid);
  }
}

function insertStockTableKlines() {
  stockSectionConfigs.forEach(config => {
    const heading = findHeading(config.headingText);
    if (!heading) return;
    const tableWrap = findNextTableWrap(heading);
    if (!tableWrap || tableWrap.dataset.stockKlinesInserted === "1") return;

    const names = extractStockNames(tableWrap);
    const prepared = names.map(name => {
      const stockData = findStockData(name);
      if (!stockData) return null;
      const rows = normalizeRows(stockData.records).slice(-klineDisplayDays);
      return rows.length ? { rows, stockData: { ...stockData, name }, fallbackTitle: name } : null;
    }).filter(Boolean);
    if (!prepared.length) return;

    const grid = document.createElement("div");
    grid.className = `stock-kline-grid stock-kline-grid-${config.gridLabel}`;
    prepared.forEach(item => {
      grid.appendChild(buildKlineCard(item.rows, item.stockData, item.fallbackTitle));
    });
    tableWrap.after(grid);
    tableWrap.dataset.stockKlinesInserted = "1";
  });
}

// 5.2 全市场月线平台突破：画月线 K 线 + 多年底部箱体阴影 + 箱体上沿 pivot 线 + 突破月标记。
function insertMonthlyBreakoutKlines() {
  const heading = findHeading("5.2");
  if (!heading) return;
  const tableWrap = findNextTableWrap(heading);
  if (!tableWrap || tableWrap.dataset.stockKlinesInserted === "1") return;
  const names = extractStockNames(tableWrap);
  const prepared = names.map(name => {
    const data = findMonthlyData(name);
    if (!data) return null;
    const rows = normalizeRows(data.records).slice(-klineDisplayMonths);
    return rows.length ? { rows, data: { ...data, name }, fallbackTitle: name } : null;
  }).filter(Boolean);
  if (!prepared.length) return;
  const grid = document.createElement("div");
  grid.className = "stock-kline-grid stock-kline-grid-module5-monthly-base";
  prepared.forEach(item => {
    grid.appendChild(buildMonthlyCard(item.rows, item.data, item.fallbackTitle));
  });
  tableWrap.after(grid);
  tableWrap.dataset.stockKlinesInserted = "1";
}

function findMonthlyData(name) {
  const normalized = normalizeStockName(name);
  const tsCode = monthlyNameIndex[name] || monthlyNameIndex[normalized];
  if (!tsCode) return null;
  return monthlyByCode[tsCode] || null;
}

function buildMonthlyCard(rows, data, fallbackTitle) {
  const card = document.createElement("article");
  card.className = "kline-card";
  card.style.position = "relative";
  const title = document.createElement("div");
  title.className = "chart-title";
  title.textContent = `${data.name || fallbackTitle} 月线 · 多年底部箱体突破`;
  const subtitle = document.createElement("div");
  subtitle.className = "chart-subtitle";
  const first = rows[0];
  const last = rows[rows.length - 1];
  const pivot = Number(data.base_top_pivot);
  subtitle.textContent = `${formatMonth(first.trade_date)} 至 ${formatMonth(last.trade_date)} · ${rows.length} 个月`
    + (Number.isFinite(pivot) ? ` · 箱体上沿 ${pivot.toFixed(2)}` : "");
  card.appendChild(title);
  card.appendChild(subtitle);
  card.appendChild(drawMonthlyKline(rows, card, data));
  card.appendChild(CK.legend([
    ["月K", "var(--neg)"],
    ["箱体上沿", "var(--orange)"],
    ["横盘箱体", "rgba(245,158,11,0.18)"],
    ["成交量", "rgba(100,116,139,0.55)"]
  ]));
  return card;
}

function drawMonthlyKline(rows, card, meta) {
  const width = 560;
  const height = 340;
  const pad = { left: 48, right: 14, top: 12, bottom: 24 };
  const usableW = width - pad.left - pad.right;
  const volPanelH = 64;
  const panelGap = 16;
  const priceH = height - pad.top - pad.bottom - volPanelH - panelGap;
  const volTop = pad.top + priceH + panelGap;
  const volBottom = volTop + volPanelH;
  const svg = svgEl("svg", { viewBox: `0 0 ${width} ${height}`, role: "img" });

  const pivot = Number(meta && meta.base_top_pivot);
  const allPrices = rows.flatMap(r => [r.high, r.low]).filter(Number.isFinite);
  if (Number.isFinite(pivot)) allPrices.push(pivot);
  let min = Math.min(...allPrices);
  let max = Math.max(...allPrices);
  if (!Number.isFinite(min) || !Number.isFinite(max)) { min = 0; max = 1; }
  if (min === max) { min -= 1; max += 1; }
  const span = max - min;
  min -= span * 0.05;
  max += span * 0.08;

  const x = idx => pad.left + (rows.length <= 1 ? usableW / 2 : idx / (rows.length - 1) * usableW);
  const y = price => pad.top + (max - price) / (max - min) * priceH;
  const candleWidth = Math.max(2, Math.min(7, usableW / Math.max(rows.length, 1) * 0.62));
  const vols = rows.map(r => r.vol).filter(v => Number.isFinite(v) && v > 0);
  const maxVol = vols.length ? Math.max(...vols) : 1;
  const volY = v => volBottom - (v / maxVol) * volPanelH;

  for (let i = 0; i <= 4; i += 1) {
    const gy = pad.top + priceH * i / 4;
    svg.appendChild(svgEl("line", { x1: pad.left, x2: width - pad.right, y1: gy, y2: gy, class: "grid-line" }));
  }
  svg.appendChild(svgEl("line", { x1: pad.left, x2: width - pad.right, y1: pad.top + priceH, y2: pad.top + priceH, class: "axis" }));
  svg.appendChild(svgEl("line", { x1: pad.left, x2: width - pad.right, y1: volBottom, y2: volBottom, class: "axis" }));

  // 横盘箱体阴影：箱体上沿成形月 → 突破月、上沿以下区域。
  const startIdx = findMonthIndex(rows, meta && meta.base_start_month);
  const breakIdx = findMonthIndex(rows, meta && meta.breakout_month);
  if (Number.isFinite(pivot) && startIdx >= 0) {
    const bx = x(startIdx);
    const bxEnd = breakIdx >= 0 ? x(breakIdx) : x(rows.length - 1);
    const boxTop = y(pivot);
    const boxBottom = pad.top + priceH;
    svg.appendChild(svgEl("rect", {
      x: bx.toFixed(2), y: boxTop.toFixed(2),
      width: Math.max(1, bxEnd - bx).toFixed(2),
      height: Math.max(1, boxBottom - boxTop).toFixed(2),
      fill: "rgba(245,158,11,0.14)", stroke: "none"
    }));
  }

  const tooltip = CK.tooltip(card);
  rows.forEach((row, idx) => {
    const px = x(idx);
    const up = row.close >= row.open;
    const cls = up ? "kline-candle-up" : "kline-candle-down";
    if (Number.isFinite(row.vol) && row.vol > 0) {
      const barTop = volY(row.vol);
      svg.appendChild(svgEl("rect", {
        x: (px - candleWidth / 2).toFixed(2), y: barTop.toFixed(2),
        width: candleWidth.toFixed(2), height: Math.max(1, volBottom - barTop).toFixed(2),
        class: `amount-bar ${up ? "amount-bar-up" : "amount-bar-down"}`, rx: 1
      }));
    }
    const bodyTop = y(Math.max(row.open, row.close));
    const bodyBottom = y(Math.min(row.open, row.close));
    svg.appendChild(svgEl("line", {
      x1: px.toFixed(2), x2: px.toFixed(2),
      y1: y(row.high).toFixed(2), y2: y(row.low).toFixed(2),
      class: `kline-wick ${cls}`
    }));
    svg.appendChild(svgEl("rect", {
      x: (px - candleWidth / 2).toFixed(2), y: bodyTop.toFixed(2),
      width: candleWidth.toFixed(2), height: Math.max(1, bodyBottom - bodyTop).toFixed(2),
      class: cls, rx: 1, opacity: 0.88
    }));
    const hit = svgEl("rect", {
      x: (px - Math.max(candleWidth, 4) / 2).toFixed(2), y: pad.top,
      width: Math.max(candleWidth, 4).toFixed(2), height: volBottom - pad.top,
      fill: "transparent", stroke: "none", style: "cursor:pointer"
    });
    hit.addEventListener("mouseenter", () => {
      tooltip.innerHTML = [
        `<div style="color:#94a3b8;font-size:11px;margin-bottom:2px;">${formatMonth(row.trade_date)}</div>`,
        `<div>开: ${formatNumber(row.open)} 高: ${formatNumber(row.high)}</div>`,
        `<div>低: ${formatNumber(row.low)} 收: ${formatNumber(row.close)}</div>`
      ].join("");
      tooltip.style.opacity = "1";
    });
    hit.addEventListener("mousemove", event => CK.moveTip(tooltip, card, event));
    hit.addEventListener("mouseleave", () => { tooltip.style.opacity = "0"; });
    svg.appendChild(hit);
  });

  if (Number.isFinite(pivot)) {
    const py = y(pivot);
    svg.appendChild(svgEl("line", {
      x1: pad.left, x2: width - pad.right, y1: py.toFixed(2), y2: py.toFixed(2),
      stroke: "var(--orange)", "stroke-width": 1.3, "stroke-dasharray": "5 3", opacity: 0.95
    }));
    svg.appendChild(svgText(width - pad.right - 2, py - 4, `上沿 ${pivot.toFixed(2)}`, "end", "var(--orange)"));
  }

  if (breakIdx >= 0) {
    const bxp = x(breakIdx);
    svg.appendChild(svgEl("line", {
      x1: bxp.toFixed(2), x2: bxp.toFixed(2), y1: pad.top, y2: pad.top + priceH,
      stroke: "var(--neg)", "stroke-width": 1, "stroke-dasharray": "2 3", opacity: 0.6
    }));
    svg.appendChild(svgText(bxp, pad.top + 10, "突破", "middle", "var(--neg)"));
  }

  svg.appendChild(svgText(4, pad.top + 4, formatNumber(max), "start", "var(--text-tertiary)"));
  svg.appendChild(svgText(4, pad.top + priceH, formatNumber(min), "start", "var(--text-tertiary)"));
  svg.appendChild(svgText(4, volTop + 12, "成交量", "start", "var(--text-tertiary)"));
  return svg;
}

function findMonthIndex(rows, monthLabel) {
  if (!monthLabel) return -1;
  const target = String(monthLabel).replace(/[^0-9]/g, "").slice(0, 6);
  if (target.length < 6) return -1;
  for (let i = 0; i < rows.length; i += 1) {
    const ym = String(rows[i].trade_date || "").replace(/[^0-9]/g, "").slice(0, 6);
    if (ym === target) return i;
  }
  for (let i = 0; i < rows.length; i += 1) {
    const ym = String(rows[i].trade_date || "").replace(/[^0-9]/g, "").slice(0, 6);
    if (ym >= target) return i;
  }
  return -1;
}

function formatMonth(value) {
  const digits = String(value || "").replace(/[^0-9]/g, "");
  if (digits.length >= 6) return `${digits.slice(0, 4)}-${digits.slice(4, 6)}`;
  return formatDate(value);
}

function findInsertionAnchor(texts) {
  const anchors = reportBody.querySelectorAll("p, h2, h3, h4");
  for (const text of texts) {
    for (const element of anchors) {
      if (!element.textContent.includes(text)) continue;
      const tag = element.tagName.toLowerCase();
      return { element, insert: tag === "h2" || tag === "h3" || tag === "h4" ? "after" : "before" };
    }
  }
  return null;
}

function findHeading(text) {
  return Array.from(reportBody.querySelectorAll("h3, h4")).find(e => e.textContent.includes(text));
}

function findNextTableWrap(heading) {
  let current = heading.nextElementSibling;
  while (current) {
    if (current.classList && current.classList.contains("table-wrap")) return current;
    if (/^H[234]$/.test(current.tagName || "")) return null;
    current = current.nextElementSibling;
  }
  return null;
}

function extractStockNames(tableWrap) {
  const headers = Array.from(tableWrap.querySelectorAll("thead th")).map(c => normalizeStockName(c.textContent));
  const stockIndex = headers.indexOf("股票");
  if (stockIndex < 0) return [];
  return Array.from(tableWrap.querySelectorAll("tbody tr"))
    .map(row => row.children[stockIndex] ? normalizeStockName(row.children[stockIndex].textContent) : "")
    .filter(Boolean);
}

function findStockData(name) {
  const normalized = normalizeStockName(name);
  const tsCode = stockNameIndex[name] || stockNameIndex[normalized];
  if (!tsCode) return null;
  return stockByCode[tsCode] || null;
}

function normalizeStockName(value) {
  return String(value || "")
    .replace(/\s+/g, "")
    .replace(/[（(]\d{6}\.(?:SH|SZ|BJ)[)）]/g, "")
    .trim();
}

function normalizeRows(records) {
  return (Array.isArray(records) ? records : [])
    .map(row => ({
      trade_date: String(row.trade_date || ""),
      open: toNumber(row.open),
      high: toNumber(row.high),
      low: toNumber(row.low),
      close: toNumber(row.close),
      pct_chg: toNumber(row.pct_chg),
      amount: toNumber(row.amount),
      vol: toNumber(row.vol)
    }))
    .filter(row => row.trade_date && [row.open, row.high, row.low, row.close].every(Number.isFinite))
    .sort((a, b) => a.trade_date.localeCompare(b.trade_date));
}

function buildKlineCard(rows, indexData, fallbackTitle) {
  const card = document.createElement("article");
  card.className = "kline-card";
  card.style.position = "relative";

  const title = document.createElement("div");
  title.className = "chart-title";
  title.textContent = `${indexData.name || fallbackTitle} ${klineDisplayDays}日K线`;
  const subtitle = document.createElement("div");
  subtitle.className = "chart-subtitle";
  const first = rows[0];
  const last = rows[rows.length - 1];
  const requested = Number(indexData.kline_days_requested) || klineDisplayDays;
  subtitle.textContent = `${formatDate(first.trade_date)} 至 ${formatDate(last.trade_date)} · ${rows.length}/${requested} 个交易日`;
  card.appendChild(title);
  card.appendChild(subtitle);
  card.appendChild(drawKline(rows, card));

  card.appendChild(CK.legend([
    ["K线", "var(--neg)"],
    ["MA20", "var(--blue)"],
    ["MA60", "var(--orange)"],
    ["成交金额", "rgba(100,116,139,0.55)"]
  ]));
  return card;
}

function drawKline(rows, card) {
  const enriched = rows.map((row, idx) => ({
    ...row, idx,
    ma20: rollingAverage(rows, idx, 20),
    ma60: rollingAverage(rows, idx, 60)
  }));
  const width = 560;
  const height = 340;
  const pad = { left: 48, right: 14, top: 12, bottom: 24 };
  const usableW = width - pad.left - pad.right;
  const amountPanelH = 64;
  const panelGap = 16;
  const priceH = height - pad.top - pad.bottom - amountPanelH - panelGap;
  const amountTop = pad.top + priceH + panelGap;
  const amountBottom = amountTop + amountPanelH;
  const svg = svgEl("svg", { viewBox: `0 0 ${width} ${height}`, role: "img" });

  const allPrices = enriched.flatMap(row => [row.high, row.low, row.ma20, row.ma60]).filter(Number.isFinite);
  let min = Math.min(...allPrices);
  let max = Math.max(...allPrices);
  if (min === max) { min -= 1; max += 1; }
  const span = max - min;
  min -= span * 0.05;
  max += span * 0.05;

  const x = idx => pad.left + (enriched.length <= 1 ? usableW / 2 : idx / (enriched.length - 1) * usableW);
  const y = price => pad.top + (max - price) / (max - min) * priceH;
  const candleWidth = Math.max(2, Math.min(8, usableW / Math.max(enriched.length, 1) * 0.62));
  const amounts = enriched.map(row => row.amount).filter(value => Number.isFinite(value) && value > 0);
  const maxAmount = amounts.length ? Math.max(...amounts) : 1;
  const amountY = value => amountBottom - (value / maxAmount) * amountPanelH;

  for (let i = 0; i <= 4; i += 1) {
    const gy = pad.top + priceH * i / 4;
    svg.appendChild(svgEl("line", { x1: pad.left, x2: width - pad.right, y1: gy, y2: gy, class: "grid-line" }));
  }
  svg.appendChild(svgEl("line", { x1: pad.left, x2: width - pad.right, y1: pad.top + priceH, y2: pad.top + priceH, class: "axis" }));
  svg.appendChild(svgEl("line", { x1: pad.left, x2: width - pad.right, y1: amountBottom, y2: amountBottom, class: "axis" }));
  svg.appendChild(svgEl("line", { x1: pad.left, x2: width - pad.right, y1: amountTop, y2: amountTop, class: "grid-line", opacity: 0.55 }));

  const tooltip = CK.tooltip(card);

  enriched.forEach(row => {
    const px = x(row.idx);
    const up = row.close >= row.open;
    const cls = up ? "kline-candle-up" : "kline-candle-down";
    if (Number.isFinite(row.amount) && row.amount > 0) {
      const barTop = amountY(row.amount);
      const amountCls = up ? "amount-bar-up" : "amount-bar-down";
      svg.appendChild(svgEl("rect", {
        x: (px - candleWidth / 2).toFixed(2),
        y: barTop.toFixed(2),
        width: candleWidth.toFixed(2),
        height: Math.max(1, amountBottom - barTop).toFixed(2),
        class: `amount-bar ${amountCls}`,
        rx: 1
      }));
    }
    const bodyTop = y(Math.max(row.open, row.close));
    const bodyBottom = y(Math.min(row.open, row.close));
    const bodyHeight = Math.max(1, bodyBottom - bodyTop);
    svg.appendChild(svgEl("line", {
      x1: px.toFixed(2), x2: px.toFixed(2),
      y1: y(row.high).toFixed(2), y2: y(row.low).toFixed(2),
      class: `kline-wick ${cls}`
    }));
    svg.appendChild(svgEl("rect", {
      x: (px - candleWidth / 2).toFixed(2),
      y: bodyTop.toFixed(2),
      width: candleWidth.toFixed(2),
      height: bodyHeight.toFixed(2),
      class: cls, rx: 1, opacity: 0.88
    }));
    const hit = svgEl("rect", {
      x: (px - Math.max(candleWidth, 4) / 2).toFixed(2),
      y: pad.top,
      width: Math.max(candleWidth, 4).toFixed(2),
      height: amountBottom - pad.top,
      fill: "transparent", stroke: "none",
      style: "cursor:pointer"
    });
    hit.addEventListener("mouseenter", () => {
      tooltip.innerHTML = [
        `<div style="color:#94a3b8;font-size:11px;margin-bottom:2px;">${formatDate(row.trade_date)}</div>`,
        `<div>开: ${formatNumber(row.open)} 高: ${formatNumber(row.high)}</div>`,
        `<div>低: ${formatNumber(row.low)} 收: ${formatNumber(row.close)}</div>`,
        `<div>涨跌幅: ${formatPercent(row.pct_chg)} · 成交额: ${formatAmount(row.amount)}</div>`
      ].join("");
      tooltip.style.opacity = "1";
    });
    hit.addEventListener("mousemove", event => CK.moveTip(tooltip, card, event));
    hit.addEventListener("mouseleave", () => { tooltip.style.opacity = "0"; });
    svg.appendChild(hit);
  });

  drawMaLine(enriched, "ma20", "var(--blue)");
  drawMaLine(enriched, "ma60", "var(--orange)");

  svg.appendChild(svgText(4, pad.top + 4, formatNumber(max), "start", "var(--text-tertiary)"));
  svg.appendChild(svgText(4, pad.top + priceH, formatNumber(min), "start", "var(--text-tertiary)"));
  svg.appendChild(svgText(4, amountTop + 12, "成交金额", "start", "var(--text-tertiary)"));
  svg.appendChild(svgText(4, amountTop + 28, formatAmount(maxAmount), "start", "var(--text-tertiary)"));
  return svg;

  function drawMaLine(items, key, color) {
    const points = items.filter(row => Number.isFinite(row[key]));
    if (!points.length) return;
    const d = points.map((row, idx) => `${idx === 0 ? "M" : "L"} ${x(row.idx).toFixed(2)} ${y(row[key]).toFixed(2)}`).join(" ");
    svg.appendChild(svgEl("path", { d, class: "ma-line", style: `stroke: ${color}` }));
  }
}

function rollingAverage(rows, idx, windowSize) {
  if (idx + 1 < windowSize) return null;
  const slice = rows.slice(idx - windowSize + 1, idx + 1).map(row => row.close).filter(Number.isFinite);
  if (slice.length !== windowSize) return null;
  return slice.reduce((sum, value) => sum + value, 0) / windowSize;
}
function toNumber(value) { const n = Number(value); return Number.isFinite(n) ? n : null; }
function formatNumber(value) {
  if (!Number.isFinite(value)) return "—";
  const abs = Math.abs(value);
  const digits = abs >= 1000 ? 1 : abs >= 100 ? 2 : 3;
  return value.toFixed(digits);
}
function formatAmount(value) {
  if (!Number.isFinite(value)) return "—";
  return `${(value / 100000).toFixed(2)}亿`;
}
"""


# --------------------------------------------------------------------------- #
# Market-style normalized comparison charts driven by evidence market_style.series.
# --------------------------------------------------------------------------- #
STYLE_COMPARE_JS = r"""
const payload = __payload || {};
const reportBody = document.getElementById("report-body");
if (!reportBody) return;

const styleItems = Array.isArray(payload.indices) ? payload.indices : [];
if (!styleItems.length) return;

const { svgEl, svgText } = CK;
const formatDate = CK.fmt.date;
const displayDays = Number(payload.display_days) || 60;
const byKey = {};
styleItems.forEach(item => { byKey[item.key] = item; });

const chartDefs = [
  {
    title: "规模轴 · 归一化走势（60 日，起点=100）",
    keys: ["mega_cap", "csi300", "csi500", "csi1000", "guozheng2000"],
    footnoteKey: "guozheng2000",
    styles: {
      csi300: { color: "var(--blue)", width: 2.8, dash: "" },
      guozheng2000: { color: "var(--neg)", width: 2.1, dash: "" },
      csi500: { color: "var(--pos)", width: 2.0, dash: "9 5" },
      csi1000: { color: "var(--orange)", width: 2.0, dash: "4 4" },
      mega_cap: { color: "var(--ink-3)", width: 2.0, dash: "1 4" }
    }
  },
  {
    title: "成长 / 价值 / 红利 · 归一化走势（60 日，起点=100）",
    keys: ["csi300_growth", "csi300_value", "csi_dividend"],
    styles: {
      csi300_growth: { color: "var(--violet)", width: 2.8, dash: "" },
      csi300_value: { color: "var(--ink-3)", width: 2.0, dash: "9 5" },
      csi_dividend: { color: "var(--orange)", width: 2.0, dash: "1 4" }
    }
  }
];

const charts = chartDefs.map(def => prepareChart(def)).filter(Boolean);
if (!charts.length) return;

const anchor = findStyleAnchor();
if (!anchor) return;

const grid = document.createElement("div");
grid.className = "style-compare-grid";
charts.forEach(chart => grid.appendChild(buildChartCard(chart)));

if (anchor.table) {
  anchor.table.after(grid);
} else {
  anchor.element.after(grid);
}

/* Anchor on the 1.3 heading; reports written with bold pseudo-headings
   (report_template.md style, <p><strong>1.3 市场风格</strong></p>) fall back to
   that paragraph, with the sibling walk stopping at the next pseudo-heading. */
function findStyleAnchor() {
  const heading = CK.findHeading(reportBody, "市场风格", "h2, h3, h4");
  if (heading) return { element: heading, table: CK.findNextTable(heading) };
  const strong = Array.from(reportBody.querySelectorAll("p > strong"))
    .find(el => (el.textContent || "").includes("市场风格"));
  if (!strong) return null;
  const para = strong.closest("p");
  let cur = para.nextElementSibling;
  let table = null;
  while (cur) {
    if (cur.classList && cur.classList.contains("table-wrap")) { table = cur; break; }
    if (/^H[234]$/.test(cur.tagName || "")) break;
    if (cur.tagName === "P" && cur.firstElementChild && cur.firstElementChild.tagName === "STRONG") break;
    cur = cur.nextElementSibling;
  }
  return { element: para, table };
}

function prepareChart(def) {
  const sliced = def.keys.map(key => {
    const item = byKey[key];
    if (!item) return null;
    const rows = normalizeRecords(item.records).slice(-displayDays);
    return rows.length ? { item, key, rows } : null;
  }).filter(Boolean);
  if (sliced.length < 2) return null;
  /* rebase every line of a chart from the latest common start date so the
     lines stay comparable when one series is shorter than the window */
  const commonStart = sliced.reduce(
    (acc, entry) => (entry.rows[0].trade_date > acc ? entry.rows[0].trade_date : acc),
    sliced[0].rows[0].trade_date
  );
  const series = sliced.map(({ item, key, rows }) => {
    const trimmed = rows.filter(row => row.trade_date >= commonStart);
    if (trimmed.length < 2 || !Number.isFinite(trimmed[0].close) || trimmed[0].close === 0) return null;
    const base = trimmed[0].close;
    const points = trimmed.map(row => ({
      date: row.trade_date,
      value: round2(row.close / base * 100)
    })).filter(point => Number.isFinite(point.value));
    if (points.length < 2) return null;
    return {
      key,
      name: item.name || key,
      styleRole: item.style_role || "",
      proxyNote: item.proxy_note || "",
      style: def.styles[key] || { color: "var(--blue)", width: 2, dash: "" },
      points
    };
  }).filter(Boolean);
  if (series.length < 2) return null;
  const dates = Array.from(new Set(series.flatMap(item => item.points.map(point => point.date)))).sort();
  return { def, series, dates };
}

function normalizeRecords(records) {
  return (Array.isArray(records) ? records : [])
    .map(row => ({
      trade_date: String(row.trade_date || ""),
      close: Number(row.close)
    }))
    .filter(row => row.trade_date && Number.isFinite(row.close))
    .sort((a, b) => a.trade_date.localeCompare(b.trade_date));
}

function buildChartCard(chart) {
  const start = chart.dates[0];
  const end = chart.dates[chart.dates.length - 1];
  const card = CK.card(
    "chart-card style-compare-card",
    chart.def.title,
    `${formatDate(start)} 至 ${formatDate(end)} · 数据截至 ${formatDate(payload.trade_date || end)} · Baostock`
  );
  card.appendChild(drawNormalizedLines(chart, card));
  card.appendChild(buildLineLegend(chart.series));
  const footnote = chart.def.footnoteKey ? (byKey[chart.def.footnoteKey] || {}).proxy_note : "";
  if (footnote) {
    const note = document.createElement("div");
    note.className = "style-compare-note";
    note.textContent = footnote;
    card.appendChild(note);
  }
  return card;
}

function drawNormalizedLines(chart, card) {
  const width = 560;
  const height = 280;
  const pad = { left: 44, right: 18, top: 14, bottom: 30 };
  const usableW = width - pad.left - pad.right;
  const usableH = height - pad.top - pad.bottom;
  const svg = svgEl("svg", { viewBox: `0 0 ${width} ${height}`, role: "img" });
  const allValues = chart.series.flatMap(item => item.points.map(point => point.value));
  let min = Math.min(...allValues, 100);
  let max = Math.max(...allValues, 100);
  if (min === max) { min -= 1; max += 1; }
  const span = max - min;
  min -= span * 0.04;
  max += span * 0.04;

  const dateIndex = new Map(chart.dates.map((date, idx) => [date, idx]));
  const x = date => pad.left + (chart.dates.length <= 1 ? usableW / 2 : dateIndex.get(date) / (chart.dates.length - 1) * usableW);
  const y = value => pad.top + (max - value) / (max - min) * usableH;

  for (let i = 0; i <= 4; i += 1) {
    const value = min + (max - min) * (4 - i) / 4;
    const gy = y(value);
    svg.appendChild(svgEl("line", { x1: pad.left, x2: width - pad.right, y1: gy, y2: gy, class: "grid-line" }));
    svg.appendChild(svgText(4, gy + 3, value.toFixed(1), "start", "var(--text-tertiary)"));
  }
  if (min <= 100 && max >= 100) {
    svg.appendChild(svgEl("line", {
      x1: pad.left, x2: width - pad.right, y1: y(100), y2: y(100),
      class: "axis", "stroke-width": 1.8, opacity: 0.85
    }));
  }
  svg.appendChild(svgEl("line", { x1: pad.left, x2: width - pad.right, y1: height - pad.bottom, y2: height - pad.bottom, class: "axis" }));

  const tickDates = pickTicks(chart.dates, 6);
  tickDates.forEach(date => {
    const px = x(date);
    svg.appendChild(svgEl("line", { x1: px, x2: px, y1: height - pad.bottom, y2: height - pad.bottom + 4, class: "axis" }));
    svg.appendChild(svgText(px, height - 10, formatDate(date).slice(5), "middle", "var(--text-tertiary)", 10));
  });

  chart.series.forEach(item => {
    const d = item.points.map((point, idx) => `${idx === 0 ? "M" : "L"} ${x(point.date).toFixed(2)} ${y(point.value).toFixed(2)}`).join(" ");
    svg.appendChild(svgEl("path", {
      d,
      fill: "none",
      stroke: item.style.color,
      "stroke-width": item.style.width,
      "stroke-linecap": "round",
      "stroke-linejoin": "round",
      "stroke-dasharray": item.style.dash || ""
    }));
  });

  const tooltip = CK.tooltip(card);
  const hitWidth = Math.max(6, usableW / Math.max(chart.dates.length, 1));
  chart.dates.forEach(date => {
    const px = x(date);
    const hit = svgEl("rect", {
      x: (px - hitWidth / 2).toFixed(2),
      y: pad.top,
      width: hitWidth.toFixed(2),
      height: usableH,
      fill: "transparent",
      stroke: "none",
      style: "cursor:pointer"
    });
    hit.addEventListener("mouseenter", () => {
      const rows = chart.series.map(item => {
        const point = item.points.find(p => p.date === date);
        return point ? `<div>${item.name}: <strong>${point.value.toFixed(1)}</strong></div>` : "";
      }).filter(Boolean);
      tooltip.innerHTML = [`<div style="color:#94a3b8;font-size:11px;margin-bottom:2px;">${formatDate(date)}</div>`].concat(rows).join("");
      tooltip.style.opacity = rows.length ? "1" : "0";
    });
    hit.addEventListener("mousemove", event => CK.moveTip(tooltip, card, event));
    hit.addEventListener("mouseleave", () => { tooltip.style.opacity = "0"; });
    svg.appendChild(hit);
  });
  return svg;
}

function buildLineLegend(series) {
  const legend = document.createElement("div");
  legend.className = "style-compare-legend";
  series.forEach(item => {
    const entry = document.createElement("span");
    const icon = svgEl("svg", { viewBox: "0 0 24 8", "aria-hidden": "true" });
    icon.appendChild(svgEl("line", {
      x1: 1, x2: 23, y1: 4, y2: 4,
      stroke: item.style.color,
      "stroke-width": item.style.width,
      "stroke-linecap": "round",
      "stroke-dasharray": item.style.dash || ""
    }));
    entry.appendChild(icon);
    entry.appendChild(document.createTextNode(item.name));
    legend.appendChild(entry);
  });
  return legend;
}

function pickTicks(dates, count) {
  if (dates.length <= count) return dates;
  const out = [];
  const last = dates.length - 1;
  for (let i = 0; i < count; i += 1) {
    out.push(dates[Math.round(i * last / (count - 1))]);
  }
  return Array.from(new Set(out));
}

function round2(value) { return Math.round(value * 100) / 100; }
"""


# --------------------------------------------------------------------------- #
# Market-trend mini-chart panel driven by market_data.json.
# --------------------------------------------------------------------------- #
MARKET_TRENDS_JS = r"""
const data = __payload || {};
const records = Array.isArray(data.records) ? data.records.filter(r => r && r.trade_date).slice(-90) : [];
if (!records.length) return;

const reportBody = document.getElementById("report-body");
const { svgEl, svgText } = CK;
const formatDate = CK.fmt.date;
const headings = reportBody.querySelectorAll("h2, h3, h4");
let targetHeading = null;
for (const h of headings) {
  if (h.textContent.includes("1.1") && h.textContent.includes("情绪趋势")) { targetHeading = h; break; }
}

const chartSection = document.createElement("div");
chartSection.className = "chart-grid";
chartSection.style.marginTop = "18px";

const charts = [
  { title: "成交额趋势", fields: [{ key: "成交额", color: "var(--blue)", scale: 1e9, unit: "万亿" }] },
  { title: "活跃度 / 情绪值", fields: [{ key: "活跃度", color: "var(--orange)" }, { key: "情绪值", color: "var(--purple)" }] },
  { title: "融资净买入", type: "bar", fields: [{ key: "融资净买入", color: "var(--green)", scale: 1e8, unit: "亿" }] },
  { title: "上涨 vs 下跌家数", fields: [{ key: "上涨", color: "var(--red)" }, { key: "下跌", color: "var(--green)" }] },
  { title: "涨停 vs 跌停家数", fields: [{ key: "涨停", color: "var(--red)" }, { key: "跌停", color: "var(--green)" }] },
];

charts.forEach(config => {
  const card = document.createElement("article");
  card.className = "chart-card";
  const title = document.createElement("div");
  title.className = "chart-title";
  title.textContent = config.title;
  const subtitle = document.createElement("div");
  subtitle.className = "chart-subtitle";
  card.appendChild(title);
  const drawable = drawChart(records, config, card, subtitle);
  card.appendChild(drawable);
  card.appendChild(CK.legend(config.fields.map(field => [field.key, field.color])));
  chartSection.appendChild(card);
});

if (targetHeading) {
  let insertAfter = targetHeading;
  let sibling = targetHeading.nextElementSibling;
  while (sibling) {
    if (/^H[234]$/.test(sibling.tagName || "")) break;
    insertAfter = sibling;
    sibling = sibling.nextElementSibling;
  }
  insertAfter.after(chartSection);
} else {
  reportBody.appendChild(chartSection);
}

function drawChart(rows, config, card, subtitle) {
  const width = 480;
  const height = 200;
  const pad = { left: 42, right: 16, top: 14, bottom: 28 };
  const usableW = width - pad.left - pad.right;
  const usableH = height - pad.top - pad.bottom;
  const svg = svgEl("svg", { viewBox: `0 0 ${width} ${height}`, role: "img" });
  const series = config.fields.map(field => {
    const points = rows.map((row, idx) => {
      const raw = row[field.key];
      const value = typeof raw === "number" ? raw / (field.scale || 1) : null;
      return { idx, date: row.trade_date, value };
    }).filter(p => Number.isFinite(p.value));
    return { field, points };
  }).filter(item => item.points.length);
  if (!series.length) {
    svg.appendChild(svgText(width / 2, height / 2, "暂无数据", "middle", "var(--text-tertiary)"));
    subtitle.textContent = "该列暂无可绘制数值";
    return svg;
  }
  const allValues = series.flatMap(item => item.points.map(p => p.value));
  let min = Math.min(...allValues);
  let max = Math.max(...allValues);
  if (min === max) { min -= 1; max += 1; }
  const span = max - min;
  min -= span * 0.08;
  max += span * 0.08;
  const x = idx => pad.left + (rows.length <= 1 ? usableW / 2 : idx / (rows.length - 1) * usableW);
  const y = value => pad.top + (max - value) / (max - min) * usableH;
  for (let i = 0; i <= 4; i += 1) {
    const gy = pad.top + usableH * i / 4;
    svg.appendChild(svgEl("line", { x1: pad.left, x2: width - pad.right, y1: gy, y2: gy, class: "grid-line" }));
  }
  svg.appendChild(svgEl("line", { x1: pad.left, x2: width - pad.right, y1: height - pad.bottom, y2: height - pad.bottom, class: "axis" }));

  const tooltip = CK.tooltip(card);

  const isBar = config.type === "bar";
  const barWidth = isBar ? Math.max(2, usableW / rows.length * 0.55) : 0;
  const y0 = y(0);

  series.forEach(item => {
    if (isBar) {
      item.points.forEach(p => {
        const px = x(p.idx);
        const py = y(p.value);
        const barH = Math.abs(py - y0);
        const barY = p.value >= 0 ? py : y0;
        const barColor = p.value >= 0 ? "var(--red)" : "var(--green)";
        const rect = svgEl("rect", {
          x: (px - barWidth / 2).toFixed(2),
          y: barY.toFixed(2),
          width: barWidth.toFixed(2),
          height: Math.max(1, barH).toFixed(2),
          fill: barColor, rx: 2, opacity: 0.85
        });
        svg.appendChild(rect);
        const hit = svgEl("rect", {
          x: (px - barWidth / 2).toFixed(2),
          y: Math.min(py, y0).toFixed(2),
          width: barWidth.toFixed(2),
          height: Math.max(1, barH).toFixed(2),
          fill: "transparent", stroke: "none",
          style: "cursor:pointer"
        });
        hit.addEventListener("mouseenter", () => {
          rect.setAttribute("opacity", "1");
          tooltip.innerHTML = `<div style="color:#94a3b8;font-size:11px;margin-bottom:2px;">${formatDate(p.date)}</div><div style="font-weight:600;">${item.field.key}: ${formatValue(p.value, item.field.unit)}</div>`;
          tooltip.style.opacity = "1";
        });
        hit.addEventListener("mousemove", e => CK.moveTip(tooltip, card, e));
        hit.addEventListener("mouseleave", () => {
          rect.setAttribute("opacity", "0.85");
          tooltip.style.opacity = "0";
        });
        svg.appendChild(hit);
      });
    } else {
      const d = item.points.map((p, i) => `${i === 0 ? "M" : "L"} ${x(p.idx).toFixed(2)} ${y(p.value).toFixed(2)}`).join(" ");
      svg.appendChild(svgEl("path", { d, class: "series-line", style: `stroke: ${item.field.color}` }));
      item.points.forEach(p => {
        svg.appendChild(svgEl("circle", {
          cx: x(p.idx).toFixed(2), cy: y(p.value).toFixed(2),
          r: 3.5, fill: item.field.color, stroke: "#ffffff", "stroke-width": 1.5
        }));
        const hit = svgEl("circle", {
          cx: x(p.idx).toFixed(2), cy: y(p.value).toFixed(2),
          r: 10, fill: "transparent", stroke: "none",
          style: "cursor:pointer"
        });
        hit.addEventListener("mouseenter", () => {
          tooltip.innerHTML = `<div style="color:#94a3b8;font-size:11px;margin-bottom:2px;">${formatDate(p.date)}</div><div style="font-weight:600;">${item.field.key}: ${formatValue(p.value, item.field.unit)}</div>`;
          tooltip.style.opacity = "1";
        });
        hit.addEventListener("mousemove", e => CK.moveTip(tooltip, card, e));
        hit.addEventListener("mouseleave", () => { tooltip.style.opacity = "0"; });
        svg.appendChild(hit);
      });
    }
  });
  svg.appendChild(svgText(4, pad.top + 4, formatValue(max, config.fields[0].unit), "start", "var(--text-tertiary)"));
  svg.appendChild(svgText(4, height - pad.bottom, formatValue(min, config.fields[0].unit), "start", "var(--text-tertiary)"));
  return svg;
}

function formatValue(value, unit) {
  if (!Number.isFinite(value)) return "—";
  const abs = Math.abs(value);
  const digits = abs >= 100 ? 0 : abs >= 10 ? 1 : 2;
  return `${value.toFixed(digits)}${unit || ""}`;
}
"""


# --------------------------------------------------------------------------- #
# Thin manifest: declare inputs, decorations and charts; shared runner does
# the rest (parse args, render, validate, write, print summary).
# --------------------------------------------------------------------------- #
def add_arguments(parser) -> None:
    parser.add_argument("--market-data", default=str(DEFAULT_MARKET_DATA), help="Derived market_data.json path.")
    parser.add_argument(
        "--evidence",
        default=None,
        help="Evidence JSON path. Defaults to sibling evidence_YYYYMMDD_utf8.json when input is report_YYYYMMDD.md.",
    )
    parser.add_argument(
        "--stock-klines",
        default=None,
        help="Stock kline JSON path. Defaults to sibling kline_YYYYMMDD.json; falls back to evidence stock_kline_records.",
    )
    parser.add_argument(
        "--lifecycle-days",
        type=int,
        default=22,
        help="主线生命周期区块的交易日窗口宽度。",
    )
    parser.add_argument(
        "--no-lifecycle",
        action="store_true",
        help="不注入主线生命周期区块（默认在 theme_daily_state 有数据时自动注入）。",
    )


def load_lifecycle_payload(input_path: Path, days: int) -> Optional[Dict[str, Any]]:
    """Trailing lifecycle window for the report date, or None.

    The block is optional display-layer data: any failure (no date in the
    filename, DB unreachable, empty ledger) skips it without failing the
    render.
    """
    m = re.search(r"(\d{4})-?(\d{2})-?(\d{2})", input_path.name)
    if not m:
        return None
    asof = "-".join(m.groups())
    try:
        from theme_lifecycle import build_window_payload, get_connection

        with get_connection() as conn:
            payload = build_window_payload(conn, asof, days)
    except (Exception, SystemExit) as exc:  # noqa: BLE001
        print(f"[theme-lifecycle] 跳过生命周期区块：{exc}", file=sys.stderr)
        return None
    if not payload.get("themes"):
        return None
    return payload


def build_job(args) -> RenderJob:
    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else input_path.with_suffix(".html")
    market_data_path = Path(args.market_data)
    evidence_path = Path(args.evidence) if args.evidence else default_evidence_path(input_path)
    kline_path = Path(args.stock_klines) if args.stock_klines else default_kline_path(input_path)
    markdown_text = input_path.read_text(encoding="utf-8")
    title = args.title or input_path.stem
    market_data = load_market_data(market_data_path)
    evidence = load_evidence(evidence_path)
    index_kline_data = extract_index_kline_payload(evidence, evidence_path)
    stock_klines_raw = load_stock_klines(evidence, kline_path)
    stock_kline_source = kline_path if kline_path is not None and kline_path.exists() else evidence_path
    stock_kline_data = extract_stock_kline_payload(
        stock_klines_raw,
        stock_kline_source,
        missing=bool((evidence.get("metadata") or {}).get("missing")) and not stock_klines_raw,
    )
    style_series_payload = extract_style_series_payload(evidence)

    builder = HtmlReportBuilder(title=title, theme=args.theme, extra_css=MARKET_SENSE_EXTRA_CSS)
    builder.add_decoration(PillDecoration(MARKET_SENSE_PILL_RULES))
    builder.add_decoration(HeroDecoration(
        heading_prefix="一句话盘面判断",
        collect_tags=("P",),
        max_blocks=3,
        stop_at_numbered=True,
        number_units="%|pct|倍",
        keyword_pattern=HERO_KEYWORDS,
        stop_mode="any_heading",
    ))
    builder.add_chart_hook(ChartHook(
        name="klines",
        payload={
            "index": index_kline_data,
            "stocks": stock_kline_data,
            "stocks_monthly": stock_kline_data.get("monthly") or {},
            "display_days": INDEX_KLINE_DISPLAY_DAYS,
            "display_months": MONTHLY_KLINE_DISPLAY_MONTHS,
        },
        js=KLINE_CHARTS_JS,
    ))
    builder.add_chart_hook(ChartHook(name="market-trends", payload=market_data, js=MARKET_TRENDS_JS))
    if style_series_payload:
        builder.add_chart_hook(ChartHook(name="style-compare", payload=style_series_payload, js=STYLE_COMPARE_JS))

    lifecycle_payload = None if args.no_lifecycle else load_lifecycle_payload(input_path, args.lifecycle_days)
    if lifecycle_payload:
        from theme_lifecycle import HOOK_NAME, LIFECYCLE_JS_BODY

        builder.add_chart_hook(ChartHook(name=HOOK_NAME, payload=lifecycle_payload, js=LIFECYCLE_JS_BODY))

    return RenderJob(
        markdown_text=markdown_text,
        builder=builder,
        output_path=output_path,
        summary={
            "market_data": str(market_data_path),
            "evidence": str(evidence_path) if evidence_path is not None else None,
            "index_kline_records": {
                key: len((value or {}).get("records") or [])
                for key, value in (index_kline_data.get("indices") or {}).items()
            },
            "stock_kline_records": len(stock_kline_data.get("by_ts_code") or {}),
            "style_series_records": {
                item["key"]: len(item.get("records") or [])
                for item in (style_series_payload or {}).get("indices", [])
            },
            "records_available": (market_data.get("quality") or {}).get("records_available", 0),
            "theme_lifecycle_themes": len(lifecycle_payload["themes"]) if lifecycle_payload else 0,
        },
    )


if __name__ == "__main__":
    raise SystemExit(
        render_report(
            description="Render a Markdown daily market report to static HTML.",
            build_job=build_job,
            add_arguments=add_arguments,
        )
    )
