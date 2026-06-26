## Description: <br>
Aggregates current AI news from public web sources, ranks items by heat, and outputs a Chinese summary with original links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kkblock](https://clawhub.ai/user/kkblock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams tracking AI industry developments use this skill to run multi-source public web searches and produce a Chinese, heat-ranked roundup of current AI news with source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public web searches can surface outdated, incomplete, or misleading AI news. <br>
Mitigation: Verify important items against the linked original sources before relying on the roundup. <br>
Risk: The workflow is designed for public-source news gathering, not private or internal research. <br>
Mitigation: Use it only for public AI-news monitoring unless the user explicitly wants public web collection for the task. <br>


## Reference(s): <br>
- [Recommended AI news sources](artifact/references/sources.md) <br>
- [ClawHub release page](https://clawhub.ai/kkblock/ai-news-collectors-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown Chinese news roundup with ranked sections and source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets 15-25 items, grouped by heat rating, with a search coverage summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
