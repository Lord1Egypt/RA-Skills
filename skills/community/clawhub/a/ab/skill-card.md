## Description:

Design, run, and analyze A/B tests to compare content variants, track metrics, and support data-driven optimization decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgta23](https://clawhub.ai/user/hgta23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and product teams use this skill to create A/B test plans, configure variants and metrics, record results, and analyze performance across websites, email campaigns, mobile apps, social media content, and e-commerce pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can escape its intended test-storage folder and read or overwrite other JSON files accessible to the user.

Mitigation: Use only trusted test names, run the skill from a low-privilege workspace, and review path validation before deployment.

Risk: Unpinned dependencies can change installation behavior over time.

Mitigation: Pin and review dependencies before installing the skill in production or shared environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hgta23/skills/ab)
- [Publisher Profile](https://clawhub.ai/user/hgta23)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline CLI commands and JSON-backed test data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update local JSON files for named A/B tests.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
