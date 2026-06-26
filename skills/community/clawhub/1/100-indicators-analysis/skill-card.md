## Description: <br>
Provides technical indicator calculation, analysis, and visualization based on 100 popular TradingView Pine Script indicators through a Prana remote wrapper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luokeer52](https://clawhub.ai/user/luokeer52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and trading-tool users can route requests to a Prana-hosted skill for technical indicator analysis derived from TradingView Pine Script indicators. The local package is a lightweight client wrapper and does not contain the underlying indicator implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User requests and trading-analysis prompts are forwarded to Prana for remote execution. <br>
Mitigation: Use the skill only with data approved for Prana processing, and avoid sending confidential trading strategies or account details unless that use is authorized. <br>
Risk: Prana API credentials may be stored in local config files. <br>
Mitigation: Prefer environment-provided credentials, keep config/api_key.txt and config/api_key.json out of version control, and set PRANA_SKILL_SKIP_WRITE_API_KEY=1 to avoid writing fetched keys to disk. <br>
Risk: The client can automatically request or create Prana API credentials when local credentials are missing. <br>
Mitigation: Set PRANA_SKILL_NO_AUTO_API_KEY=1 when automatic credential creation is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luokeer52/100-indicators-analysis) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown or JSON returned by the Prana client, depending on the remote skill response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Prana API credentials and network access; multi-turn use may preserve a thread_id from the remote response.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
