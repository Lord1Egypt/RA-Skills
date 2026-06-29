## Description: <br>
Bigdeal Supplier Finder helps an agent produce evidence-bound supplier discovery reports for sourcing briefs using public search and fetch, with explicit limits around credentials, scraping, trust scoring, and purchasing recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[its-how](https://clawhub.ai/user/its-how) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, sourcing teams, and agents use this skill to explore supplier discovery surfaces and assemble structured sourcing reports for products or briefs. It supports source mapping, candidate extraction, evidence grading, gaps, and next-search suggestions without making procurement recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live supplier research can cross into credentialed platforms, paid databases, contact enrichment, bulk scraping, or purchasing recommendations. <br>
Mitigation: Allow only public search and fetch when explicitly authorized, record restricted access as gaps, and keep outputs to evidence-bound discovery support rather than procurement decisions. <br>
Risk: Low-evidence supplier leads can be mistaken for verified or trustworthy suppliers. <br>
Mitigation: Require admissible evidence links for supplier candidates, preserve evidence grades, exclude D-grade signals from candidates, and avoid trust, safety, compliance, or purchase-ready labels. <br>


## Reference(s): <br>
- [Report Contract](references/report-contract.md) <br>
- [Supplier Discovery Source Registries](source-registries/supplier-discovery-registries.md) <br>
- [Source Repository](https://github.com/its-How/bigdeal-supplier-finder) <br>
- [ClawHub Skill Page](https://clawhub.ai/its-how/skills/bigdeal-supplier-finder) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, guidance] <br>
**Output Format:** [Markdown structured report with evidence links and named report sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source maps, supplier candidates, search result signals, source attempts, queries tried, gaps, next steps, and a risk notice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
