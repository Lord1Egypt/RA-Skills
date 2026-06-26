## Description: <br>
Dead code and unused export detector that scans JavaScript/TypeScript, Python, Go, Java, and CSS for dead code, orphan files, unused exports, and code cruft. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to scan local codebases for dead code, unused exports, orphan files, unreachable paths, and related cleanup opportunities. It can also generate reports, SARIF output, and optional pre-commit hook checks for code review and CI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local shell commands can make persistent project changes when hook installation or ignore-rule commands are used. <br>
Mitigation: Run the scan command first, review hook installation steps, and inspect any lefthook or configuration changes before enabling them. <br>
Risk: Unsafe handling of crafted local inputs could execute unexpected commands. <br>
Mitigation: Use only trusted license keys, paths, and ignore patterns until the input-handling issue is fixed. <br>
Risk: The security review marked this release suspicious because optional commands and local script behavior need extra review. <br>
Mitigation: Install only from a trusted publisher, review the scripts before running paid-tier commands, and avoid running the skill in sensitive repositories without approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suhteevah/deadcode) <br>
- [DeadCode website](https://deadcode.pages.dev) <br>
- [DeadCode pricing](https://deadcode.pages.dev/#pricing) <br>
- [DeadCode hooks documentation](https://deadcode.pages.dev/docs/hooks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output, Markdown reports, and SARIF JSON depending on the command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free scans are limited to 5 source files; Pro and Team commands require DEADCODE_LICENSE_KEY; hook installation can modify lefthook configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
