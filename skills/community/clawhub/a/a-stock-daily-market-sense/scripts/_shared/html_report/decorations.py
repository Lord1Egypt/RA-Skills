"""Data-driven UI decorations.

A *decoration* is a small JS snippet the builder runs after rendering the
report body, to upgrade plain DOM into richer UI. Patterns that recur
mechanism-identically across skills live here as parameterised classes
instead of hand-written JS in each skill:

- ``PillDecoration``  — colour table cells whose text matches a rule into pills.
- ``HeroDecoration``  — promote a summary heading + its following blocks into a
  hero ``<aside class="summary-card">``.
- ``CollapsibleUpdatesDecoration`` — wrap ``## 更新 YYYY-MM-DD：摘要`` sections
  into collapsible dated cards (newest expanded), for living reports that are
  updated in place over time.
- ``TimelineDecoration`` — merge the minimal top version table (日期|版本号)
  with the rich bottom changelog table (版本变更记录) into one clickable
  version timeline strip with per-version popovers and jump links into the
  matching update card.

Each exposes ``.js`` (a complete ``(function(){...})();`` block); decorations
that need styling also expose ``.css``, which ``builder.add_decoration``
merges into the page. For anything these can't express, the raw escape hatch
``builder.add_ui_decoration(js_string)`` still works.

Ordering note: add ``CollapsibleUpdatesDecoration`` *before* ``HeroDecoration``
(the hero walk stops at section/aside/blockquote nodes, so update cards built
first are never swallowed), and ``TimelineDecoration`` after both (it links to
the cards and offers the expand-all toggle).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Optional, Sequence, Tuple


@dataclass
class PillDecoration:
    """Colour table cells into pills by regex.

    ``rules`` is a list of ``(pattern, css_class)``; the first pattern that
    fully matches a cell's trimmed text wins. Patterns are JS regex source
    (e.g. ``r"^(成长股|成熟龙头)$"``). Cells that already contain child
    elements are skipped, matching the original per-skill behaviour.
    """

    rules: Sequence[Tuple[str, str]]

    @property
    def js(self) -> str:
        rules_js = ",\n    ".join(
            f"{{ re: new RegExp({json.dumps(pat, ensure_ascii=False)}), cls: {json.dumps(cls)} }}"
            for pat, cls in self.rules
        )
        return (
            "(function () {\n"
            '  const root = document.getElementById("report-body");\n'
            "  if (!root) return;\n"
            "  const pillRules = [\n"
            f"    {rules_js}\n"
            "  ];\n"
            '  root.querySelectorAll("td").forEach(td => {\n'
            "    const trimmed = td.textContent.trim();\n"
            "    if (!trimmed || td.children.length > 0) return;\n"
            "    for (const rule of pillRules) {\n"
            "      if (rule.re.test(trimmed)) {\n"
            '        td.innerHTML = `<span class="${rule.cls}">${trimmed}</span>`;\n'
            "        return;\n"
            "      }\n"
            "    }\n"
            "  });\n"
            "})();"
        )


_HERO_TEMPLATE = r"""(function () {
  const root = document.getElementById("report-body");
  if (!root) return;
  const summaryH = Array.from(root.querySelectorAll("h2, h3")).find(
    h => h.textContent.trim().startsWith(__PREFIX__));
  if (!summaryH) return;

  const card = document.createElement("aside");
  card.className = "summary-card";
  const label = document.createElement("div");
  label.className = "summary-label";
  label.textContent = summaryH.textContent.trim();
  card.appendChild(label);

  const collectTags = __COLLECT__;
  const maxBlocks = __MAX__;
  const stopLevel = __STOPLEVEL__;
  const collected = [];
  let cur = summaryH.nextElementSibling;
  while (cur) {
    /* stop at sectioning/callout content (update cards, finding cards, quotes):
       the summary card must never swallow or delete those blocks */
    if (/^(SECTION|ASIDE|BLOCKQUOTE)$/.test(cur.tagName)) break;
    const headingMatch = /^H([1-6])$/.exec(cur.tagName);
    if (headingMatch && Number(headingMatch[1]) <= stopLevel) break;
    const next = cur.nextElementSibling;
    const txt = cur.textContent.trim();
__NUMBERED_BLOCK__
    if (maxBlocks != null && collected.length >= maxBlocks) break;
    if (collectTags.includes(cur.tagName) && txt && !/^-{3,}$/.test(txt)) {
      cur.classList.add("summary-body");
      collected.push(cur);
    } else {
      cur.remove();
    }
    cur = next;
  }
  collected.forEach(node => card.appendChild(node));
  summaryH.replaceWith(card);

  collected.forEach(p => {
    let h = p.innerHTML.replace(/([+\-])(\d+(?:\.\d+)?)(__UNITS__)/g,
      (_, sign, num, unit) => `<span class="${sign === "+" ? "num-pos" : "num-neg"}">${sign}${num}${unit}</span>`);
__KEYWORD_BLOCK__
    p.innerHTML = h;
  });
})();"""


@dataclass
class HeroDecoration:
    """Promote a summary heading into a hero ``<aside class="summary-card">``.

    Finds the first h2/h3 whose text starts with ``heading_prefix``, pulls the
    following blocks (limited to ``collect_tags``) into a card up to the next
    heading, drops separators/other nodes, and highlights signed numbers.

    Parameters reproduce the per-skill variants:
    - ``collect_tags``      tags to keep, e.g. ``("P", "UL")`` or ``("P",)``.
    - ``max_blocks``        cap on collected blocks (``None`` = no cap).
    - ``stop_at_numbered``  stop when a numbered-list paragraph begins.
    - ``number_units``      regex alternation of units to colour after numbers.
    - ``keyword_pattern``   optional regex alternation wrapped in ``.kw`` spans.
    - ``stop_mode``         where the section ends:
        ``"section"``     — stop at a heading whose level is same-or-higher than
                            the summary heading (so a deeper subheading *inside*
                            the summary keeps collecting; the original analyzer
                            behaviour).
        ``"any_heading"`` — stop at the next heading of any level (the original
                            market-sense behaviour, and the default).
    """

    heading_prefix: str
    collect_tags: Sequence[str] = ("P", "UL")
    max_blocks: Optional[int] = None
    stop_at_numbered: bool = False
    number_units: str = "%|pct|倍|x|分位"
    keyword_pattern: Optional[str] = None
    stop_mode: str = "any_heading"

    @property
    def js(self) -> str:
        collect = "[" + ", ".join(json.dumps(t.upper()) for t in self.collect_tags) + "]"
        numbered = (
            r"    if (txt && /^[^\dA-Za-z一-鿿]*\d+\./.test(txt)) break;"
            if self.stop_at_numbered
            else ""
        )
        keyword = (
            f"    h = h.replace(/({self.keyword_pattern})/g, '<span class=\"kw\">$1</span>');"
            if self.keyword_pattern
            else ""
        )
        if self.stop_mode == "section":
            stoplevel = "Number(summaryH.tagName.slice(1))"
        elif self.stop_mode == "any_heading":
            stoplevel = "6"
        else:
            raise ValueError(f"unknown stop_mode {self.stop_mode!r}; use 'section' or 'any_heading'")
        return (
            _HERO_TEMPLATE.replace("__PREFIX__", json.dumps(self.heading_prefix, ensure_ascii=False))
            .replace("__COLLECT__", collect)
            .replace("__MAX__", "null" if self.max_blocks is None else str(int(self.max_blocks)))
            .replace("__STOPLEVEL__", stoplevel)
            .replace("__NUMBERED_BLOCK__", numbered)
            .replace("__UNITS__", self.number_units)
            .replace("__KEYWORD_BLOCK__", keyword)
        )


_UPDATES_TEMPLATE = r"""(function () {
  const root = document.getElementById("report-body");
  if (!root) return;
  const re = new RegExp(__PATTERN__);
  const esc = s => String(s == null ? "" : s).replace(/[&<>"]/g,
    c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const hits = Array.from(root.querySelectorAll("h2, h3"))
    .map(h => ({ h, m: re.exec(h.textContent.trim()) }))
    .filter(x => x.m);
  if (!hits.length) return;

  hits.forEach(({ h, m }) => {
    const level = Number(h.tagName.slice(1));
    const date = m[1];
    const summary = (m[2] || "").trim();
    const card = document.createElement("section");
    card.className = "upd-card";
    if (!document.getElementById("upd-" + date)) card.id = "upd-" + date;
    card.dataset.date = date;
    const head = document.createElement("button");
    head.type = "button";
    head.className = "upd-head";
    head.setAttribute("aria-expanded", "false");
    head.innerHTML = '<span class="upd-chevron">▸</span><span class="upd-date">' + esc(date) +
      '</span><span class="upd-sum">' + esc(summary || "更新") + "</span>";
    const body = document.createElement("div");
    body.className = "upd-body";
    h.before(card);
    const toMove = [h];
    let cur = h.nextElementSibling;
    while (cur) {
      const hm = /^H([1-6])$/.exec(cur.tagName);
      if (hm && Number(hm[1]) <= level) break;
      if (cur.classList && cur.classList.contains("upd-card")) break;
      toMove.push(cur);
      cur = cur.nextElementSibling;
    }
    card.appendChild(head);
    card.appendChild(body);
    toMove.forEach(n => body.appendChild(n));
    h.classList.add("upd-src-heading");
    head.addEventListener("click", () => {
      const open = card.classList.toggle("open");
      head.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });

  Array.from(root.querySelectorAll(".upd-card"))
    .sort((a, b) => (a.dataset.date < b.dataset.date ? 1 : -1))
    .slice(0, __OPEN__)
    .forEach(c => {
      c.classList.add("open");
      const head = c.querySelector(".upd-head");
      if (head) head.setAttribute("aria-expanded", "true");
    });
})();"""

_UPDATES_CSS = """
.upd-card { margin: 14px 0; border: 1px solid var(--line-2, #e8eaed); border-left: 3px solid var(--accent, #1a73e8); border-radius: var(--r-md, 12px); background: var(--surface, #fff); overflow: hidden; }
.upd-head { display: flex; align-items: baseline; gap: 9px; width: 100%; border: none; background: var(--surface-2, #f8f9fa); padding: 9px 14px; margin: 0; cursor: pointer; font: inherit; text-align: left; }
.upd-head:hover { background: var(--accent-soft, #e8f0fe); }
.upd-chevron { color: var(--ink-4, #9aa0a6); font-size: 11px; transition: transform .15s ease; }
.upd-card.open .upd-chevron { transform: rotate(90deg); }
.upd-date { font-family: var(--font-mono, ui-monospace, monospace); font-size: 12px; font-weight: 600; color: var(--accent-ink, #0b57d0); white-space: nowrap; }
.upd-sum { font-size: 13.5px; font-weight: 600; color: var(--ink-1, #202124); line-height: 1.5; }
.upd-body { display: none; padding: 4px 18px 14px; }
.upd-card.open .upd-body { display: block; }
.upd-src-heading { display: none; }
@media print { .upd-body { display: block !important; } .upd-chevron { display: none; } }
"""


@dataclass
class CollapsibleUpdatesDecoration:
    """Wrap dated update sections into collapsible cards.

    Finds every h2/h3 matching ``heading_pattern`` (group 1 = ISO date,
    group 2 = one-line summary), moves the heading plus its section content
    into a ``<section class="upd-card" id="upd-<date>">`` with a click-to-
    expand header (date badge + summary), and expands the ``open_latest``
    newest cards by date. Reports without matching headings are untouched.
    """

    heading_pattern: str = r"^更新\s*(\d{4}-\d{2}-\d{2})\s*[：:]?\s*(.*)$"
    open_latest: int = 1

    @property
    def js(self) -> str:
        return _UPDATES_TEMPLATE.replace(
            "__PATTERN__", json.dumps(self.heading_pattern, ensure_ascii=False)
        ).replace("__OPEN__", str(int(self.open_latest)))

    @property
    def css(self) -> str:
        return _UPDATES_CSS


_TIMELINE_TEMPLATE = r"""(function () {
  const root = document.getElementById("report-body");
  if (!root) return;
  const CHANGELOG_HEADING = __CLH__;
  const norm = s => String(s == null ? "" : s).trim();
  const esc = s => String(s == null ? "" : s).replace(/[&<>"]/g,
    c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const isDate = s => /^\d{4}-\d{2}-\d{2}$/.test(s);

  /* top minimal version table: exactly two columns 日期 / 版本… */
  let topWrap = null, topRows = [];
  for (const wrap of root.querySelectorAll(".table-wrap")) {
    const ths = Array.from(wrap.querySelectorAll("thead th")).map(th => norm(th.textContent));
    if (ths.length === 2 && ths[0] === "日期" && ths[1].indexOf("版本") === 0) {
      topWrap = wrap;
      topRows = Array.from(wrap.querySelectorAll("tbody tr")).map(tr => ({
        date: norm(tr.cells[0] && tr.cells[0].textContent),
        ver: norm(tr.cells[1] && tr.cells[1].textContent)
      }));
      break;
    }
  }

  /* rich changelog table under the 版本变更记录 heading */
  let clRows = [];
  const clHead = Array.from(root.querySelectorAll("h2,h3,h4"))
    .find(h => h.textContent.includes(CHANGELOG_HEADING));
  if (clHead) {
    let cur = clHead.nextElementSibling;
    while (cur && !/^H[1-6]$/.test(cur.tagName) &&
           !(cur.classList && cur.classList.contains("table-wrap"))) {
      cur = cur.nextElementSibling;
    }
    if (cur && cur.classList && cur.classList.contains("table-wrap")) {
      const ths = Array.from(cur.querySelectorAll("thead th")).map(th => norm(th.textContent));
      const di = ths.findIndex(t => t.includes("日期"));
      const vi = ths.findIndex(t => t.includes("版本"));
      const ci = ths.findIndex(t => t.includes("变更"));
      const ni = ths.findIndex(t => t.includes("数字"));
      if (di >= 0 && vi >= 0) {
        clRows = Array.from(cur.querySelectorAll("tbody tr")).map(tr => ({
          date: norm(tr.cells[di] && tr.cells[di].textContent),
          ver: norm(tr.cells[vi] && tr.cells[vi].textContent),
          changes: ci >= 0 && tr.cells[ci] ? norm(tr.cells[ci].textContent) : "",
          numbers: ni >= 0 && tr.cells[ni] ? norm(tr.cells[ni].textContent) : ""
        }));
      }
    }
  }

  /* merge by date; changelog detail wins over the minimal table */
  const byDate = new Map();
  topRows.forEach(r => {
    if (isDate(r.date)) byDate.set(r.date, { date: r.date, ver: r.ver, changes: "", numbers: "" });
  });
  clRows.forEach(r => {
    if (!isDate(r.date)) return;
    const prev = byDate.get(r.date) || { date: r.date, ver: "", changes: "", numbers: "" };
    byDate.set(r.date, {
      date: r.date,
      ver: r.ver || prev.ver,
      changes: r.changes || prev.changes,
      numbers: r.numbers || prev.numbers
    });
  });
  const entries = Array.from(byDate.values()).sort((a, b) => (a.date < b.date ? -1 : 1));
  if (entries.length < 2) return;

  let openPop = null;
  function closePop() {
    if (!openPop) return;
    openPop.remove(); openPop = null;
    document.removeEventListener("click", onOutside, true);
    document.removeEventListener("keydown", onKey, true);
  }
  function onOutside(e) { if (openPop && !openPop.contains(e.target)) closePop(); }
  function onKey(e) { if (e.key === "Escape") closePop(); }
  function popRow(label, text) {
    const p = document.createElement("p");
    p.className = "vtl-pop-row";
    const l = document.createElement("span");
    l.className = "vtl-pop-label";
    l.textContent = label;
    p.appendChild(l);
    p.appendChild(document.createTextNode(text));
    return p;
  }
  function openPopover(entry, anchorEl) {
    closePop();
    const pop = document.createElement("div");
    pop.className = "vtl-pop";
    const h = document.createElement("div");
    h.className = "vtl-pop-head";
    h.textContent = (entry.ver ? entry.ver + " · " : "") + entry.date;
    pop.appendChild(h);
    if (entry.changes) pop.appendChild(popRow("主要变更", entry.changes));
    if (entry.numbers) pop.appendChild(popRow("关键数字", entry.numbers));
    const upd = document.getElementById("upd-" + entry.date);
    if (upd) {
      const jump = document.createElement("button");
      jump.type = "button";
      jump.className = "vtl-pop-jump";
      jump.textContent = "查看当次更新 ↓";
      jump.addEventListener("click", () => {
        upd.classList.add("open");
        const head = upd.querySelector(".upd-head");
        if (head) head.setAttribute("aria-expanded", "true");
        closePop();
        upd.scrollIntoView({ behavior: "smooth", block: "start" });
      });
      pop.appendChild(jump);
    } else if (!entry.changes && !entry.numbers) {
      pop.appendChild(popRow("说明", "该版本无变更明细（首版或未登记）"));
    }
    document.body.appendChild(pop);
    const r = anchorEl.getBoundingClientRect();
    let left = window.scrollX + r.left;
    const maxLeft = window.scrollX + document.documentElement.clientWidth - pop.offsetWidth - 12;
    if (left > maxLeft) left = Math.max(window.scrollX + 8, maxLeft);
    pop.style.top = (window.scrollY + r.bottom + 6) + "px";
    pop.style.left = left + "px";
    openPop = pop;
    setTimeout(() => {
      document.addEventListener("click", onOutside, true);
      document.addEventListener("keydown", onKey, true);
    }, 0);
  }

  const strip = document.createElement("div");
  strip.className = "vtl";
  const track = document.createElement("div");
  track.className = "vtl-track";
  entries.forEach((e, i) => {
    const node = document.createElement("button");
    node.type = "button";
    node.className = "vtl-node" + (i === entries.length - 1 ? " hot" : "");
    node.innerHTML = '<span class="vtl-dot"></span><span class="vtl-ver">' + esc(e.ver || "—") +
      '</span><span class="vtl-date">' + esc(e.date) + "</span>";
    node.addEventListener("click", ev => { ev.stopPropagation(); openPopover(e, node); });
    track.appendChild(node);
  });
  strip.appendChild(track);

  const cards = Array.from(root.querySelectorAll(".upd-card"));
  if (cards.length) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "vtl-expand";
    const sync = () => {
      const open = root.querySelectorAll(".upd-card.open").length;
      btn.textContent = open === cards.length ? "收起全部更新" : "展开全部更新";
    };
    btn.addEventListener("click", () => {
      const allOpen = root.querySelectorAll(".upd-card.open").length === cards.length;
      cards.forEach(c => {
        c.classList.toggle("open", !allOpen);
        const head = c.querySelector(".upd-head");
        if (head) head.setAttribute("aria-expanded", allOpen ? "false" : "true");
      });
      sync();
    });
    root.addEventListener("click", () => setTimeout(sync, 0));
    sync();
    strip.appendChild(btn);
  }

  if (topWrap) {
    topWrap.after(strip);
    topWrap.style.display = "none";
    topWrap.setAttribute("aria-hidden", "true");
  } else {
    const h = root.querySelector("h1, h2");
    if (h) h.after(strip); else root.prepend(strip);
  }
})();"""

_TIMELINE_CSS = """
.vtl { grid-column: 1 / -1; display: flex; align-items: flex-start; gap: 14px; flex-wrap: wrap; margin: 14px 0 20px; }
.vtl-track { display: flex; align-items: stretch; flex-wrap: wrap; }
.vtl-node { position: relative; display: flex; flex-direction: column; align-items: flex-start; gap: 1px; border: none; background: none; cursor: pointer; padding: 2px 28px 2px 0; margin: 0; font: inherit; text-align: left; }
.vtl-node:not(:last-child)::after { content: ""; position: absolute; top: 7px; left: 15px; right: 5px; height: 2px; background: var(--line-2, #e8eaed); }
.vtl-dot { position: relative; z-index: 1; width: 12px; height: 12px; border-radius: 50%; background: var(--surface, #fff); border: 3px solid var(--accent, #1a73e8); box-sizing: border-box; }
.vtl-node.hot .vtl-dot { background: var(--accent, #1a73e8); box-shadow: 0 0 0 3px var(--accent-soft, #e8f0fe); }
.vtl-ver { font-size: 12px; font-weight: 600; color: var(--ink-1, #202124); margin-top: 4px; }
.vtl-node.hot .vtl-ver, .vtl-node:hover .vtl-ver { color: var(--accent-ink, #0b57d0); }
.vtl-date { font-family: var(--font-mono, ui-monospace, monospace); font-size: 10.5px; color: var(--ink-4, #9aa0a6); }
.vtl-expand { align-self: center; border: 1px solid var(--line-1, #dadce0); background: var(--surface, #fff); color: var(--ink-3, #5f6368); font-size: 12px; border-radius: var(--pill, 999px); padding: 3px 12px; cursor: pointer; }
.vtl-expand:hover { border-color: var(--accent, #1a73e8); color: var(--accent-ink, #0b57d0); }
.vtl-pop { position: absolute; z-index: 999; max-width: 380px; background: var(--surface, #fff); border: 1px solid var(--line-1, #dadce0); border-radius: var(--r-md, 12px); box-shadow: var(--shadow-2, 0 6px 20px rgba(0,0,0,0.16)); padding: 11px 13px; }
.vtl-pop-head { font-size: 12.5px; font-weight: 700; color: var(--ink-1, #202124); margin-bottom: 7px; padding-bottom: 6px; border-bottom: 1px solid var(--line-2, #e8eaed); }
.vtl-pop-row { margin: 0 0 6px; font-size: 12.5px; line-height: 1.65; color: var(--ink-2, #3c4043); }
.vtl-pop-label { display: inline-block; margin-right: 6px; font-size: 11px; font-weight: 600; color: var(--accent-ink, #0b57d0); background: var(--accent-soft, #e8f0fe); border-radius: var(--pill, 999px); padding: 0 7px; }
.vtl-pop-jump { margin-top: 2px; border: none; background: none; color: var(--accent-ink, #0b57d0); font-size: 12px; font-weight: 600; cursor: pointer; padding: 0; }
@media print { .vtl-expand { display: none; } }
"""


@dataclass
class TimelineDecoration:
    """Upgrade the report's version tables into a clickable timeline strip.

    Reads two conventions the living-report template mandates: the minimal
    two-column ``日期|版本号`` table under the title, and the rich
    ``版本变更记录`` table (日期/版本/主要变更/关键数字变化) at the end.
    Entries are merged by date; each node opens a popover with that version's
    changes and — when a matching ``upd-<date>`` update card exists — a jump
    link that expands and scrolls to it. The minimal top table is hidden once
    the strip is mounted; with fewer than two versions nothing changes.
    """

    changelog_heading: str = "版本变更记录"

    @property
    def js(self) -> str:
        return _TIMELINE_TEMPLATE.replace(
            "__CLH__", json.dumps(self.changelog_heading, ensure_ascii=False)
        )

    @property
    def css(self) -> str:
        return _TIMELINE_CSS
