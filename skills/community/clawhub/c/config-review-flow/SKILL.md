---
name: config-review-flow
description: Review and finalize configuration topics through a structured item-by-item confirmation flow. Use when the user wants a documented configuration review flow, wants to逐条核对配置 or 逐项确认配置, or needs a process that inventories all in-scope settings first, records decisions in a workspace `configuring/` file, and requires a final explicit pre-apply confirmation before any real configuration change. Do not use for single-setting Q&A or direct config editing without a review pass.
---

# Config Review Flow

Use this skill when the user wants a configuration topic reviewed and finalized one item at a time.

## Workflow

1. Define the review scope first.
   - Name the exact configuration topic under review.
   - State what is in scope and what is out of scope.
   - If the user mixes multiple topics, split them before continuing.
   - If the target system, file, product, or environment is unclear, pause and clarify before collecting items.

2. Collect all configurable items from trusted sources before making recommendations.
   - Prefer a sub-agent for discovery when the topic is non-trivial, broad, or documentation-heavy.
   - Trusted sources mean current local config files and local docs first, then official docs if needed.
   - Include detected runtime or environment facts and authoritative source-code defaults when they are part of the real configuration surface.
   - Build a normalized inventory of configurable items, current or detected values if known, valid options, defaults if known, constraints, dependencies, restart or reload impact, and source links or file paths.
   - Mark unknowns explicitly instead of guessing.
   - Do not start recommending values before this inventory exists.

3. Normalize and de-duplicate the inventory.
   - Merge duplicate items that appear across multiple sources.
   - Separate true user-facing choices from internal implementation details.
   - Group related items when that improves review order, but keep each final decision atomic.
   - Call out prerequisites, mutually exclusive options, and settings that only matter when another item is enabled.

4. Present the full inventory to the user for review.
   - Keep it compact.
   - Show the whole decision surface before starting item-by-item confirmation.
   - For large topics, present a grouped overview instead of dumping every detail at once, but make it clear that the full in-scope inventory has been covered.
   - Highlight missing information, risky items, and irreversible or restart-sensitive settings.
   - Tell the user that if the list looks right, the next step is item-by-item confirmation.

5. After the user confirms the inventory, create a tracking file under `workspace/configuring/`.
   - Create the folder if it does not exist.
   - Name the file after the configuration topic in kebab-case, for example `browser.md` or `openclaw-browser.md`.
   - Record the normalized inventory before starting the walkthrough.
   - Record the review scope, target environment, and any unresolved unknowns at the top.

6. Walk through one item at a time.
   - Review items in dependency order, not arbitrary order.
   - For each item, explain:
     - what it controls
     - valid options
     - default if known
     - important tradeoffs
     - dependencies or downstream effects
     - whether it needs restart, reload, migration, or no runtime action
     - your recommended choice and why
   - Keep one message focused on one decision unless two items are inseparable.
   - Ask for confirmation on that single item.
   - If the user is unsure, offer the best 2-3 options and recommend one.
   - After the user confirms, write the confirmed value under that item in the tracking file before moving on.
   - Then ask about the next item.

7. Handle revisions and branching explicitly.
   - If the user changes an earlier decision, update the tracking file immediately.
   - Re-evaluate downstream items that depend on the changed choice.
   - If a new item is discovered mid-review, add it to the inventory first, then continue.
   - If documentation conflicts, surface the conflict plainly and resolve it before continuing.

8. Use an explicit review state machine.
   - Track the overall review state as one of: `inventory`, `in-review`, `awaiting-final-confirmation`, or `approved-to-apply`.
   - Stay in `inventory` until the item inventory is complete and user-approved for walkthrough.
   - Move to `in-review` when item-by-item confirmation starts.
   - As soon as every in-scope item is marked `confirmed` or explicitly `not-applicable`, automatically switch to `awaiting-final-confirmation`.
   - Do not wait for the user to ask for a summary.
   - If a new item, conflict, or dependency issue appears before apply approval, leave `awaiting-final-confirmation`, return to `in-review`, update the tracking file, and only re-enter final confirmation after the review is fully confirmed again.
   - Only switch to `approved-to-apply` after a fresh explicit apply confirmation from the user after the final summary.
   - `approved-to-apply` means apply permission has been granted. It does not mean the real configuration has already been changed.

