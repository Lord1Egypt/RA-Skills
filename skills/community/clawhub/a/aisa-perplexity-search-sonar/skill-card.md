## Description:

Run web, multi-source, or last-30-days research through AIsa for search, synthesis, competitor scans, trend discovery, and structured retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users use this skill to run AIsa-backed web research, compare tools or companies, discover recent trends, and turn retrieved results into concise research briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search prompts, optional system instructions, and the AIsa API credential are sent to AIsa's API.

Mitigation: Avoid submitting private secrets or sensitive personal data unless your AIsa account terms and data-handling expectations allow it.

Risk: Research results can be incomplete when providers time out or fail.

Mitigation: Report timeouts or unavailable providers clearly and verify important claims against returned sources before relying on the brief.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baofeng-tech/skills/aisa-perplexity-search-sonar)
- [baofeng-tech publisher profile](https://clawhub.ai/user/baofeng-tech)
- [AIsa API base endpoint](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON returned from AIsa-backed research commands, with concise summaries and structured retrieval results when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; supported commands target sonar, sonar-pro, sonar-reasoning-pro, and sonar-deep-research.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
