## Description: <br>
Checks JavaScript projects for risky axios versions, a plain-crypto-js indicator, and known local files associated with a suspected supply-chain incident. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[preciousdust](https://clawhub.ai/user/preciousdust) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and incident responders use this skill to rapidly inspect frontend dependency trees for specific axios and plain-crypto-js risk indicators and to run an emergency remediation script when a project appears affected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script can modify package dependencies, remove lockfiles and node_modules, reinstall packages from npm, and delete specific files without a confirmation step. <br>
Mitigation: Review the script before running it, prefer a backed-up or disposable working tree, and use audit-only handling unless repair actions are explicitly intended. <br>
Risk: Automatic repair can change project dependency state during an incident response workflow. <br>
Mitigation: Capture the current dependency files first and review the resulting package and lockfile changes before continuing development or deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/preciousdust/axios-supply-chain-attack-check) <br>
- [Source article referenced by the skill](https://mp.weixin.qq.com/s/UP7_LLilOOgZPVW8tCsNrg?from=groupmessage&scene=1&subscene=10000&clicktime=1774932741&enterid=1774932741&sessionid=0&ascene=1&realreporttime=1774932741992&forceh5=1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and terminal output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled shell script reports detected indicators and may perform dependency repair actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