9. Trigger the final pre-apply confirmation automatically and stop there.
   - Immediately summarize the completed plan from the tracking file when the review enters `awaiting-final-confirmation`.
   - Separate decisions, assumptions, unresolved risks, and runtime impact.
   - Then ask for one last explicit confirmation before any real config file is modified or any service is restarted, reloaded, migrated, or deployed.
   - Treat this final confirmation as mandatory, even if the user previously said things like `go ahead`, `use your judgment`, `apply defaults`, or gave broad approval earlier in the review.
   - Do not treat per-item confirmations as permission to apply the real configuration.
   - While in `awaiting-final-confirmation`, do not continue with new recommendations, new item walkthrough, real config edits, or execution.

## Operating rules

- Prefer local documentation over web search.
- Use official documentation only when local docs are missing, unclear, or outdated.
- Use a sub-agent for the discovery or inventory step when the topic is non-trivial.
- Keep the inventory separate from recommendations.
- Do not skip directly to editing the real target config file during review.
- The `configuring/` markdown file is the source of truth for the in-progress review.
- If the user changes an earlier decision, update the tracking file immediately.
- If a setting requires restart, reload, migration, deploy, or downtime, mention that clearly, but do not perform it until the final apply confirmation.
- Distinguish facts from recommendations. Facts come from sources. Recommendations are your judgment.
- Do not invent defaults, supported values, or compatibility claims when sources are missing.
- Keep each decision atomic. Avoid asking the user to approve a large bundle unless the settings are inseparable.
- When the user only wants review, stop at the final pre-apply confirmation boundary.
- Final confirmation mode must trigger automatically when the review reaches a fully confirmed state.
- `awaiting-final-confirmation` is a hard stop. Do not modify the real target config, restart services, reload processes, run migrations, or deploy changes until the user gives a fresh explicit apply confirmation after the final summary.
- Broad earlier consent does not waive the final confirmation step.
- If a newly discovered item, conflict, or dependency issue appears while in `awaiting-final-confirmation`, move back to `in-review` before continuing.

## Suggested tracking file format

Use this structure unless the topic needs a better one:

Mechanical constraints:
- Every in-scope item must appear in both `Source inventory` and `Decisions`.
- Keep item names aligned across `Source inventory` and `Decisions`.
- If any in-scope item is still `pending`, the overall review status must not move to `awaiting-final-confirmation`.


```markdown
# <Topic>

- scope: ...
- target: ...
- status: inventory | in-review | awaiting-final-confirmation | approved-to-apply

## Unknowns
- ...

## Source inventory
### <item-name>
- current/detected value: ...
- options: ...
- default: ...
- dependencies: ...
- risk level: low | medium | high | unknown
- irreversible: yes | no | unknown
- requires-user-input: yes | no
- runtime impact: restart | reload | migration | deploy | none | unknown
- notes: ...
- sources: ...

## Decisions
### <item-name>
- status: pending | confirmed | not-applicable
- chosen: ...
- rationale: ...
- confirmed-at: ...
- last-updated-at: ...
- revision-notes: ...
- downstream-checks: ...

```

## Quality bar

A review is not complete until all of these are true:
- the exact review scope is defined
- every configurable item in scope has been inventoried
- duplicates and dependency relationships have been normalized
- every item has been explained to the user
- every confirmed item has been written to the tracking file
- revisions and dependency impacts have been reflected in the tracking file
- the review state has been advanced correctly through `inventory`, `in-review`, and `awaiting-final-confirmation`
- the final assembled plan has been summarized from the tracking file immediately after the review reaches a fully confirmed state
- runtime impact has been summarized clearly
- final confirmation mode has been triggered automatically
- no real apply action has started before a fresh explicit apply confirmation after the final summary
- only after the final summary and a fresh explicit apply confirmation may the review state move to `approved-to-apply`
- the user has been asked for a last pre-apply confirmation
