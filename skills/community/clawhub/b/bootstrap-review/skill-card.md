## Description: <br>
Reviews an agent workspace's boot files against registry-backed context notes and produces a concise audit, refactor recommendations, and optional staged rewrites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gregtysick](https://clawhub.ai/user/gregtysick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to review bootstrap files for one agent at a time, find redundancy or stale references, and prepare safer staged cleanup drafts when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A misconfigured boot context registry can cause the agent to read boot files or context notes the user did not intend to include. <br>
Mitigation: Inspect the registry before review and keep entries limited to the selected agent's boot files and approved context notes. <br>
Risk: Draft changes to boot files can affect future agent behavior if applied without review. <br>
Mitigation: Use staged replacements by default, review diffs, and require explicit approval before in-place updates. <br>


## Reference(s): <br>
- [Boot File Review Skill](artifact/references/why-this-skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown audit with optional staged Markdown files and JSON registry guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default workflow is audit-only; staged replacement drafts are produced only when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
