## Description:

Coordinates a 10-stage academic research workflow from research planning through writing, integrity checks, review, revision, finalization, and process documentation.

This skill is for research and development only.

## Publisher:

[sedey999](https://clawhub.ai/user/sedey999)

### License/Terms of Use:

CC BY-NC 4.0

## Use Case:

Researchers, students, and academic-writing support teams use this skill to route an academic project through research, drafting, integrity review, peer-style review, revision, and final packaging while preserving explicit checkpoints and audit artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may read and record substantial manuscript and conversation context during long-running academic projects.

Mitigation: Use it only for intended academic pipeline work, provide the minimum necessary materials, and review retained process records before sharing them.

Risk: Optional cross-model verification can send manuscript or dialogue content to selected external providers.

Mitigation: Keep cross-model verification disabled unless the provider and content-sharing path are approved; require HTTPS endpoints and restricted dedicated API keys.

Risk: Generated process records may contain sensitive research details or collaboration history.

Mitigation: Inspect and redact process records before distribution outside the working team.

## Reference(s):

- [README](README.md)
- [Skill Definition](SKILL.md)
- [Pipeline State Machine](references/guides/pipeline_state_machine.md)
- [Claim Verification Protocol](references/guides/claim_verification_protocol.md)
- [Integrity Review Protocol](references/guides/integrity_review_protocol.md)
- [Cross-Model Verification](references/shared/cross_model_verification.md)
- [Handoff Schemas](references/shared/handoff_schemas.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and structured text with optional JSON-schema-aligned artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces stage prompts, status dashboards, integrity and review handoffs, and process records; sibling skills produce the substantive manuscript artifacts.]

## Skill Version(s):

3.21.1 (source: frontmatter metadata and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
