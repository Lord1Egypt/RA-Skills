## Description: <br>
Answer Engine Optimization (AEO) helps an agent audit brand visibility in AI answers, build Answer Intent Maps, track recommendation positions, and maintain AEO assets for a brand or product category. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Batsirai](https://clawhub.ai/user/Batsirai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External marketing, growth, and ecommerce teams use this skill to analyze whether AI assistants recommend a brand for purchase-intent queries, identify competitive gaps, and generate AEO infrastructure such as audit reports, answer hubs, brand-facts data, schema guidance, and weekly maintenance reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated publishing templates may contain hidden AI-targeting notes or recommendation-oriented content that can make neutral-looking pages favor a preferred brand. <br>
Mitigation: Remove hidden comments and internal implementation notes before publishing, disclose commercial interests where appropriate, and review recommendation language for neutrality and factual support. <br>
Risk: AEO audits, rankings, and comparison content can include inaccurate claims, stale product data, or misleading competitor comparisons. <br>
Mitigation: Verify prices, reviews, certifications, citations, and competitor claims against current authoritative sources before relying on or publishing generated outputs. <br>
Risk: The workflows can send brand strategy, customer, or product data to third-party AI and search API providers and write reports locally. <br>
Mitigation: Avoid entering confidential data unless those providers and local storage locations are approved for that data, and load API keys through environment variables rather than embedding credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Batsirai/aeo-system) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON data files, JSON-LD snippets, filled configuration templates, and shell commands for the included Node.js script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query third-party AI and search APIs when API keys are supplied; can also run in a manual-assist mode when results are pasted in.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
