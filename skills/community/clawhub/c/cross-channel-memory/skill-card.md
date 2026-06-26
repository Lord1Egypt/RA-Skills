## Description: <br>
Maps QQ, Feishu, and other channel user identities to a unified user profile so agents can read and write shared memory for the same person across channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wljmmx](https://clawhub.ai/user/wljmmx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect a user's identities across QQ, Feishu, and other channels, then retrieve and store shared memory for that unified user across agent workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill links identities and persists conversation memory across channels and agents. <br>
Mitigation: Require explicit user or administrator approval before creating identity links, and provide ways for users to inspect, delete, or opt out of stored memories. <br>
Risk: Automatic mapping creation can attach a channel user to a unified identity without enough verification. <br>
Mitigation: Disable or tightly constrain auto-create behavior and verify channel, account, and session identifiers before writing mapping data. <br>
Risk: Hardcoded OpenClaw paths and unvalidated account identifiers can route memory to the wrong workspace. <br>
Mitigation: Replace hardcoded home-directory paths with configured storage paths and validate agent, account, channel, and session IDs before path construction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wljmmx/cross-channel-memory) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Sample mapping configuration](artifact/examples/sample_mapping.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and JSON mapping configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill writes JSON identity mappings and Markdown memory records; use only with explicit approval, constrained auto-create behavior, validated IDs, configured storage paths, and user controls to inspect, delete, or opt out of stored memories.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter says 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
