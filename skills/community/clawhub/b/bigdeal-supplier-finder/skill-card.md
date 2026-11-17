## Description:

Creates evidence-bound supplier discovery reports for sourcing briefs, producing source maps, supplier candidates, evidence links, gaps, and next-search suggestions without logging in, using paid APIs, scraping at scale, or making recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[its-how](https://clawhub.ai/user/its-how)

### License/Terms of Use:

MIT-0

## Use Case:

External buyers, sourcing operators, and agents use this skill to plan supplier discovery and assemble evidence-bound sourcing reports for products, regions, and sourcing intents. It supports search/fetch and planning-only modes while keeping supplier evidence, gaps, and next steps separate from purchase recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live supplier research can cross browser, provider, credential, paid API, form submission, or bulk crawling boundaries if those actions are separately authorized.

Mitigation: Keep runs to public search and fetch unless the expanded boundary has been separately reviewed and approved.

Risk: Unpinned upgrade commands can pull future changes that have not been reviewed.

Mitigation: Inspect or pin the repository or installer revision before updating the skill.

Risk: Supplier discovery outputs may be mistaken for recommendations, trust scores, due diligence, or purchase-ready conclusions.

Mitigation: Use reports as discovery support only and require separate supplier review before procurement decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/its-how/skills/bigdeal-supplier-finder)
- [Repository](https://github.com/its-How/bigdeal-supplier-finder)
- [Report Contract](references/report-contract.md)
- [Supplier Discovery Source Registries](source-registries/supplier-discovery-registries.md)
- [Source Family Checklist](sources.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown report with evidence links and required report sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source maps, supplier candidates, search signals, source attempts, gaps, next steps, and a risk notice; excludes procurement recommendations and supplier trust scores.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
