## Description:

Dataview provides Bash commands for recording, viewing, searching, and exporting local logs of data-operation activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use Dataview as a lightweight local tracker for data inspection and processing notes. It should not be treated as a full CSV or JSON query engine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-entered data-operation notes may be stored in plaintext local logs and included in later searches or exports.

Mitigation: Do not enter secrets, proprietary data snippets, or sensitive queries unless plaintext local storage under ~/.local/share/dataview is acceptable.

Risk: The release is presented as CSV and JSON exploration, but the security evidence says the artifact behaves as a persistent local activity logger.

Mitigation: Use this skill only for activity logging and verify any real data analysis with a dedicated CSV or JSON parser or query tool.

## Reference(s):

- [Dataview ClawHub Skill Page](https://clawhub.ai/bytesagain-lab/skills/dataview)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Plain text CLI output and local JSON, CSV, or text export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists command entries and history under ~/.local/share/dataview when commands are run.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
