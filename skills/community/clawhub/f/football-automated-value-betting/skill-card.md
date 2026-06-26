## Description: <br>
Automates live football odds monitoring, value-bet analysis, and Singbet Asian Handicap or Over/Under betting workflows with fixed-stake limits. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[hga030888-blip](https://clawhub.ai/user/hga030888-blip) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and betting-automation reviewers can use this skill to prototype live football odds analysis, value-bet reasoning, and fixed-stake bet execution workflows. It requires careful human oversight because the workflow can involve gambling decisions and credentials. <br>

### Deployment Geography for Use: <br>
Global, subject to local gambling laws and platform availability <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for automated sports betting and can support money-risking actions. <br>
Mitigation: Require explicit human confirmation before every wager and treat the current version as requiring human review before any real-money use. <br>
Risk: The artifact includes credential-style configuration for an odds API key and betting platform settings. <br>
Mitigation: Replace embedded keys, avoid storing betting credentials in plain configuration, and use a secret manager or runtime-provided credentials. <br>
Risk: Automated betting decisions may violate local gambling laws or platform terms. <br>
Mitigation: Deploy only where the operator has confirmed legal eligibility, account authorization, and platform compliance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hga030888-blip/football-automated-value-betting) <br>
- [Publisher Profile](https://clawhub.ai/user/hga030888-blip) <br>
- [The Odds API](https://the-odds-api.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with Python callable behavior and JSON-style configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce betting rationale, live-odds summaries, bet execution messages, and betting statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact configuration) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
