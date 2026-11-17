## Description:

Embeds and controls a virtual avatar through the avatar-runtime npm package, with Live2D rendering, VRM 3D, vector fallback, and provider-agnostic control for expression, body, and scene animation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neiljo-gy](https://clawhub.ai/user/neiljo-gy)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to start, configure, embed, and control avatar-runtime sessions for browser avatar widgets, Live2D characters, VRM 3D avatars, and provider-backed avatar interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run an unpinned npx avatar-runtime command, so the executed package could change after review.

Mitigation: Verify the npm package identity, pin a reviewed version before deployment, and test it in a sandboxed environment first.

Risk: Provider API keys may be passed to the runtime process through environment variables.

Mitigation: Use least-privilege non-production keys during evaluation, avoid shared shell histories and logs, and rotate exposed credentials.

Risk: Sample Live2D assets described by the artifact have license restrictions that may prohibit redistribution or commercial use.

Mitigation: Use only models with rights appropriate for the deployment, and keep restricted sample assets limited to local development.

## Reference(s):

- [Web Embedding Reference](references/WEB-EMBEDDING.md)
- [ClawHub Avatar Runtime skill page](https://clawhub.ai/neiljo-gy/skills/avatar-runtime)
- [Live2D Free Material License](https://www.live2d.com/en/sdk/license/free-material/)
- [VRoid Hub](https://hub.vroid.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with bash, HTML, JavaScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local runtime endpoints, environment variable settings, curl requests, and browser embedding snippets.]

## Skill Version(s):

0.2.1 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
