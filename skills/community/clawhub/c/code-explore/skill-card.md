## Description:

Analyzes a local codebase to explain its directory structure, entrypoints, dependencies, call chains, and data flow without modifying code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sf0799](https://clawhub.ai/user/sf0799)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to understand an unfamiliar or changing codebase, including project structure, key entrypoints, module responsibilities, call relationships, and data flow. It is intended for read-only exploration before deciding whether code changes are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects files in the current codebase to explain structure and data flow.

Mitigation: Use it only in workspaces where read-only code inspection is permitted, and review conclusions against the files the agent cites.

Risk: Analysis can be incomplete when relevant files have not been read.

Mitigation: Require the agent to mark unconfirmed areas as uncertain and base conclusions only on inspected files.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis with concise lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only project exploration; the skill does not request code edits, persistent components, or network use.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
