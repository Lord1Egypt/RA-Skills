## Description: <br>
Provides real-time car research, comparison, pricing, configuration, owner-review, and buying-advice workflows using current public sources instead of stale model knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deusyu](https://clawhub.ai/user/deusyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer car-buying, model-comparison, configuration, pricing, review, and market-data questions with current public web sources. It is most useful when vehicle details, prices, or buyer recommendations may be time-sensitive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle prices, trims, specifications, availability, incentives, and sales rankings change frequently. <br>
Mitigation: Use live public sources for time-sensitive claims and tell users to verify purchase decisions against official manufacturer or dealer sources. <br>
Risk: Owner reviews and media evaluations can be subjective or incomplete. <br>
Mitigation: Separate objective specifications from subjective feedback, summarize review patterns, and cite the source and collection time. <br>
Risk: Automotive research can invite users to share unnecessary personal or financial details. <br>
Mitigation: Avoid requesting personal details unless needed for the comparison and keep recommendations framed around user-stated preferences. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deusyu/car-advisor) <br>
- [Publisher profile](https://clawhub.ai/user/deusyu) <br>
- [Data sources reference](references/data-sources.md) <br>
- [Comparison dimensions reference](references/compare-dimensions.md) <br>
- [Tesla Model Y](https://www.tesla.cn/modely) <br>
- [Tesla Model 3](https://www.tesla.cn/model3) <br>
- [Xiaomi EV](https://www.xiaomiev.com) <br>
- [AITO](https://www.aito.com) <br>
- [Li Auto](https://www.lixiang.com) <br>
- [Dongchedi parameter pages](https://www.dongchedi.com/auto/params-carIds-x-{series_id}) <br>
- [Dongchedi sales ranking](https://www.dongchedi.com/auto/market/car/rank) <br>
- [Autohome configuration comparison](https://www.autohome.com.cn/config/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured comparison tables, summaries, source notes, and buying recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include data sources and collection time when current vehicle facts, prices, reviews, or market data are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
