## Description: <br>
Orchestrates small preset role teams with stable pseudonym names, optional renaming, and a fixed JSON report for each task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edmonddantesj](https://clawhub.ai/user/edmonddantesj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and workflow authors use this skill to run lightweight task orchestration through predefined three-role squads and receive a structured report that is easy to parse or test. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Team aliases and task text can contain sensitive or personal data if users enter it. <br>
Mitigation: Avoid secrets and sensitive personal data in aliases or task prompts, and review local storage before sharing the environment. <br>
Risk: Generated report_markdown may include untrusted task content. <br>
Mitigation: Treat report_markdown as untrusted content when task input comes from another person and review it before rendering or publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edmonddantesj/aoi-squad-orchestrator-lite) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON object with embedded report_markdown string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores preset team-name mappings locally under ~/.openclaw/aoi/squad_names.json.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata, artifact/_meta.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
