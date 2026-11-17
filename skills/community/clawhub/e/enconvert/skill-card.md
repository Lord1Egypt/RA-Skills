## Description:

Render web pages and files into agent-ready markdown, structured data, screenshots, and PDFs via EnConvert, with a render_quality honesty score on every read.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enconvert](https://clawhub.ai/user/enconvert)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to read URLs, search or discover web pages, extract structured fields, and convert hosted files into markdown, JSON, screenshots, or PDFs through EnConvert.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an EnConvert private API key.

Mitigation: Store the key only in ENCONVERT_API_KEY, do not print or hardcode it, and do not send it when fetching third-party source URLs or signed output URLs.

Risk: Selected URLs or files are sent to EnConvert for conversion.

Mitigation: Use the skill only when that transfer is intended and approved, and avoid confidential documents, private systems, localhost, internal network URLs, and cloud metadata endpoints.

Risk: Blocked or degraded pages can produce incomplete content.

Mitigation: Check render_quality and block indicators; treat scores below 0.40 or is_blocked responses as failed reads rather than reliable content.

## Reference(s):

- [EnConvert documentation](https://www.enconvert.com/docs)
- [EnConvert API keys](https://www.enconvert.com/dashboard/api-keys)
- [ClawHub skill page](https://clawhub.ai/enconvert/skills/enconvert)
- [Publisher profile](https://clawhub.ai/user/enconvert)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May point agents to signed or presigned output URLs and requires checking render_quality before trusting page content.]

## Skill Version(s):

0.0.2 (source: frontmatter and changelog, released 2026-09-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
