## Description:

Compares two local documents through Calliper and returns their differences as Markdown for review and downstream analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paodingai](https://clawhub.ai/user/paodingai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document reviewers compare two selected files to review changes, inspect clause differences, or feed structured Markdown differences into follow-up checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected document contents and filenames are sent to the configured Calliper endpoint.

Mitigation: Confirm the destination before use and obtain approval before submitting confidential or regulated documents.

Risk: Overridden endpoint settings can send documents and an API token to an unintended service.

Mitigation: Verify endpoint-related environment variables before running the skill.

Risk: Unreviewed updates may change what code runs locally.

Mitigation: Install a pinned version or reviewed commit when possible.

## Reference(s):

- [Calliper SaaS Markdown on ClawHub](https://clawhub.ai/paodingai/skills/calliper-compare2markdown)
- [paodingai publisher profile](https://clawhub.ai/user/paodingai)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown diff table; plain text or JSON if returned by the service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prints the result and optionally saves it to a Markdown file.]

## Skill Version(s):

1.4.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
