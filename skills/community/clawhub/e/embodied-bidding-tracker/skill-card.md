## Description: <br>
AIRS-具身智能订单信息采集器 organizes public bidding evidence collection, company identity checks, third-party order verification, LLM-assisted case extraction, ingestion table generation, and case quality review for industrial research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[airs-guest](https://clawhub.ai/user/airs-guest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Industry researchers and analysts use this skill to collect public tender and award evidence, verify embodied-intelligence and robotics-related orders, extract structured case records, and prepare reviewed CSV or Markdown outputs for a research case database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires sensitive local credentials, including an OpenAI-compatible API key and a logged-in Tianyancha browser session. <br>
Mitigation: Store credentials only in local config/settings.json, use an approved LLM provider for the records being processed, and keep data outputs private. <br>
Risk: Chrome remote debugging can expose an authenticated browser session if left open or used outside a trusted local environment. <br>
Mitigation: Use a dedicated low-privilege Chrome profile for Tianyancha, run remote debugging only on a trusted local machine, and close the debugging session after use. <br>
Risk: Reruns may overwrite reviewed CSV outputs where analyst edits matter. <br>
Mitigation: Back up reviewed CSVs before rerunning collection, extraction, verification, or ingestion steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/airs-guest/embodied-bidding-tracker) <br>
- [Project homepage](https://github.com/airs-guest/airs-embodied-intelligence-research-skills) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [settings.example.json](artifact/config/settings.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands and generated CSV or Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local data outputs such as company lists, bidding records, raw content Markdown, verification reports, review sheets, ingestion CSVs, and ingest reports.] <br>

## Skill Version(s): <br>
1.0.9 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
