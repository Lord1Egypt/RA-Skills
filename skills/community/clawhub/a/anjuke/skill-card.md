## Description: <br>
Provides structured information from Anjuke public pages, including property listings, agent rules, services, and help documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeclaw007](https://clawhub.ai/user/mikeclaw007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to summarize public Anjuke real estate pages, service entry points, agent rules, consultation flows, and help-center information while preserving city, listing, and timing context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Anjuke listing, pricing, city, service, or policy details may be time-sensitive or location-specific. <br>
Mitigation: Verify important details against the original Anjuke page before relying on or publishing the summary. <br>
Risk: The skill could be asked to process private, account-only, owner, broker-backend, or unpublished listing information outside its stated boundary. <br>
Mitigation: Use the skill only with public Anjuke pages and exclude account data, non-public listings, private owner data, and broker-backend content. <br>
Risk: Real estate summaries can become misleading if source context is dropped or if users request false listings, audit evasion, or off-platform transaction guidance. <br>
Mitigation: Preserve city, listing, service-entry, and timing context, and decline false listing, review-evasion, or noncompliant transaction guidance. <br>


## Reference(s): <br>
- [Anjuke public homepage](https://www.anjuke.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries and structured public-information guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should retain source context such as city, listing, service entry point, date-sensitive details, and relevant public links.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
