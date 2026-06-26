## Description: <br>
Interact with the Atoll project management API for managing tasks, projects, goals, KPIs, initiatives, milestones, comments, members, teams, labels, dependencies, automation, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doubledipcode](https://clawhub.ai/user/doubledipcode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agents use this skill to read and update Atoll workspaces, manage issues and strategy objects, and build Atoll integrations through the CLI or REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authorized API or CLI actions can modify Atoll workspace records. <br>
Mitigation: Use read-only orientation first, confirm the org/profile before writes, and keep destructive actions manual or explicitly confirmed. <br>
Risk: API keys, cookies, private business data, or third-party secrets could be exposed through prompts, comments, draft files, or issue descriptions. <br>
Mitigation: Use narrowly scoped keys, avoid placing secrets or private data in agent-visible text, and use secret references for KPI HTTP sync drafts. <br>
Risk: Recurring heartbeat or automation checks could repeatedly act on workspace data. <br>
Mitigation: Run recurring checks only when explicitly requested and confirm any resulting write action before execution. <br>


## Reference(s): <br>
- [Atoll homepage](https://atollhq.com) <br>
- [Atoll API Endpoint Reference](references/api-endpoints.md) <br>
- [Atoll API Field Reference](references/api-fields.md) <br>
- [ClawHub release page](https://clawhub.ai/doubledipcode/atoll-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown, code] <br>
**Output Format:** [Markdown guidance with shell commands, JSON examples, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ATOLL_API_KEY, ATOLL_ORG_ID, curl, and the Atoll CLI when available.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
