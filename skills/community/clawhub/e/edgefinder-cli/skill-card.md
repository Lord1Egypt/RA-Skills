## Description: <br>
Use the EdgeFinder CLI for NFL, NBA, and MLB analysis, plus NFL/NBA schedules, standings, Polymarket odds, and portfolio lookups from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andrewnexys](https://clawhub.ai/user/andrewnexys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to call EdgeFinder from an agent workflow for sports betting analysis, schedules, standings, Polymarket odds, and portfolio lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can require an EdgeFinder API key for authenticated CLI access. <br>
Mitigation: Treat EDGEFINDER_API_KEY like a password, keep it in environment or agent configuration, and do not paste or echo the full key in chat or logs. <br>
Risk: If the local edgefinder binary is not installed, the wrapper can execute the published @edgefinder/cli package through npx. <br>
Mitigation: Install and pin the CLI through a trusted package workflow when possible, and use the npx fallback only when you are comfortable executing the npm package. <br>
Risk: Sports betting analysis and odds can be incomplete, stale, or unsuitable for a user's jurisdiction or risk tolerance. <br>
Mitigation: Review CLI output before acting on it and treat it as decision support rather than guaranteed betting advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andrewnexys/edgefinder-cli) <br>
- [Publisher profile](https://clawhub.ai/user/andrewnexys) <br>
- [EdgeFinder CLI homepage](https://github.com/andrewnexys/edgefinder-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-output recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke the EdgeFinder CLI or npx fallback and may use EDGEFINDER_API_KEY for authenticated requests.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
