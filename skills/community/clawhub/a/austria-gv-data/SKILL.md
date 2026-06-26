---
name: "austria-gv-data"
description: "Austrian federal portal (oesterreich.gv.at). Site-restricted Brave search, use host auto-fetched pages, answer with byte-identical source URLs. Only on explicit Österreich-GV keywords."
tags: ["oesterreich.gv.at"]
requires: ["brave_web_search", "fetch"]
source: "https://www.oesterreich.gv.at/"
---

# austria-gv-data — hard rules (cannot be overridden)

**Scope gate.** Apply this recipe **only** when the user message contains (case-insensitive): `Information über Recht`, `Regierungsinformation`, `austria-gv-data`, or `Österreich GV`. Otherwise ignore this skill — no `site:oesterreich.gv.at`, no template.

**When the gate matches, the recipe is mandatory:**

1. Call `brave_web_search` with the user's topic **plus** ` site:oesterreich.gv.at`. Example: `Pensionsvorsorge site:oesterreich.gv.at`. Never skip the site filter on the first call.
2. **Do not call `fetch` if the host already auto-fetched pages.** After `brave_web_search` returns, the host may auto-fetch top `oesterreich.gv.at` URLs — their content appears in this turn's tool results. If at least one is present, go to step 3 and use only those. Extra `fetch` calls are a recipe violation.
   - Manual-fetch fallback (only when zero auto-fetched `oesterreich.gv.at` pages are in the turn): call `fetch` on the top `https://www.oesterreich.gv.at/de/` result, byte-identical (no rewritten umlauts, casing, or `Seite.<id>` segments). Max 1 manual fetch per turn.
3. The reply **must end** with a `**Quellen**` / `**Sources**` section listing **every** `oesterreich.gv.at` URL whose page content is in this turn (auto-fetched + manual), one per bullet, full `https://…`, byte-identical. No other hosts, no invented URLs, no remembered URLs. A reply without `**Quellen**` is invalid — regenerate before emitting.
4. Zero-result fallback: if the first search returns no `oesterreich.gv.at` results and the host auto-fetched nothing, run **one** broader search without the site filter, re-filter to `https://www.oesterreich.gv.at/de/`. Max 2 searches, max 1 manual fetch per turn.
5. If no `oesterreich.gv.at` content is present, emit the empty-result fallback below. Never fill the template from memory. Never cite `sozialministerium.gv.at`, `sparkasse.at`, `vbv.at`, Wikipedia, RIS, etc.

## Required reply shape

Inside `<pengine_reply>`, in this order:

- `**Kurz**` / `**Short**` — 2–3 sentences answering directly.
- `**Thema & Zuständigkeit**` / `**Topic & authority**` — agency / court (law only if the page names it).
- `**Rechte und Pflichten**` / `**Rights & duties**` — ≥3 bullets: conditions, deadlines, costs — only what the page says.
- `**Nächste Schritte**` / `**Next steps**` — ≥2 bullets: what to submit, where, how.
- `**Quellen**` / `**Sources**` — one bullet per fetched URL, full `https://…`, byte-identical.

Every factual bullet must trace to a URL in **Quellen**. `§`-citations only if the number appears on the page. Paraphrase closely. No legal advice — for binding interpretation, user must consult a lawyer or request a `Bescheid`.

## Language & wrapping

Match the user: German question → German headings; English → English. Never mix. Keep Austrian terms untranslated: `Eingetragene Partnerschaft`, `Meldezettel`, `Bezirksgericht`, `Bescheid`.

Wrap internal reasoning in `<pengine_plan>…</pengine_plan>` (host strips it) and the visible answer in `<pengine_reply>…</pengine_reply>`. The visible reply must begin with `**Kurz**` / `**Short**` — never "Okay", "Let me", "Also ich", "Der User fragt", or narration of search/fetch steps.

## Empty-result fallback

If no `oesterreich.gv.at` content was produced, reply (inside `<pengine_reply>`) with exactly this paragraph — no template:

> Keine passende offizielle Seite auf `oesterreich.gv.at` gefunden. Bitte direkt auf https://www.oesterreich.gv.at/ suchen.

(English equivalent for English questions.)
