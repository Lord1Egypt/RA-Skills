## Description:

AIsa Search runs web, multi-source, and last-30-days research through AIsa for search, synthesis, competitor scans, trend discovery, and structured retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, research analysts, and research-capable agents use this skill to route authenticated AIsa searches into concise research outputs. It supports recent web research, multi-source retrieval, competitor scans, trend discovery, and source-backed synthesis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, prompts, URLs, or extraction targets are sent to the external AIsa API service.

Mitigation: Avoid sending confidential prompts, private/internal URLs, secrets, or personal data unless sharing that content with AIsa is acceptable.

Risk: Some upstream research providers may time out or return partial results.

Mitigation: Report provider failures or timeouts in the final research output and retry with narrower prompts or faster modes when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/baofeng-tech/skills/aisa-search)
- [AIsa API Base URL](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON responses and Markdown summaries with CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and may return provider-specific errors, source sets, confidence scores, or timeout guidance depending on the selected retrieval mode.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
