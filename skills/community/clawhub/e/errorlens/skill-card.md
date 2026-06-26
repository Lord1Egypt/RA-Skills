## Description: <br>
ErrorLens scans codebases for empty catches, swallowed exceptions, missing error boundaries, unhandled rejections, generic error types, and unsafe error handling patterns across multiple programming languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use ErrorLens to scan source code for unsafe error handling patterns, generate findings and reports, and optionally enforce checks in pre-commit or CI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing hooks changes repository commit behavior and can block future commits based on ErrorLens findings. <br>
Mitigation: Review the bundled hook configuration and run hook install only in repositories where pre-commit enforcement is intended. <br>
Risk: Creating a baseline suppresses currently known findings from future scan output. <br>
Mitigation: Run baseline only after reviewing existing findings and deciding that they should be tracked as accepted backlog. <br>
Risk: Paid-tier commands require a local license key through ERRORLENS_LICENSE_KEY or OpenClaw configuration. <br>
Mitigation: Store the license key in local environment or user configuration and avoid committing it to source control. <br>


## Reference(s): <br>
- [ErrorLens ClawHub page](https://clawhub.ai/suhteevah/errorlens) <br>
- [Publisher profile](https://clawhub.ai/user/suhteevah) <br>
- [ErrorLens website](https://errorlens.pages.dev) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, Markdown reports, CI annotations, and JSON baseline or configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally, returns pass/fail exit codes, and may update repository hook or baseline files when those commands are invoked.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact CLI version string is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
