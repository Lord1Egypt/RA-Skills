## Description:

Helps an agent plan, draft, quality-check, and publish Chinese web-novel chapters to FireSeed through HTTP APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanzhishuyuan](https://clawhub.ai/user/sanzhishuyuan)

### License/Terms of Use:

MIT-0

## Use Case:

Authors and publishing agents use this skill to turn a novel premise into structured chapters, manage FireSeed works, and publish content after self-checks. It is suited for users who intentionally authorize an agent to create or update public FireSeed content on their behalf.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or modify public FireSeed content with broad automation.

Mitigation: Use it only when the user explicitly wants agent-assisted publishing, and review planned account, novel, chapter, and task actions before execution.

Risk: Credential handling is required for FireSeed account and token operations.

Mitigation: Prefer a limited API token in the Authorization header, avoid sharing raw passwords in chat, and do not pass tokens in URL parameters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sanzhishuyuan/skills/fireseed-auto-novel-publish)
- [Server-Resolved GitHub Repository](https://github.com/sanzhishuyuan/fireseed-auto-novel-publish)
- [FireSeed Platform](https://fireseed.online)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown prose with HTTP API request details and publishing status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update FireSeed novels and chapters when supplied with valid user authorization.]

## Skill Version(s):

2.3.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
