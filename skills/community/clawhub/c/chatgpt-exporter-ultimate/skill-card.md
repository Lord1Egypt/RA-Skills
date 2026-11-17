## Description:

Exports ChatGPT conversation lists and, when explicitly requested, message text to local JSON and Markdown files through a browser relay or bookmarklet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to create local backups or readable copies of their own ChatGPT conversations, with index-only export as the default and full message export available after explicit consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read ChatGPT conversation history through the user's logged-in browser session.

Mitigation: Run it only for your own account after reviewing the consent prompt and export scope.

Risk: Full exports can write sensitive conversation text, secrets, or personal data to plaintext local files.

Mitigation: Use index-only mode unless message bodies are needed, enable redaction for full exports, and review files before sharing them.

Risk: Plaintext exports may be exposed if saved in synced, shared, or overly broad locations.

Mitigation: Keep exports in the private local destination, avoid synced or repository folders, and purge exports when finished.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/globalcaos/skills/chatgpt-exporter-ultimate)

## Skill Output:

**Output Type(s):** [Files, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Local JSON and Markdown export files, plus concise confirmation and cleanup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default relay output is index-only; full message text is optional and writes plaintext local files.]

## Skill Version(s):

1.9.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
