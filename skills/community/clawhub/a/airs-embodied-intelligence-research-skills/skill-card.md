## Description: <br>
AIRS招投标订单采集与核查 organizes company identity resolution, Tianyancha bidding evidence collection, third-party order verification, LLM case extraction, ingestion table generation, and case quality review for embodied intelligence and robotics industry research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[airs-guest](https://clawhub.ai/user/airs-guest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Industry researchers and analysts use this skill to collect public procurement evidence, verify robotics orders, extract structured embodied intelligence case records, and prepare reviewed case-library outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a logged-in Tianyancha browser session. <br>
Mitigation: Use a dedicated browser profile or low-privilege account, keep Chrome remote debugging bound to localhost, and close the session after collection. <br>
Risk: Collected procurement and research text may be sent to the configured LLM provider. <br>
Mitigation: Verify the provider, endpoint, retention terms, and data handling policy before processing sensitive or proprietary material. <br>
Risk: External Excel inputs may be unsafe until the xlsx dependency concern is addressed. <br>
Mitigation: Avoid untrusted Excel files and pre-screen inputs before running third-party order verification. <br>
Risk: Generated outputs under data/ may be overwritten or refreshed during the workflow. <br>
Mitigation: Run the skill in a backed-up workspace and preserve copies of important outputs before reruns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/airs-guest/airs-embodied-intelligence-research-skills) <br>
- [Project homepage](https://github.com/airs-guest/airs-embodied-intelligence-research-skills) <br>
- [Tianyancha](https://www.tianyancha.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated CSV or Markdown data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local data outputs such as company lists, bidding records, raw content Markdown, verification reports, extraction sheets, ingestion CSV files, and ingest reports under data/.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
