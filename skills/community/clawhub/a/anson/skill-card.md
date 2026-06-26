## Description: <br>
Bootstrap and personalize an AI assistant with a rich, bespoke identity, user profile, and soul. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edmundworks](https://clawhub.ai/user/edmundworks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Anson to bootstrap a personalized assistant by guiding setup, interviewing for identity, user, and working-relationship context, and generating durable Markdown profile and instruction files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill builds persistent personal profile files and assistant instruction files that can shape future agent behavior. <br>
Mitigation: Review ANSON_META.md, generated profile files, and AGENTS.md or CLAUDE.md changes before relying on them. <br>
Risk: The bootstrap workflow may inspect broad workspace context, memory files, history files, and existing project files. <br>
Mitigation: Run it in a reviewed workspace and require explicit approval before reading memory or history files or unrelated project context. <br>
Risk: The skill can generate additional maker skills and alter future assistant instructions. <br>
Mitigation: Inspect and scan generated skills, then require explicit user confirmation before installing or executing them. <br>


## Reference(s): <br>
- [Bootstrap Process](references/bootstrap-process.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [Anthropic Skills Repository](https://github.com/anthropics/skills) <br>
- [Anson on ClawHub](https://clawhub.ai/edmundworks/anson) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Conversational guidance plus Markdown files, configuration instructions, and skill scaffolds.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates workspace files such as ANSON_META.md, IDENTITY.md, USER.md, SOUL.md, AGENTS.md or CLAUDE.md, and maker skill scaffolds when run with user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
