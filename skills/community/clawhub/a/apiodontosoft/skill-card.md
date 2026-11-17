## Description:

Api Odontosoft manages dental appointments in Odontosoft by listing active dentists, checking available appointment slots, finding patients by document number, and booking dental visits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jschussmuller](https://clawhub.ai/user/jschussmuller)

### License/Terms of Use:

MIT-0

## Use Case:

Clinic staff and authorized agents use this skill to check dentists and open slots, identify existing patients by document number, and book dental appointments in Odontosoft after confirming the details with the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles patient identifiers and appointment details.

Mitigation: Use it only with authorized users and ensure clinic logging and privacy controls cover patient lookup and appointment booking data.

Risk: A configurable API destination can send sensitive requests to an unintended host.

Mitigation: Configure only the official HTTPS Odontosoft API host before installing in a real clinic environment.

Risk: The skill depends on an Odontosoft bearer token.

Mitigation: Use a least-privileged token, store it as a secret, and rotate it according to clinic policy.

## Reference(s):

- [ClawHub Api Odontosoft skill page](https://clawhub.ai/jschussmuller/skills/apiodontosoft)
- [Odontosoft API host](https://api.odontosoft.com.py)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured JSON responses or error objects returned from Odontosoft API operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ODONTOSOFT_BASE_URL and ODONTOSOFT_TOKEN configuration before use.]

## Skill Version(s):

1.0.3 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
