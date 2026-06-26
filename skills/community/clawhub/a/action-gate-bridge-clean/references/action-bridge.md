# Action Bridge

Goal: convert risky next steps into typed action proposals instead of direct execution.

Typical action types:
- send_email
- send_message
- confirm_booking
- change_setting
- external_write_api
- public_post
- spend_money
- prepare_draft
- recommend_action
- update_ledger

Suggested flow:
1. detect need for action
2. classify it
3. create a typed proposal or route the write intent
4. let the sidecar return `allowed`, `needs_approval`, `blocked`, or `accepted`
5. only then decide what to show the user
6. if approved and an execution adapter exists, execute behind the sidecar

Runtime expectations:
- the action gate is a separate component
- endpoint URLs should be configured through environment variables
- the bridge should stay truthful about what is proposed, approved, blocked, or executed
