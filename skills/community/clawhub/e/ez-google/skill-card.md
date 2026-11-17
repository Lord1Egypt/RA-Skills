## Description:

Retirement notice directing users with Google Workspace tasks to Google's Workspace CLI and agent skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[araa47](https://clawhub.ai/user/araa47)

### License/Terms of Use:

MIT-0

## Use Case:

For users and agents handling Gmail, Calendar, Drive, Docs, Sheets, Slides, or Contacts requests, this retired skill explains that the former sign-in no longer works and points them to Google's Workspace CLI and its agent skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unpinned `npx skills add` command may retrieve a different package version over time.

Mitigation: Review the source and resolved version before running it; use a pinned revision when supported.

Risk: The retired ezagentauth.com sign-in and its tokens no longer work.

Mitigation: Do not use the legacy login flow; migrate to Google's Workspace CLI and remove old credentials if present.

## Reference(s):

- [Google Workspace CLI and agent skills](https://github.com/googleworkspace/cli)
- [ez-google ClawHub release page](https://clawhub.ai/araa47/skills/ez-google)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retirement and migration guidance; does not perform Google Workspace actions.]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
