## Description:

Use when auditing a repository for evidence-backed gaps between code, SPECs, architecture, and documentation before a release, after a review, or when the user asks what is missing or divergent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit repositories for evidence-backed gaps between implementation, tests, specs, architecture, and documentation, then convert confirmed gaps into draft specifications and tracked work after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can move from repository audit into draft SPEC creation, GitHub issue creation, and orchestrator handoff after user approval.

Mitigation: Review generated SPECs and approve only the intended follow-up actions before allowing external issue creation or orchestration.

Risk: The orchestrator handoff may execute all approved SPECs in .specs, not only gaps found during the current audit.

Mitigation: Verify the full approved SPEC set and dependency order before approving orchestration.

Risk: User-facing confirmations are specified in Portuguese (pt-BR), which can affect review quality for users who are not comfortable with that language.

Mitigation: Require language changes or additional review before approving high-impact steps if pt-BR prompts are not suitable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afonsoft/skills/gap-analysis)
- [Publisher profile](https://clawhub.ai/user/afonsoft)
- [Source repository metadata](https://github.com/afonsoft/skills)
- [Gap record worksheet](references/gap-record.md)
- [Gap analysis report template](references/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, draft SPEC files, GitHub issue content, and approval-gated orchestration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default until an explicit approval gate; may create draft specs, GitHub issues, and orchestrator handoff artifacts after approval.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
