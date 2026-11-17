## Description:

Build with Bun runtime avoiding Node.js compatibility traps, bundler pitfalls, and package manager gotchas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill for Bun runtime, bundler, package manager, TypeScript, testing, and migration guidance when building or moving JavaScript and TypeScript projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The migration snippet removes local dependency artifacts and lockfiles when run.

Mitigation: Confirm the intended project directory first, then commit or back up dependency state and lockfiles before running migration commands.

Risk: Bun runtime, bundler, package manager, and test-runner behavior can differ from Node.js or npm workflows.

Mitigation: Run the full project test suite, verify native dependencies and workspace links, and test production bundles in the target runtime before release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/bun)
- [Publisher Profile](https://clawhub.ai/user/ivangdavila)
- [Bundler Traps](artifact/bundler.md)
- [Node.js Compatibility Traps](artifact/node-compat.md)
- [Package Manager Traps](artifact/packages.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no active code is executed by the skill itself.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
