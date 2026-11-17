## Description:

VDV Core is a truth-seeking analysis protocol for detecting contradictions, reducing noisy complexity, and identifying invariant points in dense information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to apply a structured VDV analysis loop to complex or contradictory text. It can guide Markdown-style analysis and provide local script commands that emit JSON analysis results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags broad activation instructions and persistence of derived patterns without clear user control.

Mitigation: Review before installing, only activate the skill for explicit VDV-style analysis, and require confirmation before memory writes or custom storage paths.

Risk: Analysis or stored outputs may contain confidential source text or derived patterns.

Mitigation: Avoid confidential inputs unless local persistence and agent-memory retention are acceptable, and define a retention and deletion plan before storing results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kofna3369/skills/axiomata-vdv-core)
- [Publisher Profile](https://clawhub.ai/user/kofna3369)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with optional JSON output from local Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON analysis records when storage commands are used.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
