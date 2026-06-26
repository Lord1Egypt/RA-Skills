# Escalation Protocols

How the Project Engineer handles dev escalations. Any dev agent (FE, BE, QA) can escalate to the engineer. Escalations are expected workflow — not failures.

---

## Receiving an Escalation

Dev escalations arrive in two places — check both:
1. **`queues/to-engineer.md`** in the project folder — the full written record with all context
2. **`sessions_send` nudge** — signals urgency, but the queue file entry is the source of truth

Always read the queue file entry first. It should contain:

1. **What are you trying to do?** (Which task, which spec section)
2. **What did you try?** (Approach taken, code written)
3. **What broke?** (Error message, unexpected behavior, test failure)
4. **Where are you?** (File path, function name, line number if applicable)

If the queue file entry is incomplete, post to `queues/to-[dev-role].md` asking for the missing pieces before investigating. Do not guess — incomplete context leads to misdirected guidance.

## Investigation Steps

Once you have full context:

1. **Pull their branch** from `workspace/repo/` (via the loaded git skill):
   ```bash
   git fetch origin
   git checkout <their-branch>
   git pull origin <their-branch>
   ```

2. **Read the relevant code** in the file(s) they referenced.

3. **Check `workspace/IMPLEMENTATION_GUIDE.md` first.** Open the relevant spec section (FE-XXX, BE-XXX, etc.) and verify what the spec says this component/endpoint/feature should do.

4. **Check `KNOWN_ISSUES.md`.** Is the behavior they're describing an accepted limitation? If so, point them to the entry — it's not a bug, it's not your problem to solve now.

5. **Compare the dev's code to the spec.** The answer falls into one of three categories:

### Category A: Spec is Clear, Dev is Off-Track

The spec clearly defines the expected behavior and the dev has deviated from it.

**Response:**
- Point the dev back to the specific spec section by ID.
- Quote the relevant spec guidance.
- Show them where their code diverges.
- Suggest the specific change needed to align with the spec.

**Tone:** Helpful and direct. "The spec at BE-003 defines this endpoint as returning paginated results. Your current implementation returns all records — here's how to add pagination..."

### Category B: Spec is Ambiguous or Has a Gap

The dev's question reveals something the spec doesn't clearly cover.

**Response:**
- Provide the technical guidance the dev needs to proceed.
- Document the clarification as a spec update — add it to the Implementation Plan so future questions are covered.
- Note the update in the Change Log section of the Implementation Plan.

**Tone:** Collaborative. "Good question — the spec doesn't cover this case explicitly. Here's how it should work: [guidance]. I'm updating the Implementation Plan to cover this."

### Category C: Solution Requires a Spec Deviation

The dev's situation reveals that the spec's approach won't work, or a better approach exists that contradicts the current plan.

**Response:**
- Do NOT advise the dev to deviate without PM awareness.
- Flag to PM first: "Investigating [dev]'s escalation on [task]. The current spec at [ID] defines [approach], but [reason it won't work / reason alternative is better]. Proposing to change the approach to [new approach]. Awaiting PM acknowledgment before advising the dev."
- Once PM acknowledges, advise the dev and update the spec.

**Tone:** Transparent. "I see the issue. The spec's approach won't work here because [reason]. I'm flagging this to the PM as a spec change before we proceed — I'll get back to you shortly."

## Common Escalation Types

### "I don't understand the spec"

This is a Category B situation — the spec isn't clear enough. Re-explain the spec section in plainer terms, provide a code-level example, and update the spec to be clearer.

### "I'm getting an error I can't resolve"

Pull the branch (via the loaded git skill), reproduce the context, and diagnose:
- Is it a syntax/runtime error? → Point to the specific code issue.
- Is it a logic error? → Trace the data flow and identify where it diverges from expected.
- Is it an environment/config issue? → Ask the dev to verify their local dependencies, environment variable configuration, and database connection state. The engineer does not access env vars or databases directly — have the dev report the relevant values (without sharing secrets in chat).
- Is it a third-party issue? → Ask the dev to check API docs, rate limits, and auth status for the external service.

### "The spec says X but the existing code does Y"

For projects modifying existing code, this is common. Investigate:
- If the existing code is correct and the spec missed it → Update the spec (Category B).
- If the existing code is wrong/outdated and the spec is correct → Dev should implement per spec and note what they're replacing.
- If both have valid approaches → Engineer makes the call, updates spec, documents rationale.

### "QA says my PR has issues but I disagree"

This is a tiebreaker situation:
1. Review the PR against the Implementation Plan.
2. Review QA's concern against the QA Coverage Plan.
3. If spec supports QA → Dev must address it.
4. If spec is silent → Engineer decides and updates spec.
5. If it's a scope/requirements question → Escalate to PM.

### "I'm blocked by another dev's work"

Check the dependency map in the Implementation Plan:
- If the dependency is correctly documented → Communicate the status to both devs and the PM. The blocked dev should work on non-dependent tasks.
- If the dependency wasn't documented → Add it to the plan, notify the PM so Asana tasks reflect the dependency.

## Response Standards

Every escalation response must:
- Reference the specific `IMPLEMENTATION_GUIDE.md` section by ID
- Be actionable (the dev should know exactly what to do next)
- Be tempered and non-judgmental (escalations are normal workflow)
- Include a code example or diff when applicable
- Note any spec updates made as a result of the escalation

**Deliver responses via `queues/to-[dev-role].md`** using the standard queue message format. Also send a `sessions_send` nudge to the dev so they know a response is waiting. Mark the original entry in `queues/to-engineer.md` as `[READ]` after responding.

If the implementation guide was updated as a result of the escalation, also post to `queues/to-pm.md` noting the section that changed.

Every escalation response must NOT:
- Critique the dev for asking
- Freelance a solution that contradicts `IMPLEMENTATION_GUIDE.md` (without PM flagging)
- Provide vague guidance ("try something like...")
- Ignore the root cause in favor of a quick fix
