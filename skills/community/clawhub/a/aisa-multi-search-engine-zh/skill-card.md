## Description: <br>
AISA Multi Search Engine ZH unifies web search, academic search, Tavily search and extraction, smart search, and Perplexity-style deep research through one AISA-powered skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to run web, academic, URL extraction, and multi-source research workflows through the AISA API when they need evidence gathering, market scanning, or due diligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, URL lists, and extracted page content are sent to AISA and may reach upstream search providers. <br>
Mitigation: Do not use this skill with secrets, private or internal URLs, regulated data, credentials, or confidential documents unless external sharing is approved. <br>
Risk: The skill requires an AISA_API_KEY credential. <br>
Mitigation: Store the API key in an approved environment or secret manager, avoid exposing it in prompts or logs, and rotate it if it is disclosed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/aisa-multi-search-engine-zh) <br>
- [AIsa API](https://aisa.one) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and CLI text search summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; search queries, URL lists, and extracted page content are sent to the external AISA API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
