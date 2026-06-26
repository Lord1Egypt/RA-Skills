## Description: <br>
Schedule cleanings, manage maintenance tasks, check availability, and add service professionals with TIDY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mchusma](https://clawhub.ai/user/mchusma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External property managers, Airbnb hosts, and cleaning service coordinators use this skill to schedule and manage cleaning jobs, maintenance tasks, availability checks, service professionals, and TIDY to-do lists through the TIDY API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cancel bookings and delete maintenance tasks. <br>
Mitigation: Require explicit confirmation that repeats the exact job or task ID, property, date, and requested action before allowing destructive changes. <br>
Risk: The skill uses a non-expiring TIDY account token. <br>
Mitigation: Use a dedicated or least-privilege token where available, keep it out of chat transcripts and logs, and rotate or revoke it if exposed. <br>


## Reference(s): <br>
- [TIDY Homepage](https://tidy.com) <br>
- [Cleaning And Maintenance on ClawHub](https://clawhub.ai/mchusma/cleaning-and-maintenance) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TIDY_API_TOKEN for authenticated API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
