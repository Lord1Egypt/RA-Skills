## Description: <br>
Use when a complex problem needs a structured expert team rather than a single general answer. Runs a Single-CEO Expert Council with a Nuwa-style decision lens, Agency-style specialist selection, NEXUS handoffs, evidence-backed expert reports, and a verification layer before final synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wei840222](https://clawhub.ai/user/wei840222) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and strategy operators use this skill to route complex decisions through a small expert council that decomposes the problem, gathers evidence, verifies claims, and produces a final recommendation with assumptions, disagreements, and next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Initializing optional source assets can create local files and clone external GitHub repositories. <br>
Mitigation: Run the bootstrap only when explicitly needed, review or pin the referenced repositories first, and keep the cloned assets out of committed skill artifacts. <br>
Risk: Expert reports can overstate claims if evidence is weak, stale, or unavailable. <br>
Mitigation: Require each specialist to cite evidence or label assumptions, and require the verification layer to return PASS, FAIL, or PARTIAL before final synthesis. <br>
Risk: A poorly scoped handoff could permit edits, commits, pushes, deploys, or other external mutations during a read-only task. <br>
Mitigation: State allowed tools and forbidden actions in every handoff, and require explicit user authorization before any external mutation. <br>


## Reference(s): <br>
- [AI Expert Team on ClawHub](https://clawhub.ai/wei840222/skills/ai-expert-team) <br>
- [Publisher profile](https://clawhub.ai/user/wei840222) <br>
- [Source Research Snapshot](references/source-research-snapshot.md) <br>
- [CEO Profiles](references/ceo-profiles.md) <br>
- [Specialist Selection](references/specialist-selection.md) <br>
- [Validation Case Library](references/validation-case-library.md) <br>
- [Validation Cycle Closure](references/validation-cycle-closure.md) <br>
- [Expert Handoff Template](templates/expert-handoff.md) <br>
- [Final Synthesis Template](templates/final-synthesis.md) <br>
- [Agency Agents source asset](https://github.com/msitarzewski/agency-agents.git) <br>
- [Nuwa Skill source asset](https://github.com/alchaincyf/nuwa-skill.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with structured expert reports, verification verdicts, and final synthesis sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PASS, FAIL, or PARTIAL verification verdicts; separates verified findings, assumptions, disagreements, open risks, and next actions.] <br>

## Skill Version(s): <br>
0.1.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
