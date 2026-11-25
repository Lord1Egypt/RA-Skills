## Description:

Scores companies against an ICP on a schedule, records tier rationale and evidence, and can update matching CRM records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

RevOps and GTM teams use this skill to tier companies against their ICP and rubric, keep tiers current, and optionally sync the rationale to a CRM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marked this release suspicious because setup uses an unpinned installer and mutable source; some analysis was incomplete.

Mitigation: Verify and pin the installer and source to reviewed versions before installing, and complete a full review of the partially inspected component.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cargo-ai/skills/account-scoring)
- [Project homepage](https://github.com/getcargohq/gtm-skills)
- [Run guide](artifact/references/run.md)

## Skill Output:

**Output Type(s):** [Text, Code, Configuration, Guidance]

**Output Format:** [Structured tier records and Markdown setup guidance with TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tier (A, B, C, or disqualified), rationale, evidence URL, and tiered-at date; CRM write-back is optional.]

## Skill Version(s):

0.5.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
