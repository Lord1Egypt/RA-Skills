## Description: <br>
Audits a workspace against DONE-unit outputs and pipeline target artifacts, then writes a contract report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WILLOSCAR](https://clawhub.ai/user/WILLOSCAR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill near the end of a workspace run, or before sharing a workspace, to check whether required outputs and pipeline target artifacts are present. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The public description emphasizes output/CONTRACT_REPORT.md, while security evidence notes that the skill may also update output/QUALITY_GATE.md. <br>
Mitigation: Run it only in trusted workspaces and review both report files after execution. <br>
Risk: The artifact bundles broader research-pipeline helper code beyond the contract-audit runner. <br>
Mitigation: Review PIPELINE.lock.md and the bundled helper surface before deployment, especially in workspaces with sensitive or high-value artifacts. <br>


## Reference(s): <br>
- [Artifact Contract Auditor ClawHub Release](https://clawhub.ai/WILLOSCAR/artifact-contract-auditor) <br>
- [Source Skill Definition](artifact/SKILL.md) <br>
- [Runner Script](artifact/scripts/run.py) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report files and concise status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output/CONTRACT_REPORT.md and may update output/QUALITY_GATE.md when the pipeline is complete or contract drift is detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; bundled skill frontmatter declares 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
