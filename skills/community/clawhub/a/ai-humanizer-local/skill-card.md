## Description: <br>
Humanize AI-generated text by detecting common LLM writing patterns, scoring draft text, and suggesting or applying rewrites that sound more natural. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wings229](https://clawhub.ai/user/wings229) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and developers use this skill to review drafts for AI-like phrasing, generate scores and reports, and produce targeted rewrite suggestions while preserving the original meaning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unreviewed rewrites may change meaning, emphasis, or tone. <br>
Mitigation: Review rewritten text against the source before publishing. <br>
Risk: Always-on writing rules can affect future agent responses broadly. <br>
Mitigation: Add always-on guidance only when this writing style preference should apply beyond one draft. <br>
Risk: Local analysis requires the tool to read supplied documents. <br>
Mitigation: Process only documents intended for the tool to inspect. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wings229/ai-humanizer-local) <br>
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) <br>
- [Copyleaks stylometric fingerprint research](https://arxiv.org/abs/2503.01659) <br>
- [Pattern documentation](docs/PATTERNS.md) <br>
- [AI vocabulary reference](references/ai-vocabulary.md) <br>
- [Pattern reference](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text rewrites, Markdown reports, JSON analysis output, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reviews local text input and may produce rewrite suggestions or autofixed text; users should review output before publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
