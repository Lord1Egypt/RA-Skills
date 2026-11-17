## Description:

Identify and defend against AI-powered scams including deepfakes, voice cloning, AI phishing, and fake job offers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support agents use this skill to identify suspected AI-enabled fraud, prioritize immediate recovery steps, and guide reporting or account-protection actions after suspicious calls, video calls, emails, job offers, romance contacts, or investment pitches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle sensitive fraud-victim information, including financial loss, identity theft, police reports, payment methods, scammer contacts, and exposed personal details.

Mitigation: Use it only where persistent memory is private and controllable, and avoid storing report numbers, bank details, payment methods, scammer contacts, or exposed personal information unless the user knowingly opts in and can delete it later.

Risk: The artifact includes agent-state persistence and follow-up triggers for recovery actions without clear consent, retention, or deletion controls.

Mitigation: Before persisting recovery state or scheduling follow-ups, get explicit user consent, keep only minimal non-sensitive status fields, and provide a clear way to review or delete stored details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/howtousehumans/skills/ai-scam-defense)
- [FTC Fraud Reporting](https://reportfraud.ftc.gov/)
- [FBI Internet Crime Complaint Center](https://www.ic3.gov/)
- [FTC IdentityTheft.gov](https://www.identitytheft.gov/)
- [FDIC Consumer Resources](https://www.fdic.gov/resources/consumers/)
- [CFPB Consumer Complaint](https://www.consumerfinance.gov/complaint/)
- [FINRA BrokerCheck](https://brokercheck.finra.org/)
- [SEC EDGAR Database](https://www.sec.gov/cgi-bin/browse-edgar)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown guidance with checklists, verification protocols, recovery steps, and optional agent-state configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include jurisdiction-specific reporting guidance and follow-up reminders based on user-provided scam details.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
