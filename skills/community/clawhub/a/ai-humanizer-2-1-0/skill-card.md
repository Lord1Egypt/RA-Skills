## Description: <br>
Humanizes AI-generated text by detecting common LLM writing patterns, statistical signals, and vocabulary markers, then rewrites drafts to sound natural while preserving meaning and tone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hades4501](https://clawhub.ai/user/hades4501) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, writers, editors, and developers use this skill to evaluate drafts for AI-like writing patterns, get prioritized suggestions, and generate more natural rewrites or CLI analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users could apply the skill to hide AI authorship where disclosure is required. <br>
Mitigation: Use it as an editing aid only and follow school, workplace, publication, and platform disclosure rules. <br>
Risk: Installing the CLI without review could run untrusted local package contents. <br>
Mitigation: Verify the source and package contents before installing or running the CLI. <br>


## Reference(s): <br>
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) <br>
- [Copyleaks stylometric research](https://arxiv.org/abs/2503.01659) <br>
- [blader/humanizer reference implementation](https://github.com/blader/humanizer) <br>
- [AI vocabulary reference](references/ai-vocabulary.md) <br>
- [Pattern documentation](docs/PATTERNS.md) <br>
- [Examples](docs/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text rewrites, Markdown reports, JSON analysis, and command-line examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can provide scores, pattern findings, grouped suggestions, auto-fix text, and brief change summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact package.json reports 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
