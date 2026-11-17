## Description:

Scans project dependencies for license compatibility issues across npm, pip, Go, Rust, and Ruby projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, release engineers, and compliance reviewers use this skill to audit dependency manifests before shipping or CI deployment, identify incompatible or unknown licenses, and generate reports for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unknown or high-risk license results may be mistaken for final legal clearance.

Mitigation: Treat findings as prompts for manual legal or compliance review before release.

Risk: The skill reads dependency manifests and installed package metadata from the target project.

Mitigation: Run it only against intended local project directories and review reports before sharing them.

Risk: Go, Rust, and Ruby dependencies may report unknown licenses when local package metadata is unavailable.

Mitigation: Manually verify unknown licenses from authoritative package or repository sources before relying on the report.

## Reference(s):

- [Custom License Policy](references/custom-policy.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON, or Markdown audit reports, with optional CI exit codes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CI mode exits 0 for clean results, 1 for warnings, and 2 for policy violations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
