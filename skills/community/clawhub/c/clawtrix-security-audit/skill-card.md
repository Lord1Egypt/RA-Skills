## Description:

Audits an agent's installed ClawHub skill stack for mission-specific security risks, flags risky skills and publisher trust issues, and writes a local risk report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicope](https://clawhub.ai/user/nicope)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and security reviewers use this skill to audit installed ClawHub skills before installation, during periodic reviews, or after incidents. It inventories skills, checks risk patterns, applies mission-specific blast-radius scoring, and summarizes findings in a Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit data may be sent to ClawHub, HN/Algolia, or Paperclip as part of metadata checks, comment searches, and critical-finding escalation.

Mitigation: Review the skill before installation and require explicit approval before network calls or external notifications, especially when skill names or incident details are sensitive.

Risk: The skill writes local audit and incident reports under memory/reports/.

Mitigation: Confirm report paths and retention expectations before running it in environments where audit results may contain sensitive operational context.

Risk: Recommendations may be vendor-biased because the artifact says it never recommends competitor tools and promotes Clawtrix Pro.

Mitigation: Treat recommendations as advisory, review alternatives independently, and avoid forced upgrade or removal actions without human approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicope/skills/clawtrix-security-audit)
- [ClawHub publisher profile](https://clawhub.ai/user/nicope)
- [ClawHub skill metadata API endpoint used by the skill](https://clawhub.ai/api/v1/skills/{slug})
- [HN Algolia search endpoint used by the skill](https://hn.algolia.com/api/v1/search?query={skill_name}+malware&tags=story&hitsPerPage=5)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown risk report with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes audit reports under memory/reports/ and may include recommendations for flagged skills.]

## Skill Version(s):

0.3.0 (source: server release metadata and artifact version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
