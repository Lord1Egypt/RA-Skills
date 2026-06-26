## Description: <br>
Geo Cycle Autopilot verifies a GEO API key, processes scheduled GEO optimization tasks, exports sample and deep-imitation ZIP files, and reports mass-publishing readiness for QClaw runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chameleon-nexus](https://clawhub.ai/user/chameleon-nexus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QClaw users and operators use this skill to run scheduled GEO optimization follow-up: verify credentials, fetch enabled tasks, export fanwen and fangxie ZIP files, generate deep-imitation content when configured, and update task status without exposing internal task IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and stores a GEO API key in a local plaintext file. <br>
Mitigation: Use a restricted or revocable GEO API key, protect the key file, and replace it with a safer credential mechanism if one is available. <br>
Risk: Scheduled runs can contact the GEO SaaS service and source URLs without per-run approval. <br>
Mitigation: Enable the skill only for expected scheduled QClaw workflows and review network access expectations before installation. <br>
Risk: The skill writes exported ZIP files under the user's home directory and reports mass-publishing readiness automatically. <br>
Mitigation: Review export locations, keep the home directory protected, and confirm task status changes match the intended workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chameleon-nexus/geo-cycle-autopilot) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/chameleon-nexus) <br>
- [GEO service endpoint](https://ai.gaobobo.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status summaries with inline shell commands and local file path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes export ZIP files under the user's home directory and updates GEO task status through authenticated API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
