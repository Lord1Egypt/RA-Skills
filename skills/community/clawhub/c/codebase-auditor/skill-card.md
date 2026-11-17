## Description:

Scans a project directory and generates a JSON inventory of key configuration and credential-related files for backup planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ink5725](https://clawhub.ai/user/ink5725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before deployment or migration to inventory important environment, credential, configuration, CI/CD, and database-related file paths for backup planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated inventory can reveal sensitive file locations such as .env files, private-key filenames, and service-account filenames.

Mitigation: Keep the generated JSON private, choose the project directory deliberately, and avoid sharing the inventory with untrusted tools or people.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ink5725/skills/codebase-auditor)

## Skill Output:

**Output Type(s):** [text, configuration]

**Output Format:** [JSON file with console text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes file_inventory.json containing project path, scan timestamp, counts, and discovered file path metadata; it does not include file contents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
