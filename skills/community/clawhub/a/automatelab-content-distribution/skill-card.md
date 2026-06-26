## Description: <br>
Use when the user wants to publish a post, article, or announcement to multiple platforms at once, with platform-specific format adaptation, idempotent re-publish, per-community anti-spam rules, and scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[automatelab](https://clawhub.ai/user/automatelab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to prepare, publish, schedule, and check multi-platform posts through the Content Distribution MCP server. It is intended for workflows that need channel-specific copy, account-aware targeting, idempotent retries, and status tracking across publishing services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or schedule public content through real connected accounts. <br>
Mitigation: Confirm the exact platforms, account identities, community targets, timing, and final text before any distribute or schedule action. <br>
Risk: The skill requires OAuth tokens or other sensitive publishing credentials. <br>
Mitigation: Install only when connecting real publishing accounts is intended and verify credential status before attempting a live publish. <br>
Risk: Incorrect channel targeting or copy may violate platform or community rules. <br>
Mitigation: Use channel hints for limits, cooldowns, flair options, tag vocabularies, and formatting rules before drafting or posting variants. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/automatelab/automatelab-content-distribution) <br>
- [Project homepage](https://github.com/AutomateLab-tech/content-distribution-mcp) <br>
- [Configuration README](https://github.com/AutomateLab-tech/content-distribution-mcp#configuration) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets, platform-specific post copy, and MCP tool-call parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include channel-specific variants, scheduling details, distribution IDs, and status-check guidance.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
