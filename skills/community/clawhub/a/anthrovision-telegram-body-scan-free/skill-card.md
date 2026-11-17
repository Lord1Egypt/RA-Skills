## Description: <br>
Automates basic body scanning and measurement by submitting a user-provided video through Telegram and returning measurement results after polling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit authorized single-person body videos for basic chest, waist, and hip measurements. It is suited to fitness tracking or sizing workflows that can tolerate asynchronous Telegram-based processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive real-person body videos may be processed through Telegram or an external service. <br>
Mitigation: Use only self-provided or clearly authorized videos, and confirm privacy, retention, and deletion practices before deployment. <br>
Risk: Consent safeguards are under-scoped for a body-measurement workflow. <br>
Mitigation: Add explicit consent checks and narrow trigger conditions before using the skill in shared or customer-facing environments. <br>


## Reference(s): <br>
- [AnthroVision Telegram Body Scan Free homepage](https://www.anthrovision.com/telegram-body-scan-free) <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/anthrovision-telegram-body-scan-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or structured text containing validation guidance, scan status, and basic measurement values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include scan identifiers, processing status, and basic body measurements; no medical or health interpretation is claimed.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
