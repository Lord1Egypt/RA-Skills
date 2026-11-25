## Description:

Generate realistic digital human broadcast videos from portrait images and audio or text using Jimeng OmniHuman 1.5.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to create digital human broadcast videos from a portrait and supplied audio or text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portraits, audio, prompts, and parameters are sent to dLazy's hosted API or media storage; these inputs may contain personal or sensitive information.

Mitigation: Use media with the necessary permission, avoid uploading sensitive material, and review dLazy's service terms before submitting inputs.

Risk: The security evidence reports medium confidence and says package and local references were unresolved because the analysis was partial.

Mitigation: Review the reported whitespace and resolve the package and local references; inspect the pinned CLI package before installing it.

## Reference(s):

- [dLazy website](https://dlazy.com)
- [dLazy CLI project page](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy API key dashboard](https://dlazy.com/dashboard/organization/api-key)

## Skill Output:

**Output Type(s):** [Video, JSON]

**Output Format:** [Generated video asset (hosted URL or saved file), with JSON task and output metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation may complete asynchronously; results are hosted by dLazy.]

## Skill Version(s):

1.3.43 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
