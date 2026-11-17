## Description:

Runs multiple UX/UI designer personas in parallel against a live web app, ranks findings through cross-persona voting, and outputs a ranked report plus a machine-readable fix plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaicianflone](https://clawhub.ai/user/kaicianflone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to review live web apps through multiple UX lenses, prioritize the most impactful issues, and produce a fix plan that can guide follow-up implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes design reports into the reviewed project and stores temporary evidence/session data locally.

Mitigation: Run it only on projects where report and fix-plan files are acceptable, then review generated artifacts before committing or sharing them.

Risk: Server security evidence flags persistent local telemetry and sourceable shell state as suspicious.

Mitigation: Review or disable telemetry, timeline, and learnings hooks before installing, especially hooks that create state under ~/.gstack or execute helpers under ~/.claude/skills/gstack/bin.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaicianflone/skills/design-panel)
- [gstack browser tooling](https://github.com/garrytan/gstack)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report and schema-versioned Markdown fix plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes review artifacts under docs/design-panel/ and temporary evidence/session files under local gstack paths when available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
