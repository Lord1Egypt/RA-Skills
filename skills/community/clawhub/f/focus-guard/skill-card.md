## Description: <br>
Session coherence protocol for Claude \u2014 track decisions, resist scope creep, flag drift. Keeps long AI sessions on track without losing what was already decided. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and collaborative AI users use Focus Guard to keep multi-step Claude sessions aligned with the agreed goal, decisions, and scope. It is most useful for longer debugging, refactoring, migration, or planning sessions where context drift and unapproved scope expansion would be costly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Additional scope checks and decision-log prompts can become noisy for quick tasks. <br>
Mitigation: Use the skill for multi-step or high-stakes sessions and disable or skip it for quick one-shot tasks. <br>
Risk: The scope gate may pause legitimate new work until the user confirms a scope change. <br>
Mitigation: Confirm intentional scope expansion explicitly, then continue with the updated session anchor and decision log. <br>


## Reference(s): <br>
- [Focus Guard on ClawHub](https://clawhub.ai/jiajiaoy/focus-guard) <br>
- [Skill homepage](https://clawhub.ai/skills/focus-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown text with session anchors, decision logs, scope flags, progress check-ins, and close summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; no files, network calls, credentials, or code execution requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
