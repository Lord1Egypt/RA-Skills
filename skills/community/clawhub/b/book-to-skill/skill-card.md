## Description: <br>
Book to Skill Converter analyzes uploaded books and turns core methods, mental models, and practical steps into reusable agent skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenshuo-03](https://clawhub.ai/user/shenshuo-03) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, agents, and knowledge workers use this skill to convert user-provided books into concise, reviewable skills that capture the book's most actionable methods, concepts, and thinking models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided books may contain content the user did not intend to process or reuse. <br>
Mitigation: Only provide books intended for analysis and reuse, and review extracted content before turning it into a skill. <br>
Risk: Generated skill files may preserve incorrect, overbroad, or misleading interpretations of the source book. <br>
Mitigation: Review generated skills before relying on them, sharing them, or saving them into an agent's skill library. <br>
Risk: The skill creates local files as part of its normal workflow. <br>
Mitigation: Choose the output folder deliberately and inspect generated files before deployment. <br>


## Reference(s): <br>
- [书籍分析指南](references/analysis_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown skill drafts, local skill files, and text extraction previews] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated skills should be reviewed before use or sharing; the extractor previews up to the first 10000 characters of source text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
