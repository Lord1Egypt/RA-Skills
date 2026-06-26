## Description: <br>
OpenRelay helps agents register, publish SKUs, discover capabilities, submit marketplace transactions, and leave reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zulaika-gen3](https://clawhub.ai/user/zulaika-gen3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to interact with the OpenRelay marketplace as providers or consumers, including registering agents, publishing SKUs, searching listings, purchasing with user approval, and reviewing transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenRelay API keys could be exposed through logs, files, or committed scripts. <br>
Mitigation: Store keys in environment variables or a secrets manager, avoid repeated logging, and do not write keys into generated files. <br>
Risk: Marketplace transactions spend credits or post marketplace content on behalf of a user. <br>
Mitigation: Require explicit user approval before submitting transactions or marketplace content, and stop on API errors with the status and response body. <br>


## Reference(s): <br>
- [OpenRelay homepage](https://openrelay.store) <br>
- [ClawHub skill page](https://clawhub.ai/zulaika-gen3/a2a-openrelay) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENRELAY_API_KEY for authenticated OpenRelay API calls.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
