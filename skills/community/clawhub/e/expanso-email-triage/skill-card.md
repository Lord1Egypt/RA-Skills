## Description: <br>
AI-powered email triage that categorizes messages, extracts meeting requests, drafts suggested responses, and can sync calendar events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and agents use this skill to triage Gmail, Outlook, or IMAP inboxes by classifying messages, prioritizing action items, extracting meeting requests, and preparing draft responses. It can be run as a CLI pipeline or exposed through an MCP-style HTTP endpoint for inbox triage workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email subjects, senders, and body excerpts may be sent to OpenAI for classification and drafting. <br>
Mitigation: Use least-privilege credentials, limit runs to appropriate folders and message counts, avoid sensitive mailboxes, or choose a local backend when privacy requirements demand it. <br>
Risk: Calendar creation or archive behavior can modify connected accounts if enabled. <br>
Mitigation: Disable automatic archive behavior and manually review calendar-event creation before allowing the workflow to modify email or calendar accounts. <br>
Risk: The MCP HTTP pipeline may expose inbox triage capabilities if bound broadly or left unauthenticated. <br>
Mitigation: Bind the MCP server to localhost or protect it behind authentication before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aronchick/expanso-email-triage) <br>
- [Publisher profile](https://clawhub.ai/user/aronchick) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [skill.yaml](artifact/skill.yaml) <br>
- [pipeline-cli.yaml](artifact/pipeline-cli.yaml) <br>
- [pipeline-mcp.yaml](artifact/pipeline-mcp.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, guidance] <br>
**Output Format:** [JSON objects containing a triage summary, categorized email records, extracted calendar events, draft responses, and processing metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI mode writes JSON to stdout; MCP mode returns a synchronous response. Email content may be included in processing outputs and model prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
