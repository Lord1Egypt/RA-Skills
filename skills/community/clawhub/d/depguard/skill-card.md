## Description: <br>
Dependency audit, vulnerability scanning, and license compliance. Free vuln check + paid continuous monitoring via git hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use DepGuard to scan project dependencies for vulnerabilities and license issues, generate audit reports, configure dependency policies, create SBOMs, and optionally install commit-time monitoring for lockfile changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: `depguard fix` can modify dependency manifests or lockfiles. <br>
Mitigation: Run a scan first, start from a clean git working tree, and review dependency and lockfile diffs before accepting changes. <br>
Risk: `depguard hooks install` can add commit-time scanning that blocks commits when high-risk dependency changes are detected. <br>
Mitigation: Install hooks only in repositories where commit-time dependency checks are expected, and review the generated hook configuration. <br>


## Reference(s): <br>
- [DepGuard ClawHub listing](https://clawhub.ai/suhteevah/depguard) <br>
- [DepGuard homepage](https://depguard.pages.dev) <br>
- [OpenClaw](https://openclaw.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal output, Markdown reports, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local package-manager audit tools and may write dependency, lockfile, hook, policy, SBOM, or report files depending on the selected command.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
