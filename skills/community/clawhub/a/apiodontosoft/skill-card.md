## Description: <br>
Manages Odontosoft dental appointments by listing dentists, checking available slots, finding patients by document number, and booking appointments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jschussmuller](https://clawhub.ai/user/jschussmuller) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinic staff and authorized systems use this skill to look up active dentists, find appointment slots, locate patient records by document number, and create dental appointments in Odontosoft after confirming details with the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle sensitive patient and appointment details. <br>
Mitigation: Install only for authorized clinic staff or systems and avoid logging document numbers or appointment details. <br>
Risk: A broad or exposed Odontosoft token could allow unauthorized clinic data access or scheduling actions. <br>
Mitigation: Use a least-privileged Odontosoft token and store it through the agent platform's secret mechanism. <br>
Risk: Incorrect patient, dentist, date, or time values could create an unintended appointment. <br>
Mitigation: Confirm patient and appointment details with the user before calling the booking tool. <br>
Risk: A misconfigured base URL could send requests to the wrong service. <br>
Mitigation: Keep the base URL set to the intended HTTPS Odontosoft service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jschussmuller/apiodontosoft) <br>
- [README.md](README.md) <br>
- [manifest.json](manifest.json) <br>
- [Odontosoft API endpoint](https://api.odontosoft.com.py) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON API responses with concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured ODONTOSOFT_BASE_URL and ODONTOSOFT_TOKEN.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
