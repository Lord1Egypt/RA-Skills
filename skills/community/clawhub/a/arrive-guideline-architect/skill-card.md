## Description:

Generate ARRIVE 2.0 compliant animal research protocols with structured experimental design, sample size calculations, and reporting checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers and developers use this skill to draft or check animal research protocols against ARRIVE 2.0 reporting expectations before ethics review, grant review, or manuscript preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated protocols may omit institution-specific ethics, animal welfare, or statistical requirements.

Mitigation: Have the protocol reviewed by the relevant ethics committee, animal care staff, and statistical reviewer before study execution.

Risk: The skill can run shell commands and write protocol or checklist files.

Mitigation: Run it in a controlled workspace with intended study inputs and review output paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/arrive-guideline-architect)
- [ARRIVE 2.0 checklist evidence](artifact/arrive_checklist.md)
- [Example ARRIVE protocol evidence](artifact/example_protocol.md)
- [Example study brief evidence](artifact/example_study_brief.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown protocols and checklists, JSON study briefs, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write protocol or checklist files to a user-specified output path.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
