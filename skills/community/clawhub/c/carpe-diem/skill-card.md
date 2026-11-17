## Description:

Help developers and creators who have a Coding Agent but no clear project direction discover, validate, plan, and track a worthwhile open-source project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanghaonan3333-web](https://clawhub.ai/user/wanghaonan3333-web)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators with coding agents use this skill to choose a project direction, validate ideas, produce an implementation plan, and track progress after handoff. It is intended for facilitation and read-only progress review, not for implementing business code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer has a local file-safety issue and outdated install documentation.

Mitigation: Review the installer before running it, prefer the manual plan/apply/verify flow, and avoid one-click installation on multi-user systems until the installer handling and documentation are fixed.

Risk: The skill may request access to project directories, GitHub, issues, CI, or profile state for planning and tracking.

Mitigation: Grant only the specific read scope needed for the current session and re-authorize when the target or scope changes.

## Reference(s):

- [Carpe Diem homepage](https://github.com/wanghaonan3333-web/carpe-diem)
- [Methodology](references/methodology.md)
- [Safety Boundaries](references/safety-boundaries.md)
- [State Schema](references/state-schema.md)
- [Stage Transition Graph](references/stage-transition-graph.md)
- [Wisdom Card Index](references/wisdom/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational guidance with Markdown plans, summaries, handoff documents, and scoped shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update profile or project state only after user confirmation; tracking remains read-only.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
