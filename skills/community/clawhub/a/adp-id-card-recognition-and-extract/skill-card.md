## Description:

Extracts eight key fields from Chinese resident identity cards using Laiye ADP and returns structured JSON for identity verification, data entry, and onboarding review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

Commercial License Agreement

## Use Case:

External users and developers use this skill to invoke Laiye ADP's CLI-backed ID-card extraction workflow for single, batch, or asynchronous processing of Chinese resident identity-card images, scanned files, URLs, or Base64 inputs. The skill is suited to workflows that need structured fields such as name, gender, ethnicity, birth date, address, ID number, issuing authority, and validity period.

### Deployment Geography for Use:

Global, with separate Laiye ADP public cloud endpoints documented for China mainland and overseas regions.

## Known Risks and Mitigations:

Risk: The workflow can upload sensitive identity-document images, URLs, Base64 content, extracted fields, and API-key-authenticated requests to Laiye ADP cloud endpoints.

Mitigation: Use the skill only with ID documents the user is authorized to process, choose the documented regional endpoint deliberately, and avoid retaining extracted personal data longer than needed.

Risk: Setup instructions include remote shell and PowerShell installer methods that require careful review before execution.

Mitigation: Prefer a pinned, verified npm package or release download, and review installer scripts before running curl-to-bash or PowerShell iex commands.

Risk: The underlying CLI exposes broader custom-app administration commands beyond the ID-card extraction workflow.

Mitigation: Limit agent permissions and operator instructions to the ID-card extraction, app lookup, cache, credit, and task-query commands unless broader administration is explicitly required.

Risk: API keys and configured service URLs may be exposed through careless logging, command history, or shared agent context.

Mitigation: Store credentials in the documented ADP configuration or environment variables, keep logs free of secrets, and rotate keys if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laiye-adp/skills/adp-id-card-recognition-and-extract)
- [Laiye ADP China portal](https://adp.laiye.com/?utm_source=clawhub)
- [Laiye ADP global portal](https://adp-global.laiye.com/?utm_source=clawhub)
- [ADP CLI releases](https://github.com/laiye-ai/adp-cli/releases)
- [ADP CLI usage guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc)
- [ADP OpenAPI guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON extraction results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Handles URL, local file, directory, Base64, batch, and asynchronous extraction workflows through Laiye ADP CLI commands.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
