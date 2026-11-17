## Description:

Ship focused repository changes with Flixa: inspect, implement, verify, and return a shareable proof of work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deniai](https://clawhub.ai/user/deniai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide focused repository work: inspect local instructions, make scoped changes, run relevant verification, and report proof of work without bypassing approval or safety boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The separate Flixa backend plugin is outside this skill package and may introduce additional operational or security considerations.

Mitigation: Review the backend plugin independently before installing or using it with this workflow skill.

Risk: Repository-workflow guidance can lead to file edits, shell commands, or git operations if applied without appropriate runtime approvals.

Mitigation: Use the skill's explicit approval boundaries and perform read-only inspection before commands or edits when the active runtime requires approval.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise status sections and inline command evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a shareable Ship Card when explicitly requested; the skill requires redaction of secrets and absolute paths.]

## Skill Version(s):

0.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
