## Description:

Context Booster helps agents manage long-running conversations by compressing context, extracting key points, retrieving stored memories, and enriching future turns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pagoda111king](https://clawhub.ai/user/pagoda111king)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Context Booster to preserve continuity in long or multi-step work by summarizing active context, retrieving relevant prior memory, and injecting concise background when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad conversation context may be captured and persisted locally across sessions.

Mitigation: Avoid secrets or regulated data unless appropriate protections are configured, review local retention settings before installation, and clear stored context when it is no longer needed.

Risk: The release evidence reports an inconsistent manual install source and unavailable server-resolved GitHub provenance.

Mitigation: Verify the canonical repository and publisher profile before following manual installation instructions.

Risk: Compression and retrieval can omit, distort, or mis-rank important context.

Mitigation: Review compressed summaries and retrieved memories before relying on them for consequential work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pagoda111king/skills/context-booster)
- [README](artifact/README.md)
- [FAQ](artifact/FAQ.md)
- [Version history](artifact/VERSION_HISTORY.md)
- [Declared package repository](https://github.com/cloud-shrimp/meta-skill-system)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return compressed context, memory summaries, retrieval results, status data, or suggested next context.]

## Skill Version(s):

0.1.4 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
