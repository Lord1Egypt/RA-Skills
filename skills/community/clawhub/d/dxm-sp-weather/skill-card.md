## Description: <br>
Helps an agent answer user weather questions and query weather-service orders, quota, purchase details, and API call logs through the Duxiaoman weather service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duxiaoman](https://clawhub.ai/user/duxiaoman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to query city/date weather information and inspect paid weather-service account state, including orders, quota, purchase details, and API call history. The agent may guide the user through purchase or recharge flows when the service reports insufficient quota. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill integrates with a paid weather service and may send weather queries, account identifiers, payment links, and QR contents to dxmpay.com. <br>
Mitigation: Install only if the user trusts dxmpay.com, and review payment destinations before scanning or opening payment links. <br>
Risk: The skill stores an encrypted local EC private key configuration and requires a private-key password during use. <br>
Mitigation: Use a strong password, avoid exposing it in logs or shared shells, and remove the local configuration when it is no longer needed. <br>
Risk: The bundled QR helper can write PNG files and the security evidence notes that QR contents may be sent to dxmpay.com. <br>
Mitigation: Review QR contents and destinations before use, and clean up generated QR PNG files after the workflow completes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duxiaoman/dxm-sp-weather) <br>
- [Duxiaoman publisher profile](https://clawhub.ai/user/duxiaoman) <br>
- [Duxiaoman weather service endpoint](https://www.dxmpay.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local configuration and QR PNG files while using the bundled helper scripts.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
