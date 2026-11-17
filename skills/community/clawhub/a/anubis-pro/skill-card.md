## Description:

Anubis Pro generates a full career application package with a tailored resume, three cover letter tones, interview preparation, follow-up emails, and an application tracker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and career coaches use this skill to turn a job description and an existing resume into a complete application package, including resume, cover letters, interview preparation, follow-up emails, and a tracker entry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume and job-description contents may contain private information and are printed during execution.

Mitigation: Run the skill only in a private, non-shared terminal and avoid retaining logs that contain resume or job-description text.

Risk: The install step uses an unpinned package install into system Python.

Mitigation: Install dependencies in a virtual environment and pin or review package versions before use.

Risk: The local license check is a simple gate rather than strong entitlement protection.

Mitigation: Treat the license key check as usability gating only and do not rely on it for sensitive authorization decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/skills/anubis-pro)
- [ClawHub metadata homepage](https://clawhub.ai/occupythemilkyway/anubis-pro)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance, Shell commands]

**Output Format:** [Markdown files and inline shell/Python command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces seven dated application documents in the configured output directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
