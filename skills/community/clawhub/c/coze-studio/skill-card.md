## Description:

Provides a command-line skill branded as Coze Studio with help, status, info, and simple local data logging utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can invoke the skill's shell commands to check status and info, run placeholder functionality, and add, search, list, or export simple local entries. Reviewers should treat it as a small local utility rather than a full Coze Studio agent-development platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is advertised as a Coze Studio agent-development platform, but the inspected artifact behaves as a generic shell utility.

Mitigation: Review expected functionality before relying on it for agent development, debugging, or deployment workflows.

Risk: Commands can persist user-provided text and command history in local data files.

Mitigation: Avoid passing secrets or tokens as arguments and set COZE_STUDIO_DIR to a private trusted directory before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/skills/coze-studio)
- [Publisher profile](https://clawhub.ai/user/bytesagain-lab)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local data and command history files under COZE_STUDIO_DIR or the default user data directory.]

## Skill Version(s):

2.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
