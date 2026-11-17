## Description:

Agent Daily Paper helps users subscribe to recent arXiv papers across one or more research fields, rank them for relevance, and receive bilingual Markdown digests with titles, abstracts, arXiv links, status flags, and Chinese paper interpretations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricardo-ping](https://clawhub.ai/user/ricardo-ping)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and technical teams use this skill to configure field-based arXiv subscriptions and receive scheduled or on-demand bilingual Markdown digests. It supports local taxonomy-assisted field resolution, relevance filtering, NEW/UPDATED flags, Markdown archiving, and optional PDF-based Chinese interpretations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled local or optional remote automation can run digest jobs and write generated Markdown or state changes.

Mitigation: Review the scheduled task or workflow before enabling it, confirm the subscription timezone and push time, and run manually until configuration is verified.

Risk: The skill performs network queries to arXiv and can optionally send content to OpenAI when that translation or profile provider is enabled.

Mitigation: Use the default offline Argos translation path for sensitive work, and avoid TRANSLATE_PROVIDER=auto or openai unless third-party processing is acceptable.

Risk: Dependency and model setup can install packages or local models whose versions may change over time.

Mitigation: Pin dependencies and model versions in controlled environments before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ricardo-ping/skills/agent-daily-paper)
- [arXiv category taxonomy](https://arxiv.org/category_taxonomy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown digest output with setup commands and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write Markdown archives under output/daily and update local configuration or state files during setup and digest runs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
