## Description: <br>
Guides an agent through using Laiye ADP to extract bank-card numbers, issuing institutions, validity periods, and card types from bank-card images or documents into structured JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
Commercial License Agreement <br>


## Use Case: <br>
External developers and operations teams use this skill to configure ADP credentials, select the built-in bank-card extraction app, and process user-provided bank-card images for onboarding, payment binding, and financial data entry workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles bank-card images and extracted card fields through Laiye ADP cloud services. <br>
Mitigation: Use only with user-approved card images, follow applicable payment and privacy requirements, and avoid sending unrelated documents or unnecessary personal data. <br>
Risk: The bundled documentation includes broader ADP document-processing and administration commands beyond the narrow bank-card extraction purpose. <br>
Mitigation: Restrict agent use to the built-in bank-card extraction app and explicit extraction, query, configuration, and balance-check commands needed for this workflow. <br>
Risk: ADP API keys and service configuration are sensitive credentials. <br>
Mitigation: Store credentials in approved secret storage or environment configuration, do not echo keys in transcripts, and rotate keys if exposure is suspected. <br>
Risk: Shell and PowerShell pipe-to-shell installers are documented as fallback install paths. <br>
Mitigation: Prefer npm or verified release downloads, and review installer sources before executing them in managed environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laiye-adp/adp-credit-card-recognition-and-extract) <br>
- [ADP China mainland portal](https://adp.laiye.com/?utm_source=clawhub) <br>
- [ADP global portal](https://adp-global.laiye.com/?utm_source=clawhub) <br>
- [ADP CLI releases](https://github.com/laiye-ai/adp-cli/releases) <br>
- [ADP CLI issues](https://github.com/laiye-ai/adp-cli/issues) <br>
- [ADP CLI usage guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc) <br>
- [ADP Open API guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and expected JSON extraction results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an ADP API key, an ADP API base URL, a built-in bank-card app ID, and explicit user-provided image input by URL, local path, or Base64.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
