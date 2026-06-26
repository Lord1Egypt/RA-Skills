## Description: <br>
Uses Laiye ADP to recognize Chinese motor vehicle driving licenses and extract front- and back-page fields into structured JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
Commercial License Agreement <br>


## Use Case: <br>
External developers and operations teams use this skill to automate Chinese driving-license data capture for driver qualification checks, ride-hailing or freight onboarding, and business-system intake workflows. It guides agents through ADP CLI setup, credential configuration, app-id selection, extraction commands, and JSON result handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Driving-license images and extracted fields contain sensitive identity data. <br>
Mitigation: Use trusted ADP accounts only, protect API keys and exported result files, and redact PII before logging, displaying, or sharing outputs. <br>
Risk: The bundled ADP documentation covers broader CLI and custom-app administration capabilities beyond the driving-license workflow. <br>
Mitigation: Restrict agent use to the driving-license OOTB app_id and avoid generic parse or custom-app commands unless that broader administration is intentional. <br>
Risk: Pipe-to-shell installers can execute remote scripts during setup. <br>
Mitigation: Prefer npm installation or a verified release artifact over curl or PowerShell pipe-to-shell installation paths. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/laiye-adp/adp-driving-license-recognition-and-extract) <br>
- [ADP China Mainland Portal](https://adp.laiye.com/?utm_source=clawhub) <br>
- [ADP Global Portal](https://adp-global.laiye.com/?utm_source=clawhub) <br>
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc) <br>
- [ADP Open API User Guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc) <br>
- [ADP CLI Releases](https://github.com/laiye-ai/adp-cli/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured JSON extraction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an ADP API key and produces sensitive driving-license identity fields that should be protected and redacted when logged or shared.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
