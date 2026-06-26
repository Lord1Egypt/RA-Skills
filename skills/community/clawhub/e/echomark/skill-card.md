## Description: <br>
Rate tools you use (MCP servers, skills, CLI tools, APIs) and query ratings to make informed tool choices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruoxi0324](https://clawhub.ai/user/ruoxi0324) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use EchoMark to record local ratings for tools after use and query past ratings before choosing a tool. It supports local-first rating history with optional cloud registration, submission, and community rating lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags plaintext cloud communication and generated API key exposure. <br>
Mitigation: Prefer local-only mode unless cloud sharing is intentional, and set ECHO_MARK_API_URL to a trusted HTTPS endpoint before registration or cloud use. <br>
Risk: The registration flow prints the generated API key after saving it. <br>
Mitigation: Treat any printed API key as exposed, limit access to ~/.echomark/api_key, and rotate or replace the key if terminal output may have been logged. <br>
Risk: Tool names, numeric scores, and optional comments may be sent to the cloud service. <br>
Mitigation: Avoid sensitive tool names or comments, and use --local-only when ratings should remain on the local machine. <br>
Risk: Automatic or broad tool-rating workflows can create misleading reliability data. <br>
Mitigation: Submit ratings only after concrete tool use and review scores for accuracy, stability, efficiency, and usability before sharing them. <br>


## Reference(s): <br>
- [EchoMark ClawHub Page](https://clawhub.ai/ruoxi0324/echomark) <br>
- [EchoMark GitHub Repository](https://github.com/Duroxi/EchoMark) <br>
- [EchoMark Philosophy](https://github.com/Duroxi/EchoMark/blob/main/PHILOSOPHY.md) <br>
- [README](artifact/README.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ratings are stored in a local SQLite database by default; cloud registration, submission, and query flows use API calls when enabled.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
