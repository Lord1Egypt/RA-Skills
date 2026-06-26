## Description: <br>
Inspect, checkpoint, rollback, and branch OpenClaw sessions with the ClawReverse plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BinHuangPJLAB](https://clawhub.ai/user/BinHuangPJLAB) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to inspect session checkpoints, recover from bad tool or file changes, restore known-good states, and branch session work without rerunning long tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checkpoints and registries may persist raw session transcripts, prompts, and tool outputs locally. <br>
Mitigation: Review session data sensitivity before installation, restrict local plugin storage access, and avoid using it on sessions containing secrets or regulated customer data unless local retention is acceptable. <br>
Risk: Continuing from a checkpoint can create durable child agents, workspaces, and sessions. <br>
Mitigation: Confirm the intended checkpoint and prompt before continuing, and clean up child workspaces and records according to local retention requirements. <br>
Risk: Rollback with workspace restoration can modify live workspace files. <br>
Mitigation: Require explicit user confirmation before using --restore-workspace and inspect the selected checkpoint or rollback report first. <br>


## Reference(s): <br>
- [ClawReverse homepage](https://github.com/OpenKILab/ClawReverse) <br>
- [ClawHub release page](https://clawhub.ai/BinHuangPJLAB/clawreverse-skill) <br>
- [Publisher profile](https://clawhub.ai/user/BinHuangPJLAB) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of the openclaw reverse command family and recommends --json when machine-readable output is needed.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
