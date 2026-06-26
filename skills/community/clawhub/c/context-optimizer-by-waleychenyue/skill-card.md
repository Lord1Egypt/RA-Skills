## Description: <br>
智能上下文优化器。自动分析、精简和优化OpenClaw工作空间上下文文件，提取可复用组件为独立技能，大幅减少token消耗。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waleychenyue](https://clawhub.ai/user/waleychenyue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace maintainers use this skill to analyze OpenClaw context files, reduce redundant or token-heavy guidance, generate optimization reports, and extract reusable workflows into skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local optimization can change important workspace guidance files. <br>
Mitigation: Use version control or backups before optimization and review diffs after changes. <br>
Risk: Generated reports, configuration files, copied scripts, or new skills may affect future agent behavior. <br>
Mitigation: Review generated files before relying on them in active workspaces. <br>
Risk: Cron or CI automation can apply context changes repeatedly before the workflow is proven. <br>
Mitigation: Test on a non-critical workspace before enabling scheduled or CI automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/waleychenyue/context-optimizer-by-waleychenyue) <br>
- [EXAMPLES.md](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON analysis data, code and configuration snippets, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write reports, configuration files, copied scripts, or generated skill files in the local OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
