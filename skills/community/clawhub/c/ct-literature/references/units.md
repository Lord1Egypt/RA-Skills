# Capability Units

> Schema: Input / Output / Dependencies / AI autonomy / Composition interface
> Designed per the library convention §6. AI autonomy: ⬛ fully automatic / 🟨 semi-automatic (confirmation required) / ⬜ assistive.

---

## U1: fetch_openalex / OpenAlex fetch (primary)

- Input: `topic`, optional `review_type`, `year_from`, `year_to`, `safety` flag, `max`
- Output: OpenAlex payload `{source, query, works:[{source,id,doi,pmid,pmcid,title,authors,year,publication_date,publication,type,study_type,cited_by_count,url,open_access_url,abstract_snippet,concepts,keywords,funders,language,is_retracted,volume,issue,page,is_safety}]}`
- Depends on: none (entry)
- AI autonomy: 🟨 semi-automatic (confirm topic / review_type)
- Composition interface: → U4
- Note: public REST, no key, citation-rich; polite 0.3 s delay between pages. Abstracts stored as inverted index, reconstructed to full text.

## U2: fetch_europepmc / Europe PMC fetch (optional, MeSH precision)

- Input: same as U1
- Output: Europe PMC payload (MEDLINE/MeSH-indexed; `mesh`, `affiliations`, `journal_iso` populated)
- Depends on: none (independent enrichment)
- AI autonomy: 🟨 semi-automatic
- Composition interface: → U4
- Note: ebi.ac.uk REST, no key; adds MeSH descriptor terms + biomedical journal precision. Date filter uses `PUB_YEAR` field (not `PUBLICATION_YEAR`).

## U3: fetch_semantic_scholar / Semantic Scholar fetch (optional, citation rank)

- Input: same as U1
- Output: Semantic Scholar payload (citationCount enriched; `pmid`, `pmcid`, `open_access_url` when available)
- Depends on: none (independent enrichment)
- AI autonomy: 🟨 semi-automatic
- Composition interface: → U4
- Note: no key -> HTTP 429 common; **on 429 / any failure returns empty and is skipped** (never aborts the pipeline).

## U4: normalize / merge + dedupe

- Input: U1/U2/U3 payloads (whichever ran)
- Output: unified `works` list, de-duplicated by DOI (else normalized title); each record keeps a `sources` list for provenance; ranked by citations desc. Merges concepts/keywords across sources, takes max cited_by_count.
- Depends on: U1 (and U2/U3 when enabled)
- AI autonomy: ⬛ fully automatic
- Composition interface: → U5

## U5: report / report output

- Input: U4 merged works (+ meta: topic / review_type / year / safety)
- Output: Markdown report with:
  - Summary header (topic, filters, count, source list)
  - Top works table (with 📥 OA download links)
  - Key details cards (per-work: authors, journal/date, volume/issue/page, DOI/PubMed/PMC links, concepts, keywords, funders, full abstract)
  - Study-type distribution, yearly trend
  - Safety / CSM subset (qualitative evidence only)
- Depends on: U4
- AI autonomy: 🟨 semi-automatic (confirm output format)
- Composition interface: → `ct-pipeline` / `ct-protocol` / `ct-csr`

---

## Pipeline

```
input(topic [+ review_type + year + safety]) 
   → U1(fetch_openalex, required)
   → U2(fetch_europepmc, opt) ┐
   → U3(fetch_semantic_scholar, opt, 429→skip) ├─→ U4(normalize) → U5(report) → output
                                  └─────────────┘
   ct-registry → ct-literature (topic seed)
   ct-literature → ct-pipeline / ct-protocol / ct-csr
```

> OpenAlex is the sole REQUIRED source (U1→U4→U5 always works). U2/U3 are optional enrichments; U3 degrades gracefully. All computation local; ordinary input + public retrieval (A-tier).
