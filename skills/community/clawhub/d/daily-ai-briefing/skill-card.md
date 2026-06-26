## Description: <br>
每日AI硬核进展简报的质量规范与执行流程。定义红线规则、搜索策略、信息源、提纯标准、自检清单和输出模板。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tino-chen](https://clawhub.ai/user/tino-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and developers use this skill to compile a Chinese daily AI briefing from recent, source-checked research, industry news, and open-source project updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow browses public AI news sources, so dated claims, source eligibility, and GitHub star counts can become stale or be misread. <br>
Mitigation: Review the generated briefing's dates, source links, and repository metadata before relying on or publishing it. <br>
Risk: The workflow creates, reads, and writes briefing files under ~/Desktop/daily_ai_briefing. <br>
Mitigation: Keep that folder limited to intended briefing files and check for an existing same-date file before overwriting a prior draft. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tino-chen/daily-ai-briefing) <br>
- [Daily AI Briefing guide](https://tino-chen.github.io/notes/workflows/daily-ai-briefing.html) <br>
- [Focused source list](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a dated Chinese AI briefing and, when executed as written, saves it under ~/Desktop/daily_ai_briefing.] <br>

## Skill Version(s): <br>
1.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
