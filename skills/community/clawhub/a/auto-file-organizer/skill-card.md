## Description:

Helps users organize download folders and categorize files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neutronstar238](https://clawhub.ai/user/neutronstar238)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent to manage local files can invoke this skill to organize a specified download folder and classify files into categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad file tools could move or rewrite files in an unintended folder if the target location is ambiguous.

Mitigation: Tell the agent the exact folder to organize and require a preview of proposed moves before any changes are made.

Risk: The skill documentation is sparse and in Chinese, which may make behavior harder to review for some users.

Mitigation: Install only when Chinese-language documentation is acceptable and review the skill behavior before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with proposed file-organization actions and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Should preview proposed file moves before changing files.]

## Skill Version(s):

0.1.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
