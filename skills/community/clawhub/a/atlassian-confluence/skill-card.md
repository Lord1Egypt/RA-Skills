## Description:

Read and write Confluence pages, search content, manage labels and comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pejovicvuk](https://clawhub.ai/user/pejovicvuk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to let an agent inspect Confluence Cloud spaces and pages, retrieve content, search with CQL, and make controlled updates such as creating pages, updating pages, adding comments, and managing labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs with authenticated Confluence read and write authority, including page creation, page updates, comments, and labels.

Mitigation: Use a narrowly scoped Atlassian API token and avoid high-privilege Confluence accounts.

Risk: Server security evidence flags unsafe shell argument handling and URL validation concerns.

Mitigation: Review or fix the shell script before installation, especially the python3 -c argument interpolation and URL validation paths.

Risk: Write commands can modify Confluence content.

Mitigation: Require human review of proposed creates, updates, comments, and label changes before executing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pejovicvuk/skills/atlassian-confluence)
- [Publisher profile](https://clawhub.ai/user/pejovicvuk)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ATLASSIAN_URL, ATLASSIAN_EMAIL, and ATLASSIAN_API_TOKEN; Confluence page bodies may be truncated in command output.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
