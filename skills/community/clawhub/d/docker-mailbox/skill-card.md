## Description: <br>
docker-mailbox lets agents use a running mailboxd server to read, search, send, mark-seen, and delete mail across multiple IMAP/SMTP accounts through REST and MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psyb0t](https://clawhub.ai/user/psyb0t) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an agent or script to configured real email accounts for unified mailbox search, message retrieval, sending, deletion, and mailbox state changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent access to real email accounts, including read, send, mark-seen, and delete actions. <br>
Mitigation: Use it only with accounts and scopes intended for agent access, require explicit review before sending or deleting mail, and monitor mailbox activity. <br>
Risk: An unauthenticated or publicly exposed mailboxd service could expose email contents or allow mailbox actions. <br>
Mitigation: Configure strong auth.tokens before any non-local exposure, keep the service bound locally or behind a protected proxy, and rotate tokens when needed. <br>
Risk: config.yaml contains mailbox passwords and bearer tokens. <br>
Mitigation: Treat config.yaml as a secret, keep it out of source control and chat transcripts, restrict file permissions, and mount it read-only into containers. <br>
Risk: Using an unverified Docker image or repository can introduce supply-chain risk. <br>
Mitigation: Verify the Docker image and repository before deployment and pin trusted image versions for production use. <br>


## Reference(s): <br>
- [Setup guide](references/setup.md) <br>
- [Project homepage](https://github.com/psyb0t/docker-mailbox) <br>
- [html2text](https://github.com/Alir3z4/html2text) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown with curl commands, JSON request and response examples, and MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a running mailboxd service, MAILBOX_URL, and optional MAILBOX_TOKEN.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
