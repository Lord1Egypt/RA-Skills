## Description:

Maintains persistent focus on active work across compactions and session restarts by keeping concise workspace state in FOCUS.md and FOCUS-LOG.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crewhaus](https://clawhub.ai/user/crewhaus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to maintain a short, local record of the current project, active plan, blockers, and resume point across session starts, compactions, and restarts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local focus files may capture secrets, credentials, sensitive personal details, or confidential notes if the agent records too much context.

Mitigation: Keep FOCUS.md and FOCUS-LOG.md brief and limited to active work state; exclude secrets, credentials, sensitive personal details, and confidential notes.

Risk: Outdated local focus state may cause the agent to resume the wrong task after priorities shift or work is completed.

Mitigation: Update the active state when priorities change, archive completed work to FOCUS-LOG.md, and clear FOCUS.md when there is no active project.

## Reference(s):

- [Focus Tracker ClawHub Skill Page](https://clawhub.ai/crewhaus/skills/focus-tracker)

## Skill Output:

**Output Type(s):** [Files, Markdown, Guidance]

**Output Format:** [Markdown workspace files and concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local workspace state in FOCUS.md and FOCUS-LOG.md; no external data transfer is indicated by the security evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
