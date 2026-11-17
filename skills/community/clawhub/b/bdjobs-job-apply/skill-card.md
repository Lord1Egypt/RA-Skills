## Description:

BDJobs job search, matching, applying, undoing, and salary-update automation for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sazidulalam47](https://clawhub.ai/user/sazidulalam47)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to manage BDJobs searches, compare openings against a resume and preferences, apply to selected jobs, cancel applications, and update expected salary through OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: BDJobs credentials and session tokens may be stored locally and printed in command output.

Mitigation: Run only in a private environment with restricted file access and command logs, and rotate or remove stored credentials and tokens after use.

Risk: Apply, cancel, and salary-update scripts can make live changes to a BDJobs account.

Mitigation: Review each target job, cancellation, and salary value before executing live action scripts.

Risk: Resume and profile details are transmitted to BDJobs-related APIs during login, search, apply, and account-management flows.

Mitigation: Use the skill only when the user accepts transmission of this data to those services.

## Reference(s):

- [BDJobs API Reference](artifact/references/api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands, JSON file updates, and BDJobs API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local JSON and Markdown files under the skill data directory.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
