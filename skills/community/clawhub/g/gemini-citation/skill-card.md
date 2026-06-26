## Description: <br>
Conduct evidence-based research with exact, accurate APA citations using the Gemini API's Google Search grounding feature for factual research summaries, literature reviews, and source-linked evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoxh](https://clawhub.ai/user/guoxh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and research assistants use this skill to run Gemini-powered research queries that return APA-formatted answers and auditable source URLs. It is suited for literature reviews, fact-checking, and academic writing workflows that need cited, search-grounded evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts are sent to Google's Gemini API using a Gemini API key. <br>
Mitigation: Avoid entering secrets, personal data, proprietary material, or regulated information unless the deployment policy permits it. <br>
Risk: Generated citations and claims may be incomplete or incorrect even when search grounding is enabled. <br>
Mitigation: Manually verify important claims against the returned source URLs before relying on the output. <br>


## Reference(s): <br>
- [Google AI Studio API key setup](https://aistudio.google.com/app/apikey) <br>
- [Gemini Citation on ClawHub](https://clawhub.ai/guoxh/gemini-citation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown text or JSON with generated answer text and source metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY and sends research prompts to Google's Gemini API with Google Search grounding enabled.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
