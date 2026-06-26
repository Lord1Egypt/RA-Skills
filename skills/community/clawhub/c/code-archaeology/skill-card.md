## Description: <br>
Analyze legacy codebases to extract business rules, technical specifications, and migration requirements for modernization planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hickhe](https://clawhub.ai/user/hickhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze legacy systems, document business rules and technical constraints, assess security and technical debt, and prepare modernization or migration plans. It can also convert Code Archaeology results into AI Plan Generator context documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local Code Archaeology results and writes generated context files that may contain incomplete or incorrect business rules, technical specifications, or security findings. <br>
Mitigation: Run it in the intended project workspace, choose a non-sensitive output directory, and review generated files against the actual source code before committing, sharing, or using them for migration work. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hickhe/code-archaeology) <br>
- [README.md](README.md) <br>
- [EXAMPLE.md](EXAMPLE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON/YAML-style configuration files, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local context files such as business-rules.json, technical-specs.yaml, validation-standards.md, and integration-config.json when the conversion script is run.] <br>

## Skill Version(s): <br>
2.5.0 (source: evidence.release.version, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
