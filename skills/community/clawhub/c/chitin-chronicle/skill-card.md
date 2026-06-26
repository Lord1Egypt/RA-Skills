## Description: <br>
Coordinates multi-agent content publishing with a shared content registry, claim system, publication ledger, and timeline tracker to prevent duplicate publishing across agents and channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adroidian](https://clawhub.ai/user/adroidian) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent teams use this skill to coordinate content publishing across multiple agents and channels. It helps agents check for conflicts, claim work, record publications, and inspect timeline state before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted content IDs, channels, actions, or agent names could cause unintended shell command execution through git command handling. <br>
Mitigation: Review carefully before installing and use only trusted values until the CLI avoids shell-string git commands and validates safe characters. <br>
Risk: Claim filenames are derived from command inputs, which can create unsafe paths if untrusted identifiers are accepted. <br>
Mitigation: Constrain content IDs and agent names to a known safe character set before using the claim and release commands in shared workspaces. <br>
Risk: Git commit failures are ignored, which can leave registry, ledger, or claim changes without the expected audit trail. <br>
Mitigation: Verify git configuration before use and periodically check the ledger, registry, claims, and commit history after publishing operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/adroidian/chitin-chronicle) <br>
- [Publisher Profile](https://clawhub.ai/user/adroidian) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Test Results](artifact/TEST_RESULTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-backed workflow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Node.js and Bash workflow; zero external package dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
