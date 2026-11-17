---
name: autonomous-handoff
description: "Use clawhandoff to hand work to an OpenClaw Gateway, an existing browser chat, an A2A agent, Codex app-server, or an ACP coding agent, answer objections with commit-bound evidence, and reconcile Git/PR state before publication."
---

# Run an autonomous handoff

The local assistant owns the user's task. It runs authorized local checks, interprets the target agent's response, and calls the next MCP tool. The bridge persists each turn and verifies Git and PR facts across all five transports (`gateway`, `browser`, `a2a`, `codex`, and `acp`). Read the skill before starting, or use the client's `autonomous-handoff` MCP prompt with `targetId` and `goal`. Registering the server alone does not start this loop.

## Start and retain the handoff

1. Choose the configured `targetId` and call `bridge_preflight`. For a browser target, check `browserReady` and keep the exact chat open in one Chrome tab with an empty composer. For Gateway, A2A, Codex, or ACP targets, check `targetHealthy` and `authReady` (plus `agentCard` on A2A). Gateway, Codex, and ACP handoffs support passing `worktreeName` on `bridge_handoff_start` to run inside an isolated Git worktree without touching dirty files in the primary checkout.
2. Resolve the PR base and any source ref to 40-character Git commit SHAs. Give the task a unique, stable `requestId` and concrete `acceptanceCriteria`. For Git verification, supply a repository the bridge can read through `localRepoPath` or `remoteUrlOrPath`. Use `pinnedSourceCommitSha` to identify tested work. Use `expectedTreeSha` for an immutable tree and `lockedPaths` for files or directories that must stay unchanged after the source commit.
3. `publisherOwner` defaults to `"remote_gated"` (or the bridge config's `defaultPublisherOwner`) when omitted, using a two-stage managed remote publication under the remote agent's identity. Include any contributor `Co-authored-by:` trailer instruction in Stage 1 before Stage 2 locks the exact commit SHA. Pass `"none"` when no publication is requested, or `"local"` only when the user or config explicitly selects local publication. Set `allowManagedPublishStage: false` on every initial request. Requested capabilities are instructions to Robo. For an enforced local-only publication boundary, use `"local"` and a remote worker without publication credentials. Changing publishers requires the user's authority.
4. Call `bridge_handoff_start` with the target and envelope. Save the returned `handoffId` for all later calls. If the initial response is lost before you receive the ID, retry the same initial request with the same `requestId` and data directory. Reusing an ID reattaches to the existing handoff.

## Act on the returned directive

| `orchestratorDirective.action` | Local assistant's action |
| --- | --- |
| `POLL_ATTACH` | Call `bridge_handoff_attach` with the saved `handoffId`. An expired wait budget ends the wait only. |
| `CONTINUE_AUTONOMOUSLY` | Check the objection against source and evidence. Use `bridge_handoff_continue` with `intent: "counter_evidence_or_followup"`, a `message` and relevant `evidenceRefs` to advance the same handoff. |
| `AUTHORIZE_REMOTE_PUBLISH` | If the user authorized publication, call `bridge_handoff_continue` with `intent: "authorize_publish"` and a `message` for the verified candidate. The bridge checks the ref and PR state again immediately before sending the authorization. Submit changed Git coordinates in a separate evidence turn first. |
| `PUBLISH_LOCALLY` | Within the user's authority, publish the exact verified commit through the local owner. Verify the open PR's head and intended base branch. |
| `COMPLETE` | Check the user's acceptance criteria before reporting success. For example, a verified open PR can still have failing CI. |
| `ESCALATE_TO_HUMAN` | Inspect `orchestratorDirective.reason`, any `reported.blockers`, and `observed.verificationNotes`. Explain the remaining access, recovery, or scope decision. |

**When Robo asks for proof.** Check which commit the existing log or test artifact covers. If evidence is missing, run the authorized check in isolation. Return a specific `claim` and a stable `sourceRef` such as a CI job or artifact URL together with the tested commit in the claim. Rewording an old reference does not count as new evidence. If the fix changes the candidate, submit `updatedSourceCommitSha` and its reachable `updatedSourceRemoteRef` (plus `updatedLocalRepoPath` if you created a local clone or worktree mid-handoff) within the user's existing push authority. An explicitly supplied `updatedExpectedTreeSha` must match that new source commit.

**When a candidate becomes reachable.** For a settled or failed turn, call `bridge_verify_git` with its `handoffId` and `candidateRef` to refresh the Git and PR observations. Supply `remoteUrlOrPath` if the handoff has no repository locator, then follow the returned directive.

**When Git verification fails.** Inspect `violatedPaths`, base ancestry, and any tree mismatch. A later commit that reverts a locked file still leaves the offending commit in the checked history. If an authorized correction is possible, prepare a clean candidate from the pinned source and submit it for verification. Preserve other work and obtain authority before altering any shared branch or changing the contract.

**When delivery is uncertain.** Use the recorded `handoffId` and inspect the original session. A browser reply belongs to the current `Bridge-Reply` marker and ends in a flush-left fenced `handoff-result` block. A saved intent can still be waiting for Chrome permission or the connection to return. Recover using `bridge_handoff_attach` (which reconciles Gateway history, browser turn markers, A2A `ListTasks` message IDs, or Codex `thread/read` `clientUserMessageId` records without duplicate dispatch). For `AUTH_LOGIN_REQUIRED`, surface the operator action in the tool error's `remediation`. `bridge_handoff_abort` cancels active Gateway runs, A2A tasks (`CancelTask`), Codex turns (`turn/interrupt`), or ACP prompts (`session/cancel`); for a browser handoff (or local abandonment after inspection), `bridge_handoff_abort(localOnly=true)` closes local tracking while leaving the remote conversation untouched.

Treat `reported` as the agent's account and `observed` as the bridge's Git/PR inspection. Verify test results at the cited evidence source yourself. If a prior publication is uncertain, reconcile the existing PR before attempting another publication. Honor the selected publisher and the turn budget. If the same blocker appears on two consecutive turns without a new observed commit or a new evidence reference, or if the turn budget runs out, report the verified work and the outstanding decision.
