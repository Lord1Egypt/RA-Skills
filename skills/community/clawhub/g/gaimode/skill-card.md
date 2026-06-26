## Description: <br>
Performs Google AI Mode searches through a local authenticated Google browser session or exported Google cookies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whoisdhana](https://clawhub.ai/user/whoisdhana) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to retrieve Google AI Mode search results for current information such as sports scores, stock prices, news, weather, and AI summaries. It requires access to a local Google session through Chrome CDP or a cookies file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an authenticated Google browser session or exported Google cookies. <br>
Mitigation: Use a separate Chrome profile or low-risk Google account, and protect cookies.json like a password. <br>
Risk: Chrome CDP mode opens a browser debugging port and the launcher can close existing Chrome windows. <br>
Mitigation: Run the launcher only intentionally, avoid unsaved browser work, and close the CDP browser when finished. <br>
Risk: The server security verdict is suspicious because session access and browser debugging require review before installation. <br>
Mitigation: Install only after confirming that this access pattern is acceptable for the intended environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whoisdhana/gaimode) <br>
- [Publisher profile](https://clawhub.ai/user/whoisdhana) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text CLI output with search results, status messages, and setup instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output is truncated by the CLI; operation depends on an active Chrome CDP session or a valid local cookies file.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
