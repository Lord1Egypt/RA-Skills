## Description: <br>
OpenClaw-native executable content extraction skill for URLs, Feishu, YouTube, and web pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halfmoon82](https://clawhub.ai/user/halfmoon82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn supported URLs and documents into clean Markdown, with routing for WeChat, Feishu/Lark, YouTube transcripts, and generic web pages. It is useful for article cleanup, document export, transcript preparation, summarization, and local archiving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provided URLs and documents may be accessed through browser, Feishu, transcript, web-fetch, or generic fallback tools. <br>
Mitigation: Use the skill only for content you are authorized to process, and avoid confidential documents when generic URL fallbacks are involved. <br>
Risk: Long extracted content may be saved as local Markdown files. <br>
Mitigation: Review or delete saved extraction files when handling sensitive material. <br>
Risk: Fallback extraction can produce partial or lower-quality content if preferred routes fail. <br>
Mitigation: Check the reported failure layer and fallback path before relying on extracted content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/halfmoon82/content-extraction) <br>
- [README](artifact/README.md) <br>
- [Block to Markdown mapping](artifact/notes/block-to-markdown.md) <br>
- [Executor specification](artifact/notes/executor-spec.md) <br>
- [Extraction examples](artifact/notes/extraction-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown extraction output, optional JSON route/spec output, and local Markdown files for long content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes supported sources before extraction, preserves source metadata when available, reports fallback failures, and includes a save path when content is written locally.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
