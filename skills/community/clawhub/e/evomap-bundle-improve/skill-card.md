## Description:

Validate, fix, optimize natural language, and publish EvoMap Gene+Capsule bundles for maximum discoverability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephyb97](https://clawhub.ai/user/josephyb97)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to validate EvoMap Gene+Capsule bundle structure, repair common schema issues, improve bundle descriptions and discovery signals, and optionally publish bundles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The publish path can execute injected shell commands from bundle content.

Mitigation: Review before installing or running on untrusted bundles and avoid publish and publish-all until the shell-based curl call is replaced with a safe HTTP client.

Risk: Fix, enhance, publish, and publish-all rewrite bundle content, identifiers, and provenance-like fields in place.

Mitigation: Keep backups or use version control before running commands that modify bundles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josephyb97/skills/evomap-bundle-improve)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [CLI command guidance and rewritten JSON bundle files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Validation commands report errors and warnings; fix, enhance, publish, and publish-all commands can rewrite bundle metadata and content in place.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
