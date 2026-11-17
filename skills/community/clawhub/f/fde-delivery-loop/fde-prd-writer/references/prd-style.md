# PRD Writing Standards

Use this specification to write ideas into requirements that can be reviewed, implemented, and accepted. The template defines the structure; this document defines the presentation quality.

## 1. Information credibility

| Tags | Usage scenarios |
|---|---|
| Unmarked | Facts/decisions provided by the user, substantiated by attachments, or confirmed |
| `[Hypothesis]` | An unverified judgment made to advance the draft |
| `[To be confirmed]` | Information that is missing and would affect scope, interaction, cost, or acceptance |
| `[Dependencies]` | Prerequisites determined by external teams, systems, policies or schedules |

Don’t fake user research, competitive product conclusions, performance goals, interface fields, compliance requirements, or launch dates. When there is no reliable baseline, write "Baseline to be confirmed" and suggest how to obtain it.

## 2. Goals and Scope

- Write the problem description as "who is in what situation, for what reason, and at what cost". Do not write the page or button first.
- Write down the measurement method, target value (or to be confirmed), and observation period for each goal; do not regard "complete development" and "deploy to production" as user/business goals.
- The scope of this issue answers "what capabilities are delivered"; the non-target answer is "what capabilities are deliberately not delivered". Both should be reviewable.
-P0/P1/P2is the delivery priority, not the range boundary. Changes in scope should update the change record.

## 3. Functional requirements

A functional requirement should enable the implementer to determine what the system should do given any input. Write in order of importance:

1. Role, trigger, precondition
2. Main process and observable results
3. Business rules, field verification and status changes
4. Permissions, notifications, idempotent/repeating operations (if applicable)
5. Empty status, failure, timeout, cancellation, revocation and recovery
6. Dependencies and uncertainties

Place complex rules under the corresponding `FR-`, and do not repeat them twice in the "Function Point List". Empty states with no input and denied paths without permission are often just as important as normal flow.

## 4. Acceptance criteria

Use Given / When / Then or equivalent condition-action-result structures. Each AC only verifies one observable result, which must be able to determine pass or failure.

```markdown
AC-003（FR-002）
Given: The approver does not have approval authority for this order
When: It opens the order and tries to submit it for approval
Then: the system rejects the submission, retains the original status of the order, and displays a no permission prompt.
```

Avoid:

- "The page is friendly, loads quickly, the system handles it correctly, and supports a variety of situations."
- Write the implementation method as acceptance result, such as "use Redis cache".
- Only normal paths are covered.

## 5. Data, interfaces and non-functional items

- Use a table to write the field type/format, source, required fields and verification, display/editing permissions; don’t just list the field name.
- Describe the direction of the integration, triggers, key contracts, timeout or failure behavior, retry/compensation ownership and ownership. Unknown contract title `[to be confirmed]`.
- Non-functional requirements must be verifiable: such as concurrency, response time, availability, audit retention, browser version or accessibility level. If it cannot be quantified, record the verification method and Owner first.

## 6. Figures and Format

- Use Mermaid when the process has branches, state transitions or asynchronous callbacks; do not draw simple linear steps.
- Write business status instead of UI pixel details in the diagram, and indicate failed or asynchronous paths.
- Tables are used for fields, permissions, status, interfaces, buried points and tracking; numbered lists are used for user operations.
- Markdown by default; other formats will only be generated if explicitly requested by the user or if there is an export process in place.
