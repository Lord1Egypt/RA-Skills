---
title: "Source-pool connectors — copy-paste recipes"
purpose: "Optional reference. Read this only when wiring up research pools beyond your runtime's built-in web search."
tags: [reference, connectors, retrieval]
---

# Connectors — wiring the research pools

> **You do not need any of this to run `/deepen`.** A web search + fetch tool alone is a valid run.
> This file exists so that, when you *can* reach more pools, you draw from **non-overlapping indexes** —
> which is the only thing that makes parallel research widen recall instead of resurfacing the same pages.
> All recipes below are public APIs. Keyless pools need nothing; keyed pools are clearly marked.

**How to use this file:** examples are shown as `curl` for portability. If your runtime has no shell, issue
the same request with your fetch/HTTP tool — same URL, method, headers, and body. Always send a descriptive
`User-Agent` (some endpoints rate-limit or block blank ones). Respect rate limits; back off on HTTP 429.

---

## Keyless pools (no signup, work immediately)

### Academic — primary literature for the canon/empirical layer

**arXiv** (CS, physics, math, quant-bio; Atom XML):
```bash
curl -sG "http://export.arxiv.org/api/query" \
  --data-urlencode "search_query=all:deliberate practice expertise" \
  --data-urlencode "start=0" --data-urlencode "max_results=10"
```

**Semantic Scholar** (all fields; JSON; abstracts + citation counts — great for track-record signal):
```bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=deliberate+practice+meta-analysis&limit=10&fields=title,abstract,year,authors,citationCount,url,openAccessPdf"
```
Keyless is rate-limited (~100 req / 5 min). A free API key (`x-api-key` header) raises it; not required.

**PubMed / NCBI E-utilities** (biomedical; two-step search → fetch):
```bash
# 1) search → PMIDs
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=10&term=sleep+apnea+CPAP+adherence"
# 2) summaries for those PMIDs
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=PMID1,PMID2,PMID3"
```
Add `&api_key=<key>` to go from 3 to 10 req/s (optional). Always include `&email=<you>` as etiquette.

**Crossref** (DOIs, metadata across publishers) and **OpenAlex** (open citation graph) — two more distinct indexes:
```bash
curl -s "https://api.crossref.org/works?query=spaced+repetition+retention&rows=10&mailto=you@example.com"
curl -s "https://api.openalex.org/works?search=spaced%20repetition%20retention&per-page=10&mailto=you@example.com"
```

### Forums — practitioner ground truth + failure-mode signal

**Reddit** (JSON endpoints; send a real User-Agent or you'll be 429'd):
```bash
curl -s -A "deepen-skill/1.0 (research)" \
  "https://www.reddit.com/r/Entrepreneur/search.json?q=PPC+wasted+spend&restrict_sr=1&sort=relevance&t=year&limit=25"
```

**Hacker News** (Algolia search API; keyless, generous limits):
```bash
curl -s "https://hn.algolia.com/api/v1/search?query=rag+retrieval&tags=story"          # by relevance
curl -s "https://hn.algolia.com/api/v1/search_by_date?query=rag+retrieval&tags=story"   # newest first
```

### Code hosts — for technical domains

**GitHub** (search repos/code/issues; READMEs as raw text). Unauthenticated search works at low rate; a token
(`Authorization: Bearer <token>`) raises limits and is required for code search:
```bash
curl -s "https://api.github.com/search/repositories?q=agent+skill+expertise&sort=stars&per_page=10"
curl -s "https://raw.githubusercontent.com/<owner>/<repo>/HEAD/README.md"
```
If the `gh` CLI is installed, `gh search repos`, `gh api`, and `gh repo view` are simpler.

### Video & podcasts — the modality plain text-search misses

**yt-dlp** pulls captions/auto-subtitles without downloading the video (then read the `.vtt`/`.srt`):
```bash
yt-dlp --skip-download --write-subs --write-auto-subs --sub-lang en --convert-subs srt -o "%(id)s.%(ext)s" "<video-url>"
yt-dlp --dump-json "<video-url>" | jq '{title, upload_date, channel, duration}'   # metadata only
```
For caption-less audio, fall back to a local speech-to-text tool (e.g. Whisper). Store the **digest + link**, never the raw transcript (see the corpus fidelity rule in `SKILL.md`).

---

## Keyed pools (free tiers exist; each is a *different* semantic index → real recall diversity)

Set the key as an environment variable and reference it; **never hardcode a key into a note or commit it.**

**Exa** (neural/embedding search; returns text content inline):
```bash
curl -s -X POST "https://api.exa.ai/search" \
  -H "x-api-key: $EXA_API_KEY" -H "Content-Type: application/json" \
  -d '{"query":"operator alpha in Amazon PPC bid management","numResults":10,"contents":{"text":true}}'
```

**Tavily** (LLM-tuned search; key in body or as a Bearer token):
```bash
curl -s -X POST "https://api.tavily.com/search" -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$TAVILY_API_KEY\",\"query\":\"sleep apnea AHI thresholds\",\"search_depth\":\"advanced\",\"max_results\":10}"
```

**Brave Search** (independent web index; key in a header):
```bash
curl -s "https://api.search.brave.com/res/v1/web/search?q=paddle+core+physics+pickleball" \
  -H "X-Subscription-Token: $BRAVE_API_KEY" -H "Accept: application/json"
```

> **Security note (matches the SKILL's stance):** call these REST APIs **directly**. Do not install
> unvetted third-party "MCP servers" / plugins just to reach a search index — that runs someone else's
> code at full privilege for a request you can make in one line.

---

## Picking pools per topic

- **Academic / health / science topic** → arXiv + Semantic Scholar + PubMed + OpenAlex carry the load; web search is secondary.
- **Marketing / ops / business topic** → web + Reddit + HN + a keyed semantic index (operator alpha lives in forums and long-form posts, not papers).
- **Technical / dev topic** → GitHub + HN + arXiv + docs via web fetch.
- **Anything with talks/podcasts** (most domains) → add yt-dlp for the spoken-word layer.

The rule from `SKILL.md`: **spread workers across non-overlapping pools.** Ten workers on one index just
resurface the same pages; four workers on four different indexes is where parallel research actually pays off.
