## Description:

Manage InnoSage Draft pages and hosted Secret Shares, and read public preview feedback through bounded first-party HTTPS requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toliuweijing](https://clawhub.ai/user/toliuweijing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect and manage Draft pages in a selected JSON Workspace, read public preview feedback, and create or open hosted Secret Shares when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Page edits, publication, or hosted sharing could target unintended content or destinations.

Mitigation: Confirm the active workspace and selected content, and require explicit user direction before edits, publication, or sharing.

Risk: API keys and share passwords could be exposed.

Mitigation: Protect credentials and avoid including secret values in generated output.

Risk: The pinned npm package is external to the reviewed skill instructions.

Mitigation: Verify the pinned package before installation; review the CLI implementation separately because this assessment covers the skill instructions, not that implementation.

## Reference(s):

- [Draft](https://draft.innosage.co)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, JSON, Guidance]

**Output Format:** [CLI commands and results; page content as Markdown or text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operations depend on a selected workspace or explicit share inputs.]

## Skill Version(s):

1.10.1 (source: frontmatter; server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
