## Description: <br>
Read-only Calibre catalog lookup and one-book analysis-comments workflow over a running Calibre Content server, including ID-based viewing requests while excluding title, author, tag, series, and other metadata edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nextaltair](https://clawhub.ai/user/nextaltair) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Calibre library operators use this skill to let an agent inspect a Calibre library, answer list/search/ID lookup questions, and run one-book text analysis that can write analysis HTML back to Calibre comments when explicitly invoked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled extracted book-text cache files may expose copyrighted or private library content. <br>
Mitigation: Remove bundled state/cache files before installation or use, and clear cached text or database artifacts when analysis data is no longer needed. <br>
Risk: The workflow requires Calibre Content Server credentials and can write analysis HTML to the comments metadata field. <br>
Mitigation: Use a least-privilege Calibre account, restrict .env file permissions, avoid plaintext password arguments where possible, and review comments-write behavior before enabling the analysis apply workflow. <br>


## Reference(s): <br>
- [Calibre Catalog Read on ClawHub](https://clawhub.ai/nextaltair/calibre-catalog-read) <br>
- [Subagent analysis prompt](references/subagent-analysis.prompt.md) <br>
- [Subagent input schema](references/subagent-input.schema.json) <br>
- [Subagent analysis output schema](references/subagent-analysis.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON catalog or analysis outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [One-book analysis runs produce schema-conformant JSON and may update Calibre comments metadata after completion.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
