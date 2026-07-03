## Description: <br>
Barog helps users view booking guidance, open BeautsGO clinic pages, submit appointment requests, consult support, and check prices for Barog Hospital's Gangnam clinic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beautsgo](https://clawhub.ai/user/beautsgo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to plan or request appointments at Barog Hospital (Gangnam) through BeautsGO, including booking guidance, price lookup, support links, and appointment submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Booking details, including a phone number when provided, may be sent to BeautsGO-related external booking services. <br>
Mitigation: Review before installing, share only intended appointment details, and require clear user confirmation before each booking submission. <br>
Risk: The security scan reports embedded API tokens in the public skill artifact. <br>
Mitigation: The publisher should move API tokens out of the artifact and rotate or replace any exposed tokens before relying on the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/beautsgo/barog-clinic-booking) <br>
- [BeautsGO Barog clinic booking page](https://i.beautsgo.com/cn/hospital/barogclinic-gangnam/skill) <br>
- [BeautsGO website](https://www.beautsgo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted string with booking guidance, links, status messages, and price results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include clinic links and appointment submission status; supports Chinese and English responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, SKILL.md frontmatter, package.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
