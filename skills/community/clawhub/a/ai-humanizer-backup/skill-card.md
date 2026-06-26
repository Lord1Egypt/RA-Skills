## Description: <br>
Humanizes AI-generated text by detecting common LLM writing patterns, scoring drafts, and suggesting or applying edits that make writing sound more natural while preserving meaning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wings229](https://clawhub.ai/user/wings229) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External writers, editors, and developers use this skill to review text for AI-writing patterns, generate human-facing rewrite guidance, and apply mechanical fixes to drafts. It can also provide agent prompt guidance for consistently less formulaic writing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI-authorship scores may be treated as proof even though the evidence warns against relying on them that way. <br>
Mitigation: Present scores as editorial signals only and require human review before using them for policy, academic, workplace, or publication decisions. <br>
Risk: Rewrite mode could be used to misrepresent AI-assisted work or evade disclosure rules. <br>
Mitigation: Use the skill for transparent editing and comply with school, workplace, platform, and publication disclosure requirements. <br>
Risk: The CLI can read or edit files that a user points it at. <br>
Mitigation: Run it only on intended draft files and review any auto-fixed output before replacing source material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wings229/ai-humanizer-backup) <br>
- [Publisher profile](https://clawhub.ai/user/wings229) <br>
- [AI vocabulary reference](references/ai-vocabulary.md) <br>
- [Pattern reference](references/patterns.md) <br>
- [Writing style guide](references/style-guide.md) <br>
- [Pattern documentation](docs/PATTERNS.md) <br>
- [Examples](docs/EXAMPLES.md) <br>
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) <br>
- [Copyleaks stylometric research](https://arxiv.org/abs/2503.01659) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, Markdown reports, JSON analysis, inline shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read text from stdin or user-specified files and may produce rewrite suggestions, analysis scores, or auto-fixed text.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
