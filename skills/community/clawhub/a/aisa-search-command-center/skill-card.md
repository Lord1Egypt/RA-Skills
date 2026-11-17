## Description:

Run web, multi-source, or last-30-days research through AIsa for search, synthesis, competitor scans, trend discovery, research-ready outputs, and structured retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research-focused agents use this skill to run AIsa-backed web, scholar, multi-source, and recent-signal searches, then turn retrieved evidence into summaries, comparisons, and research briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, prompts, and target URLs are sent to AIsa-backed online services.

Mitigation: Use a scoped AISA_API_KEY, avoid confidential prompts or internal URLs, and send only public or authorized targets.

Risk: Crawl, map, and extract workflows can submit website URLs to external services.

Mitigation: Use these workflows only for public sites or sites where the user has authorization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/aisa-search-command-center)
- [AIsa API endpoint](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON-formatted CLI/API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; online retrieval results may include provider errors or partial source coverage.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
