## Description:

Manage a local key-value cache store using bash and Python, with TTL support for API responses, session data, and computed results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to store, retrieve, search, export, import, and expire local cache entries during workflows that benefit from reusable temporary data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cache may store tokens, session data, private API responses, or personal information in plaintext local files.

Mitigation: Cache only data that is acceptable to store in plaintext, avoid secrets and personal information, and review local file permissions before use.

Risk: Exported cache backups may expose cached data if placed in shared folders or source control.

Mitigation: Keep exports in private locations and exclude cache backups from repositories and shared workspaces.

Risk: The flush command can delete cache entries without confirmation.

Mitigation: Export or inspect important cache entries before running flush, especially when using broad patterns or no pattern.

## Reference(s):

- [Cache ClawHub listing](https://clawhub.ai/xueyetianya/skills/cache)
- [Publisher profile](https://clawhub.ai/user/xueyetianya)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, text, JSON]

**Output Format:** [Markdown guidance with inline bash commands; command results are raw text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores cache data locally in plaintext files under ~/.cache-tool.]

## Skill Version(s):

2.0.0 (source: server release evidence; artifact files identify tool version 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
