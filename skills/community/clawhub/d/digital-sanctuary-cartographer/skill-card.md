## Description:

A consultative planning skill for mapping digital-sanctuary boundaries, outlining stress tests, and describing a versioned atlas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and human stewards use the skill to plan reviews of permissions, data flows, trust boundaries, and failure scenarios. Treat it as an unfinished planning aid; independently verify controls and outcomes before making deployment or incident decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reports successful security checks and protected exports without implementing those checks, so its assurances may be unreliable.

Mitigation: Treat status messages, PASS results, encryption claims, and export notices as unverified; independently confirm controls, logs, and files before relying on them for deployment or incident decisions.

## Reference(s):

- [Atlas schema](references/atlas_schema.json)
- [Stress test scenarios](docs/STRESS_TEST_CASES.md)
- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/digital-sanctuary-cartographer)
- [Publisher profile](https://clawhub.ai/user/deepseekoracle)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [Human-readable planning guidance, a JSON atlas schema, and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included Windows batch commands print status messages; their reported checks and exports should not be treated as verified results.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
