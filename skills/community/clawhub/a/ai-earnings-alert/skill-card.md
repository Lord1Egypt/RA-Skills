## Description: <br>
Tracks technology and AI company earnings activity, retrieves earnings calendars and news, generates summary reports, and supports earnings alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newaiguy](https://clawhub.ai/user/newaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to help users monitor earnings dates, news, and summaries for tracked technology and AI companies. It is suited for earnings watchlists and alert workflows, but the source states that outputs are informational and not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Earnings queries are sent to Tavily and translated content may be sent to BigModel/GLM. <br>
Mitigation: Use the skill only with data that is acceptable to share with those providers, and use dedicated Tavily and ZAI credentials. <br>
Risk: The translation path can use OPENAI_API_KEY as a fallback credential. <br>
Mitigation: Run without OPENAI_API_KEY in the environment unless that fallback is explicitly approved or removed. <br>
Risk: The package includes an unused Playwright dependency that security evidence flags for review. <br>
Mitigation: Remove the dependency if browser automation is not needed, or upgrade it before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/newaiguy/ai-earnings-alert) <br>
- [Publisher profile](https://clawhub.ai/user/newaiguy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, Markdown summaries, and optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include translated earnings news, extracted financial metrics, relevance scores, tracked-company lists, and local configuration state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and manifest.json; package.json lists 2.1.0 and script documentation mentions v2.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
