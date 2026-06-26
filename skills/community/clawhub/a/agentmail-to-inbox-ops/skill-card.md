## Description: <br>
Manage Agentmail.to inbox operations with deterministic Python scripts for listing and reading messages, downloading and analyzing attachments, replying with sender filters, and setting read or unread state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4ur3l](https://clawhub.ai/user/4ur3l) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage existing Agentmail.to inboxes through repeatable scripts for reading, filtering, replying, attachment handling, and mailbox state changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send replies and change mailbox read state in bulk. <br>
Mitigation: Run reply workflows with --dry-run first, keep sender allowlists explicit, and use scoped Agentmail API credentials where available. <br>
Risk: Downloaded attachments and parsed document content may be untrusted. <br>
Mitigation: Keep downloaded files private, rely on the default metadata-only analysis unless text extraction is needed, and prefer sandboxed or containerized execution for PDF or DOCX parsing. <br>
Risk: Broad sender allowlists can cause unintended replies to messages outside the intended workflow. <br>
Mitigation: Use narrow AGENTMAIL_ALLOWED_SENDERS values or an explicit --from-email override before sending real replies. <br>


## Reference(s): <br>
- [Agentmail.to](https://www.agentmail.to/) <br>
- [AgentMail API notes](references/agentmail-api-notes.md) <br>
- [ClawHub release page](https://clawhub.ai/4ur3l/agentmail-to-inbox-ops) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts emit JSON for inbox operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses unread-only and low-limit defaults for listing and reply workflows; attachment analysis reports hashes, parsing status, and truncated summaries.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata; artifact pyproject.toml reports 0.1.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
