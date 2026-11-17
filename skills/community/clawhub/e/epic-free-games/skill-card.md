## Description:

Auto-claims free games from Epic Games Store using agent-browser with persistent login state and an automated checkout flow.

This skill is for research and development only.

## Publisher:

[anlinxi](https://clawhub.ai/user/anlinxi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run or adapt an automated Epic Games Store free-game claiming workflow after completing manual login and any required human verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores reusable Epic login state locally.

Mitigation: Protect or delete epic_auth.json, avoid sharing it, and add it to .gitignore before using version control.

Risk: The skill can automatically complete Epic Games Store checkout actions.

Mitigation: Review the source first and require explicit confirmation plus zero-price verification before any order is submitted.

Risk: The skill includes guidance related to Cloudflare automation detection.

Mitigation: Prefer manual verification handling and remove anti-detection guidance before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anlinxi/skills/epic-free-games)
- [agent-browser](https://github.com/vercel-labs/agent-browser)
- [Epic Games Store free games page](https://store.epicgames.com/zh-CN/free-games)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and console status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate a local epic_auth.json authentication-state file when login state is saved.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
