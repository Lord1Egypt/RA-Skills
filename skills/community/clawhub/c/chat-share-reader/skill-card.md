## Description:

Exports AI chat conversations from public share links and local agent session stores to Markdown, with search, batch export, and optional redaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapleleo-hub](https://clawhub.ai/user/mapleleo-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent users can archive public conversation links or search and export their own local agent sessions as readable Markdown or structured JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with medium confidence, citing bearer-token handling and sensitive-data masking concerns; portions of the code were only partially inspected.

Mitigation: Before installation, review the data the skill may save or display, confirm token masking behavior, and complete review of the code. Use a reviewed, pinned version of any referenced CLI.

Risk: The documented `--redact off` mode exports conversation content without redaction, which can include sensitive values.

Mitigation: Keep the default redaction or use strict redaction when appropriate, and inspect exported files before sharing them.

## Reference(s):

- [Project homepage listed in skill metadata](https://github.com/mapleleo-hub/chat-share-reader)
- [ClawHub release page](https://clawhub.ai/mapleleo-hub/skills/chat-share-reader)
- [Supported sites reference](references/sites.md)
- [Local session formats reference](references/sessions.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Text]

**Output Format:** [Markdown conversation archives, with optional structured JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conversation messages can be exported with configurable redaction; local session exports can include full messages and metadata.]

## Skill Version(s):

0.5.3 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
