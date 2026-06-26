## Description: <br>
Search Discord message history stored in a local discrawl SQLite database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonathanjing](https://clawhub.ai/user/jonathanjing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace agents use this skill to search local Discord guild archives for prior messages, channels, authors, and time-bounded context when answering questions about past conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad searches over local Discord archives can expose private or sensitive message content. <br>
Mitigation: Use explicit channel, author, and time filters, and only query archives the user is authorized to inspect. <br>
Risk: The shell SQL helper is unsafe for untrusted query text unless hardened. <br>
Mitigation: Review or harden the helper before passing user-supplied strings, and prefer scoped discrawl search filters where possible. <br>


## Reference(s): <br>
- [Discrawl Database Schema Reference](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline shell commands and SQL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include discrawl CLI commands, SQL query patterns, filters, and concise guidance for searching local Discord archives.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
