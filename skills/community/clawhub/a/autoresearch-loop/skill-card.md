## Description: <br>
Run an explicit, bounded modify-verify-decide loop toward a measurable metric with approval gates, scoped edits, and rollback proof. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leostehlik](https://clawhub.ai/user/leostehlik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to run a bounded iterative improvement process against a measurable goal, with explicit approval gates for commands, scope, rollback, external research, and iteration limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Iterative edits and command execution could affect private repositories, secrets, or proprietary data if the run contract is incomplete. <br>
Mitigation: Require explicit approval for scope, verify and guard commands, rollback strategy, external research policy, and private-data boundaries before starting. <br>
Risk: A change may improve the target metric while causing unrelated regressions. <br>
Mitigation: Run the approved guard command after every verification, keep one atomic change per iteration, and discard or rework changes that fail the guard. <br>
Risk: Background or unattended operation can drift from the approved goal or run longer than intended. <br>
Mitigation: Use foreground mode by default; require explicit approval, fixed scope, rollback strategy, progress cadence, and an iteration cap for background runs. <br>


## Reference(s): <br>
- [Autoresearch Loop on ClawHub](https://clawhub.ai/leostehlik/autoresearch-loop) <br>
- [Loop Protocol](references/loop-protocol.md) <br>
- [Pivot Protocol](references/pivot-protocol.md) <br>
- [Lessons Protocol](references/lessons-protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with command snippets, code edits, and structured run logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scoped iteration plans, verification and guard command use, keep/discard decisions, rollback notes, and lesson entries.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
