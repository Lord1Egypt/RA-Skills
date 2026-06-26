---
name: deep-research
description: 26-tool autonomous research agent — academic papers, arXiv, PubMed, PubChem, Census, web search, and more via x402 micropayments.
version: 1.0.0
homepage: https://github.com/plagtech/deep-research-agent
metadata:
  openclaw:
    primaryEnv: RESEARCH_API_KEY
    envVars:
      - name: RESEARCH_API_KEY
        required: true
        description: API key or x402 subscription key for the research gateway.
      - name: RESEARCH_GATEWAY_URL
        required: false
        description: Gateway URL. Defaults to https://gateway.spraay.app
    requires:
      bins:
        - curl
        - python3
---

# Deep Research

Autonomous multi-domain research agent with 26 specialized endpoints spanning academic papers, preprints, biomedical literature, chemistry, demographics, and live web search. Each call is a real x402 micropayment ($0.001–$0.03 USDC).

## How to call endpoints

Use the helper script for all gateway calls:

```bash
bash {baseDir}/scripts/research.sh METHOD ENDPOINT 'JSON_BODY'
```

GET endpoints pass JSON as query params. POST endpoints send JSON body.

## Research workflow

When the user asks you to research a topic, follow this strategy:

1. **Start broad** — use `web_search` or `web_qna` to get an overview of the topic.
2. **Go deep** — based on initial results, call domain-specific tools (papers, preprints, biomedical, chemistry, demographics) for authoritative sources.
3. **Extract details** — use `web_extract` to pull full content from promising URLs found in step 1.
4. **Cross-reference** — search the same topic across multiple databases (OpenAlex + Crossref + arXiv) for comprehensive coverage.
5. **Trace citations** — use `papers_citations` or `scholarly_citations_count` to find influential related work.
6. **Synthesize** — combine all findings into a structured, sourced answer.

Be cost-aware. Each call costs real micropayments. Don't make redundant calls, but don't skimp when thoroughness matters.

Always cite sources with DOIs, URLs, PMIDs, or arXiv IDs when available.

## Available endpoints (26 tools)

### Search & RAG

**Web Search** — $0.02
Search the live web via Tavily. Returns ranked URLs with snippets.
```bash
bash {baseDir}/scripts/research.sh POST /api/v1/search/web '{"query":"ethereum restaking 2026"}'
```

**Web Extract** — $0.02
Extract clean readable content from one or more URLs.
```bash
bash {baseDir}/scripts/research.sh POST /api/v1/search/extract '{"urls":["https://example.com/article"]}'
```

**Web Q&A** — $0.03
Question-answering over fresh web results. RAG out of the box.
```bash
bash {baseDir}/scripts/research.sh POST /api/v1/search/qna '{"query":"What is the current state of restaking?"}'
```

### Dictionary

**Define** — $0.001
Dictionary definition with phonetics and examples.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/dictionary/define '{"word":"cryptography"}'
```

**Synonyms** — $0.001
Synonyms and antonyms for a word.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/dictionary/synonyms '{"word":"decentralized"}'
```

**Phonetics** — $0.001
Phonetic transcription and audio URL.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/dictionary/phonetics '{"word":"ethereum"}'
```

### Academic Papers (OpenAlex — 250M+ papers)

**Papers Search** — $0.002
Search academic papers. Returns titles, abstracts, authors, DOIs.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/papers/search '{"query":"zero knowledge proofs scalability"}'
```

**Papers by DOI** — $0.001
Paper metadata by DOI.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/papers/by-doi '{"doi":"10.1038/s41586-021-03819-2"}'
```

**Papers by Author** — $0.002
Papers by author name or ORCID.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/papers/by-author '{"author":"Vitalik Buterin"}'
```

**Papers Citations** — $0.002
Citation graph — cited-by count and references.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/papers/citations '{"doi":"10.1038/s41586-021-03819-2"}'
```

**Papers Trending** — $0.002
Trending papers by topic in the last N days.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/papers/trending '{"topic":"large language models","days":7}'
```

### Preprints (arXiv)

**Preprints Search** — $0.002
Search arXiv preprints by keyword and category.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/preprints/search '{"query":"transformer architectures","category":"cs.AI"}'
```

**Preprints by ID** — $0.001
arXiv preprint metadata by ID.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/preprints/by-id '{"id":"2301.07041"}'
```

**Preprints Recent** — $0.002
Latest arXiv preprints by category.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/preprints/recent '{"category":"cs.CR"}'
```

### Scholarly Works (Crossref — 150M+ works)

**Scholarly Search** — $0.002
Search books, papers, datasets, conference proceedings, and more.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/scholarly/search '{"query":"decentralized finance protocols"}'
```

**Scholarly by DOI** — $0.001
Full Crossref metadata for any DOI.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/scholarly/by-doi '{"doi":"10.1145/3292500.3330647"}'
```

**Scholarly Citations Count** — $0.001
Citation count and reference list for a DOI.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/scholarly/citations-count '{"doi":"10.1145/3292500.3330647"}'
```

**Scholarly Journal Info** — $0.001
Journal metadata by ISSN.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/scholarly/journal-info '{"issn":"0028-0836"}'
```

### Chemistry (PubChem)

**Compound Lookup** — $0.002
PubChem compound by name, formula, or CID.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/chemistry/compound '{"query":"aspirin"}'
```

**Similarity Search** — $0.002
Find structurally similar compounds.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/chemistry/similarity '{"cid":"2244"}'
```

**Bioactivity** — $0.002
Biological assay results for a compound.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/chemistry/bioactivity '{"cid":"2244"}'
```

### Biomedical (PubMed — 36M+ papers)

**Biomedical Search** — $0.002
Search biomedical literature across PubMed.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/biomedical/search '{"query":"CRISPR gene therapy clinical trials"}'
```

**By PubMed ID** — $0.001
Paper metadata by PMID.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/biomedical/by-pmid '{"pmid":"33116299"}'
```

**Related Articles** — $0.002
Related articles for a PubMed ID.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/biomedical/related '{"pmid":"33116299"}'
```

### Demographics

**US Census** — $0.001
US Census data by state, county, or zip code.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/demographics/census '{"location":"California"}'
```

**Data.gov Datasets** — $0.001
Search open government datasets by keyword.
```bash
bash {baseDir}/scripts/research.sh GET /api/v1/research/demographics/datasets '{"query":"renewable energy production"}'
```

## Research modes

Adapt your strategy based on what the user needs:

**Quick** — 1-3 calls. Use `web_qna` for a fast answer, or one domain-specific search if the topic is clearly academic/biomedical/chemical.

**Deep** — 5-15 calls. Search multiple databases, cross-reference findings, trace citation graphs, extract full articles. Produce a comprehensive report with sections and citations.

**Fact-check** — 3-7 calls. Start with `web_search` to find the claim in context, then cross-reference with academic sources. Deliver a clear verdict with evidence.

**Compare** — 4-10 calls. Research each topic independently across the same databases, then structure findings side-by-side.

## Data sources

Data sourced from OpenAlex, Crossref, PubMed, PubChem, arXiv, US Census Bureau, Data.gov, and Tavily.
