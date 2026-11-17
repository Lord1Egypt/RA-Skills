## Description:

Guides an agent in operating a local GBrain knowledge base through WorkBuddy MCP, including ingestion, classification prefixes, linking, schema-pack selection, health governance, large-library batching, and Obsidian handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noaheleven](https://clawhub.ai/user/noaheleven)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage a GBrain-backed local knowledge base through MCP tools, including importing documents, assigning page types, adding links and tags, and monitoring knowledge-base health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes guidance for hidden Windows Startup launchers, watchdog loops, and alternate execution paths after WorkBuddy blocks a command.

Mitigation: Require explicit operator approval before creating startup persistence, watchdog scripts, or bypass-style service launch paths, and document how to disable any approved startup behavior.

Risk: Large private datasets may be moved, ingested, embedded, or sent to cloud embedding and LLM APIs during GBrain setup.

Mitigation: Confirm allowed source directories, data categories, and cloud-processing permissions before ingestion, and process large libraries in reviewed batches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noaheleven/skills/gbrain-guide)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with MCP tool names, command examples, and operational checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend local file movement, MCP calls, service startup commands, and batching procedures for large knowledge bases.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
