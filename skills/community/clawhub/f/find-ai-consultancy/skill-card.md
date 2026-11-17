## Description:

Finds, shortlists, vets, and enriches US AI/ML and data consulting firms using the ServiceGraph pro_services catalog and its data_ai_consulting taxonomy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nostrband](https://clawhub.ai/user/nostrband)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn AI/ML consultancy procurement requests into ServiceGraph searches, shortlists, comparisons, and optional paid contact enrichment for US firms.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The auth flow recommends sourcing .env.local as shell code, which can execute unexpected shell content.

Mitigation: Use the ServiceGraph MCP/OAuth path or export SERVICEGRAPH_API_KEY from a trusted secret manager; avoid sourcing untrusted dotenv files.

Risk: Paid unlock operations spend 10 credits per firm.

Mitigation: Confirm selected apex domains, total credit cost, and unlock intent before calling POST /v1/datasets/pro_services/unlocks.

Risk: The catalog can include misclassified AI-related firms such as SaaS products or education providers.

Mitigation: Review brief and unlocked details before recommending a firm, and skip firms that are out of scope for US AI/ML/data consulting services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nostrband/skills/find-ai-consultancy)
- [ClawHub publisher profile](https://clawhub.ai/user/nostrband)
- [ServiceGraph API base](https://api.servicegraph.co)
- [ServiceGraph pro_services fields endpoint](https://api.servicegraph.co/v1/datasets/pro_services/fields)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration instructions]

**Output Format:** [Markdown with inline HTTP and curl examples, ServiceGraph filter strings, shortlist summaries, and unlock guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include firm apex domains, brief firm cards, credit-cost notes, and contact-enrichment steps.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
