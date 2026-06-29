## Description: <br>
Processes EPUB files into structured extraction JSON, guides paragraph-aligned translation and summary filling, and assembles bilingual EPUBs with source-first reading order, preserved assets, target-language summaries, and report.txt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lywhlao2025](https://clawhub.ai/user/lywhlao2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and EPUB maintainers use this skill to convert books, magazines, newsletters, Calibre-generated EPUBs, and article collections into bilingual editions while preserving source order, assets, table-of-contents behavior, and one-to-one paragraph alignment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes the EPUB text supplied by the user, which may include private or copyrighted book content. <br>
Mitigation: Use the skill only with content the user is comfortable processing in the active agent session, and avoid external translation providers unless the user explicitly approves sending the content to that provider. <br>
Risk: Generated extraction, summary, report, and EPUB files are written to an output directory. <br>
Mitigation: Use a dedicated output folder for each conversion so generated files are isolated from unrelated user files. <br>
Risk: Large EPUB translations may consume substantial model context or tokens. <br>
Mitigation: Run the token estimate first, show it to the user, and wait for post-estimate confirmation before beginning translation work. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lywhlao2025/epub-bilingual-convert-skill) <br>
- [Resumable Translation Batches Design](docs/superpowers/specs/2026-05-31-resumable-translation-batches-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON/file output contracts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces extraction.json, bilingual EPUB files, target-language summary text files, and report.txt through local Python scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
