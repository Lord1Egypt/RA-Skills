## Description: <br>
Multi-source verification with confidence ratings for factual claims, statistics, research questions, and discovery tasks that require cross-checking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marianachow0321](https://clawhub.ai/user/marianachow0321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to verify claims across multiple sources, compare source credibility, resolve conflicting evidence, and present confidence-rated answers with citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verification or discovery prompts may be sent to the configured OpenClaw web search provider. <br>
Mitigation: Avoid confidential private claims, internal business details, or sensitive personal information unless that provider is approved for those queries. <br>
Risk: Broad activation wording may trigger the skill more often than some users expect. <br>
Mitigation: Use clear user intent for verification workflows and review generated source lists before relying on the answer. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/marianachow0321/fact-cross-check) <br>
- [Query Optimization](references/query-optimization.md) <br>
- [Research Patterns](references/research-patterns.md) <br>
- [Source Credibility Tiers](references/source-tiers.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with confidence ratings, source links, verification dates, and caveats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires direct clickable source URLs for cited sources] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
