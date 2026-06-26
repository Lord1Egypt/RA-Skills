## Description: <br>
Compresses agent responses by removing filler, pleasantries, hedging, and excess grammar while preserving technical content, code, commands, URLs, file paths, and ordered steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freak30](https://clawhub.ai/user/freak30) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users apply this skill when they want terse, fragment-style answers that reduce tokens while keeping technical accuracy. It is especially suited to concise explanations, code review comments, commit messages, and compact implementation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Terse, fragment-style answers can omit nuance that matters in medical, legal, security, financial, or other high-stakes topics. <br>
Mitigation: Use the documented stop phrases or normal mode when nuance, caveats, or complete wording matters. <br>
Risk: Compression may make responses feel abrupt or less professional in contexts where tone is important. <br>
Mitigation: Use lite mode to drop filler while keeping grammar and professional wording. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freak30/caveman-xiaoz) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Concise natural language, Markdown, code snippets, shell commands, and configuration guidance depending on the user's request.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses lite, full, and ultra compression modes; normal wording can be restored with the documented stop phrases.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
