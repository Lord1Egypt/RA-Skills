## Description: <br>
Extract web page content from a URL using Felo Web Extract API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to extract webpage content from a URL as markdown, text, HTML, or JSON for downstream summarization, capture, or processing. It supports focused extraction with CSS selectors and readability mode for article-style pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Target URLs and extraction options are sent to Felo's external API. <br>
Mitigation: Use the skill only for URLs you are comfortable sharing with Felo, and avoid private, authenticated, signed, localhost, intranet, cloud-metadata, or otherwise sensitive URLs. <br>
Risk: Changing FELO_API_BASE can route requests and API-key-authenticated traffic to a different service. <br>
Mitigation: Keep FELO_API_BASE at the trusted default unless there is an intentional, reviewed reason to change it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangzhiming1999/felo-web-extract) <br>
- [Felo Web Extract API](https://openapi.felo.ai/docs/api-reference/v2/web-extract.html) <br>
- [Felo Open Platform](https://openapi.felo.ai/docs/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, plain text, HTML, JSON, and shell commands depending on the requested extraction mode.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FELO_API_KEY and sends the requested URL plus extraction options to Felo's external API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
