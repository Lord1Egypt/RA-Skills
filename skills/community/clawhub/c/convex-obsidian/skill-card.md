## Description:

Convex Obsidian provides persistent OpenClaw memory by saving conversation turns to Convex and searching Convex plus Obsidian or Markdown notes for relevant context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreytsushima](https://clawhub.ai/user/andreytsushima)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to retain conversational memory, retrieve recent Convex records, and search local Obsidian or Markdown knowledge before generating a response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send conversation content to a fixed remote Convex service.

Mitigation: Use only a Convex deployment you control, rotate or remove exposed deploy keys, and disable automatic upload by default until the deployment is reviewed.

Risk: Persistent memory may store private conversation data without adequate scoping.

Mitigation: Add authentication, tenant checks, redaction, deletion controls, and clear retention rules before using it with sensitive or customer data.

Risk: The skill searches and writes local Obsidian or Markdown files.

Mitigation: Restrict vault folders and file permissions so the skill can access only intended memory locations.

Risk: Dependencies and backend behavior may change over time.

Mitigation: Pin dependencies and review the Convex backend before installing or redeploying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andreytsushima/skills/convex-obsidian)
- [Publisher profile](https://clawhub.ai/user/andreytsushima)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with optional JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include retrieved memory snippets, saved-memory identifiers, setup commands, and configuration examples.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
