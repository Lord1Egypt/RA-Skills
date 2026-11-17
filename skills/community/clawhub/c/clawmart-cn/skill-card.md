## Description:

Manage a ClawMart CN store through its backend API, including registration, authentication, store profile updates, products, notes, photo uploads, and booking status changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xingke2023](https://clawhub.ai/user/xingke2023)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawMart sellers and agents assisting them use this skill to register or log in, manage store profiles, products, announcements, gallery and product photos, and booking statuses through API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens may be stored insecurely in /tmp.

Mitigation: Avoid saving tokens in /tmp; keep tokens in session memory or another user-approved secure location and clear them after use.

Risk: The skill can make business-impacting changes to seller accounts, products, notes, photos, and bookings.

Mitigation: Require explicit user confirmation before seller conversion, updates, deletes, uploads, or booking-status changes.

Risk: A wrong or untrusted API host could receive credentials or store-management requests.

Mitigation: Confirm the ClawMart API host with the user before login, uploads, or protected account operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xingke2023/skills/clawmart-cn)
- [ClawMart CN API endpoint](https://www.clawmart.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown text with curl command snippets and JSON request or response handling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform authenticated store-management actions after collecting user credentials and request details.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
