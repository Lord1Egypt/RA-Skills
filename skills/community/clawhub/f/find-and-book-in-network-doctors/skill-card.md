## Description: <br>
This skill helps agents find and book in-network doctors through Zocdoc.com with verified reviews, real-time availability, insurance confirmation, and direct booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylemorgan-commits](https://clawhub.ai/user/kylemorgan-commits) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search for doctors by specialty, condition, insurance, location, appointment preference, visit type, and language preference, then review provider details and continue to Zocdoc.com to complete scheduling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Doctor searches can involve sensitive condition, insurance, and location details. <br>
Mitigation: Provide only the information needed for the search and avoid adding unnecessary personal health details. <br>
Risk: Provider availability, insurance acceptance, privacy terms, and appointment details may change before booking. <br>
Mitigation: Confirm provider, insurance, privacy, and appointment details directly on Zocdoc.com before completing scheduling. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/kylemorgan-commits/find-and-book-in-network-doctors) <br>
- [Zocdoc](https://www.zocdoc.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured provider list with summaries and direct booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provider results may include name, specialty, accepted insurance confirmation, location, verified review summary, next available appointment slots, and a direct Zocdoc.com booking link.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
