## Description: <br>
Deslop diagnoses and rewrites Chinese or English prose that reads like AI-generated text, using a two-pass process to remove stock patterns and restore voice while preserving the original facts and argument. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, reviewers, and documentation teams use Deslop to score and revise articles, documents, blog posts, and sharing drafts that feel generic or AI-written. It is not intended for code comments, commit messages, academic rewriting, or pure document generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rewrites can shift tone, author intent, or factual emphasis, especially in sensitive, formal, or voice-dependent documents. <br>
Mitigation: Review the final text against the source before accepting it, and keep uncertain edits marked for user confirmation. <br>
Risk: Private or confidential source text may be processed by the agent environment when the skill is used. <br>
Mitigation: Avoid submitting private material unless the agent environment is approved for that content. <br>


## Reference(s): <br>
- [Deslop ClawHub release](https://clawhub.ai/lanyasheng/deslop-cn) <br>
- [Complete pattern catalog](references/full-pattern-catalog.md) <br>
- [Chinese AI vs human writing examples](references/writing-patterns-zh.md) <br>
- [Scenario tone guide and quick fixes](references/tone-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with scores, rewritten passages, residual-pattern notes, and a change log] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Two-pass rewrite workflow; score-only mode may return analysis without rewritten text.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
