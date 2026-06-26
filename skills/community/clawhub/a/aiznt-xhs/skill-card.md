## Description: <br>
Generates Xiaohongshu-style multi-page graphic layout content from JSON input. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangshengli0421](https://clawhub.ai/user/wangshengli0421) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to send JSON content to a configured Xiaohongshu layout service and receive generated multi-page layout output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided Xiaohongshu content is sent to a configured upstream service. <br>
Mitigation: Install only when the upstream service is trusted and avoid submitting secrets, personal data, or regulated content without approval. <br>
Risk: The skill requires a TS_TOKEN credential for service access. <br>
Mitigation: Treat TS_TOKEN as sensitive and keep it out of logs, source files, and shared transcripts. <br>


## Reference(s): <br>
- [XHS Layout on ClawHub](https://clawhub.ai/wangshengli0421/aiznt-xhs) <br>
- [Publisher profile: wangshengli0421](https://clawhub.ai/user/wangshengli0421) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Configuration instructions] <br>
**Output Format:** [JSON returned by a command-line script after calling a configured upstream service] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TS_TOKEN and AIZNT_PROXY_URLS environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
