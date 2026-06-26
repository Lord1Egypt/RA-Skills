## Description: <br>
Builds structured Obsidian daily and weekly review notes from conversations or existing markdown notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amortalsodyssey](https://clawhub.ai/user/amortalsodyssey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who use Obsidian for work logs and AI-assisted development use this skill to turn conversations and daily notes into durable daily summaries, weekly reports, tags, and wikilinks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify local Obsidian daily and weekly markdown notes. <br>
Mitigation: Configure the vault path and Obsidian binary carefully, keep Obsidian sync or backups enabled, and use explicit commands such as /summary daily or /summary weekly before writes. <br>
Risk: A generated recap could replace the wrong generated summary block if note structure or local configuration is unexpected. <br>
Mitigation: Use the skill's generated-section markers, review summaries before relying on them, and preserve non-target note content outside the marked block. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amortalsodyssey/conversation-recap-to-obsidian) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/amortalsodyssey) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown note sections with optional shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can append session entries, refresh generated daily summary blocks, and create weekly reports grouped by work item.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
