## Description: <br>
Extract metadata and content from WeChat Official Account articles, including titles, authors, article HTML, publish times, cover images, account details, and supported article types such as posts, videos, images, voice messages, and reposts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abigale-cyber](https://clawhub.ai/user/abigale-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content workflow agents use this skill to extract structured metadata, article content, account information, media links, and error states from WeChat Official Account URLs or supplied article HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched or supplied article HTML can trigger dynamic JavaScript evaluation during extraction. <br>
Mitigation: Run the skill in a constrained environment and avoid untrusted HTML until dynamic evaluation is removed or sandboxed. <br>
Risk: URL handling and hostname checks may not be tight enough for sensitive browsing contexts. <br>
Mitigation: Use only intended WeChat and Sogou article URLs, and tighten hostname validation before broader deployment. <br>
Risk: The bundled convert.js helper contains hard-coded local input and output paths. <br>
Mitigation: Remove the helper or change it to require explicit user-provided paths before using it in shared or automated environments. <br>
Risk: Some dependencies are outdated or deprecated according to the artifact lockfile. <br>
Mitigation: Update dependencies and rerun security review before production deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/abigale-cyber/content-system-wechat-article-extractor-skill) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Markdown] <br>
**Output Format:** [Structured JSON-compatible extraction result with article metadata, account details, HTML content, content insights, engagement fields when visible, or error codes; the helper script can convert extracted content to Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access for URL extraction and may return null fields when WeChat page structure or access restrictions prevent extraction.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
