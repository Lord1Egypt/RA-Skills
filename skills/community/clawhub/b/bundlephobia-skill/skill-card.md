## Description:

Analyze JavaScript and npm package size using Bundlephobia plus related package and bundle-size checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nick2bad4u](https://clawhub.ai/user/nick2bad4u)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to measure npm package, package.json dependency, npm publish, and built artifact size, then receive concrete recommendations for reducing bundle or publish footprint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to run npm packaging checks that can execute project-controlled scripts.

Mitigation: Use `npm pack --dry-run --json --ignore-scripts` where supported, or run packaging checks in a disposable sandbox without sensitive credentials.

Risk: The artifact references helper files that are absent from this release artifact.

Mitigation: Review the installed skill contents before use and fall back to direct Bundlephobia API checks or local artifact measurement when helper scripts are unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nick2bad4u/skills/bundlephobia-skill)
- [Publisher profile](https://clawhub.ai/user/nick2bad4u)
- [Source repository](https://github.com/Nick2bad4u/Bundlephobia-Skill)
- [Bundlephobia package API](https://bundlephobia.com/api/size?package=<name[@version]>)
- [Bundlephobia package pages](https://bundlephobia.com/package/<package>)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with package-size measurements, command examples, and concrete recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include minified size, gzip size, dependency counts, packaging size, artifact size, failed package errors, and pass/fail threshold results when measured.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
