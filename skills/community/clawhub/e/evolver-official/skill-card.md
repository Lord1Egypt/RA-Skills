## Description: <br>
A self-evolution engine for AI agents that analyzes runtime history to identify improvements and applies protocol-constrained evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toller892](https://clawhub.ai/user/toller892) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent teams use this skill to inspect agent runtime history, turn recurring failures or prompt changes into auditable evolution assets, and guide protocol-constrained repair or optimization work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan classifies this release as suspicious because it can run persistently and change agent code or memory with weak default review controls. <br>
Mitigation: Run it only in a sandbox or disposable branch with backups, prefer review or dry-run behavior, and inspect proposed changes before applying them. <br>
Risk: Loop and automated modes can repeatedly modify or guide changes without sufficient human oversight. <br>
Mitigation: Avoid default automated or loop modes in production, use `--review` for sensitive environments, and keep version-controlled rollback points. <br>
Risk: Dynamic local-skill and external asset ingestion can expand the skill's effective behavior beyond the packaged release. <br>
Mitigation: Disable dynamic local-skill and external asset ingestion unless needed, restrict memory and history paths, and use least-privilege short-lived tokens for release workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/toller892/evolver-official) <br>
- [EvoMap](https://evomap.ai) <br>
- [EvoMap documentation](https://evomap.ai/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured text with command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate protocol-bound prompts, reusable evolution assets, and reviewable repair or optimization guidance.] <br>

## Skill Version(s): <br>
1.20.4 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
