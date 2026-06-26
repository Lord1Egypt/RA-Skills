## Description: <br>
Use Gemini API Google Search grounding for web search inside OpenClaw, separate from local SearXNG. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psanger](https://clawhub.ai/user/psanger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when they need Google-backed Gemini Search Grounding for current, cited web answers, especially when local search is blocked, incomplete, or not appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Google's Gemini API and may consume Gemini quota or billing. <br>
Mitigation: Install only when this external API use is acceptable, and prefer local search for private or free search needs. <br>
Risk: The skill requires sensitive Gemini or Google API credentials. <br>
Mitigation: Use a least-privileged API key, keep keys out of logs, and pass an explicit 1Password field when using 1Password-backed credentials. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown-style answer text or JSON containing the query, model, answer, sources, and grounding metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include grounding source URLs when returned by Gemini.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
