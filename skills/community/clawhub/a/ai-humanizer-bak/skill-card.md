## Description: <br>
Humanize AI-generated text by detecting common LLM writing patterns, scoring text with vocabulary and statistical signals, and suggesting more natural rewrites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sp012lk](https://clawhub.ai/user/sp012lk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and writing-focused agents use this skill to review drafts for AI-like patterns, generate scores and reports, and produce concrete humanization suggestions or safer mechanical rewrites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI-writing scores are heuristic and may be overconfident. <br>
Mitigation: Use scores as editing signals, not as sole evidence for academic, employment, moderation, compliance, or authorship decisions. <br>
Risk: Humanization rewrites may remove useful factual caveats or limitation disclosures. <br>
Mitigation: Review rewritten text and preserve factual limitations, uncertainty, and source context when they matter. <br>
Risk: Always-on prompt templates can create persistent style influence across unrelated work. <br>
Mitigation: Enable always-on behavior only when the agent is intentionally expected to write in this style. <br>


## Reference(s): <br>
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) <br>
- [Copyleaks stylometric research](https://arxiv.org/abs/2503.01659) <br>
- [Pattern reference](references/patterns.md) <br>
- [AI vocabulary reference](references/ai-vocabulary.md) <br>
- [Humanizer style guide](references/style-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text, Markdown reports, JSON analysis, and suggested rewrite guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scores text from 0-100, lists detected patterns and statistics, and can propose or apply safe mechanical fixes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
