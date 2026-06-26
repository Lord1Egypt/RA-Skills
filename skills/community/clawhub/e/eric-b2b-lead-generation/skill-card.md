## Description: <br>
B2B Lead Generation Assistant. Activated when users say 'I want to sell XXX', 'Help me find customers', 'Analyze competitors', or 'Discover opportunities'. Automatically identifies competitors, discovers potential customers through connection mining, scores and enriches leads, and generates personalized BD materials. Supports 6-phase standardized workflow: Config Generation → Information Collection → Lead Scoring → Data Enrichment → BD Material Generation → Output Delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericn26-star](https://clawhub.ai/user/ericn26-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, business development, and growth teams use this skill to turn a product description into competitor analysis, lead discovery, lead scoring, contact enrichment, and personalized outreach materials. The workflow focuses on publicly visible B2B prospecting signals and produces prioritized lead records and BD drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs privacy-sensitive B2B prospecting, including social-graph mining and contact collection for identifiable people. <br>
Mitigation: Install and use only with a lawful basis for data collection, limit collection to approved public business data, and treat generated reports as sensitive personal-data files. <br>
Risk: The workflow can encourage scraping private or credential-gated social data and inferred contact details. <br>
Mitigation: Do not scrape private or credential-gated data; avoid inferred emails, phone collection, and personality or non-work-interest profiling unless explicitly approved and compliant with applicable rules. <br>
Risk: Lead records and personalized outreach may contain incorrect or misleading inferences about people or companies. <br>
Mitigation: Review source URLs, scoring rationale, and generated outreach before use; mark unsupported enrichment fields as incomplete rather than treating them as verified facts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericn26-star/eric-b2b-lead-generation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with YAML-style configuration and lead records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes competitor lists, lead scoring tables, enriched contact fields, LinkedIn connection messages, email drafts, follow-up plans, and source URLs where available.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
