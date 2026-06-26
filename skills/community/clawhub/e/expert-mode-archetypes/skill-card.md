## Description: <br>
AI expert panel, specialist advisor, technical review, thoughtful critique, and decision-support system for OpenClaw projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[e1red](https://clawhub.ai/user/e1red) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to activate project-local expert archetypes for technical review, risk critique, strategy, planning, prompt engineering advice, customer experience guidance, and decision support. It can select or create reusable expert rosters and dossiers, then synthesize concise or deep advisory responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read project notes and create or update project-local expert roster and dossier files. <br>
Mitigation: Install it only when project-local advisory file access is acceptable, and ask the agent to confirm before making file changes outside the experts/ folder. <br>
Risk: Generated expert dossiers can become stale, include sensitive project context, or exert too much influence on later advice. <br>
Mitigation: Periodically review experts/roster.md and experts/dossiers/*.md for freshness, sensitivity, and appropriate advisory boundaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/e1red/expert-mode-archetypes) <br>
- [Activation workflow](references/activation-workflow.md) <br>
- [Archetype buckets](references/archetype-buckets.md) <br>
- [Custom expert request mode](references/custom-expert-request-mode.md) <br>
- [Dossier schema](references/dossier-schema.md) <br>
- [Expert selection taxonomy](references/expert-selection-taxonomy.md) <br>
- [Prominent expert track](references/prominent-expert-track.md) <br>
- [Response depth modes](references/response-depth-modes.md) <br>
- [Retrieval policy](references/retrieval-policy.md) <br>
- [Top-notch expert behaviour](references/top-notch-expert-behaviour.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, advisory synthesis, project-local roster and dossier Markdown files, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports quick, standard, deep, and custom-length response modes; may create or update experts/roster.md and experts/dossiers/*.md when appropriate.] <br>

## Skill Version(s): <br>
0.9.0 (source: server release metadata; artifact SKILL.md reports 0.9.0-expert-quality-and-depth-modes) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
