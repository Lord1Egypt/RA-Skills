## Description: <br>
Reads content from URLs or files, classifies it, and generates structured summaries and comments in a specific, analytical style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blackshady1130-jpg](https://clawhub.ai/user/blackshady1130-jpg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and analysts use this skill to process articles, papers, news, URLs, PDFs, and local text files into a concise Markdown review with classification, source metadata, a key takeaway, and critical commentary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The PDF reading workflow may involve shell-based download and text extraction for user-provided URLs or paths. <br>
Mitigation: Use safer PDF or file-reading tools when available, avoid untrusted PDF URLs and sensitive local paths, and require agents to quote and constrain shell arguments. <br>
Risk: Generated reviews may be persuasive or critical commentary rather than neutral summaries. <br>
Mitigation: Review the output against the source material before using it for publication, investment, research, or operational decisions. <br>


## Reference(s): <br>
- [AI-review ClawHub release](https://clawhub.ai/blackshady1130-jpg/ai-review) <br>
- [Style Guide: Opinion/Article](references/style_guide_article.md) <br>
- [Style Guide: Industry News/Commentary](references/style_guide_industry.md) <br>
- [Style Guide: Solid Paper](references/style_guide_paper.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown table with classification, date, title, source, takeaway, and comments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Comments follow one of three bundled style guides for articles, papers, or industry commentary.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
