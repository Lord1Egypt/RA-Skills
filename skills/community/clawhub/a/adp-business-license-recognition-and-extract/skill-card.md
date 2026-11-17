## Description:

Guides agents to use Laiye ADP to recognize Chinese business license documents and extract key fields into structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

Commercial License Agreement

## Use Case:

Business operations, compliance, and developer teams use this skill to extract structured company-registration fields from Chinese business licenses for qualification checks, onboarding, and business-system integration.

### Deployment Geography for Use:

Global; the ADP service documentation describes separate China mainland and overseas endpoints.

## Known Risks and Mitigations:

Risk: The release security summary flags remote-script installer commands such as curl-to-shell and PowerShell download-and-execute flows.

Mitigation: Prefer the npm package or a signed release path, and review installer provenance before execution.

Risk: Business licenses and extracted fields can contain organization identifiers, names, addresses, and other sensitive business or personal data.

Mitigation: Confirm the organization permits uploading these documents to Laiye ADP, redact or limit logging where possible, and protect exported JSON files.

Risk: The underlying ADP CLI includes broader custom-application and administration commands beyond the out-of-the-box business-license extraction workflow.

Mitigation: Constrain agent usage to the documented OOTB business-license extraction commands unless an operator explicitly approves broader CLI actions.

Risk: Extraction results may be incomplete or vary by endpoint, document quality, or returned field naming.

Mitigation: Validate required fields downstream, preserve original returned JSON, and handle empty field arrays or missing confidence values.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laiye-adp/skills/adp-business-license-recognition-and-extract)
- [Laiye ADP China Mainland Portal](https://adp.laiye.com/?utm_source=clawhub)
- [Laiye ADP Global Portal](https://adp-global.laiye.com/?utm_source=clawhub)
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc)
- [Open API User Guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)
- [ADP Public Cloud Manual](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh)
- [ADP CLI GitHub Releases](https://github.com/laiye-ai/adp-cli/releases)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON result expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The ADP extraction command returns business-license fields as JSON and can export batch results to files.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
