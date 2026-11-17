## Description:

Trades World Cup 2026 knockout-stage player fantasy-score markets on propSPACE by building multimodal distribution beliefs from FunctionSpace expected points and optional sentiment enrichment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bridgeaisocial](https://clawhub.ai/user/bridgeaisocial)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-agent operators use this skill to evaluate and optionally place play-money propSPACE positions for World Cup knockout player fantasy-score markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a propSPACE account, persist bearer tokens locally, and place account-affecting play-money trades when --live is used.

Mitigation: Run dry-run, list, and inspect modes before --live; keep .auth out of archives and source control; delete stored tokens when no longer needed.

Risk: The default FS_PASSWORD is weak and reused if the user does not override it.

Mitigation: Set a unique FS_PASSWORD of at least six characters before running the skill, especially for production bots.

Risk: Changing FS_BASE_URL can send credentials and trades to a nonstandard endpoint.

Mitigation: Use the official HTTPS FunctionSpace engine URL unless intentionally testing against a trusted endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bridgeaisocial/skills/fs-worldcup-knockout)
- [propSPACE live campaign](https://propspace.fun)
- [propSPACE signup](https://app.propspace.fun)
- [FunctionSpace competition engine](https://fs-engine-api-mech-v0-4.onrender.com)
- [FunctionSpace handoff](FUNCTIONSPACE_HANDOFF.md)
- [Skill disclaimer](DISCLAIMER.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline shell commands and runtime text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run output is read-only; passing --live can place propSPACE play-money trades.]

## Skill Version(s):

0.1.5 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
