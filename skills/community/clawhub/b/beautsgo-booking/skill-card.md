## Description: <br>
Beautsgo Booking helps agents match users to Korean dermatology and plastic surgery clinics, provide booking guidance, open clinic resources, look up prices, and submit appointment requests through BeautsGO/Yestokr services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beautsgo](https://clawhub.ai/user/beautsgo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and assistants use this skill to find Korean aesthetic clinics, compare appointment options, request prices, contact customer service, and submit booking details. <br>

### Deployment Geography for Use: <br>
Global; appointments target clinics in South Korea. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send appointment details, including clinic choice, appointment timing, party size, and contact information, to BeautsGO/Yestokr services. <br>
Mitigation: Use only when the user explicitly wants to submit a booking request and has confirmed the details to be sent. <br>
Risk: The artifact includes exposed API credentials. <br>
Mitigation: Remove or rotate exposed credentials before deployment and avoid embedding secrets in released skill files. <br>
Risk: Bundled developer scripts can have filesystem, account, publishing, or repository side effects. <br>
Mitigation: Review scripts before execution and run only the commands required for the intended workflow. <br>
Risk: Contact payloads may be logged during booking submission. <br>
Mitigation: Stop logging contact payloads and redact sensitive appointment details from diagnostics. <br>
Risk: Shell-based URL opening can be riskier than argument-based process execution. <br>
Mitigation: Replace shell-interpolated URL opening with safer argument-based process execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/beautsgo/beautsgo-booking) <br>
- [BeautsGO official site](https://beautsgo.com) <br>
- [Clinic pages](https://beautsgo.github.io/beautsgo-booking/) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill manifest](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, API calls] <br>
**Output Format:** [Markdown text with booking instructions, status messages, links, and appointment summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit appointment details to external BeautsGO/Yestokr services after collecting clinic, timing, party size, and contact information.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
