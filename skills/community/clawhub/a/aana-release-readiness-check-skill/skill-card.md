## Description:

Checks release readiness by verifying artifacts, tests, docs, approval, risks, and evidence before publishing tags, packages, or deployment notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release maintainers use this instruction-only skill to check release targets, evidence, documentation, artifact/version alignment, approval, and rollback readiness before publishing tags, packages, marketplace listings, deployment notes, or public version snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Release readiness checks could expose sensitive or private release details if an optional checker receives full logs, credentials, or unrelated repository data.

Mitigation: Send only the redacted status payload described by the skill and omit secrets, credentials, full logs, private release notes, and unrelated repository data.

Risk: The skill is instruction-only and does not verify artifacts, run tests, publish releases, or enforce approval by itself.

Mitigation: Use it as a release gate checklist and confirm test, documentation, artifact, version, rollback, and approval evidence before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindbomber/skills/aana-release-readiness-check-skill)
- [mindbomber publisher profile](https://clawhub.ai/user/mindbomber)
- [Release readiness check schema](artifact/schemas/release-readiness-check.schema.json)
- [Redacted release readiness check example](artifact/examples/redacted-release-readiness-check.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance with a structured release gate text pattern and an optional redacted JSON review payload.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; does not execute commands, write files, install dependencies, persist memory, or bundle an external checker.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
