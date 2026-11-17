## Description:

ClawLock-Rank helps agents run a local ClawLock 2.2.1+ scan, preview the sanitized leaderboard payload, and upload a confirmed score to ClawLockRank.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g1at](https://clawhub.ai/user/g1at)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill after a local ClawLock inspection to preview what score metadata will be published and, after explicit confirmation, submit it to the ClawLockRank leaderboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Leaderboard submission sends a raw device fingerprint, score, nickname, version data, timestamp, evidence hash, and finding titles to the leaderboard service.

Mitigation: Run the preview first, review the upload fields, and upload only after explicit user confirmation.

Risk: Preview mode can leave sanitized ClawLockRank payload files in the temp directory.

Mitigation: Remove leftover clawlock-rank-preview JSON files after previewing, especially on shared systems.

Risk: The upload destination can be changed by command-line argument, environment variable, or skill configuration.

Mitigation: Confirm the resolved API base is the intended HTTPS Worker before submitting a score.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g1at/skills/clawlock-rank)
- [Publisher profile](https://clawhub.ai/user/g1at)
- [Skill homepage](https://github.com/g1at/ClawLock-Rank)
- [Leaderboard Worker endpoint](https://clawlock-rank-worker.dyyxml.workers.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON preview summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can produce a local preview JSON file and can submit a sanitized score payload after explicit confirmation.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
