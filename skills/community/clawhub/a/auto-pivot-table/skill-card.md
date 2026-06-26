## Description: <br>
Auto Pivot Table helps agents implement ORBCAFE pivot-table analytics and voice navigation using CPivotTable, usePivotTable, CAINavProvider, and useVoiceInput patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenruiyang](https://clawhub.ai/user/shenruiyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to add drag-and-drop pivot dimensions, PivotChart companion views, aggregation controls, preset persistence, and space-key voice workflows to ORBCAFE UI applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install and bootstrap commands can modify a project or pull npm dependencies. <br>
Mitigation: Review the dependencies and commands before running them in a trusted project. <br>
Risk: Voice navigation can expose websocket endpoints or ASR credentials if they are hardcoded. <br>
Mitigation: Keep websocket URLs and ASR credentials in application configuration rather than source code. <br>
Risk: Parts of the artifact are written in Chinese, which may be unclear to some users. <br>
Mitigation: Translate the Chinese sections before use when full review clarity is needed. <br>


## Reference(s): <br>
- [Domain Patterns](references/domain-patterns.md) <br>
- [Pivot + AINav Guardrails](references/guardrails.md) <br>
- [Pivot + AINav Recipes](references/recipes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with TypeScript/TSX and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes module choice, minimal implementation guidance, operations notes, verification steps, and troubleshooting points.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
