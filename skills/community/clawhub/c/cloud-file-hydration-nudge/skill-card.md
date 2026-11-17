## Description:

Hydrate visible but unreadable cloud placeholder files with provider-aware read verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[talonpoint](https://clawhub.ai/user/talonpoint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to handle cloud-synced placeholder files by proving readability, choosing a provider-aware hydration nudge, and verifying the same bounded read before downstream parsing or import continues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad runtime could receive privacy-gated permissions while trying to hydrate files.

Mitigation: Grant Accessibility or similar permissions only to a trusted narrow helper or approved automation host.

Risk: Provider metadata, badges, or policy state could be mistaken for local readable bytes.

Mitigation: Require the same bounded content read to succeed before downstream parsing, copying, or import continues.

Risk: Changing paused, offline, or unavailable sync state could override user control.

Mitigation: Stop and request explicit user consent before starting, resuming, or changing provider sync state.

Risk: Automated preview-based hydration can open broader UI and parser surfaces.

Mitigation: Avoid Quick Look automation and use provider-native or approved provider-UI hydration paths first.

## Reference(s):

- [Release Notes - 1.1.0](references/release-notes-1.1.0.md)
- [Cloud File Hydration Nudge on ClawHub](https://clawhub.ai/talonpoint/skills/cloud-file-hydration-nudge)
- [talonpoint publisher profile](https://clawhub.ai/user/talonpoint)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, markdown]

**Output Format:** [Markdown guidance with inline bash, Swift, AppleScript, and local-note examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provider state must be treated as diagnostic until a bounded read succeeds.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
