## Description: <br>
Queries a 1688 distribution knowledge base for shipping workflows, product listing operations, order management, and related distribution guidance, with optional filtering by sales channel and distribution tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve Chinese-language 1688 distribution documentation and convert the results into actionable operating steps with source links. It is intended for questions about fulfillment, product distribution, order handling, platform workflows, and tool-specific 1688 distribution processes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can expose a sensitive 1688 AK if the user pastes it into chat or stores it in an uncontrolled location. <br>
Mitigation: Use a platform-managed secret entry method where possible, avoid pasting the AK into chat, and rotate the AK if exposure is suspected. <br>
Risk: The skill may transmit the AK through an untrusted gateway endpoint if OPENCLAW_GATEWAY_URL is changed. <br>
Mitigation: Verify OPENCLAW_GATEWAY_URL points to a trusted local or managed gateway before configuring credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/1688-distribution-knowledge-newton) <br>
- [1688 AK portal](https://clawhub.1688.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Chinese-language Markdown with numbered steps, source URLs, image links when present, and inline shell commands for credential setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to 20 ranked knowledge documents with score, content, and source URL; prompts for a 1688 AK, channel, and distribution tool when required.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
