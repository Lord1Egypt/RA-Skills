## Description: <br>
Searches local Apple Mail on macOS with fruitmail for fast metadata lookup, message opening, and full body reading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gumadeiras](https://clawhub.ai/user/gumadeiras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users on macOS use this skill to find and inspect local Apple Mail messages by subject, sender, recipient, date, unread state, and body content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The fruitmail CLI and the agent can access local Apple Mail search results and full email bodies. <br>
Mitigation: Install and run only in environments where that local email access is acceptable, and treat returned email content as private data. <br>
Risk: Email bodies may contain untrusted or misleading text that an agent could over-trust. <br>
Mitigation: Review important results before acting on them, especially when email content influences follow-up commands or decisions. <br>
Risk: The skill depends on an external npm package for local mail access. <br>
Mitigation: Review the fruitmail package before use in environments that require supply-chain assurance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gumadeiras/apple-mail-search-safe) <br>
- [fruitmail npm package](https://www.npmjs.com/package/fruitmail) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON output from fruitmail.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May surface private local email metadata and body text from Apple Mail; fruitmail supports --json for structured command output.] <br>

## Skill Version(s): <br>
5.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
