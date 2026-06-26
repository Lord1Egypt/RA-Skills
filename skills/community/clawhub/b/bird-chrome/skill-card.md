## Description: <br>
Use bird with Chrome cookies to read, search, and carefully post on X/Twitter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvanDataForge](https://clawhub.ai/user/EvanDataForge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to inspect X/Twitter content through the bird CLI with Chrome cookie authentication, then route posts and replies through browser-based confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent use a logged-in X/Twitter session through Chrome cookies. <br>
Mitigation: Use a dedicated browser profile or test account, keep workflows read-only by default, and do not share raw session tokens unless absolutely necessary. <br>
Risk: Posting and replying can publish content publicly from the user's account. <br>
Mitigation: Require explicit confirmation of the exact post or reply before submission and review browser actions before clicking Post or Reply. <br>
Risk: Direct bird write commands are identified by the artifact as account-suspension risk. <br>
Mitigation: Use bird only for read-only commands and route posts or replies through the OpenClaw Browser Gateway. <br>


## Reference(s): <br>
- [Bird CLI homepage](https://bird.fast) <br>
- [Bird Chrome on ClawHub](https://clawhub.ai/EvanDataForge/bird-chrome) <br>
- [EvanDataForge publisher profile](https://clawhub.ai/user/EvanDataForge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON output flags for read-only bird commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
