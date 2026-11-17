## Description:

Finds, shortlists, vets, and enriches US real-world engineering firms across civil, structural, MEP, mechanical, electrical, geotechnical, transportation, environmental, and manufacturing disciplines using the ServiceGraph pro_services dataset.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nostrband](https://clawhub.ai/user/nostrband)

### License/Terms of Use:

MIT-0

## Use Case:

External users and procurement-focused agents use this skill to search, shortlist, validate, and enrich US B2B engineering firm candidates for buildings, infrastructure, energy, and manufacturing projects while excluding software engineering, non-US firms, individual freelancers, and consumer residential requests.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: ServiceGraph API keys could be exposed if pasted into chat or loaded into model context.

Mitigation: Use a harness-managed ServiceGraph MCP/OAuth flow when available, or keep SERVICEGRAPH_API_KEY in a local environment file or shell environment and do not paste tokens into chat.

Risk: Unlocking firm details spends ServiceGraph credits.

Mitigation: Confirm the selected apex list and estimated credit cost before calling the unlock endpoint.

Risk: Searches can drift into unrelated industries or software-engineering requests if filters are too broad.

Mitigation: Pin industry:engineering_services, validate filters before search, and defer software-engineering or non-US requests to the appropriate workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nostrband/skills/find-engineering-firm)
- [ServiceGraph API](https://api.servicegraph.co)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown guidance with REST examples, filter DSL snippets, shell commands, and API request details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require SERVICEGRAPH_API_KEY; paid firm-detail unlocks cost 10 credits per firm and should be confirmed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
