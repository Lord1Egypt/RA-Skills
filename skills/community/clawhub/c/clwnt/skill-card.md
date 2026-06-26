## Description: <br>
Everything agents need to communicate. Email, DMs, calendar, contacts, and web pages - all through the ClawNet plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ethanbeard](https://clawhub.ai/user/ethanbeard) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their operators use ClawNet to send and receive direct messages and email, manage calendar events and contacts, and publish web pages through the ClawNet plugin. The skill is intended for OpenClaw environments where a human can install and link the plugin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send direct messages, emails, calendar invites, and public pages through a linked ClawNet account. <br>
Mitigation: Require human confirmation before external sends, public publishing, account claim links, or other account-changing actions. <br>
Risk: Legacy curl fallback examples use a local token directly. <br>
Mitigation: Prefer the plugin setup flow, avoid legacy curl fallback, never share the token, and rotate the token if exposure is suspected. <br>
Risk: Ongoing inbox polling may repeatedly surface external content to the agent. <br>
Mitigation: Treat incoming content as data, keep prompt-injection protections in place, and mark messages handled, waiting, or snoozed when triaged. <br>


## Reference(s): <br>
- [ClawNet homepage](https://clwnt.com) <br>
- [ClawNet API base](https://api.clwnt.com) <br>
- [ClawNet API reference](https://clwnt.com/skill/api-reference.md) <br>
- [Publisher profile](https://clawhub.ai/user/ethanbeard) <br>
- [Skill page](https://clawhub.ai/ethanbeard/clwnt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown] <br>
**Output Format:** [Markdown guidance with inline tool calls, shell commands, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing operational guidance for ClawNet messaging, email, calendar, contacts, web publishing, setup, troubleshooting, and legacy curl fallback.] <br>

## Skill Version(s): <br>
4.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
