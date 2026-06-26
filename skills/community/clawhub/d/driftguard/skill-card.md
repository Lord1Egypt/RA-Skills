## Description: <br>
DriftGuard Security Scanner+ scans local repos, OpenClaw skills, and AI agent tool folders for security drift, trust baselines, and risky capability changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[david90232](https://clawhub.ai/user/david90232) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan local repositories, installed skills, and agent tool folders before trust, then compare later updates against saved baselines. It helps surface file, dependency, symlink, install-hook, prompt-injection, shell, network, obfuscation, and sensitive-path drift for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports and baselines may reveal sensitive filenames, hashes, metadata, or quoted evidence lines from the scanned target. <br>
Mitigation: Run the scanner only against the intended folder and keep generated reports and baselines private when the target may contain sensitive information. <br>
Risk: Scanner output is heuristic review guidance and may miss issues or flag benign patterns. <br>
Mitigation: Use findings to guide human review rather than treating a clean result as a guarantee of safety. <br>
Risk: Target-provided suppressions could hide risky findings if trusted too early. <br>
Mitigation: Prefer reviewer-controlled configuration and enable target-provided suppressions only after reviewing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/david90232/driftguard) <br>
- [OpenClaw security metadata page](https://clawhub.ai/david90232/driftguard/security/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [CLI console text plus optional JSON reports, Markdown reports, baseline files, and review-ticket Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local outputs may include filenames, hashes, metadata, and quoted evidence lines from the scanned target.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release evidence and scripts/version.js) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
