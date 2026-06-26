## Description: <br>
Futures Radar helps agents fetch Yahoo Finance futures and commodity quotes for energy, metals, agricultural contracts, U.S. Treasury futures, and the DXY index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gold3bear](https://clawhub.ai/user/gold3bear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to retrieve current futures and commodity market snapshots, compare key ratios such as gold-silver and oil-gold, and frame market commentary from public Yahoo Finance data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Yahoo Finance when used for futures or commodity questions. <br>
Mitigation: Install and use it only in environments where outbound requests to Yahoo Finance are acceptable. <br>
Risk: Market commentary and quote-derived signals can be incorrect, delayed, or unsuitable for trading decisions. <br>
Mitigation: Treat outputs as informational market context, not financial advice, and verify prices before acting. <br>
Risk: The example command includes a local Windows path from the publisher's environment. <br>
Mitigation: Adjust the script path and Python dependency setup for the user's own environment before running commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gold3bear/futures-radar) <br>
- [Publisher profile](https://clawhub.ai/user/gold3bear) <br>
- [Yahoo Finance chart API endpoint](https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal text with optional Python and bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Market data depends on live Yahoo Finance responses and may be unavailable or delayed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
