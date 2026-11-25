## Description:

Daily improvement briefings with one-click fixes for your AI agent. Observes traces, diagnoses failures, and applies fixes conversationally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pedrocarballo](https://clawhub.ai/user/pedrocarballo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to monitor AI agent performance, receive daily failure briefings, inspect recommended fixes, and apply selected repository changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs telemetry and sends agent trace data to AdeptLoop.

Mitigation: Review the telemetry scope before installation and proceed only if that data sharing is acceptable for the project.

Risk: The skill stores the AdeptLoop API key in local plaintext configuration.

Mitigation: Prefer managed secret storage or lock down local file permissions before using the skill.

Risk: The skill can schedule recurring daily checks.

Mitigation: Ask for explicit approval before scheduling and make the schedule easy to inspect or remove.

Risk: The skill can apply remotely supplied file edits and create git commits.

Mitigation: Inspect every diff, keep changes on an isolated branch, restrict edits to expected repository paths, and review commits before merging.

## Reference(s):

- [AdeptLoop homepage](https://adeptloop.com)
- [ClawHub skill page](https://clawhub.ai/pedrocarballo/skills/adeptloop-improve)
- [Publisher profile](https://clawhub.ai/user/pedrocarballo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Concise Markdown briefings with unified diffs, prompts for user decisions, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Briefings are intended to stay under 500 tokens and present one recommended fix at a time.]

## Skill Version(s):

0.1.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
