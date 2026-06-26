## Description: <br>
Apple Mail search on macOS with fast metadata and full body lookup for finding messages by subject, sender, recipient, date, opening messages, and reading full body text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DurtyDhiana](https://clawhub.ai/user/DurtyDhiana) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Mac users and agents use this skill to search local Apple Mail messages, inspect matching metadata, read selected message bodies, and open messages in Mail.app. It is intended for local mailbox lookup workflows where the user is comfortable granting access to email content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose local Apple Mail content to the agent when searches or body reads are requested. <br>
Mitigation: Use narrow filters and limits, avoid full-body reads unless needed, and confirm that email content is appropriate to share with the agent. <br>
Risk: Email body text may contain prompt-injection attempts or misleading instructions. <br>
Mitigation: Treat email contents as untrusted data and do not let them override the agent's normal instructions. <br>
Risk: The required external npm package determines the behavior of the fruitmail command installed on the system. <br>
Mitigation: Verify the npm package before installing and use the read-only or copy-mode behavior described by the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DurtyDhiana/apple-mail-search-safe-5-0-4) <br>
- [Skill homepage](https://clawdhub.com/gumadeiras/apple-mail-search-safe) <br>
- [fruitmail CLI repository](https://github.com/gumadeiras/fruitmail-cli) <br>
- [npm package: apple-mail-search-cli](https://www.npmjs.com/package/apple-mail-search-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON command output when the underlying fruitmail CLI is used with --json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact metadata version 5.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
