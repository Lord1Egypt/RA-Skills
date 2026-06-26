## Description: <br>
Actively monitors token utilization and executes memory compaction routines before context bloat causes failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ElMoorish](https://clawhub.ai/user/ElMoorish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to compact OpenClaw memory state when context pressure rises. It prompts a dense progress summary, archives the active daily memory log, and can configure OpenClaw compaction defaults. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify OpenClaw local memory state by moving the active daily memory log and replacing it with a compacted file. <br>
Mitigation: Review the archive path before use and back up important local memory state before invoking the flush action. <br>
Risk: The included configuration script can rewrite OpenClaw compaction defaults. <br>
Mitigation: Run the configuration script only when those defaults are intended, and inspect the existing OpenClaw configuration before and after the change. <br>
Risk: The server security verdict is suspicious because local state changes and configuration changes have limited user-facing disclosure. <br>
Mitigation: Review the included scripts and ClawHub security guidance before installing or deploying the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ElMoorish/cognitive-compaction) <br>
- [Publisher Profile](https://clawhub.ai/user/ElMoorish) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>
- [OpenClaw Configuration Script](artifact/scripts/configure_openclaw.py) <br>
- [State Flush Script](artifact/scripts/flush_state.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with command output and local file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can archive the active OpenClaw daily memory log and rewrite OpenClaw compaction defaults when invoked.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
