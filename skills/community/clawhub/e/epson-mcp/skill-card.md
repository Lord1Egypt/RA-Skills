## Description: <br>
Print, scan, copy, and job control for the Epson WF-2250 and other network-attached Epson inkjets via MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earlvanze](https://clawhub.ai/user/earlvanze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent diagnose a network-attached Epson printer, submit text, file, or raw print jobs, and manage Windows spooler jobs through an MCP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent access can control a real printer, including raw print payloads and job cancellation. <br>
Mitigation: Install only for trusted users, require explicit confirmation before printing or canceling jobs, and restrict cancellation to exact user-provided job IDs. <br>
Risk: The MCP endpoint grants printer-control authority wherever it is configured. <br>
Mitigation: Keep the endpoint private, use the bearer-token environment variable described by the skill, and limit access to intended Tailnet users. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/earlvanze/epson-mcp) <br>
- [Epson MCP Endpoint](https://cyber.talpa-stargazer.ts.net/epson/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, shell commands, configuration] <br>
**Output Format:** [MCP tool responses and Markdown setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return printer diagnostics, status summaries, job lists, and action results from the configured MCP endpoint.] <br>

## Skill Version(s): <br>
0.2.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
