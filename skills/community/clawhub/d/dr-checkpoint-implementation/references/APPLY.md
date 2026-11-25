# Apply dr-checkpoint-implementation

Add this policy block to the workspace or agent instructions that should enforce checkpointed implementation.

```markdown
## Checkpointed Implementation

Use `dr-checkpoint-implementation` for consequential multi-stage work as defined by its trigger gate, not routine read-only checks or reversible local work.

Break work into independently reviewable checkpoints. For each checkpoint, define acceptance criteria before coding, implement only that checkpoint, run focused validation, review the evidence, revise the remaining plan if needed, and record whether the next checkpoint is self-approved or needs user approval.

Default to self-approval when acceptance criteria are met, validation passes, no materially increased risk or unauthorised external side effect is introduced, and the remaining plan still matches the user's objective. Preserve approval for its agreed scope across checkpoints and turns; do not request it again for already-authorised actions.

Stop for approval before unauthorised live effects or materially changed scope or risk. Investigate and fix failed validation within scope; pause if it remains unresolved or a genuine blocker arises. Read-only or no-save diagnostics do not require approval solely because they access production; assess their actual effects, including disruptive load and triggered side effects.
```

After applying the block, verify future complex implementation tasks explicitly include checkpoint reviews with:

- Implemented
- Evidence
- Learned
- Remaining work
- Plan changes
- Approval decision
- Reason
