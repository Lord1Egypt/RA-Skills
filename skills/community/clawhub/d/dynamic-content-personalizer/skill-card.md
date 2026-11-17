## Description:

Helps agents add an email personalization layer by mapping merge tags to real export columns with fallbacks, defining segment-specific conditional blocks, auditing broken renders, and guarding PII exposure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and agents use this skill to personalize existing email creative for B2C lifecycle, B2B outbound, or newsletter campaigns. It produces a merge-tag and fallback map, segment conditional rules, a fallback-safety audit, and a PII guard for the rendered email body.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may receive email creative, segment names, export column names, and aggregate fill-rate data that reveal marketing strategy or customer-data structure.

Mitigation: Provide only the minimum fields needed for personalization, prefer aggregate fill-rate data, and avoid raw subscriber rows unless they are necessary.

Risk: Raw subscriber rows or visible PII could be echoed into personalization specs or saved memory if supplied unnecessarily.

Mitigation: Use column names and aggregate rules instead of member-level rows, redact direct identifiers, and review saved memory entries before reuse.

Risk: Missing fallbacks or incomplete conditional branches can create broken email renders such as empty greetings, dangling punctuation, or blank content blocks.

Mitigation: Require an explicit fallback for every merge tag, a catch-all else branch for every conditional block, and a worst-case fallback-safety audit before send handoff.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/dynamic-content-personalizer)
- [Publisher profile](https://clawhub.ai/user/aaron-he-zhu)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown personalization specification with structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes merge-tag bindings, rendered fallbacks, conditional block rules, fallback-safety audit notes, PII guard decisions, and a handoff summary.]

## Skill Version(s):

19.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
