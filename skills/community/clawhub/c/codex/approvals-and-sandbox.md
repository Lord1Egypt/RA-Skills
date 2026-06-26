# Approvals and Sandbox

## Sandbox Levels

Use the least privilege that still lets the task succeed:

| Mode | Good for | Main risk |
|------|----------|-----------|
| `read-only` | inspection, planning, repo onboarding, review | no edits or write-side verification |
| `workspace-write` | normal local coding inside the approved repo | real file changes and wider-than-expected diffs |
| `danger-full-access` | externally sandboxed or explicitly high-trust environments only | unbounded local side effects |

## Approval Policy Defaults

Choose approval posture deliberately:

| Policy | Use when | Watch out for |
|--------|----------|---------------|
| `untrusted` | conservative environments where only trusted commands should pass silently | slower flow, but safer when trust is unclear |
| `on-request` | normal interactive work where the agent can escalate at clear boundaries | requires the user to stay engaged |
| `never` | controlled non-interactive environments where failures should return directly | easy to overuse if the environment is not actually safe |
| `on-failure` | legacy behavior only | deprecated; avoid as the default mental model |

## High-Risk Flags

These are not routine convenience flags:

```bash
codex exec --dangerously-bypass-approvals-and-sandbox ...
codex exec -s danger-full-access -a never ...
```

Only use them when:
- the environment is externally sandboxed
- the blast radius is accepted explicitly
- the rollback story is already understood

## Practical Rule

If you would be uncomfortable reading the exact commands and edits after the fact, the run is over-privileged.
