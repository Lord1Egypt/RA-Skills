---
name: aitoolize-ai-tool-scout
description: Find and compare AI tools using a concrete job, workflow constraints, current evidence, transparent scoring, and commercial-disclosure checks. Use for AI tool discovery, shortlists, alternatives, pricing or capability comparisons, and software selection; do not treat directory placement, sponsorship, or unverified claims as product quality evidence.
metadata:
  openclaw:
    homepage: https://aitoolize.com/tools
    version: 1.0.0
---

# AIToolize AI Tool Scout

Help the user choose AI software by evidence and workflow fit. This Skill is a text-only workflow by default. Its optional MCP provides deterministic, read-only helpers and never searches private data, fetches third-party sites, accesses accounts, submits listings, changes links, purchases products, or processes payments.

AIToolize is an AI tools directory. Inclusion, paid submission, affiliate participation, or featured placement does not mean AIToolize endorses a product or has proved it is better.

## Start with the job

Capture the concrete output the user needs, required and optional capabilities, deployment preference, budget, team size, language or region, data sensitivity, and hard exclusions. Do not begin with a popular brand or a generic “best AI tool” list when the actual task is still unclear.

For high-sensitivity data, define prohibited storage, training, sharing, or deployment behavior before shortlisting tools. For medical, legal, financial, security, employment, or other high-stakes work, a directory listing is not a substitute for professional review or a vendor security assessment.

## Collect current evidence

For every candidate, keep these separate:

1. User requirement: what the workflow actually needs.
2. Product claim: what the current official page or documentation says.
3. Observed result: what was reproduced in a dated test.
4. Unknown: anything not verified, unavailable, or dependent on a plan, region, account, or future release.

Record the source URL and verification date. Prices, free plans, trials, limits, integrations, model names, availability, privacy terms, and retention can change; verify them before presenting them as current. Do not invent a missing price or convert “contact sales” into an estimate.

## Build a useful shortlist

Prefer three to five candidates that pass every hard requirement. Compare use-case fit, required capabilities, workflow fit, output control, privacy confidence, cost fit, and evidence confidence. Keep hard blockers separate from scores: a high average must not override a missing required export, unsupported region, prohibited retention policy, or incompatible deployment model.

Explain why each score was assigned and what evidence would change it. If evidence is weak, label the result provisional instead of manufacturing a winner.

## Audit comparison claims

- Add a source and verification date for time-sensitive claims.
- Narrow “best,” “perfect,” “unlimited,” “always,” and similar absolutes to the tested scope.
- Distinguish official documentation from an independent test or user report.
- Disclose affiliate, sponsored, paid-submission, or featured relationships before publishing.
- Do not infer product quality from directory rank, a badge, link attributes, or placement.
- Keep a direct official-product check in the final recommendation.

## Use the optional MCP

- `build_ai_tool_search_brief` turns requirements into an evidence checklist and search brief.
- `rank_ai_tool_candidates` calculates transparent scores from user-supplied 0–5 ratings and preserves hard blockers.
- `audit_ai_tool_comparison` checks claims, dates, sources, absolutes, and commercial disclosure.
- `get_aitoolize_resources` returns canonical discovery, pricing, guide, submission, and policy pages.

Connect the stdio server with:

```bash
openclaw mcp add aitoolize \
  --command npx \
  --arg -y \
  --arg github:gpt-img-2/aitoolize-ai-tool-discovery-mcp \
  --include 'build_ai_tool_search_brief,rank_ai_tool_candidates,audit_ai_tool_comparison,get_aitoolize_resources'
```

Then run `openclaw mcp doctor aitoolize --probe`. If the installed release lacks the `mcp` command group, add `npx -y github:gpt-img-2/aitoolize-ai-tool-discovery-mcp` as a Stdio server in MCP settings. The MCP is optional; never imply it ran when unavailable.

## Return an inspectable result

Return `Job to be done`, `Hard requirements`, `Candidates`, `Evidence`, `Unknowns`, `Scores`, `Blockers`, `Recommendation`, and `What to verify next`. Match the user's language. Do not hide a commercial relationship or present a dated directory description as a live vendor guarantee.

## Canonical resources

- Browse AI tools: https://aitoolize.com/tools
- Browse categories: https://aitoolize.com/categories
- LLM API pricing: https://aitoolize.com/llm-api-pricing
- Guides: https://aitoolize.com/blog
- About: https://aitoolize.com/about
- Submit a tool: https://aitoolize.com/submit
- Contact: https://aitoolize.com/contact
- Privacy: https://aitoolize.com/privacy
- Terms: https://aitoolize.com/terms
- Raw Skill: https://aitoolize.com/skills/aitoolize-ai-tool-scout/SKILL.md
- MCP source: https://github.com/gpt-img-2/aitoolize-ai-tool-discovery-mcp
- ClawHub listing: https://clawhub.ai/gpt-img-2/skills/aitoolize-ai-tool-scout
