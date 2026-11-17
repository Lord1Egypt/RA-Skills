## Description:

Provides Chinese food-delivery coupon links for Meituan, Ele.me, and JD Waimai by querying Fore.vip promotion endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onsoul](https://clawhub.ai/user/onsoul)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent for Chinese food-delivery coupons or platform-specific deals and receive markdown links to current promotions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Promotion links are routed through Fore.vip and may include commercial attribution.

Mitigation: Inspect link destinations before signing in, sharing personal information, or paying on linked pages.

Risk: The external promotion endpoint can be temporarily unavailable or rate limited.

Mitigation: Retry briefly, skip failed individual links, and tell the user to try again later if no links can be retrieved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onsoul/skills/cps)
- [Fore.vip service](https://fore.vip)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown list of promotion links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 20 coupon links and may ask for a more specific platform or retry later if the endpoint is unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
