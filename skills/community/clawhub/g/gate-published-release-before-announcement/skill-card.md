## Description:

Gates an exact published npm release before its announcement by verifying what consumers actually receive from the public registry tarball.

This skill is ready for commercial/non-commercial use.

## Publisher:

[powmcp](https://clawhub.ai/user/powmcp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release maintainers use this skill after an npm package version is public but before announcement to inspect the exact published tarball, review packaging and provenance evidence, and record a release judgment within the tool's stated limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path uses an unpinned npx installer that can execute mutable remote code before the reviewed skill is installed.

Mitigation: Review the setup step, prefer a pinned installer version or commit-pinned integrity-verified installation path, and run installation from a least-privileged environment without unrelated secrets.

Risk: The workflow handles package metadata, file names, registry values, fetched content, and error strings as untrusted input.

Mitigation: Quote fetched values only as evidence, avoid using them directly in code or configuration, and do not echo secrets that appear in outputs.

## Reference(s):

- [npm Package Check reference](references/npm-package-preflight.md)
- [npm Package Check app page](https://powmcp.com/apps/npm-package-preflight/)
- [publint rules](https://publint.dev/rules)
- [Type-resolution linting workflow](https://tsdown.dev/options/lint)
- [npm provenance statements](https://docs.npmjs.com/generating-provenance-statements/)
- [npm trusted publishers](https://docs.npmjs.com/trusted-publishers/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown report with checklist items, findings table, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an exact public npm package@version and treats fetched registry content as untrusted evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
