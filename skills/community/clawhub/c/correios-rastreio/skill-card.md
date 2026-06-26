## Description: <br>
Rastreia pacotes e encomendas dos Correios usando a API oficial, com consultas por codigo, historico local e favoritos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runawaydevil](https://clawhub.ai/user/runawaydevil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to check Correios package status from tracking codes, review recent tracking history, and manage named favorites for repeated lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Correios API key and uses it to call the Correios tracking API. <br>
Mitigation: Use a dedicated API key where possible and rotate it if it is exposed or no longer needed. <br>
Risk: Tracking codes and favorite names may be stored locally as history or saved favorites. <br>
Mitigation: Avoid sensitive favorite aliases and clear src/data.json when saved tracking history should be removed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runawaydevil/correios-rastreio) <br>
- [Correios developer portal](https://developers.correios.com.br) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text CLI output and Markdown documentation with bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Correios API key supplied through CORREIOS_API_KEY and may store local tracking history.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
