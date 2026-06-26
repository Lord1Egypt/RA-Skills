---
name: dont-deal-triage
description: Use this skill when a developer or desk worker reports chest pain, chest pressure, left arm or jaw discomfort, shortness of breath, unusual sweating, faintness, or asks for an exhaustion-aware health check that should consider local work patterns from git activity and current host context.
---

# dont-deal-triage

This skill is for conservative, local-first support. It is not a diagnosis skill.

## Workflow

1. Gather local context before reasoning.
   This skill package is self-contained.
   From the skill folder, run `node scripts/index.js` to generate the latest local snapshot.
   If command execution is unavailable, read `~/.dont-deal/snapshot.json` if it already exists.

2. In quick mode, solve only the red vs yellow question.
   Read `references/quick-mode.md`.
   The core output is:
   red = emergency help now
   yellow = urgent medical review today

3. Check for immediate red flags before asking many questions.
   Read `references/emergency-thresholds.md`.
   If the user currently has active chest discomfort plus emergency features, tell them to stop working and seek emergency help now.

4. Use fatigue data as context, not proof.
   Git-derived sleep inference can raise suspicion that the user is under strain.
   It cannot rule heart risk in or out.

5. Keep the conversation short and action-oriented.
   If the user is symptomatic right now, prefer one question at a time.
   Do not ask for long histories before deciding whether the user needs urgent help.

6. Persist only local summaries.
   If the host supports it, store user-provided background history in local JSON only after explicit consent.

7. Keep machine inspection narrow.
   Detect only the current host context.
   Read only the active repository's git timestamps.
   Do not enumerate local apps, mailboxes, camera access, or source-control credentials unless the user explicitly starts that setup flow.

8. Treat bystander use as valid.
   The user may be asking for someone else.
   In that case, keep instructions imperative and focused on calling emergency help, reducing movement, and keeping the person from traveling alone.

9. Prefer the bundled scripts over ad hoc reimplementation.
   Use `scripts/quick-triage-cli.js` for local fast-mode testing.
   Use `scripts/index.js` for the local fatigue and host snapshot.

## Response rules

- Never reassure the user that symptoms are "just stress" or "probably not serious."
- Never tell the user to drive themselves to the hospital when emergency symptoms are active.
- Tell the user to reduce activity immediately if chest pain is ongoing.
- If emergency care is indicated, stop discussing code or work until the user confirms they are safe.
- Treat git activity as a weak fatigue signal, not evidence about the user's exact sleep duration.
- When the information is incomplete but concerning, lean yellow rather than reassuring.
- If the user is not in acute distress, ask about:
  chest discomfort quality, duration, radiation, breathing difficulty, sweating, nausea, faintness, known hypertension, smoking, family history, and whether symptoms occur at rest.

## Output shape

When the host can return structure, prefer:

```json
{
  "urgency": "emergency | urgent | monitor",
  "reasoning_summary": [
    "Current symptoms",
    "Fatigue context",
    "Known risk factors"
  ],
  "recommended_action": "short imperative sentence",
  "follow_up_questions": []
}
```

## Host portability

Keep this skill prompt generic:

- Claude Code can wire this through its own skill surface.
- Codex can invoke the local analyzer directly.
- OpenClaw and ClawHub can distribute this skill as a standalone folder because the runtime scripts are bundled under `scripts/`.

Do not hardcode one host's metadata format into the reasoning instructions.
