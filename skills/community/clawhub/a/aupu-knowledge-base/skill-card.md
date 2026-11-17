## Description:

When a user asks about local documents, knowledge bases, references, history, configuration files, instructions, internal materials, existing content, or file creation and reading, this skill directs the agent to retrieve or operate on files from /mnt/data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianeasy](https://clawhub.ai/user/jianeasy)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to make an agent consult a local /mnt/data knowledge base before answering document, reference, configuration, or file-operation requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad searches of /mnt/data even for ambiguous or general requests, which could expose unrelated private files, secrets, logs, or credentials if that directory is not scoped as an approved knowledge base.

Mitigation: Use only in environments where /mnt/data is intentionally curated for knowledge-base access, and prefer a revised version that searches explicit user-approved paths and asks before broad recursive scans.

Risk: The security verdict is suspicious because the skill strongly prioritizes local knowledge-base access for a wide range of user intents.

Mitigation: Review the skill before installing and scan the /mnt/data contents policy before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown or text responses with local file references and file-operation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may direct broad recursive searches under /mnt/data when requests are ambiguous or general.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
