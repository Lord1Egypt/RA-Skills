## Description:

Fetches web pages and extracts readable content for AI use, with fallbacks for pages blocked by bot checks, login walls, or JavaScript rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aurthes](https://clawhub.ai/user/aurthes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve, summarize, or extract structured information from public web pages and small URL sets, using fallback methods when direct readable fetches are blocked or incomplete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs may be sent to third-party conversion services, which can expose private, signed, or token-bearing links.

Mitigation: Use this skill only with URLs intended for agent inspection; avoid password reset links, signed download URLs, private document shares, API keys in query strings, and logged-in session pages unless that access is intentional.

Risk: Direct fetch services can return challenge pages, login walls, thin content, or secondary-source information instead of the target page.

Mitigation: Check the extraction method, confidence, and blocked or unresolved notes before relying on fetched content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aurthes/skills/aurthes-web-fetcher)
- [Publisher profile](https://clawhub.ai/user/aurthes)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON fetch results and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetch results may include the selected method, attempt history, blocked or thin-content status, and extracted page content.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
