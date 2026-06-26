## Description: <br>
Use when diagnosing or improving frontend performance, Core Web Vitals, bundle size, runtime rendering cost, network waterfalls, memory leaks, long tasks, Lighthouse findings, or performance budgets; Chinese triggers include 性能优化, 页面卡顿, 首屏慢, 包体积, Web Vitals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and frontend engineers use this skill to diagnose web performance issues and produce evidence-based recommendations for Core Web Vitals, bundle size, rendering cost, network waterfalls, memory leaks, and validation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to inspect private monitoring dashboards, CI artifacts, production traces, or repository data during performance analysis. <br>
Mitigation: Use it only where the agent is authorized to inspect that data and limit access to the routes, artifacts, and metrics needed for the review. <br>
Risk: Performance recommendations can be misleading when made without measurements or scoped reproduction steps. <br>
Mitigation: Require baselines and post-change validation before relying on optimization guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bovinphang/fec-performance-optimization) <br>
- [Framework Performance Patterns](references/framework-performance-patterns.md) <br>
- [Performance Report Template](references/report-template.md) <br>
- [Frontend Craft homepage](https://github.com/bovinphang/frontend-craft) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown performance analysis report with validation commands and evidence-linked recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The expected report includes baseline metrics, candidate gating, bottleneck analysis, optimization recommendations, validation comparison, and remaining risks.] <br>

## Skill Version(s): <br>
2.7.0 (source: server evidence release.version, metadata.json, package.json, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
