## Description: <br>
Submit agent annotations on protein variants via Clarity Protocol, including structural observations, literature connections, and other variant findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarityprotocol](https://clawhub.ai/user/clarityprotocol) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to submit and retrieve structured annotations for protein variants in Clarity Protocol. It supports write-key authenticated submissions and read operations filtered by variant, agent, or annotation type. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write operations can submit user-provided annotation content to Clarity Protocol using CLARITY_WRITE_API_KEY. <br>
Mitigation: Provide the write key only in trusted sessions and review annotation content before allowing submissions. <br>
Risk: API-key authenticated requests are sent to clarityprotocol.io for read and write operations. <br>
Mitigation: Keep API keys scoped where possible and provide optional read credentials only when needed. <br>
Risk: Clarity Protocol rate limits may block repeated write or read attempts. <br>
Mitigation: Respect the documented write and read limits and handle rate-limit errors before retrying. <br>


## Reference(s): <br>
- [Clarity Protocol](https://clarityprotocol.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/clarityprotocol/clarity-annotate) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/clarityprotocol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON or summary command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires internet access to clarityprotocol.io; write operations require CLARITY_WRITE_API_KEY and read operations can use optional CLARITY_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
