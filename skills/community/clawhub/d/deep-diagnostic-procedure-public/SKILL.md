---
name: "deep-diagnostic-procedure-public"
description: "Systematic 6-layer diagnostic framework for OpenClaw issues: policy, config, runtime, logs, network, code."
---

# Deep Diagnostic Procedure for OpenClaw Issues

## When to Use
- A tool, channel, or feature isn't working as expected
- Symptoms persist after "obvious" fixes
- You're tempted to blame an external component without evidence
- You've restarted the gateway more than twice and the problem persists

## Core Principles

1. **Don't conclude from first impression.** "It's probably X" is a hypothesis, not a diagnosis.
2. **Investigate in layers**, from closest to the problem to farthest.
3. **Evidence, not assumptions.** Every hypothesis must be verified with logs, config, or code.
4. **One real cause** is more likely than three coincidental ones.
5. **Policy before plumbing.** Permission/config issues cause more outages than network bugs.

## Investigation Layers (In Order)

### Layer 1 — Policy & Permissions (MOST OVERLOOKED)
- [ ] What does `tools.profile` remove? Check with `openclaw config get tools.profile`
- [ ] Are the required tools in the allowed list or blocked?
- [ ] Channel-specific policies: `dmScope`, `allowFrom`, `groupPolicy`
- [ ] Cross-context restrictions (e.g., messaging across channels denied)
- [ ] Exec security, host approvals, elevated permissions

**Key question:** "Does the agent actually HAVE ACCESS to the tool/channel it needs?"

> 💡 **Real-world lesson:** Weeks spent debugging outbound message delivery. Root cause? `tools.profile` silently removed the `message` tool from the agent's session. The agent literally couldn't send — nothing to do with the external library, DNS, or connection.

### Layer 2 — Configuration
- [ ] Is the config correct in `openclaw.json`? Verify with `openclaw config get <path>`
- [ ] Empty values, missing keys, or defaults that should be explicit?
- [ ] Format correctness (e.g., phone numbers with/without `+`)
- [ ] Plugins and skills enabled correctly?

**Key question:** "Is it configured the way it should be, not the way I assume it is?"

### Layer 3 — Runtime & State
- [ ] Is the gateway running? `openclaw gateway status`
- [ ] Are channels connected? `openclaw channels status --probe`
- [ ] Is there an active listener for the target channel?
- [ ] Are sessions active and routed correctly?
- [ ] Are tokens/credentials valid?

**Key question:** "Is everything actually running and connected RIGHT NOW?"

### Layer 4 — Logs & Errors
- [ ] Run `openclaw logs --follow` while reproducing the issue
- [ ] Enable verbose logging temporarily
- [ ] Capture the EXACT error message (not a summary)
- [ ] Note the timeline: when does the error appear relative to the action?

**Key question:** "What is the system TELLING US is wrong?"

### Layer 5 — Network & External Services
- [ ] Does DNS resolve? (Only if symptoms point to network)
- [ ] Can you reach external services (Ollama, Groq, GitHub, etc.)?
- [ ] Firewall or proxy blocking?
- [ ] Latency or timeout issues?

**Key question:** "Is the problem OUTSIDE of OpenClaw?"

### Layer 6 — Code & Plugin Internals
- [ ] Audit the plugin code (trace the data flow)
- [ ] Map the full path: input → processing → output
- [ ] Look for silent failure points (try/catch that swallows errors)
- [ ] Check plugin version compatibility with OpenClaw version

**Key question:** "Where exactly in the code does the flow stop?"

## Execution Procedure

```
1. Write down the precise symptom: "When I do X, Y happens instead of Z"
2. Layers 1-3: Quick verification (target: 10 minutes total)
3. Layer 4: Enable logs, reproduce the problem, capture errors
4. Form primary hypothesis → verify with evidence
5. If hypothesis doesn't confirm → move to next layer
6. Layers 5-6 only if 1-4 reveal nothing
7. Document: CAUSE → EVIDENCE → SOLUTION
```

## Anti-Patterns (WHAT NOT TO DO)

- ❌ "It's probably [external component]" without evidence
- ❌ Restarting as diagnosis (hides the problem, doesn't fix it)
- ❌ "I've seen this before" without verifying it's the same cause
- ❌ Investigating only one layer (e.g., only network)
- ❌ Concluding before checking policy & permissions
- ❌ Blaming the external component before checking internal config

## Report Template

```markdown
## Diagnostic: [Issue title]
**Symptom:** [Precise description]
**Initial hypothesis:** [What I thought first]
**Actual cause:** [What I found]
**Evidence:** [Log/config/code that confirms]
**Layers investigated:** [Which layers, in what order]
**Solution:** [What fixed it]
**Time wasted on wrong hypotheses:** [Estimate]
**Lesson:** [What to remember for next time]
```

## Historical Cases

### Case 1: Silent tool removal by tools.profile
- **Symptom:** Agent couldn't send messages to an external channel from another channel
- **Initial hypothesis:** External library bug, DNS issues, disconnection
- **Actual cause:** `tools.profile` setting silently removed the `message` tool from the agent session
- **Evidence:** Logs showed `tool policy removed N tool(s) via tools.profile: ...message...`
- **Layers investigated:** 6 (code) → 1 (policy) — WRONG ORDER, started from the end
- **Solution:** Changed `tools.profile` to include the `message` tool
- **Time wasted:** Weeks (chasing DNS, re-linking, blaming external library)
- **Lesson:** ALWAYS check policy & permissions FIRST. It's the most overlooked layer and the most common cause of "silent" failures.
