## Description: <br>
Trae Agent helps agents analyze large repositories, plan multi-file code changes, and validate results using repository indexing and ensemble search strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill for repository-level code understanding, navigation, multi-file editing, refactoring, and validation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository-level editing and command validation can modify multiple files or run commands with unintended effects. <br>
Mitigation: Keep requests narrow, use version control, review diffs before accepting changes, and run validation in an isolated workspace when repositories are untrusted. <br>
Risk: Repository indexing can expose secrets, private files, or sensitive project context. <br>
Mitigation: Exclude secrets and private paths from indexing workflows and avoid using the skill on sensitive repositories without appropriate isolation. <br>


## Reference(s): <br>
- [Trae Agent examples](references/examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/mtsatryan/ah-trae-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with summaries, plans, code snippets, command suggestions, validation results, and final status notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task understanding, search results, edit plans, execution logs, validation results, and final metrics.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
