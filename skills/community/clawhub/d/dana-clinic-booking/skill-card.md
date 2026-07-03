## Description: <br>
Dana helps users view booking guidance, consult customer service, query prices, and submit appointment requests for DAN-A Clinic in Seoul through BeautsGO. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beautsgo](https://clawhub.ai/user/beautsgo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users seeking dermatology or cosmetic clinic appointments use this skill to get booking guidance, open BeautsGO pages, query prices, and submit appointment details for DAN-A Clinic. <br>

### Deployment Geography for Use: <br>
Global, for bookings with DAN-A Clinic in Seoul, South Korea. <br>

## Known Risks and Mitigations: <br>
Risk: Appointment timing, party size, and any phone number provided may be sent to an external BeautsGO booking API. <br>
Mitigation: Use only with informed user consent and avoid entering real contact details unless the user is comfortable with BeautsGO receiving them. <br>
Risk: Booking submission can occur without a separate in-flow confirmation step after appointment details are parsed. <br>
Mitigation: Review parsed appointment details before real use and prefer a future version that requires explicit confirmation before API submission. <br>
Risk: The distributed package includes hardcoded API tokens. <br>
Mitigation: Prefer a version that moves tokens into a secret store or server-side integration before production deployment. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/beautsgo/dana-clinic-booking) <br>
- [DAN-A Clinic BeautsGO booking page](https://i.beautsgo.com/cn/hospital/dan-a-clinic/skill) <br>
- [DAN-A Clinic BeautsGO details page](https://i.beautsgo.com/cn/hospital/dan-a-clinic?from=skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted string with links and booking, consultation, price, or error status messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open whitelisted BeautsGO URLs and submit appointment or price API requests when the matching user intent is detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, skill.json, and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
