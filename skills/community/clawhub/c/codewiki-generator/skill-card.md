## Description: <br>
Generate a deep, code-first project wiki and VitePress documentation site (DeepWiki-style) for a repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samzong](https://clawhub.ai/user/samzong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a repository and generate a source-derived documentation site with structured Markdown, Mermaid diagrams, VitePress navigation, and metadata for auditing coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated documentation and metadata can expose project structure, dependencies, symbols, and copied local images. <br>
Mitigation: Review codewiki/ and codewiki/.meta/ before committing, sharing, or deploying the generated site. <br>
Risk: The bundled VitePress package template uses unpinned documentation dependencies, which can affect reproducibility. <br>
Mitigation: Pin npm dependency versions before relying on repeated or controlled builds. <br>
Risk: The optional Cloudflare Pages workflow publishes the generated documentation externally. <br>
Mitigation: Use the deployment workflow only when the documentation is intended to be public or otherwise approved for publication. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samzong/codewiki-generator) <br>
- [Structure and Heuristics](references/structure-and-heuristics.md) <br>
- [Deep Doc Templates](references/doc-templates.md) <br>
- [Deploy to Cloudflare Pages](references/deploy-cloudflare.md) <br>
- [Multi-language Support](references/i18n-setup.md) <br>
- [Evidence Rules](references/evidence-rules.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown files, JSON metadata, VitePress configuration, Mermaid diagrams, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local codewiki/ documentation site and codewiki/.meta/ analysis outputs; optional workflows can publish the generated site or add i18n.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
