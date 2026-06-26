## Description: <br>
Aerobase Travel Hotels helps agents search hotels, compare rates, manage bookings, handle amendments, use loyalty vouchers, and recommend layover-friendly stays. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kurosh87](https://clawhub.ai/user/kurosh87) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External travel-assistant users and agents use this skill to find airport or city hotels, prioritize layover and recovery needs, compare rates, and complete approved booking, amendment, cancellation, and loyalty voucher workflows through the Aerobase API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Booking, cancellation, amendment, rebooking, and loyalty redemption actions can affect a user's travel account or stored value. <br>
Mitigation: Require explicit user confirmation before those actions and show the cancellation policy before booking. <br>
Risk: The skill requires an Aerobase API key for hotel search and account-affecting travel actions. <br>
Mitigation: Install only when the agent may use an Aerobase API key, never print raw API keys, and redact secrets in responses. <br>
Risk: Browser-powered Pro comparison behavior is described but the scanned evidence does not clarify which third-party sites are accessed or what data is shared. <br>
Mitigation: Treat that capability as unclear unless Aerobase documents the accessed sites and data-sharing behavior. <br>


## Reference(s): <br>
- [Aerobase homepage](https://aerobase.app) <br>
- [Aerobase OpenClaw travel agent setup](https://aerobase.app/openclaw-travel-agent) <br>
- [ClawHub skill page](https://clawhub.ai/kurosh87/aerobase-travel-hotels) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown responses with Aerobase API request guidance and concise hotel recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AEROBASE_API_KEY; booking, cancellation, amendment, rebooking, and loyalty redemption actions require explicit user approval.] <br>

## Skill Version(s): <br>
3.3.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
