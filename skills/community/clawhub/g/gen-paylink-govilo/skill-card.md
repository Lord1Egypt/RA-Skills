## Description: <br>
Upload files to Govilo and generate paid unlock links through the Govilo Bot API for ZIPs, folders, or individual files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hau823823](https://clawhub.ai/user/hau823823) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and sellers use this skill to package selected files, upload them to Govilo, and create paid unlock links tied to their Govilo API key and Base wallet address. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected files are uploaded to Govilo/R2 to create paid unlock links. <br>
Mitigation: Install and run only if you trust Govilo and are comfortable uploading the selected files to that service. <br>
Risk: Govilo API keys and seller wallet addresses are required for operation. <br>
Mitigation: Use a dedicated .env.govilo file, avoid shared project .env files, and verify the seller wallet address before running. <br>
Risk: Incorrect price, title, or wallet values can create an unwanted paid link. <br>
Mitigation: Ask for and confirm the product title, USDC price, description, and payout address before executing the CLI. <br>
Risk: Setup instructions include installer commands for uv. <br>
Mitigation: Prefer a trusted package manager or verified installer source for uv before executing installation commands. <br>


## Reference(s): <br>
- [Gen Paylink Govilo on ClawHub](https://clawhub.ai/hau823823/gen-paylink-govilo) <br>
- [Publisher Profile](https://clawhub.ai/user/hau823823) <br>
- [Project Homepage](https://github.com/hau823823/gen-paylink-govilo) <br>
- [Setup Guide](references/setup-guide.md) <br>
- [Bot API Quick Reference](references/bot-api-quick-ref.md) <br>
- [Govilo](https://govilo.xyz/) <br>
- [uv Documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOVILO_API_KEY and SELLER_ADDRESS or an explicit seller address; uploads are limited to ZIP content up to 20 MB and 20 files.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
