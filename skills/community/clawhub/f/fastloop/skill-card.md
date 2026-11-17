## Description:

Guides an agent through configuring and operating a Polymarket fast-market trading loop for BTC, ETH, and SOL using momentum, funding, order book, timing, sizing, calibration, and fee-aware EV filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oryselias](https://clawhub.ai/user/oryselias)

### License/Terms of Use:


## Use Case:

External agents and users use this skill to configure paper-mode or live Polymarket fast-market trading workflows, tune signal and risk filters, and review calibration commands before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is for live automated trading, but the reviewed artifact does not include the referenced fastloop_improved.py trading script.

Mitigation: Do not run live or scheduled examples unless the missing script is independently obtained, audited, and matched to the documented behavior.

Risk: Persistent live execution can place real trades and create financial loss exposure.

Mitigation: Use paper mode first, configure narrowly scoped and revocable trading credentials, and enforce external spend and loss limits before any live run.

Risk: Dependencies and trading behavior were not fully reviewable from the provided artifact.

Mitigation: Pin and verify dependencies, review scanner output from the complete package, and keep live credentials separate from broader account access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oryselias/skills/fastloop)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash command blocks and configuration tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; live trading requires explicit --live usage.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
