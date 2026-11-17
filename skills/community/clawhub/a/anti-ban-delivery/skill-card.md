## Description:

Three-layer anti-ban protection for personal Zalo automation including Token Bucket rate limiting, Self-Echo Shield, and Inbound Flood Detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aizaloapp](https://clawhub.ai/user/aizaloapp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill for guidance on Zalo messaging safeguards and to check the documented Zalo-Flow status endpoint. The skill alone does not enforce these safeguards or guarantee account safety.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented rate limits, echo shield, and flood detector may not be active in a user's deployment, so the skill cannot guarantee account safety.

Mitigation: Verify the safeguards in the actual Zalo-Flow deployment before relying on them.

Risk: The release requires a ZALO_FLOW_PAT, but the example status request uses a demo bearer token and does not explain the personal access token's use.

Mitigation: Clarify why the token is needed before providing it, and avoid sending credentials in the example request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aizaloapp/skills/anti-ban-delivery)
- [Publisher profile](https://clawhub.ai/user/aizaloapp)
- [Zalo-Flow official website](https://aizalo.com)
- [Anti-Ban Engineering Guide](https://aizalo.com/blog/cach-gui-tin-nhan-tu-dong-tren-zalo-khong-bi-khoa)
- [Multi-Account Browser Isolation](https://aizalo.com/blog/cach-dang-nhap-nhieu-tai-khoan-zalo-tren-may-tinh)
- [Zalo-Flow RapidAPI Playground](https://rapidapi.com/lekhoa288/api/zalo-flow-personal-zalo-chatbot-and-crm)
- [Zalo-Flow GitHub repository](https://github.com/aizaloapp/zalo-flow)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes messaging safeguards and a status-check command; it does not implement or enforce the safeguards.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
