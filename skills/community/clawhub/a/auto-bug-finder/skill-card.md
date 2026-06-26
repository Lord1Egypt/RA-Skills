## Description: <br>
Auto Bug Finder iteratively scans, analyzes, fixes, and verifies Solidity contracts with Hardhat, Slither, coverage checks, and heuristic security checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jengajojo](https://clawhub.ai/user/jengajojo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-contract engineers use this skill to run iterative Solidity security checks before deployment, after refactors, or as a CI gate. It compiles and tests a Hardhat project, runs Slither and heuristic checks, applies supported fixes, and produces review artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool can automatically rewrite smart-contract files. <br>
Mitigation: Run it only on a disposable branch or copy, and manually inspect every generated diff before merging or deploying. <br>
Risk: The artifact contains hardcoded AgentEscrow paths and computes its project directory from the script location. <br>
Mitigation: Review and adjust the target contract, test paths, and project directory assumptions before running it on another project. <br>
Risk: The final report can use production-ready language that may overstate the assurance provided by automated checks. <br>
Mitigation: Treat the report as a helper artifact, not an independent audit signoff; keep human review and formal security review in the release process. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/jengajojo/auto-bug-finder) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Auto Bug Finder script](artifact/auto-bug-finder.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON sprint data, patch notes, console output, and Solidity code changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates an auto-bug-finder output directory and may rewrite Solidity contract files during supported fixes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
