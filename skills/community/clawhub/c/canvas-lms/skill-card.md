## Description:

Access Canvas LMS (Instructure) for course data, assignments, grades, and submissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pranavkarthik10](https://clawhub.ai/user/pranavkarthik10)

### License/Terms of Use:


## Use Case:

Students, educators, and agents assisting them use this skill to retrieve Canvas course records such as due dates, grades, submissions, files, modules, announcements, discussions, and inbox messages through the Canvas REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Canvas token to access sensitive grades, files, course content, submissions, and inbox data.

Mitigation: Use a protected secret store instead of a plaintext .env file, keep the token least-privilege and revocable, and fetch only the specific Canvas records needed for the task.

Risk: Requests to an untrusted or incorrect Canvas domain could expose the token or sensitive education records.

Mitigation: Use this skill only with a Canvas domain the user trusts and has verified before sending authenticated requests.

Risk: The security verdict requires review before installation.

Mitigation: Review the skill before installing and confirm the credential-handling and privacy posture match the deployment environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with environment-variable configuration and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted Canvas base URL and a Canvas API token supplied by the user environment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
