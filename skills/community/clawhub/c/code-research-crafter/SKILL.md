---
name: code-research-crafter
description: >
  Research codebases and craft professional RFC proposals for GitHub publication.
  Use when: user wants to analyze a codebase and propose enhancements, write an RFC,
  research a technical problem with academic rigor, design an architecture proposal,
  submit a proposal to an open-source project, or create a structured improvement plan.
  NOT for: simple code reviews, bug fixing, general Q&A, quick code searches, or one-off questions.
version: 1.1.0
context: fork
metadata:
  openclaw:
    emoji: "🔬"
    homepage: https://github.com/zz0116/code-research-crafter
    requires:
      bins:
        - git
        - gh
---

# Code Research Crafter

Craft comprehensive research proposals from code analysis to GitHub RFC publication.

## Workflow

### Phase 1: Problem Discovery & Code Analysis

1. Ask the user for the target codebase (URL or local path) and the research topic. If neither is provided, do not proceed — ask the user to clarify.
2. Map the project structure: use `glob **/*.{ts,js,py,go,rs,java}` based on the detected language. Read `README.md`, `CONTRIBUTING.md`, and docs in `docs/` for context.
3. Search for topic-relevant files: `grep "[keyword]" src/**` to locate key implementations.
4. Read the top relevant files and document findings in `research-context.md`:
   - **Code Map**: file paths and their roles (table format)
   - **Problem List**: each problem with `file:line` reference and severity (high/medium/low)
   - **Metrics**: quantified issues (e.g., "3/10 modules lack error handling", "40% of functions have no tests")
5. Search existing GitHub issues: `gh issue list -R [repo] --search "[topic]" --limit 20`.

**Error handling**: If the codebase is inaccessible, ask for an alternative URL or local path. If the topic is too broad, narrow down with the user before proceeding.

### Phase 2: Academic & Community Research

1. Load `references/academic-research-guide.md` for search methodology.
2. Use WebSearch for academic papers: `"site:arxiv.org [topic] 2024 2025"`, `"site:scholar.google.com [topic]"`.
3. Use WebFetch to read top 3-5 relevant papers and extract: algorithms, data structures, evaluation methods.
4. Search GitHub discussions: `gh api repos/[owner]/[repo]/discussions --jq '.[].title'` (if discussions are enabled).
5. Analyze community sentiment from issues: note pain points, feature requests, and maintainer feedback patterns.
6. Append findings to `research-context.md` under sections:
   - **Academic Insights**: algorithms, approaches, evaluation metrics
   - **Community Pulse**: top pain points, requested features, maintainer stance
   - **Gaps**: current implementation vs. best practices

**Error handling**: If no academic papers are found, note the gap and proceed with community research only. If the repo has no issues/discussions, focus on academic research and documentation review.

### Phase 3: Solution Design

1. Load `references/architecture-patterns.md` for proven design patterns.
2. Define evidence-based design principles derived from Phase 1-2 findings.
3. Design a layered architecture:
   - **Layer 1 — Foundation**: data collection and storage
   - **Layer 2 — Enhancement**: core features building on Foundation
   - **Layer 3 — Intelligence**: AI/ML capabilities on accumulated data
   - **Layer 4 — Governance**: control, monitoring, and policy enforcement
4. Define data models: dual-track (user-defined/static + system-learned/dynamic).
5. Plan phased implementation with milestones:
   - Phase 1 → Foundation (weeks 1-4)
   - Phase 2 → Enhancement (weeks 5-8)
   - Phase 3 → Intelligence (weeks 9-12)
   - Phase 4 → Governance (weeks 13-16)
6. Document trade-offs: migration path, backward compatibility, performance cost, risk assessment.

**Checkpoint**: Present the proposed solution design to the user. Wait for approval before proceeding. If the user requests changes, iterate on the design and re-present.

### Phase 4: Documentation Generation

1. Determine language needs:
   - If the target project's primary language is Chinese → generate bilingual (Chinese + English) documents
   - If the target project is international → generate English-only documents
   - Always generate the RFC in English (the lingua franca of open source)
2. Generate a structured technical document using python-docx (if available) or markdown:
   - Include: table of contents, numbered headings, citations, references section
   - Use consistent terminology throughout
   - Save as `proposal.md` (and `proposal.docx` if python-docx is available)

### Phase 5: RFC Writing

1. Load `references/rfc-template.md` for the standard RFC template.
2. Write the RFC in English with these required sections:
   ```
   # RFC: [Title]

   ## Metadata
   - Author: [name]
   - Date: [YYYY-MM-DD]
   - Status: Draft
   - Related Issues: #[issue numbers]

   ## Problem Statement
   [Quantified problem with code evidence and metrics]

   ## Prior Art
   [Academic research, existing solutions, and community context]

   ## Proposed Solution
   [Architecture, data models, API design, implementation phases]

   ## Trade-offs
   [Cost analysis, migration path, backward compatibility, risks]

   ## Open Questions
   [Unresolved decisions needing community input]

   ## Call for Collaboration
   [How to get involved, what help is needed]
   ```
3. Include code examples (with syntax highlighting) and ASCII architecture diagrams.
4. Reference specific GitHub issues and discussions using `#123` format.
5. Self-review: verify every claim has a citation (code location or paper reference).

### Phase 6: GitHub Publication

1. Check authentication: `gh auth status`. If not authenticated, provide setup instructions and ask the user to configure.
2. Save the RFC as `rfc-[slug].md` in the project's `docs/` or `proposals/` directory.
3. Create a GitHub issue:
   ```bash
   gh issue create -R [owner]/[repo] \
     --title "RFC: [Title]" \
     --body-file rfc-[slug].md \
     --label "enhancement" --label "RFC"
   ```
4. If `gh` CLI is unavailable, try GitHub API via `curl`:
   ```bash
   curl -X POST -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/repos/[owner]/[repo]/issues \
     -d '{"title":"RFC: [Title]","body":"[RFC content]","labels":["enhancement","RFC"]}'
   ```
5. If all CLI options fail, output the RFC markdown with manual submission instructions:
   - URL to create issue: `https://github.com/[owner]/[repo]/issues/new`
   - Suggested title and labels
   - Full RFC content to paste
6. Reference related issues in the created issue body. Do NOT tag maintainers unless the user explicitly asks.

## Output Artifacts

| Artifact | Format | Description |
|----------|--------|-------------|
| `research-context.md` | Markdown | Running document updated through Phases 1-3 |
| `proposal.md` / `proposal.docx` | MD/DOCX | Structured technical document |
| `rfc-[slug].md` | Markdown | RFC in standard format |
| GitHub Issue | Web | Link to published RFC |

## Best Practices

1. **Quote specific code locations** — always reference file paths and line numbers
2. **Quantify problems** — use metrics like "50% of files" or "3x performance improvement"
3. **Cite recent research** — prefer papers from 2024-2025
4. **Design for adoption** — include migration paths and gradual rollout plans
5. **Track costs** — document token usage, performance implications, and resource requirements
6. **Engage early** — reference existing issues and invite collaboration from the start
7. **Self-review citations** — verify every claim has a code location or paper reference
