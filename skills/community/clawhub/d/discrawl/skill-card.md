## Description:

Discrawl helps agents search local Discord archives, check archive freshness, inspect DMs and channel slices, run SQL counts, and support Discrawl repository work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclaw](https://clawhub.ai/user/openclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Discrawl to answer questions from local Discord archive data before using live Discord APIs, including freshness checks, bounded searches, DM or channel inspection, and read-only SQL counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect private DMs and local Discord artifacts.

Mitigation: Use it only for datasets and workspaces the user is authorized to inspect, and avoid sharing git snapshots that contain secrets or @me DM rows.

Risk: The install metadata uses a mutable Go module target.

Mitigation: Prefer a pinned Discrawl version before deployment.

Risk: Bot-backed sync can require Discord bot credentials.

Mitigation: Configure only authorized bot credentials and do not extract user tokens, call Discord as the user, or write to Discord storage.

Risk: Database mutation is possible when unsafe flags are explicitly used.

Mitigation: Use read-only SQL for counts and rankings, and require explicit user request and review before any --unsafe --confirm mutation.

## Reference(s):

- [Discrawl homepage](https://github.com/openclaw/discrawl)
- [ClawHub Discrawl skill page](https://clawhub.ai/openclaw/skills/discrawl)
- [OpenClaw publisher profile](https://clawhub.ai/user/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and concise archive findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports absolute date spans, channel or DM names, counts, and known gaps when archive evidence supports them.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
