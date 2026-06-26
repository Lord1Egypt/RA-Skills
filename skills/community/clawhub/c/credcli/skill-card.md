## Description: <br>
Guides agents through using CredCLI to generate, upload, stamp, and email mail-merged Chainletter credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntbooks](https://clawhub.ai/user/ntbooks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create credential issuance workflows with CredCLI, including workspace setup, recipient CSV preparation, rendering, Chainletter upload, stamping, and claim email generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential contents and recipient data may become publicly accessible when using public issuance and IPFS-backed verification. <br>
Mitigation: Use public issuance only when recipients consent and the credential contents are appropriate for public verification; use private mode for internal-only records. <br>
Risk: The workflow depends on an external CredCLI package and a Chainletter token that controls workspace and issuance actions. <br>
Mitigation: Verify trust in the @credcli/cli package before installation, use a least-privilege Chainletter token, and confirm token scope with credcli register -i before issuing credentials. <br>
Risk: Tokens or SMTP credentials can be exposed through visible command history or shared sessions. <br>
Mitigation: Avoid entering real secrets in shared terminals or transcripts, prefer least-privilege credentials, and restrict network access to required Chainletter and stamping domains. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ntbooks/credcli) <br>
- [Publisher Profile](https://clawhub.ai/user/ntbooks) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides CredCLI workflows that can produce credential PDFs, PNGs, email files, and Chainletter issuance actions.] <br>

## Skill Version(s): <br>
0.2.4 (source: server evidence release version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
