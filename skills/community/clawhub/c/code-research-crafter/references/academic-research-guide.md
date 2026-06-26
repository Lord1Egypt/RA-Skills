# Academic Research Guide

Methodology for conducting academic research in Phase 2 of the Code Research Crafter workflow.

## Search Strategy

### 1. Primary Sources

| Source | Search Query Pattern | Priority |
|--------|---------------------|----------|
| arXiv | `site:arxiv.org [topic] 2024 2025` | High |
| Google Scholar | `site:scholar.google.com [topic] survey` | High |
| ACM Digital Library | `site:dl.acm.org [topic]` | Medium |
| IEEE Xplore | `site:ieeexplore.ieee.org [topic]` | Medium |
| Semantic Scholar | `site:semanticscholar.org [topic]` | Medium |

### 2. Search Queries

Use WebSearch with these structured queries:

```
# Broad survey
"[topic] survey" OR "[topic] review" 2024 OR 2025

# Specific technique
"[algorithm name]" AND "[domain]" implementation

# Comparative study
"[topic] comparison" OR "[topic] benchmark" 2024 OR 2025

# Problem-oriented
"[problem description] solution" OR "[problem description] approach"
```

### 3. Paper Selection Criteria

Prioritize papers that score high on:

- **Recency**: 2024-2025 preferred; 2023 acceptable; older only if foundational
- **Relevance**: directly addresses the problem domain or proposes applicable techniques
- **Citations**: higher citation count indicates community validation
- **Venue**: top-tier conferences/journals (e.g., ICSE, FSE, ASE, NeurIPS, ICLR)

## Extraction Framework

For each relevant paper, extract:

| Field | Description | Example |
|-------|-------------|---------|
| **Citation** | Author, Year, Title | Smith et al., 2024. "Neural Code Analysis..." |
| **Core Algorithm** | Main technique proposed | Graph Neural Network for dependency analysis |
| **Key Result** | Primary finding | 23% improvement in bug detection |
| **Applicability** | How it relates to our problem | Could enhance Phase 3 intelligence layer |
| **Limitations** | Known weaknesses | Requires large training dataset |

## Synthesis Method

After collecting 3-5 relevant papers:

1. **Map the landscape**: Create a comparison table of approaches
2. **Identify consensus**: What do most papers agree on?
3. **Spot gaps**: What problems remain unsolved?
4. **Assess feasibility**: Which approaches can be realistically adopted?
5. **Note risks**: What are the failure modes identified in literature?

## Citation Format

Use this format in the RFC:

```
[Author1, Author2, & Author3, Year]. "[Title]" [Conference/Journal]. [URL if available]
```

Example:
```
[Li, Zhang, & Wang, 2024]. "Attention-Based Code Clone Detection" ICSE 2024. https://arxiv.org/abs/xxxx.xxxxx
```

## Common Pitfalls

- **Cherry-picking**: Don't only cite papers that support your proposed solution — include contradictory evidence too
- **Stale research**: Avoid papers older than 3 years unless they are foundational (e.g., the original paper introducing a core algorithm)
- **Over-claiming**: Don't claim a paper "proves" your approach works if it only addresses a sub-problem
- **Missing negative results**: Include papers that report failures or limitations of similar approaches
