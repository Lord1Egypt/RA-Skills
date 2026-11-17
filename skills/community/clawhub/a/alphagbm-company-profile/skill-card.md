## Description:

Build and maintain company research profiles on AlphaGBM from fundamentals, PE/PB band history, financial red flags, and event radar, with scheduled refreshes for each user and ticker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create, list, refresh, view, and archive private AlphaGBM company research profiles and to retrieve PE/PB valuation band data for tickers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a bearer API key and supports a configurable base URL.

Mitigation: Store ALPHAGBM_API_KEY in managed secrets, keep ALPHAGBM_BASE_URL unset unless a trusted AlphaGBM-compatible endpoint is intentionally used, and review endpoint configuration before deployment.

Risk: The skill can create, refresh, and archive private company profiles in a mutable workspace.

Mitigation: Review profile create, refresh, and archive actions with the user before allowing them, especially when tier limits or archived status could affect the workspace.

Risk: Server security evidence marks the release suspicious because of broad activation language around private workspace operations.

Mitigation: Restrict use to explicit company-profile, research-brain, knowledge-base, or PE/PB-band requests and review proposed API actions before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clementgu/skills/alphagbm-company-profile)
- [AlphaGBM Website](https://alphagbm.com)
- [Default AlphaGBM API Base URL](https://alphagbm.zeabur.app)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown, Configuration instructions]

**Output Format:** [Markdown with API request examples and JSON response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ALPHAGBM_API_KEY; ALPHAGBM_BASE_URL is optional and should only target a trusted AlphaGBM-compatible endpoint.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
