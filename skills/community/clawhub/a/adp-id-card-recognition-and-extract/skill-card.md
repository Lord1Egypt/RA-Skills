## Description: <br>
基于来也科技 ADP 平台的中国居民身份证识别与信息抽取 skill，可 guide an agent to configure ADP credentials, select the built-in ID-card app, and run CLI extraction commands for images, PDFs, URLs, local files, or Base64 inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
Commercial License Agreement <br>


## Use Case: <br>
Developers and operations teams use this skill to automate Chinese resident ID-card field extraction for identity verification, onboarding review, information entry, and batch document workflows through Laiye ADP cloud services. <br>

### Deployment Geography for Use: <br>
Global, with separate China mainland and overseas ADP service endpoints documented by the publisher. <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive identity documents and extracted personal fields. <br>
Mitigation: Use it only when authorized to process the documents, confirm privacy and retention terms, and avoid sending unnecessary ID-card data. <br>
Risk: Inputs and extracted fields are sent to Laiye ADP cloud services under the user's API key. <br>
Mitigation: Configure credentials deliberately, protect the API key, and choose the documented China mainland or overseas service endpoint appropriate for the user. <br>
Risk: The artifact includes broad CLI and app-management instructions beyond the narrow ID-card extraction workflow. <br>
Mitigation: Restrict agent use to the built-in ID-card extraction app and avoid custom-app management commands unless separately approved. <br>
Risk: Some install examples use remote shell or PowerShell scripts. <br>
Mitigation: Prefer npm installation or verified release artifacts before considering pipe-to-shell installation paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laiye-adp/adp-id-card-recognition-and-extract) <br>
- [ADP China mainland portal](https://adp.laiye.com/) <br>
- [ADP overseas portal](https://adp-global.laiye.com/) <br>
- [ADP CLI releases](https://github.com/laiye-ai/adp-cli/releases) <br>
- [ADP CLI user guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc) <br>
- [Open API user guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc) <br>
- [Public cloud operation manual](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, JSON, Markdown guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of ADP CLI commands and interpretation of structured extraction results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
