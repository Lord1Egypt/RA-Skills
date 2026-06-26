# Reviewing Template

Use this reference when the user wants a review-oriented Team built on top of ClawMem.

## Best fit

Use this template for:
- code review
- PR review
- design review
- architecture review
- policy or document inspection

## Design choices

Choose one of two tracking models:
- one-off review
  - best for occasional requests
  - lighter setup
- queue-backed review
  - best for repeated review intake
  - better when multiple reviewers rotate

Reviewers may all share one OpenClaw host or run on different hosts. On a shared host, the requester can dispatch directly to a reviewer; across hosts, reviewers pick up review requests by polling the shared repo (`issue_list state:open` plus the review task-kind label). Record which mode applies in the Team contract so verification targets the right evidence. The role names `requester` / `reviewer` are template-level — if the user prefers different names, treat the user's names as authoritative.

## Recommended blueprint shape

Define:
- review requester
- lead reviewer or coordinating agent
- reviewer set
- review artifact location
- completion rule, tied to a terminal status label on the review issue and to `state: closed`
- Workflow Label Schema covering request kind, review status values (including exactly one terminal), and reviewer assignment

ClawMem stays label-agnostic, so the label set here belongs to this Team, not to the plugin.

## Bootstrap path

1. Confirm whether review work is one-off or recurring.
2. Create or reuse the repo that will store review requests.
3. Create or reuse the actors and access model.
4. Write the canonical review contract, including its Workflow Label Schema, as a stable ClawMem memory node labeled with a pair such as `kind:convention topic:team-contract`. The agent decides whether the contract lives in a dedicated review repo or alongside the review requests in the same repo, based on the user's setup; record the choice in the blueprint.
5. Define the review-request body template. Every review request this Team creates opens its body with an explicit citation such as:
   > Review contract: `memory_get #<contract-id>` (kind:convention topic:team-contract) before acting.
   and inlines the schema's most critical rules (allowed status labels, reviewer assignee format, and the rule that the terminal status must be set together with `state:closed` via the same `issue_update`). No per-host install is required — the bundled `clawmem` skill's turn loop triggers the fetch when the id is cited in the body.
6. Seed one review request if the user wants a live demo, using that body template.

## Minimal demo

One minimal demo should show:
1. create one review request whose body references the canonical review contract
2. the assigned reviewer fetches the canonical review contract via an explicit tool call before acting
3. that reviewer records findings
4. that reviewer sets the terminal status label and closes the review issue in the same `issue_update` call
5. the canonical polling filter (`issue_list state:open` plus the review task-kind label) no longer returns the completed review
6. the result is visible from the chosen artifact
