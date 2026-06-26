## Description: <br>
Call 179 professional agents on-demand from database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[717986230](https://clawhub.ai/user/717986230) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and ClawHub users use this skill to search, browse, retrieve, and apply bundled agent prompts for tasks such as code review, system architecture, growth strategy, and multi-agent collaboration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is marked suspicious because it asks users to share a ClawHub token and carries high-authority capability tags. <br>
Mitigation: Authenticate only through official browser or local CLI flows, never paste tokens into chat, and review the skill before installation. <br>
Risk: Retrieved agent prompts are lower-trust content and may request sensitive actions such as posting, payments, wallet use, purchases, or signing. <br>
Mitigation: Review each retrieved prompt before giving it tool access, and keep wallet, purchase, posting, and signing tools disabled unless explicitly approved. <br>
Risk: The skill initializes and queries a local prompt database populated from bundled agent data. <br>
Mitigation: Install only when a local reusable prompt library is desired, and inspect the bundled agent data before using retrieved prompts in higher-trust workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/717986230/agency-agents-caller) <br>
- [Publisher profile](https://clawhub.ai/user/717986230) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Python dictionaries, CLI text output, and retrieved Markdown prompt content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Retrieves local SQLite records initialized from bundled agent data.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
