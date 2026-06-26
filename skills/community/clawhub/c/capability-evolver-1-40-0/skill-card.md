## Description: <br>
A self-evolution engine for AI agents that analyzes runtime history to identify improvements and applies protocol-constrained evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zengyu199009](https://clawhub.ai/user/zengyu199009) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect agent runtime history, select reusable GEP assets, produce protocol-bound evolution prompts, and record auditable evolution events. It is most relevant for teams maintaining agent prompts, logs, repair workflows, and networked evolution operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Network-connected evolution and worker features can exchange tasks, assets, heartbeats, and reviews with external services. <br>
Mitigation: Run offline first, configure only required endpoints, and keep worker mode, auto-publish, and network task handling disabled unless they are intentionally needed. <br>
Risk: Self-modification or solidification features can write assets, memory, and source files in the workspace. <br>
Mitigation: Use review mode, a dedicated non-sensitive workspace, version control review, and conservative rollback settings before accepting generated changes. <br>
Risk: Optional GitHub automation may create releases or issues using repository tokens. <br>
Mitigation: Use least-privilege tokens, avoid broad GitHub credentials, and leave auto-issue and release automation disabled unless required. <br>
Risk: Runtime logs and memory files may contain sensitive data that could be analyzed locally or included in networked reports. <br>
Mitigation: Use non-sensitive logs, review redaction behavior, and disable remote memory graph or hub reporting features for sensitive environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zengyu199009/capability-evolver-1-40-0) <br>
- [Publisher profile](https://clawhub.ai/user/zengyu199009) <br>
- [EvoMap documentation](https://evomap.ai/wiki) <br>
- [EvoMap homepage](https://evomap.ai) <br>
- [GitHub repository referenced by artifact](https://github.com/EvoMap/evolver) <br>
- [GitHub releases referenced by artifact](https://github.com/EvoMap/evolver/releases) <br>
- [MIT license reference from artifact README](https://opensource.org/licenses/MIT) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and stdout text with inline shell commands, JSON-like protocol prompts, and generated local asset files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write GEP assets, memory records, evolution events, and optional source changes when solidification features are enabled.] <br>

## Skill Version(s): <br>
1.40.0 (source: artifact package.json and _meta.json); ClawHub release version 1.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
