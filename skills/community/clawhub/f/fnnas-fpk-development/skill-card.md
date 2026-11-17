## Description:

FNNAS FPK application development skill for the full Feiniu fnOS FPK workflow, including creation, configuration, build, debugging, and release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songxf1024](https://clawhub.ai/user/songxf1024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, configure, test, package, and publish FNNAS/fnOS FPK applications. It guides agents to consult bundled FNNAS documentation before giving implementation details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends optional third-party global npm tooling that can run code on a user's machine.

Mitigation: Review the tooling before use, prefer pinned or local installation where possible, run it in an isolated development environment, and avoid elevated shells.

Risk: The security summary rates the release as suspicious because it includes optional third-party tooling and extra skill recommendations.

Mitigation: Install only when a Chinese FNNAS/fnOS development workflow is expected, and review optional recommendations before executing them.

## Reference(s):

- [FNNAS FPK Development Skill](SKILL.md)
- [Bundled FNNAS Development Documentation](references/ALL_DOCS.md)
- [FNNAS Developer Guide](https://developer.fnnas.com/docs/guide)
- [FNNAS Developer Platform](https://developer.fnnas.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are grounded in the bundled FNNAS documentation and may include project file guidance, manifest configuration, build commands, and release checklists.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
