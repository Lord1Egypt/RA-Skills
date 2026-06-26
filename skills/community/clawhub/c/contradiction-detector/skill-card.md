## Description: <br>
Detects contradictions between OpenClaw agent instruction files, cron prompts, skill files, and hooks, then reports findings and proposed fixes for review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[korengast](https://clawhub.ai/user/korengast) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit OpenClaw agent workspaces for conflicting instructions across AGENTS.md, SOUL.md, HEARTBEAT.md, MEMORY.md, cron prompts, skill files, and hooks before reviewing proposed fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw instruction files, installed skill files, hook listings, and cron prompt text. <br>
Mitigation: Install it only in workspaces where this read access is acceptable and limit use to intended OpenClaw directories. <br>
Risk: Proposed fixes can change agent behavior if accepted without review. <br>
Mitigation: Review each proposed diff before approval and require explicit discussion before changing schedules, task ownership, security rules, or permission boundaries. <br>
Risk: Optional periodic scheduling can create recurring audits that read workspace instruction sources. <br>
Mitigation: Do not enable HEARTBEAT or cron scheduling unless recurring audits are specifically intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/korengast/contradiction-detector) <br>
- [Contradiction patterns](references/contradiction-patterns.md) <br>
- [Discovery procedure](references/discovery.md) <br>
- [Reporting and fixes](references/reporting-and-fixes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with evidence quotes, proposed diffs, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires review before applying fixes; reads OpenClaw workspace, skill, hook, and cron instruction sources.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
