## Description: <br>
Manage a ClawMart CN store through its backend API, including account registration, login, store profile updates, products, announcements, bookings, and photo uploads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xingke2023](https://clawhub.ai/user/xingke2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ClawMart sellers use this skill to operate a live store from an agent workflow. It helps them authenticate, maintain store details, manage products and announcements, handle bookings, and upload store or product images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live business changes to a ClawMart seller account, including product edits, deletes, announcements, photo changes, and booking status updates. <br>
Mitigation: Confirm destructive actions and booking-status changes with the user before execution, and show returned IDs or names after changes complete. <br>
Risk: The skill handles login credentials and bearer tokens, and may store a token in /tmp/clawmart_token.txt. <br>
Mitigation: Confirm the API URL before login, avoid credential reuse on self-hosted endpoints the user does not control, and delete /tmp/clawmart_token.txt when finished or after authentication failures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xingke2023/clawmart-cn) <br>
- [ClawMart API base URL](https://www.clawmart.cn/api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated workflows may store a bearer token in /tmp/clawmart_token.txt for reuse.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
