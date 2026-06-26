## Description: <br>
AI meeting partner for solopreneurs and professionals that generates pre-meeting briefs from notes and context, captures structured meeting notes during conversations, and produces action item summaries with owners and deadlines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Clawdssen](https://clawhub.ai/user/Clawdssen) <br>

### License/Terms of Use: <br>
CC-BY-NC-4.0 <br>


## Use Case: <br>
Solopreneurs, professionals, and teams use this skill to prepare for meetings, capture structured notes, extract action items, and maintain local meeting records for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting notes and action items may contain sensitive business or personal information stored in local workspace files. <br>
Mitigation: Use the skill only in workspaces where local meeting records are acceptable, sanitize sensitive meetings before content-generation workflows, and protect the meetings folder according to the user's confidentiality needs. <br>
Risk: Follow-up drafts, investor updates, or newsletter outputs may include incorrect or overly broad summaries of private discussions. <br>
Mitigation: Manually review all outbound drafts and derived content before sharing, and do not send messages automatically. <br>
Risk: Standing AGENTS.md or HEARTBEAT.md additions can change how the agent records meetings and checks overdue actions. <br>
Mitigation: Review any standing-instruction additions before enabling them and keep only the workflows that match the user's meeting process. <br>


## Reference(s): <br>
- [Meeting Assistant ClawHub Page](https://clawhub.ai/Clawdssen/agentledger-meeting-assistant) <br>
- [advanced-patterns.md](references/advanced-patterns.md) <br>
- [The Agent Ledger](https://theagentledger.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, checklists, structured sections, and occasional bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local workspace meeting logs, open-action lists, archives, and follow-up drafts when requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
