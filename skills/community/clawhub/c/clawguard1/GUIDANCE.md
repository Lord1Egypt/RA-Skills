# ClawGuard Governance Protocol

**Mandatory rule:** Before executing any SQL statement, file-system mutation, or API request that can write, delete, or update data, you MUST call `evaluate_action(action_type, justification, risk_level)`.

1. Describe the intent (e.g., "Update user 42 email", "Rotate API key", "Delete tmp directory").
2. Assign a `risk_level` from 1 (minimal) to 5 (catastrophic). When uncertain, round **up**.
3. Call `evaluate_action` and wait for the response.
   - If `allowed: true`, proceed with the operation.
   - If `allowed: false`, STOP. Surface the `message` to the user and do not attempt the action.
4. After completing the operation, include the approval reference in any follow-up notes or summaries.

This protocol applies globally and without exception. Every write-capable action must have a logged evaluation before execution.
