## Description:

Check which exchanges work from your location and search for tokens with trading rules (min order size, price increment, order types).

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengtality](https://clawhub.ai/user/fengtality)

### License/Terms of Use:


## Use Case:

Developers and trading operators use this skill to check which Hummingbot exchange connectors are accessible from their location and to look up trading rules for token pairs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts handle trading API credentials and default to basic credentials if the environment does not override them.

Mitigation: Use only a local Hummingbot API you control and replace default credentials with unique credentials before running the scripts.

Risk: Remote API endpoints or untrusted environment files could expose credentials or alter script behavior.

Mitigation: Avoid remote HTTP endpoints and do not run the skill in directories containing untrusted .env files.

Risk: Untrusted token or data-file values passed to search_token.sh may be handled unsafely.

Mitigation: Pass only trusted token and data-file arguments, and review command inputs before execution.

Risk: Connector tests may overwrite or create trading-rules output data.

Mitigation: Expect test_all.sh to write data/trading_rules.json or a chosen output path and choose the output path deliberately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengtality/skills/connectors-available)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON files]

**Output Format:** [Markdown tables, shell command guidance, and JSON trading-rules data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write data/trading_rules.json or a caller-selected output path.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
