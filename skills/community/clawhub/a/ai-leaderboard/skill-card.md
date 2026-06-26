## Description: <br>
Comprehensive AI leaderboard for LLM models and AI applications that queries model rankings, model IDs, and pricing from OpenRouter, Artificial Analysis, and Pinchbench. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luduoxin](https://clawhub.ai/user/luduoxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and AI evaluators use this skill to retrieve current model and application leaderboard data, compare model performance, find OpenRouter model IDs, and inspect pricing or free-model options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can invoke browser automation and visit external ranking sites while retrieving live leaderboard data. <br>
Mitigation: Use a non-sensitive browser context for automated page access and review fetched results before relying on them. <br>
Risk: Leaderboard and pricing data are retrieved from external sources and may change over time. <br>
Mitigation: Treat outputs as current lookups from the cited sources and re-run the skill when making time-sensitive comparisons. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luduoxin/ai-leaderboard) <br>
- [Artificial Analysis](https://artificialanalysis.ai/) <br>
- [Artificial Analysis LLM Leaderboard](https://artificialanalysis.ai/leaderboards/models) <br>
- [Artificial Analysis API Providers Leaderboard](https://artificialanalysis.ai/leaderboards/providers) <br>
- [OpenRouter Rankings](https://openrouter.ai/rankings) <br>
- [OpenRouter Apps](https://openrouter.ai/apps) <br>
- [OpenRouter Models](https://openrouter.ai/models) <br>
- [Pinchbench](https://pinchbench.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with ranking tables, model IDs, pricing notes, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use browser automation or public API calls to retrieve current external leaderboard data.] <br>

## Skill Version(s): <br>
1.20.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
