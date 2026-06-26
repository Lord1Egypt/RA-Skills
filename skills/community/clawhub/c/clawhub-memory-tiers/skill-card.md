## Description: <br>
Clawhub Memory Tiers gives OpenClaw agents startup context through self-updating L0 and L1 markdown memory files so they can resume recent work without re-reading larger history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DirtyRootsStudio](https://clawhub.ai/user/DirtyRootsStudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add lightweight persistent memory to OpenClaw agents through L0.md and L1.md files. It helps agents resume work with current focus, recent activity, active tasks, key state, and blockers without re-reading larger history on every activation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent L0.md and L1.md files may retain secrets, credentials, private personal data, or untrusted instructions that future agent runs rely on. <br>
Mitigation: Keep memory files free of secrets and private data, avoid storing untrusted instructions, and review the files periodically. <br>
Risk: Outdated or inaccurate memory entries can steer later agent runs toward stale priorities, stale blockers, or incorrect state. <br>
Mitigation: Update L0.md and L1.md before every activation ends, keep L1 to the most recent seven days, and remove resolved blockers promptly. <br>
Risk: Shared memory files can cause task collisions or incorrect cross-agent state in multi-agent setups. <br>
Mitigation: Give each agent its own L0.md and L1.md, and let orchestrators read other agents' memory files without writing to them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DirtyRootsStudio/clawhub-memory-tiers) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown instructions and templates for agent memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and maintains local L0.md and L1.md memory files in each agent workspace; no network or external API access is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
