## Description:

Analyze OpenClaw costs and detect billing issues using bundled Node.js logic that runs locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[echoudhry](https://clawhub.ai/user/echoudhry)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users and developers use this skill to inspect local cost drivers across configuration, session usage, transcripts, and workspace signals. It returns cost findings, estimates, and concrete fix guidance so users can reduce avoidable model spend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill analyzes sensitive local OpenClaw data and the security evidence says some local data access is under-disclosed.

Mitigation: Review the skill before installation and run it only where local configuration, session, transcript, and web-chat data may be inspected.

Risk: Generated reports or JSON output may expose configuration details, identifiers, third-party network metadata, tokens, or commands.

Mitigation: Check and redact generated reports before sharing them outside the local environment.

Risk: Optional dashboard paths and unpinned npx examples are called out as unsuitable for sensitive systems until issues are fixed.

Mitigation: Prefer the reviewed ClawHub release and non-dashboard output modes on sensitive systems; pin external package execution when running outside ClawHub.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/echoudhry/skills/clawculator)
- [Project Homepage](https://github.com/echoudhry/clawculator)
- [Live Demo](https://echoudhry.github.io/clawculator)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Terminal text, Markdown report, JSON, and optional local HTML dashboard depending on flags.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include local OpenClaw configuration and session-derived identifiers; review before sharing.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
