## Description: <br>
Extract and clean readable article content, metadata, and Markdown from URLs, raw HTML, or web page text for research, note-taking, and web scraping workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[extrastu](https://clawhub.ai/user/extrastu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to turn cluttered web pages or copied HTML into readable Markdown or structured metadata for downstream notes, datasets, and LLM processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Article cleaning may send private pages or copied HTML to an external parser if the agent uses the defuddle.md service. <br>
Mitigation: Before processing private or sensitive content, confirm whether the agent will use the external defuddle.md service, a local Defuddle CLI, or another approved parser. <br>


## Reference(s): <br>
- [Defuddle Reference](references/defuddle-usage.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/extrastu/defuddle) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown article content or structured JSON metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include title, author, site, description, published date, content, contentMarkdown, domain, favicon, image, wordCount, and parseTime when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
