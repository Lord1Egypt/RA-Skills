## Description:

Detects Douyin and short-video sensitive, prohibited, traffic-limiting, advertising-risk, and medical-risk terms in Chinese copy using a local word list with optional daily updates from public GitHub word-list sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yourlin](https://clawhub.ai/user/yourlin)

### License/Terms of Use:

MIT

## Use Case:

External creators, marketers, and agent users use this skill to check short-video scripts, livestream talking points, and promotional copy for words that may create platform, advertising, or content-compliance risk before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill can provide advice for disguising flagged wording to get content past moderation.

Mitigation: Use it as a compliance review aid and require human review of any rewrite guidance so edits reduce policy risk rather than evade moderation.

Risk: The security summary says the skill automatically trusts mutable third-party GitHub word lists.

Mitigation: Disable or manually control updates when reproducible checks are required, and treat downloaded word lists as non-authoritative inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yourlin/skills/douyin-sensitive-check)
- [Open-source word-list sources](references/word_sources.md)
- [konsheng/Sensitive-lexicon](https://github.com/konsheng/Sensitive-lexicon)
- [bigdata-labs/sensitive-stop-words](https://github.com/bigdata-labs/sensitive-stop-words)
- [jkiss/sensitive-words](https://github.com/jkiss/sensitive-words)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Terminal text and agent-facing guidance with highlighted matched terms and context snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read from stdin, a command-line string, or a local text file; may update a local word-list cache once per day when network access is available.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
