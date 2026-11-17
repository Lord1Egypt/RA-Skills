## Description:

Automates a court-themed task workflow for receiving commands, auditing intent, managing token budgets, scheduling ComfyUI image and video jobs, and recording monitoring and audit evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fenzyh](https://clawhub.ai/user/fenzyh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run an auditable task pipeline that turns user instructions into reviewed, budgeted, scheduled ComfyUI jobs. It records task archives, token ledgers, execution status, monitoring events, and audit reports for follow-up review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weak filesystem scoping could leak local JSON data or write files outside intended task folders.

Mitigation: Run with a tightly scoped PROJECT_ROOT, validate task IDs, and generate safe local output filenames.

Risk: External ComfyUI or agent connections could expose data or accept untrusted traffic.

Mitigation: Use only trusted ComfyUI servers, require HTTPS and authentication, and keep external agent endpoints narrowly configured.

Risk: The recurring scheduler can process queued tasks automatically before task approval and rate limits are in place.

Mitigation: Disable the recurring scheduler until explicit task approval, rate limits, and operational controls are configured.

Risk: Workflow files and dependencies may introduce unsafe behavior if accepted broadly or left stale.

Mitigation: Restrict workflow files to an allowlisted workflows directory and update or remove risky dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fenzyh/skills/daming-core)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [HYBRID_ARCHITECTURE.md](artifact/HYBRID_ARCHITECTURE.md)
- [JINYIWEI_GUIDE.md](artifact/JINYIWEI_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON files, Markdown reports, console text, and Python or shell usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write task archives, token ledgers, execution records, statistics, logs, and downloaded ComfyUI output files under the configured project root.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact skill.json reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
