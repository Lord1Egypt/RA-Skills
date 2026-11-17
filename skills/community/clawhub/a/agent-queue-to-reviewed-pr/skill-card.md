## Description:

Turn a ticket queue into reviewed draft PRs with an agent that never merges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to design an agent loop that turns prioritized tickets into grounded draft pull requests. It covers queue and acknowledgement contracts, duplicate prevention, local quality gates, optional browser QA, remediation handoffs, staleness checks, and retention controls while preserving human review and merge authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent and forge tokens, queue endpoints, and browser profiles can expose repository or session access if configured broadly.

Mitigation: Use dedicated least-privilege tokens, trusted HTTPS endpoints, secrets stored outside the workspace, and a dedicated test browser profile against preview or test data only.

Risk: Browser QA screenshots can contain authenticated session data.

Mitigation: Keep screenshots local, never attach them to PRs, and run the retention process so QA run directories are removed when PRs close and no later than seven days.

Risk: Weak queue acknowledgement or grounding gates can produce duplicate, off-scope, or falsely successful PR work.

Mitigation: Require conditional idempotent acknowledgements, process one ticket per run, mirror the grounding gate locally and server-side, and do not acknowledge work when checks fail.

Risk: Queues without conditional writes can leave work stuck in an in-progress state after crashes or races.

Mitigation: Confirm claims by read-back, write terminal failure states on every failed exit path, and reclaim orphaned claims by TTL.

## Reference(s):

- [The queue/ack HTTP contract](artifact/references/queue-contract.md)
- [Grounding - raw request to anchored brief](artifact/references/grounding-brief.md)
- [Browser QA of the preview, and remediation](artifact/references/browser-qa.md)
- [Brief staleness - drift as a first-class state](artifact/references/brief-staleness.md)
- [ClawHub skill page](https://clawhub.ai/alexbloch-ia/skills/agent-queue-to-reviewed-pr)
- [ClawHub publisher profile](https://clawhub.ai/@AlexBloch-IA)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, shell commands, Python helper scripts, and fixed status-report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for a single agent workflow; helper scripts validate grounding payloads and enforce local retention plans.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
