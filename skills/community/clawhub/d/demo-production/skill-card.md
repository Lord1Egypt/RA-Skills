## Description:

Turn rough product ideas into interactive demos with a structured prototype-review-production pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stdoses72](https://clawhub.ai/user/stdoses72)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to turn vague product ideas into planned, clickable demos with explicit assumptions, mock-versus-real boundaries, a review gate, and follow-up edge case validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages the agent to infer missing product requirements, which can produce an impressive demo that still reflects wrong assumptions.

Mitigation: Keep assumptions explicit and use the Stage 3 review gate to confirm workflow, visual direction, missing screens, and whether to continue.

Risk: Demo work touching sensitive domains, real infrastructure, authentication, billing, compliance, or production data can carry higher operational or policy risk.

Mitigation: Review assumptions before approving Stage 4 and require explicit user confirmation before using real systems or sensitive data.

Risk: Focused reference research can improve familiar product patterns but may lead to copying protected branding, proprietary UI, or marketing language.

Mitigation: Use references only for workflow, information architecture, terminology, and interaction patterns; avoid cloning protected assets or product-specific copy.

## Reference(s):

- [Demo Production on ClawHub](https://clawhub.ai/stdoses72/skills/demo-production)
- [README](artifact/README.md)
- [Evaluation Guidance](artifact/EVAL.md)
- [Test Cases](artifact/TEST_CASES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown progress updates and final delivery notes, with code, file edits, shell commands, configuration, and runnable demo artifacts as needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include assumptions, clickable prototype notes, mocked or simulated behavior boundaries, run instructions, and edge case validation results.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
