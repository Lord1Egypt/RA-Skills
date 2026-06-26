## Description: <br>
Fetches daily classical Chinese poetry, painting-caption quotes, and notable excerpts from gushiwen.cn and formats them into a concise message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Enchograph](https://clawhub.ai/user/Enchograph) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users invoke this skill when they ask for daily classical Chinese poetry, selected ancient-text recommendations, or gushiwen.cn homepage highlights. The skill gathers the current public content and returns a readable message with poems, painting-caption quotes, notable excerpts, and optional image media references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to gushiwen.cn and related public image URLs when daily or selected classical-poetry content is requested. <br>
Mitigation: Install only if this network access is acceptable, and prefer scoped fetch mechanisms for deployments that restrict shell-based web access. <br>
Risk: Fetched homepage content changes over time and may be parsed incorrectly or become unavailable. <br>
Mitigation: Review the generated message before redistribution when accuracy or presentation quality matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Enchograph/daily-gushiwen) <br>
- [Gushiwen homepage](https://www.gushiwen.cn/) <br>
- [Parsing guide](references/parsing-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Media URLs] <br>
**Output Format:** [Structured Markdown-style message with section separators and optional image media references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Content is based on the current gushiwen.cn homepage and should be kept concise rather than reproducing long classical texts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
