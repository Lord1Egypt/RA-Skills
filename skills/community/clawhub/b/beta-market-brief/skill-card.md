## Description: <br>
Generates concise Chinese hourly market briefs for trader agents using Tiger API data first and Yahoo Finance as supplementary context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1477009639zw-blip](https://clawhub.ai/user/1477009639zw-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders or market-briefing agents use this skill to request hourly Chinese market snapshots backed by Tiger API data. The skill directs the agent to return the referenced script output with minimal extra commentary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to run a hard-coded local Python script that was not included in the artifact. <br>
Mitigation: Install only after reviewing the referenced tiger_market_brief.py script and confirming it reads market data without placing trades or accessing unrelated account data. <br>
Risk: Broad market-brief triggers could cause the agent to run the local script when the user did not explicitly intend a Tiger market brief. <br>
Mitigation: Use the skill only for explicit Tiger market-brief requests and confirm the expected data sources before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1477009639zw-blip/beta-market-brief) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and direct script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The expected brief is concise Chinese text; market data should come from Tiger API first, with Yahoo Finance only as supplementary context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
