## Description:

Fetches public OKX spot prices for requested cryptocurrency symbols, displays USD-denominated prices in input order, and supports text or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chgy123](https://clawhub.ai/user/chgy123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to answer cryptocurrency price questions by running a small OKX market-data lookup helper for specified symbols. It is suited to public spot-price lookups where live exchange data is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper makes live HTTPS requests to OKX, so availability, latency, and returned prices depend on an external market-data service.

Mitigation: Allow outbound access to www.okx.com only when live public price lookup is intended, and verify important prices against another trusted source before acting on them.

Risk: The Python dependency is declared as a lower-bound requests version rather than a pinned version.

Mitigation: Pin and scan the dependency in managed deployments before installing the skill.

Risk: The usage examples include an install path that may not match every runtime environment.

Mitigation: Confirm the local skill path before running the example command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chgy123/skills/btc-price)
- [OKX public market endpoint host](https://www.okx.com)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text price list or JSON array from a Python command-line helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns one result per requested symbol, preserving input order and selecting USDT, then USDC, then USD spot pairs when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
