## Description:

Repairs damaged Codex Desktop sessions that fail after provider switches, imports, stale remote-compaction reasoning IDs, unsupported saved models, or Gemini model-turn compaction errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wardlu](https://clawhub.ai/user/wardlu)

### License/Terms of Use:

MIT

## Use Case:

Developers and support operators use this skill to diagnose a single broken saved Codex Desktop conversation, run a dry-run report, and apply the smallest backup-first repair that can make the session resumable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A repair could be run against the wrong Codex session or stale diagnosis.

Mitigation: Use an exact session UUID, confirm the dry-run report shows the expected embedded session metadata, and apply only after Codex is fully closed.

Risk: Installation through an unpinned command may expose users to supply-chain changes.

Mitigation: Prefer a pinned or locally verified install and review the skill before installing.

Risk: Session repair modifies local rollout and database state.

Mitigation: Keep the generated backups and verify the post-repair report before reopening the repaired session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wardlu/skills/codex-cross-provider-session-repair)
- [Publisher repository metadata link](https://github.com/WardLu/skills/tree/main/codex-cross-provider-session-repair)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON status or report snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Backup-first, target-scoped workflow that may produce bilingual wait, apply, and verification status.]

## Skill Version(s):

0.7.6 (source: release metadata; artifact frontmatter lists 0.7.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
