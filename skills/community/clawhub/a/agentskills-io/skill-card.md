## Description: <br>
Create, validate, and publish Agent Skills following the official open standard from agentskills.io. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killerapp](https://clawhub.ai/user/killerapp) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, validate, document, and publish portable Agent Skills for agent environments such as Claude Code, Cursor, GitHub Copilot, OpenAI integrations, and VS Code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Validation commands fetch and run a validator from GitHub. <br>
Mitigation: Prefer one-shot uvx use, or pin and review the upstream validator before permanent installation. <br>
Risk: The version-bump script can modify plugin metadata and marketplace entries. <br>
Mitigation: Inspect git diffs after running the script before committing or publishing changes. <br>


## Reference(s): <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [Agent Skills Reference Repository](https://github.com/agentskills/agentskills) <br>
- [Specification Reference](references/specification.md) <br>
- [Validation Guide](references/validation.md) <br>
- [Examples](references/examples.md) <br>
- [Best Practices](references/best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with YAML frontmatter examples, inline shell commands, and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or update skill files, validation commands, plugin metadata, and version-bump guidance.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release metadata; skill frontmatter metadata lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
