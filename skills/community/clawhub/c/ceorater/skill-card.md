## Description: <br>
CEORater lets agents query institutional-grade CEO performance analytics for S&P 500 and major U.S. public companies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ceorater-skills](https://clawhub.ai/user/ceorater-skills) <br>

### License/Terms of Use: <br>
Proprietary API terms of service <br>


## Use Case: <br>
External analysts, investors, and research agents use this skill to look up CEO scores, market outperformance metrics, compensation efficiency, and related executive performance data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a CEORATER_API_KEY for authenticated API requests. <br>
Mitigation: Store the key as a dedicated secret, avoid logging it, and do not place it in shared configuration or prompts. <br>
Risk: Broad finance or executive research queries may route data to the paid CEORater API. <br>
Mitigation: Use the skill only when CEORater is intended for the task and keep lookup or search queries scoped to the needed company, ticker, sector, or CEO. <br>
Risk: CEORater data is proprietary and some integrations require an enterprise agreement. <br>
Mitigation: Confirm the applicable CEORater terms before integrating the data into proprietary models, AI training, or products. <br>


## Reference(s): <br>
- [CEORater ClawHub listing](https://clawhub.ai/ceorater-skills/ceorater) <br>
- [CEORater website](https://www.ceorater.com) <br>
- [CEORater API documentation](https://www.ceorater.com/api-docs.html) <br>
- [CEORater agent manifest](https://www.ceorater.com/.well-known/agent.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CEORATER_API_KEY and sends read-only lookup or search requests to CEORater.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
