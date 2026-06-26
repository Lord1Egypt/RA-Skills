## Description: <br>
Dashpass is an encrypted credential vault on Dash Platform that helps agents store, retrieve, rotate, and export API keys, tokens, and passwords with local encryption before network storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashbot-0001](https://clawhub.ai/user/dashbot-0001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Dashpass to manage agent credentials on Dash Platform, including storing, retrieving, rotating, checking expiry, deleting, and exporting secrets. The skill is most relevant when an agent needs repeatable credential access without plain-text .env files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a Dash identity key that can decrypt and mutate the credential vault. <br>
Mitigation: Use testnet or a dedicated identity, keep CRITICAL_WIF tightly controlled, and install only where that level of key access is acceptable. <br>
Risk: Sensitive credential material may remain available through local cache behavior. <br>
Mitigation: Set DASHPASS_CACHE=none for sensitive use and avoid syncing ~/.dashpass to shared backups or cloud storage. <br>
Risk: Exporting credentials through eval workflows can expose secrets to shell history, process environments, or logs. <br>
Mitigation: Avoid eval for sensitive credentials and prefer pipe-oriented commands that minimize displayed output. <br>
Risk: The current mutual confirmation mode should not be treated as real independent human approval. <br>
Mitigation: Require an explicit external review or separate approval process for high-value decryptions until mutual confirmation is independently enforced. <br>
Risk: Artifact documentation says Dashpass has been tested and verified on Dash testnet only. <br>
Mitigation: Do not store production credentials on testnet and validate mainnet behavior separately before any production use. <br>


## Reference(s): <br>
- [Dashpass ClawHub page](https://clawhub.ai/dashbot-0001/dashpass) <br>
- [Dash Platform Identity tutorial](https://docs.dash.org/en/stable/docs/tutorials/identities-and-names.html) <br>
- [Dash Platform identity top-up tutorial](https://docs.dash.org/en/stable/docs/tutorials/identities-and-names.html#top-up-an-identity) <br>
- [CLI command reference](references/cli-commands.md) <br>
- [Security model](references/security-model.md) <br>
- [Security analysis summary](references/security-analysis-summary.md) <br>
- [Trust architecture](references/trust-architecture.md) <br>
- [FAQ and known limitations](references/faq.md) <br>
- [First-time setup](setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js plus CRITICAL_WIF and DASHPASS_IDENTITY_ID environment variables; operations may read or write encrypted credential records through the Dashpass CLI.] <br>

## Skill Version(s): <br>
0.9.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
