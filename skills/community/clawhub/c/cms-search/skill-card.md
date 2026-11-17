## Description:

Searches the web and retrieves current information for requests that need online sources, recent news, policies, announcements, current data, market research, medical information, financial information, or cross-source verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spzwin](https://clawhub.ai/user/spzwin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent must collect timely web evidence, compare sources, and summarize or verify current information across general, domestic, international, market, medical, financial, or policy topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, selected source, optional datetime, and CMS_USER_KEY are sent to a fixed CMS search service.

Mitigation: Install only in environments where sending those values to the service is acceptable, and keep CMS_USER_KEY in environment-managed secrets rather than scripts or command arguments.

Risk: Returned search results are untrusted web evidence and may be incorrect, outdated, or incomplete for sensitive topics.

Mitigation: Verify important claims independently, especially for medical, financial, policy, or business-sensitive decisions.

## Reference(s):

- [Cms Search ClawHub Skill Page](https://clawhub.ai/spzwin/skills/cms-search)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or JSON search results, with direct Python command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CMS_USER_KEY; supports optional source and datetime parameters.]

## Skill Version(s):

1.5.5 (source: server release metadata and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
