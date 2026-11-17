---
name: citation-competitor-intelligence
description: 'Discover hidden competitors through academic citation network analysis.
  Forward: given a paper/professor, trace citation threads (backward to prior art,
  forward to derivative work) to find researchers who may have commercialized similar
  technology. Reverse: given a company, map its academic footprint and trace the
  citation graph to uncover unlisted competitors. 通过学术论文引用网络发现隐性竞品。
  正向：给定论文/教授，追踪引用线索（反向至已有成果、正向至衍生研究）找到可能已产业化的同类研究者。
  反向：给定公司，绘制其学术足迹并从引用网络挖掘未被媒体覆盖的竞品。Use when researching
  deep-tech startups, university spin-offs, professor-founded companies, or technology
  commercialization in hardware/pharma/materials/optics. Triggers: 教授创业、
  成果转化、学术竞品、论文引用竞品分析、citation competitor、university spin-off
  competitor、academic competitor discovery、论文→竞品、引用网络分析'
version: 0.1.0
agent_created: true
disable: true
---

# Citation Competitor Intelligence

## Overview

Media and patent databases cover most commercial competitors. But a significant class of
competitors — especially in deep-tech fields where university research drives
commercialization — never appears in industry news. They exist in academic citation
networks: another professor whose group published similar results six months later, or a
postdoc who built on your advisor's work and just spun out a company.

**Core insight**: Academic citation networks encode technology evolution timelines.
By tracing citation threads — backward (who did this first?) and forward (who built on
this?) — you can discover competitors that industry databases miss, often years before they
appear in commercial registries.

This skill implements a 7-step workflow for both directions:

- **Forward** (paper/professor → competitors): Given a target paper or research group,
  trace the citation graph to find other researchers working on the same technology, then
  verify whether they have commercialized (patents, companies, products).
- **Reverse** (company → unknown academic competitors): Given a company, map its
  academic footprint (key papers, inventor network), then trace the citation graph to find
  unlisted competitors who are still in academic/lab stage but approaching commercialization.

## When to Use

Trigger when any of the following applies:

- Researching a university spin-off or professor-founded company — need to find who else
  in academia is working on the same technology
- Evaluating a deep-tech startup — want to check for stealth competitors still in labs
- Analyzing a technology domain where the key players are academic groups, not companies
- Given a patent or paper and asked "who else is doing this?"
- Keyword triggers (bilingual): 教授创业, 成果转化, 学术竞品, 论文引用竞品, citation
  competitor, university spin-off competitor, academic startup competitor,
  论文→竞品, 引用网络分析, 学术成果产业化

## Step 0: Applicability Pre-check

| Domain | Applicability | Rationale |
|--------|---------------|-----------|
| Optics / photonics / semiconductors / materials / pharma / biotech | **Strong** | Heavy academic→commercial pipeline; papers predate products by 3-8 years |
| AI / ML / software | **Medium** | Fast-moving; preprints and code repos often better signals than formal papers |
| Consumer internet / business model innovation | **Weak** | Academic footprint is minimal or irrelevant |
| Traditional manufacturing / commodities | **Not applicable** | Technology differentiation comes from scale/cost, not research |

## Direction Selection

| Direction | Starting point | Goal | Example trigger |
|-----------|---------------|------|-----------------|
| **Forward** | Paper P or Professor X | Find other researchers commercializing similar technology | "陈开鑫的模斑转换器还有谁在做？" |
| **Reverse** | Company C | Find academic groups competing with C's core tech | "薄方团队的公司竞品有哪些还在实验室阶段？" |

## Workflow Overview (7 steps)

1. **Anchor identification**: Identify the core paper(s) and researcher(s). Map authorship network.
2. **Backward citation mining**: Trace references and literature review to find prior art and earlier researchers in the same lineage.
3. **Forward citation mining**: Trace who cited the anchor paper — who built on this work?
4. **Similarity filtering**: Filter forward/backward results for genuine technology overlap (not tangential citations).
5. **Performance/timeline benchmarking**: Compare key metrics across discovered groups. Who was first? Who performs best? Who is improving fastest?
6. **Author-to-company mapping**: For each identified researcher/group, check patents, company registrations, funding rounds, product announcements.
7. **Competitor matrix output**: Position each competitor on technology maturity × commercialization progress axes.

Detailed operations in `references/workflow.md`.

## Input/Output Contract

**Input**:
- **Forward**: Target paper (DOI/title) or researcher name + institution + technology domain
- **Reverse**: Company name + core technology domain
- Optional: known competitors to exclude, time range, citation depth limit

**Output**: Competitor intelligence report, including:
- Anchor summary (paper/researcher/company profile)
- Citation graph summary (N backward + M forward citations, K after similarity filter)
- Per-competitor profile: researcher → institution → papers → patents → company status → technology positioning
- Competitor positioning matrix (technology maturity vs. commercialization progress)
- Timeline visualization: who published first, who improved, who commercialized
- Risk assessment: which competitor is closest to commercialization? which has strongest IP?

## Tool Integration

| Phase | Tools | Purpose |
|-------|-------|---------|
| Citation search | WebSearch (Google Scholar, Semantic Scholar, Web of Science) | Backward/forward citation mining |
| Paper analysis | WebSearch, arXiv API, CNKI | Read abstracts, compare methods/metrics |
| Patent search | PatSnap patsnap-search connector, tushare patent API | Check if researchers hold related patents |
| Company search | Tianyancha tyc-mcp, Qichacha qcc-company, WebSearch | Check company registrations, funding, legal entities |
| Deep-tech verification | WebSearch, industry reports, conference proceedings | Cross-validate commercialization claims |

## Key Principles

- **Citations encode competition timelines**: A paper citing your anchor paper means the author is aware of and building on this work — the most direct form of competition
- **Not all citations are competitors**: Many citations are tangential (background, methodology). Similarity filtering is mandatory.
- **The gap between paper and patent is the commercialization window**: A group with papers but no patents may still be pre-commercial. A group with both papers and patents is closer to market.
- **Reverse direction reveals stealth competitors**: Companies without media coverage but WITH academic papers and patent families are the highest-risk discoveries
- **Interoperability**: Optional bridge to `patent-gap-supply-chain` skill for deeper supply-chain analysis of discovered companies

## Resources

- `references/workflow.md` — Detailed 7-step operations, directional variations
- `references/checklists.md` — Similarity filtering checklist, commercialization indicators, confidence scoring
- `examples/real-case-spot-size-converter.md` — Real case: 陈开鑫 vs 薄方, stepped vs wedge SSC
