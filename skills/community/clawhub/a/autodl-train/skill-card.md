## Description:

Operates remote model training jobs on AutoDL Linux servers over SSH.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuoran-liu](https://clawhub.ai/user/zhuoran-liu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML engineers use this skill to start, monitor, diagnose, and summarize remote training runs on configured AutoDL Linux servers. It helps inspect job status, GPU/CPU/memory/disk pressure, recent logs, common failures, and checkpoint-oriented next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SSH-based scripts can exceed the intended project-folder boundary when configuration is too broad.

Mitigation: Review the scripts before installation and use a dedicated non-root SSH account constrained to the training project with narrowly scoped project_path and allowed_project_roots.

Risk: Status and log checks may inspect unrelated workloads or sensitive logs on shared servers.

Mitigation: Use the skill only against appropriate training servers, keep log_path and log_candidates relative to the project, and set a specific process_match or train_command.

Risk: Password-based SSH can increase credential exposure risk.

Mitigation: Prefer key-based SSH; if password mode is unavoidable, provide AUTOCLAW_TRAIN_SSH_PASSWORD through the environment or an uncommitted local .env file.

## Reference(s):

- [Usage Guide](artifact/references/usage.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/zhuoran-liu/skills/autodl-train)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, JSON, Guidance]

**Output Format:** [Markdown summaries with command snippets and optional JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include remote job status, resource summaries, log excerpts, parsed training metrics, failure hints, and recommended next steps.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
