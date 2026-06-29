# Apply dr-checkpoint-implementation

Add this policy block to the workspace or agent instructions that should enforce checkpointed implementation.

```markdown
## Checkpointed Implementation

For complex implementation, production-risk work, cron/alerting/data/integration/monitoring/reporting changes, operational tooling, or tasks where requirements may evolve after inspecting real code, APIs, tests, or data, always use `dr-checkpoint-implementation`.

Break work into independently reviewable checkpoints. For each checkpoint, define acceptance criteria before coding, implement only that checkpoint, run focused validation, review the evidence, revise the remaining plan if needed, and record whether the next checkpoint is self-approved or needs user approval.

Default to self-approval when acceptance criteria are met, validation passes, no new production risk or external side effect is introduced, and the remaining plan still matches the user's objective.

Stop for user approval before live external side effects, production mutations, material scope or architecture changes, weak or contradictory validation, uncertain real-data calibration, or work touching secrets, permissions, billing, customer data, or production infrastructure.
```

After applying the block, verify future complex implementation tasks explicitly include checkpoint reviews with:

- Implemented
- Evidence
- Learned
- Remaining work
- Plan changes
- Approval decision
- Reason
