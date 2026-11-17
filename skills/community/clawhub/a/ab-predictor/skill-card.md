## Description:

Predicts which ad hook, email subject, or social post is likely to perform best by scoring variants against audience-specific profiles, confidence intervals, rewrite suggestions, cross-ICP comparisons, and quality gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivenautoplex1](https://clawhub.ai/user/drivenautoplex1)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, sales, and growth teams use this skill to compare ad hooks, email subjects, and social posts before committing budget or scheduling campaigns. It helps agents rank variants, explain why a likely winner is stronger, and suggest targeted rewrites for lower-scoring copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may execute an unverified sibling scorer module when that directory is present.

Mitigation: Install and run it only where the sibling content-resonance-scorer directory is trusted or absent, and review the environment before use.

Risk: The skill gives targeted advertising and messaging recommendations for regulated or sensitive financial, mortgage, veteran, and credit-repair contexts.

Mitigation: Have qualified reviewers check generated recommendations for policy, legal, and platform compliance before using them in campaigns.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/drivenautoplex1/skills/ab-predictor)
- [Publisher Profile](https://clawhub.ai/user/drivenautoplex1)
- [Project Homepage](https://github.com/drivenautoplex1/openclaw-skills)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown-style CLI text or JSON, depending on flags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ranked scores, confidence intervals, flags, rewrite suggestions, and optional cross-audience comparisons.]

## Skill Version(s):

2.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
