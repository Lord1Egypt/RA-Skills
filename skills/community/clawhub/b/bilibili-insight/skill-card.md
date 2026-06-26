## Description: <br>
Analyzes public Bilibili creator profiles, video performance, audience attributes, and viral content patterns for creators, brands, and MCN teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[275254cl-hash](https://clawhub.ai/user/275254cl-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators, brands, and MCN teams use this skill to analyze public Bilibili creator, video, audience, and trending-content signals, then turn those insights into topic and competitive-monitoring guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creator and audience analytics can be misused to identify private individuals or infer sensitive traits. <br>
Mitigation: Limit use to public, aggregate insights and avoid identifying private people or making sensitive-trait inferences. <br>
Risk: Competitor monitoring or automated Bilibili queries may violate platform rules or privacy expectations. <br>
Mitigation: Use only allowed public data sources and respect Bilibili terms, rate limits, and consent expectations. <br>
Risk: The skill may install requests and make network queries through Python or curl. <br>
Mitigation: Review dependencies and commands before execution and run the workflow in a constrained environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/275254cl-hash/bilibili-insight) <br>
- [Publisher profile](https://clawhub.ai/user/275254cl-hash) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style analytical summaries with examples, recommendations, and public-data caveats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Python, curl, and the requests package for network-based public Bilibili analytics workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
