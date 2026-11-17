## Description:

Guides developers through connecting a model to an application by selecting a model, reusing or creating a suitable endpoint, and optionally obtaining a code example.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this workflow to turn an intent to use a model in an application into a safe onboarding path. It checks identity and model eligibility, reuses a matching available endpoint when possible, requires confirmation before endpoint creation, and can provide an optional code example.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan raised an instruction-scope concern but did not provide a detailed finding, leaving its scope uncertain.

Mitigation: Treat the concern as a review item and inspect the skill instructions and their referenced skills before installation or use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/jasonstarlight/skills/arkcli-onboard)
- [Publisher profile](https://clawhub.ai/user/jasonstarlight)
- [Evaluation cases](artifact/references/evals.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with workflow guidance, shell commands, and optional code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes users among related skills; endpoint creation requires explicit confirmation.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
