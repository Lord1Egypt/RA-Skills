## Description: <br>
Detects trend signals for up to five keywords and classifies each as Rising, Peaking, Declining, or Insufficient_Data using web search and an LLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinu4you](https://clawhub.ai/user/jinu4you) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
External users and developers use this agent to compare keyword momentum over a selected timeframe and receive ranked trend classifications with evidence URLs and a short brief. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Entered keywords, generated search queries, and retrieved article snippets may be sent to Tavily and the selected LLM provider. <br>
Mitigation: Use only data approved for those providers and configure quota-limited API keys. <br>
Risk: Running npm start can execute the included sample job and make API calls when credentials are configured. <br>
Mitigation: Review runtime behavior before execution and run it only in controlled environments. <br>


## Reference(s): <br>
- [Agent Trend Radar on ClawHub](https://clawhub.ai/jinu4you/agent-trend-radar) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON] <br>
**Output Format:** [JSON result containing trend records, evidence URLs, and a brief text summary that may include Markdown emphasis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scores are sorted descending; each trend includes keyword, signal, score, reason, and evidence URL fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
