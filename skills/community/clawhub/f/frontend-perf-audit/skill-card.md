## Description:

帮助开发者诊断网页和 SPA 性能问题，并按 Core Web Vitals、资源加载、渲染阻塞、代码分割、图片懒加载、缓存策略和 Bundle 分析给出审计步骤。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenxiaoyu0124-web](https://clawhub.ai/user/chenxiaoyu0124-web)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and front-end engineers use this skill to audit slow web pages or SPAs, interpret Core Web Vitals symptoms, and plan improvements for loading, rendering, bundle size, images, and caching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Lighthouse command may resolve the latest package when run with `npx`.

Mitigation: Use a pinned Lighthouse version or a locally locked dependency workflow before running the command in sensitive projects.

Risk: Performance recommendations may be misprioritized if applied without project-specific measurements.

Mitigation: Validate changes with Lighthouse, Chrome DevTools, and project metrics before deploying optimizations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenxiaoyu0124-web/skills/frontend-perf-audit)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language performance checklist; includes optional Lighthouse command examples.]

## Skill Version(s):

1.1.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
