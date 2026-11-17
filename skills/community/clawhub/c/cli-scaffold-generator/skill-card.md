## Description:

Generates professional Node.js CLI application scaffolds with project structure, command templates, documentation, and test setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to quickly scaffold Node.js command-line tools with common CLI framework patterns, package metadata, README content, and local development commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generator can overwrite unintended files when run with unsafe project names or output locations.

Mitigation: Run it only in a disposable or empty directory and avoid absolute paths or ../ path components.

Risk: Generated npm project metadata or dependencies may be unsafe when derived from untrusted inputs.

Mitigation: Inspect the generated package.json before running npm install, npm link, or publishing commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sunshine-del-ux/skills/cli-scaffold-generator)
- [Publisher Profile](https://clawhub.ai/user/sunshine-del-ux)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Markdown]

**Output Format:** [Generated project files with command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a CLI project directory containing JavaScript source, package metadata, README content, tests, and executable permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
