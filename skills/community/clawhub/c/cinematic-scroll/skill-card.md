## Description: <br>
Builds cinematic scroll-driven websites and audits scroll experiences using reusable parallax, 3D tilt, pinned reveal, design-token, and verification workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mustbesimo](https://clawhub.ai/user/mustbesimo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and design engineers use this skill to build cinematic scroll sections, launch pages, product stories, editorial microsites, and Next.js release sites. They can also use its audit mode to score authorized pages for pacing, performance, accessibility, and emotional arc. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional fal.ai generation and other networked workflows may upload prompts, assets, or page content to third-party services. <br>
Mitigation: Use your own fal.ai key, avoid private customer data in generation or capture workflows, and run networked modes only when those data flows are acceptable. <br>
Risk: Generated pages may load CDN-hosted scripts, fonts, or model assets at runtime. <br>
Mitigation: Self-host fonts, scripts, and model assets when deployment policy forbids third-party CDN calls. <br>
Risk: Secrets such as FAL_KEY can be exposed if committed with generated project files. <br>
Mitigation: Keep secrets in gitignored environment files or a secret manager and review generated files before committing. <br>
Risk: Audit and screenshot capture workflows can process sensitive page content. <br>
Mitigation: Run audits only on sites you own or are authorized to test and avoid pages containing private customer data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mustbesimo/skills/cinematic-scroll) <br>
- [Design Contract](artifact/design.md) <br>
- [Taste Guardrails](artifact/taste-guardrails.md) <br>
- [Scroll Patterns](artifact/references/scroll-patterns.md) <br>
- [Component Grammar](artifact/references/component-grammar.md) <br>
- [Performance Budget](artifact/references/performance-budget.md) <br>
- [3D Stack](artifact/references/3d-stack.md) <br>
- [fal.ai](https://fal.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML, CSS, TypeScript, JSON artifacts, and optional shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce reviewable build artifacts such as cinematic-audit.md, motion-storyboard.md, technical-spec.md, code output, and polish-report.md.] <br>

## Skill Version(s): <br>
2.5.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
