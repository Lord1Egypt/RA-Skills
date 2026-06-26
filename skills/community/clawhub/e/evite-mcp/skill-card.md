## Description: <br>
This skill connects an agent to an Evite MCP server to read and manage Evite events, guest lists, RSVPs, messages, and event authoring actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they intentionally want an agent to access their Evite account to inspect invitations, RSVP information, guest lists, messages, and host-side event workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording could cause generic invitation, RSVP, guest list, or party-hosting requests to route into an authenticated Evite tool. <br>
Mitigation: Use the skill only for explicit Evite requests and confirm that the user intends Evite account access before invoking tools. <br>
Risk: The skill can require sensitive Evite credentials or session cookies. <br>
Mitigation: Prefer email and password authentication when appropriate, avoid raw session cookies unless necessary, and limit installation to environments where Evite account access is intended. <br>
Risk: Write actions can message guests, send invites, edit events, cancel events, or change RSVP and guest data. <br>
Mitigation: Review dry-run previews carefully and set confirm: true only after the requested action and affected event or guests are clear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/evite-mcp) <br>
- [Evite](https://www.evite.com) <br>
- [evite-mcp npm package](https://www.npmjs.com/package/evite-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, API calls] <br>
**Output Format:** [Markdown with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require Evite credentials or session state and uses confirm-gated write actions with dry-run previews by default.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
