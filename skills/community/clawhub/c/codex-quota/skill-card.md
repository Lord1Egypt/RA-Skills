## Description:

Check OpenAI Codex CLI rate limit status for daily and weekly quotas using local session logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect Codex CLI quota status before heavy Codex work, troubleshoot possible rate limits, or monitor quota across saved accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The --all --yes mode temporarily replaces the live Codex authentication file and may leave the wrong account active if interrupted.

Mitigation: Prefer cached mode or --fresh for one active account; if --all --yes is needed, close other Codex activity first and verify the active account afterward.

Risk: The all-accounts output stores account quota metadata in /tmp/codex-quota-all.json.

Mitigation: Treat the /tmp output as local account metadata and remove it when it is no longer needed.

## Reference(s):

- [Codex Quota ClawHub Skill Page](https://clawhub.ai/odrobnik/skills/codex-quota)
- [Codex CLI](https://codex.openai.com)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text status output or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local Codex session logs; --fresh and --all require the codex CLI.]

## Skill Version(s):

1.2.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
