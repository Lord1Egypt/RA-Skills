## Description:

Send physical letters anywhere in Germany with a single command, using an API key from agentic-letters.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eisimo](https://clawhub.ai/user/eisimo)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to send A4 PDF letters, cancellations, legal notices, data access requests, complaints, and similar documents to German postal addresses via agentic-letters.com.

### Deployment Geography for Use:

Germany

## Known Risks and Mitigations:

Risk: Sensitive PDFs, recipient names, addresses, and letter metadata are sent to agentic-letters.com.

Mitigation: Use only with user consent for the exact document and recipient, minimize sensitive content, and delete records that are no longer needed.

Risk: Sending a letter consumes credits and initiates real postal mail.

Mitigation: Require final manual confirmation of the exact PDF, recipient, country, and expected cost or credit impact before running the send command.

Risk: API keys and local letter records can expose account access and PII if stored with broad permissions.

Mitigation: Store the API key and generated records with owner-only permissions and periodically remove obsolete records.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/eisimo/skills/agentic-letters)
- [Agentic Letters Website](https://agentic-letters.com)
- [Agentic Letters API Key Purchase](https://agentic-letters.com/buy)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, JSON, files]

**Output Format:** [Markdown guidance with shell commands; the CLI returns JSON to stdout and stores local JSON letter records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AGENTIC_LETTERS_API_KEY; sent-letter records include recipient and letter metadata.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
