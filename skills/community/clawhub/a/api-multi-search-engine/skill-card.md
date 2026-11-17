## Description:

Provides no-API search guidance across 17 Chinese and international search engines, including advanced operators, time filters, site search, privacy-oriented engines, and WolframAlpha queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kakaxiazai](https://clawhub.ai/user/kakaxiazai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to construct search URLs and web_fetch calls for broad web, site-specific, filetype, time-filtered, privacy-oriented, and knowledge-query searches without managing API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are disclosed to the selected external search provider.

Mitigation: Do not search for passwords, tokens, confidential company material, or personal data unless that disclosure is authorized and acceptable.

Risk: Cached or archived-result search examples may expose sensitive or unauthorized content.

Mitigation: Use cached or archived-result techniques only when authorized and appropriate for the investigation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kakaxiazai/skills/api-multi-search-engine)
- [International search guide](artifact/references/international-search.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with URL templates and inline web_fetch examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys required; queries are sent to the selected external search provider.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
