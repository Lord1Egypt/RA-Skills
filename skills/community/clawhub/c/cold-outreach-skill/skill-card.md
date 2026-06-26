## Description: <br>
Meta-skill for orchestrating Apollo API, LinkedIn API, YC Cold Outreach, and MachFive Cold Email into a complete B2B cold outreach pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h4gen](https://clawhub.ai/user/h4gen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, growth, and business development users use this skill to source B2B leads, enrich available context, draft personalized outreach sequences, and prepare scheduling handoff recommendations for an external sending system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup guidance can update all installed ClawHub skills, expanding the change surface beyond this release. <br>
Mitigation: Install only the named dependencies and pin reviewed versions where possible. <br>
Risk: The workflow uses outreach service API keys and contact data. <br>
Mitigation: Use scoped or test API keys and confirm lead sourcing and outreach comply with privacy, platform, and anti-spam requirements. <br>
Risk: Generated outreach may include unsupported personalization or claims if source context is weak. <br>
Mitigation: Keep unavailable personalization fields explicit, review factuality before approval, and do not claim a lead posted or said something unless it is verifiable. <br>


## Reference(s): <br>
- [Cold Outreach Skill on ClawHub](https://clawhub.ai/h4gen/cold-outreach-skill) <br>
- [Publisher profile: h4gen](https://clawhub.ai/user/h4gen) <br>
- [Inspected Upstream Skills](references/inspected-skills.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown sections with structured lead summaries, enrichment summaries, sequence packages, and execution plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are recommendations and generated outreach assets for external sending or scheduling systems; the skill does not directly send messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
