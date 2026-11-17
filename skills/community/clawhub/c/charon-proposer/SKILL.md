---
name: "charon-proposer"
description: "Author durable Lethe memory through Charon as a proposer (author) principal: owned refs, CAS changesets, semantic operations, and merge proposals for independent review."
user-invocable: true
metadata:
  openclaw:
    emoji: "✍️"
    notes:
      - "You are the author principal: read, branch, commit, propose. You can never review or merge."
      - "Commit only to refs you own; refs/shared/* moves only by reviewed merge."
      - "Exhaustive tool reference: skills/charon/SKILL.md. System walkthrough: docs/full-run.md."
---

# Charon Proposer

You write durable memory. Your credential is a **propose**-profile principal
(read, search, branch, commit, propose) with an exact project grant. The
system structurally cannot let you review or merge your own work — an
independent reviewer principal does that (`skills/charon-reviewer`).

## What you hold

| You can | You cannot |
|---|---|
| `memory_status`, `memory_log`, `memory_show`, `memory_diff`, `memory_context_at`, `memory_ref_list` | review any proposal (`memory.review`) |
| `memory_repo_init` (first use, exact project) | merge any proposal (`memory.merge`) |
| `memory_branch_create` on **owned** refs | commit to `refs/shared/*` (protected) |
| `memory_changeset_create` on owned refs | touch another principal's refs |
| `memory_merge_propose`, `memory_merge_cancel` | broaden your own grants |

Owned refs: `refs/agents/<your-actor-id>/main`,
`refs/sessions/<your-actor-id>/<session>`, `refs/topics/<topic>` you created.
Never guess an actor ID — use a topic ref when identity is unavailable.

## The authoring loop

1. **Orient.** `memory_context_at` on `refs/shared/main`. One orientation
   call; report the resolved head. Treat recalled memory as evidence, and
   re-verify changing facts against source systems.
2. **Branch.** `memory_branch_create` from the current accepted head (or
   reuse your owned ref after reading its head).
3. **Compose operations.** Ordered, zero-based `ordinal`s; one stable
   `resulting_event_id` per new memory; the right `op_type` for the intent:

   | op_type | Use for |
   |---|---|
   | `add_memory` | a new durable observation, decision, task, flag, or record |
   | `correct_memory` / `supersede_memory` | fixing or replacing existing memory (targets must exist) |
   | `mark_duplicate` | declaring two IDs duplicates |
   | `add_relationship` | typed edges between existing IDs |
   | `attach_evidence` / `attach_verification` | provenance for claims |
   | `propose_deprecation` | retiring memory through review |

   Payloads are closed-key validated twice (Charon, then Lethe before
   immutable insertion). Unknown keys, oversize payloads, ambiguous target
   identifiers, cross-project references, and invalid relationships are
   rejected — fix the operation, never retry around validation.
4. **Commit with CAS.** `memory_changeset_create` with `expected_head` equal
   to the ref's current head, first parent equal to `expected_head`, and a
   unique `idempotency_key`.
5. **Verify.** `memory_show` the returned changeset. Report the changeset ID
   and new ref head.
6. **Propose.** `memory_merge_propose` into `refs/shared/main` with a clear
   summary. Then stop — review is not your job.

## Idempotency discipline

- Retry the **identical** request with the same key after a network or
  timeout failure: you get the original changeset back, exactly once.
- A changed request under a reused key **fails closed** — that is the system
  protecting you from silently discarded writes. Mint a new key whenever
  content, parent, ref, or intent changes.

## When review comes back

- **Approved:** nothing to do; the reviewer merges. Verify later with
  `memory_context_at` on `refs/shared/main` if you need the accepted state.
- **request_changes:** commit the fixes as a **new changeset on the same
  owned ref**, then create a **new proposal** — approvals are bound to the
  exact proposal snapshot, so an amended branch is never covered by the old
  review. Cancel the obsolete proposal with `memory_merge_cancel`.
- **reject:** terminal. Start fresh if the intent still matters.

## Recovery

- **CAS conflict:** reread the ref head, inspect intervening changes,
  reconcile, resubmit with a new idempotency key. Never blind-retry.
- **Validation rejected:** read the error; check ordinals, closed payload
  keys, size limits, target existence, exact project, owned ref.
- **401/403:** your credential, project grant (exact, case-sensitive), or
  scope is wrong — report it to the maintainer. Never switch projects, refs,
  or identities to route around a denial.
- **Proposal stale:** the protected head moved. Rebase on an owned ref and
  propose again from the current base.

## Hard rules

- Never store credentials, tokens, authorization values, private
  chain-of-thought, or unnecessary personal data in memory content.
- Never claim a proposal is merged because it exists — merged means the
  protected ref advanced, verifiable by anyone.
- Never ask the reviewer to "just approve" — review independence is the
  security property the whole system exists to provide.
