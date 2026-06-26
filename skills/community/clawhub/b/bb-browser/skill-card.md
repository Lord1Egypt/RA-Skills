## Description: <br>
Turn websites into CLI commands for structured extraction across supported platforms using bb-browser through OpenClaw's browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yan5xu](https://clawhub.ai/user/yan5xu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover and run bb-browser site adapters that extract structured website data through the user's OpenClaw browser session. It is useful for social, developer, finance, news, video, shopping, and knowledge workflows that benefit from CLI-accessible web data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate through logged-in OpenClaw browser sessions and extract account-visible website data. <br>
Mitigation: Use a separate or least-privileged browser profile and avoid sensitive accounts unless the workflow requires them. <br>
Risk: Community site adapters may change what data they access or how commands behave after updates. <br>
Mitigation: Review adapters before updating and approve each target site and command intentionally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yan5xu/bb-browser) <br>
- [Publisher profile](https://clawhub.ai/user/yan5xu) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands commonly include --openclaw and may include --json or --jq filtering for structured output.] <br>

## Skill Version(s): <br>
0.6.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
