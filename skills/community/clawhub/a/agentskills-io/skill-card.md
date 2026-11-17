## Description:

Create, validate, and publish Agent Skills following the official open standard from agentskills.io for new skill authoring, metadata validation, documentation conversion, and cross-platform compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killerapp](https://clawhub.ai/user/killerapp)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and engineers use this skill to create, validate, and publish portable Agent Skills, including converting existing documentation into skills and checking structure, frontmatter, and metadata for cross-platform use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation commands can execute unpinned remote validator code.

Mitigation: Pin the validator source to a reviewed commit or release before running installation or one-shot validation commands.

Risk: Repository validation scripts may run in trusted repositories where CI secrets are present.

Mitigation: Run validation without CI secrets exposed and review the validator source before using it in automated workflows.

Risk: The version-bump script can be exploited through unsafe SemVer parsing.

Mitigation: Do not run the version-bump script on untrusted plugin metadata until SemVer parsing is fixed.

## Reference(s):

- [Agent Skills Specification](https://agentskills.io/specification)
- [Agent Skills Reference Repository](https://github.com/agentskills/agentskills)
- [Specification Reference](references/specification.md)
- [Validation Guide](references/validation.md)
- [Examples](references/examples.md)
- [Best Practices](references/best-practices.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline YAML and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include skill templates, validation commands, troubleshooting guidance, and repository maintenance commands.]

## Skill Version(s):

2.5.0 (source: ClawHub release metadata; artifact frontmatter metadata version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
