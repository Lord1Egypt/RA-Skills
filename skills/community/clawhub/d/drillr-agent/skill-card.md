## Description: <br>
Drillr gives agents access to financial research, market signals, analyst articles, and account-backed watchlists through MCP, REST, or CLI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[little-grebe](https://clawhub.ai/user/little-grebe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer market research questions, review company fundamentals and signals, read Drillr articles, and manage Drillr watchlists after configuring a dedicated API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dedicated Drillr API key, and the security evidence notes that users may paste live keys into chat. <br>
Mitigation: Configure the key through a local secret store or environment managed outside chat, avoid pasting raw keys into conversations or shell history, and use a revocable least-privilege key when available. <br>
Risk: The skill can access or change persistent account-backed Drillr watchlists. <br>
Mitigation: Require explicit user confirmation before deleting watchlists or making bulk watchlist changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/little-grebe/drillr-agent) <br>
- [Drillr homepage](https://drillr.ai) <br>
- [Drillr developer portal](https://drillr.ai/developer) <br>
- [Drillr API reference](https://drillr.ai/developer/docs) <br>
- [Create or manage Drillr API keys](https://drillr.ai/developer/keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, YAML, and shell command examples; Drillr API responses may be JSON or markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-specific Drillr API key and may access or change persistent per-user Drillr watchlists.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
