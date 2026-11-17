## Description:

Helps an agent complete user-delegated data analysis tasks over uploaded files in the working directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realroc](https://clawhub.ai/user/realroc)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to delegate data analysis tasks to an agent, including analysis work over explicitly uploaded files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided datasets may contain sensitive information.

Mitigation: Only provide datasets appropriate for the surrounding agent environment and the tools it may use.

Risk: File-based analysis can fail or target the wrong file if uploaded filenames are not referenced directly.

Mitigation: Reference intentionally provided files by their uploaded filename and avoid relying on external paths.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text, with code or shell snippets when file analysis requires them.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assumes user-provided files are available by filename in the working directory.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
