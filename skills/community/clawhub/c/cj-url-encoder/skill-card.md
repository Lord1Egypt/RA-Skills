## Description: <br>
快速对文本或 URL 进行 Encode (编码) 和 Decode (解码) 操作，解决中文乱码和特殊字符传输问题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lapidcj](https://clawhub.ai/user/lapidcj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and general users use this skill to URL-encode or URL-decode text, links, query strings, Chinese characters, spaces, and special symbols for API requests, shared links, and readable inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic encode or decode phrasing may trigger the skill for non-URL text. <br>
Mitigation: Ask explicitly for URL or percent encoding or decoding when precision matters. <br>
Risk: Prompt text provided for encoding or decoding may contain sensitive values. <br>
Mitigation: Avoid pasting secrets unless the agent environment is approved to process that text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lapidcj/cj-url-encoder) <br>
- [Publisher profile](https://clawhub.ai/user/lapidcj) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code] <br>
**Output Format:** [Markdown with encoded or decoded string results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Python standard-library URL percent encoding and decoding; no external dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
