## Description: <br>
Monitors and controls the AutoSignals autonomous research loop. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research engineers use this skill to monitor, start, stop, and inspect a local autonomous trading-signal research loop. It supports experimentation with signal logic and backtest results, not live trading or guaranteed profitable strategies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls an autonomous trading-research loop that can run continuously, edit local files, and write logs. <br>
Mitigation: Use it in a dedicated sandbox or disposable repository, review the affected files and logs, and confirm start and stop behavior before enabling the loop. <br>
Risk: Trading-signal experiments can produce misleading or overfit results and should not be treated as investment advice. <br>
Mitigation: Keep usage to research and development, avoid live trading connections, and require independent validation before using any generated signal logic. <br>
Risk: The security review classified the release as suspicious because the autonomous loop needs review before use. <br>
Mitigation: Follow the server security guidance: review resource impact, logging location, start/stop commands, and surrounding controls before installation. <br>


## Reference(s): <br>
- [AutoSignals ClawHub listing](https://clawhub.ai/clawdiri-ai/autosignals-davinci) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and status-oriented explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local project paths, logs, process IDs, score summaries, and experiment records.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
