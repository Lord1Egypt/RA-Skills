## Description: <br>
Run deep research queries using Chonkie DeepResearch and return comprehensive research reports with citations for market analysis, competitive intelligence, technical deep dives, and other research-heavy tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chonknick](https://clawhub.ai/user/chonknick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and other agent users use this skill to run long-running Chonkie DeepResearch queries and retrieve cited research reports without blocking the main agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create lingering cron-based status checks for Chonkie research jobs. <br>
Mitigation: Prefer the sub-agent wait flow for one-off research and require explicit user confirmation before creating cron jobs. <br>
Risk: Chonkie research queries and generated reports may contain sensitive information. <br>
Mitigation: Install only when the Chonkie CLI and service are trusted, keep CHONKIE_API_KEY private, and avoid sensitive queries unless Chonkie is an acceptable destination. <br>
Risk: Research reports can be very large and may consume excessive context if loaded in full. <br>
Mitigation: Read summaries or targeted sections first, using search and offsets before loading report content. <br>


## Reference(s): <br>
- [Chonkie](https://chonkie.ai) <br>
- [Chonkie API Keys](https://labs.chonkie.ai/settings/api-keys) <br>
- [ClawHub Skill Page](https://clawhub.ai/chonknick/chonkie-deepresearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Research reports may be large; the skill instructs agents to inspect summaries and targeted sections rather than loading entire reports.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
