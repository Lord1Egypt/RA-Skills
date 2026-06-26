## Description: <br>
Deprecated legacy ClawHub skill for analyzing, planning, and archiving low-value OpenClaw workspace memory logs to reduce redundant context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[irideas](https://clawhub.ai/user/irideas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this deprecated compatibility release to inspect workspace memory logs, create a cleanup plan, and archive low-value or older memory files after review. New users should prefer the replacement context-cleanup skill from the same publisher. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Archive actions can move workspace memory files and affect what context remains immediately available. <br>
Mitigation: Run analyze and plan first, review the listed files, use --dry-run when uncertain, and use --yes only after approving the exact cleanup plan. <br>
Risk: This is a deprecated legacy slug retained for compatibility. <br>
Mitigation: Prefer the replacement context-cleanup skill from the same publisher for new usage. <br>


## Reference(s): <br>
- [Context cleanup policy](references/policy.md) <br>
- [ClawHub skill page](https://clawhub.ai/irideas/bobo-context-cleanup) <br>
- [Publisher profile](https://clawhub.ai/user/irideas) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The archive workflow supports analyze, plan, archive, dry-run, confirmation, cutoff date, and machine-readable JSON modes.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
