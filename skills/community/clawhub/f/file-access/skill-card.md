## Description:

Read, list, and organize files inside owner-approved folders only, with size caps, an audit log, and a hard ban on deletes, system folders, and credential files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thepodemail-lgtm](https://clawhub.ai/user/thepodemail-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

An agent uses this skill to find, read, summarize, copy, and organize everyday files within folders approved by the owner, while recording actions for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review had medium confidence and was partial because several referenced paths were missing.

Mitigation: Check that the missing references are expected before installing, and keep file operations within owner-approved folders.

## Reference(s):

- [GitHub source (skills/file-access)](https://github.com/thepodemail-lgtm/openclaw-hardened-file-access/tree/main/skills/file-access)
- [ClawHub release](https://clawhub.ai/thepodemail-lgtm/skills/file-access)

## Skill Output:

**Output Type(s):** [Files, Text, Markdown]

**Output Format:** [Files in owner-approved formats, text summaries and metadata, and a Markdown audit log]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions are limited by owner-approved folders and documented size and run caps.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
