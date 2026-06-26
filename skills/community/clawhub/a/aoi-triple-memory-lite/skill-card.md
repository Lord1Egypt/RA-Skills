## Description: <br>
AOI Triple Memory (Lite) provides file search and decision-note templates without plugins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edmonddantesj](https://clawhub.ai/user/edmonddantesj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and workspace operators use this skill to search local project files, keep file-based memory, and create structured decision notes under a workspace context directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The search command can scan the entire selected workspace. <br>
Mitigation: Run it only in workspaces where broad file search is acceptable, and avoid repositories containing secrets or private configuration unless access is restricted. <br>
Risk: The note command writes Markdown files under ./context. <br>
Mitigation: Review generated notes before committing or sharing them, especially when they may contain project decisions or sensitive context. <br>
Risk: The skill depends on ripgrep even though the dependency is not declared. <br>
Mitigation: Confirm rg is installed and available on PATH before relying on search behavior. <br>
Risk: The security evidence reports a ripgrep option-injection risk. <br>
Mitigation: Prefer a fixed version that passes the search pattern after an rg option delimiter such as --. <br>


## Reference(s): <br>
- [AOI Triple Memory (Lite) on ClawHub](https://clawhub.ai/edmonddantesj/aoi-triple-memory-lite) <br>
- [AOI Skills Issues](https://github.com/edmonddantesj/aoi-skills/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [JSON command output and Markdown decision-note files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The search command emits JSON results, and the note command writes Markdown files under ./context.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence, package.json, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
