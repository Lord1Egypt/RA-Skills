## Description: <br>
AI-powered tool generating structured news summaries from Twitter and RSS feeds with digest options for 4H, daily, weekly, and monthly intervals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[94W666](https://clawhub.ai/user/94W666) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use Clawfeed to run a news digest service that summarizes Twitter and RSS sources into recurring 4H, daily, weekly, or monthly digests. Readers can browse digests in read-only mode, while authenticated users can use bookmark and feed-management features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports unclear and conflicting access control for APIs that can change server state. <br>
Mitigation: Before installing or exposing the service, confirm from the actual source code that write and configuration endpoints require authentication or an API key. <br>
Risk: The security guidance warns against exposing the API publicly until access control is verified. <br>
Mitigation: Keep the API off the public internet or behind trusted network controls until authentication, API key protection, and CORS settings are validated. <br>
Risk: The security guidance notes that package and server files are missing from the evidence. <br>
Mitigation: Install only from a trusted source that includes the complete package and server files, then review those files before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/94W666/clawfeed-2) <br>
- [Publisher profile](https://clawhub.ai/user/94W666) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with setup commands, configuration tables, endpoint descriptions, and deployment guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documents read-only operation, optional Google OAuth credentials, API key configuration, SQLite runtime dependency, and reverse proxy setup.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
