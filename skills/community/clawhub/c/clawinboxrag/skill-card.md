## Description: <br>
Community skill for parsing and executing local mailbox retrieval commands (`mail ...`) against a local backend with safe defaults, bounded output, and read-only constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dmoraine](https://clawhub.ai/user/dmoraine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to translate `mail ...` requests into local mailbox retrieval, status, label, sync, and recent-message commands for a configured ClawInboxRAG backend. It is intended for read-only Gmail search workflows with bounded, snippet-oriented output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and locally index Gmail mailbox data through a trusted local backend. <br>
Mitigation: Install only when read-only Gmail access is intended, review the configured GMAIL_RAG_REPO backend, and confirm where local indexes and embeddings are stored. <br>
Risk: OAuth tokens, secret paths, and indexed mail data are sensitive. <br>
Mitigation: Protect local token files, avoid exposing credential paths or tokens in outputs, and confirm the process for deleting local indexed data. <br>
Risk: Broad or malformed mail commands could return more mailbox context than intended. <br>
Mitigation: Keep numeric limits clamped, use allowlisted subcommands, and return concise snippets rather than full raw message bodies by default. <br>


## Reference(s): <br>
- [ClawInboxRAG ClawHub page](https://clawhub.ai/dmoraine/clawinboxrag) <br>
- [Commands](references/commands.md) <br>
- [Security Guidance](references/security.md) <br>
- [Setup](references/setup.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON parser output and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output is bounded by configured result limits and avoids full raw message bodies by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
