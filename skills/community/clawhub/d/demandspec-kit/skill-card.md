## Description:

DemandSpec helps agents analyze, clarify, specify, review, validate, approve, and archive product and business requirements, including PRDs, AI scenarios, prototypes, acceptance criteria, requirement changes, and development handoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[debtvc2022](https://clawhub.ai/user/debtvc2022)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, business analysts, designers, and engineers use DemandSpec to turn raw ideas, meeting notes, existing PRDs, UI or system material, and AI scenario proposals into workspace requirement assets. It supports requirements intake, clarification, scoping, process modeling, prototype specification, acceptance criteria, validation, development handoff, and archival.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects workspace materials and may read unrelated sensitive files if the requested scope is broad.

Mitigation: Give the agent specific files or folders to inspect and exclude unrelated sensitive paths when using the skill.

Risk: The skill writes or updates requirement assets in the workspace as part of its normal workflow.

Mitigation: Use the skill when file creation or updates are intended; ask explicitly for advice only when no files should be changed.

Risk: Generated requirement documents can contain assumptions, unresolved blockers, or validation failures that are not business-approved facts.

Mitigation: Review facts, assumptions, blockers, owners, and validation results before treating generated documents as confirmed requirements.

## Reference(s):

- [DemandSpec Template Filling Guide](artifact/references/template-filling-guide.md)
- [Visit Form Auto-Generation Example](artifact/references/visit-form-auto-generation-example.md)
- [DemandSpec ClawHub Skill Page](https://clawhub.ai/debtvc2022/skills/demandspec-kit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files, structured completion reports, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill writes selected requirement assets to workspace paths such as demands/<demand-id>/ or changes/<change-id>/ when file creation or updates are requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
