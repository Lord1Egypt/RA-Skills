## Description: <br>
Beauty Diagram helps agents use the `bd` CLI to render, export, share, or generate polished Mermaid and PlantUML diagrams as SVG, PNG, and hosted diagram links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[levi840714](https://clawhub.ai/user/levi840714) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and agents use this skill to convert Mermaid or PlantUML sources into polished diagram assets, create share links, embed diagrams in Markdown, and optionally generate Mermaid source from a text description. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The npm CLI sends diagram source or AI prompts to the external Beauty Diagram service. <br>
Mitigation: Review source and prompt sensitivity before invoking the CLI, and use the workflow only when external processing is acceptable. <br>
Risk: Share and embed workflows can create externally hosted diagram URLs and may edit Markdown files. <br>
Mitigation: Prefer local SVG or PNG outputs for sensitive material, confirm share/embed intent before creating hosted URLs, and review repository diffs after Markdown edits. <br>
Risk: Authenticated workflows require a Beauty Diagram API key and, for AI generation, an `ai:write` scope on a Pro or Premium plan. <br>
Mitigation: Use the minimum required credential scope, avoid exposing tokens in command output or files, and surface authentication, plan, or quota errors directly to the user. <br>


## Reference(s): <br>
- [Beauty Diagram ClawHub release](https://clawhub.ai/levi840714/beauty-diagram) <br>
- [Beauty Diagram website](https://www.beauty-diagram.com) <br>
- [Beauty Diagram CLI on npm](https://www.npmjs.com/package/@beauty-diagram/cli) <br>
- [Beauty Diagram API keys](https://www.beauty-diagram.com/account/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated Mermaid, SVG, PNG, or hosted diagram URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write editable diagram source files, rendered image files, Markdown image references, or share/embed URLs depending on the requested workflow.] <br>

## Skill Version(s): <br>
1.6.1 (source: frontmatter, package.json, changelog, ClawHub release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
