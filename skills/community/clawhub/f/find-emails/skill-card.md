## Description:

Crawl websites locally with crawl4ai to extract contact emails, accept multiple URLs, and output domain-grouped results for clear attribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukem121](https://clawhub.ai/user/lukem121)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to crawl specified websites or inspect local markdown files for contact email addresses. It is intended for contact discovery workflows where results need to remain grouped by source domain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs broad outbound crawling of user-supplied websites and installs crawler/browser dependencies.

Mitigation: Review before installing, run in an isolated environment with restricted outbound network access, and prefer pinned dependencies or a locked environment.

Risk: Extracted email addresses are contact or personal data and may be subject to website terms and applicable law.

Mitigation: Avoid internal or sensitive URLs, save outputs only to intended locations, and handle extracted emails according to applicable policy and law.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lukem121/skills/find-emails)
- [Publisher profile](https://clawhub.ai/user/lukem121)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration]

**Output Format:** [Markdown-style terminal text or JSON, optionally written to a file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs email addresses grouped by source domain with page paths when available.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
