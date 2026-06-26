## Description: <br>
Agent Memory Tiers helps OpenClaw agents maintain concise L0 state snapshots and L1 rolling context files so each activation starts with current state and recent task history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DirtyRootsStudio](https://clawhub.ai/user/DirtyRootsStudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add lightweight local memory to OpenClaw agents, reducing startup context gathering and improving continuity across repeated activations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory files can carry stale, misleading, or unreviewed instructions into future agent runs. <br>
Mitigation: Keep L0.md and L1.md concise, periodically review memory instructions, and remove stale blockers or outdated state during each end-of-run update. <br>
Risk: Local memory files may accidentally retain secrets or sensitive operational details. <br>
Mitigation: Do not store secrets, API credentials, or sensitive data in L0.md or L1.md; limit entries to necessary status summaries. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown templates and setup guidance for L0.md, L1.md, and SOUL.md memory instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory guidance and file templates; no network or external API access required.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
