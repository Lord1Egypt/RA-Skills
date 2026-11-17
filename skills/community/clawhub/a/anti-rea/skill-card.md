## Description:

Guides developers integrating antiRea into server-side applications to detect data scraping and coordinated automated abuse while leaving enforcement decisions to the host application.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dankezo](https://clawhub.ai/user/dankezo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate per-identity access metering and abuse signals into a Node.js web application. They use the signals to inform host-side decisions about new actions and data access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial: four local references could not be resolved, and a credential-related signal was treated as expected rather than confirmed behavior.

Mitigation: Review the unresolved references and credential-related example in the source before integrating; treat antiRea signals as advisory and let host authorization logic decide responses.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dankezo/skills/anti-rea)
- [Declared source repository (package metadata)](https://github.com/dankezo/antiRea)
- [npm package](https://www.npmjs.com/package/@dannyphan190/anti-rea)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with TypeScript and JavaScript examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Server-side integration guidance; host-specific enforcement remains the application's responsibility.]

## Skill Version(s):

3.0.0 (source: release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
