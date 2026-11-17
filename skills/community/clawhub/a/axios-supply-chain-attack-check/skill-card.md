## Description:

Provides a quick shell-script workflow for checking frontend projects for malicious axios versions, the plain-crypto-js backdoor dependency, and related incident cleanup steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[preciousdust](https://clawhub.ai/user/preciousdust)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security responders use this skill to inspect frontend dependency trees for flagged axios and plain-crypto-js versions and to follow an emergency remediation script when risk is detected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the bundled script can automatically uninstall packages, reinstall axios, remove node_modules and lockfiles, and delete host files without confirmation.

Mitigation: Review the script first, run it only in a disposable or backed-up project, and prefer a read-only audit or manually controlled remediation workflow.

Risk: The release security verdict is suspicious because cleanup behavior can modify dependencies and files during incident response.

Mitigation: Treat execution as a privileged remediation action and require human approval before applying changes to a project or host system.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/preciousdust/skills/axios-supply-chain-attack-check)
- [Source article referenced by the skill](https://mp.weixin.qq.com/s/UP7_LLilOOgZPVW8tCsNrg?from=groupmessage&scene=1&subscene=10000&clicktime=1774932741&enterid=1774932741&sessionid=0&ascene=1&realreporttime=1774932741992&forceh5=1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a command to run a bundled shell script that can inspect and remediate local npm dependencies.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
