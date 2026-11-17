## Description:

Create Business Plan is a reusable cross-category methodology for helping agents craft, assess, and revise new-product business plans for investment review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swanwei](https://clawhub.ai/user/swanwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and business teams can use this skill to guide an agent through product-launch business planning, including market research, competitive analysis, unit-economics modeling, compliance planning, launch gating, and editable BP deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes behavior that may persistently edit its own SKILL.md after feedback.

Mitigation: Disable automatic self-editing or require explicit user approval and review before any skill-file update is applied.

Risk: The skill may read project memory or logs during update requests.

Mitigation: Confirm the exact memory or log files before reading them and limit access to files needed for the requested update.

Risk: The skill describes external document-upload and knowledge-base storage workflows.

Mitigation: Require explicit user approval before cloud uploads or knowledge-base storage, and keep credentials out of files and memory.

Risk: The skill references dependencies and helper tooling for document generation or upload workflows.

Mitigation: Pin dependencies and review helper scripts before execution in production environments.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code snippets, shell commands, and document-generation instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce editable document workflows such as PPTX, DOCX, HTML, or aipage guidance depending on the user's requested deliverable.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
