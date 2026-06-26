## Description: <br>
Ruofan Bargain Arena helps users join Ruofan's bargain event and negotiate with Ruofan's shop assistant for a dedicated discount code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruffood](https://clawhub.ai/user/ruffood) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to participate in Ruofan's public bargain event, relay their chosen messages to the Ruofan service, track remaining rounds and offers, and receive any resulting discount code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outbound API calls send the user's nickname and bargain messages to the Ruofan service, and the artifact notes that bargain conversations may be publicly displayed on Ruofan's activity page. <br>
Mitigation: Ask for the user's nickname before joining, avoid sending sensitive personal information, and review the message content before relaying it to the service. <br>
Risk: The skill can surface coupon codes and commercial offer details returned by the Ruofan service. <br>
Mitigation: Display returned coupon details clearly to the user and avoid sending further bargain messages after the service reports a deal or no-deal terminal status. <br>
Risk: Server security evidence reports no artifact-backed malicious or materially suspicious behavior, but still recommends review before running actions. <br>
Mitigation: Review the network calls and user-visible messages before use, especially when running the included shell command examples. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ruffood/bargins) <br>
- [Publisher Profile](https://clawhub.ai/user/ruffood) <br>
- [Ruofan Bargain Join API](https://www.ruffood.com/api/bargain/join) <br>
- [Ruofan Bargain Message API](https://www.ruffood.com/api/bargain/message) <br>
- [Ruofan Bargain Session API](https://www.ruffood.com/api/bargain/session) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with API response summaries and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May display discount amounts, session status, remaining rounds, and coupon codes returned by the Ruofan service.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
