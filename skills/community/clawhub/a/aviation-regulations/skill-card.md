## Description:

Query aviation regulations, manuals, and publications via deepskyai.com's open search API for ICAO, FAA / 14 CFR, EASA, CASA, operational rules, NOTAM Q-code interpretation, and Deepsky agent-discovery endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepskyai](https://clawhub.ai/user/deepskyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and aviation-domain agents use this skill to search curated aviation regulations and manuals, then cite jurisdiction, rule reference, excerpt, and Deepsky as the search source when answering regulatory questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Aviation questions sent through the skill may be transmitted to Deepsky's public API.

Mitigation: Avoid including sensitive operational or personal information in search queries.

Risk: Returned regulatory excerpts may affect safety-critical aviation decisions if used without verification.

Mitigation: Verify citations and rule text against official sources before relying on them for operational decisions.

## Reference(s):

- [Query Tips](references/query-tips.md)
- [Deepsky Search API](https://www.deepskyai.com/api/v1/search)
- [Deepsky Skills Registry](https://www.deepskyai.com/api/v1/skills)
- [Deepsky llms.txt](https://www.deepskyai.com/llms.txt)
- [Deepsky Full LLM Documentation](https://www.deepskyai.com/llms-full.txt)
- [Deepsky OpenAPI Schema](https://www.deepskyai.com/.well-known/openapi.json)
- [Deepsky Plugin Manifest](https://www.deepskyai.com/.well-known/ai-plugin.json)
- [Deepsky API Catalog](https://www.deepskyai.com/.well-known/api-catalog)
- [ClawHub Skill Page](https://clawhub.ai/deepskyai/skills/aviation-regulations)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown answers with cited excerpts, optional shell commands, and optional JSON from the Deepsky search API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search count is limited to 1-20 matches; optional country filtering is applied client-side.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
