## Description:

Personal knowledge base for capturing and retrieving information about people, places, restaurants, games, tech, events, media, ideas, and organizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderaven](https://clawhub.ai/user/coderaven)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to maintain a persistent personal knowledge base for named entities, preferences, interactions, and related attachments. It guides agents to search existing memory, create or update Markdown entries, and preserve original media when users provide supporting files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist personal details and original media files in a local knowledge base.

Mitigation: Install only when a persistent local brain is intended, use explicit save and delete instructions, avoid storing sensitive third-party information without consent, and periodically clean the brain and attachments folders.

Risk: The optional QMD backend setup includes an unpinned global install step.

Mitigation: Skip the optional QMD install unless the dependency can be pinned, verified, and installed in an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coderaven/skills/2nd-brain)
- [QMD optional backend](https://github.com/tobi/qmd)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files, concise text guidance, and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent brain entries and attachment indexes under the configured OpenClaw workspace.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
