## Description: <br>
AutoDream Memory periodically organizes MEMORY.md and local memory files by deduplicating, merging, pruning stale entries, and producing consolidation reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigkingcn](https://clawhub.ai/user/bigkingcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to keep a workspace's long-term memory files organized, bounded, and easier for agents to load across repeated sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite persistent agent memory, which may remove or alter useful long-term context. <br>
Mitigation: Review or back up MEMORY.md and the memory directory before running, then inspect the generated report and pruned entries afterward. <br>
Risk: The documented dry-run safety control may not prevent all file writes. <br>
Mitigation: Test in a copied workspace or disposable memory directory before using it on active agent memory. <br>
Risk: The setup script can configure recurrence and also run the memory cycle immediately. <br>
Mitigation: Run the main cycle manually first and enable the setup script only after confirming recurring execution is desired. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bigkingcn/autodream-memory) <br>
- [AutoDream skill definition](artifact/SKILL.md) <br>
- [AutoDream README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports, JSON state and report files, configuration files, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes workspace memory files such as MEMORY.md and memory/autodream/*.json when run without dry-run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
