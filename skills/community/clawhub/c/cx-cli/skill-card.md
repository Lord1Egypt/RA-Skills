## Description: <br>
Semantic code navigation with the `cx` CLI for understanding code structure, finding symbol definitions, tracing references before refactoring, and exploring large codebases efficiently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wei840222](https://clawhub.ai/user/wei840222) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to choose targeted `cx` CLI commands before reading files, so they can inspect code structure, symbol definitions, and references with less context overhead. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on the external `cx-cli` package and local `cx` binary behavior. <br>
Mitigation: Install and use it only when you trust or have reviewed the external package. <br>
Risk: `cx` can create local code indexes and its grammar or cache commands can change cx-managed local state. <br>
Mitigation: Run `cx` in repositories where local indexing is acceptable, and review cache or grammar maintenance commands before executing them. <br>


## Reference(s): <br>
- [cx Decision Tree](references/decision-tree.md) <br>
- [cx Output Examples](references/output-examples.md) <br>
- [Skill page](https://clawhub.ai/wei840222/cx-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and command-output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides read-only semantic code navigation with optional JSON output from the cx CLI.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
