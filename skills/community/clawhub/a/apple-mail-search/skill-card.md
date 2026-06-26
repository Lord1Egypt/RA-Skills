## Description: <br>
Fast Apple Mail search via SQLite on macOS. Search emails by subject, sender, date, attachments - results in ~50ms vs 8+ minutes with AppleScript. Use when asked to find, search, or list emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mneves75](https://clawhub.ai/user/mneves75) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and macOS users use this skill to have an agent search local Apple Mail metadata quickly by subject, sender, recipient, date, unread status, and attachments. It is intended for finding, listing, opening, or exporting Apple Mail search results from the local Mail database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Apple Mail search results and exports can contain private email metadata. <br>
Mitigation: Keep result limits narrow and review JSON or CSV exports before sharing them. <br>
Risk: The skill depends on a separate local mail-search executable with access to Apple Mail metadata. <br>
Mitigation: Verify the executable before copying it into /usr/local/bin and install only on Macs where local Apple Mail search is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mneves75/apple-mail-search) <br>
- [Skill homepage](https://github.com/steipete/clawdbot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON or CSV command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide bounded searches with result limits and optional database path selection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
