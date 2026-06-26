## Description: <br>
Manage Freshdesk tickets, notes, watchers, conversations, and support workflows via the Freshdesk API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support agents and operations teams use this skill to inspect Freshdesk tickets, manage notes and replies, update ticket state, manage watchers, and coordinate customer-support workflows through the connected Freshdesk account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Freshdesk credentials and OAuth tokens are used by the connected ClawLink account. <br>
Mitigation: Use only the intended Freshdesk account, keep permissions limited to the required support workflows, and avoid asking users to paste API keys into chat. <br>
Risk: Write operations can create, update, delete, or publicly reply to Freshdesk tickets. <br>
Mitigation: Preview and confirm the target ticket, message visibility, and intended effect before any write or destructive operation. <br>
Risk: Ticket visibility and action results depend on the connected agent's Freshdesk permissions. <br>
Mitigation: Verify the ticket ID and account access before acting, and report real Freshdesk permission or not-found errors without guessing. <br>


## Reference(s): <br>
- [Freshdesk Skill on ClawHub](https://clawhub.ai/hith3sh/freshdesk-support) <br>
- [Freshdesk API Documentation](https://developers.freshdesk.com/api/) <br>
- [Freshdesk Ticket API](https://developers.freshdesk.com/api/#tickets) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash commands and JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected Freshdesk account through ClawLink; write operations require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
