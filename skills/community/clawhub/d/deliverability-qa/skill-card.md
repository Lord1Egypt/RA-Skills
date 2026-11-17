## Description:

Runs a one-time email deliverability pre-flight for SPF, DKIM, DMARC, BIMI, domain and IP reputation, inbox placement, campaign content, links, rendering, and point-in-time bounce and complaint hygiene.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, email operations, and growth teams use this skill before a send or scale-up to identify authentication, reputation, placement, content, and list-hygiene gaps. It produces a SEND-S deliverability evidence read and flags S1 authentication status without computing final EQS or veto verdicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to share email deliverability materials, including DNS and DMARC evidence, ESP reports, reputation data, seed-test results, and campaign HTML.

Mitigation: Installers should confirm that sharing these materials is acceptable for their program before using the skill.

Risk: Optional API-key use and memory or consent-record writes may retain or access account-specific information.

Mitigation: Review optional API-key use before enabling it and approve memory saves or consent-record writes only when retention is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/deliverability-qa)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Deliverability Pre-flight Checklist](references/deliverability-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown with structured item states and evidence gaps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports Pass, Partial, Fail, Unknown, or N/A per item and only emits a SEND-S score when all applicable coverage is present.]

## Skill Version(s):

19.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
