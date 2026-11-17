## Description: <br>
This skill guides agents through uploading audio files to a third-party streaming API with batch queues, resumable chunk uploads, encoding presets, and metadata configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, media operators, and content teams use this skill to prepare API calls, Python snippets, shell commands, and configuration for uploading authorized audio files with custom streaming settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to send selected local audio files, metadata, and API credentials to a third-party upload service. <br>
Mitigation: Install only if the upload service is trusted, confirm exact file paths and destination before upload, and avoid sensitive or copyrighted media unless authorized. <br>
Risk: API keys may be exposed through generated commands, headers, logs, or copied snippets. <br>
Mitigation: Use dedicated limited-permission API keys, provide credentials through environment variables, and avoid printing or storing secrets in outputs. <br>
Risk: The artifact declares read, write, and exec tool use while upload workflows may involve shell commands and local file access. <br>
Mitigation: Require explicit approval of each command and file path, run in a constrained workspace, and prefer reviewed command templates over ad hoc shell execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/thcjp/skills/audio-stream-upload) <br>
- [Third-party upload API endpoint](https://api-w3stream.attoaioz.cyou/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Python, shell, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include upload configuration, retry guidance, metadata examples, and API request templates.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
