## Description: <br>
AutoDream-Core is an adapter-based memory consolidation engine for AI agents that deduplicates, merges, and prunes stale memory entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigkingcn](https://clawhub.ai/user/bigkingcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to consolidate long-running agent memories across OpenClaw or adapter-backed workspaces by scanning memory and session files, normalizing entries, deduplicating content, pruning stale items, and updating MEMORY.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session transcripts and memory files may contain sensitive workspace content. <br>
Mitigation: Install only in workspaces where scanning session transcripts and memory files is acceptable; start with a test workspace and review files written under memory/autodream. <br>
Risk: The skill rewrites MEMORY.md and can remove or merge entries during consolidation. <br>
Mitigation: Back up MEMORY.md before running, trigger the first run manually, and review the resulting memory changes before routine use. <br>
Risk: Local analytics logs may record usage events. <br>
Mitigation: Disable analytics in configuration when local usage logs are not wanted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bigkingcn/autodream-core) <br>
- [README.md](artifact/README.md) <br>
- [RELEASE_REPORT.md](artifact/RELEASE_REPORT.md) <br>
- [OpenClaw Docs](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown memory updates, JSON run summaries, JSONL analytics, and shell or Python usage snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Updates MEMORY.md and writes local state and analytics files under memory/autodream when enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
