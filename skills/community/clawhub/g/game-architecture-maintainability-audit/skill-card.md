## Description:

Audit architecture, state management, boundaries, coupling, and maintainability risks that will make future AI or human iteration harder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike007jd](https://clawhub.ai/user/mike007jd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game engineers use this skill to inspect game projects for architecture, state management, module boundary, coupling, and maintainability risks. It helps produce evidence-based audit outputs that guide future human or AI-assisted iteration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may write or update audit documentation in a project.

Mitigation: Review changes to docs/game-studio/audit before committing or publishing them.

Risk: Audit findings may be incomplete or misleading when project context is sparse.

Mitigation: Run with enough project file access for evidence and verify findings against the codebase.

Risk: If shell or build access is enabled, the agent may use normal project inspection or build commands for evidence.

Mitigation: Run in an appropriate workspace and review commands when the agent environment supports approval gates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mike007jd/skills/game-architecture-maintainability-audit)
- [README](artifact/README.md)
- [Architecture Maintainability Audit Checklist](artifact/shared/checklists/architecture-maintainability-audit-checklist.md)
- [Game-dev abstractions](artifact/shared/reference/game-dev-abstractions.md)
- [Usage Examples](artifact/examples/usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown audit summaries, JSON scorecards, and risk register guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write bounded audit files under docs/game-studio/audit when file access is available.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
