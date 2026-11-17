## Description:

CodeRules is a Chinese-language coding-standards assistant that detects a project's technology stack, loads matching language and framework rules, guides compliant code generation, reviews existing code, and helps fix non-compliant code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoxulaila](https://clawhub.ai/user/xiaoxulaila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to apply project-specific coding standards when generating, reviewing, fixing, or initializing code. It is especially suited to teams that want Chinese-language guidance for TypeScript, Python, Go, React, Vue, and Next.js conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad coding requests because its trigger scope includes general code generation and review prompts.

Mitigation: Use it when coding-standards enforcement is desired, and review the selected rules before applying generated changes.

Risk: Some advertised technology stacks are not backed by shipped rule files in the artifact.

Mitigation: Confirm that a matching rule file exists for the target language or framework, and fall back to general coding rules where coverage is missing.

Risk: The default guidance is Chinese-language and may not be localized for all users.

Mitigation: Ask the agent to translate or summarize the selected rules when the user or reviewer needs another language.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoxulaila/skills/coderules)
- [Publisher profile](https://clawhub.ai/user/xiaoxulaila)
- [Skill definition](artifact/SKILL.md)
- [CodeRules rule index](artifact/rules/index.json)
- [Project analyzer](artifact/scripts/analyzer.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks, file lists, rule summaries, generated code, and self-checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project analysis results and recommendations based on local project metadata and bundled rule files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
