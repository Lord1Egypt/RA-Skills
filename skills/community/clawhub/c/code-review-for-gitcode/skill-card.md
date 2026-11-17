## Description:

Complete code review workflow for GitCode PRs. Combines automated security scanning with manual code review, outputs formatted findings, and posts comments to PR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guitenbay](https://clawhub.ai/user/guitenbay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review GitCode pull requests by combining automated issue scanning with required manual review, selecting the highest-priority findings, formatting comments, and optionally posting them to a PR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can publish GitCode PR comments.

Mitigation: Require a human preview and explicit confirmation before running the posting step.

Risk: GitCode access tokens may be exposed when passed on the command line or in URLs.

Mitigation: Use narrowly scoped tokens, avoid long-lived credentials, do not pass tokens in URLs or shell history, and rotate any token already exposed that way.

Risk: Automated review findings can miss logic, design, performance, error-handling, and test-coverage issues.

Mitigation: Treat scanner output as a starting point and complete the documented manual review checklist before selecting findings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guitenbay/skills/code-review-for-gitcode)
- [GitCode PR comment API](artifact/API.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON review artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces temporary JSON files for scan results, selected issues, and formatted PR comments; final posting is optional and should require explicit confirmation.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
