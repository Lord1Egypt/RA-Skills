## Description:

This skill guides agents to use Laiye ADP to recognize Chinese bank account opening permits and extract key permit fields as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and business automation teams use this skill to configure the ADP CLI, select the built-in account-opening-permit extraction app, and extract permit identifiers, representative names, banks, account numbers, and related fields from images, PDFs, URLs, local files, or Base64 input.

### Deployment Geography for Use:

Global, subject to the user's selected Laiye ADP service region and applicable data handling requirements.

## Known Risks and Mitigations:

Risk: Installer commands include pipe-to-shell patterns and remote package installation.

Mitigation: Review before installing, prefer a pinned and verified release or inspected local installer, and avoid administrator or root execution unless explicitly required.

Risk: The workflow sends account-opening permits and extracted PII-bearing fields to Laiye ADP cloud services.

Mitigation: Confirm organizational approval for cloud processing, select the appropriate ADP service region, and redact or protect outputs before logging, storage, or redistribution.

Risk: API keys and local ADP configuration are required for operation.

Mitigation: Store credentials securely, avoid committing local config or exported task files, and rotate keys if exposure is suspected.

Risk: The ADP CLI supports broader parsing, custom-app, and administrative commands beyond the narrow permit-extraction use case.

Mitigation: Use only the commands needed for account-opening-permit extraction unless a reviewer explicitly approves broader CLI operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laiye-adp/skills/adp-bank-account-permit-recognition-and-extract)
- [Laiye ADP China portal](https://adp.laiye.com/?utm_source=clawhub)
- [Laiye ADP global portal](https://adp-global.laiye.com/?utm_source=clawhub)
- [ADP CLI user guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc)
- [ADP Open API user guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)
- [ADP CLI GitHub releases](https://github.com/laiye-ai/adp-cli/releases)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with CLI commands and structured JSON extraction results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce stdout JSON for single documents or exported JSON files and task IDs for batch or asynchronous processing.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
