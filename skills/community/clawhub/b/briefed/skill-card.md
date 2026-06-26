## Description: <br>
Briefed sets up a personal AI newsletter intelligence system that fetches Gmail newsletters, uses Claude Haiku to summarize articles, and serves a local web reader with voting, notes, and interest tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jamesnation](https://clawhub.ai/user/jamesnation) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use Briefed with OpenClaw to build a daily Gmail newsletter digest, generate AI summaries, and review or save stories in a local reader. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The unauthenticated local reader can expose stored Gmail newsletter bodies if port 3001 is reachable beyond the user's machine. <br>
Mitigation: Bind the reader to 127.0.0.1 or add authentication, and do not expose port 3001 to a network. <br>
Risk: Read-only Gmail OAuth access and the local token file can expose personal newsletter content if mishandled. <br>
Mitigation: Protect the Gmail token file, use the read-only Gmail scope, and revoke the OAuth grant when the skill is no longer in use. <br>
Risk: Newsletter-derived content is sent to the configured model provider and any user-selected notification channel. <br>
Mitigation: Install only if that data flow is acceptable for the mailbox being processed and the configured provider and notification channel are trusted. <br>


## Reference(s): <br>
- [Briefed ClawHub release page](https://clawhub.ai/jamesnation/briefed) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [gog Gmail OAuth CLI](https://github.com/openclaw/gogcli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON, Code] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON schemas, configuration snippets, and bundled Python/Node.js files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup instructions and local workflow artifacts for Gmail fetching, AI summary generation, reader operation, notes, voting, and saved reading-list output.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
