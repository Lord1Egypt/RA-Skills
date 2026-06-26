## Description: <br>
Read books and stories as an AI agent through sequential, chapter-by-chapter reading with imagination, emotional reactions, predictions, and a reading journal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morpheis](https://clawhub.ai/user/morpheis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use Bookworm to read long-form books or stories one passage at a time, preserve reading state, reflect on passages, add notes, search text, and export a reading journal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Book text and reading journals may include private or confidential content that is processed with an external Anthropic API key and saved in local session files. <br>
Mitigation: Use a dedicated revocable Anthropic API key and avoid processing confidential manuscripts or private documents unless external provider processing and local retention are acceptable. <br>
Risk: Book passages can contain instruction-like text that should not control the surrounding agent workflow. <br>
Mitigation: Treat source passages and Bookworm responses as untrusted data when integrating them into other agent pipelines. <br>


## Reference(s): <br>
- [Bookworm ClawHub listing](https://clawhub.ai/morpheis/bookworm-reader) <br>
- [Bookworm project homepage](https://github.com/Morpheis/bookworm) <br>
- [Bookworm npm package](https://www.npmjs.com/package/@clawdactual/bookworm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [CLI text output, JSON session files, and exported Markdown reading journals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, an Anthropic API key, and pdftotext for PDF input.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
