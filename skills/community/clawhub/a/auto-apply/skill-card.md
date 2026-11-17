## Description:

Automate job search and career management through Mokaru by searching jobs, preparing applications, tailoring resumes, tracking applications, and managing contacts and career-profile records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vndck](https://clawhub.ai/user/vndck)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search for jobs, maintain a Mokaru application tracker, tailor and export resumes, and manage career-profile data. The skill prepares application materials and provides apply links; it does not submit job applications itself.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive Mokaru account data, including resumes, work history, education, skills, applications, and contacts.

Mitigation: Install only when this account access is acceptable, keep MOKARU_API_KEY private, and review retrieved data before sharing it outside the session.

Risk: Write and delete operations can modify or remove career, resume, application, education, skill, and contact records.

Mitigation: Require the agent to show the exact record and requested change, then obtain explicit confirmation before any write or delete request.

Risk: Profile changes can affect resumes that use profile data.

Mitigation: Review profile updates carefully and confirm downstream resume impact before applying changes.

## Reference(s):

- [Mokaru API documentation](https://docs.mokaru.ai)
- [Mokaru API base URL](https://api.mokaru.ai)
- [ClawHub skill page](https://clawhub.ai/vndck/skills/auto-apply)

## Skill Output:

**Output Type(s):** [text, guidance, shell commands, configuration, markdown, files]

**Output Format:** [Markdown guidance with curl commands, JSON examples, and occasional generated files such as exported resumes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MOKARU_API_KEY plus curl and jq; API responses may include sensitive career, application, resume, profile, education, skill, and contact data.]

## Skill Version(s):

1.0.7 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
