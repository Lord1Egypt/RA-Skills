# Pending completion across a Gateway restart

Use for a required subagent result that is complete but still awaiting delivery
when the Gateway restarts. Keep this optional for unrelated custom builds.
The target is one observed delivery across the tested recovery attempts, not a
universal exactly-once guarantee for every transport or crash window.

## Prepare comparable runs

Pin baseline, candidate, and reproduction identities separately. Inspect existing
owner tests and QA scenarios first; reuse their supported harness and capture
surface when they exercise the required boundary. A test title mentioning
restart is not enough: inspect when completion and delivery actually happen.

Use OCM-owned fixtures with synthetic data and no personal channel credentials.
For Windows/WSL, record both the controlling shell and executing OS/distribution;
resolve paths and OCM in that distribution. Never equate a Windows controller
with native Windows Gateway proof.
For permission-sensitive failures on a mounted Windows drive, compare a native
Linux checkout and preserve both results before attributing a candidate regression.

Define equivalent input, delivery destination, unique marker, and recovery
trigger for both revisions. Use separate fresh fixtures, or independent OCM
copies of a stopped, consistent seed supported by both revisions. Never run the
baseline on candidate-migrated state. Record fixture/snapshot identity and any
migration separately from the behavior verdict.

## Observe the pending boundary

Use a supported deterministic harness barrier to hold delivery after durable
completion is recorded. Record the task/run, intended recipient, completion
identity, authoritative pending state, and receiver count of zero. Do not infer
pending state from a delayed reply, sleeping worker, or service PID.

If the available harness cannot expose this boundary, mark the required runtime
scenario blocked and name the missing control or observation. An owner test
that seeds persisted state and mocks delivery is useful automated evidence;
it does not become real Gateway/channel proof. Do not add production switches,
edit live databases, or copy personal state to manufacture the checkpoint.

## Restart and observe recovery

Inspect installed OCM restart help and record the actual restart mode. Graceful
drain, recovery handoff, and forced process replacement are different experiments.
If the selected mode delivers the result before stopping, the pending-across-
restart precondition was missed; report that attempt as inconclusive.

1. Capture the old Gateway instance and fixture state location at the pending
   barrier. Keep the same fixture through the restart.
2. Restart only that OCM environment. Verify the replacement instance, runtime
   identity, live health, and relevant authenticated API readiness. An in-process
   restart needs lifecycle evidence; a PID alone cannot distinguish generations.
3. Release or re-establish the harness-owned delivery control as its contract
   requires. Observe the persisted completion reach the original destination
   once, with matching content and authoritative delivery settlement. A newly
   spawned post-restart worker does not prove recovery of the pending task.
4. Exercise another supported recovery/reconnect attempt after settlement.
   Keep receiver capture continuous across the restart and count actual delivery
   events; do not deduplicate evidence by text or reset the receiver cursor.
   Check that the original task is not re-executed or its side effect repeated.

Identify each counter's source and scope: accepted recipient records, executed
spawns, planned tool calls, and provider requests are different observations.
Record how capture survives Gateway replacement and any retention/cursor limits.
Export the evidence before teardown can clear receiver or provider state.

Declare the observation window separately from the retry/recovery boundary to
exercise, using the inspected implementation or harness contract. Report which
boundary was actually crossed. Elapsed time alone does not prove a scheduled
retry ran. If only a time-bounded window was observed, say so and name uncovered
retries or crash windows; do not present it as full retry coverage. A required
but unexercised boundary remains a gap. A single matching message at first
arrival cannot exclude later duplicates.

## Record the result

Use the worksheet's conditional restart section; link raw private evidence from
each checkpoint. Sanitize identities and payloads before external publication.

- Baseline fails the target behavior and candidate passes the same reproduction:
  evidence for the fix within that scope.
- Both pass: no reproduced regression; candidate coverage only.
- Candidate loses, duplicates, misroutes, or repeats work: failed behavior check.
- Pending checkpoint, receiver capture, comparable baseline, or required retry
  coverage missing: record the gap; do not claim the fix is validated.

Keep infrastructure smoke, automated owner tests, and fixture runtime results
as separate proof rows. When a required row remains unavailable, report blocked
unless an observed failure already determines the overall result. Derive the
existing report format from the worksheet; no second ledger or schema is needed.
