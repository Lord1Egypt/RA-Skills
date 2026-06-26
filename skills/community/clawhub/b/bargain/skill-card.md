## Description: <br>
Ruofan Bargain Arena helps an agent guide users through Ruofan's coupon-bargaining activity by joining a session, relaying bargain messages, and presenting any resulting coupon code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruffood](https://clawhub.ai/user/ruffood) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to participate in Ruofan's bargain activity, send their chosen messages to Ruofan's AI shopkeeper, and receive the current offer, remaining rounds, deal status, and any coupon code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The user's nickname and bargain messages are sent to Ruofan and may be shown publicly on the activity page. <br>
Mitigation: Use a non-sensitive nickname and only send bargain messages the user is comfortable sharing with Ruofan and potentially displaying publicly. <br>
Risk: The session token and coupon code are specific to the user's bargain session. <br>
Mitigation: Treat the session token and any returned coupon code as session-specific values and avoid sharing them beyond the intended checkout flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ruffood/bargain) <br>
- [Ruofan bargain join API](https://www.ruffood.com/api/bargain/join) <br>
- [Ruofan bargain message API](https://www.ruffood.com/api/bargain/message) <br>
- [Ruofan bargain session API](https://www.ruffood.com/api/bargain/session) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with API request examples and user-facing bargain status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include session status, remaining rounds, offer amount, coupon amount, coupon code, or coupon availability message returned by Ruofan.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
