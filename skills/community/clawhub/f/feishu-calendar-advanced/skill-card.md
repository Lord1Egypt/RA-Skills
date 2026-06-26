## Description: <br>
Feishu calendar management via feishu-agent. View calendars, list events, create and delete events with conflict detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boyd4y](https://clawhub.ai/user/boyd4y) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to configure Feishu calendar access and manage calendars or events through the feishu-agent CLI, including listing calendars, listing events, creating events with attendees, and deleting events by ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an external CLI package to access Feishu calendar data and perform calendar actions. <br>
Mitigation: Install only after trusting or reviewing @teamclaw/feishu-agent, and consider pinning the package version before use. <br>
Risk: Calendar create and delete actions can affect real Feishu calendar records. <br>
Mitigation: Verify event titles, times, attendees, calendar targets, and event IDs before running create or delete actions. <br>
Risk: Feishu OAuth credentials and app permissions may grant broader calendar access than needed. <br>
Mitigation: Use least-privileged Feishu app scopes where possible and reauthorize only through the documented Feishu OAuth flow. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bun and the external @teamclaw/feishu-agent CLI with Feishu OAuth authorization.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
