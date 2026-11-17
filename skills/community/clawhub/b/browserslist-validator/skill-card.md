## Description:

Validate .browserslistrc files and browserslist config in package.json for syntax errors, deprecated browsers, redundant queries, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend engineers use this skill to validate Browserslist configuration, check browser targeting, audit frontend build configs, and lint .browserslistrc or package.json browserslist entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coverage estimates use embedded browser usage data and may be stale or approximate.

Mitigation: Treat coverage output as heuristic and confirm production browser targeting with current Browserslist data before changing support policy.

Risk: The coverage command suggests an external npx command for more accurate results.

Mitigation: Review the command and package behavior before running it in the target environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text, JSON, or one-line summary output with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes error, warning, and informational findings; strict mode can treat warnings as errors.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
