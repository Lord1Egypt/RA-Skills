## Description:

Perform 12-Factor App compliance analysis on any codebase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit SaaS and cloud-native application codebases against the 12-Factor App methodology and identify architecture gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads project files during an architecture audit and may surface sensitive-looking configuration or credential strings in its report.

Mitigation: Run it only on repositories the operator is authorized to review, and review generated findings before sharing them outside the intended audience.

## Reference(s):

- [The Twelve-Factor App](https://12factor.net)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with analysis tables, file evidence, recommendations, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports Strong, Partial, or Weak compliance for each of the twelve factors.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
