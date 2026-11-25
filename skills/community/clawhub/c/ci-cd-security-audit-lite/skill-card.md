## Description:

Lint a single GitHub Actions workflow file for the top supply-chain risks — unpinned actions, pull_request_target, secrets echoed in run steps, overly broad permissions. Local file only. Use when the user asks to check a workflow's security.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CI maintainers use this skill to lint one supplied GitHub Actions workflow for common supply-chain risks and receive actionable findings with line numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious and flags an undisclosed external submission of feedback; its scan was partial and does not establish that the skill is safe.

Mitigation: Review the feedback handling and directory access described by the scan before use, and avoid sensitive workflows until you are comfortable with those behaviors.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [JSON report on stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports line numbers without echoing matched secret values. It checks one workflow against a limited set of rules; zero findings do not establish that a pipeline is secure.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
