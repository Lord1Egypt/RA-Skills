## Description:

Detect new Bear notes tagged #share, extract core content into JSON Canvas knowledge nodes on agent_capabilities.canvas, then distribute a preview via BlueBubbles iMessage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to sync Bear notes tagged for sharing into a JSON Canvas knowledge graph and prepare compact BlueBubbles iMessage previews for a trusted work group.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move private Bear note content into a shared canvas and iMessage previews.

Mitigation: Use it only with trusted notes and recipients, and add explicit confirmation or redaction before sending previews.

Risk: The current scripts use unsafe command patterns for JSON and configuration data.

Mitigation: Pass JSON and configuration as data through files, stdin, or validated arguments instead of inline Python source.

Risk: External sharing controls are weak around the message target.

Mitigation: Validate BEAR_SHARE_TARGET against approved phone numbers, emails, or chat GUIDs before scheduled or automated use.

Risk: The processed-note filter needs correction before scheduled use.

Mitigation: Fix and test note ID filtering so already processed notes are not resent or skipped incorrectly.

## Reference(s):

- [Canvas Schema Reference](artifact/references/canvas-schema.md)
- [JSON Canvas 1.0 Specification](https://jsoncanvas.org/spec/1.0/)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration instructions]

**Output Format:** [Markdown instructions with bash commands, JSON note data, JSON Canvas file updates, and formatted preview text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates a canvas file, tracks processed note IDs in a state file, and truncates preview content before message delivery.]

## Skill Version(s):

4.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
