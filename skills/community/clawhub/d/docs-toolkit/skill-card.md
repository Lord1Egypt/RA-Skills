## Description:

文档助手工具 helps agents answer SkillHub documentation questions, navigate documentation decision trees, and assist with document handling, conversion, and information extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operations teams use this skill to quickly find SkillHub documentation answers, route setup or troubleshooting questions to relevant documentation areas, and summarize document-processing results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution and write capability even though its main purpose is documentation guidance.

Mitigation: Install with read-only or limited permissions unless command and write access are explicitly needed and reviewed for the target environment.

Risk: The artifact includes an unclear script-running instruction that is not scoped or explained.

Mitigation: Require review of any generated shell command or script invocation before execution, and avoid running unspecified scripts from the skill.

Risk: Documentation answers or conversion guidance may be inaccurate or outdated.

Mitigation: Verify important answers against linked documentation or project-maintained sources before applying configuration changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/docs-toolkit)
- [Discord provider documentation](https://docs.clawd.bot/providers/discord)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include documentation links, configuration snippets, execution summaries, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 1.2.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
