## Description:

Audit and harden an OpenClaw workspace setup (AGENTS/SOUL/USER/HEARTBEAT/memory) with concise, enforceable rules, safety boundaries, and low-bloat instruction design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cwheeler67](https://clawhub.ai/user/cwheeler67)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to audit and improve workspace instruction and memory files for clearer behavior, tighter safety boundaries, and lower instruction bloat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Edits to workspace instruction or memory files can change future agent behavior in unintended ways.

Mitigation: Review proposed diffs carefully before accepting changes, especially changes to privacy, approval, or destructive-action boundaries.

Risk: Overbroad hardening edits could remove user preferences or useful platform-specific norms.

Mitigation: Keep changes small and targeted, preserve explicit user preferences, and ask before applying broad policy changes.

## Reference(s):

- [Workspace Hardening Rubric](references/rubric.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown summary with file-change list and one recommended next step]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected summary is 3-8 bullets, plus changed files and a single highest-leverage follow-up.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
