## Description: <br>
Systematic root-cause debugging with verification for errors, stack traces, broken tests, flaky tests, regressions, or other unexpected behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliaal](https://clawhub.ai/user/iliaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to reproduce failures, identify root causes with evidence, test competing hypotheses, and verify fixes before completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iliaal/compound-eng-debugging) <br>
- [SPEC.md](artifact/SPEC.md) <br>
- [Analysis of Competing Hypotheses](artifact/references/competing-hypotheses.md) <br>
- [Defense in Depth](artifact/references/defense-in-depth.md) <br>
- [Root Cause Tracing](artifact/references/root-cause-tracing.md) <br>
- [Specialized Debugging Patterns](artifact/references/specialized-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown debug reports with evidence, file:line references, verification commands, and optional diagnostic reports from collect-diagnostics.sh.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated diagnostics can include local and repository metadata; review and redact repository URLs, usernames, local paths, commit messages, branch names, and environment values before sharing.] <br>

## Skill Version(s): <br>
4.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
