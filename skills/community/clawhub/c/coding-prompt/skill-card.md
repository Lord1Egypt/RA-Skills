## Description: <br>
AI coding prompt optimizer and coach for improving programming prompts, reviewing coding instructions, and detecting common prompt-related failure patterns during active coding sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neuhanli](https://clawhub.ai/user/neuhanli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn vague coding requests into clearer AI instructions with context, constraints, validation expectations, and output structure. It also helps monitor active coding sessions for high-priority issues such as placeholder implementations or hardcoded rule-based logic where LLM-native reasoning is more appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The update-skill flow can add incorrect, over-specific, or stale coding preferences to the learnings file. <br>
Mitigation: Review every proposed learning before approving the update-skill flow, and keep accepted entries reusable and concise. <br>
Risk: Session learnings could accidentally capture secrets, proprietary project details, or personal data. <br>
Mitigation: Do not save sensitive details into learnings.md; abstract lessons into general coding-prompt guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neuhanli/coding-prompt) <br>
- [Publisher profile](https://clawhub.ai/user/neuhanli) <br>
- [Anti-Pattern Quick Reference](references/anti-patterns.md) <br>
- [Prompt Diagnosis Checklist](references/checklist.md) <br>
- [Coding Prompt Learnings](references/learnings.md) <br>
- [Communication Patterns](references/patterns.md) <br>
- [Core Principles](references/principles.md) <br>
- [Structural Wisdom](references/structure.md) <br>
- [Workflow Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with diagnostic bullets, rewritten prompts, alerts, and structured proposals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include bilingual Chinese and English prompt guidance when triggered by the user's language or examples.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
