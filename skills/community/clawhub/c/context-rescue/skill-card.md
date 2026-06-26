## Description: <br>
Create a thread-based recovery summary when an agent loses the thread. Read the relevant conversation and canonical files, summarize what was done, where it is documented, and what the real next step is, then write a compressed reorientation snapshot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wroadd](https://clawhub.ai/user/wroadd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to recover orientation in long, fragmented, or resumed work threads. It reads the relevant conversation and canonical project-state files, produces a focused reorientation summary, writes a `state/ORIENT.md` snapshot, and stops before implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads current thread and project-state files that may contain sensitive work context. <br>
Mitigation: Install it only in workspaces where the agent may read those materials, as recommended by the security guidance. <br>
Risk: The skill creates or updates `state/ORIENT.md`, which may replace prior orientation notes. <br>
Mitigation: Check `state/ORIENT.md` before use when preserving previous orientation notes matters. <br>
Risk: A recovery summary can become misleading when thread memory and canonical files disagree. <br>
Mitigation: Follow the skill rule to prefer file truth and explicitly call out conflicts. <br>


## Reference(s): <br>
- [Context Rescue on ClawHub](https://clawhub.ai/wroadd/context-rescue) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Files] <br>
**Output Format:** [Markdown summary and `state/ORIENT.md` snapshot] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill writes one disclosed orientation snapshot and instructs the agent to stop before executing the next step.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
