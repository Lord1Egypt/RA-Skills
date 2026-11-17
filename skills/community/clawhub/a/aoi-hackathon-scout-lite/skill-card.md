## Description:

Public-safe hackathon source registry and filtering output for hackathons, builder programs, and grants, with no crawling or submissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edmonddantesj](https://clawhub.ai/user/edmonddantesj)

### License/Terms of Use:

MIT

## Use Case:

Developers, builders, and operators use this skill to list, filter, and shortlist public hackathon or funding sources from local registry files, then generate paste-ready planning text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Brave Search setup stores a search API key in OpenClaw configuration.

Mitigation: Review whether Brave Search is needed, use a scoped key if enabled, and disable web search again when it is no longer required.

Risk: Recommendations are best-effort and depend on locally maintained registry and shortlist files.

Mitigation: Confirm deadlines, eligibility, and application details on the source site before making submission decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edmonddantesj/skills/aoi-hackathon-scout-lite)
- [Devpost Artificial Intelligence Hackathons](https://devpost.com/c/artificial-intelligence)
- [Brave Search API](https://brave.com/search/api/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON command output and Markdown text with shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local context registry and shortlist files; optional Brave Search setup can be disabled.]

## Skill Version(s):

0.1.6 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
