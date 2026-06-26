## Description: <br>
Execute booking/search flows via browser automation with verification artifacts. Use for reservation forms, availability checks, and capture of proof (screenshots/confirmation IDs). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[austineyapp](https://clawhub.ai/user/austineyapp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to complete reservation, booking, or availability-search workflows in a browser and return proof such as screenshots, confirmation IDs, and concise completion status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate on booking forms where accidental payment submission or final reservation changes may have real-world consequences. <br>
Mitigation: Require explicit user approval before submitting payment or finalizing any transaction. <br>
Risk: Captcha, login, or two-factor authentication can block automation or require sensitive user action. <br>
Mitigation: Stop the automated flow and request user action when captcha, login, or two-factor authentication is encountered. <br>
Risk: Booking results may be disputed or hard to audit without captured evidence. <br>
Mitigation: Preserve verification artifacts for critical steps, including page URL, key entered parameters, visible price, cancellation terms, confirmation reference, and screenshot paths. <br>


## Reference(s): <br>
- [Verification Checklist](references/verification-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown status summary with verification details and artifact paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include screenshot paths, confirmation numbers, entered booking parameters, prices, cancellation terms, and blocked or needs-user-input status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
