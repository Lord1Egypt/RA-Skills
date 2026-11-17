## Description:

AetherCore v3.3.4 helps agents optimize JSON processing, index files, and compact user-specified local content through Python CLI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aetherclawai](https://clawhub.ai/user/aetherclawai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical agents use this skill to run local JSON optimization, benchmark JSON performance, build searchable indexes, and compact files in explicitly selected paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has a suspicious security verdict and should not be trusted solely because its artifact documentation claims security review readiness.

Mitigation: Review the source and scanner evidence before installation, and test in an isolated environment first.

Risk: Unsafe loading of existing .pkl index files can expose users to untrusted serialized data.

Mitigation: Do not load existing .pkl index files from untrusted locations; recreate indexes in a clean workspace when possible.

Risk: The skill processes files and directories selected by the user, which can expose sensitive local content if pointed at credential or system paths.

Mitigation: Run it only on reviewed, non-sensitive paths and avoid credential stores, home-directory sweeps, and system directories.

Risk: Dependency and installation behavior can vary across environments.

Mitigation: Use a pinned virtual environment and install only the declared dependency set needed for testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aetherclawai/skills/aethercore)
- [AetherCore homepage](https://clawhub.ai/aethercore)
- [Security and Scope Declaration](SECURITY_AND_SCOPE_DECLARATION.md)
- [Core Code Analysis](CORE_CODE_ANALYSIS.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local file or configuration outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Works on user-specified local paths and may produce optimized JSON, indexes, compaction results, and benchmark text.]

## Skill Version(s):

3.3.4 (source: server release metadata, artifact frontmatter, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
