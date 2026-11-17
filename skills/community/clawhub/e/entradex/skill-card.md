## Description:

EntradeX helps agents use the EntradeX CLI for DNSE workflows, including credential setup, account and market lookup, order review, and placing, modifying, or canceling trades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hieuhani](https://clawhub.ai/user/hieuhani)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure DNSE credentials, inspect account, market, and order data, and prepare EntradeX CLI commands for DNSE trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place, modify, or cancel real DNSE trades when valid credentials and a trading token are available.

Mitigation: Require explicit user confirmation before any trade-changing command and prefer a limited DNSE account or narrowly scoped credentials.

Risk: DNSE_API_KEY and DNSE_API_SECRET are sensitive trading credentials.

Mitigation: Avoid exposing credentials in prompts, logs, or command-line history, and rotate keys if unauthorized access is suspected.

Risk: The documented install path uses an unpinned global npm package.

Mitigation: Install an audited, pinned entradex-cli version in an isolated environment before using the skill.

## Reference(s):

- [EntradeX CLI npm package](https://www.npmjs.com/package/entradex-cli)
- [DNSE OpenAPI endpoint](https://openapi.dnse.com.vn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that require DNSE credentials and a trading token.]

## Skill Version(s):

0.1.16 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
