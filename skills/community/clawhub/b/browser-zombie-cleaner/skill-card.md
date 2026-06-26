## Description: <br>
Detect and clean up zombie browser processes left by OpenClaw's browser tool after Gateway restarts, with detect-only reporting by default and optional scoped termination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoqunabc](https://clawhub.ai/user/guoqunabc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to identify orphaned OpenClaw browser processes, review memory impact, and optionally terminate only scoped stale browser sessions during cleanup or health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script can terminate browser processes when --kill is used. <br>
Mitigation: Run detect-only first, review the listed PIDs, and use --kill only for orphaned OpenClaw browser sessions you intend to close. <br>
Risk: Changing the process match pattern can expand which browser processes are considered candidates. <br>
Mitigation: Keep the default .openclaw/browser/ pattern unless intentionally broadening scope, and review results before enabling termination. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands; the cleanup script can emit text logs or JSON summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default execution is detect-only; process termination requires --kill and records actions to a local audit log.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
