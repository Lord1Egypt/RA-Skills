## Description:

Convert static character images into vivid action videos with Jimeng Dream Actor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to turn a static character image into an action video by providing a prompt and image to Jimeng Dream Actor through dLazy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports a benign verdict with medium confidence, but its analysis was partial, some references were unresolved, and it flagged an undeclared `dlazy login` operation.

Mitigation: Review the login and authentication behavior and unresolved references before use; follow the documented dLazy authentication flow and keep the API key in the CLI configuration or environment variable.

Risk: Prompts and local media provided to the skill are sent to dLazy hosted services.

Mitigation: Only submit prompts and media you are authorized to share; check each file for sensitive content before invoking the skill.

## Reference(s):

- [CLI repository link declared in skill metadata (server provenance unavailable)](https://github.com/dlazy-ai/cli)
- [dLazy CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)
- [dLazy API key dashboard](https://dlazy.com/dashboard/organization/api-key)

## Skill Output:

**Output Type(s):** [Media files, JSON]

**Output Format:** [JSON response with generated media URLs and task status; optionally a saved media file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation may complete asynchronously; use the returned task ID to check status.]

## Skill Version(s):

1.3.44 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
