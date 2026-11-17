## Description:

软件架构4+1视图自动生成器可分析代码文件或工程目录，并生成逻辑、过程、物理、开发和场景视图以及 README 文档，全部使用 Mermaid 图渲染。

This skill is ready for commercial/non-commercial use.

## Publisher:

[langlitaosha80](https://clawhub.ai/user/langlitaosha80)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software engineers use this skill to generate 4+1 architecture documentation from source files or project directories. It is intended to create Mermaid-based architecture views that help explain static structure, runtime flows, deployment topology, module organization, and key scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated architecture diagrams may contain source-derived details that are sent to public Mermaid services during validation.

Mitigation: Review before installing on private or regulated codebases, and only use external Mermaid validation when sending diagram content to public services is acceptable.

Risk: Architecture metadata may be persisted in .claude/arc4plus1-cache/.

Mitigation: Clear or disable the cache when retained architecture metadata is sensitive.

Risk: The fallback Mermaid validation path can use an unpinned npx package.

Mitigation: Avoid the npx fallback unless the package version is pinned or the required Mermaid CLI is preinstalled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/langlitaosha80/skills/arc4plus1)
- [Mermaid Live](https://mermaid.live)
- [Mermaid image rendering endpoint](https://mermaid.ink/img/base64?code=<base64>)
- [Mermaid syntax parse endpoint](https://mermaid.live/api/v1/syntax/parse)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown files containing Mermaid code blocks plus a README document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes architecture documentation under an arcview directory and may include inferred architecture notes when source evidence is incomplete.]

## Skill Version(s):

1.1.4 (source: server release metadata; artifact frontmatter and package.json report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
