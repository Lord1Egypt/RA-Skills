## Description: <br>
Professional AI stock and market analysis powered by investment expert models and integrated with the OpenClaw AI Agent. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[hengruiyun](https://clawhub.ai/user/hengruiyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw agents use this skill to request delayed market sentiment, sector momentum, capital-flow, quantitative screening, and stock diagnosis reports. It is suited for mid-to-long-term research and strategic verification, not high-frequency or real-time trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market, sector, and ticker queries are sent to the TTfox service. <br>
Mitigation: Inform users before external calls and avoid sending sensitive, personal, or confidential trading context. <br>
Risk: Returned buy/sell-style recommendations may be delayed research rather than personalized investment advice. <br>
Mitigation: Present results as research signals, include the delayed-data limitation, and advise users to verify information before making financial decisions. <br>
Risk: Broad finance prompts may invoke the skill and trigger external market lookups. <br>
Mitigation: Only call stock-specific analysis when the user explicitly requests market, sector, or ticker analysis. <br>


## Reference(s): <br>
- [AI Stock Master on ClawHub](https://clawhub.ai/hengruiyun/ai-stock-master) <br>
- [TTFox Intelligence Server](https://master.ttfox.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, API calls] <br>
**Output Format:** [Markdown-style analyst reports and structured status dictionaries from API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include market sentiment, sector rankings, stock recommendations, risk levels, and error messages from the TTfox service.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
