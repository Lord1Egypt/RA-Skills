## Description:

Expert Mode helps an agent select, create, and consult project-local expert archetypes for technical review, critique, decision support, and reusable Markdown dossiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e1red](https://clawhub.ai/user/e1red)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use Expert Mode to bring specialist archetype lenses into planning, review, and decision-support work. The skill can maintain project-local expert rosters and reusable dossiers so recurring expert context stays focused and lightweight.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or update project-local expert roster and dossier files.

Mitigation: Require confirmation before file creation or updates, and review generated Markdown before relying on it.

Risk: Broad documentation-update authority could affect persistent agent behavior.

Mitigation: Do not allow changes to installed skill documentation or persistent agent behavior without explicit human review.

Risk: Expert-archetype advice can be mistaken for licensed professional advice or real-person authority.

Mitigation: Use the output as decision-support from archetypal lenses, avoid impersonation, and require qualified human review for high-stakes legal, medical, financial, safety, security, or compliance decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/e1red/skills/expert-mode-archetypes)
- [Expert Mode Activation Workflow](references/activation-workflow.md)
- [Archetype Buckets](references/archetype-buckets.md)
- [Beta Example Archetypes](references/beta-example-archetypes.md)
- [Compact Dossier Template](references/compact-dossier-template.md)
- [Custom Expert Request Mode](references/custom-expert-request-mode.md)
- [Expert Mode Dossier Schema](references/dossier-schema.md)
- [Expert Mode Examples](references/examples.md)
- [Expert Selection Taxonomy](references/expert-selection-taxonomy.md)
- [Prominent Expert Track](references/prominent-expert-track.md)
- [Response Depth Modes](references/response-depth-modes.md)
- [Expert Mode Retrieval Policy](references/retrieval-policy.md)
- [Top-Notch Expert Behaviour](references/top-notch-expert-behaviour.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional Markdown roster and dossier files plus shell commands for local helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project-local experts/roster.md and experts/dossiers/*.md when file writing is appropriate and confirmed.]

## Skill Version(s):

0.9.0 (source: server release metadata; artifact SKILL.md version: 0.9.0-expert-quality-and-depth-modes)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
