## Description:

Enhanced Permissions provides OpenClaw agents with four-level permission checks, confirmation prompts, audit logging, memory version control, auto-organization, smart suggestions, and knowledge graph helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abcd784253626](https://clawhub.ai/user/abcd784253626)

### License/Terms of Use:

MIT-0

## Use Case:

Developers integrating OpenClaw use this skill to check operation permissions, require confirmation for higher-risk actions, and manage agent memories with version history, organization, recall, suggestions, and entity relationships.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill auto-loads code and can alter memory state through storage, update, rollback, and auto-organization tools.

Mitigation: Review configuration before installation, keep auto-organization in dry-run mode until trusted, and require explicit approval for workflows that modify or roll back memories.

Risk: Trusted sessions may auto-approve moderate write operations.

Mitigation: Limit trusted session names to controlled contexts and periodically review permission settings for least privilege.

Risk: Audit logs may persist unredacted operation parameters.

Mitigation: Avoid sending secrets or sensitive personal data in operation parameters, and rotate or protect the audit log location.

Risk: OpenViking integration can process memory text through an external embedding service when configured.

Mitigation: Enable the integration only after reviewing data handling requirements and avoid embedding confidential memory content unless approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abcd784253626/skills/enhanced-permissions)
- [README](artifact/README.md)
- [CHANGELOG](artifact/CHANGELOG.md)
- [Installation guide](artifact/INSTALL-GUIDE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON-like tool results, confirmation text, Markdown audit logs, and TypeScript or JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update memory state, create version history, write audit logs, and use an external embedding service when OpenViking is configured.]

## Skill Version(s):

1.0.6 (source: server release evidence, package.json, CHANGELOG; released 2026-04-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
