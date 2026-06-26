# Examples

## Example 1: Sensitive planning note
A local agent has confidential customer input that affects priority.

Safe approach:
- Keep customer details `private`.
- Add a `sealed-ref` noting that confidential priority input exists.
- Create a `task` for a sanitized prioritization proposal.

## Example 2: Claimable low-risk documentation update
A repo policy allows claimable documentation work.

Safe approach:
- Verify the task is `open` and low risk.
- Submit a `claim`.
- Move the task to `in_progress` if policy permits.
- Commit the documentation update and close with status.

## Example 3: Conflicting agent ownership
Two agents want the same implementation task.

Safe approach:
- Record both claim attempts.
- Do not overwrite ownership silently.
- Create or update a `risk` item.
- Wait for human adjudication if policy does not resolve the conflict.
