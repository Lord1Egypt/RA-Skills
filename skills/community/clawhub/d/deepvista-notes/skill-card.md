## Description:

DeepVista Notes helps agents create, read, update, delete, and quick-capture user-managed DeepVista notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingconan](https://clawhub.ai/user/jingconan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage DeepVista note cards for explicit knowledge such as meeting notes, research, summaries, and decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, and delete stored DeepVista notes.

Mitigation: Confirm create, update, and delete actions before execution, and review note identifiers and content before changing stored notes.

Risk: Imported local files or URL content may be stored in DeepVista exactly as provided.

Mitigation: Avoid importing private local files or URL content unless the user intends the exact content to be stored in DeepVista.

Risk: The DeepVista CLI dependency is not pinned in the release metadata.

Mitigation: Prefer reviewed or pinned CLI installs when available.

## Reference(s):

- [DeepVista CLI homepage](https://cli.deepvista.ai)
- [Deepvista Notes on ClawHub](https://clawhub.ai/jingconan/skills/deepvista-notes)
- [Publisher profile](https://clawhub.ai/user/jingconan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and DeepVista note URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce DeepVista CLI commands for note list, get, create, update, delete, quick capture, and file or URL import workflows.]

## Skill Version(s):

0.1.0-alpha.21 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
