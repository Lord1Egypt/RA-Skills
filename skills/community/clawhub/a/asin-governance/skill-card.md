## Description:

Cybernetic governance substrate for the ASIN Federated Adaptive Cognition Stack, providing constraint checks, safety-oracle rules, drift detection, sandbox replay, audit logging, and ASH-0.2 session-handshake tooling for agent ecosystems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dbottrader](https://clawhub.ai/user/dbottrader)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to gate autonomous agent actions through constraint profiles, safety rules, replay checks, and auditable session exchange controls before actions are allowed to proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says governance and safety promises are undercut by fail-open checks.

Mitigation: Review and tighten fail-open paths before relying on the oracle, entropy budget, or replay gates; keep human approval in the loop for non-read-only actions.

Risk: The security guidance warns that the heartbeat can use a Moltbook API key.

Mitigation: Use a least-privilege test credential, avoid production credentials during evaluation, and verify credential storage and outbound calls before scheduled execution.

Risk: The security summary identifies broad activation and a standalone session server.

Mitigation: Run the server only on an intended bind address, restrict network exposure, and validate scopes, node profiles, rate limits, and logs before deployment.

Risk: The packaged fuzz report shows all tested post-payload mutations passed safety checks.

Mitigation: Treat the safety oracle as experimental and add blocking checks for oversized content, empty titles, injection strings, credentials in content, null bytes, and high-volume Unicode before using it for autonomous posting.

Risk: The artifact writes persistent local audit logs, token secrets, and revocation data when executable components are run.

Mitigation: Run in a dedicated workspace with expected file permissions and retention controls, and inspect generated logs and secrets after testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dbottrader/skills/asin-governance)
- [SKILL.md](artifact/SKILL.md)
- [Safety rules](artifact/oracle/safety.json)
- [Risk taxonomy](artifact/constraints/taxonomy.json)
- [Fuzz report](artifact/sandbox/fuzz-report.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, shell output, and Python command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local audit logs, token secrets, revocation data, and fuzz reports when the executable artifact components are run.]

## Skill Version(s):

1.0.1 (source: server release evidence; packaged skill metadata says 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
