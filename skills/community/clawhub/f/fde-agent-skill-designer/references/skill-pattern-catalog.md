# Agent skill mode directory

## Routing mode

Classify tasks first, then select dedicated processes. Suitable for type boundaries to be stable; routing errors should be detectable and fallbackable.

## Prompt chain mode

Divide fixed tasks into extraction, judgment, generation, and inspection. Suitable for gates that require intermediate quality; do not add meaningless calls.

## Parallel analysis mode

Independent dimensions are processed in parallel and then merged. Suitable for documents or metrics that are independent of each other; merging must handle conflicts.

## Evaluation—Optimization Mode

After generation, it is checked and iterated by explicit scales. Limit the maximum number of rounds, cost and rewrite scope to prevent infinite loops.

## Retrieve—generate schema

Regenerate evidence from authorized knowledge. No results, expiration, conflicts, permissions, and source consistency must be handled.

## Tool execution mode

Plan, verify parameters, confirm necessary, execute, verify final status. Write operations add idempotence and compensation.

## Manual confirmation mode

Demonstrate actions, goals, rationale, risks and irreversible effects. Confirmation must come from an authorized user and cannot use a vague "do you want to continue".

## Manual takeover mode

When information is missing, low confidence, high risk, policy conflict, or tool failure, output the reason for takeover, what was completed, and required next steps.

## Read-only suggestion mode

The agent only queries and makes suggestions, which are executed by humans. Suitable for early POC, high risk and insufficient platform control scenarios.

## Draft mode

Generate unvalidated objects, such as email drafts and ticket drafts. Downstream interfaces must clearly differentiate between draft and sent status.

## Evidence mode

Each conclusion is accompanied by input, documentation, query or tool evidence. No forced selection when sources conflict.

## State machine mode

When the business state is limited and the rules are clear, use explicit states and allow transitions to prevent the model from freely determining all state changes.

## Budget mode

Limit model calls, tool times, time, tokens, amounts and processing objects. Summarize and request a decision when the cap is reached.

## Multi-agent mode

Only if responsibilities, context, or permissions truly require separation. Define coordinators, handover contracts, shared state, conflicts, and termination.

## Memory mode

Differentiate between session context, user preferences, business facts, and long-term records. Source, permissions, expiration and deletion rules are required before writing to long-term memory.

## Batch mode

Define single failure, partial success, retries, sequence, rate, and aggregation. Don’t lose an entire batch of evidence because of one failure.

## Example pattern

Examples are used to demonstrate boundaries and formatting and should not contain full assessment answers or sensitive customer information.

## Rule priority

Platform/Security Constraints > Customer Policies > Task Rules > User Current Preferences > Style Preferences. In case of conflict, explain higher rules and escalation methods.

## Output mode

Structured output is suitable for downstream machines; Markdown is suitable for human review; when both are needed, the single source of truth is clear.

## Select check

- Is there a simpler deterministic method;
- The added latency and cost of the model;
- Can the failure be detected;
- Whether manual judgment is required;
- Whether a representative assessment can be constructed;
- Whether the platform can achieve the required permissions and status.

## Combination example

Customer Service Draft: Routing → Retrieve Evidence → Status Check → Generate Draft → Consistency Assessment → Manual Confirmation.

Contract review: document extraction → parallel clause inspection → conflict merging → risk classification → manual takeover.

Data modification: read-only analysis → plan → parameter verification → authorized user confirmation → idempotent execution → status verification.
