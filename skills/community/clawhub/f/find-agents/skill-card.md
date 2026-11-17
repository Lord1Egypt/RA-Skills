## Description:

Performs intelligent web and specialized searches, aggregates multi-source results, and returns summarized answers with source citations and confidence signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgta23](https://clawhub.ai/user/hgta23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agent users can use this skill to search current web, news, academic, code, and image sources, then receive concise cited summaries for research, fact checking, technical lookup, and information gathering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and fetched page URLs or page content may be sent to external web, search, or AI services during use.

Mitigation: Avoid private or sensitive queries, use approved service endpoints and keys, and run the skill only in environments where this network behavior is permitted.

Risk: Summaries, citations, source credibility scores, and fact-check verdicts can be incomplete, outdated, or misleading when upstream search results are weak.

Mitigation: Review cited sources, dates, and source quality before relying on results for important decisions.

Risk: The default search language setting may not match the user's intended locale.

Mitigation: Set SEARCH_LANGUAGE explicitly for the target audience or workflow.

Risk: Unlocked dependency installation may introduce supply-chain variance across environments.

Mitigation: Use a locked dependency install and managed package policy for production or enterprise deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hgta23/skills/find-agents)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured Markdown, CLI text, and JSON-style result objects with summaries, key findings, source URLs, confidence scores, and related queries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on configured search services, result limits, timeout settings, language settings, and the availability and quality of external sources.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
