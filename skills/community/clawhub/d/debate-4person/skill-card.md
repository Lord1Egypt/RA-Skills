## Description: <br>
四人制标准辩论工具，AI 扮演正反方 8 名辩手，按立论→攻辩→总结流程辩论，支持打断、评委点评打分。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[woqigeshenmemingzibijiaoheshine](https://clawhub.ai/user/woqigeshenmemingzibijiaoheshine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to run a structured four-person debate simulation with affirmative and negative teams, optional web-search-supported arguments, interruption handling, and judge scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Web-search-backed debate queries may be sent to Tavily when TAVILY_API_KEY is configured. <br>
Mitigation: Use non-sensitive debate topics when web search is enabled. <br>
Risk: Generated statistics, citations, or argumentative claims may be incorrect or misleading. <br>
Mitigation: Verify important statistics and citations before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/woqigeshenmemingzibijiaoheshine/debate-4person) <br>
- [Publisher profile](https://clawhub.ai/user/woqigeshenmemingzibijiaoheshine) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style conversational debate transcript with judge feedback and scores] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use Tavily web search when TAVILY_API_KEY is configured; otherwise falls back to model knowledge.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
