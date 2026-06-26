## Description: <br>
ClevrPay helps agents guide trusted stablecoin payment workflows between verified counterparties, including A-Pass checks, deposit address lookup, institution whitelist checks, wallet registration, and A-Token deposit, withdrawal, or transfer guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[umy997](https://clawhub.ai/user/umy997) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent-commerce builders use this skill to route ClevrPay and Cleanverse payment tasks such as A-Pass registration or status checks, supported-chain lookup, deposit address retrieval, institution whitelist checks, wallet registration, and A-Token withdrawal or transfer workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto payment, wallet-registration, withdrawal, or transfer workflows can cause unrecoverable on-chain mistakes if the chain, token, amount, recipient, or wallet mapping is wrong. <br>
Mitigation: Require explicit user confirmation and independently verify the chain, token, amount, destination address, A-Pass state, and wallet registration before any registration, withdrawal, or transfer. <br>
Risk: The security summary says routing and confirmation safeguards are under-specified for a high-impact financial use case. <br>
Mitigation: Review the skill carefully before installation and use it only for explicit ClevrPay or Cleanverse workflows. <br>
Risk: Static chain and token documentation may drift from live service configuration. <br>
Mitigation: Use query_chain_config as the source of truth before claiming support for a chain or token. <br>


## Reference(s): <br>
- [Clevr Pay Skills API Documentation](references/api-doc.md) <br>
- [Quick API map](references/quick-api-map.md) <br>
- [Retrieval and boundaries](references/retrieval-and-boundaries.md) <br>
- [Use cases](references/use-cases.md) <br>
- [Glossary and retrieval language](references/glossary.md) <br>
- [Access Core Contract ABI](references/access_core.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with API workflow guidance and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API command names, wallet addresses, chain names, token symbols, and verification steps for payment workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
