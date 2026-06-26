## Description: <br>
Archon is a personal AI assistant for technical managers that runs in an AI IDE, stores data in local Markdown files, and supports daily logs, decisions, team signals, coaching, meeting preparation, periodic reviews, and priority project management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sopaco](https://clawhub.ai/user/sopaco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Technical managers use Archon to maintain a private workspace of management notes, daily logs, decisions, team signals, coaching records, meeting preparation, and priority project reviews. It is intended for personalized decision support and operating cadence management in a local AI IDE workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad natural-language triggers can start workflows that read or change sensitive management notes. <br>
Mitigation: Install only in a private workspace and narrow triggers or require explicit Archon-prefixed commands before broader use. <br>
Risk: Profile, daily-log, coaching, signal, and project files may contain personal or organizational context. <br>
Mitigation: Require confirmation before profile or daily-log mutations and review proposed file changes before retaining them. <br>
Risk: The bundled behavior is tailored to the Sopaco publisher profile and boss context. <br>
Mitigation: Replace Sopaco-specific profile and organization context before using the skill for another person or team. <br>


## Reference(s): <br>
- [Archon Agent Prompts](references/prompts.md) <br>
- [Archon File Schemas](references/schemas.md) <br>
- [Archon Brain ClawHub Release](https://clawhub.ai/sopaco/archon) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance, Configuration] <br>
**Output Format:** [Markdown with YAML frontmatter, structured reports, and concise conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local workspace records for daily logs, decisions, coaching notes, signals, meeting preparation, and project reviews after user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence, created 2026-05-01) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
