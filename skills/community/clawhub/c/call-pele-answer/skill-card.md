## Description:

把回答按内容分块，选择合适的文字、表格、图表或交互组件，并生成可调色和批注的离线讲解页。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dotpopo](https://clawhub.ai/user/dotpopo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn explanations, comparisons, diagnostics, and procedures into structured Markdown and offline interactive pages. It is intended for answers where diagrams or other structured views can improve understanding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Answer content may be sent to external classification services, and the security review raises activity and capability concerns with incomplete component analysis.

Mitigation: Avoid use with confidential answer content until external classification can be disabled, self-hosted routing behavior is clarified, and activity logging limits are reviewed; assess the components not fully analyzed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dotpopo/skills/call-pele-answer)
- [Project homepage](https://github.com/dotpopo/call-pele-answer)
- [CLI and router guide](references/cli.md)
- [Routing guide](references/routing.md)
- [Page customization guide](references/page.md)

## Skill Output:

**Output Type(s):** [Markdown, HTML]

**Output Format:** [Markdown manuscript and offline interactive HTML page]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The page can include diagrams, interactive views, color controls, and annotations.]

## Skill Version(s):

0.5.10 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
