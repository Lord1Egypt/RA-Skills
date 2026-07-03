## Description: <br>
Translate technical & legal documents while preserving original formatting, terminology consistency, and domain context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to translate technical, legal, marketing, and general documents while preserving structure, glossary terms, code blocks, links, tables, and bilingual review formats. Review is especially important for legal or high-stakes translations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may report a successful translation even when no real translation was produced or the source document was copied unchanged. <br>
Mitigation: Before relying on outputs, compare source and generated files, spot-check translated segments, and require human review for technical, legal, or publication use. <br>
Risk: Legal or high-stakes translations may be inaccurate or uncertified. <br>
Mitigation: Use the output only as a review aid and require a qualified translator or legal reviewer before relying on it. <br>


## Reference(s): <br>
- [Domain Translation Modes](artifact/references/domain-modes.json) <br>
- [Input Schema](artifact/schemas/input.schema.json) <br>
- [Output Schema](artifact/schemas/output.schema.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/document-translation-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and CLI text with optional JSON-shaped translation, glossary, and consistency-report outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can describe translated document segments, glossary terms, consistency checks, and format-preservation reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
