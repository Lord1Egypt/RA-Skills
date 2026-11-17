## Description:

Checks the share of sentences containing numbers or dates that include source markers and lists those missing citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and reviewers use this skill to measure source-marker coverage in reports and identify sentences with numbers or dates that may need citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented --input example does not match the available CLI options.

Mitigation: Use --file or --text when checking a document.

Risk: Broad allowed-tools metadata exceeds the local checker's needs.

Mitigation: Limit granted tools to those needed for local input reading and reporting.

## Reference(s):

- [Citation Coverage Check on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/citation-coverage-check)
- [LGD theory (background linked in README)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [CLI text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coverage counts, pass/fail result, and missing-citation snippets; exit status 1 below the configured threshold.]

## Skill Version(s):

1.0.5 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
