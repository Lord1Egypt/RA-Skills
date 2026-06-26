## Description: <br>
Api3 Feed Manager helps agents discover, activate, fund, and maintain Api3 data feeds for downstream on-chain projects while defaulting to discovery, readiness checks, and dry-run planning before signer-backed execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daav3](https://clawhub.ai/user/daav3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when a project needs a reliable Api3 price feed on a supported chain, needs feed runway checked, or needs an already-enabled feed maintained. It can return feed identity, readiness, funding status, execution plans, transaction records, and maintenance recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect and potentially fund Api3 feeds, so signer-backed execution can spend funds. <br>
Mitigation: Prefer dry-run, browser, or wallet-based signing paths and require explicit operator approval before submitting any transaction that spends funds. <br>
Risk: The artifact includes private-key command-line guidance, which can expose sensitive credentials. <br>
Mitigation: Avoid passing private keys as command-line arguments; use local runtime wallet setup or browser/wallet signing instead. <br>
Risk: Security evidence marks the release as suspicious because spending capability and unsafe key-handling guidance require review. <br>
Mitigation: Review the skill before installing or delegating execution, and keep signer-backed actions within the guarded execution boundary described by the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daav3/api3-feed-manager) <br>
- [Project homepage](https://github.com/daav3/agentic-lending-project) <br>
- [Api3 dApp quickstart](https://docs.api3.org/dapps/quickstart/) <br>
- [Api3 dApp integration](https://docs.api3.org/dapps/integration/) <br>
- [Api3 contract integration](https://docs.api3.org/dapps/integration/contract-integration.html) <br>
- [Api3 OEV rewards](https://docs.api3.org/dapps/oev-rewards/) <br>
- [Api3 data feeds](https://docs.api3.org/oev-searchers/in-depth/data-feeds/) <br>
- [Api3 Market](https://market.api3.org) <br>
- [Api3 dAPI pricing data](https://api3dao.github.io/data-feeds/market/dapi-pricing) <br>
- [Part 1 Skill Spec](references/part1-skill-spec.md) <br>
- [Part 1 Research](references/part1-research.md) <br>
- [Part 1 Architecture Update](references/part1-architecture-update.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or structured text with command examples and transaction details when execution is requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include feed status fields, funding estimates, actions taken, transaction hashes, warnings, and next maintenance recommendations.] <br>

## Skill Version(s): <br>
0.4.4 (source: server release evidence, changelog, package.json; released 2026-05-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
