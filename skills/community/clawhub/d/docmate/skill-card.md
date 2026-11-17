## Description:

DocMate helps agents answer from project documentation, verify implementation-sensitive documentation against code, report documentation gaps, and optionally prepare GitHub PRs or GitLab MRs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wufei-png](https://clawhub.ai/user/wufei-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use DocMate to route questions to configured project documentation, verify stale claims against source code, and produce concise documentation gap or repair outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ClawHub package is an install notice and does not contain the runtime skill body.

Mitigation: Review the current DocMate repository and installer before making local agent-host changes.

Risk: DocMate can work with configured documentation repositories and may prepare PRs or MRs for documentation repairs.

Mitigation: Configure only intended repositories and use conservative repair modes unless automated repair proposals are acceptable.

## Reference(s):

- [Official DocMate repository](https://github.com/wufei-png/DocMate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with optional code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include documentation gap reports, repository configuration guidance, and proposed documentation repairs.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
