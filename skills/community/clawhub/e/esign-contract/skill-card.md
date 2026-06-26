## Description: <br>
esign-contract helps an agent draft or upload contracts, format them as PDFs, start e签宝 signing flows, return signing links, manage signing status, download signed documents, and verify electronic signatures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[esign-cn-open-source](https://clawhub.ai/user/esign-cn-open-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business teams use this skill to draft Chinese-language contracts or upload existing PDF, DOC, and DOCX files, route them through e签宝 signing, manage status, revocation, and downloads, and verify signatures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive contract contents, signer identities, phone numbers, and e-signature workflow control. <br>
Mitigation: Install and use it only when the publisher and e签宝 account are trusted, and avoid processing sensitive contracts on shared or unmanaged machines. <br>
Risk: The skill asks for powerful e签宝 credentials and may write them to ~/.config/esign-contract/.env. <br>
Mitigation: Prefer manual credential setup or a secrets manager, use least-privilege or sandbox credentials where possible, and do not paste production secrets into chat. <br>
Risk: The skill may persist token cache, flow history, temporary contract drafts, and downloaded signed files locally. <br>
Mitigation: Review and clean ~/.config/esign-contract, system temporary directories, and downloaded signed documents after use, especially on shared or sensitive machines. <br>
Risk: Signing initiation and revocation can affect real legal or business workflows. <br>
Mitigation: Require user confirmation before creating or revoking signing flows and verify signer details, contract content, and target environment before execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/esign-cn-open-source/esign-contract) <br>
- [Publisher profile](https://clawhub.ai/user/esign-cn-open-source) <br>
- [Contract generation guide](references/contract-generation.md) <br>
- [Signing guide](references/signing-guide.md) <br>
- [Error handling guide](references/error-handling.md) <br>
- [e签宝 official site](https://www.esign.cn) <br>
- [e签宝 open platform](https://open.esign.cn) <br>
- [e签宝 API documentation](https://open.esign.cn/doc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, PDF files, API calls, shell commands, configuration] <br>
**Output Format:** [Markdown and concise user-facing status text, with generated contract files, PDFs, signing links, downloaded signed documents, and signature verification results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses e签宝 credentials and may persist configuration, token cache, flow history, temporary contract drafts, and downloaded signed documents locally.] <br>

## Skill Version(s): <br>
1.0.5 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
