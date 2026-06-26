## Description: <br>
AI Citation Content Writer helps agents draft AI-citable content assets such as FAQ pages, definition articles, comparison guides, how-to guides, and statistics roundups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geoly-geo](https://clawhub.ai/user/geoly-geo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External content marketers, SEO teams, and developers use this skill to create structured content drafts intended for AI search and assistant citations. It is suited for FAQ pages, definition articles, comparison guides, how-to guides, and statistics roundups that still require editorial review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documentation advertises batch and interactive commands that are not supported by the included artifact files. <br>
Mitigation: Use the included single-file generator command with explicit safe output filenames, and verify available scripts before relying on documented batch or interactive workflows. <br>
Risk: Generated content can contain placeholders or unsupported formats because the bundled generator only implements a definition template. <br>
Mitigation: Review and complete generated drafts before publication, especially for FAQ, comparison, how-to, and statistics content. <br>
Risk: AI-citable content may be misleading if source claims, statistics, or citations are not checked. <br>
Mitigation: Perform editorial and factual review before using the output in customer-facing or commercial content. <br>


## Reference(s): <br>
- [AI Vocabulary Blacklist](references/ai-vocabulary.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/geoly-geo/geo-citation-writer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown content templates with optional Python CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated drafts may include placeholders and should be reviewed before publication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
