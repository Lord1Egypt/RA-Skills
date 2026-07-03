## Description: <br>
Trades World Cup 2026 knockout-stage propSPACE play-money player fantasy-score markets by building a multimodal distribution from FunctionSpace expected points plus optional sentiment and selecting high-divergence positions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bridgeaisocial](https://clawhub.ai/user/bridgeaisocial) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agent operators use this skill to inspect, dry-run, and optionally place propSPACE play-money positions for World Cup 2026 knockout-stage player fantasy-score markets. The default workflow selects one FWD, one MID, and one DEF for the current open round, while --live performs the play-money trade mutation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: --live can place propSPACE play-money positions that affect a real-prize competition. <br>
Mitigation: Run --list-markets, --inspect, and the default dry run before using --live; keep FS_MAX_COLLATERAL within the intended play-money budget. <br>
Risk: The default FS_PASSWORD is weak and persisted authentication tokens are sensitive. <br>
Mitigation: Set a unique strong FS_PASSWORD before first use and protect or remove .auth token files after execution. <br>
Risk: The optional Brave enrichment script can expose part of BRAVE_API_KEY in shared logs. <br>
Mitigation: Avoid running enrichment in shared log environments until the API-key print is removed or masked. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bridgeaisocial/skills/fs-worldcup-knockout) <br>
- [FunctionSpace / propSPACE](https://functionspace.dev) <br>
- [FunctionSpace World Cup competition engine](https://fs-engine-api-mech-v0-4.onrender.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output with Markdown setup instructions and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run by default; passing --live places propSPACE play-money positions.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
