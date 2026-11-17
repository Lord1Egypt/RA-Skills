## Description:

Evolve Self-Improving helps an agent evaluate corrections, feature requests, knowledge gaps, and errors during a conversation and persist only verified, reusable lessons to local knowledge files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzusp](https://clawhub.ai/user/zzusp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve stable lessons from corrections, feature requests, knowledge gaps, and resolved errors across sessions. It is intended for local knowledge maintenance where saved entries are evidence-backed, scoped, and periodically reviewed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory can influence future sessions even when entries are scoped.

Mitigation: Install only when persistent local memory is desired, review saved entries periodically, and avoid saving sensitive, private, credential, customer, or raw conversation content.

Risk: Incorrect or insufficiently verified lessons could be reused later.

Mitigation: Save only evidence-backed, reusable conclusions and run the bundled validation checks before relying on updated knowledge or experience files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zzusp/skills/evolve-self-improving)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, generated index text, shell commands, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local knowledge and experience entries under ~/.agent-knowledge/ when the skill's evidence and validation criteria are met.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
