## Description: <br>
Deer helps users view booking guidance, submit appointment requests, contact online support, and check prices for Lumiin Dermatology through BeautsGO. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beautsgo](https://clawhub.ai/user/beautsgo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External patients and clinic customers use Deer to get booking guidance, submit appointment details, open BeautsGO consultation pages, and check treatment prices for Lumiin Dermatology in Seoul. <br>

### Deployment Geography for Use: <br>
Global; service destination is Seoul, South Korea. <br>

## Known Risks and Mitigations: <br>
Risk: Appointment details, including a phone number when provided, can be sent to the BeautsGO booking service without a clear in-flow confirmation step. <br>
Mitigation: Provide contact information only when booking follow-up is intended, and require an explicit confirmation step before submitting appointment data. <br>
Risk: Service API tokens are embedded in the skill artifact. <br>
Mitigation: Remove hardcoded tokens, rotate exposed credentials, and load service credentials from a managed secret store before deployment. <br>
Risk: The skill relies on external BeautsGO, yestokr.com, and beise.com network services for booking, consultation, and price workflows. <br>
Mitigation: Deploy only in environments where those external calls are acceptable, and review allowed domains and data-sharing expectations before installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/beautsgo/deer-clinic-booking) <br>
- [BeautsGO Publisher Profile](https://clawhub.ai/user/beautsgo) <br>
- [Lumiin Dermatology Booking Page](https://i.beautsgo.com/cn/hospital/lumiin-dermatology/skill) <br>
- [Lumiin Dermatology BeautsGO Profile](https://i.beautsgo.com/cn/hospital/lumiin-dermatology?from=skill) <br>
- [BeautsGO Website](https://www.beautsgo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open BeautsGO web pages and call external booking or price APIs when the user requests those actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, skill.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
