## Description:

Chou Fei helps agents simulate external resource fetching, extract key information from text, and allocate local compute based on task priority and system load.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lt8899789](https://clawhub.ai/user/lt8899789)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Chou Fei to add Chinese-language resource intake, text information extraction, and lightweight compute-allocation guidance to agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake simulated fetch or search behavior for real retrieval.

Mitigation: Label these outputs as simulated and verify any cited or retrieved information before use.

Risk: Future changes that add real URL, API, or file retrieval could send sensitive content externally.

Mitigation: Add destination limits and user confirmation before enabling real external retrieval.

Risk: The skill uses a Chinese-language interface that may not fit all deployment teams.

Mitigation: Confirm localization expectations before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lt8899789/skills/chou-fei)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON objects and streamed text, with optional CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetch behavior is simulated; text extraction and compute allocation use lightweight local heuristics.]

## Skill Version(s):

1.0.35 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
