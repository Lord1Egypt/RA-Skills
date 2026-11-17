## Description:

Provides a persistent five-layer cognitive memory flow that records inputs, retrieves related working, episodic, and semantic memory, and suggests a response strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[louiskwee](https://clawhub.ai/user/louiskwee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to enrich an agent run with persistent memory recall, intent analysis, skill selection, and response guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores raw prompts and can reuse remembered conversation content in later context.

Mitigation: Do not use it with secrets, credentials, personal data, or confidential work unless persistence is opt-in, scoped, redacted, and deletable.

Risk: The security evidence reports that memory files may be written outside the package folder.

Mitigation: Configure storage to an approved host-controlled location and review write permissions before deployment.

Risk: Automatically injected memory can carry stale or sensitive context into future agent responses.

Mitigation: Review injected context, provide deletion and redaction controls, and limit memory scope per user or workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/louiskwee/skills/backup-global-cognitive-brain-20260316-100703)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Structured dictionary containing a thought trace, selected skill, and Markdown response suggestion.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist and reuse conversation content across sessions.]

## Skill Version(s):

1.0.0 (source: server release evidence and package metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
