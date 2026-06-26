## Description: <br>
Research upcoming earnings events, analyze historical beat/miss patterns, and estimate post-earnings price reactions using the Finskills API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finskills](https://clawhub.ai/user/finskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research earnings calendars, per-stock earnings history, estimate revisions, options-implied moves, and pre-earnings setups using Finskills market data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Finskills API key, which is a sensitive credential. <br>
Mitigation: Store the key only in the required FINSKILLS_API_KEY environment variable and avoid exposing it in prompts, logs, or shared outputs. <br>
Risk: Earnings dates, market data, estimate revisions, and options prices can be stale, delayed, or incorrect. <br>
Mitigation: Verify important data against company investor relations pages, broker data, or another market data source before acting on it. <br>
Risk: Generated earnings setups may be mistaken for investment advice. <br>
Mitigation: Treat outputs as research support only and make trading or investment decisions through qualified review and independent analysis. <br>


## Reference(s): <br>
- [ClawHub earnings-analyst page](https://clawhub.ai/finskills/earnings-analyst) <br>
- [Finskills earnings-analyst homepage](https://github.com/finskills/earnings-analyst) <br>
- [Finskills API](https://finskills.net) <br>
- [Finskills registration](https://finskills.net/register) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown earnings calendar or per-ticker earnings analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tabular earnings history, estimate revision summaries, options-implied move ranges, recent news signals, and key watch items.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
