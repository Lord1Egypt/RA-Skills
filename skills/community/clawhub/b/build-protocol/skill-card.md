## Description:

Rigorous workflow for producing long-form knowledge content with multi-agent collaboration, independent audit, versioned errata, and machine-verifiable quality gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christianye](https://clawhub.ai/user/christianye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and content teams use this skill to structure long-form knowledge products such as textbooks, knowledge bases, and deep reports. It guides planning, sub-agent task design, assembly, independent audit, fixes, publishing checks, and errata management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic activation can move the agent into heavyweight publishing, uploading, moving, archiving, or overwrite workflows.

Mitigation: Require explicit user confirmation before publishing, uploading, moving, archiving, replacing, or overwriting deliverables.

Risk: The bundled audit script template may be mistaken for a ready CI gate.

Mitigation: Review and fix its exit-status behavior and zero-match handling before relying on it for automated gating.

Risk: The workflow is intentionally heavyweight and may be inappropriate for short or simple writing tasks.

Mitigation: Use it only for long-form knowledge products or multi-step, multi-agent content work where independent audit and versioned errata are required.

## Reference(s):

- [Build Protocol Skill Page](https://clawhub.ai/christianye/skills/build-protocol)
- [Workflow Checkpoints](artifact/references/workflow-checkpoints.md)
- [Audit Script Template](artifact/references/audit-script-template.sh)
- [Sub-agent Task Spec Examples](artifact/references/subagent-spec-examples.md)
- [Supplements Knowledge Base Case Study](artifact/references/case-study-supplements.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with task specifications, checklists, changelog structure, and shell audit command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included audit script template is project-specific and should be configured and reviewed before use as a gate.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
