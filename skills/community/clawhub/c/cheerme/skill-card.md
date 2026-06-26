## Description: <br>
Cheerme provides companion-style encouragement, warm support, goal planning, and personalized responses using configurable roles and regional dialects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oxoyo](https://clawhub.ai/user/oxoyo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use Cheerme to add encouragement, goal setting, progress support, and companion-style responses when a conversation shows self-doubt, anxiety, procrastination, low motivation, or a request for guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad auto-activation and companion framing could surprise users during sensitive conversations. <br>
Mitigation: Keep auto-mode off unless the user explicitly wants it, and review trigger behavior before deployment. <br>
Risk: Memory-oriented guidance may encourage retention or reuse of personal details. <br>
Mitigation: Avoid collecting highly sensitive information and confirm the host environment supports viewing, clearing, or disabling memory for this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oxoyo/cheerme) <br>
- [Publisher homepage](https://github.com/OXOYO/cheerme) <br>
- [Commands reference](references/commands.md) <br>
- [Output patterns reference](references/output-patterns.md) <br>
- [Workflows reference](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Conversational Markdown with optional progress tables and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include role-specific tone, regional dialect phrasing, goal plans, progress check-ins, and encouragement.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
