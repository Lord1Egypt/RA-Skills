## Description: <br>
基于来也科技ADP平台的中国机动车行驶证智能识别与信息抽取Skill，支持行驶证正副页20+关键字段抽取，并输出结构化JSON。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and business automation teams use this skill to invoke Laiye ADP cloud extraction for Chinese vehicle license images, files, folders, URLs, or Base64 inputs. It helps convert vehicle registration, insurance, ride-hailing, and freight onboarding documents into structured JSON fields for downstream systems. <br>

### Deployment Geography for Use: <br>
Global, with China mainland and overseas ADP endpoints documented. <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle-license images and extracted fields are sent to Laiye ADP cloud services. <br>
Mitigation: Use the skill only for data that may be processed by Laiye ADP, and treat returned or exported JSON as sensitive personal data. <br>
Risk: The ADP CLI has broader document-processing and custom-app management capabilities than this vehicle-license workflow requires. <br>
Mitigation: Limit agent actions to OOTB vehicle-license extraction commands and avoid custom-app administration commands unless explicitly intended. <br>
Risk: The skill documents curl|bash and irm|iex installation paths. <br>
Mitigation: Prefer npm installation or verified release binaries before using shell-script installation methods. <br>
Risk: API keys are required for the cloud service. <br>
Mitigation: Restrict the API key, store it securely, and avoid exposing it in prompts, logs, or shared command output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laiye-adp/adp-vehicle-license-recognition-and-extract) <br>
- [Laiye ADP China mainland portal](https://adp.laiye.com/?utm_source=clawhub) <br>
- [Laiye ADP overseas portal](https://adp-global.laiye.com/?utm_source=clawhub) <br>
- [ADP CLI user guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc) <br>
- [Open API user guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc) <br>
- [Public cloud operation manual](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh) <br>
- [ADP CLI GitHub releases](https://github.com/laiye-ai/adp-cli/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash command examples and structured JSON extraction output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May export one JSON result per input file for batch processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
