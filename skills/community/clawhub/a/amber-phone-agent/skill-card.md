## Description: <br>
Amber gives OpenClaw agents phone capabilities for inbound answering, call screening, confirmed scheduling, optional outbound calling, and phone-task workflows configured through a short setup wizard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[batthis](https://clawhub.ai/user/batthis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Amber to add phone workflows to OpenClaw or MCP-capable agents, including call screening, confirmed scheduling, call history, CRM lookup, contacts lookup, and prepared outbound calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Amber handles sensitive communications and can retain or enrich caller data through call logs, transcripts, CRM records, calendar access, contacts lookup, and MCP tools. <br>
Mitigation: Operate it as a sensitive communications system: disclose AI call handling and logging where required, set retention and deletion practices, review or correct CRM data, and limit Apple Contacts export to names and phone numbers unless extra fields are needed. <br>
Risk: Provider credentials, webhook secrets, local runtime files, and local dashboards can expose phone, transcript, CRM, calendar, contacts, or account access if mishandled. <br>
Mitigation: Use dedicated Twilio and OpenAI credentials, protect runtime/.env, rotate secrets as needed, keep bridge/dashboard/MCP access restricted to trusted local users, and review dependency or configuration changes before deployment. <br>
Risk: Outbound calling and calendar updates can affect external people or operator commitments. <br>
Mitigation: Keep code-enforced confirmation gates enabled, use operator approval for outbound calls, require explicit confirmation before calendar writes, and escalate payment or financial-commitment requests to the human operator. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/batthis/amber-phone-agent) <br>
- [Publisher Profile](https://clawhub.ai/user/batthis) <br>
- [Source Homepage](https://github.com/batthis/amber-openclaw-voice-agent) <br>
- [Amber Skill Documentation](SKILL.md) <br>
- [Runtime Bridge Documentation](runtime/README.md) <br>
- [Architecture Notes](references/architecture.md) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Interactive Setup Demo](https://asciinema.org/a/l1nOHktunybwAheQ) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce setup steps, runtime configuration guidance, MCP tool usage guidance, and local operational notes for phone, CRM, calendar, contacts, and call-history workflows.] <br>

## Skill Version(s): <br>
5.5.39 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
